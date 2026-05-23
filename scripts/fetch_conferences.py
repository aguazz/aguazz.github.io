#!/usr/bin/env python3
"""
Weekly academic event discovery for aguazz.github.io.

Sources searched:
  - researchseminars.org  (free JSON API, seminars & workshops)
  - WikiCFP               (free RSS, conferences call-for-papers)
  - Tavily Search API     (web search, catches everything else)

Claude ranks each candidate for relevance to the research profile below.
Events scoring < 6 are dropped before the PR is opened.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import anthropic
import feedparser
import requests
import yaml

# ---------------------------------------------------------------------------
# Research profile — edit this section to update the bot's search focus
# ---------------------------------------------------------------------------

RESEARCH_PROFILE = """
Abel Azze is an Associate Professor at CUNEF Universidad (Madrid, Spain).
Research areas:
  - Optimal stopping theory (free boundary problems, smooth-fit, variational approach)
  - Stochastic control (impulse control, singular control, classical control)
  - Stochastic differential equations (SDEs, Lévy processes)
  - Mathematical finance (option pricing, optimal execution, contract theory)
  - Operations research and dynamic programming
  - Probability theory and stochastic processes
"""

SEARCH_KEYWORDS = [
    "optimal stopping",
    "stochastic control",
    "impulse control",
    "singular control",
    "free boundary",
    "stochastic processes",
    "mathematical finance",
    "dynamic programming",
    "probability theory",
]

# WikiCFP query terms (space-encoded as +)
WIKICFP_TERMS = [
    "stochastic",
    "optimal+stopping",
    "mathematical+finance",
    "operations+research",
    "probability",
]

# Tavily natural-language queries
TAVILY_QUERIES = [
    "upcoming conference optimal stopping stochastic control 2025 2026",
    "workshop stochastic processes free boundary problems 2025 2026",
    "summer school stochastic control mathematical finance 2025 2026",
    "seminar series optimal stopping probability theory 2025",
    "conference impulse control dynamic programming operations research 2025 2026",
]

DATA_FILE = Path("_data/conferences.yml")
RELEVANCE_THRESHOLD = 6
CLAUDE_MODEL = "claude-opus-4-7"
CLAUDE_BATCH_SIZE = 30  # candidates per API call

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_existing() -> list[dict]:
    if DATA_FILE.exists():
        with open(DATA_FILE, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, list) else []
    return []


def known_urls(events: list[dict]) -> set[str]:
    return {e["url"] for e in events if e.get("url")}


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text or "").strip()


# ---------------------------------------------------------------------------
# Source 1: researchseminars.org
# ---------------------------------------------------------------------------


def search_researchseminars() -> list[dict]:
    candidates = []
    base = "https://researchseminars.org/api/0/search/seminars"
    for kw in ["optimal stopping", "stochastic control", "mathematical finance"]:
        try:
            r = requests.get(base, params={"keywords": kw}, timeout=20)
            if not r.ok:
                continue
            for s in r.json().get("results", []):
                name = s.get("name", "").strip()
                shortname = s.get("shortname", "")
                if not name or not shortname:
                    continue
                candidates.append(
                    {
                        "name": name,
                        "url": f"https://researchseminars.org/{shortname}",
                        "type": "seminar",
                        "raw": strip_html(s.get("description", "")),
                    }
                )
        except Exception as exc:
            print(f"[researchseminars] '{kw}': {exc}", file=sys.stderr)
    return candidates


# ---------------------------------------------------------------------------
# Source 2: WikiCFP RSS
# ---------------------------------------------------------------------------


def search_wikicfp() -> list[dict]:
    candidates = []
    for term in WIKICFP_TERMS:
        url = f"http://www.wikicfp.com/cfp/rss?q={term}"
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                candidates.append(
                    {
                        "name": entry.get("title", "").strip(),
                        "url": entry.get("link", "").strip(),
                        "type": "conference",
                        "raw": strip_html(entry.get("summary", "")),
                    }
                )
        except Exception as exc:
            print(f"[WikiCFP] '{term}': {exc}", file=sys.stderr)
    return candidates


# ---------------------------------------------------------------------------
# Source 3: Tavily web search
# ---------------------------------------------------------------------------


def search_tavily(api_key: str) -> list[dict]:
    from tavily import TavilyClient

    client = TavilyClient(api_key=api_key)
    candidates = []
    for query in TAVILY_QUERIES:
        try:
            results = client.search(query, max_results=6, search_depth="basic")
            for r in results.get("results", []):
                candidates.append(
                    {
                        "name": r.get("title", "").strip(),
                        "url": r.get("url", "").strip(),
                        "type": "conference",
                        "raw": r.get("content", "")[:600],
                    }
                )
        except Exception as exc:
            print(f"[Tavily] '{query}': {exc}", file=sys.stderr)
    return candidates


# ---------------------------------------------------------------------------
# Claude scoring
# ---------------------------------------------------------------------------


def score_batch(client: anthropic.Anthropic, batch: list[dict]) -> list[dict]:
    today = datetime.now().strftime("%Y-%m-%d")
    prompt = f"""You are helping Abel Azze (Associate Professor, CUNEF Universidad) find relevant academic events.

