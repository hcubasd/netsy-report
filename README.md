# NetSy publications

Shared starting point for publications derived from NetSy. This `v0` branch is
infrastructure and a minimal compiling template, not a research report.

## Build

With Docker: `make container`. This uses the image digest in
`infrastructure/texlive-image.txt`; no TeX installation or update occurs during CI.

With an existing TeX Live installation: `make check` (Python 3, make, latexmk,
pdfLaTeX and Biber required). Local dependencies must already be installed.
`make build` only compiles; `make check` also runs infrastructure tests, rejects
unresolved references/citations and overfull boxes, and collects the checked PDF
and build provenance in `dist/`. Underfull boxes remain informational.
`make clean` removes generated files.

## Layout

- `publication.json`: publication identity, release policy and parent manuscript.
- `manuscript/`: LaTeX entry point and sections; journal classes can differ by branch.
- `references/`: bibliography and reference metadata.
- `figures/`, `tables/`: assets used by this manuscript.
- `analysis/`, `results/`: generation scripts and small versioned numerical evidence.
- `infrastructure/`, `scripts/`: pinned TeX environment and common build tools.
- `docs/branches.md`: publication branching and release convention.

Large data and reference-paper PDFs stay outside Git. Root `data/` and `literature/`
are ignored optional local directories; small publication figure PDFs are allowed.

## CI and releases

Branch pushes and pull requests call the same build workflow. Obsolete CI runs on
the same ref are cancelled. Successful builds upload checked PDFs and provenance;
logs are retained even on failure. These CI artifacts are not GitHub releases.

Only a tag push matching `v*.*.*` can trigger CD. The exact tag must satisfy the
three-number format and the major in publication.json. Template releases are blocked.
An eligible tag rebuilds/checks the manuscript, then publishes the PDF, source archive,
provenance and SHA-256 checksums. Release jobs have write permission; checks do not.
See `docs/branches.md` before enabling publication on a paper branch.

No generated PDF, release, source from an old report, or previous Git history is
included in this initial repository. Legacy material remains outside this checkout.
