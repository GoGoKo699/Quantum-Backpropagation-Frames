# PF-05: independent audit of the exact readout optimum

Status: COMPLETE WITH FINDINGS; remote execution identified separately in
REMOTE_VALIDATION.json after inspection. Pinned PF-04 baseline:
`996d60ab06e872ec44a0ab447917f2e198b4241b`. Branch:
`audit/PF-05-optimal-readout`. Main is not changed or merged.

## Scientific decision

The exact equal-spectrum theorem survives independent rederivation, including
complex physical POVMs, continuous outcomes, parameter redundancy, and
unconditional universal unbiasedness of the full measurement. If the r nonzero
eigenvalues of T^T T all equal lambda, then

```math
\mathcal V(T)=\lambda\max\{2r,4(r-1)\}.
```

This is the fixed single-copy, real-response, universally unbiased trace-risk
contract, not arbitrary biased estimation, coherent query complexity, or exact
high-confidence sample complexity. PROOF_AUDIT.md gives the complete argument.
No valid-domain mathematical defect was found in the audited statement.

## A simpler attaining measurement

The original character POVM is sufficient but unnecessary. A sparse measurement
has 2r active outcomes (direction index and sign) plus one complementary outcome.
It splits the reference amplitude evenly among direction channels and
interferes each with the corresponding response component. Active outcomes
return one signed singular-direction contribution; all records still contribute
to a complete P-vector after the final output map. Its exact trace risk equals
the original construction's risk for every real response.

This reduces the sufficient outcome count from the earlier at-most-4r+1 bound
to 2r+1. It does not prove that 2r+1 is minimal. It does not uniformly improve
all covariance entries: the two attaining constructions can have different
covariance matrices with the same trace.

An explicit Naimark isometry is supplied and checked. Its algebraic existence
is not an efficient compiled circuit for arbitrary tangent bases. Conditional
on basis access, signed channel counts require O(K) updates and the output map
is applied once. A generic dense P-by-r map costs O(Pr), and basis computation,
quantum synthesis and P output writes remain charged. No free tangent basis,
general fast compiler or new end-to-end advantage is asserted.

## The important literature distinction

Real pure-state models can already admit state-independent measurements
attaining quantum Fisher information (Miyazaki-Matsumoto, Theorem 3). That is not
one globally unbiased finite-copy score. In this model the local bound at a
tangent axis is 2(r-1)lambda; the global universal-unbiased minimax value for
r>=3 is 4(r-1)lambda. Independent code constructs a locally unbiased score with
the smaller local error and explicitly detects its bias elsewhere.

Likewise, a theorem ruling out pointwise-dominant measurements on nonclassical
models does not rule out a minimax optimum for a fixed loss. Exact scalar
minimax formulations on convex mixed-state domains also have different
quantifiers. SOURCE_AUDIT.md records eight primary sources and theorem locators.

The exact specialization was not found in the inspected source statements.
Novelty remains OPEN. The general lower-bound machinery and measurement
principles are established. Neither theorem validity nor a bounded source
comparison establishes PRL readiness or the project's advantage requirement.

## Tested failure modes of overgeneralization

Renormalizing by the active probability changes the target. Imaginary responses
and convex mixtures can have trace risk 4r lambda, greater than the pure-real
optimum. Adding unbiased noise in a null output direction increases risk and
orthogonal projection removes it. Permitting bias lets zero output beat the
one-copy universally unbiased optimum at sufficiently loose accuracy.

These are boundaries of the model, not counterexamples to its theorem. The
same-family zero-angle spectrum and fixed small-angle perturbation bound were
also rechecked without importing the previous formula functions.

## Fresh local execution

Seed 2026091581; Python 3.13.5; NumPy 2.3.5. audit.py imports no PF-04 formulas.
The uploaded PF-04 archive and nine manifest entries were verified before use.

| New diagnostic group | Cases |
|---|---:|
| Sparse attaining POVM, explicit Born means and risks | 384 |
| Sparse positivity, completeness and operator identities | 48 |
| Independently reconstructed original character comparison | 384 |
| Nuisance sector, wrong postselection and null outputs | 16 |
| Random redundant POVMs and both lower inequalities | 16 |
| Complex-effect realification | 16 |
| Explicit dilation isometries | 32 |
| Deliberate model-boundary comparisons | 9 |
| Locally unbiased Fisher contrast | 3 |
| Same-family small-angle stability | 40 |

All ten groups passed. The largest fresh risk residual was 9.95e-14; the largest
operator-contract residual was 1.34e-15. These are floating-point checks, not
interval certificates or optimization over all POVMs. The random POVM tests
are adversarial diagnostics, not proof by sampling.

The remote gate reruns inherited integration checks, original PF-04 diagnostics
and this independent audit. Its source-specific receipt and artifact identify
what actually executed. Local files came from the supplied archive rather than
a full Git checkout. No old timestamps, results or archived code were changed.

## Outcome

Retain the exact theorem and add the sparse attainer as an audit result. Do not
promote it to a fastest-gradient claim. No new price sweep, arbitrary-spectrum
study, ansatz, manuscript, license, release, or merge was performed.

The next justified scientific test is compiler feasibility for this sparse
measurement on the existing scalable circuit family, with the tangent-basis
routing and output map explicitly charged and optimized known readouts allowed.
This is a recommendation, not a dispatched task. Another repetition of the same
internal proof audit or favorable-parity search is not the next priority.
