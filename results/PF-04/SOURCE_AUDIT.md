# PF-04 source comparison

Read on 2026-09-15 through primary arXiv pages. Versioned HTML was used; no PDF
figures/tables were needed. This is a bounded attribution/contract check, not
exhaustive novelty clearance. Generated HTML date banners were not used as
publication dates; arXiv identifiers and versions are the source locators.

| ID | Primary source and location | Relevance and boundary |
|---|---|---|
| S1 | Tsang, Albarelli, Datta, Quantum Semiparametric Estimation, arXiv:1906.09871v7, III.1 Eq. (13), VIII Theorem 8 Eq. (175), Theorem 9 Eq. (180) | The moment/error-operator inequality and distinctions concerning locally unbiased measurements are established. Its Helstrom/Holevo factor-two relation is NOT our finite one-copy globally unbiased minimax theorem. PF-04(A) is a direct application, not a new general estimation principle. |
| S2 | Huang, Kueng, Preskill, Predicting Many Properties of a Quantum System from Very Few Measurements, arXiv:2002.08953v2, Supplement on Clifford measurement/shadow norm (Proposition 1 and moment calculation) | Shared records and Clifford moment bounds supply eligible O(s)-variance comparators. Their classical reconstruction/observable costs must be counted. PF-04 does not replace those bounds or defeat them by comparing to an unoptimized decoder. |
| S3 | Park, Teo, Jeong, Resource-efficient shadow tomography using equatorial stabilizer measurements, arXiv:2311.14622v4, real-equatorial estimator and implementation sections | Random quadratic phases/all-X measurement and terminal linear processing are established ingredients. The inherited full-mask covariance is used as an upper bound and independently enumerated in PF-04. It is not claimed as new. |
| S4 | Li et al., Efficient Quantum Gradient and Higher-order Derivative Estimation via Generalized Hadamard Test, arXiv:2408.05406v1, reversed Hadamard test section | Swapping objective/generator roles and suffix reversal provide a strong allowed baseline. A common reversed state with local targets is a specialization/composition, not an independent novelty claim. |
| S5 | Fischer et al., Dual frame optimization for informationally complete quantum measurements, arXiv:2401.18071v2, II.4, III.1-III.2 | State-dependent dual optimization and tractable local processing are already studied. Our lower bound allows ensemble-level unbiasedness and does not exclude redundant decoders. Our proposed attaining POVM is not an optimized canonical shadow decoder. Efficient processing of an optimal dual is not automatic in this source either. |
| S6 | Markov and Shi, Simulating quantum computation by contracting tensor networks, arXiv:quant-ph/0511069v7, abstract/main contraction theorem | Tensor-network/treewidth methods show why a light-cone table-size bound cannot be called a universal classical-decoding lower bound. This source is used only for that boundary, not for a claim that every growing cone is easy or hard. |
| S7 | Lahiry and Nussbaum, Minimax estimation of low-rank quantum states and their linear functionals, arXiv:2111.03279v2, 1.1 and Section 6 | Quantum LAN and asymptotic minimax functional estimation are closely related but have a different model/loss/limit. Their theorem is not imported as a finite-copy, universal-unbiased vector-risk formula. |
| S8 | Bowles, Wierichs, Park, Backpropagation scaling in parameterised quantum circuits, arXiv:2306.14962v4, Definition 2.1 | Published elementwise-variance/time-memory criterion is distinct from whole-vector Euclidean accuracy. PF-04 keeps both conventions separate. |
| S9 | Global Minimax Readout of a Qubit Direction, arXiv:2608.16840v1, II Definition 1 and Theorem 1; Section VI | A current nearby result optimizes ordinary Fisher losses for a fixed-radius Bloch direction. Its stated scope explicitly distinguishes this from finite-sample estimator risk. It neither proves nor contradicts PF-04(B). No inference from the shared word 'minimax' is made. |

## Exact locators

- S1: https://arxiv.org/html/1906.09871v7
- S2: https://arxiv.org/html/2002.08953v2
- S3: https://arxiv.org/html/2311.14622v4
- S4: https://arxiv.org/html/2408.05406v1
- S5: https://arxiv.org/html/2401.18071v2
- S6: https://arxiv.org/abs/quant-ph/0511069v7
- S7: https://arxiv.org/html/2111.03279v2
- S8: https://arxiv.org/html/2306.14962v4
- S9: https://arxiv.org/html/2608.16840v1

## Search and novelty disposition

Queries included quantum universally unbiased one-copy minimax functionals,
real-amplitude POVM estimation, and off-diagonal element estimation. The checked
sources supply moment inequalities, tight-frame/character tools, optimal-dual
methods, and local/asymptotic minimax analysis. No checked theorem was identified
as an immediate statement of lambda*max(2r,4r-4) on the exact reference family with
a P-entry unbiased vector output. This is NOT a novelty certificate, and no
bibliometric claim is made. The elementary ingredients and short proof warrant
an especially careful equivalence check before describing it as a publication
contribution. PF-04's exact combination remains NOVELTY OPEN.

The local causal-cone algorithm is an independently implemented standard
cancellation/simulation technique. The L-entry table-output lower bound is an
ordinary output-size bound. Neither is presented as new complexity theory.
