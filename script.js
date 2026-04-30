// Theme toggle
(function () {
  const t = document.querySelector('[data-theme-toggle]');
  const r = document.documentElement;
  let d = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';

  function render() {
    r.setAttribute('data-theme', d);
    if (!t) return;
    t.setAttribute('aria-label', 'Switch to ' + (d === 'dark' ? 'light' : 'dark') + ' mode');
    t.innerHTML =
      d === 'dark'
        ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
        : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  }
  render();
  if (t) {
    t.addEventListener('click', () => {
      d = d === 'dark' ? 'light' : 'dark';
      render();
    });
  }
})();

// Flow node → scroll to phase detail
(function () {
  document.querySelectorAll('.node').forEach((node) => {
    node.addEventListener('click', () => {
      const phase = node.getAttribute('data-phase');
      const target = document.getElementById('phase-' + phase);
      if (!target) return;
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      // Highlight briefly
      target.animate(
        [
          { boxShadow: '0 0 0 0 rgba(1,105,111,0.55)', transform: 'translateY(0)' },
          { boxShadow: '0 0 0 16px rgba(1,105,111,0)', transform: 'translateY(-2px)' },
          { boxShadow: '0 0 0 0 rgba(1,105,111,0)', transform: 'translateY(0)' },
        ],
        { duration: 1200, easing: 'cubic-bezier(0.16, 1, 0.3, 1)' }
      );
    });
  });
})();

// Config tab switcher
(function () {
  const groups = document.querySelectorAll('[data-tabs]');
  groups.forEach((group) => {
    const name = group.getAttribute('data-tabs');
    const tabs = group.querySelectorAll('.tab');
    const panels = document.querySelectorAll('[data-panel]');
    tabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        const target = tab.getAttribute('data-tab');
        tabs.forEach((t) => {
          t.classList.remove('tab-active');
          t.setAttribute('aria-selected', 'false');
        });
        tab.classList.add('tab-active');
        tab.setAttribute('aria-selected', 'true');
        panels.forEach((p) => {
          if (p.getAttribute('data-panel') === target) {
            p.classList.add('tab-panel-active');
            p.hidden = false;
          } else {
            p.classList.remove('tab-panel-active');
            p.hidden = true;
          }
        });
      });
    });
  });
})();

// Reveal-on-scroll for phase cards
(function () {
  if (!('IntersectionObserver' in window)) return;
  const items = document.querySelectorAll('.phase, .kpi, .schema-card, .cron-card, .rules li, .config-card, .arch-box, .cat-card, .bandit-card, .roadmap-phase, .metric, .arch-note, .reward-step, .reward-example, .reward-guard, .gate-card, .trace-stop, .api-card, .trace-attr, .gov-card, .ramp-step, .gloss, .qs-card, .monitor-table tr, .sota-table tbody tr, .compounder-card, .curr-phase, .hier-level, .roas-mech, .rfs, .conv-node, .conv-metric, .callout, .impl-card, .cost-card, .tier-card, .lever-card, .fclass, .cb-card, .ks-card, .int-node, .int-rule, .impl-slo, .impl-trace, .ledger-schema');
  items.forEach((el) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(12px)';
    el.style.transition = 'opacity 500ms cubic-bezier(0.16, 1, 0.3, 1), transform 500ms cubic-bezier(0.16, 1, 0.3, 1)';
  });
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          io.unobserve(entry.target);
        }
      });
    },
    { rootMargin: '0px 0px -8% 0px', threshold: 0.1 }
  );
  items.forEach((el) => io.observe(el));

  // Reveal any elements already visible on initial render (fixes hash-anchor navigation
  // where IO has no scroll event to trigger on).
  requestAnimationFrame(() => {
    const vh = window.innerHeight || document.documentElement.clientHeight;
    items.forEach((el) => {
      const rect = el.getBoundingClientRect();
      if (rect.top < vh && rect.bottom > 0) {
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      }
    });
  });
})();

// Gameplan filter bar + completion progress reconciliation
(function () {
  const filtersEl = document.getElementById('gp-filters');
  if (!filtersEl) return;
  const statusEl = document.getElementById('gp-filter-status');
  const resetBtn = document.getElementById('gp-filter-reset');
  const rows = Array.from(document.querySelectorAll('#gameplan tr[data-status]'));
  const total = rows.length;

  const active = { priority: 'all', lane: 'all', status: 'all', mini: 'all' };

  function apply() {
    let visible = 0;
    rows.forEach((row) => {
      const statusOk =
        active.status === 'all' ||
        (active.status === 'remaining' ? row.dataset.status !== 'done' : row.dataset.status === active.status);
      const ok =
        (active.priority === 'all' || row.dataset.priority === active.priority) &&
        (active.lane === 'all' || row.dataset.lane === active.lane) &&
        statusOk &&
        (active.mini === 'all' || row.dataset.mini === active.mini);
      row.classList.toggle('gp-row-hidden', !ok);
      if (ok) visible++;
    });

    // Mark empty milestones
    document.querySelectorAll('#gameplan .gp-milestone').forEach((ms) => {
      const anyVisible = ms.querySelectorAll('tr[data-status]:not(.gp-row-hidden)').length > 0;
      ms.classList.toggle('gp-ms-empty', !anyVisible);
    });

    const parts = Object.entries(active).filter(([, v]) => v !== 'all').map(([k, v]) => {
      if (k === 'priority') return v.toUpperCase();
      if (k === 'status' && v === 'remaining') return 'remaining only';
      return v;
    });
    if (parts.length === 0) {
      statusEl.textContent = `Showing all ${total} tasks`;
    } else {
      statusEl.textContent = `Showing ${visible} of ${total} tasks · filtered by ${parts.join(' · ')}`;
    }

    // Sync active chip states per group
    filtersEl.querySelectorAll('[data-filter]').forEach((chip) => {
      const group = chip.getAttribute('data-filter');
      const val = chip.getAttribute('data-value');
      const isActive = active[group] === val;
      chip.classList.toggle('gp-filter-active', isActive);
      chip.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });
  }

  filtersEl.addEventListener('click', (e) => {
    const chip = e.target.closest('[data-filter]');
    if (!chip) return;
    const group = chip.getAttribute('data-filter');
    const val = chip.getAttribute('data-value');
    active[group] = val;
    apply();
  });

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      active.priority = 'all';
      active.lane = 'all';
      active.status = 'all';
      active.mini = 'all';
      apply();
    });
  }

  // Reconcile completion card from actual DOM counts (keeps values honest)
  const done = rows.filter((r) => r.dataset.status === 'done').length;
  const numEl = document.getElementById('gp-progress-num');
  const fillEl = document.getElementById('gp-progress-fill');
  const pctEl = document.getElementById('gp-progress-pct');
  const pct = total > 0 ? (done / total) * 100 : 0;
  if (numEl) numEl.textContent = String(done);
  if (fillEl) fillEl.style.width = pct.toFixed(1) + '%';
  if (pctEl) pctEl.textContent = Math.round(pct) + '%';
  const meta = document.querySelector('.gp-summary-progress .gp-summary-meta');
  if (meta) meta.innerHTML = `<span id="gp-progress-pct">${Math.round(pct)}%</span> shipped · ${total - done} remaining`;

  apply();
})();
