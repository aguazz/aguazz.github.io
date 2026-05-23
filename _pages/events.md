---
layout: page
permalink: /events/
title: Events
description: Upcoming conferences, workshops, summer schools, and seminars in optimal stopping, stochastic control, and related areas. Updated weekly by an automated bot — <a href="https://github.com/aguazz/aguazz.github.io/pulls?q=label%3Aautomated" target="_blank">see recent updates</a>.
nav: true
nav_order: 6
---

{% assign all_events = site.data.conferences %}

{% assign conferences = all_events | where: "type", "conference" | sort: "date" %}
{% assign workshops   = all_events | where: "type", "workshop"   | sort: "date" %}
{% assign schools     = all_events | where: "type", "summer_school" | sort: "date" %}
{% assign seminars    = all_events | where: "type", "seminar"    | sort: "name" %}

{% if conferences.size > 0 %}
### Conferences

{% for ev in conferences %}
- [**{{ ev.name }}**]({{ ev.url }}){:target="_blank"}{% if ev.location %} · {{ ev.location }}{% endif %}{% if ev.date %} · {{ ev.date | date: "%b %Y" }}{% endif %}{% if ev.deadline %} · <span style="color:var(--global-theme-color)">Deadline: {{ ev.deadline | date: "%d %b %Y" }}</span>{% endif %}{% if ev.notes %}  
  <span style="font-size:0.9em; color:var(--global-text-color-light)">{{ ev.notes }}</span>{% endif %}
{% endfor %}
{% endif %}

---

{% if workshops.size > 0 %}
### Workshops

{% for ev in workshops %}
- [**{{ ev.name }}**]({{ ev.url }}){:target="_blank"}{% if ev.location %} · {{ ev.location }}{% endif %}{% if ev.date %} · {{ ev.date | date: "%b %Y" }}{% endif %}{% if ev.deadline %} · <span style="color:var(--global-theme-color)">Deadline: {{ ev.deadline | date: "%d %b %Y" }}</span>{% endif %}{% if ev.notes %}  
  <span style="font-size:0.9em; color:var(--global-text-color-light)">{{ ev.notes }}</span>{% endif %}
{% endfor %}
{% endif %}

---

{% if schools.size > 0 %}
### Summer Schools

{% for ev in schools %}
- [**{{ ev.name }}**]({{ ev.url }}){:target="_blank"}{% if ev.location %} · {{ ev.location }}{% endif %}{% if ev.date %} · {{ ev.date | date: "%b %Y" }}{% endif %}{% if ev.deadline %} · <span style="color:var(--global-theme-color)">Deadline: {{ ev.deadline | date: "%d %b %Y" }}</span>{% endif %}{% if ev.notes %}  
  <span style="font-size:0.9em; color:var(--global-text-color-light)">{{ ev.notes }}</span>{% endif %}
{% endfor %}
{% endif %}

---

{% if seminars.size > 0 %}
### Seminar Series

{% for ev in seminars %}
- [**{{ ev.name }}**]({{ ev.url }}){:target="_blank"}{% if ev.location %} · {{ ev.location }}{% endif %}{% if ev.notes %}  
  <span style="font-size:0.9em; color:var(--global-text-color-light)">{{ ev.notes }}</span>{% endif %}
{% endfor %}
{% endif %}

<div style="margin-top: 2rem; font-size: 0.85em; color: var(--global-text-color-light)">
  Events are discovered weekly by a bot that searches academic databases and ranks results by relevance using Claude AI.
  To suggest an event or correct an entry, open an <a href="https://github.com/aguazz/aguazz.github.io/issues" target="_blank">issue</a>.
</div>
