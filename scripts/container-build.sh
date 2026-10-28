#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
image=$(cat infrastructure/texlive-image.txt)
SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH:-$(git log -1 --format=%ct)}
export SOURCE_DATE_EPOCH
exec docker run --rm \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp -e TZ=UTC -e SOURCE_DATE_EPOCH -e FORCE_SOURCE_DATE=1 \
  -e "NETSY_TEX_IMAGE=$image" \
  -v "$PWD:/workdir" -w /workdir "$image" make check
