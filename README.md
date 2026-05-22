# aguazz.github.io

Personal academic website of **Abel Guada Azze**, Associate Professor at CUNEF Universidad.

Live at: [aguazz.github.io](https://aguazz.github.io)

---

## How the site works

The site is built with [Jekyll](https://jekyllrb.com/) using the [al-folio](https://github.com/alshedivat/al-folio) theme. Content is written in Markdown and YAML files. When changes are pushed to GitHub, a **GitHub Actions** workflow automatically builds the site and publishes it — no local software needed.

```
edit files → git push → GitHub Actions builds → site updates (2–3 min)
```

---

## Repo structure

```
_pages/          ← one .md file per page (about, publications, teaching, talks, cv)
_bibliography/
  papers.bib     ← all publications in BibTeX format
_talks/          ← one .md file per talk/seminar/poster
_data/
  socials.yml    ← social links shown on the site (email, Google Scholar, etc.)
  coauthors.yml  ← coauthor name → profile URL mappings
assets/
  img/
    prof_pic.jpg ← profile photo
  pdf/
    Curriculum_Vitae.pdf ← CV file
_config.yml      ← site-wide settings (name, description, URL)
```

Everything else (`_sass/`, `_includes/`, `_layouts/`, `_plugins/`, `assets/css/`, `assets/js/`) is theme infrastructure — **do not edit these**.

---

## Making changes

See [EDITING_GUIDE.md](EDITING_GUIDE.md) for step-by-step instructions on all common edits.

See [TO_DO.md](TO_DO.md) for pending tasks (e.g. slides PDFs to be added).

---

## Deployment

Push to `master`. GitHub Actions handles the rest. Build status is visible under the **Actions** tab on GitHub.
