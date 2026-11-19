# Proposed first-paper architecture and evidence decisions

This venue-oriented outline is planning, not manuscript text or an approved title.
The working research design is now in [the experiment protocol](../experiment-plan.md). The background source is SLR v0.2.0, branch `slr`, commit `bc28fd1fea954fa772c9b4378b42684b8f4135f6`.

## Article rather than SLR

The research article should answer a bounded question about freight network-load and emissions assessment. The SLR supplies concepts and references; the paper needs its own methods, experiment and findings. It need not reproduce the SLR's eight search strands or seven functional subsections as its article structure. A compact functional account can explain the relevant modelling responsibilities without becoming a software manual.

An environmental framing to develop with the advisor is: **how do routing and emissions formulations change the interpretation of freight network environmental outcomes, after establishing a reproducible reference-consistent baseline?** This is a candidate emphasis, not a claim that the experimental results already support it or that general-purpose transfer has been demonstrated.

## Working outline

| Section | Job in this paper | Evidence/material |
|---|---|---|
| 1. Introduction | Environmental problem, methodological gap, research question and explicit contributions | Selected SLR findings; why the Dutch benchmark is informative |
| 2. Background and related work | Position the chosen formulations and the reference configuration | Focused sources, not the complete SLR or its search appendix |
| 3. Framework, study area and data | Define the model boundary, relevant functional responsibilities and Dutch configuration | Data provenance/access, units/classifications, observed versus assumed inputs, versions |
| 4. Experimental and assessment design | Define comparisons, controls, interventions, metrics and uncertainty | Source and repaired reference; inherited baseline; isolated routing/factor changes; seeds and assessment targets |
| 5. Results | Answer research questions with controlled evidence | Environmental outputs and mechanisms, supported by baseline correspondence and operational indicators |
| 6. Discussion | Explain consequences, trade-offs, applicability and limitations | Model divergence versus accuracy; fleet/data/terrain assumptions; policy relevance within scope |
| 7. Conclusions | State supported findings and their bounded implications | No untested claims of transfer, adoption or measured accuracy |
| Appendices/supplements | Reproducibility and detail that would interrupt the argument | Tables/crosswalks, equations where needed, repair log, extra comparisons, configurations and accessible code/data links |

This outline is our recommendation. Current live-guide length/layout rules still need confirmation. Separate Results and Discussion is a working choice; published examples also combine them.

## Scientific decisions before drafting results

### 1. What counts as validation?

Existing Dutch checks establish correspondence with a particular MASS-GT implementation and account for identified differences. They are not independent observations of reality. The source reference, minimal repairs, NetSy baseline and modelling alternatives must be distinguishable. Three NetSy seeds against one source realization do not provide a stochastic-equivalence test or source-model variance estimate. Decide which independent evidence supports which claimed outcome and whether additional runs are needed; do not automatically generate a seed count without a precision target.

### 2. What is genuinely changed?

Clarke–Wright is an established optional parcel-tour heuristic, not a novel routing algorithm. NetSy v0.5.0 also adds configurable uphill/downhill Dijkstra penalties. Those penalties are declared route preferences, not a calibrated energy optimizer or an implementation of the advisor paper's entire route-cost formulation. COPERT V is an established emissions method; integration and the controlled findings may be contributions without claiming new factor theory. Bug fixes, execution speedups, generalization and modelling alternatives need separate attribution.

### 3. What can the Dutch configuration actually test?

The recorded COPERT example assumes a fleet and flat network grades. Flat grades cannot demonstrate a geographical benefit from grade-aware paths. A terrain experiment needs defensible signed gradients, chosen/justified costs and suitable assessment, or a clearly labelled synthetic mechanism test with appropriately limited claims. Changes in paths and changes in factors should first be isolated. Preserve trips, fleet, operating assumptions and reference versions where needed to attribute differences.

### 4. What environmental boundary is defensible?

State pollutants, energy/GHG conversion, exhaust/non-exhaust coverage and spatial/temporal aggregation. The existing example has no non-exhaust input and is not an observed Dutch fleet estimate. Do not infer emissions accuracy from traffic-count fit or model disagreement. Explain whether the outcome is a planning sensitivity, model-transfer check or empirically validated prediction.

### 5. What must be available to others?

Version code, settings, source repairs, seeds and shareable outputs. Verify permission before redistributing source datasets. Explain restricted inputs and reproducibility limits. The final submission export must be separate from GitHub's source archive and tested with the journal's source workflow.

## Branch setup

Reserve `trd` for this research article, with `publication.json.release_namespace = "trd"`, a parent link to the exact `slr` source commit, and `publish_pdf = false` until an actual manuscript milestone is approved. Do not release the inherited SLR as `trd/v1.0.0`. The active manuscript now develops Methods and exploratory Results from the frozen Dutch experiments; the original design brief is retained in `docs/history/`. Authorship and the final article remain to be developed.
