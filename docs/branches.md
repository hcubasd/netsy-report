# Publication graph

`v0` is the evolving template. Each publication has one long-lived branch (`v1`,
`v2`, or an agreed codename) containing only its own manuscript and infrastructure.
A new publication starts from the template or a specific commit in another paper.

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
General infrastructure changes originate on `v0`; venue-specific changes remain on
the paper branch. Do not routinely merge template manuscript changes into a paper.

Before a publication release:
1. Set `id`, `title` and the reserved `major` in publication.json; record `parent`.
2. Replace the placeholder and bibliography fixture with the actual manuscript.
3. Set `publish_pdf` to true only when PDF releases are appropriate.
4. Pass CI; tag the intended commit with its matching major version and push the tag.

No release tag is created by initialization. Template PDF publication is disabled.
Changing that policy requires an explicit source change; the guard also rejects
all major-zero PDF releases. Tags for template history can exist, but the release
workflow deliberately refuses to publish them.
