---
layout: page
permalink: /talks/
title: Talks
description: Conference talks, seminars, and posters.
nav: true
nav_order: 3
---

### Invited Talks

{% assign invited = site.talks | where: "type", "Invited Talk" | sort: "date" | reverse %}
{% for talk in invited %}
- **{{ talk.date | date: "%Y" }}** — *{{ talk.title }}*  
  {{ talk.venue }}{% if talk.location %}, {{ talk.location }}{% endif %}{% if talk.slides %} · <a href="{{ talk.slides }}" target="_blank">Slides</a>{% endif %}{% if talk.video %} · <a href="{{ talk.video }}" target="_blank">Video</a>{% endif %}{% if talk.event_url %} · <a href="{{ talk.event_url }}" target="_blank">Event</a>{% endif %}
{% endfor %}

---

### Contributed Talks

{% assign contributed = site.talks | where: "type", "Talk" | sort: "date" | reverse %}
{% for talk in contributed %}
- **{{ talk.date | date: "%Y" }}** — *{{ talk.title }}*  
  {{ talk.venue }}{% if talk.location %}, {{ talk.location }}{% endif %}{% if talk.slides %} · <a href="{{ talk.slides }}" target="_blank">Slides</a>{% endif %}{% if talk.video %} · <a href="{{ talk.video }}" target="_blank">Video</a>{% endif %}{% if talk.event_url %} · <a href="{{ talk.event_url }}" target="_blank">Event</a>{% endif %}
{% endfor %}

