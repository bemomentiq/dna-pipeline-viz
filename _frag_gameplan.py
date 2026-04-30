#!/usr/bin/env python3
"""Inject #gameplan section + nav link + styles into the DNA viz monolith.

Idempotent: re-running replaces existing gameplan section.
"""
from pathlib import Path
import re

ROOT = Path(__file__).parent
HTML = ROOT / "index.html"
CSS = ROOT / "style.css"

# ------------------------------------------------------------------
# Task board data — merges VIZ (5) + DNA M10-M13 (33) = 38 tasks total
# ------------------------------------------------------------------
TASKS = [
    # VIZ — modularization sprint (parallel to DNA build kickoff)
    ("VIZ.1", "Scaffold Vite + tokens.css + base.css + app shell", "viz", "p0", "codex", "mini-1", "S", "—",                "Fleet-ready"),
    ("VIZ.2", "Extract sections 1-7 (hero→bandits) into modules",   "viz", "p0", "codex", "mini-2", "M", "VIZ.1",           "Fleet-ready"),
    ("VIZ.3", "Extract sections 8-14 (roadmap→monitoring)",          "viz", "p0", "codex", "mini-3", "M", "VIZ.1",           "Fleet-ready"),
    ("VIZ.4", "Extract sections 15-22 (rollout→integration)",        "viz", "p0", "codex", "mini-4", "M", "VIZ.1",           "Fleet-ready"),
    ("VIZ.5", "Integrate + screenshot-diff parity + extract hub/buildplan", "viz", "p0", "claude", "mini-5", "L", "VIZ.2, VIZ.3, VIZ.4", "Fleet-ready"),

    # M10 — SOTA Training Pipeline (8)
    ("M10.1", "Create dna_training_corpus + dna_features tables",    "infra", "p0", "codex",  "mini-1", "S", "—",                  "Planned"),
    ("M10.2", "Build dna-kalodata-harvester service",                "training", "p0", "codex",  "mini-2", "M", "M10.1",             "Planned"),
    ("M10.3", "Build dna-cloudinary-uploader service",               "training", "p0", "codex",  "mini-3", "M", "M10.1",             "Planned"),
    ("M10.4", "Build dna-ingest event handler",                      "training", "p0", "codex",  "mini-4", "M", "M10.2, M10.3",      "Planned"),
    ("M10.5", "Judge ensemble: fidelity + naturalness scorers",      "judge",    "p1", "claude", "mini-5", "L", "M10.4",             "Planned"),
    ("M10.6", "Judge ensemble: commerce + diversity + safety",       "judge",    "p1", "claude", "mini-5", "L", "M10.4",             "Planned"),
    ("M10.7", "dna-feature-extractor (visual/audio/hook vectors)",   "training", "p1", "claude", "mini-4", "L", "M10.4",             "Planned"),
    ("M10.8", "OTel traces + SLO publishing for M10 services",       "obs",      "p2", "codex",  "mini-1", "M", "M10.5",             "Planned"),

    # M11 — Autonomous A/B + OPE (12)
    ("M11.1", "Create dna_arms + dna_scores + dna_bandit_state",     "infra", "p0", "codex",  "mini-1", "S", "M10.1",                "Planned"),
    ("M11.2", "LinTS contextual bandit router (service)",            "ab",    "p0", "claude", "mini-5", "XL","M11.1",                "Planned"),
    ("M11.3", "dna-ope-estimator (Doubly-Robust IPS)",               "ab",    "p0", "claude", "mini-4", "L", "M11.1",                "Planned"),
    ("M11.4", "dna-nightly-distill (LoRA fine-tune loop)",           "training","p0","claude", "mini-3", "L", "M10.5",                "Planned"),
    ("M11.5", "dna-rollout-controller (canary + auto-revert)",       "ab",    "p0", "codex",  "mini-2", "L", "M11.3",                "Planned"),
    ("M11.6", "POST /api/v1/dna/config/promote + active_config_view","ab",    "p0", "codex",  "mini-1", "M", "M11.5",                "Planned"),
    ("M11.7", "Guard-sweep service (kill switches)",                 "ab",    "p0", "codex",  "mini-2", "M", "M11.5",                "Planned"),
    ("M11.8", "CC integration — issue-sync cron",                    "infra", "p1", "codex",  "mini-3", "M", "—",                    "Planned"),
    ("M11.9", "PR Guardian fork for momentiq-dna",                   "infra", "p1", "codex",  "mini-4", "S", "—",                    "Planned"),
    ("M11.10","Perplexity cron registry (6 crons)",                  "infra", "p1", "codex",  "mini-1", "S", "M11.6",                "Planned"),
    ("M11.11","Protobuf contracts for dna-sdk",                      "obs",   "p1", "codex",  "mini-2", "M", "M11.2",                "Planned"),
    ("M11.12","Canary dashboard UI",                                 "ab",    "p2", "codex",  "mini-3", "M", "M11.5",                "Planned"),

    # M12 — Multi-Level ROAS + Convergence (7)
    ("M12.1", "Hierarchical arms schema (brand × L1 × L2 × L3)",     "roas",        "p0", "codex",  "mini-1", "M", "M11.1",           "Planned"),
    ("M12.2", "7-dim brand embedding extractor",                     "roas",        "p0", "claude", "mini-4", "L", "—",               "Planned"),
    ("M12.3", "Half-life 14d learnings decay",                       "roas",        "p1", "codex",  "mini-2", "S", "M12.1",           "Planned"),
    ("M12.4", "IDS score computation service",                       "convergence", "p0", "claude", "mini-5", "L", "—",               "Planned"),
    ("M12.5", "Convergence dashboard (indistinguishability curves)", "convergence", "p1", "codex",  "mini-3", "M", "M12.4",           "Planned"),
    ("M12.6", "L2/L3 category promotion logic",                      "roas",        "p1", "claude", "mini-4", "M", "M12.1",           "Planned"),
    ("M12.7", "Brand-specific bandit priors from embeddings",        "roas",        "p1", "claude", "mini-5", "L", "M12.2",           "Planned"),

    # M13 — Production Ops + Observability (6)
    ("M13.1", "18 SLOs published to Grafana",                        "obs", "p0", "codex", "mini-1", "M", "—",                 "Planned"),
    ("M13.2", "3-tier kill-switch implementation",                   "obs", "p0", "codex", "mini-2", "M", "M11.7",             "Planned"),
    ("M13.3", "32-failure circuit breakers",                         "obs", "p0", "codex", "mini-3", "L", "M13.2",             "Planned"),
    ("M13.4", "Pact tests for cross-system contracts",               "obs", "p1", "codex", "mini-4", "M", "M11.11",            "Planned"),
    ("M13.5", "Lineage audit weekly cron",                           "obs", "p1", "codex", "mini-5", "S", "—",                 "Planned"),
    ("M13.6", "Cost dashboards (unit economics per lever)",          "obs", "p2", "codex", "mini-1", "M", "—",                 "Planned"),
]

