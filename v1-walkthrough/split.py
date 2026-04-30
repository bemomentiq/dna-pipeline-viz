#!/usr/bin/env python3
"""
One-time splitter: reads index.html and writes partials/*.html
based on section boundaries.
"""
from __future__ import annotations
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "index.html"
OUT = ROOT / "partials"
OUT.mkdir(exist_ok=True)

src = SRC.read_text(encoding="utf-8")

# Locate the <main id="top"> open and </main> close
main_open_match = re.search(r'(    <main id="top">\n)', src)
main_close_match = re.search(r'(\n</main>\n)', src)
if not main_open_match or not main_close_match:
    raise SystemExit("Could not find <main> boundaries")

head = src[: main_open_match.end()]
body = src[main_open_match.end(): main_close_match.start()]
foot = src[main_close_match.start():]

# Split body by top-level <section ...> ... </section> at indent 6 spaces.
# Sections are always indented with exactly 6 spaces at the top level.
# We'll find all positions of '      <section ' and use them as starts.
section_pattern = re.compile(r'^      <section[^\n]*\n', re.MULTILINE)
starts = [m.start() for m in section_pattern.finditer(body)]
starts.append(len(body))

# Map section id (or class-derived id) -> filename prefix
# Order is implicit (ordered list); prepend 3-digit indices 010,020,... for stable sort
section_meta: list[tuple[int, str, str]] = []  # (start, end, idx_prefix_name)

# We'll name files by extracting the id (or a label).
id_pattern = re.compile(r'<section[^>]*id="([^"]+)"')
hero_detected = False

for i in range(len(starts) - 1):
    start = starts[i]
    end = starts[i + 1]
    chunk = body[start:end]
    # strip trailing whitespace from chunk
    m = id_pattern.search(chunk)
    if m:
        name = m.group(1)
    else:
        # First unnamed <section class="hero">
        if 'class="hero"' in chunk and not hero_detected:
            name = "hero"
            hero_detected = True
        else:
            name = f"sec-{i}"
    section_meta.append((start, end, name))

# Sort is natural order; assign 010,020,...
# Write head as 000-head.html (include the inter-section comment if any)
head_text = head
# Trim any trailing blank from head
(OUT / "000-head.html").write_text(head_text, encoding="utf-8")

# The hero section is first but the `<section id="hub">` is the first with id.
# Some comments like <!-- HERO --> and <!-- OVERVIEW --> are between the main open and first section.
# Capture pre-first-section content as part of head or as 005-prelude.
first_start = section_meta[0][0]
prelude = body[:first_start]
if prelude.strip():
    # Append prelude to 000-head.html so head+prelude remain contiguous
    with (OUT / "000-head.html").open("a", encoding="utf-8") as f:
        f.write(prelude)

# Only gameplan contains nested <section class="gp-milestone">.
# We treat the top-level #gameplan section as ONE partial (keeps its inner structure intact).
# But our regex matched 6-space indentation only, and inner gp-milestones are at 8 spaces → safe.

for idx, (s, e, name) in enumerate(section_meta, start=1):
    # Pad index to 3 digits for sort, e.g. 010, 020 ...
    prefix = f"{idx*10:03d}"
    filename = f"{prefix}-{name}.html"
    (OUT / filename).write_text(body[s:e], encoding="utf-8")

# Foot
(OUT / "999-foot.html").write_text(foot, encoding="utf-8")

print(f"✓ wrote {len(section_meta)} section partials + head + foot to partials/")
for p in sorted(OUT.glob("*.html")):
    print(f"  {p.name:30s} {p.stat().st_size:>7} bytes")
