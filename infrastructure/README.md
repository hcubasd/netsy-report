# TeX toolchain

`texlive-image.txt` is the single container-image pin used by `make container`, CI
and release builds. It identifies the full upstream TeX Live image by immutable
multi-platform digest, resolved from `texlive/texlive:latest` on 2026-10-28. The
registry index includes linux/amd64 and linux/arm64 manifests. Normal builds do
not resolve `latest`, install packages or run `tlmgr`.

The full image trades a larger download for packages already baked upstream.
There is no custom image to publish or registry credential to configure. If size
becomes a problem, build a smaller image with its dependencies preinstalled and
replace this pin with the tested result; keep package installation outside report
builds. A committed Dockerfile alone would not pin a live package repository.

To update: select a new image digest, change this file in a dedicated infrastructure
commit, run `make container`, review the PDF and checks, then selectively cherry-pick
that commit into publication branches. Do not automatically update frozen submissions.

The image makes TeX dependencies repeatable; we do not promise byte-identical PDFs
across arbitrary local environments. Container builds set SOURCE_DATE_EPOCH from
the source commit. Build metadata records the source revision, actual tool versions
and container pin (when run through the container wrapper).

Upstream: https://github.com/islandoftex/texlive
