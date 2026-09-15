# Reproduce PF-06

From a checkout containing the PF-05 baseline and the new packet:

```bash
python -m pip install -r requirements.txt
python tools/integration_check.py --output runs/integration-pf06
python results/PF-06/study.py --output runs/pf06-study
```

Both output paths must be new. The inherited integration gate requires a clean
full Git checkout. The new study needs only NumPy plus the immutable circuit
fixture, whose SHA-256 is checked before import. It imports no prior POVM code.
It writes only to its requested new output directory. The standalone ZIP includes
the fixture for the new study, not a fabricated full checkout.

compiler.py contains the actual elementary circuit generator and a small
statevector simulator. A generated example gate list is written as
example_plan.json. Sites are big-endian; site 0 is the reference qubit. `ry`
means exp(-i theta Y), so an API using conventional R_y(phi) needs phi=2 theta.
The original output parameter order is generator slot then block.

Seed 2026091591; fixed small grid: m=1..4, zero angles and two fixed draws each
from [-0.04,0.04] and [-0.4,0.4]. Scalable zero-angle compiler-only grid:
m=1,2,4,8,16,32,64,128,256. The maximum full diagnostic state has nine qubits
(including reference), not 513. The latter size only generates gate lists,
constant-size tangent blocks and the resource record.

Tests verify Gray decompositions, inactive-control identity, prepared amplitudes,
full Born probabilities, unbiased original gradients, second moments, POVM
completeness/positivity, aggregation, independent finite differences, exact
flat spectra, input errors and a deliberately invalid two-layer extension.
Finite-shot checks use multinomial sampling of exact probabilities and report
standard errors; they do not numerically certify a uniform confidence theorem.

The local run uses supplied archive files because container DNS for github.com
failed, not a full authenticated checkout. Local archive/packet identities and
actual environment are recorded. Read-only GitHub CI separately runs the full
inherited gate, PF-04/PF-05 diagnostics and PF-06. A remote receipt is added only
after inspecting the real completed job; it never retroactively claims a new
code version was executed. Old files and negative results are not overwritten.
