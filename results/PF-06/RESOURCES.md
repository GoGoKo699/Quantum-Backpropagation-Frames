# PF-06 matched implementation ledger

## Common contract and units

All readouts receive the same single-copy real reference-response state and
return the original P=6m gradient entries. Each preparation uses the declared
controlled objective once. Count physical input preparation, the forward circuit
and its actual inverse, controls and calibration equally on every side. A
zero-angle trainable circuit is the identity and may be removed for ALL methods;
we do not charge the comparator for executing known identity rotations.

Let C be the actual common response cost, Q_X/Q_S the extra quantum readout work,
L_X/L_S the streamed bit/arithmetic work, F_X/F_S preprocessing, and D_X/D_S final
mapping/output work. For a common unchanged-sample-mean Markov guarantee,

```math
K_j=\left\lceil B_j/(\delta\varepsilon^2)\right\rceil,
\qquad W_j=F_j+K_j(C+Q_j+L_j)+D_j.
```

This is a sufficient-budget comparison, not exact optimal high-confidence
sample complexity. Gates, bits, arithmetic, memory and time are not silently
added without prices. The supplied resources.json keeps the components separate.

## New sparse construction

For m blocks the displayed reference-readout circuit has 14m-5 CNOTs, 12m-4
single-qubit full-angle R_y gates, two X gates and one H. It uses no extra work
qubits, intermediate measurements, or resets. All n+1 qubits are measured in Z.
Preprocessing constructs 18m tangent scalars, 3m row norms and O(m) gate data.
The outcome scan touches at most m two-bit blocks; there is at most one signed
counter update. Final block contractions require 18m multiplications and 12m
additions plus normalization operations, all counted in the executable record.
Classical work is O(Kn+P), storage O(P), and physical gate work O(Kn)+K C.

No quantum basis routing occurs: only a known sparse reference vector is
prepared. The exact minimax result applies at the flat zero-angle point.
At other one-layer points the bound is computed from constant-size block
matrices and is not an anisotropic minimax theorem.

## Strong alternatives remain eligible

| Method | Variance budget and quantum work | Classical cost and qualification |
|---|---|---|
| No-mask local Walsh | At zero: B_X=4P exactly, n+1 H gates and no entangling readout; elsewhere the disjoint local S(y) maximum gives a valid bound | O(m) signed-histogram updates per record; one local transform/contraction after averaging. O(P) memory. |
| Optimized exact full mask | B=4P. Use the existing direct/pivot/greedy terminal plans, with their mandatory affine relabeling. Do not force the n(n-1)/4 direct-CZ expectation if a cheaper plan is available | Include mask sampling, synthesis, relabeling and local Gray-character accumulation. No dense response or snapshot is required. At the flat point masks add no statistical improvement over no mask. |
| Grouped suffix reversed tests | Three eligible groups of two commuting generator slots, not one circuit per derivative. Each group has 2m coordinates, sufficient v_a=8m. Optimal allocation gives B=(3sqrt(8m))^2=72m=12P | Different suffix costs must be retained. Work for a squared-error budget is (sum_a sqrt(v_a c_a))^2/epsilon^2; common confidence factor can be inserted. This is an upper prescription, not a lower bound on every re-grouping. |
| Reference-adapted block shadows | One fixed partition aligned with disjoint blocks suffices; no two-partition coverage penalty is necessary. Rank-two two-qubit operators have a sufficient summed bound (40/3)P using the 5/6 Clifford moment factor | O(m) fixed-size Clifford circuits and sampling per record; aggregate only needed zero-column entries, then contract. Never force full global snapshots or per-shot gradient multiplication. |
| Global Clifford and other optimized measurements | Existing moment bounds give O(P) total variance. Measurements, synthesis and decoder optimizations are allowed | No universal runtime ranking or gate-count lower bound is obtained here. A measurement framework allowed to implement this same sparse POVM can reproduce it. |

The block-shadow number is a substitution into the standard dimension-four
third-moment identity and the reference-state reduced block. It is a comparator
upper bound, not a newly benchmarked optimal block design. The established
methods and source contracts are listed in SOURCE_NOTES.md. This phase does not
repeat the PF-02 price sweep or overwrite its negative result.

## Exact zero-angle crossover with the cheapest comparator

At zero angles, B_X=24m and B_S=24m-8. Ignoring integer rounding, sparse beats
no mask under a DECLARED full cost model only if

```math
8C>(24m-8)(Q_S+L_S)-24m(Q_X+L_X)
       +\delta\varepsilon^2(F_S+D_S-F_X-D_X).
```

The gate-only CNOT specialization takes Q_X=0, Q_S=14m-5 and ignores ALL
single-qubit, classical and measurement costs. In that explicitly incomplete
ledger, the crossover is

```math
C_{\rm CNOT}>(3m-1)(14m-5).
```

For m=4 it is 561 common CNOTs; for m=256 it is 2,745,093. The maximum
worst-case preparation-count improvement is 3m/(3m-1), which approaches one.
This cannot support a growing asymptotic advantage. It also does not mean every
objective has only an eight-unit variance improvement: pointwise the gap is
2P(1-||Pi q||^2), and can be extensive. Using that information operationally
requires a valid bound or charged pilot data, not hindsight.

For fixed epsilon and delta both sparse and no-mask have total work
O(P(C+P)/epsilon^2), up to the common confidence factor, in this one-layer
regime. The successful compiler therefore closes a feasibility gap but does
not prove a new scaling separation from a strong existing local readout.

## Not modeled

All-to-all arbitrary-rotation logical counts are not routed depth, wall-clock
time, noisy-device robustness, fault-tolerant synthesis, or classical-hardness
claims. Small validation objectives are deliberately easy and test identities.
The circuit can receive a general controlled real reflection; no favorable
objective runtime or classical separation is inferred from that access promise.