# Milestone metadata
MILESTONES = [
    ("VIZ", "Modularization Sprint", "Break monolith into composable modules — runs in parallel to DNA kickoff.", "viz"),
    ("M10", "SOTA Training Pipeline", "Kalodata → Cloudinary → features → judges. Real dataset + ground-truth scorers.", "m10"),
    ("M11", "Autonomous A/B + OPE",   "LinTS bandit + DR-IPS off-policy eval + canary controller + guard sweeps.",      "m11"),
    ("M12", "Multi-Level ROAS + Convergence", "Hierarchical brand×L1×L2×L3 arms, half-life decay, IDS convergence score.", "m12"),
    ("M13", "Production Ops",         "18 SLOs, 3-tier kill switches, 32-failure circuit breakers, lineage audit.",      "m13"),
]

# Production readiness gates (10)
GATES = [
    ("Gate 1", "ADDITIVE-ONLY invariant verified",    "Every table & endpoint uses dna_ prefix. No existing config touched.", "critical"),
    ("Gate 2", "Schema migrations idempotent",        "All Neon migrations rollback-safe, zero-downtime, with down-scripts.", "critical"),
    ("Gate 3", "Judge ensemble ≥ 0.85 agreement",    "5 judges agree on ≥85% of held-out samples. Disagreement surfaced in ledger.", "high"),
    ("Gate 4", "OPE bounds tight enough to gate",     "DR-IPS 95% CI half-width < 0.02 before any canary promotion.",        "critical"),
    ("Gate 5", "Canary auto-revert rehearsed",        "Force-fail injected; controller reverts within 1 cycle. Test cron green.", "critical"),
    ("Gate 6", "18 SLOs live in Grafana",             "All ingestion, judge, bandit, rollout, and cost SLOs publishing + alerting.", "high"),
    ("Gate 7", "3-tier kill switches tested",         "Arm-level / category-level / global kill all fire on guard-sweep trigger.", "high"),
    ("Gate 8", "32-failure circuit breakers tested",  "Chaos run triggers each failure mode; breakers open + recover cleanly.", "medium"),
    ("Gate 9", "Lineage audit completes weekly",      "Every promoted config traceable to dataset + judge versions + OPE bounds.", "high"),
    ("Gate 10","Weekly cost < budget with buffer",    "Unit economics dashboards stable; weekly spend < target − 15%.",       "medium"),
]

