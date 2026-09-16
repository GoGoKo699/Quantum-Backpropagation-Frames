# PF-07: overlapping intervals admit a streamed known-reference compiler

[Canonical theory](../THEORY.md) · [Constructive circuits](../COMPILERS.md) · [Evidence](../EVIDENCE.md)

Reading copy with mathematical rendering syntax adjusted. The source's scientific statements and wording are preserved. [Original source, plain view](../../results/PF-07/PROOF.md?plain=1).

Original source SHA-256:

```text
f5d243f28f2bb54c6a2301fd06de0eb69a36c5a4c57be02a8e482e31beed1045
```

[Deterministic generator and identity check](../../tools/render_source_readings.py).

## 1. Contract and result

At one parameter point let the real reversed tangents be

```math
t_j=\tau_j\otimes|0\rangle_{\overline{I_j}},\quad
I_j=[l_j,r_j),\quad |I_j|\le w,\quad (\tau_j)_0=0.
```

Intervals may overlap arbitrarily and columns need not be orthogonal, distinct,
or equally sensitive. The local tables are CHARGED input, with total size
L=sum_j 2^{|I_j|}; their circuit-derived construction is counted separately.
T has columns t_j, s=||T||_F^2>0, and the target is the complete original vector
g(q)=2T^Tq for an unknown real unit q. The experiment receives exactly one copy
of (|0,0>+|1,q>)/sqrt(2). Its controlled-objective/preparation cost is common to
all compared readouts. The response is not classically supplied to the learner.

**Constructive theorem.** A circuit of O(n 2^w) CNOT and arbitrary one-qubit
rotation gates, with no additional work qubits, prepares the row-norm reference
on the reference-zero branch while leaving the entire response branch unchanged.
It is compiled from the local tables without a global support-address union or
a tangent eigendecomposition. A local sparse decoder is universally unbiased,
has active record norm 2 sqrt(s), and worst-case total variance at most 4s.
The precision-dependent cost of finite-gate synthesis is not included in these
exact logical gate counts. No strongest-method or anisotropic minimax claim is
part of the theorem.

The proof below constructs every operation; the implementation supplies actual
CNOT/Ry/X/H instructions. Its Ry(theta)=exp(-i theta Y) uses full angles.

## 2. Row-norm readout, with overlaps retained

Let k_x be the transpose of row x of T. Define

```math
d_x=\|k_x\|_2^2=\sum_j(t_j)_x^2,\qquad
c_x=\sqrt{d_x/s},\qquad
|c\rangle=\sum_{d_x>0}c_x|x\rangle.
```

Overlapping tangent contributions are added as SQUARED amplitudes before taking
the square root. Coherently adding tangent vectors is not the same reference.
No parameter coordinate is changed. Zero rows need no reference amplitude.

Prepare c only in the reference-zero branch and apply H to that reference bit.
After measuring all n+1 physical bits in Z, return

```math
p(b,x)=\tfrac14(c_x+(-1)^bq_x)^2,\qquad
Z(b,x)=2(-1)^b k_x/c_x\quad(d_x>0),
```

and zero otherwise. All physical outcomes count towards the number K of trials;
there is no postselection or normalization by an active-outcome probability.
Since p(0,x)-p(1,x)=c_x q_x, the mean is exactly 2T^Tq. Every active record has
norm 2sqrt(s). Writing Pi_S for the projector onto the NONZERO COORDINATE ROWS,

```math
\mathcal R(q)=\mathrm{tr}\mathrm{Cov}_q Z
 =2s(1+\|\Pi_Sq\|_2^2)-4\|T^{\mathsf T}q\|_2^2\le4s.       (1)
```

Pi_S need not be the projector onto the tangent column span. In particular, if
there is a unit q in this coordinate support with T^Tq=0, the bound 4s is exactly
attained. Such directions occur whenever the number of nonzero rows exceeds
rank(T). The new circuit does NOT extend PF-05's flat-spectrum exact optimum to
arbitrary overlapping or unequal-spectrum cases. The inherited all-measurement
lower bound 2s still makes (1) a factor-two upper approximation within the real,
single-copy, universally unbiased trace-risk contract; this is an application
of that prior result, not a new lower-bound proof.

## 3. A unique first nonzero site removes the ambiguity

Every x!=0 has a unique leftmost 1, at site a. A tangent can contribute only if
its interval contains a and all later nonzero bits. Let

