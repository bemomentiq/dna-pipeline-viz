#!/usr/bin/env node
/**
 * Refresh data/roadmap.json from a source-of-truth audit doc in bemomentiq/momentiq-dna.
 *
 * Strategy:
 *   1. If `ROADMAP_SOURCE_URL` is set, fetch JSON or markdown from there.
 *   2. Else try the latest audit doc on `main` via the GitHub raw URL.
 *   3. Parse counts (shipped / wiring / not started / total) and (optionally) phase
 *      + gap blocks tagged in the doc.
 *   4. Rewrite data/roadmap.json, preserving any phases/gaps already there if the
 *      source does not provide them.
 *
 * Usage:
 *   node scripts/snapshot-roadmap.mjs
 *
 * Auth-free: hits raw.githubusercontent.com on the public repo. For higher rate
 * limits set GITHUB_TOKEN.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const dataPath = path.join(__dirname, '..', 'data', 'roadmap.json');

const SOURCE_REPO = 'bemomentiq/momentiq-dna';
const DEFAULT_DOC = 'docs/codebase-vs-roadmap.md';
const SOURCE_URL =
  process.env.ROADMAP_SOURCE_URL ||
  `https://raw.githubusercontent.com/${SOURCE_REPO}/main/${DEFAULT_DOC}`;

async function main() {
  const today = new Date().toISOString().slice(0, 10);
  const headers = {};
  if (process.env.GITHUB_TOKEN) headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`;

  let raw = '';
  try {
    const res = await fetch(SOURCE_URL, { headers });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    raw = await res.text();
  } catch (err) {
    console.warn(`[snapshot] could not fetch ${SOURCE_URL}: ${err.message}`);
    console.warn('[snapshot] keeping existing data/roadmap.json');
    return;
  }

  // If the source happens to be JSON — drop in directly
  let next;
  try {
    next = JSON.parse(raw);
  } catch {
    next = parseMarkdown(raw);
  }

  if (!next) {
    console.warn('[snapshot] could not parse source; leaving data/roadmap.json untouched');
    return;
  }

  const existing = fs.existsSync(dataPath)
    ? JSON.parse(fs.readFileSync(dataPath, 'utf8'))
    : null;

  const merged = {
    capturedAt: next.capturedAt || today,
    totals: next.totals || existing?.totals || { shipped: 0, wiring: 0, notstarted: 0, total: 0 },
    source: { ...(existing?.source || {}), ...(next.source || {}), repo: SOURCE_REPO },
    phases: next.phases?.length ? next.phases : existing?.phases || [],
    topGaps: next.topGaps?.length ? next.topGaps : existing?.topGaps || [],
  };

  fs.writeFileSync(dataPath, JSON.stringify(merged, null, 2) + '\n');
  console.log(
    `[snapshot] wrote data/roadmap.json @ ${merged.capturedAt} ` +
      `(${merged.totals.shipped}/${merged.totals.wiring}/${merged.totals.notstarted} of ${merged.totals.total})`
  );
}

function parseMarkdown(md) {
  const totals = { shipped: 0, wiring: 0, notstarted: 0, total: 0 };

  const m = (re) => (md.match(re) || [])[1];
  totals.shipped = +(m(/Shipped[^\d]*(\d+)/i) || 0);
  totals.wiring = +(m(/Wiring(?:\s+incomplete)?[^\d]*(\d+)/i) || 0);
  totals.notstarted = +(m(/Not\s+started[^\d]*(\d+)/i) || 0);
  totals.total = +(m(/Total\s+claims?[^\d]*(\d+)/i) || 0);
  if (!totals.total) {
    totals.total = totals.shipped + totals.wiring + totals.notstarted;
  }
  if (!totals.total) return null;
  return { totals };
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
