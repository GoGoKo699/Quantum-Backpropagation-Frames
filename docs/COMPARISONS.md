# Comparisons and limitations

[Home](../README.md) · [Theorem](THEORY.md) · [Circuits](COMPILERS.md) · [Evidence](EVIDENCE.md)

The exact theorem is a statistical limit under one carefully specified contract.
It does not establish a computational advantage over the strongest applicable
gradient method. This page separates those questions and explains what the
negative and supporting results teach.

## Which optimality is proved?

| Model | What is established here? |
|---|---|
| One supplied copy; one fixed universally unbiased decoder; all real unit responses | Exact worst-response trace risk for equal nonzero tangent sensitivities |
| Reference-preserving real phase/Walsh readout; conditional unbiasedness | Restricted variance identities and benchmark; a smaller measurement class |
| A decoder unbiased only near one response | Different local estimation problem; its Fisher bound need not equal the theorem |
| Biased estimation, collective measurements, extra coherent calls | Outside the exact theorem |
| A circuit producing a gradient state or one directional derivative | Different output from the complete classical coordinate vector |

For rank $r$ and common nonzero eigenvalue $\lambda$, the exact all-POVM risk is
$\lambda\max\{2r,4(r-1)\}$. The older restricted frame/Walsh benchmark is
$4r\lambda$. For $r\ge3$ their ratio is $r/(r-1)$ and tends to one. This compares
single-copy worst-response variance in the stated models. It is not a general
impossibility result for quantum backpropagation.

The existing zero-angle disjoint family has $\lambda=2$, $P=2r$, attaining risk
$4P-8$ and no-mask risk $4P$. A constant subtraction does not produce an
asymptotic runtime improvement. At one response an estimator may perform better
than its worst-case value; the response used inside a simulator cannot be
supplied to an unknown-response algorithm for free.

The local Fisher example in the [original audit](../results/PF-05/PROOF_AUDIT.md)
has rank three and $\lambda=1$. A locally unbiased score has risk four at its
chosen tangent-axis response but is biased elsewhere. The globally unbiased
minimax value is eight. These statements concern different quantifiers.

## The role of the reference and the state model

The coherent relative sign in the supplied reference-response state is an
access assumption. A bare unknown response state is a different input. The
measurement includes inactive records with score zero; dividing by the number
of active records generally introduces bias. If the response has squared weight $1/4$ in the tangent span, active
probability is $5/8$, so postselected normalization scales the mean by $8/5$.

Realness, purity, and unbiasedness are substantive restrictions. Complexifying
or mixing the response changes the risk problem. Allowing bias changes it too:
the zero estimator has worst-case squared error $4\lambda$, below the unbiased
minimax risk when $r\ge3$. Neither observation contradicts the theorem.

## Variance, confidence, and total work

For independent copies and sample averaging, a uniform variance bound $B$ gives
a **sufficient** whole-vector guarantee using
$K=\lceil B/(\delta\varepsilon^2)\rceil$. The one-copy minimax theorem does not
prove that this confidence budget is optimal. Collective or additional coherent
access has a different resource contract.

A complete comparison charges, for each method $j$,

```math
W_j=F_j+K_j(C+Q_j+D_j)+O_j.
```

Here $F_j$ is parameter-point preprocessing, $C$ common response preparation,
$Q_j$ additional quantum work per record, $D_j$ physical-bit and classical
processing per record, and $O_j$ final output assembly. Program storage or
recurring regeneration and precision costs belong in the applicable terms.
There are at least $P$ output writes when the full vector is materialized.

If two methods receive the same sufficient shot budget $K$, their shared
preparation cost cancels:

```math
W_S-W_F=(F_S-F_F)+(O_S-O_F)
+K\bigl[(Q_S+D_S)-(Q_F+D_F)\bigr].
```

Making the common objective arbitrarily expensive cannot alone reverse this
equal-budget ordering. Unequal justified shot budgets are a separate case.
Dense simulators, unpriced tangent-basis access, free source tables, and zero-cost
classical output cannot be used to manufacture a separation.

