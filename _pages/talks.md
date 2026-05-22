---
layout: page
permalink: /talks/
title: talks
description: Conference talks, seminars, and posters.
nav: true
nav_order: 3
---

### Seminars

{% assign seminars = site.talks | where: "type", "Seminar" | sort: "date" | reverse %}
{% for talk in seminars %}
- **{{ talk.date | date: "%Y" }}** — *{{ talk.title }}*  
  {{ talk.venue }}{% if talk.location %}, {{ talk.location }}{% endif %}{% if talk.slides %} · [Slides]({{ talk.slides }}){% endif %}
{% endfor %}

---

### Invited Talks

{% assign invited = site.talks | where: "type", "Invited Talk" | sort: "date" | reverse %}
{% for talk in invited %}
- **{{ talk.date | date: "%Y" }}** — *{{ talk.title }}*  
  {{ talk.venue }}{% if talk.location %}, {{ talk.location }}{% endif %}{% if talk.slides %} · [Slides]({{ talk.slides }}){% endif %}
{% endfor %}

---

### Contributed Talks

{% assign contributed = site.talks | where: "type", "Talk" | sort: "date" | reverse %}
{% for talk in contributed %}
- **{{ talk.date | date: "%Y" }}** — *{{ talk.title }}*  
  {{ talk.venue }}{% if talk.location %}, {{ talk.location }}{% endif %}{% if talk.slides %} · [Slides]({{ talk.slides }}){% endif %}
{% endfor %}

---

### Posters

{% assign posters = site.talks | where: "type", "Poster" | sort: "date" | reverse %}
{% for talk in posters %}
- **{{ talk.date | date: "%Y" }}** — *{{ talk.title }}*  
  {{ talk.venue }}{% if talk.location %}, {{ talk.location }}{% endif %}{% if talk.slides %} · [Poster]({{ talk.slides }}){% endif %}
{% endfor %}
