# Implementation and input contracts

[Home](../README.md) · [Tutorial](TUTORIAL.md) · [Theory](THEORY.md) ·
[Circuits](COMPILERS.md) · [Reproduce](REPRODUCIBILITY.md)

The maintained interface is the `qbp_frames` Python package. Its compilers emit
logical gates and decode measured bit records. They do not connect to hardware
or prepare the supplied unknown response. Dense statevector helpers check small
examples; they are not part of the scalable compilation path.

## Install and run

From a clean checkout, use Python 3.10 or newer and a virtual environment:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install .
python examples/flat_readout.py
python examples/compile_large.py
```

NumPy is the only runtime dependency. The package uses Python's integer
`bit_count`, requiring Python 3.10 or newer; this is a language requirement,
not a claim that every Python/NumPy combination has been tested. The exact
validation environments and development dependencies are documented in
[reproduction](REPRODUCIBILITY.md). Build metadata uses `0+unreleased` solely
to make a local installation identifiable; there is no versioned release or
registry publication.

The first example prints the full target `[0, 1, 0, 0, 0, 1]`, zero-score
probability `0.375`, trace risk `13.0` for the chosen response, and minimax risk
`16.0` versus the no-mask worst-case value `24`. It also decodes a fixed possible
16-record histogram. That illustrative sample gives approximately
`[0, 1.515544456623, 0.216506350946, 0.216506350946, 0, 1.515544456623]`.
The sample is not its expectation and is not a new simulation data set.

The larger example recompiles an already validated flat disjoint case:
128 system qubits, 384 original coordinates, 192 tangent directions, 891 CNOTs,
764 full-angle rotations, two X gates, and one H gate. It stores 1,658 gate
records and returns a full 384-entry decoder output. The respective worst-case
trace risks are 1,528 and 1,536. No global state or Born probabilities are
allocated; this is a compiler demonstration, not a 128-qubit simulation or a
runtime advantage.

## Supported entry points

| Module | Interface and purpose |
|---|---|
| `qbp_frames.disjoint` | `compile_plan(angles)` for one disjoint six-generator layer; plan methods `counts`, `classify`, `finish`, `exact_risk_bound` |
| `qbp_frames.local` | `parameter_count(n, depth)`, `compile_local(n, depth, angles)`, `reference_plan(local)` for the existing staggered line family |
| `qbp_frames.intervals` | `IntervalReference.from_tables(n, intervals, tables)`; methods `gates`, `ledger`, `row`, `score`, `add_record`, `finish` |
| `qbp_frames.parity` | Validated Walsh moments, covariance and risk functions, phase masks, local scores, and `rounds_for_relative_bound` |
| `qbp_frames.readout` | `direct`, `pivot`, `greedy`, `portfolio`, and `quadratic_character` for terminal quadratic-phase measurements |

Construct plans with the listed factories. Direct construction or mutation of
plan fields bypasses their validation and is unsupported. Names beginning with
an underscore, including the package-local parity reference kernel, are
implementation details. The research packets retain their original programs
as evidence, not as an alternative supported import path.

### One disjoint layer

```python
import numpy as np
from qbp_frames import disjoint

plan = disjoint.compile_plan(np.zeros((2, 6)))
assert plan.n == 4 and plan.P == 12

# Each physical record contains a reference bit b and ALL n system bits.
signed_counts = np.zeros((plan.blocks, 3))
records = [(0, 1), (1, 4), (0, 0)]
for b, system_outcome in records:
    channel = plan.classify(system_outcome)
    if channel is not None:
        signed_counts[channel] += (-1)**b
