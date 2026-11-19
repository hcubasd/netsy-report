# Article analyses

No new research experiments are implemented in this branch yet. The SLR-only
import, bibliography-generation and synthesis-index scripts remain on v0.
Shared nicrainha palette tooling is inherited for figures when useful.

Before adding manuscript results, define the experiment design, case/version
provenance, metrics, seeds and sharing boundaries. See `docs/venue/paper-plan.md`.
Venue retrievals and PDF inspection material are in the external recon
collection; portable findings are in `docs/venue/`.

`python analysis/inventory-evidence.py [AUDIT_DIRECTORY]` records selected
historical audit hashes and case-schema checks. It uses standard-library
read-only inspection, requires the external audit/case files, and is not part
of CI. It does not execute experiments or generate result findings.
