/**
 * Information architecture map.
 * 7 layers · 33 v1 sections + v2 roadmap dashboard at the top of Home.
 * Drilldowns live under each layer route.
 */
import type { SectionLink } from '@/components/SectionGrid';

export const LAYERS: { slug: string; title: string; blurb: string; sections: SectionLink[] }[] = [
  {
    slug: 'overview',
    title: 'Overview',
    blurb: 'How the loop works, end-to-end. The hub, the flow, the phase-by-phase walkthrough.',
    sections: [
      { href: '/overview/loop/', title: 'The closed loop', blurb: 'Closed-loop training, not a one-shot ETL.' },
      { href: '/overview/flow/', title: 'The full flow', blurb: 'The full loop, in one pane.' },
      { href: '/overview/phases/', title: 'Phase walkthrough', blurb: 'What actually happens at each node.' },
      { href: '/overview/hub/', title: 'Pipeline hub', blurb: 'Where to start. Top-level navigation across the engine.' },
    ],
  },
  {
    slug: 'architecture',
    title: 'Architecture',
    blurb: 'Where DNA lives in the stack — configs, schema, APIs, integrations.',
    sections: [
      { href: '/architecture/stack/', title: 'Stack placement', blurb: 'Where DNA lives across services and stores.' },
      { href: '/architecture/configs/', title: 'Configs', blurb: 'Every DNA knob, by content surface.' },
      { href: '/architecture/schema/', title: 'Schema', blurb: 'Net-new database surface in Neon.' },
      { href: '/architecture/api/', title: 'API surface', blurb: 'All `/api/v1/dna/*` endpoints.' },
      { href: '/architecture/integration/', title: 'Integrations', blurb: 'Kalodata, content platform, Reacher, Veo.' },
    ],
  },
  {
    slug: 'bandits',
    title: 'Bandits & Reward',
    blurb: 'Per-attribute × category Thompson sampling, reward shape, and category drift.',
    sections: [
      { href: '/bandits/thompson/', title: 'Thompson sampling', blurb: 'Posteriors per attribute × category.' },
      { href: '/bandits/reward/', title: 'Reward shape', blurb: 'How live performance rewires the bandits.' },
      { href: '/bandits/categories/', title: 'Category drift', blurb: 'DNA shifts per category.' },
      { href: '/bandits/convergence/', title: 'Convergence loop', blurb: 'Closed loop that converges on indistinguishability.' },
      { href: '/bandits/compounder/', title: 'Compounder', blurb: 'The generator gets better every week, not just the bandits.' },
    ],
  },
  {
    slug: 'quality',
    title: 'Quality & Gates',
    blurb: 'Nothing ships that hasn\'t cleared every gate. Invariants, monitoring, rollout, governance.',
    sections: [
      { href: '/quality/gates/', title: 'Gates', blurb: 'Nothing ships without clearing every gate.' },
      { href: '/quality/invariants/', title: 'Invariants', blurb: 'Non-negotiable rules the pipeline enforces.' },
      { href: '/quality/monitoring/', title: 'Monitoring', blurb: 'The 12 signals that keep the pipeline honest.' },
      { href: '/quality/rollout/', title: 'Rollout', blurb: 'From 0% canary to steady-state — the 5 promotion ramps.' },
      { href: '/quality/governance/', title: 'Governance', blurb: 'Roles, on-call, change control.' },
    ],
  },
  {
    slug: 'operations',
    title: 'Operations',
    blurb: 'Day-to-day: cron, traces, failures, quickstart, ROAS, cost/ROI.',
    sections: [
      { href: '/operations/cron/', title: 'Scheduled jobs', blurb: 'Crons that keep the loop alive.' },
      { href: '/operations/trace/', title: 'Trace', blurb: 'Every primary attribute, end-to-end.' },
      { href: '/operations/failures/', title: 'Failure modes', blurb: 'What breaks, how it surfaces, who fixes it.' },
      { href: '/operations/quickstart/', title: 'Quickstart', blurb: 'If something breaks — this card first.' },
      { href: '/operations/roas/', title: 'Portfolio ROAS', blurb: 'Brand → L3 → L2 → L1 → ecosystem.' },
      { href: '/operations/cost-roi/', title: 'Cost & ROI', blurb: 'Pipeline economics.' },
    ],
  },
  {
    slug: 'reference',
    title: 'Reference',
    blurb: 'Glossary, SOTA gap, implementation notes, build plan, gameplan.',
    sections: [
      { href: '/reference/glossary/', title: 'Glossary', blurb: 'Every term you\'ll see in the ledger.' },
      { href: '/reference/sota-gap/', title: 'SOTA gap', blurb: '27-capability delta vs 2024–2026 state-of-the-art.' },
      { href: '/reference/impl/', title: 'Implementation', blurb: 'How phases land in code.' },
      { href: '/reference/build-plan/', title: 'Build plan', blurb: 'Sprint-by-sprint plan to feature-complete.' },
      { href: '/reference/gameplan/', title: 'Gameplan', blurb: 'Production readiness gameplan.' },
    ],
  },
];

export function findLayer(slug: string) {
  return LAYERS.find((l) => l.slug === slug);
}
