# Publication graph

`slr` is the reusable literature-review line (formerly `v0`). `trd` is the
Transportation Research Part D original-research line (formerly `v1`), descended
from SLR v0.2.0, commit `bc28fd1fea954fa772c9b4378b42684b8f4135f6`.
Each publication has its own manuscript and independent version sequence.
New publications may branch from a specific commit in either line. Record the
source commit and scientific relationship in `publication.json.parent`.

Release tags are namespaced: `slr/v0.2.1`, `slr/v0.3.0`, `trd/v0.1.0`,
`trd/v1.0.0`. Minor versions denote substantial developments; patches denote
corrections. Define the meaning of a 1.0 milestone for each publication before
releasing it. Versions describe manuscript development, not API compatibility.
Historical unprefixed tags (`v0.1.0`, `v0.2.0`, etc.) stay immutable and continue
to identify their original commits and releases. No replacement tags are needed.

Branch pushes run CI. Tag pushes run CD, requiring both a matching
`release_namespace` and `publish_pdf: true` in that commit's publication metadata.
The SLR opts into PDF releases; TR-D remains opted out. Renaming the branches
creates no release. Build first, then tag a reviewed commit and push that tag.
Source-archive filenames replace the tag's slash with a hyphen.

Cherry-pick shared infrastructure fixes between publications as appropriate;
do not routinely merge one manuscript into another. Existing clones can rename
local branches with `git branch -m v0 slr` and `git branch -m v1 trd`, fetch with
`--prune`, and set upstreams to `origin/slr` and `origin/trd`. Fresh clones can
use `git switch --track origin/slr` or `git switch --track origin/trd`.