# Fleet allocation — which Mini owns which focus after VIZ completes
FLEET_MAP = [
    ("mini-1", "codex",  "Infra + schema migrations",        "M10.1 · M10.8 · M11.1 · M11.6 · M11.10 · M12.1 · M13.1 · M13.6"),
    ("mini-2", "codex",  "Ingestion + rollout + breakers",   "M10.2 · M11.5 · M11.7 · M11.11 · M12.3 · M13.2"),
    ("mini-3", "codex",  "Distill + convergence UI",         "M10.3 · M11.4 · M11.8 · M11.12 · M12.5 · M13.3"),
    ("mini-4", "mixed",  "Ingest + OPE + features",          "M10.4 · M10.7 · M11.3 · M11.9 · M12.2 · M12.6 · M13.4"),
    ("mini-5", "claude", "Judges + bandit + convergence",    "M10.5 · M10.6 · M11.2 · M12.4 · M12.7 · M13.5"),
]

# Week-by-week execution timeline
TIMELINE = [
    ("Week 1", "VIZ modularization + M10 infra + ingestion", [
        "VIZ.1–VIZ.5 ship (parallel, 5 Minis)",
        "M10.1 schema migration (mini-1)",
        "M10.2 harvester + M10.3 uploader begin",
    ]),
    ("Week 2", "M10 finalize + M11 launch", [
        "M10.4 ingest handler lands",
        "M10.5 + M10.6 judges enter review",
        "M11.1 arms schema migrates",
        "M11.2 LinTS router scaffolded",
    ]),
    ("Week 3", "M11 full swing + OPE gates", [
        "M11.3 OPE estimator wired to judges",
        "M11.5 rollout controller + M11.7 guard sweep",
        "First 1% canary rehearsal (auto-revert drill)",
    ]),
    ("Week 4", "M12 convergence + M11 wrap", [
        "M11.4 LoRA distill loop live",
        "M12.1 hierarchical arms + M12.4 IDS",
        "M11.12 canary dashboard UI",
    ]),
    ("Week 5", "M13 ops + production gates", [
        "M13.1 18 SLOs live",
        "M13.2 + M13.3 kill switches + breakers",
        "M13.4 Pact tests + M13.5 lineage audit",
        "All 10 production gates verified green",
    ]),
]

# ------------------------------------------------------------------
# Build HTML fragment
# ------------------------------------------------------------------
def chip(label: str, kind: str) -> str:
    return f'<span class="gp-chip gp-chip-{kind}">{label}</span>'

def render_tasks_for_milestone(milestone_id: str) -> str:
    rows = []
    for tid, title, lbl, prio, lane, mini, effort, deps, status in TASKS:
        if not tid.startswith(milestone_id):
            continue
        status_kind = {"Planned": "planned", "Fleet-ready": "ready", "Dispatched": "dispatched",
                       "In-progress": "progress", "Completed": "done", "Blocked": "blocked"}.get(status, "planned")
        rows.append(f"""
            <tr data-status="{status_kind}" data-lane="{lane}" data-priority="{prio}">
              <td class="gp-id"><code>{tid}</code></td>
              <td class="gp-title">{title}</td>
              <td>{chip(prio.upper(), f"prio-{prio}")}</td>
              <td>{chip(lane, f"lane-{lane}")}</td>
              <td class="gp-mini"><code>{mini}</code></td>
              <td class="gp-effort">{effort}</td>
              <td class="gp-deps">{deps}</td>
              <td>{chip(status, f"status-{status_kind}")}</td>
            </tr>""")
    return "\n".join(rows)

