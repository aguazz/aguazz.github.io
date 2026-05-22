# Site Restructuring Plan

**Goal:** Simplify the repo so that only files you need to edit are visible, the site is easier to maintain, and the codebase reflects only the sections you actually use.

**Active sections:** About, CV, Publications, Teaching, Talks (to be enabled)
**You are not using:** Blog/posts, Portfolio, Comments, Analytics, Talks map

---

## Current state (what you inherited)

The site is built on the **academicpages template** — a Jekyll site packaged with its entire theme source code (~150 files). Most of that is invisible plumbing (CSS, HTML templates, JS plugins) that you never touch. Your actual content lives in ~15 files. The rest is either unused features or theme internals.

Key problems:
- Disabled features (Portfolio, Blog, Comments, Analytics) still have config blocks and leftover files, creating noise
- Talks section is configured but never enabled
- `_config.yml` has ~50 lines of empty/irrelevant social profile fields
- Several orphaned template pages exist with no links pointing to them
- The `_sass/` folder has ~100 SCSS files you will never edit

---

## Phase 1 — Safe deletions and config cleanup

No risk of breaking anything visible. These items are disabled, disconnected, or empty.

### 1.1 Delete orphaned pages

**Prompt:**
> Delete the files `_pages/collection-archive.html` and `_pages/page-archive.html`. These are unused archive template pages — nothing links to them and they serve no function on the current site.

### 1.2 Delete legacy comments data

**Prompt:**
> Delete the folder `_data/comments/` and everything inside it. This was used by a comment system (Staticman) that is disabled. The data is stale and unused.

### 1.3 Clean up `_config.yml` — remove dead features

**Prompt:**
> In `_config.yml`, clean up the following disabled/empty blocks. Keep the structure of the file intact but remove or simplify:
> 1. The entire `comments:` block (lines ~23–27) and the `staticman:` block (lines ~33–48) — comments provider is empty and the system is off.
> 2. The `analytics:` block (lines ~75–79) — the provider is set to `"google-universal"` but there is no tracking ID, so it does nothing. Replace with `analytics:\n  provider: false`.
> 3. In the `defaults:` section, remove `share: true`, `comments: true`, and `read_time: true` from the `_posts`, `_teaching`, and `_publications` defaults — sharing and comments are not configured, and there are no posts to calculate read time for.
> 4. Remove `jekyll-paginate` from both the `plugins:` and `whitelist:` lists — pagination is commented out and unused.
> 5. Remove the `category_archive:` and `tag_archive:` blocks at the bottom — no tags or categories are used on this site.

### 1.4 Trim unused author social fields in `_config.yml`

**Prompt:**
> In `_config.yml`, in the `author:` block, delete all the social profile fields that are empty (have no value after the colon). Keep only the fields that have actual values filled in. Currently those are: `name`, `avatar`, `bio`, `location`, `employer`, `googlescholar`, `email`, `researchgate`, `github`, `LinkedIn`, `orcid`. Delete the rest (bitbucket, codepen, dribbble, flickr, facebook, foursquare, google_plus, keybase, instagram, impactstory, lastfm, pinterest, soundcloud, stackoverflow, steam, tumblr, twitter, vine, weibo, xing, youtube, wikipedia, pubmed, uri).

---

## Phase 2 — Enable the Talks section

The Talks collection is partially configured in `_config.yml` but the collection itself is commented out. This phase turns it on and adds your content.

### 2.1 Enable Talks in `_config.yml`

**Prompt:**
> In `_config.yml`, uncomment the talks collection so it reads:
> ```yaml
> talks:
>   output: true
>   permalink: /:collection/:path/
> ```
> The defaults block for talks (layout: talk, author_profile: true, share: true) already exists and can stay.

### 2.2 Create the Talks content directory and first entries

