# A Non-Coder's Guide to Editing Your Website

This guide will walk you through the most common edits you'll want to make to your academic website. All changes can be made directly from the GitHub interface, without writing any code.

The general process for editing any file is:
1.  Navigate to the file in your GitHub repository.
2.  Click the pencil icon (✏️) in the top-right corner to edit the file.
3.  Make your changes.
4.  Scroll to the bottom of the page, type a brief commit message (e.g., "Update publications list"), and click "Commit changes".
5.  Wait a minute or two for GitHub to automatically update your live website.

---

### How to Change Your Profile Picture

1.  **Upload your new picture:**
    *   Go to the `assets/images/` directory in your repository.
    *   Click `Add file` > `Upload files`.
    *   Drag and drop your new profile picture here. Let's say you name it `profile-pic.jpg`.
2.  **Update the configuration file:**
    *   Open the `_config.yml` file.
    *   Find the `author:` section.
    *   Update the `avatar:` line to point to your new image:
        ```yaml
        author:
          name             : "Your Name"
          avatar           : "/assets/images/profile-pic.jpg" # Change this line
          # ... other settings
        ```

---

### How to Update Your CV PDF File

1.  **Upload your new CV:**
    *   Go to the `files/` directory. If it doesn't exist, you can create it.
    *   Click `Add file` > `Upload files`.
    *   Upload your new CV PDF, for example, `my_cv.pdf`.
2.  **Update the link on your CV page:**
    *   Open the `_pages/cv.md` file.
    *   You can add a link to the top of the page like this:
        ```markdown
        ---
        layout: archive
        title: "CV"
        permalink: /cv/
        author_profile: true
        ---

        [Download my CV as a PDF](/files/my_cv.pdf)

        Education
        ======
        * B.S. in ...
        ```
    *   Replace `my_cv.pdf` with the exact name of the file you uploaded.

---

### How to Edit Page Content (About, CV, Publications)

Your main pages are located in the `_pages/` directory. These are simple text files using Markdown syntax.

*   **To Edit Your "About" Page:** Open `_pages/about.md`. You can edit the text directly under each heading (`======`).
*   **To Edit Your "CV" Page:** Open `_pages/cv.md`. You can add or remove items from the lists under "Education", "Work experience", etc. Use a `*` for bullet points.
*   **To Edit Your "Publications" Page:** Open `_pages/publications.md`. Each publication is a bullet point. To add a new one, just copy the format of an existing one and paste it at the top of the list.

    *Example of a publication entry:*
    ```markdown
    * Azze, Abel; D’Auria, Bernardo; García-Portugués, Eduardo. "Optimal stopping of Gauss–Markov bridges", 2025, Advances in Applied Probability, to appear. [Journal link](https://doi.org/...) [ArXiv link](https://arxiv.org/...)
    ```

---

### How to Modify the Sidebar Information and Social Media Links

All of this information is in one central file.

1.  Open the `_config.yml` file.
2.  Scroll down to the `author:` section.
3.  Edit the following fields:
    ```yaml
    author:
      name             : "Your Full Name"
      avatar           : "/assets/images/your-photo.jpg"
      bio              : "Your title and affiliation (e.g., Assistant Professor at CUNEF Universidad)"
      location         : "City, Country"
      email            : "your.email@example.com"
      # ...
    ```
4.  To edit **social media links**, find the `author.links:` section within the same file. You can update the URL for each entry or add/remove services.

    ```yaml
      links:
        - label: "Email"
          icon: "fas fa-fw fa-envelope-square"
          url: "mailto:your.email@example.com"
        - label: "Website"
          icon: "fas fa-fw fa-link"
          url: "https://your-website.com"
        - label: "Twitter"
          icon: "fab fa-fw fa-twitter-square"
          url: "https://twitter.com/your_handle"
        # - label: "GitHub"
        #   icon: "fab fa-fw fa-github"
        #   url: "https://github.com/your_username"
    ```
    *   To **remove** a link, you can either delete the lines or "comment them out" by adding a `#` at the beginning of each line (as shown for GitHub above).
    *   To **add** a link, copy an existing block and change the `label`, `icon`, and `url`.

---

### How to Add a New Page (e.g., "Teaching") and Link it in the Top Bar

This is a two-step process: you first create the page, then you add the link.

**Step 1: Create the New Page**

1.  Go to the `_pages/` directory.
2.  Click `Add file` > `Create new file`.
3.  Name the file `teaching.md` (or `projects.md`, etc.).
4.  Copy and paste the following template into the file. This is the "front matter" that Jekyll needs.

    ```markdown
    ---
    layout: archive
    title: "Teaching"
    permalink: /teaching/
    author_profile: true
    ---

    Here you can write about your teaching experience.

    ## Course Title 1
    *   Details about the course...

    ## Course Title 2
    *   More details...
    ```
5.  Change the `title:` and `permalink:` to match your new page. The `permalink` will be the URL (e.g., `your-site.com/teaching/`).
6.  Add your content below the `---` lines.

**Step 2: Add the Link to the Top Navigation Bar**

1.  Open the `_data/navigation.yml` file.
2.  To add a link to your new "Teaching" page, add the following lines to the list. The order in the file determines the order on the website.

    ```yaml
    # main navigation
    main:
      - title: "Home"
        url: /
      - title: "Publications"
        url: /publications/
      - title: "Teaching"      # <-- New line
        url: /teaching/     # <-- New line
      - title: "CV"
        url: /cv/
    ```
    *   The `title:` is the text that appears on the button.
    *   The `url:` must match the `permalink:` you set in the page's file.

---

### How to Edit or Reorder Existing Links in the Top Bar

1.  Open the `_data/navigation.yml` file.
2.  **To rename a link:** Simply change the `title:` value. For example, to change "Home" to "About":
    ```yaml
    - title: "About" # Was "Home"
      url: /
    ```
3.  **To reorder links:** Cut and paste the blocks of `title` and `url` to change their order in the list.