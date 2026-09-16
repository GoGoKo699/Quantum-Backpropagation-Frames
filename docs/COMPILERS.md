# Constructive readout circuits

[Overview](../README.md) · [Exact theorem](THEORY.md) ·
[Supported implementation](IMPLEMENTATION.md) · [Reproduction](REPRODUCIBILITY.md)

The exact theorem guarantees a measurement exists. To run it, one also needs
a circuit and a decoder whose costs are explicit. Two constructions are
available: an attaining linear-size circuit at the existing disjoint flat
point, and a bounded-risk reference compiler for overlapping interval tangents.
This page derives both. The overlap result is a supporting compiler theorem;
it does not extend exact minimax optimality to arbitrary tangents. Every
rotation below uses the full-angle convention $R_y(\theta)=\exp(-i\theta Y)$;
a conventional half-angle SDK rotation therefore receives angle $2\theta$.

## Row-norm reference readout

Use the model and symbols of [Theory](THEORY.md): real known
$T\in\mathbb R^{N\times P}$, $T^{\mathsf T}e_0=0$, real unit response $q$, and
$s=\mathrm{tr}(T^{\mathsf T}T)>0$. For the transpose $k_x\in\mathbb R^P$ of row
$x$ of $T$, define

```math
d_x=\|k_x\|_2^2,\qquad c_x=\sqrt{d_x/s},\qquad
|c\rangle=\sum_{d_x>0}c_x|x\rangle.
```

These amplitudes are known from the tangents; they do not depend on $q$.
Starting with the supplied $\Omega(q)$, apply a known preparation $A$ only when
the reference qubit is zero, where $A|0\rangle=|c\rangle$. Leave the complete
reference-one branch unchanged. A Hadamard on the reference then gives

```math
\frac12\left(|0\rangle(|c\rangle+|q\rangle)
             +|1\rangle(|c\rangle-|q\rangle)\right).
```

Measure all physical bits. For reference result $`b\in\{0,1\}`$ and system
address $x$, the probability and score on a nonzero row are

```math
p(b,x)=\frac{(c_x+(-1)^bq_x)^2}{4},\qquad
Z(b,x)=2(-1)^b\frac{k_x}{c_x}.
```

For a zero row return the zero vector. Include these records in the trial count.
Since $p(0,x)-p(1,x)=c_xq_x$, summing signed scores proves
$\mathbb E_q Z=2T^{\mathsf T}q$ for every real unit response. Every active score
has norm $2\sqrt s$. Let $`S=\{x:d_x>0\}`$, and let $\Pi_S$ project onto its
computational coordinate states. The active probability is
$`(1+\|\Pi_Sq\|_2^2)/2`$, so

```math
\mathcal R(q)=2s(1+\|\Pi_Sq\|_2^2)
                    -4\|T^{\mathsf T}q\|_2^2\le4s.
```

This derivation supplies the general upper bound in [Theory](THEORY.md).
**Coordinate-row support need not equal the tangent span.** If the number of
nonzero rows exceeds $\mathrm{rank}(T)$, the coordinate subspace contains a
unit vector $q$ with $T^{\mathsf T}q=0$. Its risk is exactly $4s$. A flat tangent
spectrum alone therefore does not make this particular reference optimal.
The theorem's singular-basis attainer and this coordinate-row construction are
different in general.

## Disjoint one-layer realization

Consider $m\ge1$ disjoint two-qubit blocks, $n=2m$ system qubits and $P=6m$
original full-angle parameters. Each block applies the ordered generators

```math
A_0=YI,\quad A_1=IY,\quad A_2=YX,\quad
A_3=XY,\quad A_4=YZ,\quad A_5=ZY,
```

with rotations $\exp(-i\theta_jA_j)$. These gates are real. If $U_{b,<j}$ is the
product of earlier gates in block $b$, cancellation of the later gates in the
reversed tangent gives

```math
t_{b,j}=\left[U_{b,<j}^{\mathsf T}(-iA_j)U_{b,<j}|00\rangle\right]
                   \otimes|0\rangle_{\text{other blocks}}.
```

