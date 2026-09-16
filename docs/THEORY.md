# Exact single-copy readout limit

[Overview](../README.md) · [Worked tutorial](TUTORIAL.md) ·
[Constructive circuits](COMPILERS.md) · [Comparisons and limitations](COMPARISONS.md)

A reference arm interferes with an unknown real response. One measurement
record receives a signed vector score, and averaging records estimates every
original gradient coordinate. This page proves the exact best worst-case
single-copy variance when the tangent matrix has equal nonzero singular values.
The proof allows every fixed measurement of the supplied copy, including
ancillas and randomly chosen settings.

## The experiment and its notation

The system has dimension $N$; for an $n$-qubit system, $N=2^n$.
Write $e_0=|0\rangle$ for its computational reference state. There are $P$
original real parameters. Their known tangent matrix is
$T\in\mathbb R^{N\times P}$, with columns $t_j$, and

```math
T^{\mathsf T}e_0=0,\qquad
G=T^{\mathsf T}T,\qquad s=\mathrm{tr}(G)>0.
```

The unknown response $q\in\mathbb R^N$ has unit norm. Each experiment receives
one supplied copy of

```math
|\Omega(q)\rangle=\frac{|a\rangle+|b_q\rangle}{\sqrt2},
\qquad |a\rangle=|0\rangle|0\rangle,\quad
|b_q\rangle=|1\rangle|q\rangle.
```

The first register is a reference qubit. The target is the full classical
$P$-vector

```math
g(q)=2T^{\mathsf T}q.
```

The relative phase between the two arms is supplied: $q$ and $-q$ are
distinguishable in this family. Access to an isolated $|q\rangle$ without that
reference is a different task. The theorem prices one supplied copy; constructing
it and any additional coherent oracle access require separate accounting.

For the circuit application, let $U(\theta)$ be a real orthogonal circuit,
$\psi=U(\theta)e_0$, and $J$ the matrix of derivatives of $\psi$ in the original
angle coordinates. If the observable $O$ is real Hermitian and unitary, set
$T=U^{\mathsf T}J$ and $q=U^{\mathsf T}O\psi$. Normalization gives
$T^{\mathsf T}e_0=0$, and differentiating $\psi^{\mathsf T}O\psi$ gives the target
above. This example explains the gradient interpretation; the statistical
result below quantifies over **every** real unit $q$, including responses not
reachable from a particular restricted observable family.

## The exact theorem and its quantifiers

A measurement is a positive-operator-valued measure (POVM) $E$: each effect is
positive and all effects sum, or integrate, to identity. Outcome $\omega$
receives a real vector score $Z(\omega)\in\mathbb R^P$. Both the measurement and
its decoder may depend on the known $T$, but are fixed independently of $q$.
The requirements are

```math
\mathbb E_q Z=g(q)\quad\text{for every real unit }q,
\qquad \mathbb E_q\|Z\|_2^2<\infty.
```

A random setting and its result together form one POVM outcome. **Only the
complete experiment must be unbiased.** Unbiasedness conditional on each
setting is not imposed. Ancillas, general joint operations on the supplied
registers, and continuous outcome spaces are allowed.

For such a measurement define its trace risk and the minimax value by

```math
\mathcal R_{E,Z}(q)
 =\mathrm{tr}\,\mathrm{Cov}_q(Z)
 =\mathbb E_q\|Z-g(q)\|_2^2,
```

```math
\mathcal V(T)=\inf_{(E,Z)\text{ satisfying the requirements}}
                 \ \sup_{q\in\mathbb R^N,\ \|q\|_2=1}
                    \mathcal R_{E,Z}(q).
```

**Theorem.** Suppose the $r\ge1$ nonzero eigenvalues of $G$ all equal
$\lambda>0$. Then

```math
\boxed{\mathcal V(T)=\lambda\max\{2r,\,4(r-1)\}.}
```

A single joint POVM with at most $2r+1$ effects attains this value and returns all
$P$ original coordinates. The outcome count is a sufficient upper bound, not a
minimality theorem or a bound on circuit synthesis cost.

The theorem concerns real pure responses, one copy, finite second moments,
universal unbiasedness, and whole-vector trace risk. It is not a local Fisher
bound, an optimum over biased estimators, a collective multi-copy theorem, or
an exact high-confidence sample complexity. Those distinctions are discussed
in [Comparisons](COMPARISONS.md).

## Reduction to real effects and finite moments

Only the occupied space matters:

```math
\mathcal H_0=\mathrm{span}\{a,b_{e_0},\ldots,b_{e_{N-1}}\}.
```

