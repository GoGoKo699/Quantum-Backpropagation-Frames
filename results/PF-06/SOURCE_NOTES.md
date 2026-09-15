# PF-06 primary-source and attribution notes

Opened on 2026-09-15. This is a bounded implementation-source check, not another
exhaustive novelty audit. The statistical optimum and sparse POVM are inherited
from PF-04/PF-05 with their original qualifications and are not rebranded here.

| ID | Primary source and exact location | Use and boundary |
|---|---|---|
| S1 | Mottonen, Vartiainen, Bergholm, Salomaa, arXiv:quant-ph/0407010v1, Section II, Fig. 2 and Eq. (3), printed page 2 | Cyclic-Gray uniformly controlled rotations and the Walsh angle transform. The rendered page was inspected. Two-control synthesis into four CNOTs plus four rotations is an established ingredient; our gate action is independently checked on every basis input. |
| S2 | Bartschi and Eidenbenz, arXiv:1904.07358v1, Sections 2-3 and Theorem 1 | Linear-size preparation of W/Dicke states is established. Our conditional marker-chain is an explicit specialization; the source's LNN property is NOT imported into our globally controlled readout. |
| S3 | Li et al., arXiv:2408.05406v1, Sections II.4 and III.1.1, Appendix A.4 | Reversed tests and grouping must be allowed. Three commuting groups and shorter suffixes are retained as baselines. Give the comparator the same controlled whole-objective access, not an unnecessary Pauli decomposition. |
| S4 | Huang, Kueng, Preskill, arXiv:2002.08953v2, Supplementary Sections 1B and 5B | Standard shadow first/third moments and linear aggregation. The local block alternative does not reconstruct a dense global snapshot. The bounds compared here are whole-vector sums, not an unmodified infinity-norm theorem. |
| S5 | Park, Teo, Jeong, arXiv:2311.14622v4, real equatorial measurement construction and synthesis discussion | Exact quadratic masks are an existing measurement baseline. Terminal synthesis and outcome relabeling must be allowed; direct dense CZ count is not an intrinsic cost. |
| S6 | Chen, Gilyen, de Wolf, arXiv:2405.14765v2, Section 3.3 | Projected/subnormalized tomography is already available under its stronger preparation access. This task consumes one supplied reference copy per execution and does not perform coherent iterative tomography. |

## Locators

S1 https://arxiv.org/pdf/quant-ph/0407010v1
S2 https://arxiv.org/html/1904.07358v1
S3 https://arxiv.org/html/2408.05406v1
S4 https://arxiv.org/html/2002.08953v2
S5 https://arxiv.org/html/2311.14622v4
S6 https://arxiv.org/html/2405.14765v2

## Attribution and decision

KNOWN INGREDIENTS: controlled reference interference, W/sparse state preparation,
Gray-code multiplexors, grouping, shadow-moment identities, aggregate-first
linear decoding. The compiled reference-row construction uses these ingredients.

IMPLEMENTED HERE: an explicit CNOT/R_y/X/H readout for the existing one-layer
six-rotation family, correct physical outcome classification and raw-coordinate
map, and an extension to nonzero one-layer angles by row-norm-balanced reference
amplitudes. At the equal spectrum it realizes the audited sparse attainer
without a tangent SVD, quantum routing oracle, or dense output map.

NOT CLAIMED: a new state-preparation primitive, fastest general POVM compiler,
novelty clearance, superiority over every shadow or reversed-test method, or
cheap implementation for overlapping circuits. The visible structure, not a
small abstract outcome count, supplies the linear construction.
