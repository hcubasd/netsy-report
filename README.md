# NetSy publications

NetSy: **A Network loads and emissions Synthesizer**.

Publication infrastructure and the NetSy literature review on `v0`.
The current available-evidence review uses eight search strands: six subject
areas, data availability/transferability, and MASS-GT reference discovery.
Findings follow seven functional responsibilities, with data requirements and
the MASS-GT configuration integrated into every section.
A search/selection appendix prints all 33 retained query pairs, including
model-name refinement, and records the limits of the current evidence base.
Model positioning and implementation choices are deliberately deferred.
The v0 line explicitly opts in to tagged PDF releases.
Release v0.2.0 reorganizes the synthesis while retaining the evidence cohort of
v0.1.0; the earlier published tag remains unchanged.

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
three-number format and the major in publication.json. Publication lines without explicit opt-in are blocked.
An eligible tag rebuilds/checks the manuscript, then publishes the PDF, source archive,
provenance and SHA-256 checksums. Release jobs have write permission; checks do not.
See `docs/branches.md` before enabling publication on a paper branch.

The checked local review is `dist/netsy-slr.pdf`. Build outputs are ignored and
are not source-controlled. Tagged releases are enabled for this review line. Reference PDFs and the full
review audit remain outside this checkout; portable query/reading metadata are
versioned in `results/` and `references/`. See `docs/draft.md` for scope and provenance.
`results/synthesis-framework.json` describes the search-to-function mapping;
`results/source-function-map.csv` indexes citations by functional section.
The historical `domains` fields in imported evidence retain search-strand
identifiers A1–A7; they are not the new functional section numbers.
