# Continuing the publications

Clone `https://github.com/hcubasd/netsy-report.git` separately, then switch to
`slr` for the literature review or `trd` for the research article. Each branch
contains its own manuscript; keep publication-specific writing on that branch.
Run `make check` locally, or `make container` with Docker for the pinned TeX build.
Branch pushes run CI. Release tags use `slr/vMAJOR.MINOR.PATCH` or
`trd/vMAJOR.MINOR.PATCH`; TR-D PDF releases remain disabled.

The separate `netsy-report-handoff` resource directory contains the paper PDFs,
search snapshots/strings, reading notes, venue guidance and experiment inputs.
It contains no repository clone. Start with its `START-HERE.md` and
`RESOURCE-CATALOG.md`. Its dated snapshots are evidence of past searches, not
instructions to present an unfinished review as a fully screened SLR.

On `slr`, start with `docs/review-status.md`, `docs/review-protocol.md` where
present, the manuscript's review methodology and the generated search appendix.
The latest narrative uses functional responsibilities; the six academic fields,
data feasibility and MASS-GT remain separate search strands. Historical reading
reports can use earlier seven-bucket terminology. The manuscript and latest
institutional-review overlay take precedence over those historical summaries.

On `trd`, start with `docs/draft.md`, `docs/experiment-plan.md`,
`results/dutch-pilot/README.md` and `docs/venue/requirements.md`. Five paired
realizations and 60 main configuration results are exploratory, not independent
empirical validation. Road grades are screened AHN terrain proxies; fleet and
fuel-carbon assumptions are not harmonized between emission configurations.
The live journal author guide still needs verification.

The resource bundle records preserved input hashes and omitted regenerable
files. Large raster caches, Dijkstra caches and row-level simulation outputs
are not required to edit or build either manuscript and stay outside Git.
Keep research source PDFs and externally supplied inputs outside the clone.
