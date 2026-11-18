# Publication graph

`v0` is the NetSy literature-review publication line. `v1` is the proposed
Transportation Research Part D original-research line, initialized from v0.2.0
(`bc28fd1fea954fa772c9b4378b42684b8f4135f6`) with PDF releases disabled. Each publication has one long-lived branch (`v1`,
`v2`, or an agreed codename) containing only its own manuscript and infrastructure.
A new publication starts from a suitable infrastructure baseline or a specific commit in another paper.

Record its source branch/commit and scientific relationship in `publication.json`
(`parent`, e.g. {"branch": "v1", "commit": "FULL_SHA", "relationship": "..."}).
Git ancestry records manuscript history; it is not by itself scientific provenance.

Use immutable tags `vMAJOR.MINOR.PATCH`. On `v0`, examples are v0.1.0, v0.1.1,
v0.2.0. A correction applies to the latest state; older minor lines are not maintained.
Here major identifies a publication line, minor a significant milestone and patch
an incremental correction. This is a project convention, not an API compatibility
claim under strict Semantic Versioning. Tags are repository-wide: reserve a distinct
major number per publication, even if branches have descriptive codenames.

Keep infrastructure changes in separate commits so they can be cherry-picked.
General infrastructure changes may originate on `v0`; venue-specific changes remain on
the paper branch. Cherry-pick relevant infrastructure changes rather than routinely
merging another publication’s manuscript.

Before a publication release:
1. Set `id`, `title` and the reserved `major` in publication.json; record `parent`.
2. Replace the placeholder and bibliography fixture with the actual manuscript.
3. Set `publish_pdf` to true only when PDF releases are appropriate.
4. Pass CI; tag the intended commit with its matching major version and push the tag.

Initialization did not publish a PDF. The literature review now explicitly opts in to
PDF releases on v0, including v0.1.0. Every publication line, including major zero,
must set publish_pdf to true and use a tag matching its reserved major.
