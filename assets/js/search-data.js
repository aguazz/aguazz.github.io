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
          description: "Courses taught at CUNEF Universidad and elsewhere.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/teaching/";
          },
        },{id: "nav-cv",
          title: "CV",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "nav-events",
          title: "Events",
          description: "Upcoming conferences, workshops, summer schools, and seminars in optimal stopping, stochastic control, and related areas. Updated weekly by an automated bot — see recent updates.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/events/";
          },
        },{id: "talks-estimación-por-kernel-en-muestras-pequeñas",
          title: 'Estimación por Kernel en muestras pequeñas',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2013-01-01-kernel-muestras-pequenas-havana";
            },},{id: "talks-bandwidth-selection-for-heavy-tailed-distributions",
          title: 'Bandwidth selection for heavy-tailed distributions',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2014-01-01-bandwidth-heavy-tailed-cuba-mexico";
            },},{id: "talks-estimación-por-kernel-para-colas-pesadas",
          title: 'Estimación por Kernel para Colas Pesadas',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2014-01-01-kernel-colas-pesadas-havana";
            },},{id: "talks-inferring-the-optimal-stopping-boundary-for-a-brownian-bridge",
          title: 'Inferring the optimal stopping boundary for a Brownian bridge',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2018-01-01-inferring-stopping-smbd-poster";
            },},{id: "talks-optimal-stopping-and-volterra-type-equations-application-to-the-brownian-bridge",
          title: 'Optimal stopping and Volterra type equations: application to the Brownian Bridge',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2018-04-04-optimal-stopping-volterra-maf";
            },},{id: "talks-optimal-exercise-for-american-options-under-stock-pinning",
          title: 'Optimal exercise for American options under stock pinning',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2019-06-05-american-options-pinning-sysorm";
            },},{id: "talks-optimal-exercise-for-american-options-under-pinning-effect",
          title: 'Optimal exercise for American options under pinning effect',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2020-01-13-american-options-pinning-leeds";
            },},{id: "talks-optimal-stopping-of-gauss-markov-bridge",
          title: 'Optimal stopping of Gauss–Markov bridge',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2023-11-13-gauss-markov-bridge-bymat";
            },},{id: "talks-optimal-stopping-of-gauss-markov-processes",
          title: 'Optimal stopping of Gauss-Markov processes',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2023-12-20-gauss-markov-cunef-seminar";
            },},{id: "talks-optimal-stopping-of-gauss-markov-bridges-with-applications-to-american-options",
          title: 'Optimal stopping of Gauss-Markov bridges with applications to American options',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2024-07-08-gauss-markov-bridges-bachelier";
            },},{id: "talks-optimal-stopping-of-gauss-markov-bridges",
          title: 'Optimal stopping of Gauss-Markov bridges',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2024-09-23-gauss-markov-bridges-zaragoza";
            },},{id: "talks-optimally-stopping-a-gauss-markov-process-with-random-terminal-value",
          title: 'Optimally Stopping a Gauss-Markov process with random terminal value',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2025-03-26-gauss-markov-random-terminal-manchester";
            },},{id: "talks-optimal-stopping-of-gauss-markov-processes-with-random-terminal-value",
          title: 'Optimal stopping of Gauss-Markov processes with random terminal value',
          description: "",
          section: "Talks",handler: () => {
              window.location.href = "/talks/2025-09-12-gauss-markov-random-terminal-fields";
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
