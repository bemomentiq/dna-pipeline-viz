# dna-pipeline-site

Structured, modularized Next.js 15 site for the MomentIQ DNA Pipeline.

- **Home** — live roadmap dashboard (auto-refreshed daily from `bemomentiq/momentiq-dna`) + 7-layer entry grid
- **7 layers** — Overview · Architecture · Bandits & Reward · Quality & Gates · Operations · Reference (and Home/Roadmap)
- **30 drilldown pages** — one per section from the original 33-section walkthrough, each its own modular file under `app/<layer>/<slug>/page.tsx`
- **Static export** — `output: 'export'`, deployable as a flat folder

## Layout

```
app/
  layout.tsx           shared chrome (topbar nav, footer, theme)
  globals.css          design tokens + components
  page.tsx             Home — roadmap dashboard + layer grid
  overview/            layer index + drilldowns (loop, flow, phases, hub)
  architecture/        stack, configs, schema, api, integration
  bandits/             thompson, reward, categories, convergence, compounder
  quality/             gates, invariants, monitoring, rollout, governance
  operations/          cron, trace, failures, quickstart, roas, cost-roi
  reference/           glossary, sota-gap, impl, build-plan, gameplan
components/
  RoadmapDashboard.tsx home dashboard (totals, phases, gap list)
  SectionGrid.tsx      reusable layer / section grid
data/
  roadmap.json         daily snapshot (refreshed by scripts/snapshot-roadmap.mjs)
lib/
  ia.ts                IA map (layers + sections, single source of truth)
  roadmap.ts           snapshot loader
scripts/
  snapshot-roadmap.mjs daily refresh script — pulls audit doc from momentiq-dna
```

## Local dev

```bash
cd site
npm install
npm run dev          # localhost:3000
npm run snapshot     # refresh data/roadmap.json from upstream audit doc
npm run build        # static export → out/
```

## Auto-refresh

`.github/workflows/snapshot.yml` runs daily at 13:00 UTC, hits the audit doc on
`bemomentiq/momentiq-dna` `main`, rewrites `site/data/roadmap.json`, and commits
back if anything changed.

`.github/workflows/build-site.yml` validates the static export on every push to
`site/**`.

## Editing content

Each section is its own file:

```
app/<layer>/<slug>/page.tsx
```

Layers and section metadata live in [`lib/ia.ts`](./lib/ia.ts) — adding a new
section means appending one entry there and creating the page file.

The legacy 33-section walkthrough is preserved at the repo root under
[`v1-walkthrough/`](../v1-walkthrough/) and the dated dashboard at
[`v2-roadmap-2026-04-30/`](../v2-roadmap-2026-04-30/).