```math
R_a=\max(\{a+1\}\cup\{r_j:l_j\le a\lt r_j\}),\quad
\ell_a=R_a-a-1\le w-1.
```

Define an array h_a(z), z in {0,1}^{ell_a}, by summing local squared tangent
entries compatible with zeros before a, a 1 at a, suffix z, and zeros after R_a.
For j with a in I_j, its local address must begin with zeros and its first 1 at
local position a-l_j. Put c_j=2^{r_j-a-1}; the relevant amplitudes are exactly

```math
\tau_j[c_j:2c_j].
```

Square that slice and insert it into h_a at strides 2^{R_a-r_j}. This enforces
zero padding beyond the contributing interval. Then h_a(z)=d_x for the unique
associated physical x. Let mu_a=sum_z h_a(z). The sectors are disjoint and

```math
\sum_a\mu_a=s.
```

Each nonzero local-table address belongs to ONE first-site slice, even when a
global physical address receives contributions from several columns. Thus all
mu_a values can be formed with O(L+sum_j |I_j|+n) arithmetic/index work. After
that, construct one h_a at a time and discard it when its circuit block has
been emitted. No list of n-bit global addresses or complete union is created.
This is a memory/representation statement, NOT an assertion that the local
2^w work disappears. All local tables remain stored and charged.

## 4. Actual controlled preparation and why the direction matters

### Stage A: one marker

On reference=0, set physical system site 0 to 1. A chain of n-1 controlled
single-excitation exchange rotations prepares

```math
\sum_a\sqrt{\mu_a/s}|e_a\rangle,
```

where e_a has just its a-th bit equal to 1. The angle on markers a,a+1 is
atan2(sqrt(sum_{b>a} mu_b),sqrt(mu_a)). Empty sectors use well-defined limiting
angles. This is a weighted W-state preparation using established primitives.
Every exchange is explicitly controlled on reference=0. The exchange action
is 10 -> cos(theta)10+sin(theta)01, with 00 and 11 fixed. It is compiled as a
CNOT, a complete two-control Ry multiplexor, and a CNOT (six CNOTs/four Ry).
The initial negative control uses two X gates and one CNOT.

### Stage B: fill bounded suffixes, RIGHT TO LEFT

For a=n-1,...,0, conditioned on reference=0 and system bit a=1, prepare

```math
\sum_z\sqrt{h_a(z)/\mu_a}|z\rangle
```

on the ell_a sites immediately to the right. Skip mu_a=0. No operation targets
a site left of its marker. The following induction proves the control is valid.
Before processing a, a branch whose original marker is b<a has not yet been
filled, so its a-th bit is zero. A branch whose marker is b>a was filled only
to the right of b, so its a-th bit is also zero. The branch with marker a has
its suffix in the all-zero state. Therefore exactly the intended branch fires.
Later processing of smaller markers cannot disturb this completed branch.

At the end the amplitude for x with first site a is
sqrt(mu_a/s)*sqrt(h_a(z)/mu_a)=sqrt(d_x/s), as required. The response-one branch
is identity through every COMPLETE controlled block, on every input state.
Processing in the opposite order is generally wrong: newly created suffix
ones can act as false later markers. The packet contains an explicit failing
three-qubit example and tests the correct order through full gate execution.

## 5. No uncompiled multiple controls

The positive suffix state uses sequential conditional rotations from its
binary prefix masses. For suffix bit j=0,...,ell_a-1, the controls are its j
previous suffix bits plus the marker and reference. The angle table has 2^{j+2}
entries, with nonzero angles only in marker=1,reference=0. Each complete cyclic-
Gray multiplexor has exactly 2^{j+2} CNOTs and the same number of Ry rotations.
The coefficients are a Walsh transform with a Gray permutation [S1, Eq. (3)].
The implemented FAST transform takes O((j+2)2^{j+2}) arithmetic, not a dense
Walsh-matrix multiplication. No phase byproduct is omitted.

Let A={a:mu_a>0} and F=sum_{a in A}4(2^{ell_a}-1). Exact emitted counts are

```math
N_{\rm CNOT}=6n-5+F,\qquad N_{R_y}=4(n-1)+F,
```

plus two X gates and the final reference H. There are n+1 terminal measurements
and ZERO additional work qubits, intermediate measurements or resets. Gates
are not asserted to be individually optimized; zero rotations may be retained.
All-to-all connectivity is assumed. This sequential program does not establish
a routed or logarithmic-depth implementation.

For the full width-w nonvacuum address envelope,

