# DNA Pipeline Viz — Partials

Each `NNN-name.html` file is one section of the roadmap page. Numeric prefix
controls ordering. The final `index.html` is built by running:

```
python3 build.py
```

from the project root. That script concatenates every `*.html` partial in this
directory (sorted lexicographically) into `../index.html`, adding an HTML
comment marker before each partial for traceability.

## Structure

- `000-head.html` — `<!doctype>`, `<head>`, header/nav, `<main id="top">` open
- `010-hero.html` … `320-gameplan.html` — one file per `<section>`
- `999-foot.html` — `</main>`, `<script src="script.js">`, close tags

## Editing workflow

1. Edit a partial (e.g. `100-roadmap.html`).
2. Run `python3 build.py`.
3. Local server automatically picks up the new `index.html`.
4. Deploy via the platform's `deploy_website` with entry_point=`index.html`.

## Notes

- The NBSP (`\u00a0`) character inside `schema\u00a0ready` must be preserved.
- `build.py` is intentionally dumb — no templating, no variables; order comes
  from filenames only.
- `split.py` was a one-time tool used to bootstrap these partials from the
  monolithic `index.html`. It is retained for reference but should not be run
  again.
