#!/usr/bin/env python3
"""
DNA Pipeline Viz — build script.

Concatenates `partials/*.html` (sorted by filename) into `index.html`.
Partials are expected to be:
  00-head.html          — everything from <!doctype html> through <main id="top">
  10-hub.html           — first section
  20-overview.html
  ...
  900-gameplan.html     — last section
  999-foot.html         — </main>, <script>, </body></html>

Run: python3 build.py
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTIALS = ROOT / "partials"
OUT = ROOT / "index.html"


def main() -> int:
    if not PARTIALS.is_dir():
        print(f"ERROR: partials/ directory missing at {PARTIALS}", file=sys.stderr)
        return 1

    files = sorted(PARTIALS.glob("*.html"))
    if not files:
        print("ERROR: no partials to build", file=sys.stderr)
        return 1

    chunks: list[str] = []
    for p in files:
        marker = f"<!-- ========== partial: {p.name} ========== -->"
        chunks.append(marker)
        chunks.append(p.read_text(encoding="utf-8").rstrip() + "\n")

    OUT.write_text("\n".join(chunks) + "\n", encoding="utf-8")
    print(f"✓ built {OUT.name} from {len(files)} partials ({sum(p.stat().st_size for p in files):,} bytes source)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