estimate = plan.finish(signed_counts, shots=len(records))
assert estimate.shape == (12,)
```

The six generator slots are `YI, IY, YX, XY, YZ, ZY`. Input angles have shape
`(B, 6)` for B disjoint neighboring pairs. The full original parameter vector
and returned gradient use **slot first, block second** ordering:
`angles.T.reshape(-1)`. Entry `j*B + b` differentiates `angles[b, j]`.
The input matrix is a convenient block representation; it does not redefine
coordinates. A block's three active system patterns are `01`, `10`, `11`.
An outcome with zero or multiple active blocks receives zero score.

`finish` accepts a `(B, 3)` signed histogram and a positive integer shot count.
Counts must be finite integers with total absolute count at most `shots`;
`shots` must be at most `2**53`, the exact-integer range used by the binary64
accumulator. Zero-score records still contribute to `shots`. This check cannot
reconstruct omitted records: the caller must supply the actual total.

At zero angles, the nonzero eigenvalues are all 2, rank is `3*B`, and the exact
minimax trace risk is `4*P - 8`. Away from that point, `exact_risk_bound()` gives
the risk bound of this particular row measurement using numerical eigenvalues.
It is not an arbitrary-spectrum minimax solver. Applying the disjoint classifier
to an overlapping circuit can miss nonzero derivatives; use interval tables.

### Overlapping intervals and their source tables

An interval table is one reversed tangent column restricted to a contiguous
set of system sites. Amplitudes outside that interval are fixed to zero bits.
Tables retain their signs. They are charged classical input: constructing them
is part of the algorithm's cost, not a free gradient or an eigenbasis oracle.

For the existing staggered line family, the maintained source compiler supplies
them directly:

```python
import numpy as np
from qbp_frames import local

