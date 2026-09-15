# PF-02: input repair and optimized-readout acceptance test

**Status: COMPLETE WITH FINDINGS.**

Parent: `79423bc1e68b16ec8f0e8a45969240b1aa1c1c9f` (PF-01).
Branch: `repair/PF-02`. Main is not modified. See START.md for the bounded task.

## Result

Accept the maintained input interface and the two exact terminal-readout
compilers. The final priced test does not select a positive-round parity method
in any of its 144 scenarios. Do not promote this negative finite comparison into
a general impossibility or a proof of optimality for another method.

## 1. Input repair

The maintained interface is `qbp_frames/parity.py`. It checks real numeric dtype,
finite values, shapes, reference orthogonality, normalization, sign phases,
integer counts, masks, and outcomes before calling the preserved calculations.
Complex dtypes are rejected even when their imaginary part is zero. Unsupported
values are not silently projected, normalized or coerced. Numeric overflow
raises an error. The historical source is SHA-256 pinned and unchanged.

PF-01's NaN-response, NaN-tangent, NaN-phase and complex-response probes are now
rejected without warnings by the maintained API. Additional regression tests
cover infinity, strings, object arrays, bool/fractional rounds, invalid masks,
invalid outcomes and extreme finite scalar tolerances. Valid-domain outputs
match the archived implementation exactly in the executed tests.

This is an interface repair, not a replacement theorem. Direct imports of the
immutable historical core still reproduce its known defects; downstream work
must use the maintained interface. See qbp_frames/README.md.

## 2. Optimized exact full-mask comparison

The competing compiler is no longer forced to implement one CZ per graph edge.
`qbp_frames/readout.py` supplies:

- Direct CZ realization.
- Quadratic-form pivot elimination into CNOTs and disjoint CZs.
- Greedy CNOT congruence reduction, accepting a move only when the saved CZ
  count exceeds the additional CNOT count.
- A portfolio that pays to construct all three candidates before selecting one.

All optimized plans carry an affine classical outcome map. The circuit's
unmeasured unitary is not generally the original diagonal gate. The final
measurement, after relabeling, is exactly the same. PROOF_AND_SOURCES.md gives
the contract. This is known terminal-linear-processing structure, not a new
Clifford-synthesis primitive [S1, S2]. The implemented heuristics are not claimed
to be globally optimal or to implement every published synthesis algorithm.

Exhaustive phase checks cover every quadratic mask and basis input for one
through five qubits: 67,732 comparisons across the two optimized compilers.
Independent folded Born-distribution checks cover 120 compiler cases on arbitrary
complex reference/system inputs. These test the compiler contract; they do not
extend the parity covariance theorem to complex responses. Terminal measured
parity is checked in 32 complete-distribution cases.

At five qubits, best-of-three gate-only selection reduces the average entangling
count from 5 to 4.38671875, with strict improvement for 476 of 1,024 masks. This
number omits the synthesis cost and is NOT the acceptance metric.

## 3. One priced output contract

Every candidate returns the complete raw gradient at epsilon=0.1 and delta=0.1.
The unchanged unbiased independent sample mean uses the common sufficient
prescription K=ceil(B/(delta*epsilon^2)). This is a conservative Markov bound,
not optimal confidence dependence or measured empirical shot complexity.

The 12 parameter points use the existing six-Pauli-rotation nearest-neighbor
family, n=2..5 and one to three block layers. Seed: 2026091566. Their actual
angles, local widths, tangent norms and imbalance values are stored in the
machine-readable summary. No new ansatz or hard objective is claimed.

Compare 30 candidate prescriptions at each point: no mask; direct/pivot/greedy/
portfolio full masking; clean and measured parity for k=1..4; all four compiler
policies applied to the same finite-round parity ensemble; and grouped suffix
reversed tests with cost-aware shot allocation and integer rounding.

Compiler cost expectations are summed over ALL original quadratic masks, not
estimated from a few favorable examples. Uniform original-mask sampling is
preserved after optimization. Finite-round mask distributions use the preserved
exact XOR-convolution routine on valid small integer inputs. The enumerated bank
is a diagnostic convenience, not free learner preprocessing: each synthesis is
priced on every sampled mask.

Classical processing includes local-tangent preprocessing, imbalance evaluation
where needed, mask sampling and synthesis, affine relabeling, record processing,
final contraction and output. Full masks use a Gray-traversal local character
kernel, not a separately evaluated quadratic polynomial at every address.
Parity may use shifted Walsh lookups or aggregate-first decoding. Lookup cost
includes address generation, table reads, multiplication and addition, not just
one nominal lookup per term. All methods may reuse shared local supports.

Grouped reversed tests use three commuting generator-pair groups per physical
layer, the shorter inverse suffix, and optimized sufficient shot allocation.
Their preprocessing does not pay for tangent tables they do not need [S3].

The cost unit is declared normalized serialized work, not seconds. Three
positive price profiles emphasize quantum gates, classical kernel work or
measurement/reset cost. The controlled-objective cost takes 0, 10, 1000 and
1e6 units; zero is an intentional stress case. The parameter and output memory,
accumulators and work qubits are listed. Memory is a one-time resident-word
charge, not memory-time or a hardware rent estimate. The model omits routing,
noise, error correction, parallel execution, CPU/interpreter overhead and
finite-precision synthesis. See acceptance.py and generated summary.json.

## 4. Final acceptance outcome

| Minimum-work prescription | Scenarios won |
|---|---:|
| Exact full mask, direct CZ realization | 96 |
| Exact full mask, greedy terminal compiler | 24 |
| No mask | 24 |
| Any positive-round parity prescription | 0 |

144 scenarios = 12 parameter points x 3 price profiles x 4 objective prices.
There are 4,320 candidate cost rows, not 4,320 quantum experiments. The best
parity/best-nonparity work ratio ranges from about 1.00031 to 2.86271 in this
restricted grid. No statistical significance is inferred from those ratios.

Earlier draft ledgers priced shifted-table terms too cheaply and did not use
the Gray kernel for full masks. Their apparent favorable parity cases are not
accepted results. The final source and results include both corrections. No
historical scientific packet or PF-01 record was altered to obtain this outcome.

This compares specified sufficient bounds and declared cost prescriptions. It
neither proves that direct or greedy masking is globally fastest nor rules out
a parity advantage at larger widths, different prices, or tighter instance-
dependent accuracy bounds. A model-wide strongest-method advantage remains open.

## 5. Reproduction

The 18 new unittest methods pass locally. The local starter has nine preexisting
tests, so the local combined run has 27; do not confuse it with the remote
baseline's 12 preexisting tests. The supplied parity and matched validators pass
in isolated copies. Both input archives and all 22 scientific files remain
unchanged. Actual remote counts, hashes and logs are in REMOTE_VALIDATION.json
and its named run directory once that workflow completes.

The source files uploaded through GitHub were checked against locally computed
Git blob hashes. The container cannot resolve github.com, so local validation
used the supplied archives, not an authenticated checkout. Remote branch state
and writes use the authorized GitHub connection. No external peer review or
new audit of the older spectral/coherence arguments occurred.

## Stop

PF-02's implementation, finite acceptance comparison and decision are recorded.
No merge, publication, release, license, manuscript, hardware campaign, new
ansatz or further parameter sweep is authorized or performed by this step.
