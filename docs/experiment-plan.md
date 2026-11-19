# First-paper research design — working protocol

19 November 2026. Branch `v1`; target: Transportation Research Part D.
Status: initial design, not a preregistration, completed experiment or approved
claim of improvement. The one-page brief is built from `manuscript/main.tex`.

## Question, contribution and scope

**Main question:** How do parcel-tour construction and emissions formulations
affect freight network environmental estimates in a controlled Dutch application?

- **RQ1 — reference correspondence:** Where does the generalized implementation
  reproduce the source configuration, and which residuals arise from randomness,
  explicit source repairs or changed assumptions?
- **RQ2 — operational sensitivity:** For the same parcel demand and operating
  constraints, how does Clarke–Wright change tours, vehicle activity and emissions
  relative to the corrected inherited scheduler?
- **RQ3 — environmental sensitivity:** How do the declared emission-factor/fleet
  configurations change totals and spatial patterns on fixed activity, and does
  their choice change the estimated effect of the scheduling alternative?

The proposed contribution is a reproducible framework and a controlled account
of environmental sensitivity, supported by reference correspondence. Neither
Clarke–Wright, Dijkstra nor COPERT is claimed as a new algorithm. Generalized
interfaces and Dutch correspondence do not demonstrate geographical transfer.
Higher accuracy requires independent observations appropriate to the outcome.

The core study is the existing Dutch freight/parcel/service configuration and
its external gateways. Stockholm is outside scope. UCC/microhub scenarios are
supporting correspondence checks unless an explicit question justifies expanding
the environmental experiment. Published MASS-GT microhub functionality is not
claimed as a NetSy invention.

## Versions and study boundary

- Literature baseline: SLR `v0.2.0`, commit
  `bc28fd1fea954fa772c9b4378b42684b8f4135f6`.
- Proposed implementation freeze: NetSy `v0.5.0`, commit
  `491b1d59c7d0cf5f8579f733afa6d1690a13abe6`. A subsequent code change requires
  a new recorded snapshot and rechecking affected comparisons.
- MASS-GT checkout: `4f727c3633bf5edabc1b0d0fa081a9e232bf169a`, with existing
  execution/compatibility changes identified in the audit. Raw outputs, execution
  repairs and corrections to model logic must have separate identities.
- Source of preliminary evidence: `/workdir/docs/validation/README.md` and
  `results/*.json`. These are historical audit outputs, **not reruns at the new
  freeze**. The inventory in `results/evidence-inventory.json` records their
  hashes and limits; it is not a new result table.

Use the same modelled period and units throughout, explicitly reconciling hourly
tour departures and period-level service matrices. Do not relabel a modelled
period as an observed national day. No congestion feedback, exposure or life-cycle
outcome is implied by the present supplied-speed network/emissions chain.

## Comparison matrix

### Correspondence controls

1. **M-RAW / M-EXEC:** retain the source outputs and an executable reference with
   individually documented compatibility/execution repairs. Do not count those
   repairs as a new modelling formulation.
2. **M-CORR:** retain explicitly corrected source calculations where available;
   otherwise identify the expected correction analytically. Do not invent a
   complete corrected source run that does not exist.
3. **FIXED-TRIPS:** load the same source tours, parcel schedule and van matrices
   into NetSy with inherited factors, then explain link-level residuals and
   source-factor corrections. This isolates downstream correspondence from
   upstream stochastic synthesis.
4. **N00:** establish the corrected inherited NetSy baseline, with grade penalties
   zero and `route_samples = 1`, before interpreting alternatives.

### Core factorial experiment

| Configuration | Parcel-tour construction | Emissions configuration |
|---|---|---|
| N00 | Corrected inherited scheduling | Inherited factor configuration |
| N10 | Clarke–Wright savings | Same inherited factor configuration |
| N01 | Same activity as N00 | Declared COPERT fleet/factors |
| N11 | Same activity as N10 | Same declared COPERT fleet/factors |

For N00 versus N10, hold upstream demand, customer quantities, depots, carrier
grouping, fleet availability, capacities, service assumptions, network and
supplied speeds fixed. Include depot returns and empty movements. Departure
generation must use a declared common protocol; changed tour counts do not
permit identical per-tour timestamps. If link speeds vary by interval, report
the temporal contribution or add a fixed-speed control before attributing all
differences to distance savings. Freight and service trips remain fixed within
each paired replicate; only the parcel-scheduling treatment changes them.

For N00 versus N01 and N10 versus N11, **reuse identical saved link activity**,
speed, payload strata and time aggregation. If payload-bin loading is needed,
use that same representation for both factor calculations, checking that legacy
totals are preserved within documented numerical tolerance. Keep exhaust and
non-exhaust outputs separate.

