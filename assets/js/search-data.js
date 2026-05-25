// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "About",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-publications",
          title: "Publications",
          description: "Papers are listed in reverse chronological order.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-talks",
          title: "Talks",
          description: "Conference talks, seminars, and posters.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/talks/";
          },
        },{id: "nav-teaching",
          title: "Teaching",
          description: "Courses taught listed by institution. GitHub repositories with teaching materials are available for some courses.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/teaching/";
          },
        },{id: "nav-events",
          title: "Events",
          description: "Upcoming editions of key conferences related to my research interests and professional networks.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/events/";
          },
        },{id: "talks-optimal-stopping-of-gauss-markov-processes-with-random-terminal-value",
          title: 'Optimal stopping of Gauss-Markov processes with random terminal value',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2025-05-12-gauss-markov-random-terminal-fields";
            },},{id: "talks-optimally-stopping-a-gauss-markov-process-with-random-terminal-value",
          title: 'Optimally Stopping a Gauss–Markov process with random terminal value',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2025-06-10-lleida-seio";
            },},{id: "talks-optimal-stopping-of-a-gauss-markov-process-with-random-terminal-density",
          title: 'Optimal Stopping of a Gauss-Markov Process with random terminal density',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2025-09-19-odosp25-toronto";
            },},{id: "talks-ergodic-singular-control-for-ambiguous-compound-poisson-jump-diffusion-processes",
          title: 'Ergodic singular control for ambiguous compound-Poisson jump-diffusion processes',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2026-03-02-clapem-montevideo";
            },},{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