The local $00$ entry vanishes because $-iA_j$ is real antisymmetric. Each column
has unit norm because $A_j^2=I$. Retain the other three local rows in
$K_b\in\mathbb R^{3\times6}$, in address order $01,10,11$. Thus

```math
s=\sum_b\|K_b\|_F^2=6m=P.
```

Each $K_b$ is computed with six prefix steps on four-dimensional matrices.
No exponentially large state or tangent matrix is needed. Global parameter
order is generator slot first, then block: index $jm+b$ for slot $j$ and block
$b$. The six entries of a row of $K_b$ always update these original coordinates.

Only addresses with one nonzero two-bit block can have nonzero tangent rows.
Their row energies and reference amplitudes are

```math
d_{b,t}=\sum_j(K_b)_{t,j}^2,\qquad
c_{b,t}=\sqrt{d_{b,t}/s}.
```

This is exactly the row-norm construction above.

### Exact optimality at the flat point

At zero angles every block has

```math
K_b=\begin{pmatrix}
0&1&0&0&0&1\\
1&0&0&0&1&0\\
0&0&1&1&0&0
\end{pmatrix},\qquad K_bK_b^{\mathsf T}=2I_3.
```

Across blocks the active computational addresses are orthogonal. Hence
$r=3m=P/2$, $\lambda=2$, and $c_x=1/\sqrt r$ on the $r$ active rows. The
coordinate-row readout now coincides with the sparse singular-basis attainer:
$L$ embeds those computational addresses and $V^{\mathsf T}=K/\sqrt2$, with
$K$ the active rows of the global $T$ in the original parameter ordering.
The exact theorem therefore gives

```math
\sup_q\mathcal R(q)=4P-8.
```

The no-mask all-X benchmark at this point has pointwise risk
$`4P-\|g(q)\|_2^2`$ and worst-case risk $4P$. The row-norm risk is smaller by
$`2P(1-\|\Pi_Sq\|_2^2)`$ pointwise. Its worst-case improvement is the constant
$8$, with ratio $4P/(4P-8)$ tending to one. This is no asymptotic runtime
advantage.

At nonzero angles the same construction stays unbiased, with the row-norm
risk formula. If all active blocks have full row rank, let $\mu_{\min}$ be the
smallest eigenvalue of the block diagonal matrix with blocks
$K_bK_b^{\mathsf T}$. Then this measurement's exact worst-case risk is

```math
B_{\mathrm{row}}=\max\{2s,\,4s-4\mu_{\min}\}.
```

To see this, fix the response's squared weight in the active support:

```math
h=\|\Pi_Sq\|_2^2,\qquad
\|T^{\mathsf T}q\|_2^2\ge\mu_{\min}h.
```

The quadratic bound is attained in a least-eigenvalue direction. The largest
risk at fixed $h$ is therefore affine in $h$; maximizing over $h\in[0,1]$ gives
the formula. Both endpoints are available because $e_0$ lies outside the support.
If rows disappear or rank is lost, the pointwise formula with the actual support remains authoritative;
$4s$ remains sufficient. Including zero eigenvalues from absent rows can make
a numerical bound conservative. No exact unequal-spectrum optimum is claimed.

### Preparing the reference with elementary gates

The reference qubit is physical site zero. In each system block the right
qubit serves initially as a marker. On reference zero, set the first marker
to one; a negative-control CNOT uses two reference X gates and one CNOT.
Let

```math
w_b=\sum_{t=1}^3d_{b,t},\qquad R_b=\sum_{j=b}^{m-1}w_j.
```

A chain of $m-1$ controlled exchanges splits this one excitation among the
block markers. The exchange between successive markers has full angle

```math
\theta_b=\mathrm{atan2}(\sqrt{R_{b+1}},\sqrt{w_b}),
```

and sends $10$ to $`\cos\theta_b\,10+\sin\theta_b\,01`$, leaving $00$ and $11$
fixed. Induction along the chain leaves marker $b$ with amplitude
$\sqrt{w_b/s}$. The ideal block mass is six; using the computed masses preserves
the weighted construction in floating arithmetic.