Compressing effects to this space preserves all probabilities and scores. For
a Hermitian positive effect $E$, its entrywise real part is real symmetric and
positive. Indeed its quadratic form is nonnegative on real vectors; for a
complex vector $u+iv$, the quadratic form of this real symmetric matrix is the
sum of its forms on $u$ and $v$. Taking real parts also preserves completeness
and every probability on real $\Omega(q)$. It therefore preserves every score
moment. Complex physical operations cannot evade a lower bound proved for real
effects here.

For continuous outcomes, use the scalar measure $\mu=\mathrm{tr}(E)$ on this
finite-dimensional occupied space. The density of $E$ with respect to $\mu$ is
a positive matrix, so it admits rank-one refinement. Retain the original score
on each refined outcome. All sums below then mean integrals when needed.

Moment operators are well defined on the whole occupied space: the sum of
model densities at $q=\pm e_x$, for all $x$, is

```math
\sum_{x=0}^{N-1}\left(\rho_{e_x}+\rho_{-e_x}\right)
 =N|a\rangle\langle a|+\sum_x|b_{e_x}\rangle\langle b_{e_x}|,
```

which is strictly positive there. Finiteness of the score's second moment at
these finitely many allowed responses consequently controls every matrix
entry of the second-moment operator. First moments follow by Cauchy–Schwarz.

## First lower bound: the zero-signal response

For coordinate $j$ define operators on $\mathcal H_0$ by

```math
M_j=\int Z_j\,dE,\qquad Q_j=\int Z_j^2\,dE.
```

In the decomposition $\mathbb R a\oplus\mathbb R^N$, denote the reference
entry by $\alpha_j$, the off-diagonal vector by $m_j$, and the symmetric
response block by $B_j$. Unbiasedness says

```math
\tfrac12\left(\alpha_j+2m_j^{\mathsf T}q
                         +q^{\mathsf T}B_jq\right)=2t_j^{\mathsf T}q.
```

Subtract the equation at $-q$: $m_j=2t_j$. Add the two equations:
$q^{\mathsf T}B_jq=-\alpha_j$ on the entire unit sphere. A real symmetric
quadratic form constant on that sphere is a scalar multiple of identity. Thus

```math
M_j=\begin{pmatrix}
\alpha_j&2t_j^{\mathsf T}\\
2t_j&-\alpha_j I_N
\end{pmatrix}.
```

The operator moment inequality is $Q_j\succeq M_j^2$. For a discrete POVM,
the map $\mathcal W v=(\sqrt{E_\omega}v)_\omega$ is an isometry. Let $D_j$
multiply the outcome component by $Z_j(\omega)$. Then

```math
Q_j-M_j^2
 =\mathcal W^*D_j(I-\mathcal W\mathcal W^*)D_j\mathcal W\succeq0.
```

The integral dilation gives the same identity for continuous outcomes, with
the finite moments justified above. This is established moment-inequality
machinery, included explicitly so the argument is self-contained.

At the allowed response $q=e_0$ the target is zero, since
$T^{\mathsf T}e_0=0$. Squaring the block matrix gives

```math
\langle\Omega(e_0)|M_j^2|\Omega(e_0)\rangle
 =\alpha_j^2+2\|t_j\|_2^2.
```

Summing over the original $P$ coordinates proves

```math
\mathcal R_{E,Z}(e_0)\ge2s.
```

This lower bound holds for every admissible $T$, without equal singular values.
In the theorem's setting, $s=r\lambda$, so it supplies $2r\lambda$.

## Second lower bound: the signed tangent axes

Factor the equal-spectrum matrix as

```math
T=\sqrt\lambda\,L V^{\mathsf T},\qquad
L^{\mathsf T}L=V^{\mathsf T}V=I_r,\qquad L^{\mathsf T}e_0=0.
```

Here $L\in\mathbb R^{N\times r}$ describes orthonormal state-space directions
and $V\in\mathbb R^{P\times r}$ embeds them in the original parameter space.
There may be more parameters than independent tangent directions. Projecting
any estimator orthogonally onto the range of $V$ preserves its mean and cannot
increase its squared error. It is therefore enough for this lower bound to
use $r$ scores with target $2\sqrt\lambda L^{\mathsf T}q$.

Refine the real POVM to effects $|v_\omega\rangle\langle v_\omega|$, retaining
its scores $z_\omega\in\mathbb R^r$. If $u_i=Le_i$, put

```math
x_\omega=\langle a|v_\omega\rangle,\qquad
(y_\omega)_i=\langle b_{u_i}|v_\omega\rangle.
```

Completeness and the off-diagonal first-moment constraints give

