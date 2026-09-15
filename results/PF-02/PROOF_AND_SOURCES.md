# Terminal compiler contract and source map

This note verifies the two concrete classical compilers. It introduces no new
claim about randomized designs or gradient-query optimality.

## Exact contract

Let f(x) be the sampled quadratic binary polynomial. A compiler returns a CNOT
network L, a residual CZ polynomial Q, and a bit mask h such that

```math
Q(Lx)=f(x)+h\cdot x \pmod 2.
```

Execute L then the residual CZ circuit. It maps |x> to
(-1)^(f(x)+h.x)|Lx>. The X measurement outcome y is mapped to

```math
y_{\mathrm{ideal}}=L^{\mathsf T}y+h.
```

This proves equality of the folded Born probabilities for arbitrary input
states, not equality of the unmeasured unitary. It also preserves a zero-state
reference. Relabeling can be computed by traversing the transposed CNOTs in
reverse order; a dense n x n multiplication is unnecessary.

## Pivot construction

Choose an edge (i,j). Write the current polynomial as

```math
x_i x_j+x_i A(x)+x_j B(x)+C(x).
```

Set y_i=x_i+B and y_j=x_j+A using CNOTs from the remaining active variables.
Then the polynomial is y_i y_j+C+AB. Cross terms of AB update the residual graph;
its diagonal terms form a known linear character. Deactivate i,j and repeat.
The recorded pair CZs and CNOT network realize the contract with that character.

## Greedy construction

Changing variables by CNOT(c,t) substitutes x_t=y_t+y_c. Only the row/column at
c changes in the graph; an edge (c,t) additionally contributes a linear y_c term.
A current linear y_t term also adds y_c. Repeat only transformations saving at
least two CZs for one CNOT. At the end translate the linear character by L.T.
The total CNOT+CZ count therefore cannot exceed the direct edge count in this
unweighted gate library. Synthesis work and different gate prices still matter.

## Sources examined in PF-02

[S1] G. Park, Y. S. Teo and H. Jeong, arXiv:2311.14622v4,
https://arxiv.org/html/2311.14622v4 . Methods C, Theorem 3 and Appendix G discuss
exact equatorial-mask compilation and terminal outcome postprocessing. They
specifically allow removing terminal reversible linear work from the quantum
circuit. Our pivot and greedy routines are independently implemented instances
of binary phase-polynomial manipulation, not claimed copies of their exact
LNN construction or globally optimal synthesis. Full masking retains its
original ensemble and covariance; gate optimization does not change that fact.

[S2] D. Maslov and W. Yang, arXiv:2210.16195v2,
https://arxiv.org/html/2210.16195v2 . Sections II-III concern Hadamard-free
Clifford circuits, mixing CNOT/phase/CZ layers, and architecture-specific depth.
This supports allowing such synthesis in the baseline. Its depth results are
not imported as finite gate-count certificates for the two routines here.

[S3] D. Li et al., arXiv:2408.05406v1,
https://arxiv.org/html/2408.05406v1 . Reversed Hadamard tests motivate moving the
objective into the controlled operation and grouping measured generators.
PF-02 reuses the already checked grouped-suffix fixture and includes its
shorter suffix, joint measurement, and cost-aware shot allocation.

Accessed 2026-09-15 via web retrieval. Primary-source HTML was examined; no PDF
figures were analyzed. This is a bounded implementation-source check, not a
fresh novelty audit. The stronger design-order, locality and scope caveats in
results/PF-01/SOURCE_AUDIT.md remain in force. No source says that the implemented
portfolio exhausts all optimized Clifford or shadow strategies.
