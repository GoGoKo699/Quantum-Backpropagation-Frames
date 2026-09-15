# PF-07 resource contract and matched-method boundary

The output remains the entire raw-coordinate gradient with Euclidean error
and explicit confidence. The initial reference-response preparation, exact
calibrated controlled objective, and parameter point are common to eligible
methods. A single readout consumes one copy. No additional coherent oracle
query is used. Hardware timing, routing and fault-tolerant synthesis are not
identified with the arbitrary-rotation CNOT ledger.

## Charged input and the compiler

Local tangents are represented by their interval endpoints and explicit tables.
Let L=sum_j 2^{|I_j|}, W=sum_j |I_j|, w=max_j |I_j| and nu the maximum number of
intervals covering a site. Computing those tables from the existing circuit
uses the prior causal compiler. Its actual local gate visits and amplitude
kernel work are recorded. No tangent eigenbasis, QRAM, global state, dense
Jacobian or free compressed input is assumed.

The new preprocessing is O(L+W+n w 2^w). Working memory excluding emitted program
storage is O(L+W+n+2^w). Holding the emitted circuit adds one record per gate,
O(n2^w), including classical precision/index bits. Streaming emission avoids
retaining that list during compilation; it does not make program storage or
repeated regeneration cost vanish in a deployed system.

For ell_a=R_a-a-1 and positive first-sector masses, F=sum_a 4(2^{ell_a}-1).
The exact displayed circuit has CNOT=6n-5+F, Ry=4(n-1)+F, X=2 and H=1. It has
no extra work qubits, intermediate measurements or resets. It measures n+1
physical bits. The schedule is sequential and all-to-all, not low-depth/routed.
A complete physical-outcome scan and sparse original-coordinate score cost
O(n+nu w) bit/scalar work, at most nu parameter updates, and O(P) final output.
The real/scalar model separates this from the precision cost of arithmetic.

## Common confidence prescription

The logical sample mean has MSE<=4s/K and active score norm 2sqrt(s). Use
K=ceil(4s/(delta epsilon^2)) as the SAME conservative sufficient prescription
where the comparator has variance bound 4s. Do not infer exact optimal tails
or adapt the sample count using q known only inside the validation simulator.
The main exact minimax theorem for flat spectra is not extended to general
rows. Coordinate-support null directions can saturate 4s for this decoder.

## Strong comparators

| Method | Statistical/circuit treatment | Classical treatment |
|---|---|---|
| No-mask Walsh | Keep its actual compiled imbalance or small-system exact risk. It costs only n+1 H measurement gates; no reason to require a mask when it is sufficient. | Share local interval histograms and transforms. Permit direct/table lookups and aggregate-first contractions. |
| Exact quadratic mask | Worst trace variance 4s is attained at q=vacuum. Allow the maintained direct/pivot/greedy terminal circuits with mandatory affine outcome correction. Direct O(n^2) CZ masking is not an optimal synthesis lower bound. | Include mask sampling, synthesis, correction and shared local Gray-character accumulation. Never reconstruct the global response. |
| Parity masks | Both clean and measured-uncomputation variants, with their audited covariance interpolation and corrected decoding cost. | PF-02's negative 144-scenario result is retained. No new favorable price profile is searched. |
| Block Clifford shadows | Cover width-w intervals with valid staggered blocks, or exploit a better aligned cover where available. The established rank-two construction has O(s) trace-risk budgets but extra block gates. | Aggregate only needed zero-column entries. Direct O(L poly(w)) per-record work is an IMPLEMENTATION upper bound, not a lower bound on every optimized decoder. |
| Grouped suffix reversed tests | Allow the eligible commuting subgroups at each layer, unequal suffix costs and optimal charged shot allocation. | Permit shared sums and only one output assembly. Do not use coordinate-by-coordinate parameter shift as the sole baseline. |
| Sparse-state preparation alternatives | Modern ancilla-free, control-stripped, measurement-assisted and Toffoli/T optimized constructions remain eligible after matching their contracts. | Charge the required support list/representation construction, any permutation/isometry and its classical compilation. A framework using this same first-site preparation is the same method, not a slower competitor. |

Given preprocessing F_j, common response C, extra quantum work Q_j, streamed
classical work D_j and final output O_j, compare

```math
T_j=F_j+K_j(C+Q_j+D_j)+O_j.
```

For the new implementation, under precompiled-program replay,

```math
T_{\rm new}=F_{\rm tangent}+O(L+W+nw2^w)
 +K\bigl[C+O(n2^w)+O(n+\nu w)\bigr]+O(P).
```

For the depth-d line family, P=Theta(nd), w<=2d and nu=O(d^2). Bounded d therefore
permits linear preprocessing and readout work, but that is also achievable by
existing structured readouts. Growing d exposes an exponential-width reference
circuit. Reducing streamed classical decoding alone does not establish a
reduction in TOTAL work if the cost moves into the reference circuit.

**Acceptance:** the overlap obstruction is removed by an explicit compiler.
**Not established:** a strongest-method total-work separation, hardware win,
new price-grid winner, universal decoder lower bound or new state-preparation
primitive. The auxiliary fixed-envelope dimension count is a preparation-only
statement and cannot replace this comparison.