**Prompt (run after you have your talk details ready):**
> Create the folder `_talks/` in the repo root. For each talk, create a markdown file named `YYYY-MM-DD-short-title.md` with this front matter:
> ```yaml
> ---
> title: "Talk title"
> collection: talks
> type: "Talk"           # or "Seminar", "Invited talk", etc.
> permalink: /talks/YYYY-MM-DD-short-title
> venue: "Conference or institution name"
> date: YYYY-MM-DD
> location: "City, Country"
> ---
> Brief description of the talk (optional).
> ```
> Fill in one file per talk with the actual details.

### 2.3 Create the Talks page

**Prompt:**
> Create `_pages/talks.md` with the following content:
> ```markdown
> ---
> layout: archive
> title: "Talks"
> permalink: /talks/
> author_profile: true
> ---
> {% raw %}{% include base_path %}
>
> {% for post in site.talks reversed %}
>   {% include archive-single-talk.html %}
> {% endfor %}{% endraw %}
> ```
> Then add a "Talks" entry to `_data/navigation.yml` so it appears in the top menu, pointing to `/talks/`.

---

## Phase 3 — Theme migration (optional, bigger payoff)

**This phase is optional.** Do Phase 1 and 2 first and see if that's enough. Come back to this if you still find the repo hard to navigate.

The current theme bakes all its internals (the `_sass/`, `_includes/`, `_layouts/`, `assets/` folders) directly into your repo. That's ~130 files you'll never edit but can't easily ignore. A gem-based theme hides all of that — your repo would contain only your content.

The best candidate for migration is **[al-folio](https://github.com/alshedivat/al-folio)**, a popular Jekyll theme built specifically for academic personal pages. It supports all your sections (About, Publications, Teaching, Talks, CV) and looks polished.

### What migration involves

| Step | What happens |
|------|-------------|
| Fork al-folio repo | Start from a clean slate |
| Transfer content | Copy your markdown content from `_pages/`, `_publications/`, `_teaching/`, `_talks/` |
| Adapt front matter | Minor format differences between themes |
| Update `_config.yml` | Reconfigure with your details in al-folio format |
| Transfer assets | Profile photo, CV PDF, any images |
| Test on GitHub Pages | Enable GitHub Pages on the new repo |

**Prompt (when ready to start):**
> I want to migrate my site from the academicpages/Minimal Mistakes Jekyll theme to al-folio. Walk me through the migration step by step. My current content sections are: About (homepage), CV, Publications, Teaching, and Talks. I do not use a blog, portfolio, or comments. My repo is at `aguazz.github.io`. Start by explaining what al-folio's repo structure looks like and how it maps to my current content files.

---

## Order of operations

```
Phase 1.1  Delete orphaned pages          (2 min, zero risk)
Phase 1.2  Delete comments data           (1 min, zero risk)
Phase 1.3  Clean _config.yml features     (10 min, low risk)
Phase 1.4  Trim author social fields      (5 min, low risk)
    ↓
    → Commit & push → verify site still looks correct on GitHub Pages
    ↓
Phase 2.1  Enable Talks collection        (5 min, low risk)
Phase 2.2  Add your talk files            (depends on how many talks)
Phase 2.3  Create Talks page + nav link   (5 min, low risk)
    ↓
    → Commit & push → verify Talks page appears
    ↓
Phase 3    Theme migration                (1–2 hours, medium risk)
           — only if you want it —
```

---

## Files you will actually edit going forward

After Phase 1 and 2, the files you ever need to touch are:

| File | What it controls |
|------|-----------------|
| `_config.yml` | Site title, your name, bio, social links |
| `_pages/about.md` | Your homepage text |
| `_pages/cv.md` | CV page layout |
| `_pages/publications.md` | Publications page layout |
| `_pages/teaching.md` | Teaching page layout |
| `_pages/talks.md` | Talks page layout (after Phase 2) |
| `_publications/*.md` | One file per publication |
| `_teaching/*.md` | One file per course |
| `_talks/*.md` | One file per talk (after Phase 2) |
| `files/cv.pdf` | Your CV PDF |
| `images/profile.jpg` | Your profile photo |
| `_data/navigation.yml` | Top navigation menu links |