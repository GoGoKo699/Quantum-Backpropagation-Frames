# Matched frame-gradient readout audit

Date: 2026-09-15. This is a local, independently written numerical reference, not a repository release or a hardware benchmark.

## Task and scope

Complete classical raw-coordinate gradient at a fixed parameter point, under exact phase-calibrated controlled-reflection access. The trainable circuit is the same 1D real nearest-neighbor family for all readouts. Logical parameter angles use exp(-i theta P), not the half-angle convention.

Compared methods:

1. Fixed all-X local Walsh records.
2. Reversed Hadamard tests grouped into three commuting pairs of generator types per physical layer, reversing only the needed suffix. The non-product two-qubit bases cost one CNOT per pair in the logical ledger.
3. Reversed tests with uniform local-Pauli shadows.
4. Reference-adapted rank-two observables with two staggered block-Clifford partitions.

The objective-dependent response vectors define validation reflection instances. These instances are classically easy. They do not establish computational quantum advantage.

## Run

Tested with Python 3.13.5 and NumPy 2.3.5. NumPy is the only non-standard-library dependency.

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python run_comparison.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python validate.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python cost_certificates.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python uniform_comparison.py
```

The full-state reference tests stop at small n. The exact local-Pauli ensemble is deliberately limited to n <= 5. Memory grows exponentially in this diagnostic implementation; this is not the scalable production cone compiler.

## Records

- comparison.json: 15 circuit parameter points and 60 reflection-response cases. Local-Pauli ensembles are fully enumerated for 48 cases, not the 12 n=6 cases.
- validation.json: independent grouped-test probabilities, block-shadow moments, and aggregate-first decoder identities. Block validation enumerates all 6, 60, and 1080 stabilizer states for one-, two-, and three-qubit blocks.
- cost_certificates.json: objective-independent sufficient second-moment bounds, a local dynamic-programming check, and logical CNOT coefficients. CNOT charges are not physical runtimes and exclude objective implementation cost, readout, single-qubit-gate pricing, routing and fault tolerance.
- uniform_comparison.json: an analytically derived objective-uniform sufficient variance comparison, with floating-point substitutions for the selected ansatz parameter points. These are not interval-arithmetic proof certificates.

For an unbiased sample mean, MSE = covariance_trace / number_of_records. For separately sampled gradient groups, the recorded A_R is the optimal continuous allocation coefficient (sum sqrt(group_variance))**2. It is not the covariance of one group shot. Finite integer shot counts require rounding. In hindsight comparisons the true moments are used; they are not silently supplied to a deployable learner.

The sufficient budget scripts use objective-independent bounds instead. Markov's inequality gives a common, deliberately conservative guarantee K >= R/(delta epsilon**2). No optimal tail-probability or hardware-cost claim is made.

No earlier spectral/coherence minimax theorem is audited by this package.

## Primary sources and attribution

- Li et al., arXiv:2408.05406v1: reversed Hadamard tests and measurement optimization.
- Huang, Kueng, Preskill, arXiv:2002.08953v2: classical-shadow inversion and Clifford moment identities.
- Huang, Kueng, Preskill, arXiv:2103.07510: derandomized Pauli measurement.
- Bowles, Wierichs, Park, arXiv:2306.14962v4: backpropagation definitions and structured measurements.

The common-state transformation, local decoder formulas, objective-uniform comparison criterion, and this code are calculations made for the current project. Their novelty is not asserted.