On block $b$, conditional on reference zero, split its local marker $01$:
first rotate the left bit conditional on the right bit being one, with

```math
\alpha_b=\mathrm{atan2}(\sqrt{d_{b,2}+d_{b,3}},\sqrt{d_{b,1}}).
```

Then rotate the right bit conditional on the left bit being one, with

```math
\gamma_b=-\mathrm{atan2}(\sqrt{d_{b,2}},\sqrt{d_{b,3}}).
```

Take $\gamma_b=0$ if both arguments vanish. Acting on $01$, these rotations
produce amplitudes proportional to
$(\sqrt{d_{b,1}},\sqrt{d_{b,2}},\sqrt{d_{b,3}})$ on $01,10,11$. Empty blocks stay
$00$. Every complete controlled block is identity on the whole reference-one
space, including arbitrary unknown responses. Individual elementary gates in
the decomposition need not be identity there; the complete block is.

Each exchange uses a CNOT, a complete two-control rotation multiplexor, then
a CNOT. The multiplexor has four CNOTs and four full-angle $R_y$ rotations;
its explicit decomposition is given below. Each local split uses one such
multiplexor. Including the final reference Hadamard, the readout counts are

```math
N_{\mathrm{CNOT}}=14m-5,\qquad N_{R_y}=12m-4,
```

plus two X gates, one H, and $n+1$ terminal measurements. No work qubit beyond
the already supplied reference is needed. Common response preparation is
separate. These are counts of this explicit sequential, all-to-all logical
circuit, not minimum counts, routed hardware costs, or logarithmic depth.

### Classical work and the one-layer boundary

Store $18m$ tangent scalars, $3m$ row energies and $O(m)$ gate records.
Preprocessing takes $O(m)$ scalar work and is repeated when parameters change.
Dense statevector routines are small-system diagnostics; they are not the
method behind this scalable compilation bound.
For each measurement record, scan the actual $n$ system bits to check that
exactly one block is nonzero, then update its signed row count. The final
contraction with all $K_b$ emits all $P$ coordinates. This costs
$O(Kn+P)$ classical work and $O(P)$ memory for $K$ trials; it is not $O(K)$ when
physical bit processing is included. The contraction itself uses $18m$
multiplications and $12m$ additions, with normalization/scaling also charged.

This selector applies to one disjoint layer. Overlapping later layers can
produce addresses with several nonzero blocks; using the same selector would
lose derivatives. The retained diagnostic includes such a four-qubit case.

The nearby-spectrum comparison is also preserved. If all six block angles
have magnitude at most $h$, column $j$, indexed from zero, changes from its
zero-angle value by at most $2jh$. The bound follows from the two occurrences
of the orthogonal prefix and $`\|U_{b,<j}-I\|\le jh`$. Summing column squares gives

```math
\|K_b-K_b(0)\|\le\sqrt{220}\,h.
```

