#!/usr/bin/env python3
"""Static-site generator for the DNA Pipeline Site.

No build step. Reads:
  - data/ia.json     — layer/section metadata
  - data/roadmap.json — current roadmap snapshot
  - content/<layer>/<slug>.html — per-section content fragments (body only)
  - content/<layer>/index.html  — optional layer-index intro fragment
Writes:
  - index.html
  - <layer>/index.html
  - <layer>/<slug>/index.html

Run:
  python3 scripts/build.py

All asset paths use a per-page `BASE` prefix so the same HTML works at any
deploy depth (e.g. /, /sites/<id>/, etc).
"""
import json, os, html, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CONTENT = ROOT / "content"

ia = json.loads((DATA / "ia.json").read_text())
roadmap = json.loads((DATA / "roadmap.json").read_text())

def base_for(depth: int) -> str:
    """`depth` = how many directories deep this page sits relative to site root.
    Returns the relative prefix for asset/link refs (e.g. "" for root, "../" for layer index, "../../" for drilldown)."""
    return "../" * depth

def nav_html(base: str, current_layer: str | None) -> str:
    items = [("", "Home", None)] + [(f"{l['slug']}/", l['title'], l['slug']) for l in ia['layers']]
    parts = []
    for href, label, slug in items:
        cls = ' class="active"' if slug == current_layer else ''
        # Use base + href so all nav links work from any depth
        parts.append(f'<a href="{base}{href}"{cls}>{html.escape(label)}</a>')
    return "\n          ".join(parts)

def page(*, depth: int, current_layer: str | None, title: str, body: str) -> str:
    base = base_for(depth)
    nav = nav_html(base, current_layer)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · DNA Pipeline · MomentIQ</title>
<meta name="description" content="MomentIQ DNA Pipeline — Kalodata → AI Content Platform training pipeline.">
<link rel="stylesheet" href="{base}assets/style.css">
</head>
<body>
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="{base}" aria-label="Home">
      <span class="brand-mark" aria-hidden>◆</span>
      <span>DNA Pipeline</span>
      <span class="brand-org">MomentIQ</span>
    </a>
    <nav class="primary-nav">
          {nav}
    </nav>
  </div>
</header>
<main class="page">
{body}
</main>
<footer class="site-footer">
  <div class="site-footer-inner">
    <span>MomentIQ · DNA Pipeline</span>
    <span>Source · <a href="https://github.com/bemomentiq/dna-pipeline-viz" target="_blank" rel="noreferrer">bemomentiq/dna-pipeline-viz</a></span>
  </div>
</footer>
</body>
</html>
"""

def render_roadmap_dashboard() -> str:
    t = roadmap["totals"]
    total = t.get("total") or (t.get("shipped",0)+t.get("wiring",0)+t.get("notstarted",0)) or 1
    pct = lambda n: round((n/total)*1000)/10
    src = roadmap.get("source", {})
    src_bits = " · ".join(filter(None, [src.get("repo"), src.get("pr"), src.get("commit")]))

    phases = ""
    for p in roadmap.get("phases", []):
        items = "".join(f"<li>{html.escape(i)}</li>" for i in p.get("items", []))
        meta = f'<span class="phase-meta">{html.escape(p.get("meta",""))}</span>' if p.get("meta") else ""
        status = p.get("status", "wiring")
        label = {"shipped":"Shipped","wiring":"Wiring","notstarted":"Not started","inprog":"In progress"}.get(status, status)
        phases += f"""
        <article class="phase">
          <div class="phase-head">
            <span class="phase-title">{html.escape(p['title'])}</span>
            <span class="badge {status}">{label}</span>
            {meta}
          </div>
          <ul>{items}</ul>
        </article>"""

    gaps = ""
    for g in roadmap.get("topGaps", []):
        gaps += f'<li><b>{html.escape(g["title"])}</b>{html.escape(g["detail"])}</li>'

    doc = src.get("doc")
    doc_bit = f'See <code>{html.escape(doc)}</code>.' if doc else ""

    return f"""
