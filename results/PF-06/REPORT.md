# PF-06: an executable sparse optimal readout

Status: COMPLETE WITH FINDINGS, subject to the separately recorded remote run.
Baseline: 070b2728dbdc022d35b9bb9a36bf8938e8bd9408 (PF-05).
Branch: research/PF-06-sparse-compiler. Main is unchanged; no merge is performed.

## Result

The sparse measurement can be compiled on the existing disjoint one-layer
six-rotation family without a quantum tangent-basis transformation. The system's
computational addresses already distinguish the needed local response directions.
Prepare a known reference over those addresses on the reference-qubit-zero
branch, leave the unknown response branch untouched, apply H to the reference,
and measure all qubits in Z. An active outcome updates one direction count;
all other outcomes contribute zero without postselection.

For m two-qubit blocks there are n=2m system qubits and P=6m gate parameters.
At zero angles this implements PF-05's sparse attainer exactly on the occupied
reference-response family, with r=3m and lambda=2. Its worst-case trace variance
is 4P-8, the exact all-POVM optimum under the existing real, universally unbiased,
single-copy contract. The compiled sequence has 14m-5 CNOTs, 12m-4 single-qubit
full-angle R_y gates, two X gates and one H. It requires no additional work
qubits beyond the already present reference qubit.

This is a feasible exact logical implementation, not a generic optimal POVM
compiler or a claim that the elementary synthesis is minimal. W-state and
uniformly controlled rotation primitives are established and are credited.
The additional controls are explicitly decomposed and tested, not assumed free.

## Nonzero angles without a singular basis

The compiler calculates a 3-by-6 reversed-tangent matrix per block using only
four-dimensional prefix operations. Let k_x be an active row of the full
Jacobian-in-the-input-frame, d_x=||k_x||^2, s=sum_x d_x=P. Choose known reference
amplitudes c_x=sqrt(d_x/s), and return 2(-1)^b k_x/c_x on an active outcome.
The complete-gradient mean is exactly 2T^Tq for every real unit q.

The exact trace risk is 2s(1+||Pi q||^2)-4||T^Tq||^2. Thus the measurement stays
unbiased throughout the one-layer angle domain, and on full-row-rank points
its worst risk is max(2s,4s-4mu_min). No unequal-spectrum minimax claim follows.
Small nonzero-angle tests are correctness checks, not favorable-cost searches.

Preprocessing, gate compilation and final output mapping are O(P). Stored
local tangents contain 18m scalars. An outcome needs O(n) bit work to check its
support before one counter update. The full classical cost is O(Kn+P), not
O(K) after ignoring the physical outcome. No N-by-P table or dense Pr output
map is needed. The emitted output remains all P original coordinate entries.

## Matched comparison

The cheapest no-mask readout already has worst risk 4P at the flat point, with
no entangling measurement gates, local aggregate-first decoding and O(P) storage.
Its risk and the sparse risk differ by only 8 in worst-case variance. Both have
the same asymptotic total-work order under the common whole-vector prescription.
A growing asymptotic advantage is therefore NOT established by this compilation.

This does not assert pointwise equivalence: the all-X minus sparse trace-risk
difference is 2P(1-||Pi q||^2), which can be extensive. Using a smaller
instance-dependent budget must be justified without free knowledge of q.

RESOURCES.md derives the full symbolic crossover with preprocessing, readout,
streaming and final output separate. Its clearly limited CNOT-only specialization
requires common response cost C>(3m-1)(14m-5). It is not an end-to-end runtime
claim. The zero-angle U=I simplification is allowed on ALL sides. Exact full
masking receives the existing direct/pivot/greedy terminal optimizations;
grouped reversed tests receive three groups and shorter suffixes; block shadows
receive an aligned single partition and aggregate-first decoding. No new price
profiles or winning-method sweep are introduced.

## Boundary found

The one-layer support rule cannot be used unchanged after overlapping gates.
A fixed four-qubit, two-layer example has gradient norm 2.7639718921748453 for a
real response entirely outside the one-active-disjoint-block sector. The invalid
truncated decoder would return zero. This is an explicit scope counterexample,
not a no-go theorem against a different compact compiler for overlapping layers.

## Executed local checks

The two supplied PF-04/PF-05 archives and all 18 packet-manifest entries were
verified. Local execution used those files because github.com DNS resolution
failed; it was not a complete authenticated Git checkout. The circuit fixture
is SHA-256 checked and used only for independent small dense comparisons.
The new code imports no earlier POVM formula implementation.

Seed: 2026091591. Python 3.13.5, NumPy 2.3.5. All 17 diagnostic groups passed:
24 multiplexor matrix tests, four controlled exchanges, 20 existing-family
parameter points, 135 reference/response gate-Born checks and gradient/risk
checks, 20 POVM and aggregate-decoder cases, 75 finite-difference coordinates,
four flat-optimum checks, nine compiler-only sizes, one overlap counterexample,
four invalid-input probes and three finite-shot MSE experiments.

Largest gate-probability residual: 2.23e-15. Largest full-gradient mean residual:
4.22e-15. Largest trace-risk residual: 1.43e-13. Independent finite differences
agree within 2.07e-10. These are floating-point diagnostics, not interval proofs.

The compiler-only runs reach 512 system qubits, 1,536 parameters, 4,608 stored
tangent scalars, 3,579 CNOTs and 3,068 R_y gates. No 2^512 state was constructed;
full Born simulations stop at eight system qubits plus one reference. A
four-qubit finite-shot example has gradient norm 2sqrt(2); 5,000 repetitions at
each of K=64,256,1024 agree with the predicted 40/K MSE within reported sampling
error. This is not a hardware run or empirical uniform-confidence certificate.

Local diagnostics and source hashes are supplied in the delivery. Read-only
GitHub CI separately verifies the unchanged integration baseline, PF-04/PF-05
packets and this study. The actual executed commit, job and artifact are stated
only in REMOTE_VALIDATION.json after their successful completion is inspected.
Historical sources, tests, APIs and negative PF-02 results are not overwritten.

## Decision

Accept the compiler as a concrete implementation of the audited optimum on a
scalable existing family. Retain the nonzero-angle unbiased extension with its
explicit variance bound. Do not claim generic basis routing, anisotropic
optimality, novel state-preparation primitives, hardware superiority or a
strongest-method scaling separation. The remaining research question is compact
reference construction and decoding for overlapping tangent supports, not
another internal reproof or favorable parity sweep. No follow-on task is run.
