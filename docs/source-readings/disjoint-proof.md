# PF-06: compile the sparse readout by preparing its reference

[Canonical theory](../THEORY.md) · [Constructive circuits](../COMPILERS.md) · [Evidence](../EVIDENCE.md)

Reading copy with mathematical rendering syntax adjusted. The source's scientific statements and wording are preserved. [Original source, plain view](../../results/PF-06/PROOF.md?plain=1).

Original source SHA-256:

```text
ad3389ce5a29d1f1e0ebe6c0f4db91472280608d634a1c8256ecead895d375d7
```

[Deterministic generator and identity check](../../tools/render_source_readings.py).

This packet gives an explicit terminal measurement on the disjoint one-layer
subfamily of the existing six-rotation circuit. It does not assume a supplied
tangent-basis oracle, change gate-angle coordinates, or extend the exact minimax
theorem to nonflat spectra. All formulas here use a real normalized response q.

## 1. Known local structure replaces basis routing

Use m disjoint two-qubit blocks, n=2m system qubits and P=6m full-angle gate
parameters. Each block has the ordered generators YI,IY,YX,XY,YZ,ZY. Global
parameter order is generator-slot first, then block (the inherited ordering).
At a fixed parameter point,

```math
T=U^{\mathsf T}J,\qquad q=U^{\mathsf T}OU|0\rangle,
\qquad g=2T^{\mathsf T}q.
```

For parameter slot j in block b, cancellation of the later gates gives

```math
t_{b,j}=U_{b,\lt j}^{\mathsf T}(-iA_j)U_{b,\lt j}|00\rangle
            \otimes|0\rangle_{\text{other blocks}}.
```

Reality and normalization make the 00 entry zero. Define K_b as its three
remaining rows and six columns. Each column has unit norm, since A_j^2=I.
Thus s=sum_b ||K_b||_F^2=6m=P, throughout the angle domain. Computing each K_b
uses only constant-size (four-dimensional) matrices and six prefix steps.

The relevant addresses x(b,t), t=1,2,3, contain one nonzero two-bit block and
zeros elsewhere. Distinct such addresses are orthogonal. Let k_x in R^P be
the corresponding row of T, with only that block's six parameter entries.
Set d_x=||k_x||^2 and c_x=sqrt(d_x/s). Zero rows can be excluded; they contribute
no derivative. No SVD is needed. At full block rank the active space has r=3m
dimensions. The decoder uses the original K_b, not rotated parameters.

## 2. The actual readout

Starting with one supplied copy

```math
|\Omega(q)\rangle=(|0,0\rangle+|1,q\rangle)/\sqrt2,
```

apply a known state-preparation unitary A ONLY on the reference-qubit-zero
branch. Its sole required input-column contract is

```math
A|0\rangle=|c\rangle=\sum_{x:d_x>0}\sqrt{d_x/s}|x\rangle.
```

The response branch is unchanged. Apply H to the reference qubit, then measure
all n+1 physical qubits in the computational basis. For active address x and
reference outcome b the exact probability and returned score are

```math
p(b,x)=\frac{(c_x+(-1)^b q_x)^2}{4},
\qquad Z(b,x)=2(-1)^b\frac{k_x}{c_x}.
```

Every other physical outcome returns zero. Keeping those zero records in K is
essential: there is no postselection or conditional normalization. Coarse-grain
them into one complementary POVM outcome if desired. This implements a
2r+1-outcome POVM on the occupied reference-response subspace when all d_x>0;
it still physically measures n+1 bits per experiment.

Indeed p(0,x)-p(1,x)=c_x q_x, so summing scores proves E[Z]=2T^Tq. The active
score norm is exactly 2 sqrt(s). Consequently, with Pi the projector onto the
active coordinate addresses,

```math
\mathrm{tr}\mathrm{Cov}_q(Z)
=2s(1+\|\Pi q\|^2)-4\|T^{\mathsf T}q\|^2.           (1)
```

For full row rank in this coordinate subspace, write mu_min for the smallest
eigenvalue of the block diagonal matrix diag_b(K_b K_b^T). Then the exact
worst-case trace risk of THIS measurement is

```math
B_{\rm sparse}=\max\{2s,4s-4\mu_{\min}\}.               (2)
```

The response can lie outside the active subspace, or in a least-eigenvalue
active direction, so both endpoints are attainable. If rows are absent or the
blocks lose rank, (1) with the actual nonzero-row support remains valid; 4s is
always a sufficient bound. The code's inclusion of zero eigenvalues can give a
conservative bound in a reduced-support case. Numerical eigenvalues are not
interval certificates.

## 3. Exact optimum on the audited flat instance

At zero angles K_b K_b^T=2I_3, d_x=2, r=3m and s=P=6m. Hence c_x=1/sqrt(r).
The effects and scores restricted to span(a,b_x) become exactly the sparse
attainer in PF-05, with L the computational-coordinate embedding and
V^T=K/sqrt(2). Therefore the existing all-POVM theorem applies:

```math
B_{\rm sparse}=4P-8
  =\inf_{\text{universally unbiased one-copy POVMs}}
       \sup_q\mathrm{tr}\mathrm{Cov}_q(Z).
```