Research profile:
{RESEARCH_PROFILE}

Today: {today}

Below is a list of candidate events. For each, output a JSON array where every element has:
  "index"     : integer (original 0-based index in the list below)
  "relevance" : integer 1–10 (10 = core topic, 1 = irrelevant)
  "type"      : one of "conference", "workshop", "summer_school", "seminar"
  "name"      : clean event name (remove HTML artifacts, fix encoding)
  "date"      : start date as "YYYY-MM-DD", or null
  "deadline"  : abstract/paper submission deadline as "YYYY-MM-DD", or null
  "location"  : "City, Country" or "Online" or null
  "notes"     : one sentence on relevance (null if score < {RELEVANCE_THRESHOLD})

Rules:
- Drop events with relevance < {RELEVANCE_THRESHOLD} (still include them in the array with the low score so they can be filtered).
- Drop events that are clearly past (end date before today) or are commercial/non-academic.
- Be strict: a general computer-science or engineering conference with no stochastic/probability track scores ≤ 3.

Candidates:
{json.dumps(
    [
        {
            "index": i,
            "name": c["name"],
            "url": c["url"],
            "description": c["raw"][:400],
        }
        for i, c in enumerate(batch)
    ],
    indent=2,
    ensure_ascii=False,
)}

Respond with ONLY a valid JSON array. No markdown, no explanation."""

    msg = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = msg.content[0].text.strip()
    # Strip markdown code fences if Claude added them
    raw = re.sub(r"^```[a-z]*\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    scored_items = json.loads(raw)
    today_dt = datetime.strptime(today, "%Y-%m-%d")

    results = []
    for item in scored_items:
        if item.get("relevance", 0) < RELEVANCE_THRESHOLD:
            continue
        # Skip events whose date is clearly in the past
        raw_date = item.get("date")
        if raw_date:
            try:
                if datetime.strptime(raw_date, "%Y-%m-%d") < today_dt:
                    continue
            except ValueError:
                pass

        idx = item["index"]
        original = batch[idx]
        results.append(
            {
                "name": item.get("name") or original["name"],
                "url": original["url"],
                "type": item.get("type", original.get("type", "conference")),
                "date": item.get("date"),
                "deadline": item.get("deadline"),
                "location": item.get("location"),
                "relevance": item["relevance"],
                "notes": item.get("notes"),
                "added": today,
            }
        )
    return results


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------


def deduplicate(candidates: list[dict], seen: set[str]) -> list[dict]:
    fresh = []
    for c in candidates:
        url = c.get("url", "").rstrip("/")
        if url and url not in seen:
            seen.add(url)
            fresh.append(c)
    return fresh


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    existing = load_existing()
    seen = {u.rstrip("/") for u in known_urls(existing)}

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_key:
        print("ANTHROPIC_API_KEY not set — aborting.", file=sys.stderr)
        sys.exit(1)

    claude = anthropic.Anthropic(api_key=anthropic_key)

    # Gather from all sources
    candidates: list[dict] = []
    print("Searching researchseminars.org …")
    candidates.extend(search_researchseminars())

    print("Searching WikiCFP …")
    candidates.extend(search_wikicfp())

    tavily_key = os.environ.get("TAVILY_API_KEY")
    if tavily_key:
        print("Searching web via Tavily …")
        candidates.extend(search_tavily(tavily_key))
    else:
        print("TAVILY_API_KEY not set — skipping web search.")

    print(f"Raw candidates: {len(candidates)}")

    # Remove already-known URLs before sending to Claude (saves cost)
    fresh = deduplicate(candidates, seen)
    print(f"New candidates (after dedup): {len(fresh)}")

    if not fresh:
        print("Nothing new found. Exiting.")
        return

    # Score in batches
    scored: list[dict] = []
    for i in range(0, len(fresh), CLAUDE_BATCH_SIZE):
        batch = fresh[i : i + CLAUDE_BATCH_SIZE]
        print(f"Scoring batch {i // CLAUDE_BATCH_SIZE + 1} ({len(batch)} items) …")
        try:
            scored.extend(score_batch(claude, batch))
        except Exception as exc:
            print(f"Claude error on batch {i}: {exc}", file=sys.stderr)

    print(f"Passed relevance filter: {len(scored)}")

    if not scored:
        print("No events passed the relevance filter. Exiting.")
        return

    # Merge: keep existing (user-approved) entries, append new ones
    merged = existing + scored

    # Sort: events with a date first (ascending), undated last, then by relevance desc
    def sort_key(e: dict):
        d = e.get("date") or "9999-99-99"
        r = -(e.get("relevance") or 0)
        return (d, r)

    merged.sort(key=sort_key)

    # Write
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        # Preserve the header comment
        f.write(
            "# Academic events relevant to optimal stopping, stochastic control, and related areas.\n"
            "# Auto-updated weekly. Edit via Pull Request on GitHub.\n\n"
        )
        yaml.dump(
            merged,
            f,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
            width=120,
        )

    print(f"Written {len(merged)} events to {DATA_FILE} ({len(scored)} new).")


if __name__ == "__main__":
    main()
