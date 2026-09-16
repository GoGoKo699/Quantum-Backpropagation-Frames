# PF-05 primary-source and novelty audit

Audit date: 2026-09-15. Sources were opened through web access, not inferred from
repository descriptions. Exact versions below determine the comparisons. This
is a bounded primary-source audit, not a proof of absence of prior art.

## Question being compared

One fixed, globally unbiased real vector decoder of one copy of
Omega(q)=(a+b_q)/sqrt(2), uniformly over the full real unit sphere, minimizes the
worst-case trace covariance. Equal nonzero singular values of T give
lambda max{2r,4(r-1)}. Joint POVMs are unrestricted; implementation cost is not.

The distinctions between local and universal unbiasedness, pure and convexified
state models, and minimax and pointwise dominance are essential, not labels.

| Source | Location inspected | Actual connection and disposition |
|---|---|---|
| S1: Tsang, Albarelli and Datta, *Quantum Semiparametric Estimation*, arXiv:1906.09871v7 | Section III.1 Eq. (13); Section VIII, Theorems 8-9, especially Eq. (175) | Operator moment/error inequalities and local nuisance-parameter estimation are established. The general 2s lower bound uses this machinery directly. The source does not supply the audited flat-spectrum finite global minimax value at the inspected locators. |
| S2: Miyazaki and Matsumoto, *Imaginarity-free quantum multiparameter estimation*, arXiv:2010.15465v3 | Section 2.1, Eqs. (2)-(4), (7), (11); Section 3.3, Theorem 3, printed p. 9 | Real/antiunitary-invariant rank-one POVMs can attain the quantum Fisher matrix with a state-independent measurement. Local or asymptotically consistent estimation is not a single finite globally unbiased score. Claiming the first state-independent optimal measurement for real models would be wrong. |
| S3: Salmon, Strelchuk and Arvidsson-Shukur, *Only Classical Parameterised States have Optimal Measurements under Least Squares Loss*, arXiv:2205.14142v2 | Eq. (4), definition of measurement dominance; Theorem 3.2, printed pp. 2-3 | Optimality means dominating every competing measurement/estimator at every parameter value, with estimator choices quantified separately. That is stronger than minimizing the maximum of one prescribed trace loss. The nonexistence result does not contradict this minimax optimum. |
| S4: Fischer et al., *Dual frame optimization for informationally complete quantum measurements*, arXiv:2401.18071v2 | Sections II.4, III.1-III.2; Eqs. (9)-(10) | Dual scores for a fixed informationally complete measurement can be optimized, including state-dependent and empirical choices. Canonical shadow decoding is not generally optimal. The source is not an all-POVM minimax characterization of this restricted pure-state vector family. |
| S5: *Simultaneous Measurement of Multiple Incompatible Observables and Tradeoff in Multiparameter Quantum Estimation*, arXiv:2310.11925v2 | Results, approximation error Eq. (1), SDP Eq. (12); supplementary Sections S4 and S9 | Joint-measurement approximation bounds and tight pure-state constructions are relevant. Their state-dependent operator-approximation error is not the same as worst-response trace covariance of a universally unbiased vector. A known-state optimum cannot be supplied free to the unknown-response algorithm. |
| S6: Cha and Lee, *Spectral Minimax Direct Fidelity Estimation for Generic Target States*, arXiv:2605.01438v1 | Section II unbiasedness constraint; Section IV, Theorems 2-3, Eqs. (18)-(19) | Exact spectral minimax formulations already exist for a scalar projector, a prescribed measurement family, and all density operators. Our state family is not that convex set. The explicit axis-mixture countercheck shows why convexifying it changes the risk. This is not a general new spectral minimax principle. |
| S7: *Exponential quantum advantage in processing massive classical data*, arXiv:2604.07639v1 | Lemma F.16 and proof, Eqs. (F.64)-(F.68), printed pp. 127-128 | Reference interference plus reusable signed-overlap estimation is an established input. The stated shadow guarantee is not this exact one-copy vector-risk optimum. Its classical-query assumptions still have to be charged. |
| S8: Chen, Gilyen and de Wolf, *A Quantum Speed-Up for Approximating the Top Eigenvectors of a Matrix*, arXiv:2405.14765v2 | Section 3.3, Corollary 3.4 | Subnormalized tomography and coherent refinement already have precise guarantees. They do not remove the tangent-basis construction/output-map costs here, and their extra coherent oracle access differs from a supplied single copy. |

PDF pages containing the relevant formulas/theorems in S2 and S3 were also
inspected as rendered pages. The S7 proof page was inspected in rendered form.
No claim is based only on an uninspected title or on a secondary summary.

## Exact locators

- S1: https://arxiv.org/html/1906.09871v7
- S2: https://arxiv.org/pdf/2010.15465v3
- S3: https://arxiv.org/pdf/2205.14142v2
- S4: https://arxiv.org/html/2401.18071v2
- S5: https://arxiv.org/html/2310.11925v2
- S6: https://arxiv.org/html/2605.01438v1
- S7: https://arxiv.org/abs/2604.07639v1
- S8: https://arxiv.org/html/2405.14765v2

## Search scope and decision

Queries included combinations of globally/universally unbiased, single-copy,
minimax, real pure states, signed amplitudes, off-diagonal observables, and the
exact titles above, followed by reading the stated contracts. Irrelevant search
hits and abstract-only screens are not treated as theorem evidence.

ALREADY KNOWN: operator-moment machinery; real-model Fisher compatibility;
state-independent measurements in that Fisher sense; measurement dilation;
character orthogonality; generic dual optimization; signed-overlap interference.

KEEP AS AN INTERNALLY VERIFIED CANDIDATE: the exact finite universal-unbiased
flat-spectrum value, its two-ensemble lower-bound proof, and an attaining vector
measurement. The new sparse 2r+1-outcome construction makes the attainability
proof simpler than a sign-design construction but is not novelty-cleared.

OPEN: whether this exact specialization or an equivalent theorem appears in
other optimal-experiment-design/statistical-decision literature. None of the
inspected results, with their stated quantifiers, directly establishes the exact
formula. That bounded finding is not evidence of exhaustive novelty or PRL
readiness. Do not cite absence of a match as a proof of novelty.

No novel primitive, unrestricted measurement-depth advantage, or efficient
all-POVM compiler follows. The proof's simplicity makes a precise prior-art
statement more important, not less. Keep the mathematical result separate from
the still-unmet end-to-end advantage goal.
