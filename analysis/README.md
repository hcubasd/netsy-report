# Review data and figure generation

The manuscript builds from versioned TeX, bibliography and small metadata files;
CI does not query scholarly APIs, access the reading library or install Node.

- `generate-palette.mjs`: optional colour tooling from the first layout, using
  **nicrainha 1.1.0**, pinned in `package-lock.json`. Regenerate with
  `npm ci --ignore-scripts && npm run palette` in this directory (Node 24).
  Exact library RGB output is stored in `../figures/palette.tex`; the n-gon,
  lightness and rotation are recorded in `../results/palette.json`.
- `import-review.py AUDIT_ROOT`: imports the dated search specifications,
  all three retrieval rounds, held-source eligibility decisions, pending-access
  records and reading provenance from the external canonical-literature audit.
  Generates the exact-search appendix, source-to-query map and portable supporting metadata, incorporating the dated institutional-review overlay; normal
  builds do not rerun the import.
- `build-bibliography.py`: creates the bibliography from the reviewed DOI list and
  verified source manifests. Dated Crossref/OpenAlex bibliographic metadata is cached in
  `../references/metadata.json`. Non-DOI sources and manifestation corrections are
  explicit in the script. Run with `--offline` to use the existing cache.

The current manuscript uses no figures or colour assets. The optional palette
helper is not a build dependency. Reference PDFs and full search/access logs
remain outside Git.
