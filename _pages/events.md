---
layout: page
permalink: /events/
title: Events
description: Upcoming editions of key congresses in probability and mathematical finance.
nav: true
nav_order: 5
events_subscribe: true
---

<div class="events-page">

{% assign today = 'now' | date: '%s' | plus: 0 %}
{% assign congresses = site.data.events.congresses %}

{% comment %} Sort by nearest start date, putting blank-dated entries at the end {% endcomment %}
{% assign with_date = congresses | where_exp: "c", "c.next_edition.dates_start != ''" %}
{% assign without_date = congresses | where_exp: "c", "c.next_edition.dates_start == ''" %}
{% assign with_date_sorted = with_date | sort: "next_edition.dates_start" %}

<div class="events-grid">

{% for congress in with_date_sorted %}
  {% assign start_ts = congress.next_edition.dates_start | date: '%s' | plus: 0 %}
  {% assign days_left = start_ts | minus: today | divided_by: 86400 %}
  <div class="event-card" id="event-{{ congress.id }}">
    <div class="event-card-header">
      <span class="event-short-name">{{ congress.short_name }}</span>
      {% if days_left > 0 %}
        {% if days_left <= 30 %}
          <span class="event-badge badge-urgent">{{ days_left }} days</span>
        {% elsif days_left <= 90 %}
          <span class="event-badge badge-soon">{{ days_left }} days</span>
        {% else %}
          <span class="event-badge badge-upcoming">{{ days_left }} days</span>
        {% endif %}
      {% else %}
        <span class="event-badge badge-past">Past</span>
      {% endif %}
    </div>

    <h3 class="event-full-name">
      {% if congress.next_edition.edition_website != '' %}
        <a href="{{ congress.next_edition.edition_website }}" target="_blank" rel="noopener">{{ congress.name }}</a>
      {% elsif congress.website != '' %}
        <a href="{{ congress.website }}" target="_blank" rel="noopener">{{ congress.name }}</a>
      {% else %}
        {{ congress.name }}
      {% endif %}
    </h3>

    <p class="event-description">{{ congress.description }}</p>

    <div class="event-details">
      {% if congress.next_edition.dates_start != '' %}
        <div class="event-detail-row">
          <span class="event-detail-icon">&#128197;</span>
          <span>
            {{ congress.next_edition.dates_start | date: "%b %-d" }}
            {% if congress.next_edition.dates_end != '' %}
              &ndash;{{ congress.next_edition.dates_end | date: "%-d, %Y" }}
            {% else %}
              , {{ congress.next_edition.dates_start | date: "%Y" }}
            {% endif %}
          </span>
        </div>
      {% endif %}

      {% if congress.next_edition.location != '' %}
        <div class="event-detail-row">
          <span class="event-detail-icon">&#128205;</span>
          <span>{{ congress.next_edition.location }}</span>
        </div>
      {% endif %}

      {% if congress.next_edition.abstract_deadline != '' %}
        <div class="event-detail-row">
          <span class="event-detail-icon">&#128221;</span>
          <span>Abstract deadline: <strong>{{ congress.next_edition.abstract_deadline | date: "%b %-d, %Y" }}</strong></span>
        </div>
      {% endif %}

      {% if congress.next_edition.registration_deadline != '' %}
        <div class="event-detail-row">
          <span class="event-detail-icon">&#9989;</span>
          <span>Registration deadline: <strong>{{ congress.next_edition.registration_deadline | date: "%b %-d, %Y" }}</strong></span>
        </div>
      {% endif %}

      {% if congress.next_edition.notes != '' %}
        <div class="event-detail-row event-notes">
          <span class="event-detail-icon">&#128161;</span>
          <span>{{ congress.next_edition.notes }}</span>
        </div>
      {% endif %}
    </div>

    {% if congress.next_edition.edition_website != '' %}
      <a class="event-link" href="{{ congress.next_edition.edition_website }}" target="_blank" rel="noopener">
        Visit congress website &rarr;
      </a>
    {% elsif congress.website != '' %}
      <a class="event-link" href="{{ congress.website }}" target="_blank" rel="noopener">
        Visit website &rarr;
      </a>
    {% endif %}
  </div>
{% endfor %}

{% for congress in without_date %}
  <div class="event-card event-card-tbd" id="event-{{ congress.id }}">
    <div class="event-card-header">
      <span class="event-short-name">{{ congress.short_name }}</span>
      <span class="event-badge badge-tbd">TBD</span>
    </div>

    <h3 class="event-full-name">
      {% if congress.website != '' %}
        <a href="{{ congress.website }}" target="_blank" rel="noopener">{{ congress.name }}</a>
      {% else %}
        {{ congress.name }}
      {% endif %}
    </h3>

    <p class="event-description">{{ congress.description }}</p>

    {% if congress.next_edition.notes != '' %}
      <p class="event-notes-tbd">{{ congress.next_edition.notes }}</p>
    {% else %}
      <p class="event-notes-tbd">Next edition dates not yet announced.</p>
    {% endif %}

    {% if congress.website != '' %}
      <a class="event-link" href="{{ congress.website }}" target="_blank" rel="noopener">
        Visit website &rarr;
      </a>
    {% endif %}
  </div>
{% endfor %}

</div>

{% if site.data.events.last_updated != '' %}
  <p class="events-last-updated">Last updated: {{ site.data.events.last_updated }}</p>
{% endif %}

---

### Stay up to date

Subscribe to receive a monthly email with upcoming deadlines and announcements for the congresses you follow.

<div class="events-subscribe-section" id="events-subscribe">
  <form id="events-subscribe-form" class="events-form" novalidate>
    <div class="events-form-email">
      <input
        type="email"
        id="subscribe-email"
        name="email"
        placeholder="your@email.com"
        required
        class="events-email-input"
      >
    </div>

    <fieldset class="events-form-checkboxes">
      <legend>Notify me about:</legend>
      <div class="events-checkbox-grid">
        {% for congress in congresses %}
          <label class="events-checkbox-label">
            <input
              type="checkbox"
              name="congress"
              value="{{ congress.id }}"
              checked
            >
            <span>{{ congress.short_name }}</span>
          </label>
        {% endfor %}
      </div>
    </fieldset>

    <button type="submit" class="events-submit-btn" id="subscribe-btn">
      Subscribe
    </button>

    <p class="events-form-note">
      You can unsubscribe at any time via the link in any email you receive.
    </p>
  </form>

  <div class="events-form-success" id="subscribe-success" style="display:none;">
    <p>&#10003; Check your inbox to confirm your subscription.</p>
  </div>

  <div class="events-form-error" id="subscribe-error" style="display:none;">
    <p>Something went wrong. Please try again or email me directly.</p>
  </div>
</div>

</div>

<script>
  window.BUTTONDOWN_USERNAME = "{{ site.buttondown_username }}";
  window.BUTTONDOWN_API_KEY  = "{{ site.buttondown_api_key }}";
</script>
<script defer src="{{ '/assets/js/events-subscribe.js' | relative_url | bust_file_cache }}"></script>