For $h<1/\sqrt{110}$ the three singular values remain positive, between
$\sqrt2-\sqrt{220}h$ and $\sqrt2+\sqrt{220}h$. Different blocks retain disjoint
nonvacuum support. The [spectral comparison](THEORY.md#general-bounds-and-nearby-spectra)
therefore applies uniformly in the number of blocks. This stability statement
is not an unequal-spectrum minimax formula or a new circuit family.

## Overlapping interval construction

Now suppose each original tangent is supplied as a local table on an interval:

```math
t_j=\tau_j\otimes|0\rangle_{\overline{I_j}},\qquad
I_j=[l_j,r_j),\quad 1\le|I_j|\le w,\quad (\tau_j)_0=0.
```

There are $n$ ordered system sites and $P$ such tables. They are real, finite,
and may overlap; tangents need not be distinct, orthogonal, or equally
sensitive. Their total stored size is
$L_{\mathrm{tab}}=\sum_j2^{|I_j|}$. This input is charged, including its
construction when derived from a circuit.

**Constructive theorem.** From these tables one can compile a reference-zero
preparation of $`c_x=\|k_x\|_2/\sqrt s`$ using $O(n2^w)$ CNOTs and arbitrary
one-qubit rotations, no extra work qubits, and no global support-address union
or tangent eigendecomposition. The response-one branch is unchanged. The
sparse original-coordinate decoder is universally unbiased and has trace
risk at most $4s$.

The logical angles are exact real numbers in this statement. Finite synthesis,
source-table errors and hardware errors require separate budgets. The claim
concerns this preparation and readout, not the exact minimax risk for arbitrary
overlapping tangents.

### Assign each address its first nonzero site

Every nonzero physical bit string $x$ has a unique first one at a site $a$,
counting from the left. A local tangent contributes to its row only if its
interval contains every nonzero bit. Define

```math
R_a=\max\bigl(\{a+1\}\cup\{r_j:l_j\le a<r_j\}\bigr),
\qquad \ell_a=R_a-a-1\le w-1.
```

Represent all rows whose first one is $a$ by a suffix table $h_a$ of length
$2^{\ell_a}$. For each interval containing $a$, let $c_j=2^{r_j-a-1}$. The
local table entries whose first one occurs there are precisely the slice
$\tau_j[c_j:2c_j]$, using big-endian local addresses. Square these entries and
add them to $h_a$ at stride $2^{R_a-r_j}$. The stride pads zeros beyond that
interval's right endpoint. Therefore the resulting table satisfies

```math
h_a(z)=\sum_j(t_j)_x^2=d_x
```

for the unique string with zeros before $a$, a one at $a$, suffix $z$, and zeros
after $R_a$. Squares are summed before taking the square root; coherently
adding tangent amplitudes would produce a different reference.

Let $\mu_a=\sum_z h_a(z)$. These first-site sectors are disjoint and cover every
nonzero row, giving $\sum_a\mu_a=s$. Each nonzero local table address occurs in
exactly one first-site slice. All sector masses can thus be constructed in
$O(L_{\mathrm{tab}}+W+n)$ work, where $W=\sum_j|I_j|$ counts interval incidences.
One can form, compile and discard each $h_a$ separately. This avoids storing a
global union of $n$-bit addresses; it does not eliminate the local $2^w$ work.

### Prepare markers, then fill suffixes from right to left

On the reference-zero branch, set system site zero to one. A chain of $n-1$
controlled exchanges, of the same kind as above, prepares

```math
\sum_{a=0}^{n-1}\sqrt{\mu_a/s}\,|e_a\rangle,
```

where $e_a$ denotes the physical bit string with just site $a$ set. Each exchange
uses angle $\mathrm{atan2}(\sqrt{\sum_{b>a}\mu_b},\sqrt{\mu_a})$; sectors with
zero mass use the limiting angles. A completely zero remaining tail has no
amplitude and may use angle zero.

Process markers in descending order $a=n-1,\ldots,0$. If $\mu_a>0$, conditional
on reference zero and marker $a$ being one, prepare

```math
\sum_{z\in\{0,1\}^{\ell_a}}
       \sqrt{h_a(z)/\mu_a}\,|z\rangle
```

on the next $\ell_a$ sites. To prove this control suffices, consider each branch
just before processing $a$:

- An original marker $b<a$ has not yet been filled, so its bit at $a$ is zero.
- An original marker $b>a$ was filled only to the right of $b$, so its bit at
  $a$ is still zero.
- The branch with marker $a$ has an all-zero suffix and is the only branch
  on which the control fires.

Later operations at smaller markers cannot disturb this completed branch,
because its bits to the left remain zero. This induction proves that the
amplitude finally assigned to each physical string is
$\sqrt{\mu_a/s}\sqrt{h_a(z)/\mu_a}=\sqrt{d_x/s}$. The complete reference-one branch
is identity throughout. Reversing the processing order is generally invalid:
new suffix ones can trigger later marker controls. A retained three-qubit
counterexample and full gate-execution checks enforce this order.

### Compile every multiple control

A positive suffix state is prepared bit by bit from binary-prefix masses.
For suffix bit $j$, split each prefix's remaining mass into its next-zero and
next-one masses, say $m_0$ and $m_1$. A full-angle rotation
$\mathrm{atan2}(\sqrt{m_1},\sqrt{m_0})$ creates that split. There are $j+2$
controls: the $j$ earlier suffix bits, the marker, and the reference. Only
marker-one/reference-zero entries of the angle table are nonzero. Unreachable
zero-mass prefixes may use angle zero.

For completeness, an angle table $\theta_b$ for $k\ge1$ controls can be compiled
without leaving any implicit multi-controlled gate. Let $M=2^k$ and let $g_j$ be the cyclic Gray labels, computed as
`j xor (j >> 1)` for $j=0,\ldots,M-1$. Set

```math
\alpha_j=\frac1M\sum_{b=0}^{M-1}
                (-1)^{g_j\cdot b}\theta_b.
```

Here the dot product is binary parity, and the first listed control is the
least significant bit of the angle-table index. Emit $R_y(\alpha_j)$ on the
target followed by a CNOT from the one control that changes between $g_j$ and
$g_{j+1}$, including the final cycle back to $g_0$. For a fixed control string,
$XR_y(\alpha)X=R_y(-\alpha)$ makes the net angle the inverse Walsh sum,
$\theta_b$. The closed cycle cancels the final X parity. Thus there is no
unaccounted diagonal or terminal permutation.

This gives $M$ CNOTs and $M$ rotations per complete multiplexor. The coefficients
are computed with a fast Walsh transform in $O(k2^k)$ arithmetic, rather than
forming a dense Walsh matrix. In particular, a two-control multiplexor costs
four CNOTs and four rotations, as used for each controlled exchange.

Let $`A=\{a:\mu_a>0\}`$ and

```math
F=\sum_{a\in A}4(2^{\ell_a}-1).
```

Summing $2^{j+2}$ over each suffix's bits and adding marker preparation gives
exact emitted counts

```math
N_{\mathrm{CNOT}}=6n-5+F,\qquad
N_{R_y}=4(n-1)+F.
```

There are also two X gates, one final H and $n+1$ terminal measured bits.
There are no additional work qubits, intermediate measurements or resets.
Zero-angle rotations may remain in the emitted program. Connectivity is
all-to-all and arbitrary rotations are logical primitives; no routed-device
or depth advantage is asserted.

The envelope of all nonzero addresses whose first and last ones fit in a
interval of width $w$ has size

```math
M_w=\sum_{a=0}^{n-1}2^{\min(w-1,n-a-1)}
   =(n-w+2)2^{w-1}-1.
```

Consequently

```math
N_{\mathrm{CNOT}}\le4M_w+2n-5,\qquad
N_{R_y}\le4M_w-4.
```

These bounds are $O(n2^w)$ and $O(M_w)$, uniformly for $1\le w\le n$.
The implementation uses the formula as a bound; it does not enumerate the
whole envelope.

The preserved parameter-count observation applies only to preparing every
positive normalized state on this fixed envelope. That family has $M_w-1$
continuous degrees of freedom, so exact circuits built from fixed CNOT/X/H
and one-parameter rotations need at least $M_w-1$ adjustable rotation
parameters in the worst case. For each finite gate topology, a smaller-dimensional smooth
parameterization has measure-zero image in this state family. The countable
union over finite topologies still cannot cover it. This establishes the
preparation-only worst-case order. It is not a CNOT lower bound, an approximate synthesis bound,
a bound for the smaller physically generated tangent family, or a lower bound
on other gradient measurements. General sparse-state results with unknown
supports have different hypotheses.

### Decoder, source tables and program memory

Let $`\nu=\max_a\#\{j:a\in I_j\}`$. Once the local tables are supplied, the
classical compiler takes

```math
O(L_{\mathrm{tab}}+W+n w2^w)
```

arithmetic/index work, including sector sums, incidence tables, prefix masses,
and fast Walsh transforms. Working memory, excluding emitted program storage,
is $O(L_{\mathrm{tab}}+W+n+2^w)$.

Keeping the whole program adds $O(n2^w)$ gate records with their angle precision
and site-index bits. A compiler-only counter can consume a stream with much less
storage, but replaying a discarded program requires regeneration and charges
that arithmetic for **each execution**. Neither program storage nor regeneration
is free quantum memory access.

To decode a physical result, first scan its $n$ system bits for the first and
last ones, $a$ and $z$. Only intervals containing $a$ can contribute. Reject any
that end before the last one; use the substring in each remaining interval to
read its tangent entry. These entries give $k_x$ and its norm. Update the original
parameter indices by $`2(-1)^b\sqrt s\,k_x/\|k_x\|_2`$, where $b$ is the reference
bit, or make no update when the row is zero. The reference bit must not be
confused with the position of the last system one.

A word implementation with local indices of width $w$ uses $O(n+\nu w)$ bit/scalar
work and at most $\nu$ parameter updates per record. After all $K$ records,
divide the $P$-entry accumulator by $K$ and emit every coordinate, including
zero ones. No dense $P$-vector is allocated per shot, and no response is
reconstructed classically.

For the existing line circuit of depth $d$, $P=\Theta(nd)$, $w\le2d$ and
$\nu=O(d^2)$. Constructing the local tangent tables with the retained causal
compiler costs $O(d^2L_{\mathrm{tab}})$ scalar kernels plus incidence and
priority-queue indexing; actual gate-visit and kernel counts are recorded.
With fixed depth these quantities are linear in system size. For growing
depth, the width exponent remains. Table size is an output requirement of
this representation, not a universal classical lower bound: other methods
may contract tensors without materializing all tables.

## Precision and numerical limits

The exact logical row-norm estimator has mean-squared error at most $4s/K$.
The sufficient fixed sample-mean budget
$K=\lceil4s/(\delta\varepsilon^2)\rceil$ follows from Markov's inequality for
whole-vector error $\varepsilon$ and failure probability $\delta$. This is
not an optimal-tail theorem, and a smaller diagnostic risk computed using a
known simulated $q$ is not automatically a usable budget for an unknown
experimental response. Trace-risk control does not assert constant variance
for each original coordinate or an infinity-norm gradient guarantee.

If the implemented readout unitary differs from its ideal by operator norm
at most $\zeta$, the outcome distributions differ in L1 norm by at most
$2\zeta$. Scores have norm at most $2\sqrt s$, so the resulting mean error is
at most $`4\sqrt s\,\zeta`$. For $G_{\mathrm{gates}}$ elementary gates, bounding
each gate's operator error by

```math
\frac{\varepsilon}{8G_{\mathrm{gates}}\sqrt s}
```

suffices for readout bias at most $\varepsilon/2$ by the telescoping unitary
error bound. A complete accuracy budget must also allocate error to sampling,
classical tables, response preparation and hardware. Arbitrary-angle logical
gate counts are not fault-tolerant synthesis counts.

The supported floating implementation checks real, finite, shape and count
contracts; see [Implementation](IMPLEMENTATION.md) for its exact interface.
For inherited circuit-derived local tables, the analytically zero reference
entry is set to zero only after checking that its residual is below $10^{-10}$,
and the residual is recorded. Other small entries are not thresholded away.
Squared-amplitude underflow is rejected rather than silently losing a tangent
direction. Floating safeguards and numerical eigenvalues are not formal
interval certificates.

## Sources and evidence

The original [disjoint construction](../results/PF-06/PROOF.md) and
[overlapping-interval proof](../results/PF-07/PROOF.md) remain unchanged.
Their [disjoint source notes](../results/PF-06/SOURCE_NOTES.md) and
[interval source audit](../results/PF-07/SOURCE_AUDIT.md) attribute the established
W-state, Gray-code rotation and sparse-preparation ingredients. These
constructions do not claim those primitives as new.

The [evidence index](EVIDENCE.md) maps each claim to implementations, tests,
source hashes and cost records. The [comparison page](COMPARISONS.md) explains
why a measurement's variance and its total computational work are different
comparisons, and preserves the fixed negative acceptance record.
