# Reproduce PF-04

From a clean full checkout of research/PF-04-boundary, using root requirements:

```bash
python -m pip install -r requirements.txt
python tools/integration_check.py --output runs/pf04-integration
python results/PF-04/study.py --output runs/pf04-study
```

Both output directories must be new. The integration gate reruns the 36 existing
tests, preserved diagnostics and the identical PF-02 acceptance grid. The study
separately prints and saves eight check groups and its structural data. Only the
small equivalence check imports the preserved matched-readout fixture; its
SHA-256 is checked. No historical results or maintained functions are overwritten.

The study's moment and flat-spectrum risk formulas are checked against actual
POVM matrices and Born probabilities. The broad lower bound is also tested on
independently generated overcomplete mixtures with exact first-moment
reconstruction. These are finite diagnostics, not numerical minimax proofs.

The growing-size compiler uses no global statevector. Its per-wire causal graph
and local gate operations are independently compared with the inherited dense
fixture through six qubits. The reported entry counts are operation/representation
sizes, not hardware costs, elapsed-time bounds or a positive acceptance result.

The branch's single read-only CI workflow runs both commands and publishes their
logs as an artifact. It does not push or change old evidence. A verified receipt
will identify the exact run/commit, not merely a local success. NumPy 2.3.5 and
Python 3.13 are the intended versions; reports record the actual patch versions.
