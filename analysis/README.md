# Dutch experiment execution

These scripts run the frozen NetSy v0.5.0 model without modifying model code.
Run data and downloaded rasters stay outside Git under
`/workdir/docs/validation/paper-v1/`. Compact derived evidence is placed in
`results/dutch-pilot/`; no national geodata or row-level outputs are committed.

The local analysis environment is `/workdir/netsy/.venv/bin/python` (its exact
freeze is recorded with each experiment). Additional geospatial dependency:
rasterio. The report build itself does not require the analysis environment.
The scripts currently assume the documented `/workdir` project layout.

1. Run `complement_grades.py /workdir/docs/validation/paper-v1/elevation`.
   It selects official AHN4 5 m DTM/DSM tiles for physical source nodes, verifies
   provider archive checksums, samples endpoint elevations, screens uncertain
   links and produces a separate augmented network and provenance. The initial
   WCS retrieval was abandoned for performance; its cached rasters are not used.
2. Run `run_paper_experiments.py RUN_ROOT --prepare` (seeds default to 1–5).
3. Run `run_paper_experiments.py RUN_ROOT --execute` for the paired factorial.
   Successful stages resume from their local completion stamps. These are not
   arbitrary mutable-input caches: keep the frozen input snapshot, coefficients
   and case directories unchanged. Start a separate run root after changes.
4. Run `summarize_experiments.py RUN_ROOT` from the report repository root.
5. Run `make check` to build the partial manuscript.

`--execute --assign-only --coefficients 0` can prepare zero-penalty paths before
terrain retrieval finishes; terrain is required before any emission assessment.
Once complete, both graded and ungraded paths are assessed against the same
augmented network. `--seeds` selects disjoint realization subsets if needed.
Keep memory-heavy assignments within available RAM; observed per-process memory
is several GB. No runtime comparison is inferred from these heterogeneous runs.

The execution cache stores only deterministic Dijkstra predecessors. Its key
contains the exact cost graph and SciPy version; process-specific temporary
files and atomic replacement support independent processes. No stochastic
activity or alternative cost graph shares a cache entry by assumption.

Verification:

```
PYTHONPATH=/workdir/netsy/src /workdir/netsy/.venv/bin/python analysis/test_experiment_controls.py
```

This checks directional grade arithmetic/fallbacks, assignment identity with
and without path caching, and full-frame versus batched frozen emissions.
National-run checks additionally require finite emissions, preserved row/link
identity, known parcel stream, all expected cells and conserved parcel totals.
The five realizations are a pilot, not a precision-justified final sample.

`inventory-evidence.py` retains its separate purpose: it inspects historical
audit hashes and case schemas using only the standard library, without running
models. Shared nicrainha palette tooling is retained for figures when colour
is useful; the current comparison figure uses grayscale.

National assignment subprocesses acquire a shared file lock, so only one
memory-heavy assignment runs at a time even with separate realization runners.
Emission assessments can overlap an assignment. A first attempt with overlapping
assignments had an out-of-memory kill; successful artifacts were retained and
the affected case resumed under the lock. Runtime records include waiting and
heterogeneous execution conditions and are not performance benchmarks.
