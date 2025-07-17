# Website Workflow

This document explains how your academic website is built and which files are essential for it to work. The website is built using [Jekyll](https://jekyllrb.com/), a static site generator that is deeply integrated with GitHub Pages.

## Core Concepts

Jekyll takes your content (written in Markdown), merges it with templates (HTML files), and generates a complete, static website (made of HTML, CSS, and JavaScript files) that can be hosted on any web server. GitHub Pages does this automatically for you every time you push changes to your repository.

## Essential Files and Directories

Here is a breakdown of the files and directories in your repository that are essential for the website's functionality.

### 1. Configuration

-   **`_config.yml`**: This is the main configuration file for your entire site. It contains global settings like your website's title, your name, your social media links, and other site-wide parameters. When Jekyll builds your site, it uses the values in this file.

### 2. Content

Your website's content lives in Markdown files (`.md`).

-   **`_pages/`**: This directory holds the main pages of your website. Each file corresponds to a page.
    -   `about.md`: This is your homepage (`/`). It contains your biography and research interests.
    -   `cv.md`: This is your CV page (`/cv/`).
    -   `publications.md`: This is your Publications page (`/publications/`).

-   **`index.html` (or `index.md`)**: This file in the root directory is often used as the landing page. In this template, `_pages/about.md` is configured to be the homepage via its `permalink: /`.

### 3. Structure and Templates (The "Look" of your site)

These files define the HTML structure and layout of your pages.

-   **`_layouts/`**: This directory contains the main HTML templates for your pages. For example, `archive.html` is used by your `cv.md` and `publications.md` pages to create their layout. The `--- layout: archive ---` line at the top of your markdown files tells Jekyll which layout to use.

-   **`_includes/`**: This directory contains smaller, reusable snippets of HTML that can be included in your layouts or pages. This helps avoid repeating code.
    -   `author-profile.html`: The sidebar with your picture and links.
    -   `navigation.html`: The main navigation bar at the top of the page.
    -   `footer.html`: The footer at the bottom of the page.

### 4. Styling and Assets

-   **`_sass/`**: This directory contains the SCSS files, which are a more powerful version of CSS. They define the colors, fonts, spacing, and overall visual style of your website. Jekyll processes these into a single CSS file that your browser uses to style the page.

-   **`assets/`**: This directory is for static files.
    -   `assets/css/`: The final CSS file will be placed here by Jekyll.
    -   `assets/js/`: For any JavaScript files.
    -   `assets/images/`: You should place your profile picture and any other images here.

### 5. Data

-   **`_data/`**: This directory is for structured data that your site can use.
    -   `navigation.yml`: This file defines the links that appear in your main navigation bar ("Home", "CV", "Publications"). You can edit this file to add, remove, or change navigation links.

### The Build Process: How it all connects

1.  You make a change to a file (e.g., you edit `_pages/publications.md`).
2.  You `git push` the change to your `aguazz/aguazz.github.io` repository on GitHub.
3.  GitHub Pages detects the change and triggers a Jekyll build.
4.  Jekyll reads `_config.yml` for site-wide settings.
5.  It takes your content from `_pages/publications.md`.
6.  It looks at the `layout: archive` in that file and wraps your content with the HTML from `_layouts/archive.html`.
7.  The `archive.html` layout probably includes other files from `_includes/` (like the navigation bar and footer).
8.  Jekyll processes the SCSS files from `_sass/` to create a CSS stylesheet.
9.  Finally, Jekyll combines everything into a final `publications/index.html` file and places it in a special directory (`_site`) along with all the CSS, JS, and images.
10. GitHub Pages serves the content of this generated `_site` directory as your live website.

By understanding this workflow, you can see that you only need to edit the Markdown files in `_pages/` for content, `_config.yml` for settings, and `_data/navigation.yml` for the navigation bar to manage your site. The rest of the files define the look and feel, and you generally don't need to touch them unless you want to make design changes.