n, depth = 4, 2
angles = np.linspace(-0.4, 0.5, local.parameter_count(n, depth))
source = local.compile_local(n, depth, angles)
plan, reference_roundoff = local.reference_plan(source)
accumulator = np.zeros(plan.P)
plan.add_record(accumulator, 0, "0010")
plan.add_record(accumulator, 1, "0000")  # Counts in the denominator.
estimate = plan.finish(accumulator, shots=2)
ledger = plan.ledger()
# Iterate plan.gates() to emit gates without retaining the full gate list.
```

Coordinates are ordered by layer, then the six generator slots above, then
ascending left endpoint. Even layers use pairs `(0,1), (2,3), ...`; odd layers
use `(1,2), (3,4), ...`. `compile_local` requires explicit angles and records
local predecessor visits and amplitude-kernel entries. It does not silently
choose random parameters. Each local vector still has exponential size in its
interval width.

`reference_plan` is for this compiler's output. Analytically, each table has
zero reference amplitude. The helper checks that the maximum computed residual
is at most `1e-10`, reports that residual, and sets only those entries to exact
zero. It does not modify the returned source tables. Direct user-supplied
`IntervalReference.from_tables` inputs must already have an **exact** zero first
entry; they are never silently projected.

For explicit tables, `n` is a positive integer. `intervals` and `tables` must
have the same nonzero length P. Every interval is nonempty, contiguous,
increasing, and inside sites `0` through `n-1`; a width-k table has length
`2**k`. Zero tangent columns are allowed, but the total squared tangent mass
must be positive. Duplicate intervals and overlapping intervals are allowed.
Their nonzero computational rows need not span exactly the tangent subspace,
so this readout is not a generic exact minimax construction.

`score(b, bits)` returns the original coordinate indices and their signed
values. `b` is exactly 0 or 1, and `bits` is a string of exactly n binary digits.
`add_record` adds those sparse values to a writable NumPy `float64` P-vector
initialized to zero. It checks finiteness on touched coordinates and validates
each update before mutation; it never scans or constructs a P-vector per record.
`finish` checks the entire accumulator for finiteness once and divides by all
records, including inactive ones. It checks shape and a positive integer
`shots <= 2**53`; the caller remains responsible for the histogram's history.
The physical bit scan and final P-entry output both count toward the work.

## Bit order and rotation angles

The disjoint, local, and interval modules number **physical sites from the
left** of the printed bit string: site 0 is most significant. A readout gate
program places the reference qubit at physical site 0, followed by the n system
qubits. System intervals themselves are numbered from 0 before that reference
site is added. Local table addresses use the usual binary order, with the
leftmost interval site most significant.

The internal uniformly controlled rotation decomposition indexes its angle
table with the **first control least significant**. This is a local truth-table
convention, not a reversal of system-site numbering. The emitted gate tuples
already account for the conversion.

Every emitted `('ry', site, theta)` means

```math
R(\theta)=\begin{pmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{pmatrix}.
```

A conventional SDK `Ry(phi) = exp(-i phi Y/2)` therefore receives
`phi = 2*theta`. The original circuit coordinates also use full-angle Pauli
rotations `exp(-i theta Q)`. Changing to half angles without transforming the
derivatives changes the target and all risk constants.

The parity and terminal-mask modules instead use integer masks with **bit 0
least significant**. A parity pair is `(a, b)` with masks in `[0, 2**n)`.
Quadratic mask bits follow edges `(0,1), (0,2), ...` in lexicographic order.
Do not interchange these masks with physical site numbers without conversion.

## Parity and terminal-mask contracts

`parity` accepts a real finite tangent matrix T with shape `(2**n, P)`, P positive,
reference-row norm at most `1e-10`, and a matching real unit response q whose
norm differs from 1 by at most `1e-10`. It performs no normalization. Phase
vectors must contain exact signs ±1 and fix address zero to +1. Rounds, masks,
and outcomes must be genuine integers in range; booleans and coerced floats
are rejected. A zero tangent matrix is allowed by the parity moment functions.

`rounds_for_relative_bound(beta, eta)` requires finite real `beta >= 1` and
`eta > 0`. It uses exact integer arithmetic on the supplied binary64 values to
find the smallest sufficient round count. This preserves the repaired behavior
at power-of-four thresholds, including adjacent representable inputs.

The terminal compiler's `plan.outcome(y)` applies the affine output correction
for its CNOT change of basis and phase character. **Always decode that corrected
outcome.** The plan implements a terminal measurement, not a coherent substitute
for the original diagonal phase oracle. `portfolio` returns the direct,
pivot, and greedy constructions; it does not certify globally optimal synthesis.
The original terminal relabeling regression remains unchanged.

## Numerical and resource limits

All supported real arrays reject complex dtypes even when the imaginary part
is zero, as well as object, string, boolean, and nonfinite inputs. Arrays are
copied into binary64. Unsupported magnitudes, squared-amplitude underflow in
interval tables, and nonfinite numerical results are errors rather than
successful certificates. Integer counts reject booleans and nonintegral values.
The API uses `ValueError` for invalid supported inputs. Resource exhaustion from
an impractically large dense allocation is not translated into an input error.

These are ideal real logical circuits with binary64 diagnostic arithmetic.
Floating-point equality checks are not exact-real proofs. State preparation
uses arbitrary-angle rotations; no hardware calibration, routing, noise, or
fault-tolerant gate synthesis is included. Small tangent-row probabilities may
require greater rotation and arithmetic precision. The logical resource bounds
must be combined with the precision qualifications in [the circuit analysis](COMPILERS.md).

For a disjoint layer, block tables and the emitted program scale linearly in n.
The plan retains its gate list, so those records count as storage. For intervals,
let L be the number of source-table entries, W the sum of interval lengths,
w the largest interval width, and ν the maximum number of intervals containing
one site. After charging source-table construction, reference preprocessing
costs `O(L + W + n w 2**w)` and working memory costs `O(L + W + n + 2**w)`.
Retaining emitted gates adds `O(n 2**w)` program records. Streaming avoids that
retained list during compilation; repeated regeneration and deployed program
storage are still costs. Readout uses `O(n 2**w)` logical gates, reads n+1
physical bits, updates at most ν coordinates per record, and ultimately writes
all P outputs.

The disjoint helpers `dense_tangents`, `dense_scores`, `reference_vector`,
`risk_from_coordinates`, `apply_gate`, and `apply_circuit` allocate global
arrays and are **small-system diagnostics only**. Parity moment and covariance
routines also materialize exponentially large arrays. Neither belongs in the
compiler-only large example.

## Preservation and regression coverage

Historical source programs remain byte-for-byte at their original locations.
The maintained copies are mapped in the [evidence index](EVIDENCE.md). The
package-local parity numerical kernel is byte-identical to its original;
the validated wrapper continues to guard it. Disjoint, interval, and source-table
migrations have direct output, gate-list, score, and source-table equivalence
checks against the originals in [test_supported.py](../tests/test_supported.py).
Stricter maintained validation changes no accepted scientific model. The
original round-threshold and terminal-outcome tests remain in place.
