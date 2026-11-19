# Dutch exploratory experiment evidence

Frozen model: NetSy v0.5.0, `491b1d59c7d0cf5f8579f733afa6d1690a13abe6`.
Five independent upstream realizations, seeds 1–5; paired alternatives reuse
saved activity/demand as documented in the Methods. These are an exploratory
pilot, not a final precision-justified or source-equivalence sample.

- `input-snapshot.json`: immutable copied case inputs and SHA-256 values.
- `environment-model.txt`: model/analysis environment when the run snapshot was
  made; `environment-analysis.txt` additionally records retrieval dependencies
  installed during data collection. Core model dependency versions are unchanged.
- `terrain-summary.json`: accepted proxies and flagged fallbacks from native
  AHN4 5 m DTM/DSM tiles. No surveyed road-deck interpretation is claimed.
- `parcel-conservation.json`: same quantities by carrier and customer zone,
  fixed demand and tour counts; the case capacity is 180 parcels.
- `fixed-reference-control.json`: fresh frozen NetSy run using the existing
  imported MASS-GT reference trips. It is not a new MASS-GT simulation.
- Generated configuration/contrast CSV files, summaries and run provenance:
  produced by `analysis/summarize_experiments.py` only after all expected cells
  exist. Source artifacts remain outside Git in the recorded run directory.

Primary cross-configuration emissions use common physical-road factor support.
`all_g` totals deliberately retain diagnostics outside that support. Modern
COPERT fleet assumptions are not matched to inherited STREAM assumptions.
The PM boundary is unresolved; raw PM diagnostics are not a comparable accuracy
endpoint. There are no non-exhaust factors in this case. CO2 is nominal mass.

Parcel emission utilization is fixed at 0.5; its decline with onboard parcel
quantity is not modelled. `empty_network_vkt` in the raw summary means exactly
zero modelled utilization and is not complete empty parcel travel. The supplied
van COPERT coefficients are identical across grade bins, whereas truck factors
vary. Direct grade effects and path effects therefore have different boundaries.

Fixed demand, deterministic spatial parcel scheduling and time-independent
link speeds imply deterministic parcel aggregates conditional on this case;
small seed differences may be float32 aggregation noise. Repeated coincident
parcel outcomes are not additional evidence of generalization or accuracy.

`terrain-provenance.json` records source shapefile components, provider index
and augmented-network hashes, plus the exact-preservation check on original
network attributes and geometry. `terrain-tiles.json.gz` is a compact JSON list
of all 2,344 selected tile URLs, provider archive checksums and raster hashes;
it contains provenance, not the rasters. The separate raw retrieval cache is
retained in the local supplement directory.

`network-geometry-qa.json` checks source node coordinates against geometry
endpoints and records geometry/case kilometre discrepancies. The two accepted
links with >5% length discrepancies retain the original case kilometres for
network loading; grade uses geometry length, as declared in Methods.

`paired-control-checks.csv` verifies that scheduling contrasts leave nonparcel
VKT and CO2 unchanged (tolerances: 1e-5 km and 1 g). `baseline-regression.json`
compares the fresh seed-1 baseline with the historical NetSy audit, allowing
1e-6 km and 1 g for aggregate float precision; payload stratification can change
row counts without changing linear inherited emissions. `direct-grade-contrast.csv`
separates direct COPERT grade-factor response from path selection.
`scheduling-factor-interactions.csv` records differences between scheduling
contrasts under the two factor/fleet configurations; these are model-internal
interactions, not measured causal effects.

`emissions-input-provenance.json` records the exact original factor table,
COPERT workbook and adapter hashes. The case uses July 2026 Appendix 4 data
(COPERT 5.10); CO2 is derived from energy consumption at 74.1 g/MJ diesel.
Inherited fuel-carbon conventions are not reconstructed or harmonized.