```math
\sum_\omega x_\omega^2=1,\qquad
\sum_\omega\|y_\omega\|_2^2=r,
```

```math
\sum_\omega x_\omega z_\omega^{\mathsf T}y_\omega
 =2r\sqrt\lambda.
```

Define

```math
A=\sum_\omega x_\omega^2\|z_\omega\|_2^2,\qquad
B=\sum_\omega\|y_\omega\|_2^2\|z_\omega\|_2^2.
```

Cauchy–Schwarz with vector factors $x_\omega z_\omega$ and $y_\omega$ gives
$(2r\sqrt\lambda)^2\le Ar$. Using the scalar factors $x_\omega$ and
$z_\omega^{\mathsf T}y_\omega$, followed by
$(z_\omega^{\mathsf T}y_\omega)^2\le\|z_\omega\|_2^2\|y_\omega\|_2^2$, gives
$(2r\sqrt\lambda)^2\le B$. Hence

```math
A\ge4r\lambda,\qquad B\ge4r^2\lambda.
```

Average the risk over the $2r$ valid pure responses $q=\pm u_i$. Their average
density has reference weight $1/2$ and weight $1/(2r)$ on each $b_{u_i}$.
Every constituent target has squared norm $4\lambda$. Its average risk is
therefore

```math
\frac{A+B/r}{2}-4\lambda\ge4(r-1)\lambda.
```

A supremum over all responses is at least this finite-ensemble average. This
use of an ensemble proves a bound for the original pure-state model; it does
not replace that model by one whose unknown input may be an arbitrary mixture.
Combining both mechanisms proves

```math
\mathcal V(T)\ge\lambda\max\{2r,4(r-1)\}.
```

## Sparse measurement attaining the bound

For each $i\in\{1,\ldots,r\}$ and $\sigma\in\{-1,+1\}$ define

```math
|\phi_{i,\sigma}\rangle
 =|a\rangle+\sigma\sqrt r\,|b_{u_i}\rangle,
\qquad E_{i,\sigma}=\frac{|\phi_{i,\sigma}\rangle
                              \langle\phi_{i,\sigma}|}{2r}.
```

Add the complementary effect

```math
E_*=I-|a\rangle\langle a|
       -\sum_{i=1}^r|b_{u_i}\rangle\langle b_{u_i}|.
```

The first effects are positive by construction. Their pairwise sums cancel
the cross terms, and their total is the projector subtracted in $E_*$. Thus
all effects are positive and sum to identity. The score is

```math
Z_{i,\sigma}=2\sigma\sqrt{r\lambda}\,Ve_i,
\qquad Z_*=0.
```

These are $P$-entry vectors in the original coordinates. One record contributes
a known vector, possibly to several original coordinates; measuring each
coordinate separately is unnecessary.

Write $z=L^{\mathsf T}q$. Born's rule gives

```math
p(i,\sigma\mid q)=\frac{(1+\sigma\sqrt r\,z_i)^2}{4r},
\qquad p(*\mid q)=\frac{1-\|z\|_2^2}{2}.
```

Since $p(i,+\mid q)-p(i,-\mid q)=z_i/\sqrt r$, summing scores yields
$\mathbb E_q Z=2\sqrt\lambda Vz=g(q)$. The active probability is
$(1+\|z\|_2^2)/2$, and each active score has squared norm $4r\lambda$. Subtracting
the squared mean gives the pointwise risk

```math
\mathcal R(q)=2r\lambda+(2r-4)\lambda\|L^{\mathsf T}q\|_2^2.
```

Both endpoints of $\|L^{\mathsf T}q\|_2^2\in[0,1]$ are possible: take
$q=e_0$ or $q=u_1$. The maximum is $2\lambda$ for $r=1$, $4\lambda$ for $r=2$,
and $4(r-1)\lambda$ for $r\ge3$. This matches the lower bound and proves the
theorem.

**Zero outcomes count.** For $K$ trials, divide the sum of all scores by $K$,
including trials with score zero. Discarding complementary outcomes and
renormalizing divides the mean by the unknown active probability and generally
introduces bias. For example, if $\|z\|_2^2=1/4$, that probability is $5/8$.

A decoder may accumulate $r$ signed channel counts $C_i=N_{i,+}-N_{i,-}$ and
then return

```math
\widehat g=\frac{2\sqrt{r\lambda}}K\,VC.
```

This explicitly recovers all original coordinates, including redundant ones.
Given labeled outcomes, accumulation takes $O(K)$ updates. A generic dense $V$
requires $O(Pr)$ storage and final arithmetic, plus $P$ output writes. Physical
measurement-bit processing is an additional cost when labels must be decoded.

