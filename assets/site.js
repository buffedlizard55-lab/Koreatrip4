/* Korea Trip Desk UI — no external dependencies */
(function () {
  'use strict';

  var trip = window.KOREATRIP;
  if (!trip) return;

  var sourceById = {};
  trip.sourceRegister.forEach(function (source) { sourceById[source.id] = source; });

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function sourceLinks(ids) {
    if (!ids || !ids.length) return '<span class="no-source">No primary source identified</span>';
    return '<div class="source-list">' + ids.map(function (id) {
      var source = sourceById[id];
      if (!source) return '';
      return '<a class="source-chip" href="' + escapeHtml(source.url) + '" target="_blank" rel="noopener noreferrer" title="Open ' + escapeHtml(source.title) + '">' + escapeHtml(id) + '<span class="sr-only">: ' + escapeHtml(source.title) + '</span></a>';
    }).join('') + '</div>';
  }

  function statusLabel(status) {
    var labels = { verified: 'Verified', partial: 'Qualified', review: 'Flag for review', unverified: 'Unverified' };
    return labels[status] || 'Unverified';
  }

  function statusBadge(status) {
    var safe = ['verified', 'partial', 'review', 'unverified'].indexOf(status) > -1 ? status : 'unverified';
    return '<span class="status status-' + safe + '">' + statusLabel(safe) + '</span>';
  }

  function cell(primary, secondary) {
    return '<strong>' + escapeHtml(primary) + '</strong>' + (secondary ? '<span class="cell-secondary">' + escapeHtml(secondary) + '</span>' : '');
  }

  function rowSearch(item) {
    return Object.keys(item).filter(function (key) { return key !== 'sources'; }).map(function (key) {
      return typeof item[key] === 'string' ? item[key] : '';
    }).join(' ').toLowerCase();
  }

  function injectSiteChrome() {
    var page = document.body.getAttribute('data-page') || '';
    var nav = [
      ['index.html', 'Dashboard', 'home'],
      ['itinerary.html', 'Itinerary', 'itinerary'],
      ['transport.html', 'Transport', 'transport'],
      ['places.html', 'Places', 'places'],
      ['food-shopping.html', 'Food + shops', 'food'],
      ['sources.html', 'Sources', 'sources'],
      ['flagged.html', 'Review', 'review']
    ];
    var header = document.getElementById('site-header');
    if (header) {
      header.innerHTML = '<a class="skip-link" href="#main-content">Skip to content</a>' +
        '<div class="site-header"><div class="nav-shell">' +
          '<a class="brand" href="index.html" aria-label="Korea Trip Desk home"><span class="brand-mark" aria-hidden="true">◒</span><span><strong>Korea Trip Desk</strong><span>verified itinerary review</span></span></a>' +
          '<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav"><span aria-hidden="true">☰</span> Menu</button>' +
          '<nav id="primary-nav" class="primary-nav" aria-label="Primary navigation">' + nav.map(function (item) {
            var current = item[2] === page ? ' aria-current="page"' : '';
            var review = item[2] === 'review' ? ' nav-review' : '';
            return '<a class="' + review.trim() + '" href="' + item[0] + '"' + current + '>' + item[1] + '</a>';
          }).join('') + '</nav>' +
        '</div></div>';
      var toggle = header.querySelector('.nav-toggle');
      var menu = header.querySelector('.primary-nav');
      toggle.addEventListener('click', function () {
        var open = menu.classList.toggle('is-open');
        toggle.setAttribute('aria-expanded', String(open));
      });
    }
    var footer = document.getElementById('site-footer');
    if (footer) {
      footer.innerHTML = '<footer class="site-footer"><div class="container footer-grid">' +
        '<div><strong>Korea Trip Desk</strong><p>Research snapshot: ' + escapeHtml(trip.reviewedOn) + '. Facts shown as verified are tied to linked official or operator sources. Hours, routes, fares, closures and reservations can change — reconfirm before travel.</p></div>' +
        '<nav class="footer-links" aria-label="Footer navigation"><a href="sources.html">Source register</a><a href="flagged.html">Flagged for review</a><a href="https://github.com/buffedlizard55-lab/Koreatrip4" target="_blank" rel="noopener noreferrer">Project on GitHub</a></nav>' +
      '</div></footer>';
    }
  }

  function renderHome() {
    var stats = document.getElementById('dashboard-stats');
    var verified = trip.itineraryRows.filter(function (row) { return row.status === 'verified'; }).length;
    var review = trip.itineraryRows.filter(function (row) { return row.status === 'review'; }).length;
    var high = trip.flags.filter(function (flag) { return flag.priority === 'High'; }).length;
    if (stats) {
      stats.innerHTML = [
        ['08', 'itinerary days retained'],
        [String(trip.sourceRegister.length).padStart(2, '0'), 'linked source records'],
        [String(verified).padStart(2, '0'), 'source-backed itinerary rows'],
        [String(high).padStart(2, '0'), 'high-priority items to resolve']
      ].map(function (stat) {
        return '<article class="stat-card"><span class="number">' + stat[0] + '</span><p>' + stat[1] + '</p></article>';
      }).join('');
    }
    var cards = document.getElementById('day-cards');
    if (cards) {
      cards.innerHTML = trip.dayCards.map(function (day) {
        return '<a class="day-card" href="itinerary.html#day-' + escapeHtml(day.day) + '">' +
          '<span class="day-no">DAY ' + escapeHtml(day.day) + ' · ' + escapeHtml(day.city) + '</span>' +
          '<h3>' + escapeHtml(day.label) + '</h3><p>' + escapeHtml(day.detail) + '</p>' +
          '<span class="day-status">' + (day.state === 'verified' ? 'Source-backed core stops' : escapeHtml(day.flag)) + '</span>' +
        '</a>';
      }).join('');
    }
    var quick = document.getElementById('dashboard-quick');
    if (quick) {
      quick.innerHTML = [
        ['↗', 'Read the itinerary', 'Every supplied stop, with only source-supported operating facts.', 'itinerary.html'],
        ['⇄', 'Check public transport', 'Airport, tower, rail and Busan routing separated from unsupported timing claims.', 'transport.html'],
        ['!', 'Resolve review items', 'Dates, flight, KTX details and ambiguous venue identities are held visibly open.', 'flagged.html']
      ].map(function (card) {
        return '<article class="route-card"><span class="route-icon" aria-hidden="true">' + card[0] + '</span><h3>' + card[1] + '</h3><p>' + card[2] + '</p><a class="text-link" href="' + card[3] + '">Open</a></article>';
      }).join('');
    }
  }

  function renderItinerary() {
    var target = document.getElementById('itinerary-table');
    if (!target) return;
    var seenDays = {};
    var html = '<div class="table-shell"><table><caption>Each row preserves the planned stop; linked sources support only the specific statement in the verification column.</caption><thead><tr><th>Day</th><th>Planned stop</th><th>Verification finding</th><th>Location &amp; hours</th><th>Status</th><th>Official source</th></tr></thead><tbody>';
    trip.itineraryRows.forEach(function (row) {
      var anchor = !seenDays[row.day] ? ' id="day-' + escapeHtml(row.day) + '"' : '';
      seenDays[row.day] = true;
      html += '<tr' + anchor + ' data-status="' + escapeHtml(row.status) + '" data-search="' + escapeHtml(rowSearch(row)) + '">' +
        '<td class="day-cell">DAY ' + escapeHtml(row.day) + '<span class="cell-secondary">' + escapeHtml(row.time) + '</span></td>' +
        '<td>' + cell(row.plan, row.type) + '</td>' +
        '<td>' + escapeHtml(row.finding) + '<span class="cell-secondary">' + escapeHtml(row.note) + '</span></td>' +
        '<td>' + cell(row.location, row.hours) + '</td>' +
        '<td>' + statusBadge(row.status) + '</td>' +
        '<td>' + sourceLinks(row.sources) + '</td>' +
      '</tr>';
    });
    html += '</tbody></table></div>';
    target.innerHTML = html;
    makeFilters(target, 'itinerary');
  }

  function renderPlaces() {
    var target = document.getElementById('places-table');
    if (!target) return;
    var html = '<div class="table-shell"><table><caption>Core stays and attractions with the official facts that can be safely carried into the plan.</caption><thead><tr><th>City</th><th>Place</th><th>Confirmed fact</th><th>Access / timing note</th><th>Status</th><th>Official source</th></tr></thead><tbody>';
    trip.placeRows.forEach(function (row) {
      html += '<tr data-status="' + escapeHtml(row.status) + '" data-search="' + escapeHtml(rowSearch(row)) + '">' +
        '<td>' + escapeHtml(row.city) + '</td><td>' + cell(row.place, row.category) + '</td><td>' + escapeHtml(row.verified) + '</td>' +
        '<td>' + cell(row.access, row.hours) + '</td><td>' + statusBadge(row.status) + '</td><td>' + sourceLinks(row.sources) + '</td></tr>';
    });
    target.innerHTML = html + '</tbody></table></div>';
    makeFilters(target, 'places');
  }

  function renderFoodShopping() {
    var target = document.getElementById('food-shopping-table');
    if (!target) return;
    var html = '<div class="table-shell"><table><caption>Restaurant, café, market, activity and shopping entries. A name alone does not establish a particular branch.</caption><thead><tr><th>Area</th><th>Planned venue</th><th>Confirmed fact</th><th>Hours</th><th>Status</th><th>Official source</th></tr></thead><tbody>';
    trip.foodShoppingRows.forEach(function (row) {
      html += '<tr data-status="' + escapeHtml(row.status) + '" data-search="' + escapeHtml(rowSearch(row)) + '">' +
        '<td>' + escapeHtml(row.area) + '</td><td>' + cell(row.item, row.kind) + '</td><td>' + escapeHtml(row.verified) + '</td>' +
        '<td>' + escapeHtml(row.hours) + '</td><td>' + statusBadge(row.status) + '</td><td>' + sourceLinks(row.sources) + '</td></tr>';
    });
    target.innerHTML = html + '</tbody></table></div>';
    makeFilters(target, 'food');
  }

  function renderTransport() {
    var target = document.getElementById('transport-table');
    if (!target) return;
    var html = '<div class="table-shell"><table><caption>Routes are phrased conservatively. Live schedules and selected terminals/stations still need a traveler check.</caption><thead><tr><th>Leg</th><th>Mode</th><th>Official guidance</th><th>Traveler action</th><th>Status</th><th>Official source</th></tr></thead><tbody>';
    trip.transitRows.forEach(function (row) {
      html += '<tr data-status="' + escapeHtml(row.status) + '" data-search="' + escapeHtml(rowSearch(row)) + '">' +
        '<td>' + cell(row.leg) + '</td><td>' + escapeHtml(row.mode) + '</td><td>' + escapeHtml(row.officialGuidance) + '</td>' +
        '<td>' + escapeHtml(row.action) + '</td><td>' + statusBadge(row.status) + '</td><td>' + sourceLinks(row.sources) + '</td></tr>';
    });
    target.innerHTML = html + '</tbody></table></div>';
    makeFilters(target, 'transport');
  }

  function renderSources() {
    var target = document.getElementById('sources-table');
    if (!target) return;
    var html = '<div class="table-shell"><table class="source-table"><caption>Official, public-authority, tourism-authority and operator sources reviewed for this dashboard.</caption><thead><tr><th>ID</th><th>Publisher / source</th><th>What this dashboard relies on</th><th>Checked</th></tr></thead><tbody>';
    trip.sourceRegister.forEach(function (source) {
      html += '<tr data-search="' + escapeHtml(rowSearch(source)) + '"><td><span class="source-id">' + escapeHtml(source.id) + '</span></td>' +
        '<td><strong><a href="' + escapeHtml(source.url) + '" target="_blank" rel="noopener noreferrer">' + escapeHtml(source.title) + '</a></strong><span class="source-meta">' + escapeHtml(source.publisher) + '</span><span class="source-url">' + escapeHtml(source.url) + '</span></td>' +
        '<td>' + escapeHtml(source.claims) + '</td><td>' + escapeHtml(source.checked) + '</td></tr>';
    });
    target.innerHTML = html + '</tbody></table></div>';
    makeSearchOnly(target, 'sources');
  }

  function renderFlags() {
    var target = document.getElementById('flag-list');
    if (!target) return;
    target.innerHTML = trip.flags.map(function (flag, index) {
      var priorityClass = flag.priority.toLowerCase();
      var anchor = index === 0 ? ' id="date-conflict"' : '';
      return '<article' + anchor + ' class="flag-card" data-priority="' + escapeHtml(flag.priority) + '" data-search="' + escapeHtml(rowSearch(flag)) + '">' +
        '<div><span class="priority priority-' + priorityClass + '">' + escapeHtml(flag.priority) + '</span></div>' +
        '<div><p class="flag-label">Issue</p><h3>' + escapeHtml(flag.issue) + '</h3></div>' +
        '<div><p class="flag-label">Why it matters</p><p>' + escapeHtml(flag.detail) + '<br><br><strong>Impact:</strong> ' + escapeHtml(flag.impact) + '</p></div>' +
        '<div><p class="flag-label">Resolve before booking</p><p>' + escapeHtml(flag.resolve) + '</p></div>' +
        sourceLinks(flag.sources) +
      '</article>';
    }).join('');
    makeFlagFilters(target);
  }

  function filterControls(statuses, label) {
    var buttons = [['all', 'All'], ['verified', 'Verified'], ['partial', 'Qualified'], ['review', 'Review']];
    return '<div class="filter-bar" data-filter-for="' + label + '"><span>Filter rows</span>' + buttons.map(function (button, index) {
      return '<button type="button" class="filter-button' + (index === 0 ? ' is-active' : '') + '" data-filter="' + button[0] + '">' + button[1] + '</button>';
    }).join('') + '<label class="search-field"><span class="sr-only">Search rows</span><input type="search" placeholder="Search ' + label + '" aria-label="Search ' + label + '"></label></div><p class="results-note" aria-live="polite"></p>';
  }

  function makeFilters(target, label) {
    var controls = document.createElement('div');
    controls.innerHTML = filterControls(['verified', 'partial', 'review'], label);
    target.parentNode.insertBefore(controls, target);
    var bar = controls.querySelector('.filter-bar');
    var input = controls.querySelector('input');
    var note = controls.querySelector('.results-note');
    var active = 'all';
    function apply() {
      var query = input.value.trim().toLowerCase();
      var rows = Array.prototype.slice.call(target.querySelectorAll('tbody tr'));
      var visible = 0;
      rows.forEach(function (row) {
        var statusMatches = active === 'all' || row.getAttribute('data-status') === active;
        var queryMatches = !query || row.getAttribute('data-search').indexOf(query) > -1;
        var show = statusMatches && queryMatches;
        row.hidden = !show;
        if (show) visible += 1;
      });
      note.textContent = visible + ' matching ' + (visible === 1 ? 'row' : 'rows') + '.';
    }
    bar.addEventListener('click', function (event) {
      var button = event.target.closest('[data-filter]');
      if (!button) return;
      active = button.getAttribute('data-filter');
      Array.prototype.forEach.call(bar.querySelectorAll('[data-filter]'), function (item) { item.classList.toggle('is-active', item === button); });
      apply();
    });
    input.addEventListener('input', apply);
    apply();
  }

  function makeSearchOnly(target, label) {
    var controls = document.createElement('div');
    controls.innerHTML = '<div class="filter-bar"><span>Search sources</span><label class="search-field"><span class="sr-only">Search ' + label + '</span><input type="search" placeholder="Search publisher, topic or ID" aria-label="Search ' + label + '"></label></div><p class="results-note" aria-live="polite"></p>';
    target.parentNode.insertBefore(controls, target);
    var input = controls.querySelector('input');
    var note = controls.querySelector('.results-note');
    function apply() {
      var query = input.value.trim().toLowerCase();
      var rows = Array.prototype.slice.call(target.querySelectorAll('tbody tr'));
      var visible = 0;
      rows.forEach(function (row) {
        var show = !query || row.getAttribute('data-search').indexOf(query) > -1;
        row.hidden = !show;
        if (show) visible += 1;
      });
      note.textContent = visible + ' matching ' + (visible === 1 ? 'source' : 'sources') + '.';
    }
    input.addEventListener('input', apply);
    apply();
  }

  function makeFlagFilters(target) {
    var controls = document.createElement('div');
    controls.innerHTML = '<div class="filter-bar"><span>Filter issues</span><button type="button" class="filter-button is-active" data-filter="all">All</button><button type="button" class="filter-button" data-filter="High">High</button><button type="button" class="filter-button" data-filter="Medium">Medium</button><button type="button" class="filter-button" data-filter="Low">Low</button><label class="search-field"><span class="sr-only">Search issues</span><input type="search" placeholder="Search issues" aria-label="Search issues"></label></div><p class="results-note" aria-live="polite"></p>';
    target.parentNode.insertBefore(controls, target);
    var bar = controls.querySelector('.filter-bar');
    var input = controls.querySelector('input');
    var note = controls.querySelector('.results-note');
    var active = 'all';
    function apply() {
      var query = input.value.trim().toLowerCase();
      var cards = Array.prototype.slice.call(target.querySelectorAll('.flag-card'));
      var visible = 0;
      cards.forEach(function (card) {
        var priorityMatches = active === 'all' || card.getAttribute('data-priority') === active;
        var queryMatches = !query || card.getAttribute('data-search').indexOf(query) > -1;
        var show = priorityMatches && queryMatches;
        card.hidden = !show;
        if (show) visible += 1;
      });
      note.textContent = visible + ' matching ' + (visible === 1 ? 'issue' : 'issues') + '.';
    }
    bar.addEventListener('click', function (event) {
      var button = event.target.closest('[data-filter]');
      if (!button) return;
      active = button.getAttribute('data-filter');
      Array.prototype.forEach.call(bar.querySelectorAll('[data-filter]'), function (item) { item.classList.toggle('is-active', item === button); });
      apply();
    });
    input.addEventListener('input', apply);
    apply();
  }

  document.addEventListener('DOMContentLoaded', function () {
    injectSiteChrome();
    renderHome();
    renderItinerary();
    renderTransport();
    renderPlaces();
    renderFoodShopping();
    renderSources();
    renderFlags();
  });
}());
