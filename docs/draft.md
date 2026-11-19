# First research-paper status

Branch: `trd`. Target: Transportation Research Part D: Transport and Environment.
Active title: **NetSy: A Network loads and emissions Synthesizer**.
Publication ID: `netsy-trd`; PDF releases remain disabled.

The draft now develops Materials and methods, a refreshed fixed-source-trip
correspondence result, terrain data quality, and the Dutch exploratory factorial
results. It is a partial research manuscript, not a complete article or a
journal-ready submission. No finished Introduction, Abstract, overall Discussion
or policy conclusion is implied. The original one-page design brief is preserved
in `docs/history/`.

Background baseline: NetSy SLR v0.2.0 / `bc28fd1fea954fa772c9b4378b42684b8f4135f6`.
The reusable SLR manuscript and its search records stay on `slr`; selected
scientific references support this original-research manuscript.

The frozen experiment uses NetSy v0.5.0, five paired upstream realizations,
two parcel schedulers, three uphill-cost coefficients and two factor/fleet
configurations. The five runs are an exploratory pilot, not a sufficient-sample
or distributional-equivalence claim. The AHN4 grades are screened terrain proxies,
with flagged fallbacks. COPERT fleet assumptions remain unmatched to inherited
factors; no cross-method emissions-accuracy or non-exhaust result is claimed.

Read `docs/experiment-plan.md` (including its execution amendment),
`analysis/README.md` and `results/dutch-pilot/README.md` for interpretation and
reproduction. Large artifacts stay under `/workdir/docs/validation/paper-v1/`.
The supplemented network is also accessible through
`/workdir/netherlands/terrain-ahn4/network.gpkg`; original case inputs remain
preserved.

Authorship, empirical validation, final inferential design, road-deck grade
validation/sensitivity, fleet harmonization and the final scientific claim
remain author decisions. The exact current journal author guide still needs
verification following the recorded HTTP 403; `docs/venue/` retains the recon.
Prepare a journal-compatible template and flattened submission export after
that verification. No release tag or submission is created by this work.