<section aria-labelledby="roadmap-heading">
  <span class="kicker">Roadmap snapshot</span>
  <h1 id="roadmap-heading">DNA Pipeline — Status</h1>
  <p>Audit refresh {html.escape(roadmap.get("capturedAt","—"))}. Source: {html.escape(src_bits)}. {doc_bit}</p>

  <div class="snapshot-stats">
    <div class="stat shipped"><div class="num">{pct(t.get('shipped',0))}%</div><div class="label">Shipped ({t.get('shipped',0)})</div></div>
    <div class="stat wiring"><div class="num">{pct(t.get('wiring',0))}%</div><div class="label">Wiring incomplete ({t.get('wiring',0)})</div></div>
    <div class="stat notstarted"><div class="num">{pct(t.get('notstarted',0))}%</div><div class="label">Not started ({t.get('notstarted',0)})</div></div>
    <div class="stat total"><div class="num">{total}</div><div class="label">Total claims</div></div>
  </div>

  <div class="legend">
    <span class="l-shipped">Shipped</span>
    <span class="l-wiring">Wiring incomplete</span>
    <span class="l-notstarted">Not started</span>
  </div>
  <div class="bar" aria-hidden>
    <span class="b-shipped" style="width:{pct(t.get('shipped',0))}%"></span>
    <span class="b-wiring" style="width:{pct(t.get('wiring',0))}%"></span>
    <span class="b-notstarted" style="width:{pct(t.get('notstarted',0))}%"></span>
  </div>

  <h2>Phases</h2>
  <div class="phase-list">{phases}
  </div>

  <h2>Top remaining wiring gaps</h2>
  <div class="gap-list card"><ol>{gaps}</ol></div>
</section>
"""

def render_layer_grid(base: str, layers) -> str:
    cards = ""
    for l in layers:
        cards += f"""
        <a class="section-card" href="{base}{l['slug']}/">
          <h3>{html.escape(l['title'])}</h3>
          <p>{html.escape(l['blurb'])}</p>
        </a>"""
    return f"""
<h2 style="margin-top:48px">Explore the engine</h2>
<p>Seven layers, drill all the way down. Pulled from the original 33-section walkthrough.</p>
<div class="section-grid">{cards}
</div>
"""

def render_section_grid(layer_slug: str, sections) -> str:
    cards = ""
    for s in sections:
        cards += f"""
        <a class="section-card" href="{s['slug']}/">
          <h3>{html.escape(s['title'])}</h3>
          <p>{html.escape(s['blurb'])}</p>
        </a>"""
    return f'<div class="section-grid">{cards}\n</div>\n'

def read_content(rel: pathlib.Path) -> str | None:
    p = CONTENT / rel
    if p.exists() and p.is_file():
        return p.read_text()
    return None

def write(out_path: pathlib.Path, content: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content)
    print("  wrote", out_path.relative_to(ROOT))

def build_home():
    body = render_roadmap_dashboard() + render_layer_grid("", ia["layers"])
    write(ROOT / "index.html", page(depth=0, current_layer=None, title="Home", body=body))

def build_layer(layer):
    intro = read_content(pathlib.Path(layer["slug"]) / "index.html")
    intro_html = intro if intro else f'<p>{html.escape(layer["blurb"])}</p>'
    body = f"""
<span class="kicker">Layer</span>
<h1>{html.escape(layer["title"])}</h1>
{intro_html}
{render_section_grid(layer["slug"], layer["sections"])}
"""
    write(ROOT / layer["slug"] / "index.html",
          page(depth=1, current_layer=layer["slug"], title=layer["title"], body=body))

def build_section(layer, section):
    body_frag = read_content(pathlib.Path(layer["slug"]) / f'{section["slug"]}.html')
    if body_frag is None:
        body_frag = f'<div class="empty">Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.</div>'
    body = f"""
<div class="subnav">
  <a href="../">← {html.escape(layer["title"])}</a>
</div>
<span class="kicker">{html.escape(layer["title"])}</span>
<h1>{html.escape(section["title"])}</h1>
<p>{html.escape(section["blurb"])}</p>
{body_frag}
"""
    write(ROOT / layer["slug"] / section["slug"] / "index.html",
          page(depth=2, current_layer=layer["slug"], title=section["title"], body=body))

def main():
    print(f"Building site at {ROOT}")
    build_home()
    for layer in ia["layers"]:
        build_layer(layer)
        for section in layer["sections"]:
            build_section(layer, section)
    print("Done.")

if __name__ == "__main__":
    main()
