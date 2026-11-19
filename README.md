# NetSy — proposed Transportation Research Part D article

`trd` is the first original-research publication line. Target venue:
**Transportation Research Part D: Transport and Environment**. The title in
`publication.json` is a working identifier, not an approved article title.

The reusable SLR remains on `slr`, with [v0.2.0](https://github.com/hcubasd/netsy-report/releases/tag/v0.2.0)
as this branch's background baseline. Git ancestry and `publication.json.parent`
record the exact relationship. The SLR manuscript/search machinery is not
carried as this article's active content; it remains available on its own branch.
The inherited scientific bibliography and cached metadata are a starting pool,
not a final selection of references for the article.

## Start here

- [Venue reconnaissance](docs/venue/README.md).
- [Requirements and unresolved verification](docs/venue/requirements.md).
- [Patterns in three published articles](docs/venue/paper-patterns.md).
- [Proposed paper outline and evidence decisions](docs/venue/paper-plan.md).
- [Research design and experiment protocol](docs/experiment-plan.md).
- [Draft status](docs/draft.md) and [publication graph](docs/branches.md).

The live journal author guide returned HTTP 403. Exact current word limits,
review model and journal-specific submission requirements are not certified.
Official publisher policies and the official LaTeX archive were collected;
a historical 2022 guide is labelled as historical, not current authority.

## Build and publication

`make check` builds the **partial research manuscript (Methods and exploratory Results)**, runs infrastructure tests,
checks layout/references, and writes `dist/netsy-trd.pdf` plus provenance.
The manuscript remains incomplete and does not certify journal formatting. `make container`
uses the inherited pinned TeX image; CI does not run live package updates.

Branch pushes run CI. PDF publication is explicitly disabled for `trd`.
Future approved milestones on this line use `trd/vMAJOR.MINOR.PATCH` tags; no `trd/v1.0.0`
research release has been created. The source archive made for GitHub releases
is not an Editorial Manager submission bundle: a flattened source exporter and
journal-compatible bibliography workflow still need to be prepared.

Large source PDFs and retrieval snapshots stay outside Git, in the local recon
collection at `/workdir/docs/report-planning/trd-recon/`. The portable findings
are versioned in `docs/venue/`. Compact experimental evidence is versioned in `results/dutch-pilot/`; national
inputs, rasters and row-level outputs remain outside Git. Authorship and funding
statements are not invented, and no journal submission has been initiated.

The working experiment compares inherited versus Clarke–Wright parcel
scheduling under inherited versus declared COPERT factor/fleet configurations,
with grade-informed path sensitivities and separate source-correspondence
controls. See [execution instructions](analysis/README.md). `results/experiment-matrix.csv`
records planned roles; `results/evidence-inventory.json` inventories historical
audit evidence without relabelling it as new runs at the proposed model freeze.
