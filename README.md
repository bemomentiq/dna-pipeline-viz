# DNA Pipeline Viz

The original visualization of the MomentIQ DNA Engine roadmap — a single static
page that walks through the full Kalodata → AI Content Platform training
pipeline (overview, flow, phases, architecture, configs, categories, bandits,
roadmap, reward, gates, trace, API, governance, monitoring, rollout, glossary,
quickstart, schema, cron, invariants, SOTA gap, compounder, ROAS, convergence,
implementation, cost/ROI, failures, integration, build plan, gameplan).

This is the seed artifact from which the [DNA Autonomy Hub](https://github.com/bemomentiq/momentiq-dna)
multi-page Next.js platform was later derived.

## Structure

```
index.html        ← built artifact (do not edit directly)
style.css         ← base styles
refine.css        ← layout + section refinements
script.js         ← lightweight client logic (anchors, toggles)
partials/         ← source of truth: one file per section, lexicographic order
build.py          ← concatenates partials/*.html → index.html
split.py          ← one-time bootstrap tool (do not re-run)
```

## Build

```bash
python3 build.py
```

Reads every `partials/NNN-name.html` (sorted) and writes `index.html` at the
project root. Each partial is fronted with an HTML comment marker for
traceability.

## Edit workflow

1. Edit a partial in `partials/` (e.g. `100-roadmap.html`).
2. Run `python3 build.py`.
3. Open `index.html` locally or deploy as a static site.

## Notes

- The NBSP (`\u00a0`) inside `schema\u00a0ready` must be preserved.
- `build.py` is intentionally dumb — no templating, no variables; ordering
  comes purely from the numeric prefix.
- Successor: the multi-page hub at [bemomentiq/momentiq-dna](https://github.com/bemomentiq/momentiq-dna)
  (Next.js 15, deployed as `dna-pipeline-viz`).