## Eligible strong baselines

- **No-mask Walsh:** permit compiled imbalance bounds, shared interval
  histograms/transforms, and aggregate-first contractions. A mask is unnecessary
  where the unmasked circuit suffices.
- **Quadratic masks:** allow direct, pivot, and greedy terminal circuits with
  mandatory affine outcome relabeling. The direct dense-CZ construction is an
  implementation, not a synthesis lower bound.
- **Parity masks:** retain both clean and measured-uncomputation variants and
  their charged mask sampling, compilation, and decoding.
- **Block Clifford shadows:** use valid interval covers and optimized local
  contractions. A displayed decoder's upper cost is not a lower bound on every
  shadow decoder.
- **Grouped suffix reversed tests:** permit commuting subgroups, unequal suffix
  costs, and charged shot allocation. Coordinate-by-coordinate parameter shift
  is insufficient as the sole comparator.
- **Sparse-state preparation and classical methods:** charge support/table
  construction, permutations, ancillas, and precision. Use an eligible classical
  adjoint baseline when the same model permits it. A method implementing the
  same preparation is not a distinct slower comparator.

These are the preserved comparison contracts, not claims that all optimized
implementations have been exhaustively benchmarked.

## What the negative comparison establishes

The fixed parity acceptance grid contains **144 scenarios and 4320 candidate
rows**. Full direct masking wins 96 scenarios, greedy full masking 24, and no
mask 24. Positive-round parity wins zero. The
[original report](../results/PF-02/REPORT.md),
[durable scenario table](../results/PF-02/remote_validation/34956367799-1/acceptance/scenarios.csv),
[candidate table](../results/PF-02/remote_validation/34956367799-1/acceptance/candidates.csv),
and [acceptance code](../results/PF-02/acceptance.py) define the evidence.

The lesson is that lowering a variance contribution can lose once compilation,
sampling, and decoding are priced. This result rejects a claimed win in that
model; it is not a universal impossibility proof. The grid, prices, sufficient
budgets, categorical outcomes, and numerical tolerances remain fixed.

## What the overlap comparison establishes

The fixed overlap analysis reuses 30 small parameter points and 10 compiler-only
cases. Row-reference worst-response variance is below no-mask variance at all
30 small points; it is below full-mask variance at 22 and equal within the
stated $10^{-10}$ relative and absolute comparison tolerance at eight. The largest comparator-to-
reference ratio is 1.5 in that finite grid. Compiler-only cases do not have a
new dense-state risk calculation.

At 256 qubits, the recorded depth-two reference circuit uses 6615 CNOTs and
6104 Ry rotations; at depth four it uses 96759 CNOTs and 96248 Ry rotations.
The direct full-mask comparator has 16320 expected CZs. Under the existing
incomplete quantum-operation prices (CNOT/CZ: 1; one-qubit gate: 0.1;
measurement: 1), the depth-two readout saves 9120 projected units per record,
while depth four costs 90038.4 more. These are **neither seconds nor complete
acceptance wins**. Classical processing, compilation, memory, final output,
and stronger mask synthesis still matter.

See [the fixed-data analysis](../results/PF-08/REPORT.md) and
[resource contract](../results/PF-07/RESOURCES.md). The interval construction
removes a compiler obstruction but retains exponential width dependence.
Coordinate-row support need not equal tangent span, so its $4\,\mathrm{tr}(G)$
bound does not make it a generic exact minimax implementation.

## Novelty and stopping point

The [primary-source map](../literature/README.md) credits operator-moment bounds,
real-state Fisher compatibility, dual-frame estimation, measurement dilation,
reference interference, and state-preparation ingredients. The finite universal-
unbiasedness theorem is presented with its exact contract. The bounded source
audits do not provide final novelty clearance; internal checks are not external
peer review.

The repository therefore establishes an exact statistical result and explicit
constructive realizations, with reproducible limitations. It does not establish
the original strongest-method end-to-end advantage goal. That qualification
remains part of the result rather than a reason to expand the frozen research.