milestone_blocks = []
for mid, name, tagline, slug in MILESTONES:
    task_rows = render_tasks_for_milestone(mid)
    count = sum(1 for t in TASKS if t[0].startswith(mid))
    milestone_blocks.append(f"""
        <section class="gp-milestone gp-ms-{slug}" id="gp-{slug}">
          <header class="gp-ms-head">
            <div class="gp-ms-id">{mid}</div>
            <div class="gp-ms-body">
              <h3>{name} <span class="gp-ms-count">{count} tasks</span></h3>
              <p>{tagline}</p>
            </div>
          </header>
          <div class="gp-table-wrap">
            <table class="gp-table">
              <thead>
                <tr>
                  <th>ID</th><th>Task</th><th>Priority</th><th>Lane</th>
                  <th>Mini</th><th>Effort</th><th>Depends</th><th>Status</th>
                </tr>
              </thead>
              <tbody>{task_rows}
              </tbody>
            </table>
          </div>
        </section>""")

gate_rows = "\n".join(
    f"""            <li class="gp-gate gp-gate-{sev}">
              <span class="gp-gate-num">{num}</span>
              <div class="gp-gate-body">
                <strong>{name}</strong>
                <p>{desc}</p>
              </div>
              <span class="gp-gate-sev">{sev.upper()}</span>
            </li>"""
    for num, name, desc, sev in GATES
)

fleet_rows = "\n".join(
    f"""            <div class="gp-fleet-card" data-lane="{lane}">
              <header>
                <code class="gp-fleet-mini">{mini}</code>
                <span class="gp-chip gp-chip-lane-{lane}">{lane}</span>
              </header>
              <h4>{focus}</h4>
              <p class="gp-fleet-owns">{owns}</p>
            </div>"""
    for mini, lane, focus, owns in FLEET_MAP
)

timeline_rows = "\n".join(
    f"""            <article class="gp-week">
              <header>
                <span class="gp-week-num">{week}</span>
                <h4>{title}</h4>
              </header>
              <ul>
                {''.join(f'<li>{item}</li>' for item in items)}
              </ul>
            </article>"""
    for week, title, items in TIMELINE
)

# Aggregate summary
total = len(TASKS)
planned = sum(1 for t in TASKS if t[-1] == "Planned")
ready   = sum(1 for t in TASKS if t[-1] == "Fleet-ready")
codex_n = sum(1 for t in TASKS if t[4] == "codex")
claude_n= sum(1 for t in TASKS if t[4] == "claude")
p0_n    = sum(1 for t in TASKS if t[3] == "p0")

GAMEPLAN_HTML = f"""
      <!-- ============================================================
           GAMEPLAN — Full E2E production gameplan
           ============================================================ -->
      <section id="gameplan" class="section section-gameplan">
        <div class="container">
          <header class="section-head">
            <div class="section-eyebrow">Full gameplan · Fleet-ready · Production checklist</div>
            <h2>Gameplan &amp; production readiness</h2>
            <p class="section-sub">
              Every task that must ship to take the DNA pipeline from zero to
              autonomous production. {total} tasks across 5 milestones — {ready} fleet-ready,
              {planned} planned — routed to 5 Minis across the Codex + Claude lanes.
              This page is the live single source of truth while the fleet builds.
            </p>
          </header>

          <div class="gp-summary">
            <div class="gp-summary-card">
              <span class="gp-summary-label">Total tasks</span>
              <span class="gp-summary-value">{total}</span>
              <span class="gp-summary-meta">{p0_n} P0 · {codex_n} codex · {claude_n} claude</span>
            </div>
            <div class="gp-summary-card">
              <span class="gp-summary-label">Fleet-ready now</span>
              <span class="gp-summary-value">{ready}</span>
              <span class="gp-summary-meta">VIZ modularization · parallel on 5 Minis</span>
            </div>
            <div class="gp-summary-card">
              <span class="gp-summary-label">Planned DNA</span>
              <span class="gp-summary-value">{planned}</span>
              <span class="gp-summary-meta">Seeding as GitHub issues → CC queue</span>
            </div>
            <div class="gp-summary-card">
              <span class="gp-summary-label">Production gates</span>
              <span class="gp-summary-value">{len(GATES)}</span>
              <span class="gp-summary-meta">All must be green before full rollout</span>
            </div>
            <div class="gp-summary-card">
              <span class="gp-summary-label">Fleet load</span>
              <span class="gp-summary-value">~14%</span>
              <span class="gp-summary-meta">of 36-slot capacity at peak</span>
            </div>
            <div class="gp-summary-card">
              <span class="gp-summary-label">Target wall-clock</span>
              <span class="gp-summary-value">5 wks</span>
              <span class="gp-summary-meta">Critical path ≈ 19 sequential hrs</span>
            </div>
          </div>

          <h3 class="sub-h">Task board — all milestones</h3>
          {"".join(milestone_blocks)}

          <h3 class="sub-h">Fleet allocation</h3>
          <div class="gp-fleet-grid">
{fleet_rows}
          </div>

          <h3 class="sub-h">5-week execution timeline</h3>
          <div class="gp-timeline">
{timeline_rows}
          </div>

          <h3 class="sub-h">Production readiness checklist</h3>
          <ul class="gp-gates">
{gate_rows}
          </ul>

          <div class="gp-callout">
            <strong>This page updates as the fleet works.</strong>
            Task statuses, PR links, and gate progress roll forward automatically —
            every commit to <code>bemomentiq/momentiq-dna</code> that closes an issue
            flips the corresponding row from Planned → In-progress → Completed.
          </div>
        </div>
      </section>
"""

