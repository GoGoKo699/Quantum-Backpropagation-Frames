# Reproduce the bounded final comparison

Use the frozen PF-07 code to generate the same input, then analyze it:

```bash
python results/PF-07/study.py --output runs/pf07-fixed
python results/PF-08/compare.py --input runs/pf07-fixed/diagnostics.json --output runs/pf08-final
```

Both output directories must be new. The analysis has no numerical dependency
beyond the Python standard library; the inherited study uses pinned NumPy. It
verifies the source identities, exact grid labels/counts, finite risks and raw
normalization. Eight independent bookkeeping/validation tests run before output.
The analysis emits small_comparison.csv, scaling_tradeoff.csv, quantum_projection.json,
summary.json and tests.log. No new model or optimization is run.

For the full original integration regression, use a clean full Git checkout and
`python tools/integration_check.py --output runs/integration-pf08`. The single
read-only workflow also verifies prior packet manifests and reruns PF-04 through
PF-07. New PF-08 output is generated from that same run's PF-07 result.

A fresh environment need not reproduce elapsed times or identical floating
bytes. Frozen code hashes and the comparison coverage are enforced. Physical
simulation stays in the inherited n<=8 diagnostics; n<=256 records are compiler
ledgers, not large-state simulations. Do not interpret reanalysis as external
review, new asymptotic evidence, measured timings or stronger novelty clearance.
