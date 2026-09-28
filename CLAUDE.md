# rodrigoroque.dev

Personal portfolio and résumé, published on GitHub Pages. A static single page
(`site/`) plus two résumé PDFs compiled from LaTeX (`cv/`). No framework, no
bundler, no package manager: plain HTML/CSS/JS, a `Makefile`, and a stdlib-only
Python script. See `README.md` for the build commands.

## Gotchas

- **Content is duplicated by hand.** The résumé facts live in `cv/cv-pt.tex`,
  `cv/cv-en.tex` *and* the copy in `site/index.html` (hero metrics, about,
  experience). Nothing syncs them — a change to one usually needs the others.
- **Build needs Tectonic**, not a full TeX install (`make` runs
  `tectonic -X compile`). `make site` assembles `_site/` (gitignored); the PDFs
  are published as `rodrigo-roque-cv-{pt,en}.pdf`, and the page links those
  names, so don't rename one side only.
- **Cache busting happens in the Makefile, not the source.** `make site` rewrites
  the `styles.css` / `app.js` references in the copied `index.html` with a
  `?v=<sha256 prefix>`. It matches the exact strings `href="styles.css"` and
  `src="app.js"` — keep them literal in `site/index.html` or the rewrite silently
  stops applying.
- **The Open Source cards are generated.** Everything between
  `<!-- projects:start -->` and `<!-- projects:end -->` in `site/index.html` is
  overwritten by `make projects` (`python3 -m scripts.project_stats`) from
  `data/projects.json`. Edit the JSON (or the renderer in
  `scripts/project_stats/rendering.py`), never the cards in the HTML. The script
  also re-sorts the cards by stars, then downloads, and writes the fetched counts
  back into the JSON. A source that fails keeps its previous value (warning only);
  the run fails only when every project failed.
- `package.registry` in `data/projects.json` is one of `pypi` (pepy.tech badge
  scraped for the total), `npm` (registry API, summed in ≤540-day windows) or
  `github-releases` (sum of release asset downloads). Omit `package` for a
  project with no download count.
- **The weekly stats workflow triggers the deploy explicitly**
  (`gh workflow run deploy.yml`) after committing to `main`: a push made with
  `GITHUB_TOKEN` does not fire the `push` trigger of `deploy.yml`. Keep that step
  if you touch `update-project-stats.yml`.
- `CNAME` must stay in the repo root — `make site` copies it into `_site/`, and
  Pages is configured with **Source = GitHub Actions** (not a branch).
- Theme: an inline script in `<head>` applies the stored theme (`rr-theme` in
  `localStorage`) before first paint; `app.js` reads/writes the same key. Keep
  them in agreement.

## Conventions

- Site copy is Brazilian Portuguese (English only in `cv/cv-en.tex` and the
  "Resume (EN)" link); code, identifiers and commit messages are English.
- Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, `ci:`).
- CI lives in `.github/workflows/`; `auto-assign.yml` delegates to the shared
  `roquerodrigo/workflows` repo. There is no lint or test job.