The historical STREAM configuration's implied technology/fleet and pollutant
boundaries must be identified. If fleet assumptions cannot be harmonized,
describe the contrast as **factor/fleet-configuration sensitivity**, not a pure
emissions-formula effect. If environmental boundaries cannot be reconciled,
omit that cross-configuration endpoint rather than comparing unlike quantities.
Evaluate the scheduling effect within each emissions configuration and the
difference between those effects; do not interpret this internal model contrast
as a measured causal effect in the real transport system.

## Outcomes and assessment

**Primary planned endpoint:** absolute and relative change in modelled-period
network CO2, with a common, documented carbon/system boundary. Report both the
affected parcel stream and the entire freight/parcel/service network.

**Secondary:** NOx and exhaust PM only after pollutant definitions and coverage
are reconciled; spatial distribution at fixed link/area resolution; parcel and
whole-network VKT; empty VKT; tour/vehicle counts; utilization; demand served;
and capacity/window feasibility where represented. CO may be reported within
the COPERT configurations, but is not automatically comparable with source
factors. Do not label CO2 as CO2e or report the energy field as pollutant mass.

For correspondence, report conservation checks, demand/OD differences, shipment
and tour distributions, and link-load MAE/RMSE and total differences. Separate
connector and ordinary-road residuals. Percent differences need a defined
nonzero denominator; do not use MAPE over zero-flow links. Document units and
finite-precision tolerances before using numerical equality as a gate.

Spatial summaries use consistent boundaries, bins and normalization. A map of
modelled emissions is not an exposure estimate. Links, hours and customers are
not independent stochastic replications.

## Randomness and uncertainty

Use paired comparisons sharing the **same saved upstream realization** for each
replicate; using the same integer seed in different algorithms is not evidence
of identical random streams. Record stage seeds and artifact hashes. Separate
synthesis randomness from input/parameter uncertainty.

Start with a planned pilot of five paired upstream realizations. This is a
workload/pilot choice, not a sufficient sample size or power claim. Measure
variability of the paired contrasts, then set and document an absolute precision
target in relevant units, a final fixed replication count and computational
cap before the confirmatory batch. A near-zero contrast needs an absolute,
not solely relative, precision criterion. Do not repeatedly test significance
and stop when a preferred conclusion appears. Report pilot versus final-run
roles and Monte Carlo uncertainty conditional on the frozen inputs.

If an outcome is deterministic under the frozen case, report that and do not
inflate its apparent evidence by repeating it. Existing seeds 1–3 contain only
one complete assignment/emissions chain and one source realization. They do not
provide a distributional-equivalence test. Formal source-model equivalence would
additionally require repeated source runs and justified equivalence margins;
otherwise restrict the claim to fixed-reference correspondence.

## Grade-informed paths and other extensions

Grade routing is **not a core experiment yet**. The inspected historical COPERT
network has no `grade` field; default-flat emissions are not measured terrain.
NetSy's new grade coefficients express route preferences, not calibrated energy
consumption, payload-dependent route costs or regenerative braking.

A terrain extension requires directional grade data, documented units/coverage,
justified coefficients and feasible vehicle restrictions. First isolate a
grade-cost path change with the emissions method fixed, then factor changes on
the same paths. A synthetic mechanism test may establish implementation
behaviour, but must not be presented as a Dutch geographical or policy result.
Its inclusion needs a clearly stated incremental scientific question.

## Gates and execution order

1. **Freeze/provenance:** manifest code, environment, data, adapters and repairs;
   preserve old runs and use isolated new output directories.
2. **Accounting:** reconcile periods, units, demand conservation and factor
   coverage; reject silent omissions and explain numerical residuals.
3. **Environmental comparability:** check fleet mappings, CO2/NOx/PM definitions,
   energy conversion and exhaust boundaries before assigning endpoint roles.
4. **Controls:** refresh the necessary correspondence controls at the frozen
   version; prepare the four configurations and shared-activity checks.
5. **Pilot/design lock:** assess variance, choose precision/replications and
   record changes to this plan before the main experiment.
6. **Analysis:** report all planned contrasts, including small or adverse effects;
   distinguish model sensitivity, source repairs and empirical validity.

The first evidence displays should be an input/version/boundary table, a compact
correspondence table, paired operational/emissions contrasts and a spatial
comparison if it adds information. Do not draw result charts before results
exist. The live TR-D guide remains unverified; its formatting restrictions do
not settle this scientific design. AI-assisted planning and subsequent research
assistance must be documented under the collected publisher policy, with author
review before submission.
