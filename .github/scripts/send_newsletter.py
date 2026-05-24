"""
Monthly script: reads _data/events.yml and sends a segmented Buttondown email
to subscribers tagged with each congress id.

One email per congress (only if that congress has upcoming dates).
Subscribers who chose multiple congresses receive multiple emails.
"""

import os
import sys
from datetime import date, datetime

import requests
import yaml

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
EVENTS_FILE = os.path.join(REPO_ROOT, "_data", "events.yml")

API_KEY = os.environ.get("BUTTONDOWN_API_KEY", "")
API_BASE = "https://api.buttondown.email/v1"
SITE_URL = "https://aguazz.github.io/events/"


def load_events() -> dict:
    with open(EVENTS_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def headers() -> dict:
    return {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }


def format_date(d: str) -> str:
    if not d:
        return "TBD"
    try:
        return datetime.strptime(d, "%Y-%m-%d").strftime("%B %-d, %Y")
    except ValueError:
        return d


def build_email_body(congress: dict) -> str:
    ed = congress.get("next_edition", {})
    name = congress["name"]
    short = congress["short_name"]
    desc = congress.get("description", "").strip()
    website = ed.get("edition_website") or congress.get("website", "")

    start = format_date(ed.get("dates_start", ""))
    end = format_date(ed.get("dates_end", ""))
    location = ed.get("location") or "TBD"
    abstract_dl = format_date(ed.get("abstract_deadline", ""))
    reg_dl = format_date(ed.get("registration_deadline", ""))
    notes = ed.get("notes", "")

    dates_str = f"{start}" + (f" – {end}" if ed.get("dates_end") else "")

    lines = [
        f"# {name} ({short})",
        "",
        desc,
        "",
        "## Next edition",
        "",
        f"📅 **Dates:** {dates_str}",
        f"📍 **Location:** {location}",
    ]

    if ed.get("abstract_deadline"):
        lines.append(f"📝 **Abstract deadline:** {abstract_dl}")
    if ed.get("registration_deadline"):
        lines.append(f"✅ **Registration deadline:** {reg_dl}")
    if notes:
        lines += ["", f"💡 {notes}"]
    if website:
        lines += ["", f"[Visit congress website]({website})"]

    lines += [
        "",
        "---",
        "",
        f"View all upcoming events on [aguazz.github.io/events/]({SITE_URL})",
        "",
        "You are receiving this because you subscribed to updates for "
        f"**{short}** on Abel Azze's website. "
        "You can unsubscribe at any time using the link below.",
    ]

    return "\n".join(lines)


def has_upcoming_dates(edition: dict) -> bool:
    start = edition.get("dates_start", "")
    if not start:
        return False
    try:
        return datetime.strptime(start, "%Y-%m-%d").date() >= date.today()
    except ValueError:
        return False


def send_email(subject: str, body: str, tag: str) -> None:
    payload = {
        "subject": subject,
        "body": body,
        "status": "sent",
        "filters": [{"type": "tag", "value": tag}],
    }
    resp = requests.post(f"{API_BASE}/emails", json=payload, headers=headers(), timeout=30)
    if resp.ok:
        print(f"  Sent: {subject!r} → tag={tag!r}")
    else:
        print(f"  ERROR sending {subject!r}: {resp.status_code} {resp.text}")


def run() -> None:
    if not API_KEY:
        print("BUTTONDOWN_API_KEY not set — aborting.")
        sys.exit(1)

    data = load_events()
    congresses = data.get("congresses", [])
    today_str = date.today().strftime("%B %Y")

    sent = 0
    for congress in congresses:
        ed = congress.get("next_edition", {})
        if not has_upcoming_dates(ed):
            print(f"  Skipping {congress['short_name']} — no upcoming dates.")
            continue

        subject = f"[{congress['short_name']}] Upcoming congress — {today_str}"
        body = build_email_body(congress)
        send_email(subject, body, congress["id"])
        sent += 1

    print(f"\nDone. {sent} email(s) sent.")


if __name__ == "__main__":
    run()
