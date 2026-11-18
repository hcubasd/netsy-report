# Patterns in published TR-D articles

Three complete publisher-version papers were downloaded from institutional repositories. This is a purposive sample for article architecture, not a systematic survey of editorial decisions or evidence of a universally required structure. Inspection covered front matter, section structure, selected methods/results, discussion, conclusions and end matter. It is not a fresh full scientific appraisal of every model or numerical result.

## Downloaded examples

| Local ID | Published article | Why inspect it | Observed architecture |
|---|---|---|---|
| P01 | Ghisolfi et al. (2024), [Dynamics of freight transport decarbonization: A simulation study for Brazil](https://doi.org/10.1016/j.trd.2023.104020) | Freight simulation connecting model structure, scenario assumptions and environmental interpretation | Introduction; literature review; empirical context; model; results; discussion; conclusions; technical appendices |
| P03 | Weber et al. (2025), [Exhaust emission rates along German inland waterways](https://doi.org/10.1016/j.trd.2025.104955) | Bottom-up activity-to-emissions chain with explicit operating conditions and coverage limits | Introduction; methods and data; combined results/discussion; conclusion; supplements and availability statement |
| P04 | Galkin et al. (2025), [Navigating the future of urban logistics: Conceptual framework for Dynamic Freight Management](https://doi.org/10.1016/j.trd.2025.104956) | Urban-freight framework and scenario presentation | Introduction; literature review; methodology; results; discussion; conclusions; appendix and declarations |

All three PDFs show acceptance and publication details. P01 was accepted 10 December 2023 and published online 15 January 2024; P03 was accepted 6 August 2025 and published online 16 August; P04 was accepted 6 August 2025 and published online 20 August. The DOI year and journal-volume year need not match: P01's correct DOI contains **2023**, although its issue is 2024. Its initial guessed DOI was corrected against the PDF.

### P01 — model, case and experiment are distinguishable

The paper separately establishes the case, presents interacting submodels, reports baseline and policy scenarios, and interprets implementation timing. Detailed equations and model tests are placed in appendices; sensitivity inputs are tabulated. Its policy discussion also acknowledges assumptions and limits. Useful pattern: keep the framework, its case-specific configuration and the experiment distinguishable. Do not borrow its particular decarbonization conclusions for NetSy.

Inspected: PDF pp. 2–5 (front matter, rationale and context), 12–13 (implementation and uncertainty), 18–22 (discussion/conclusions/end matter), plus section/caption structure throughout. The repository adds a cover page: physical PDF pages differ from printed article pages.

### P03 — environmental quantities organize the account

The methods explain observation coverage, data processing and the activity-to-emissions chain before results at different scales and a fleet scenario. The conclusion identifies operational situations the model does not cover. Useful pattern: define outputs and units, explain missing/approximated inputs, and relate mechanism-level findings to network totals. This is a waterway model; its equations and empirical performance are not a road-freight benchmark.

Inspected: PDF pp. 1–5 (rationale, formulation and data), 11–12 (conclusion, limitations, declarations and data statement), and the result-section structure on pp. 6–10. “Data available on request” is an observed statement, not proof of generally obtainable inputs or the current journal's minimum data policy.

### P04 — a framework becomes a bounded application

The article moves from a conceptual framework to operational logic, a named study area and scenario results, followed by practical interpretation. Its conclusion acknowledges dependence on simulation and limits to transfer. Useful pattern: identify who could use the findings and under which conditions. We should independently substantiate our own empirical claims rather than emulate novelty language or treat simulation as a realized policy effect.

Inspected: PDF pp. 1–5 (framework and methods), pp. 18–21 (discussion, limitations and end matter), and the results' section/caption structure on pp. 12–17.

## Descriptive size observations — not author limits

| ID | Physical PDF pages | Main-text numbered figures / tables | Rough extracted body tokens |
|---|---:|---:|---:|
| P01 | 34, including repository cover and appendices | 16 / 10 | 11,850 |
| P03 | 14 | 6 / 1 | 7,737 |
| P04 | 23 | 12 / 9 | 11,471 |

Token counts are whitespace splits between “1. Introduction” and the first CRediT heading in `pdftotext -layout` output. They include table cells, captions, equations and running headers, can include extraction artifacts, and are **not journal word counts**. Figure/table counts come from main-text caption numbering. Neither these measures nor final publisher layouts establish a submission maximum. `papers/structure-metrics.json` records the computation.

## Patterns we can reasonably adapt

These are our cross-paper inferences, not publisher rules:

1. Start with an environmental or transport-management problem, then identify the modelling gap and contribution.
2. Explain the formulation separately from the local evidence used to configure it.
3. State scenarios, assumptions and comparison conditions before interpreting results.
4. Organize results around scientific questions and environmental consequences, rather than listing software modules or commits.
5. Use figures/tables for mechanisms, input provenance and comparisons; place exhaustive technical material in appendices/supplements where appropriate.
6. Discuss implications within the evidence boundary. Keep calibration, source reproduction, independent validation and sensitivity analysis distinct.
7. Both separate and combined results/discussion structures occur; neither is a universal editorial requirement.

## Additional candidates not used for full-text pattern claims

- Heinold (2020), [Comparing emission estimation models for rail freight transportation](https://doi.org/10.1016/j.trd.2020.102468). Publisher abstract/intro and bibliographic identity were available, but no complete PDF was obtained. The attempted thesis download returned HTML. A promising example for controlled model comparisons; not included in the measured sample.
- Pagnier et al. (2026), [Linking freight transport and energy system models for strategic investments decisions](https://doi.org/10.1016/j.trd.2025.105114). Publisher abstract/selected section text was available; no complete PDF obtained. Do not infer its entire final structure from snippets or substitute a one-page SSRN abstract.
- Rosenberg et al. (2023), [Modelling the interaction between the energy system and road freight in Norway](https://doi.org/10.1016/j.trd.2022.103569). Old repository hostname no longer resolved in this container; not read in full or included in the structural sample.

Tirico et al. (2025), already in our SLR, is published in *Sustainable Cities and Society*, so it was not counted as a TR-D venue example. Existing SLR evidence remains background rather than becoming journal-specific guidance.