## Physical realization and its cost boundary

An isometry on the active input space is specified by

```math
W|a\rangle=\frac1{\sqrt{2r}}\sum_i(|i,+\rangle+|i,-\rangle),
```

```math
W|b_{u_i}\rangle=\frac{|i,+\rangle-|i,-\rangle}{\sqrt2}.
```

Its columns have unit norm and are mutually orthogonal. Send the orthogonal
input complement isometrically to a separate sector. Measuring the output
basis and grouping all complementary results implements exactly the effects
above. Multiple physical failure outcomes may be grouped into the one effect
$E_*$.

This proves existence of a physical measurement. It does not supply inexpensive
access to the tangent basis. Generic $L$ and $V$ require $Nr$ and $Pr$ real
entries to describe; constructing those data, synthesizing $W$, reference
splitting, ancilla routing, and decoding must be counted. The
[disjoint-block construction](COMPILERS.md#disjoint-one-layer-realization)
implements the attainer in linear size at an existing flat circuit point,
using known local reference amplitudes instead of a supplied singular-basis
oracle.

## General bounds and nearby spectra

For arbitrary admissible $T$, the zero-signal argument gives $2s$ and the
[row-norm measurement](COMPILERS.md#row-norm-reference-readout) gives $4s$:

```math
2s\le\mathcal V(T)\le4s.
```

The upper bound also follows from the preserved full-quadratic-mask estimator.
The bracket is about this one-copy unbiased model, not unrestricted estimation.

If the nonzero eigenvalues of $G$ lie in $[\lambda_-,\lambda_+]$ with
$\lambda_->0$, let $D$ contain their positive square roots and write
$T=LDV^{\mathsf T}$. Applying $D^{-1}V^{\mathsf T}$ to any unbiased output gives
an unbiased output for target $2L^{\mathsf T}q$. For each realized error,
projection and the minimum singular value give

```math
\|Z-g\|_2^2\ge\lambda_-\,
 \|D^{-1}V^{\mathsf T}(Z-g)\|_2^2.
```

Conversely, apply $VD$ to the unit-spectrum attaining estimator. Its squared
error grows by at most $\lambda_+$. Taking risks and extrema yields

```math
\lambda_-\max\{2r,4(r-1)\}\le\mathcal V(T)
 \le\lambda_+\max\{2r,4(r-1)\}.
```

This is a comparison bound, not an exact unequal-spectrum solution. Coordinate
columns need not be independent or orthogonal.

## Repeated copies and what the theorem leaves open

For $K$ independent copies measured with the same fixed unbiased protocol,
$\widehat g=K^{-1}\sum_{k=1}^K Z_k$ has

```math
\mathbb E_q\|\widehat g-g(q)\|_2^2=\frac{\mathcal R(q)}K.
```

If $B$ bounds its single-copy risk uniformly, Markov's inequality gives the
sufficient guarantee

```math
K\ge\frac{B}{\delta\varepsilon^2}
\quad\Longrightarrow\quad
\Pr_q\{\|\widehat g-g(q)\|_2>\varepsilon\}\le\delta.
```

Here $\varepsilon>0$ is whole-vector Euclidean error and $0<\delta<1$ is failure
probability. This conversion is sufficient, not an exact optimum for tails or
sample complexity. It proves no lower bound against arbitrary biased,
adaptive, collective, or extra-coherent-access algorithms. For example, the
biased zero estimator has worst squared error $4\lambda$ in the equal-spectrum
model. The all-POVM theorem does not rule it out under a different contract.

The exact result and constructions have internal proofs and regression evidence.
Final novelty clearance and a strongest-method end-to-end advantage remain
unestablished. The separate [comparison route](COMPARISONS.md) preserves the
negative acceptance evidence and the narrower phase/Walsh estimator class.

## Sources and evidence

This canonical proof consolidates the unchanged
[original derivation](../results/PF-04/PROOF.md) and
[independent internal audit with sparse attainer](../results/PF-05/PROOF_AUDIT.md).
The [frozen result synopsis](../results/PF-08/CORE_RESULT.md) specifies its scope.
The [source audit](../results/PF-05/SOURCE_AUDIT.md) records exact primary-source
versions and the distinction from local quantum estimation. In particular,
the moment inequality is established estimation machinery; neither it nor
measurement dilation is claimed as a new primitive.

Proof, implementation, tests, immutable source hashes and limitations are mapped
in the [evidence index](EVIDENCE.md). The source records support attribution;
citing a paper does not confer permission to redistribute its contents.
