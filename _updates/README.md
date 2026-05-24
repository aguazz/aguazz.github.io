# Site Update System

This directory contains the tools to update [aguazz.github.io](https://aguazz.github.io) automatically.

---

## How to add a new publication or talk

**Step 1 — Copy the template**
```bash
cp _updates/update_template.yml _updates/update.yml
```

**Step 2 — Fill in the form**  
Edit `_updates/update.yml`. Keep only the entries you want to add; delete the rest.

**Step 3 — Add PDF attachments** *(only if you have slides or similar files)*  
Place the PDFs in `_updates/attachments/` and reference them by filename in the form:
```yaml
slides: my-slides.pdf
```

**Step 4 — Commit and push**
```bash
git add _updates/
git commit -m "add new publication/talk"
git push
```

**Step 5 — Wait ~3 minutes**  
GitHub Actions will:
1. Append the BibTeX entry to `_bibliography/papers.bib`
2. Create the talk Markdown file in `_talks/`
3. Move any PDFs to `assets/pdf/talks/`
4. Update `assets/pdf/CV_AbelGuadaAzze.tex` via Claude API *(if key is set)*
5. Archive the filled form to `_updates/processed/`
6. Trigger a full rebuild and deploy of the site

---

## Form field reference

### Publications

| Field | Required | Notes |
|-------|:--------:|-------|
| `type` | yes | `article` · `inproceedings` · `preprint` |
| `title` | yes | Full paper title |
| `authors` | yes | `"Azze, Abel and D'Auria, Bernardo"` |
| `journal` | yes | Journal name; conference name for `inproceedings` |
| `year` | yes | Four-digit year |
| `volume` | no | |
| `number` | no | |
| `pages` | no | Use LaTeX dashes: `"1--34"` |
| `doi` | no | DOI only, e.g. `"10.1017/apr.2024.21"` |
| `arxiv` | no | arXiv ID only, e.g. `"2211.05835"` |
| `selected` | no | `true` = show as featured paper on homepage |

### Talks

| Field | Required | Notes |
|-------|:--------:|-------|
| `title` | yes | |
| `type` | yes | `Talk` · `Invited Talk` · `Seminar` · `Poster` |
| `venue` | yes | Full name of the event |
| `date` | yes | `YYYY-MM-DD` — use the start date for multi-day events |
| `location` | yes | `City, Country` |
| `coauthors` | no | e.g. `"Bernardo D'Auria"` |
| `slides` | no | PDF filename placed in `_updates/attachments/` |

---

## One-time setup (first use only)

### Anthropic API key — enables CV `.tex` auto-update

1. Get a key at [console.anthropic.com](https://console.anthropic.com).
2. Go to your GitHub repo → **Settings → Secrets and variables → Actions**.
3. Click **New repository secret**, name it `ANTHROPIC_API_KEY`, paste the key.

> If this secret is absent, the workflow still updates the website but skips the `.tex` update. You can add it later without changing anything else.

### Resend API key — enables monthly email reminders

1. Sign up at [resend.com](https://resend.com) (free tier: 3,000 emails/month, no credit card).
2. Go to **API Keys** and create one.
3. Add it as GitHub secret: `RESEND_API_KEY`.
4. In **Domains**, either verify your own domain or note your Resend sending address.
5. Edit `.github/workflows/notify-update.yml` and update the `from:` field to match your verified sender.

> Without `RESEND_API_KEY`, the monthly reminder workflow fails silently. The update workflow is unaffected.

---

## Adding a new coauthor

The script does **not** auto-add coauthors. Edit `_data/coauthors.yml` manually:

```yaml
"last-name-key":
  - firstname: ["Full Name", "F."]
    url: https://their-profile-url
```

The key must be the lowercase last name (or hyphenated last name). It is matched against the author field of BibTeX entries to generate profile links.

---

## Directory layout

```
_updates/
├── update_template.yml   ← copy to update.yml to trigger an update
├── update_site.py        ← the automation script (run by GitHub Actions)
├── attachments/          ← place PDFs here before committing
│   └── .gitkeep
└── processed/            ← archived forms, one per update (auto-generated)
    └── .gitkeep
```

---

## How the CV `.tex` auto-update works

When `ANTHROPIC_API_KEY` is set and you add publications or talks, the script sends the current `assets/pdf/CV_AbelGuadaAzze.tex` to Claude together with a description of the new entries. Claude inserts them in the correct section using the exact formatting of the existing entries and returns the updated file. You then review it, compile to PDF locally, and push the new PDF.

The `.tex` is only ever modified when you explicitly push `_updates/update.yml` — it is never touched automatically otherwise.
