# PF-07 bounded primary-source comparison

Checked 2026-09-16. This is not exhaustive novelty clearance. Our sources are
research papers, not search snippets treated as proofs. arXiv HTML failures are
recorded below; PDF pages were used where available. No external code is copied.

| ID | Exact source inspected | Use, closest comparison, and boundary |
|---|---|---|
| S1 | Mottönen et al., quant-ph/0407010v1, Sec. II, Fig. 2, Eq. (3), printed p.2; Sec. III | Complete cyclic-Gray controlled-rotation synthesis and Walsh angle transform. PDF rendered p.2 inspected. Established ingredient, not a PF-07 primitive. Our implementation uses a fast Walsh algorithm and retains both marker and reference controls. |
| S2 | Grover and Rudolph, quant-ph/0208112, abstract; Ramacciotti et al. 2310.19309v1 Secs. 3-4, Algorithms 3-5 | Conditional-mass amplitude preparation and sparse-state preparation are established. The latter's PDF pp.5 and 8 were inspected. Its supplied arbitrary address list and generic permutation step differ from compiling one local first-site sector at a time. Do not assert superiority over an optimized implementation on our special support. |
| S3 | Ramacciotti et al., 2604.24973v1, Sec. II-A, Sec. III-A/B/C | Exact stripping of controls on unreachable branches and approximate merging are explicit prior art. Our right-to-left induction is a structural control-removal justification; it is not the first exploitation of unreachable branches. The source also prices classical optimization. The unknown response branch remains protected by the reference control in our circuit. |
| S4 | Li and Luo, 2406.16142v2, Theorems 1-2, 4, 6-7 and Sec. 1.2 | General sparse-state circuit bounds already improve on O(nM), including an ancilla-free O(nM/log n+n) upper bound. Their worst-case lower bounds vary over arbitrary support locations; our fixed bounded-window envelope is a special family. Neither their lower bound nor our elementary dimension count proves that our readout beats every state-preparation compiler. |
| S5 | Li et al., 2408.05406v1, Sec. III.1.1 and measurement grouping discussion | Reversed tests may group generators and use shorter suffixes. Give them the same controlled whole-objective interface. No parameter-shift-only advantage comparison is accepted. |
| S6 | Huang, Kueng, Preskill, 2002.08953v2, supplementary moment/linear-estimator analysis | Global and block shadows already attain O(s) trace-risk prescriptions in the relevant reference observables. Aggregation and optimized decoding must be permitted. The infinity-norm sample theorem is not silently substituted for the full-vector contract. |
| S7 | Rupprecht and Wölk, 2601.09388v2 (PDF abstract and introduction); Quantum 10, 2208 journal record | Recent sparse-state isometry and Toffoli-count improvements exist. Toffoli/T counts, ancilla budgets and approximate dense preparation are not the same cost model as our exact Ry/CNOT count. This task does not claim a fault-tolerant advantage. HTML v2 was unavailable; PDF and official journal page were used. |
| S8 | Luo and Li, 2608.00414v1, Theorem 1 | Sublinear T-count sparse preparation is available at constant error with a stated ancillary-space budget. It does not contradict an exact continuous-parameter counting observation. It precludes treating our total logical gate count as a T-count lower bound. |

## Locators

S1 https://arxiv.org/pdf/quant-ph/0407010
S2 https://arxiv.org/abs/quant-ph/0208112 and https://arxiv.org/pdf/2310.19309v1
S3 https://arxiv.org/html/2604.24973v1
S4 https://arxiv.org/html/2406.16142v2
S5 https://arxiv.org/html/2408.05406v1
S6 https://arxiv.org/html/2002.08953v2
S7 https://arxiv.org/pdf/2601.09388 and https://quantum-journal.org/papers/q-2026-09-10-2208/
S8 https://arxiv.org/html/2608.00414v1

## What is established here versus inherited

INHERITED: the reference-response interface; row-norm scores and their risk
identity from PF-06; the 2s lower bound and flat-spectrum all-POVM optimum from
PF-04/PF-05; constant-size gate simulation and the causal local-table compiler.

IMPLEMENTED HERE: unique first-site aggregation of overlapping rows, descending
conditional suffix preparation, an elementary fast-UCR compiler, and local
sparse original-coordinate decoding. Explicit bounds include table generation,
program storage or regeneration, physical bit scanning, and final output.

STANDARD CONSEQUENCE: the generic O(M_w) preparation size for the bounded-window
positive state class has a matching continuous-parameter dimension lower bound.
This does not establish quantum readout optimality or a new lower-bound method.

OPEN: novelty of the exact interval compiler/gradient application combination.
No claim of a first general sparse preparation method, globally optimal synthesis,
state tomography speedup, hardware advantage, or strongest-baseline separation.
The bounded search did not locate a source with our identical complete compiler,
but absence of a match is not novelty evidence.
