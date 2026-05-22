# Editing Guide

Quick reference for all common edits to the site. After any change, commit and push — the site updates automatically within a few minutes.

---

## Quick reference

| What you want to change | File to edit |
|---|---|
| Bio text on homepage | `_pages/about.md` |
| Add / remove a publication | `_bibliography/papers.bib` |
| Add / remove a talk | `_talks/` (one file per talk) |
| Update teaching list | `_pages/teaching.md` |
| Replace CV PDF | `assets/pdf/Curriculum_Vitae.pdf` |
| Replace profile photo | `assets/img/prof_pic.jpg` |
| Social links (email, Scholar, etc.) | `_data/socials.yml` |
| Site title / name / description | `_config.yml` (top section) |
| Add a new page | Create `_pages/yourpage.md` |
| Remove a page | Delete the file in `_pages/` |

---

## Homepage (`_pages/about.md`)

Edit the text below the `---` block freely. The front matter (between the two `---` lines) controls layout and profile options — only change `subtitle` and the body text.

```markdown
---
layout: about
title: about
permalink: /
subtitle: Associate Professor, <a href="https://www.cunef.edu">CUNEF Universidad</a>
...
---

Your bio text goes here. Supports **bold**, *italic*, and [links](https://url.com).
```

---

## Publications (`_bibliography/papers.bib`)

Each publication is one BibTeX entry. The type (`@article`, `@unpublished`, etc.) controls how it is categorised.

**Minimal entry for a published journal article:**

```bibtex
@article{yourkey2025,
  bibtex_show = {true},
  title   = {Your paper title},
  author  = {Last, First and Coauthor, Name},
  journal = {Journal Name},
  volume  = {10},
  pages   = {1--20},
  year    = {2025},
  doi     = {10.xxxx/xxxxx},
  html    = {https://doi.org/10.xxxx/xxxxx},
  arxiv   = {2501.12345},
}
```

**For a working paper / preprint:**

```bibtex
@unpublished{yourkey2025,
  bibtex_show = {true},
  title  = {Your paper title},
  author = {Last, First and Coauthor, Name},
  year   = {2025},
  note   = {Working paper},
  html   = {https://doi.org/10.48550/arXiv.2501.12345},
  arxiv  = {2501.12345},
}
```

**Key naming:** use `authornameyear` with no spaces (e.g. `azze2025gauss`). Must be unique across all entries.

**To remove a publication:** delete the entire `@article{...}` block including the closing `}`.

**Special characters in titles:** wrap proper nouns in `{ }` to preserve capitalisation, e.g. `{Gauss}--{Markov}`.

---

## Talks (`_talks/`)

Each talk is a separate `.md` file. The filename format is `YYYY-MM-DD-short-title.md`.

**To add a talk**, create a new file with this content:

```markdown
---
title: "Your talk title"
collection: talks
type: "Talk"
permalink: /talks/YYYY-MM-DD-short-title
venue: "Conference or institution name"
date: YYYY-MM-DD
location: "City, Country"
slides:
---

With Coauthor Name (optional description).
```

**`type` options** control which section of the Talks page it appears under:
- `"Talk"` — Contributed talks
- `"Invited Talk"` — Invited talks
- `"Seminar"` — Seminars
- `"Poster"` — Posters

**To add slides:** upload the PDF to `assets/pdf/` and set:
```yaml
slides: /assets/pdf/your-slides-filename.pdf
```

**To remove a talk:** delete the file from `_talks/`.

---

## Teaching (`_pages/teaching.md`)

This is plain Markdown — edit it like a text document. Add or remove bullet points, years, and course names as needed. No special format required.

---

## CV (`assets/pdf/Curriculum_Vitae.pdf`)

Replace the file at `assets/pdf/Curriculum_Vitae.pdf` with your updated PDF. Keep the exact same filename so no links break.

---

## Profile photo (`assets/img/prof_pic.jpg`)

Replace the file at `assets/img/prof_pic.jpg` with your new photo. Keep the exact same filename. Any standard image format (`.jpg`, `.png`) works as long as you also update the filename in `_pages/about.md` if you change it.

---

## Social links (`_data/socials.yml`)

Each line is a social network. Remove a line to hide that icon; add a line to show a new one.

```yaml
email: your.email@institution.edu
scholar_userid: XXXXXXXXXX          # Google Scholar profile ID
orcid_id: 0000-0000-0000-0000
linkedin_username: your-linkedin-id
github_username: yourgithubname
researchgate_username: Your-Name-2
cv_pdf: /assets/pdf/Curriculum_Vitae.pdf
```

The Scholar ID is the string after `user=` in your Google Scholar profile URL.

---

## Adding a new page

1. Create `_pages/yourpage.md` with this front matter:

```markdown
---
layout: page
title: your page title
permalink: /yourpage/
nav: true
nav_order: 6
---

Page content here.
```

2. Set `nav_order` to control where it appears in the navigation bar (existing pages use 2–5).

3. Push — the page and nav link appear automatically.

---

## Removing a page

Delete the file from `_pages/`. The page and its navigation link disappear automatically on next build. If you want to keep the file but hide it from the nav bar, set `nav: false` in its front matter instead.

---

## Site settings (`_config.yml`)

The only section you should ever need to edit is at the very top:

```yaml
first_name: Abel
last_name: Azze
description: >
  Associate Professor at CUNEF Universidad. ...
url: https://aguazz.github.io
```

Do not edit anything below the `# Layout` section.
