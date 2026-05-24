#!/usr/bin/env python3
"""Processes _updates/update.yml and updates the Jekyll academic site.

Publications → appended to _bibliography/papers.bib
Talks        → new Markdown files created in _talks/
Attachments  → moved from _updates/attachments/ to assets/pdf/talks/
CV .tex      → updated via Claude API  (requires ANTHROPIC_API_KEY secret)
Form         → archived to _updates/processed/<timestamp>_update.yml
"""

import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parent.parent

BIB_FILE       = REPO / "_bibliography" / "papers.bib"
TALKS_DIR      = REPO / "_talks"
CV_TEX         = REPO / "assets" / "pdf" / "CV_AbelGuadaAzze.tex"
ATTACHMENTS    = REPO / "_updates" / "attachments"
TALKS_ASSETS   = REPO / "assets" / "pdf" / "talks"
PROCESSED      = REPO / "_updates" / "processed"
UPDATE_FORM    = REPO / "_updates" / "update.yml"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(text: str, max_len: int = 40) -> str:
    s = text.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")[:max_len]


def bib_key(authors: str, year: int, title: str) -> str:
    first = authors.split(" and ")[0].strip()
    last = first.split(",")[0].strip() if "," in first else first.split()[-1]
    last = re.sub(r"[^a-z]", "", last.lower())

    stopwords = {"a", "an", "the", "of", "on", "in", "for", "and", "or",
                 "with", "optimal", "some", "new"}
    words = re.sub(r"[^a-z\s]", "", title.lower()).split()
    word = next((w for w in words if w not in stopwords), words[0] if words else "paper")

    return f"{last}{year}{word}"


# ---------------------------------------------------------------------------
# Publications → papers.bib
# ---------------------------------------------------------------------------

def make_bib_entry(pub: dict) -> str:
    ptype = str(pub.get("type", "article")).lower()
    bib_type_map = {
        "article":       "article",
        "inproceedings": "inproceedings",
        "preprint":      "misc",
        "working":       "misc",
    }
    bib_type = bib_type_map.get(ptype, "article")
    key = bib_key(str(pub["authors"]), int(pub["year"]), str(pub["title"]))

    def field(name: str, val: str) -> str:
        return f"  {name:<12} = {{{val}}},"

    lines = [
        f"@{bib_type}{{{key},",
        field("bibtex_show", "true"),
        field("title",  "{" + str(pub["title"]) + "}"),
        field("author", str(pub["authors"])),
    ]

    if bib_type == "article":
        lines.append(field("journal",   str(pub.get("journal", ""))))
    elif bib_type == "inproceedings":
        lines.append(field("booktitle", str(pub.get("journal", ""))))
    elif pub.get("journal"):
        lines.append(field("howpublished", str(pub["journal"])))

    lines.append(field("year", str(pub["year"])))

    for opt in ["volume", "number", "pages"]:
        if pub.get(opt):
            lines.append(field(opt, str(pub[opt])))

    if pub.get("doi"):
        lines.append(field("doi",  str(pub["doi"])))
        lines.append(field("html", f"https://doi.org/{pub['doi']}"))
    if pub.get("arxiv"):
        lines.append(field("arxiv", str(pub["arxiv"])))
    if pub.get("abstract"):
        lines.append(field("abstract", str(pub["abstract"]).strip()))
    if pub.get("selected"):
        lines.append(field("selected", "true"))

    lines.append("}")
    return "\n".join(lines)


def process_publications(pubs: list) -> None:
    print(f"\nPublications ({len(pubs)}):")
    entries = [make_bib_entry(p) for p in pubs]
    existing = BIB_FILE.read_text(encoding="utf-8")
    BIB_FILE.write_text(
        existing.rstrip() + "\n\n" + "\n\n".join(entries) + "\n",
        encoding="utf-8",
    )
    for p in pubs:
        print(f"  + [{p.get('type', 'article')}] {str(p['title'])[:70]}")


# ---------------------------------------------------------------------------
# Talks → _talks/*.md
# ---------------------------------------------------------------------------

TYPE_DISPLAY = {
    "talk":         "Talk",
    "invited talk": "Invited Talk",
    "seminar":      "Seminar",
    "poster":       "Poster",
}


def make_talk_file(talk: dict) -> tuple:
    date  = str(talk["date"])
    tslug = slugify(str(talk["title"]), 30)
    vslug = slugify(str(talk.get("venue", "")), 20)
    fname = f"{date}-{tslug}-{vslug}.md"

    talk_type = TYPE_DISPLAY.get(
        str(talk.get("type", "Talk")).lower(),
        str(talk.get("type", "Talk")),
    )

    slides = ""
    if talk.get("slides"):
        slides = f"/assets/pdf/talks/{talk['slides']}"

    front = {
        "title":      str(talk["title"]),
        "collection": "talks",
        "type":       talk_type,
        "permalink":  f"/talks/{date}-{tslug}-{vslug}",
        "venue":      str(talk.get("venue", "")),
        "date":       date,
        "location":   str(talk.get("location", "")),
        "slides":     slides,
    }
    header = "---\n" + yaml.dump(front, allow_unicode=True, default_flow_style=False) + "---\n"
    body = f"\nWith {talk['coauthors']}.\n" if talk.get("coauthors") else "\n"

    return fname, header + body


