# PF-04: growing-depth implementation regime

[Canonical theory](../THEORY.md) · [Constructive circuits](../COMPILERS.md) · [Evidence](../EVIDENCE.md)

Reading copy with mathematical rendering syntax adjusted. The source's scientific statements and wording are preserved. [Original source, plain view](../../results/PF-04/STRUCTURE.md?plain=1).

Original source SHA-256:

```text
7136645f6f9ecbf2ffc6aa3f3f24f8bdc5e7f639299dfd1d030bd7e16bdce199
```

[Deterministic generator and identity check](../../tools/render_source_readings.py).

## Task and chosen family

Use the same real nearest-neighbor family as the preserved matched-readout
fixture: alternating layers of disjoint pairs, with the six full-angle Pauli
rotations YI,IY,YX,XY,YZ,ZY in each pair. Do not change coordinates or give a
method stronger objective access. The complete P-entry gradient and whole-vector
accuracy remain the output contract. Fix d(n)=ceil(log2(n)/2), hence P=Theta(nd)
and a reversed tangent has interval width at most w=2d=O(log n).

This is a structural compilation check, not a new acceptance sweep. The five
sizes 8,16,32,64,128 and seed 2026091571 were fixed before evaluating the compiler.
There are no sampled objective responses in this part and no search for favorable
price profiles. Small matrix tests separately use the original fixture.

## Independent local compiler

Represent the circuit by per-wire predecessor indices. To compile tangent j,
start from the preceding gates on the nonidentity support of its generator.
Visit the causal predecessors in reverse index order. Include a gate once; add
its sites and predecessors. Gates outside this backward operator cone cancel.
The resulting local word computes

```math
t_j=-iU_{\lt j}^{\dagger}A_jU_{\lt j}|0\rangle
   =\tau_j\otimes|0\rangle_{\overline{I_j}}.
```

Apply only the selected prefix gates to the local vacuum, apply -i A_j, then
reverse those selected gates. All operations are real because each generator
has exactly one Y. The implementation uses sparse Pauli permutations, not dense
2^w-by-2^w local gates. It never constructs the global state or a dense Jacobian
in the growing-size checks. Local cone compilation agrees with independently
calculated full-state tangents for n=2..6 and d=1..3.

Let L=sum_j 2^|I_j| be the length of the explicit tangent representation. Each
cone contains O(d^2) elementary local gates. The compiler has O(d^2 L) scalar
arithmetic and O(L+P) resident storage, plus polynomial indexing overhead. The
current heap implementation adds a logarithmic scheduling overhead. Computing
all Walsh tables costs O(sum_j |I_j| 2^|I_j|). Every parameter point pays this
preprocessing again.

A narrow lower bound is immediate: a compiler REQUIRED TO MATERIALIZE these L
entries must write L scalars and retain that much output storage. This is an
output-size lower bound for this representation, not a lower bound on all exact
or approximate decoders. Tensor-network contraction can avoid a full table in
other structured cases; circuit contraction complexity is controlled by graph
structure (S6), not only by a light-cone-width upper bound.

## Why the inherited parity recipe does not yet separate

For the worst-width certificate beta<=2^w and fixed variance slack eta, parity
requires k=O(w+log(1/eta)). Its clean or measured implementation has O(nk)
additional two-qubit operations. Its displayed shifted-table decoder has 4^k
terms per coordinate. When k is chosen using beta of order 2^w, this is of order
2^w at fixed eta (up to constants), not a cure for exponential-width processing.
An optimized direct quadratic-mask decoder also computes its local characters
in O(2^w+poly(w)) word kernels through Gray traversal. Shift collisions and
alternative contractions can improve either implementation; no decoder lower
bound is inferred from these upper counts.

For d=Theta(log n), the crude explicit-table upper bound is polynomial rather
than exponential in n, but can be O(n^2 polylog n). No-mask precomputed lookup
can be fast online but retains its potentially large variance. Paying extra
mask gates while retaining a similar table-processing cost does not establish a
new end-to-end scaling.

## Strong eligible alternatives

- Full exact masking attains total variance <=4s. Terminal synthesis and
  aggregation remain allowed; it need not use one unoptimized CZ per edge.
- Grouped suffix reversed tests do not construct tangent tables. Their 3d
  commuting-pair groups have sufficient concatenated variance budget O(dP).
  Count their different suffix costs and shot allocation; do not compare only
  with one circuit per coordinate. The construction follows the same prior
  reversed-Hadamard principle (S4).
- Rank-two local block shadows from the retained comparison have total variance
  <=32s. Two staggered block partitions of length <=2w cover each cone. Uniform
  Clifford transformations on blocks have conventional polynomial-in-w
  sampling/synthesis and O(w^2) gate implementations, totaling O(nw) readout
  gates over all blocks, absent routing. Thus parity's O(nw) gate upper bound
  is not an asymptotic separation over this comparator. Relevant stabilizer
  amplitudes can be evaluated on the union of tangent supports. Do not force
  full-block density matrices or per-shot complete-gradient contraction.
- Generic global Clifford shadows already give total variance O(s). Their
  synthesis and decoder must be priced; a two-design alone is not the usual
  third-moment guarantee (S2, S3).
- The exact POVM in PROOF.md improves constants, but the cost of its tangent
  basis/isometry is unspecified for this growing family. It is not eligible
  as a claimed efficient implementation simply because it has O(r) outcomes.

These are theorem-level and kernel-cost comparisons, not a new full priced
experiment. resources.json deliberately does not name a winner. PF-02's 144
priced scenarios, negative parity result, code and records are unchanged.

## Decision

The local compiler is executable in the growing-depth regime and avoids a full
2^n statevector. This confirms feasibility of the explicit local representation.
It does not establish a separation from the strongest matched decoder or
measurement class. The only implementation lower bound proved here is the
explicit-representation output-size bound. No unrestricted circuit lower bound
was obtained, and no generic efficient tangent-eigenbasis compiler is supplied.

The evidence does not justify a larger favorable-case parity sweep. A future
implementation study must select a compact representation with a charged
construction and a comparator for which that representation changes total work,
rather than just substituting a sharper variance constant.
