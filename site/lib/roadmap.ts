import fs from 'node:fs';
import path from 'node:path';

export type Phase = {
  id: string;
  title: string;
  status: 'shipped' | 'wiring' | 'notstarted' | 'inprog' | 'unknown';
  meta?: string;
  items: string[];
};

export type Gap = { title: string; detail: string };

export type RoadmapSnapshot = {
  capturedAt: string;
  totals: { shipped: number; wiring: number; notstarted: number; total: number };
  phases: Phase[];
  topGaps: Gap[];
  source: { repo: string; commit?: string; pr?: string; doc?: string };
};

const DATA_PATH = path.join(process.cwd(), 'data', 'roadmap.json');

export function loadRoadmap(): RoadmapSnapshot {
  if (fs.existsSync(DATA_PATH)) {
    return JSON.parse(fs.readFileSync(DATA_PATH, 'utf8')) as RoadmapSnapshot;
  }
  return {
    capturedAt: '2026-04-30',
    totals: { shipped: 33, wiring: 9, notstarted: 9, total: 51 },
    phases: [],
    topGaps: [],
    source: {
      repo: 'bemomentiq/momentiq-dna',
      pr: '#255',
      doc: 'docs/codebase-vs-roadmap-2026-04-30.md',
    },
  };
}