# ------------------------------------------------------------------
# Insert HTML — replace any existing #gameplan section, otherwise append
# before </main>
# ------------------------------------------------------------------
html = HTML.read_text()

# Remove existing gameplan
html = re.sub(
    r'\s*<!-- =+\s*\n\s*GAMEPLAN[\s\S]*?</section>\s*\n',
    "\n",
    html,
    flags=re.MULTILINE,
)
# Also clean bare re-inserts
html = re.sub(
    r'\s*<section id="gameplan"[\s\S]*?</section>\s*',
    "\n",
    html,
    flags=re.MULTILINE,
)

# Nav link: insert after Build plan
if '<a href="#gameplan">Gameplan</a>' not in html:
    html = html.replace(
        '<a href="#buildplan">Build plan</a>',
        '<a href="#buildplan">Build plan</a>\n          <a href="#gameplan">Gameplan</a>',
        1,
    )

# Append before </main>
html = html.replace("</main>", GAMEPLAN_HTML + "\n</main>", 1)

HTML.write_text(html)
print(f"HTML: inserted #gameplan ({total} tasks, {len(GATES)} gates, {len(FLEET_MAP)} Minis, {len(TIMELINE)} weeks)")

# ------------------------------------------------------------------
# Append CSS
# ------------------------------------------------------------------
GP_CSS = """

/* ============================================================
   GAMEPLAN — #gameplan section (Round 4)
   ============================================================ */
.section-gameplan {
  background: linear-gradient(180deg, #fafbfd 0%, #f4f6fa 100%);
  padding-top: 64px;
  padding-bottom: 88px;
}
.section-gameplan .sub-h {
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.015em;
  color: #0b0d11;
  margin: 40px 0 16px;
  padding-bottom: 10px;
  border-bottom: 2px solid #d7dbe0;
}

/* summary cards */
.gp-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px;
  margin: 24px 0 36px;
}
.gp-summary-card {
  background: #fff;
  border: 1px solid #d7dbe0;
  border-radius: 12px;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  box-shadow: 0 1px 2px rgba(15,17,21,0.04);
}
.gp-summary-label {
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-primary);
}
.gp-summary-value {
  font-size: 2.4rem;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.03em;
  color: #0b0d11;
  font-variant-numeric: tabular-nums lining-nums;
  margin-top: 4px;
}
.gp-summary-meta {
  font-size: 0.82rem;
  color: #3d4552;
  margin-top: 2px;
  line-height: 1.45;
}

/* milestone blocks */
.gp-milestone {
  background: #fff;
  border: 1px solid #d7dbe0;
  border-radius: 14px;
  padding: 22px 24px;
  margin-bottom: 20px;
  box-shadow: 0 1px 2px rgba(15,17,21,0.04);
}
.gp-ms-head {
  display: flex;
  gap: 18px;
  align-items: flex-start;
  margin-bottom: 18px;
  padding-bottom: 14px;
  border-bottom: 1px solid #e0e4e9;
}
.gp-ms-id {
  flex: 0 0 auto;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  font-weight: 800;
  font-size: 0.95rem;
  letter-spacing: 0.02em;
  color: #fff;
  background: #6b737f;
}
.gp-ms-viz  .gp-ms-id { background: linear-gradient(135deg, #3e4452, #0b0d11); }
.gp-ms-m10 .gp-ms-id { background: linear-gradient(135deg, var(--c-source, #d19900), #a87200); }
.gp-ms-m11 .gp-ms-id { background: linear-gradient(135deg, var(--c-gate, #a12c7b), #6a1f52); }
.gp-ms-m12 .gp-ms-id { background: linear-gradient(135deg, var(--c-dist, #437a22), #2d5418); }
.gp-ms-m13 .gp-ms-id { background: linear-gradient(135deg, var(--c-gen, #7a39bb), #4d2375); }
.gp-ms-body h3 {
  margin: 0 0 4px;
  font-size: 1.2rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: #0b0d11;
}
.gp-ms-count {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--color-primary);
  background: #e1eeef;
  padding: 2px 10px;
  border-radius: 999px;
  margin-left: 8px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.gp-ms-body p {
  margin: 0;
  font-size: 0.95rem;
  color: #2c333f;
  line-height: 1.55;
}

/* task tables */
.gp-table-wrap { overflow-x: auto; }
.gp-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
  font-variant-numeric: tabular-nums lining-nums;
}
.gp-table th {
  text-align: left;
  padding: 10px 10px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #3d4552;
  background: #f4f6f9;
  border-bottom: 2px solid #d7dbe0;
  white-space: nowrap;
}
.gp-table td {
  padding: 11px 10px;
  border-bottom: 1px solid #e8ebf0;
  color: #1a1d23;
  vertical-align: middle;
}
.gp-table tbody tr:hover { background: #fafbfd; }
.gp-id code,
.gp-mini code {
  font-family: var(--font-mono);
  font-size: 0.82rem;
  background: #f1f4f8;
  padding: 2px 7px;
  border-radius: 4px;
  color: #1b4775;
  font-weight: 600;
}
.gp-title { font-weight: 500; min-width: 260px; line-height: 1.4; }
.gp-effort { font-weight: 700; color: #0b0d11; }
.gp-deps { font-family: var(--font-mono); font-size: 0.78rem; color: #3d4552; }

/* chips */
.gp-chip {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 999px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  white-space: nowrap;
  line-height: 1.4;
}
.gp-chip-prio-p0 { background: #fde4e4; color: #8a1a1a; }
.gp-chip-prio-p1 { background: #fef0d8; color: #8a5a00; }
.gp-chip-prio-p2 { background: #dde9f5; color: #1b4775; }
.gp-chip-lane-codex  { background: #dde9f5; color: #1b4775; }
.gp-chip-lane-claude { background: #e6ddfc; color: #4a2a9c; }
.gp-chip-lane-mixed  { background: #eaeaf0; color: #3d4552; }
.gp-chip-status-planned    { background: #eaeaf0; color: #3d4552; }
.gp-chip-status-ready      { background: #d5eef0; color: #0c4e54; }
.gp-chip-status-dispatched { background: #fef0d8; color: #8a5a00; }
.gp-chip-status-progress   { background: #fef0d8; color: #8a5a00; animation: gp-pulse 1.8s ease-in-out infinite; }
.gp-chip-status-done       { background: #d5ead4; color: #1f5c28; }
.gp-chip-status-blocked    { background: #fde4e4; color: #8a1a1a; }
@keyframes gp-pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }

/* fleet grid */
.gp-fleet-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 14px;
  margin: 20px 0 12px;
}
.gp-fleet-card {
  background: #fff;
  border: 1px solid #d7dbe0;
  border-left: 4px solid var(--color-primary);
  border-radius: 10px;
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  box-shadow: 0 1px 2px rgba(15,17,21,0.04);
}
.gp-fleet-card[data-lane="codex"]  { border-left-color: #1b4775; }
.gp-fleet-card[data-lane="claude"] { border-left-color: #4a2a9c; }
.gp-fleet-card[data-lane="mixed"]  { border-left-color: #3d4552; }
.gp-fleet-card header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}
.gp-fleet-mini {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 700;
  background: #f1f4f8;
  padding: 2px 8px;
  border-radius: 5px;
  color: #0b0d11;
}
.gp-fleet-card h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: #0b0d11;
  letter-spacing: -0.005em;
  line-height: 1.3;
}
.gp-fleet-owns {
  margin: 0;
  font-family: var(--font-mono);
  font-size: 0.76rem;
  color: #3d4552;
  line-height: 1.55;
  word-break: break-word;
}

/* timeline */
.gp-timeline {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 14px;
  margin: 20px 0 12px;
}
.gp-week {
  background: #fff;
  border: 1px solid #d7dbe0;
  border-radius: 12px;
  padding: 18px 20px;
  box-shadow: 0 1px 2px rgba(15,17,21,0.04);
}
.gp-week header {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e8ebf0;
}
.gp-week-num {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-primary);
  background: #e1eeef;
  padding: 3px 9px;
  border-radius: 999px;
}
.gp-week h4 {
  margin: 0;
  font-size: 0.98rem;
  font-weight: 700;
  color: #0b0d11;
  letter-spacing: -0.005em;
  line-height: 1.3;
}
.gp-week ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.gp-week li {
  font-size: 0.88rem;
  line-height: 1.5;
  color: #1a1d23;
  padding: 5px 0 5px 14px;
  position: relative;
}
.gp-week li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 11px;
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--color-primary);
}

/* production readiness gates */
.gp-gates {
  list-style: none;
  margin: 20px 0 12px;
  padding: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
@media (max-width: 720px) { .gp-gates { grid-template-columns: 1fr; } }
.gp-gate {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 14px;
  align-items: center;
  background: #fff;
  border: 1px solid #d7dbe0;
  border-left: 4px solid #6b737f;
  border-radius: 10px;
  padding: 14px 16px;
  box-shadow: 0 1px 2px rgba(15,17,21,0.04);
}
.gp-gate-critical { border-left-color: #a12c1e; }
.gp-gate-high     { border-left-color: #a87200; }
.gp-gate-medium   { border-left-color: #1b4775; }
.gp-gate-num {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  background: #f1f4f8;
  padding: 4px 8px;
  border-radius: 5px;
  color: #0b0d11;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.gp-gate-body strong {
  display: block;
  font-size: 0.98rem;
  font-weight: 700;
  color: #0b0d11;
  letter-spacing: -0.005em;
  margin-bottom: 2px;
}
.gp-gate-body p {
  margin: 0;
  font-size: 0.85rem;
  color: #2c333f;
  line-height: 1.5;
}
.gp-gate-sev {
  font-size: 0.66rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  padding: 3px 8px;
  border-radius: 999px;
  background: #eaeaf0;
  color: #3d4552;
}
.gp-gate-critical .gp-gate-sev { background: #fde4e4; color: #8a1a1a; }
.gp-gate-high .gp-gate-sev     { background: #fef0d8; color: #8a5a00; }
.gp-gate-medium .gp-gate-sev   { background: #dde9f5; color: #1b4775; }

/* callout */
.gp-callout {
  margin-top: 32px;
  padding: 20px 24px;
  background: linear-gradient(180deg, #fff, #f7f9fc);
  border: 1px solid #d7dbe0;
  border-left: 4px solid var(--color-primary);
  border-radius: 12px;
  font-size: 0.95rem;
  color: #1a1d23;
  line-height: 1.6;
}
.gp-callout strong { color: #0b0d11; }
.gp-callout code {
  font-family: var(--font-mono);
  background: #f1f4f8;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.85rem;
  color: #1b4775;
}

/* mobile */
@media (max-width: 720px) {
  .gp-ms-head { flex-direction: column; gap: 12px; }
  .gp-ms-id { width: 48px; height: 48px; font-size: 0.85rem; }
  .gp-table { font-size: 0.82rem; }
  .gp-table th, .gp-table td { padding: 8px 6px; }
  .gp-title { min-width: 180px; }
}
"""

# Remove any existing GAMEPLAN css block
css = CSS.read_text()
css = re.sub(
    r'\n\n/\* =+\s*\n\s*GAMEPLAN[\s\S]*?(?=\n\n/\* =+|\Z)',
    "",
    css,
    flags=re.MULTILINE,
)
css = css.rstrip() + "\n" + GP_CSS
CSS.write_text(css)
print(f"CSS: appended gameplan styles ({len(GP_CSS)} chars)")
