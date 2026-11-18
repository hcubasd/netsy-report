# References and review provenance

`references.bib` contains cited research, official guidance and methodological sources. `metadata.json` caches bibliographic fields. Source-verified author/date/version corrections and non-DOI entries are explicit in `../analysis/build-bibliography.py`; regenerate with `--offline`.

`review-evidence.json` records every held source in the available-document cohort, with hash, identity, relevant domains, actual reading extent and inclusion/background/awaiting-full-text decision. Complete files and fully read papers are different states. The two earlier one-page files are superseded by institutionally obtained complete papers; historical versions remain in the external audit, not as duplicate included studies. The supplier-selection source is explicitly an author preprint, and publication versions remain distinguishable.

`access-pending.json` records unresolved access targets. They are not scientifically excluded or treated as supporting full-text evidence. The remaining three of the original 14 priorities appear in the printed appendix. Eleven received papers and one unrelated exclusion are recorded in institutional-review.json. `../results/review-selection.csv` is the readable held-source decision ledger. `../results/source-search-map.csv` links sources to exact query IDs or their supplementary routes. `../results/review-supplements.json` retains targeted web expressions. This does not claim complete screening of all database results.

Reference PDFs remain outside Git: reading collection `/workdir/docs/report-planning/canonical-literature/`, audit sibling `canonical-literature-audit/`. These paths document provenance; the manuscript build does not depend on them. No external PDF access is needed in CI.
