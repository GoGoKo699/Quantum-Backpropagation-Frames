# Maintained numerical interface

Use `from qbp_frames import parity` for new numerical work. The immutable
research/parity_frames/core.py retains its original four PF-01 input defects;
it is not the supported input interface. The adapter pins its SHA-256.

The adapter rejects complex dtypes (including zero imaginary parts), nonfinite
values, object/string/bool arrays, invalid dimensions, zero-column tangents,
invalid phases, coerced integer counts, and out-of-range masks/outcomes before
numeric evaluation. It does not normalize or project invalid inputs. Dense
functions remain diagnostic rather than large-system implementations.

Reference-row and unit-response checks use the inherited 1e-10 numerical
tolerance. This is a floating-point acceptance tolerance, not a theorem that
relaxes exact realness or normalization. Phases are exact real +/-1 values and
must fix address zero. Arrays are converted to float64 after validation.

PF-03 makes scalar conversion failures consistently raise ValueError and selects
the smallest nonnegative k satisfying beta-1 <= 2*eta*4**k by exact integer-ratio
arithmetic on the validated binary64 scalars. This avoids a one-round error at
logarithm thresholds and handles subnormal eta without overflow. It does not
certify that a beta estimated numerically is an upper bound on true imbalance.

```python
import numpy as np
from qbp_frames import parity
T = np.array([[0.0], [1.0]])
q = np.array([0.0, 1.0])
mean, covariance, probabilities, records = parity.measurement_moments(T, q)
```

`readout.py` supplies direct, pivot and greedy terminal measurement plans.
Apply `plan.outcome(y)` to the measured bit string. The optimized circuit can
permute basis addresses and is not a drop-in coherent diagonal unitary. Sampling
the original mask uniformly and then choosing a compiler preserves its measured
ensemble after that correction. The heuristics are not globally optimal.

`quadratic_character` evaluates local characters by Gray traversal. Use it on
small tangent-support intervals, not a large full register. Bit zero is the
least significant address bit. Integration leaves these compilers unchanged.

PF-02's 144 declared scenarios produced zero parity winners; the interface
repair does not reverse that result. See results/PF-02/REPORT.md and the PF-03
integration report for the implementation and evidence boundaries.
