"""
Monthly script: uses Claude with web search to find upcoming congress editions
and updates _data/events.yml in place.
"""

import json
import os
import re
import sys
from datetime import date, datetime, timezone

import anthropic
import yaml

REPO_ROOT = os.environ.get("GITHUB_WORKSPACE") or os.path.join(os.path.dirname(__file__), "..", "..")
EVENTS_FILE = os.path.join(REPO_ROOT, "_data", "events.yml")

SEARCH_PROMPT = """\
You are helping maintain a list of upcoming academic congresses in probability
and mathematical finance for a researcher's personal website.

Today is {today}.

For each congress below, search the web to find the next upcoming edition
(the one that hasn't happened yet, or is currently ongoing).
Return ONLY a JSON object — no markdown, no prose — with this exact structure:

{{
  "<congress_id>": {{
    "year": "<year as string, or empty string if unknown>",
    "dates_start": "<YYYY-MM-DD or empty string>",
    "dates_end": "<YYYY-MM-DD or empty string>",
    "location": "<City, Country or empty string>",
    "abstract_deadline": "<YYYY-MM-DD or empty string>",
    "registration_deadline": "<YYYY-MM-DD or empty string>",
    "edition_website": "<URL or empty string>",
    "notes": "<short note if anything important, otherwise empty string>"
  }},
  ...
}}

Congresses to search for:

{congresses}

Rules:
- Only include congresses listed above. Do not invent new ones.
- Dates must be in YYYY-MM-DD format or empty string "".
- If a deadline has already passed, leave it as "".
- If you cannot find reliable information, leave all fields as empty strings.
- Do not guess; only output what you find from actual search results.
"""


def load_events() -> dict:
    with open(EVENTS_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_events(data: dict) -> None:
    with open(EVENTS_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)


SEARCH_HINTS = {
    "bachelier": (
        "Check bachelier-finance.org and bacheliercongress.com. "
        "It is held every two years."
    ),
    "seio": (
        "Check seio.es. It is held every two years. "
        "Also check for any announced future congress on that site."
    ),
    "iwspa": (
        "Check sites.google.com/view/iwspa2026/home for the 2026 edition. "
        "URL pattern for past editions: sites.google.com/view/iwspa{year}-gt-seio or "
        "sites.google.com/view/iwspa{year}. "
        "It is also sometimes announced on seio.es. "
        "Find dates, location, and any submission deadlines."
    ),
    "clapem": (
        "Check clapem.org and ime.usp.br/~slapem/ (the SLAPEM society website). "
        "The XVII edition was held March 2-6, 2026 in Montevideo — that has passed. "
        "Look for any announcement of the XVIII edition (next one, expected around 2029). "
        "If not announced, leave all date fields empty but note it in 'notes'."
    ),
}


def build_congress_description(congresses: list) -> str:
    lines = []
    for c in congresses:
        hint = SEARCH_HINTS.get(c["id"], "")
        line = (
            f"- id: {c['id']}, name: {c['name']}, "
            f"website: {c.get('website', '')}"
        )
        if hint:
            line += f"\n  search hint: {hint}"
        lines.append(line)
    return "\n".join(lines)


def extract_json(text: str) -> dict:
    """Extract the first JSON object from Claude's response."""
    # Strip markdown code fences if present
    text = re.sub(r"^```[a-z]*\n?", "", text.strip(), flags=re.MULTILINE)
    text = re.sub(r"\n?```$", "", text.strip(), flags=re.MULTILINE)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in response")
    return json.loads(match.group(0))


def run() -> None:
    data = load_events()
    congresses = data.get("congresses", [])

    client = anthropic.Anthropic()

    congress_desc = build_congress_description(congresses)
    prompt = SEARCH_PROMPT.format(
        today=date.today().isoformat(),
        congresses=congress_desc,
    )

    print("Querying Claude for upcoming congress dates…")

    try:
        response = client.beta.messages.create(
            model="claude-opus-4-7",
            max_tokens=4096,
            tools=[
                {
                    "type": "web_search_20250305",
                    "name": "web_search",
                    "max_uses": 12,
                }
            ],
            betas=["web-search-2025-03-05"],
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:
        print(f"API call failed: {exc}")
        sys.exit(1)

    print(f"Stop reason: {response.stop_reason}")
    print(f"Response blocks: {[type(b).__name__ for b in response.content]}")

    # Extract the final text block from the response
    result_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            result_text += block.text

    if not result_text.strip():
        print("No text response from Claude — skipping update.")
        sys.exit(0)

    print("Claude response received. Parsing JSON…")

    try:
        updates = extract_json(result_text)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"Failed to parse JSON: {exc}")
        print("Raw response:\n", result_text)
        sys.exit(1)

    # Apply updates to each congress
    changed = False
    for congress in congresses:
        cid = congress["id"]
        if cid not in updates:
            print(f"  {cid}: no update from Claude")
            continue

        new_data = updates[cid]
        old_edition = congress.get("next_edition", {})

        for field in [
            "year",
            "dates_start",
            "dates_end",
            "location",
            "abstract_deadline",
            "registration_deadline",
            "edition_website",
            "notes",
        ]:
            val = new_data.get(field, "")
            if val and val != old_edition.get(field, ""):
                print(f"  {cid}.{field}: {old_edition.get(field, '')!r} → {val!r}")
                congress["next_edition"][field] = val
                changed = True

    if not changed:
        print("No changes detected.")
    else:
        data["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        save_events(data)
        print(f"Saved updated events to {EVENTS_FILE}")


if __name__ == "__main__":
    run()
