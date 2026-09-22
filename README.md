# netsy-report

Report on [netsy](https://github.com/hcubasd/netsy): the mathematical models behind its synthesis, and the shape of its data files. Work in progress.

## Build

Needs a TeX Live installation with the packages in `dependencies.txt`, which `scripts/install-dependencies.sh` installs with `tlmgr`.

```
make all     # builds dist/main.pdf
make clean
```

## Layout

- `src/main.tex`: preamble and document skeleton
- `src/development.tex`: the synthesis models
- `src/data-files.tex`: appendix with the data file shapes
- `src/references.bib`: bibliography

## CI

Every push builds the report. Pushing a tag like `v0.1.0` attaches `main.pdf` to a GitHub release.
