# Maintained numerical interface

Use `from qbp_frames import parity` for new numerical work. The functions in
`research/parity_frames/core.py` remain an immutable historical source, with the
four PF-01 input defects intentionally reproducible. They are not the maintained
input interface. The adapter checks the source hash before importing it.

The adapter rejects complex dtypes (even zero imaginary parts), NaN/infinity,
non-numeric/object/string arrays, invalid dimensions, zero-column tangents,
nonunit responses, nonzero reference rows, invalid signs, fractional/Boolean
counts, and out-of-range masks or outcomes. Validation precedes float conversion.
It neither normalizes nor projects inputs. Numerical reference-row and response
norm checks retain the source's `1e-10` tolerance. Phases must be exact real +/-1
values fixing address zero. Unsafe overflow raises an error instead of returning
nonfinite output. Root dimensions require at least one system qubit; local score
tables require at least two entries. Dense functions are diagnostic, not a
large-system implementation.

```python
import numpy as np
from qbp_frames import parity
T = np.array([[0.0], [1.0]])
q = np.array([0.0, 1.0])
mean, covariance, probabilities, records = parity.measurement_moments(T, q)
```

`readout.py` returns direct, pivot-elimination and greedy exact terminal readout
plans. A plan's `outcome(y)` correction is mandatory. An optimized plan is not a
coherent substitute for the diagonal unitary: it also permutes system basis
addresses. Uniformly sampling the original quadratic mask, then choosing a
compiler, preserves the original measurement ensemble after relabeling.

`quadratic_character` uses Gray traversal for local accumulator updates; it does
not evaluate a quadratic polynomial separately at every basis string. It should
be applied to small tangent-support intervals, not the full system when n is
large. Bit zero is the least significant address bit.

No globally optimal synthesis, noise guarantee, license change, new estimator,
or scientific novelty is asserted by this interface. See results/PF-02/REPORT.md.
