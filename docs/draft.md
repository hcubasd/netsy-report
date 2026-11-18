# NetSy literature review — v0.1.0

Title: **NetSy: A Network loads and emissions Synthesizer**. Publication line: `v0`.

The manuscript synthesizes seven academic domains with MASS-GT as a designated reference in each. Data availability, representation and transferability is both a domain and a cross-domain assessment dimension. NetSy implementation positioning and redesign are deferred to a separate exercise.

The 18 November revision reviews eleven institutionally obtained full texts, superseding two earlier one-page files. One unrelated upload is excluded. The current cohort has 61 complete documents: 59 domain evidence sources and two background sources. The appendix retains 33 actual paired query configurations, 29 supplementary discovery/access expressions, selection/appraisal methods, the fixed MASS-GT reference, provenance amendments and three remaining priority requests. It does not claim exhaustive search or complete independent screening of all database hits.

Portable evidence: `references/review-evidence.json`, `references/institutional-review.json`, `references/access-pending.json`, `results/review-selection.csv` and `results/source-search-map.csv`. Search parameters/timestamps are in `results/review-searches.json`; supplementary expressions in `results/review-supplements.json`. Large source PDFs remain outside Git. Institutional-access PDFs are not redistributed.

Build: `make check`; checked artifact: `dist/netsy-slr.pdf`. Normal builds require no API, reading-library access or package downloads. `publication.json` explicitly permits releases for major zero; branch pushes run CI, tag pushes run CD. Immutable release milestone: v0.1.0.