```math
M_w=(n-w+2)2^{w-1}-1\quad(1\le w\le n),
```

and sum_a 2^{min(w-1,n-a-1)}=M_w. Hence

```math
N_{\rm CNOT}\le4M_w+2n-5,\qquad N_{R_y}\le4M_w-4.
```

This is O(n2^w), and also O(M_w) uniformly up to w=n. The envelope size is an
analytic bound; the implementation does not enumerate its global addresses.

A STANDARD parameter-count observation explains this preparation-only scale:
all positive normalized states on the fixed M_w-address envelope have M_w-1
continuous degrees of freedom. Exact circuits from fixed CNOT/X/H and one-
parameter Ry gates that cover that whole class need at least M_w-1 adjustable
rotation parameters in the worst case (finite circuit topologies of smaller
parameter dimension cannot cover the positive sphere). Therefore the displayed
O(M_w) total gate bound has the correct worst-case order for preparing that
entire envelope class in this exact gate model. This observation is NOT a new
parameter-counting technique, a CNOT lower bound, a lower bound for the smaller
physical circuit-derived reference family, an approximate/T-count bound, or a
lower bound on other gradient measurements. Existing general sparse-state
complexity theorems allow unknown supports; their lower bounds cannot simply
be applied to our fixed known geometric envelope [S4].

## 6. Compiler, decoder and memory costs

Write W=sum_j |I_j| and nu=max_a #{j:a in I_j}. Once local tables are supplied,
classical preparation costs O(L+W+n w2^w): table-slice sums, incidence indices,
one temporary h_a, prefix weights and fast Walsh compilation. The working
memory excluding emitted gate storage is O(L+W+n+2^w). Retaining the entire
emitted program adds O(n2^w) gate records and their precision/index bits. The
standalone study streams large programs into a counter instead; a runtime
that regenerates the stream must charge its arithmetic PER EXECUTION. Program
storage and replay are not free QRAM access.

To decode x, scan the actual n-bit string for its first and last one, a and b.
Only the at most nu intervals containing a need consideration. Reject an
interval ending before b; use the local substring to access the remaining
tangent entries. Compute the row norm, then update only its nonzero original
parameter indices with 2(-1)^b sqrt(s) k_x/||k_x||. A word-based implementation
with w-bit indices costs O(n+nu w) bit/scalar work per record, including string
checks and local address construction, with at most nu parameter updates.
After K records divide the accumulator by K and emit all P entries: O(P) work.
There is no P-dimensional temporary record or global response reconstruction.

For the existing depth-d line circuit, P=Theta(nd), w<=2d and nu=O(d^2).
The inherited causal local-tangent compiler costs O(d^2 L) scalar kernels plus
its incidence/priority-queue indexing; its measured gate-visit/kernel counts
are retained rather than hidden as a free input. Thus bounded d gives linear
preprocessing, per-record quantum/physical-bit work, and O(P) memory. For growing
d the width exponent remains. Tensor contractions may avoid table materialization
in other methods; L is not a universal decoder lower bound.

## 7. Accuracy and numerical scope

The logical estimator is exactly unbiased and has MSE at most 4s/K. The common
unchanged-sample-mean prescription K=ceil(4s/(delta epsilon^2)) suffices for
whole-vector error epsilon with confidence 1-delta by Markov. This is not an
optimal-tail theorem. Small-system exact risks are diagnostic only; simulation
knowledge of q is not supplied to the run-budget selection. Trace-risk control
does not imply constant variance for each individual coordinate: this sparse
measurement can concentrate variance, and no Abbas-style infinity-norm overhead
claim is inferred by changing the requested norm.

If the overall implemented readout unitary has operator error zeta, outcome-L1
error is at most 2zeta. With record norm <=2sqrt(s), the induced mean error is
at most 4sqrt(s)zeta. A sufficient per-gate synthesis error epsilon/(8G sqrt(s))
for G gates bounds readout bias by epsilon/2. Classical table error, numerical
imbalance, response preparation and hardware noise require additional budgets.
No fault-tolerant synthesis claim is made from arbitrary-angle logical counts.

The floating code rejects nonfinite/complex arrays and nonzero reference entries.
When using the inherited real-circuit compiler, the analytically zero reference
amplitude is set to zero after checking its residual below 1e-10; the observed
residual is recorded. Other small amplitudes are not thresholded. Squared-
amplitude underflow is rejected rather than silently discarding a direction.
These safeguards and finite checks are not a formal interval certificate.