def process_talks(talks: list) -> None:
    print(f"\nTalks ({len(talks)}):")
    TALKS_ASSETS.mkdir(parents=True, exist_ok=True)

    for talk in talks:
        if talk.get("slides"):
            src = ATTACHMENTS / str(talk["slides"])
            dst = TALKS_ASSETS / str(talk["slides"])
            if src.exists():
                shutil.move(str(src), str(dst))
                print(f"  Moved {talk['slides']} → assets/pdf/talks/")
            else:
                print(f"  Warning: '{talk['slides']}' not found in _updates/attachments/ — skipping.")

        fname, content = make_talk_file(talk)
        (TALKS_DIR / fname).write_text(content, encoding="utf-8")
        print(f"  + {fname}")


# ---------------------------------------------------------------------------
# CV .tex update via Claude API
# ---------------------------------------------------------------------------

# Format examples taken directly from the CV so Claude matches the style exactly.
CV_FORMAT_EXAMPLES = """
Working paper:
  \\cvitem{2025}{Azze A, D'Auria B. Title. arXiv. \\url{https://doi.org/...}}

Refereed paper:
  \\cvitem{2025}{Azze A, D'Auria B, García-Portugués E. Title. Journal Name. YEAR;VOL(NO):PAGES. \\url{https://doi.org/...}}

Seminar (section: "Seminar contributions (speaker underlined)"):
  \\cventry{DD/MM/YYYY}{``Title''}{Event name}{Venue}{\\underline{Abel Azze}, Coauthor}{}

Invited talk (subsection "Invited talks" under "Conference contributions"):
  \\cventry{DD/MM/YYYY DD/MM/YYYY}{``Title''}{Conference name}{Location}{\\underline{Abel Azze}, Coauthor}{}

Contributed talk (subsection "Contributed talks"):
  same format as invited talk

Poster (subsection "Posters"):
  same format as invited talk
"""


def update_cv(pubs: list, talks: list) -> None:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\nCV .tex: skipped (ANTHROPIC_API_KEY not set).")
        return
    if not CV_TEX.exists():
        print("\nCV .tex: skipped (CV_AbelGuadaAzze.tex not found).")
        return

    try:
        import anthropic
    except ImportError:
        print("\nCV .tex: skipped (anthropic package not installed).")
        return

    lines = []
    for p in pubs:
        lines.append(
            f"Publication ({p.get('type','article')}): "
            f"{p['authors']}. {p['title']}. "
            f"{p.get('journal','')} {p.get('year','')}. "
            f"DOI: {p.get('doi','N/A')}. arXiv: {p.get('arxiv','N/A')}."
        )
    for t in talks:
        lines.append(
            f"Talk ({t.get('type','Talk')}): \"{t['title']}\". "
            f"{t.get('venue','')}. {t.get('date','')}. {t.get('location','')}. "
            f"Coauthors: {t.get('coauthors','N/A')}."
        )

    prompt = (
        "You are updating a LaTeX CV file. Insert each new entry into the correct section, "
        "matching the existing formatting exactly.\n\n"
        "Section mapping:\n"
        "  article / inproceedings  →  \\subsection{Refereed papers}\n"
        "  preprint / working       →  \\subsection{Working papers}\n"
        "  Seminar                  →  \\section{Seminar contributions (speaker underlined)}\n"
        "  Invited Talk             →  \\subsection{Invited talks}\n"
        "  Talk                     →  \\subsection{Contributed talks}\n"
        "  Poster                   →  \\subsection{Posters}\n\n"
        "Rules:\n"
        "  - Insert in reverse chronological order within each section.\n"
        "  - For \\cventry talk entries, mark Abel as speaker with \\underline{Abel Azze}.\n"
        "  - Return ONLY the complete updated .tex source. No markdown, no explanation.\n\n"
        f"FORMAT EXAMPLES:{CV_FORMAT_EXAMPLES}\n"
        f"NEW ENTRIES:\n" + "\n".join(lines) + "\n\n"
        f"CURRENT CV:\n{CV_TEX.read_text(encoding='utf-8')}"
    )

    print("\nCV .tex: updating via Claude API …")
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )
    result = response.content[0].text.strip()
    result = re.sub(r"^```[a-z]*\n", "", result)
    result = re.sub(r"\n```$", "", result)

    CV_TEX.write_text(result, encoding="utf-8")
    print("  Done.")


# ---------------------------------------------------------------------------
# Archive the form
# ---------------------------------------------------------------------------

def archive_form() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    dest  = PROCESSED / f"{stamp}_update.yml"
    shutil.move(str(UPDATE_FORM), str(dest))
    print(f"\nForm archived → _updates/processed/{dest.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not UPDATE_FORM.exists():
        print("No _updates/update.yml found — nothing to do.")
        sys.exit(0)

    data  = yaml.safe_load(UPDATE_FORM.read_text(encoding="utf-8")) or {}
    pubs  = [p for p in (data.get("publications") or []) if p]
    talks = [t for t in (data.get("talks")        or []) if t]

    if not pubs and not talks:
        print("update.yml contains no publications or talks — nothing to do.")
        archive_form()
        sys.exit(0)

    if pubs:
        process_publications(pubs)
    if talks:
        process_talks(talks)
    if pubs or talks:
        update_cv(pubs, talks)

    archive_form()
    print("\nAll done.")


if __name__ == "__main__":
    main()