For nonzero angles the same executable measurement is universally unbiased
and obeys (1)-(2), but no anisotropic optimality claim is made. Weighted reference
amplitudes keep its score norm bounded without a quantum singular-vector basis.

At the flat point ordinary all-X readout has risk 4P-||g||^2, while (1) gives
2P(1+||Pi q||^2)-||g||^2. Their pointwise trace difference is
2P(1-||Pi q||^2)>=0. Nevertheless their WORST-case risks differ only by 8; the
worst-case ratio 4P/(4P-8) tends to 1. Pointwise error behavior and a uniform
confidence prescription are different comparisons.

## 4. Elementary circuit, including the controls

Reference qubit is site 0. Each block uses two system sites, with the right
site its initial marker. Start by flipping the first marker conditioned on
reference=0 (two X gates on the reference and one CNOT).

Let w_b=sum_t d_(b,t), R_b=sum_{j>=b} w_j. A chain of m-1 controlled exchange
rotations sends a marker from block b to b+1 with angle

```math
\theta_b=\mathrm{atan2}(\sqrt{R_{b+1}},\sqrt{w_b}).
```

This creates amplitude sqrt(w_b/s) on each one-marker address. The ideal
w_b=6 here, but the weighted expression also handles rounding consistently.
The two-level exchange preserves 00 and 11 on its marker pair. It is compiled as
CNOT, a two-control R_y multiplexor, and CNOT. The middle rotation acts only
when the second marker is one AND reference is zero. With our full-angle
convention R_y(theta)=exp(-i theta Y), its active angle is -theta_b.

On each occupied block, two further controlled rotations produce its three
local amplitudes. From local 01, rotate the left bit conditioned on right=1
and reference=0, by

```math
\alpha_b=\mathrm{atan2}(\sqrt{d_{b,2}+d_{b,3}},\sqrt{d_{b,1}}).
```

Then rotate the right bit conditioned on left=1 and reference=0 by

```math
\gamma_b=-\mathrm{atan2}(\sqrt{d_{b,2}},\sqrt{d_{b,3}}).
```

The latter angle is zero when both arguments vanish. Empty blocks remain 00.
The response branch is EXACTLY the identity for every input vector, not only
for the tested q. The final H produces the probabilities above.

A standard cyclic-Gray uniformly controlled rotation with two controls uses
four CNOTs and four one-qubit rotations [S1]. The implementation retains its
complete cycle, with no uncharged residual diagonal. This gives the displayed
readout counts, excluding the common response preparation:

```math
N_{\rm CNOT}=1+6(m-1)+8m=14m-5,
\quad N_{R_y}=4(m-1)+8m=12m-4.
```

There are also two X gates, one H, n+1 measurements, and ZERO additional work
qubits beyond the reference qubit already in Omega. These are counts of our
explicit circuit, not minimum synthesis bounds. W/Dicke-state preparation and
controlled-rotation synthesis are established ingredients [S1,S2]. Counts assume
all-to-all connectivity and arbitrary one-qubit rotations. The given sequential
schedule has O(m) depth; no logarithmic-depth or routed-device claim is made.

## 5. Classical and precision costs

The compiler stores 18m tangent scalars, 3m row energies and O(m) gate data. All
preprocessing is O(m) scalar work at a fixed parameter point and is repeated
when the parameters change. No N-by-P object, dense Pr output map, or quantum
address-compression circuit is supplied for free.

Scan the n-bit system result to check whether exactly one two-bit block is
nonzero: O(n) bit work in the worst case. Update one of 3m signed counters, or
make no update on a failure. After K experiments, contract the counts with the
stored 3-by-6 block matrices once and emit all P entries. The full classical
cost is O(Kn+P), with O(P) memory; it is NOT O(K) if reading/classifying the
physical outcomes is counted. The final contraction needs 18m multiplications
and 12m additions, plus explicitly recorded normalization/scaling operations.

For the unchanged sample mean, MSE<=B/K and Markov gives the common sufficient
budget K>=B/(delta epsilon^2). No exact optimal-tail or adaptive guarantee is
claimed. Finite gate synthesis needs its own error budget: if the entire
readout unitary has operator error zeta, outcome L1 distance is <=2zeta and
score norms <=2sqrt(s) imply bias <=4sqrt(s)zeta. With G compiled gates, bounding
each gate error by epsilon/(8G sqrt(s)) is sufficient for readout bias <=epsilon/2.
This does not price fault-tolerant synthesis or include imperfect response-state
preparation, classical table error, or hardware noise. Those are additional
errors, not removed by the exact logical calculation.

## 6. Boundary of the construction

A second overlapping layer can create tangent amplitudes on addresses with
multiple nonzero disjoint blocks. The one-layer selector would discard genuine
derivatives. The diagnostic packet exhibits such a four-qubit case explicitly.
Neither the one-layer proof nor the compiled circuit is a general tangent-basis
compiler for overlapping or arbitrary-depth circuits. The linear-time claim
uses the charged, existing disjoint block structure, not only small tangent rank.
