# PF-04: single-copy unbiased gradient readout

Internal derivation, 2026-09-15. These statements concern measurement statistics,
not the circuit cost of an optimal measurement, unrestricted coherent oracles,
biased estimators, or novelty. Source relationships are in SOURCE_AUDIT.md.

## 1. Contract

Let T be a known real N by P matrix with T[0,:]=0 and s=tr(T^T T)>0.
The unknown vector q ranges over the entire real unit sphere in R^N. One copy
of the supplied state is

```math
|\Omega(q)\rangle=(|a\rangle+|b_q\rangle)/\sqrt2,
\quad |a\rangle=|0,0\rangle,\quad |b_q\rangle=|1\rangle|q\rangle.
```

The requested classical vector is g(q)=2 T^T q. A measurement/decoder may
depend on T, not on q. Arbitrary joint POVMs, ancillas, and recorded classical
randomization are permitted. Only the complete measurement is required to be
unbiased for every q; a random setting need not be unbiased separately. Require
finite second moments. Write

```math
\mathcal V(T)=\inf_{(E,Z):\ \mathbb E_q Z=2T^{\mathsf T}q\ \forall q}
\sup_{\|q\|=1}\mathrm{tr}\,\mathrm{Cov}_q(Z).
```

Every experiment receives just this copy. Extra oracle calls, a differently
prepared oracle experiment, multi-copy collective measurements, or an estimator
whose coefficients depend on previous unknown-state data are not covered by the
one-copy optimum. Randomization independent of q is part of the POVM outcome.

Compression to H0=span(a,b_0,...,b_{N-1}) loses no probabilities. Since the model
is real, replacing each Hermitian effect by its entrywise real part preserves
positivity, normalization, probabilities, and all score moments. Thus real
symmetric effects suffice even when arbitrary complex operations were allowed.
Finite moments on all model states imply finite moments on this occupied space:
the sum of densities for q=+/-e_x is strictly positive there.

## 2. First moments and the general lower bound

For coordinate j let M_j=int Z_j dE and Q_j=int Z_j^2 dE on H0. Comparing q and
-q in the unbiasedness identity forces

```math
M_j=\begin{pmatrix}\alpha_j&2t_j^{\mathsf T}\\2t_j&-\alpha_j I_N\end{pmatrix}.
```

Indeed the odd part determines the off-diagonal block, and a quadratic form
constant on the unit sphere must be a scalar multiple of identity.

The operator moment inequality Q_j >= M_j^2 is standard (S1, Eq. 175). A direct
proof uses the isometry V: v -> (sqrt(E_w)v)_w. If D is the diagonal operator
with entries Z_j(w), then M=V^*DV, Q=V^*D^2V and
Q-M^2=V^*D(I-VV^*)DV>=0. Integrals follow by the same dilation argument.

At q=e_0 the mean is zero and

```math
\langle\Omega(e_0)|M_j^2|\Omega(e_0)\rangle
=\alpha_j^2+2\|t_j\|^2.
```

Consequently every admissible vector decoder obeys

```math
\mathrm{tr}\,\mathrm{Cov}_{e_0}(Z)\ge 2s.
```

The retained full-quadratic-mask estimator supplies
Sigma(q)=4 T^T diag(1-q_x^2) T and worst-case trace 4s. Hence

```math
2s\le\mathcal V(T)\le4s.                         \tag{A}
```

This is a direct application of existing moment inequalities to this reference
family, not a proposed new quantum Cramer-Rao principle.

## 3. Exact theorem for equal nonzero singular values

Suppose T=sqrt(lambda) U V^T, where U and V have r orthonormal columns,
U^T e_0=0, and lambda>0. Parameter columns need not be orthogonal: P can exceed r.
Orthogonally projecting the returned vector onto range(V) cannot increase
squared error. Work in the r output coordinates with target
2 sqrt(lambda) U^T q.

**Theorem.** For the contract in section 1,

```math
\mathcal V(T)=\lambda\max\{2r,4(r-1)\}.           \tag{B}
```

### Lower bound from two different response ensembles

Section 2 supplies 2r lambda. To obtain the other term, refine a real POVM to
rank-one effects |v_w><v_w|, retaining the same decoded vector on refined
outcomes. Continuous outcomes work with integrals; refinement is solely a proof
device, not an assertion of efficient physical implementation.

Write x_w=<a|v_w>, y_w=(<b_{u_i}|v_w>)_i, and let z_w be its r-dimensional score.
Completeness implies sum x_w^2=1 and sum ||y_w||^2=r. The required first moments
imply

```math
\sum_w x_w\,z_w\!\cdot y_w=2r\sqrt\lambda.
```

Define A=sum ||z_w||^2 x_w^2 and B=sum ||z_w||^2 ||y_w||^2. Cauchy-Schwarz, used
once with the y norm and once with the x norm, gives

```math
A\ge4r\lambda,\qquad B\ge4r^2\lambda.
```

Average the risk over the 2r valid responses q=+/-u_i. Their averaged state is
( |a><a| + r^{-1} sum_i |b_{u_i}><b_{u_i}| )/2. Every one has squared target norm
4 lambda. Thus the averaged risk is (A+B/r)/2-4 lambda, at least
4(r-1)lambda. A worst-case risk is at least each of these two lower bounds.
No local asymptotic expansion or prior-dependent measurement is used.

### Finite POVM attaining both bounds

Let ell=ceil(log2(r)), m=2^(ell+1), and choose distinct labels L_i in F_2^(ell+1)
whose first bit is one. For y in F_2^(ell+1) put c_i(y)=(-1)^(L_i dot y).
Their means and all triple products vanish; their pair products average to
delta_ij. This is ordinary character orthogonality, not a full design claim.

Set

```math
|v_y\rangle=|a\rangle+\sum_{i=1}^r c_i(y)|b_{u_i}\rangle,
\quad E_y=m^{-1}|v_y\rangle\langle v_y|,
\quad E_*=I-\Pi_{\mathrm{span}(a,b_{u_1},...,b_{u_r})}.
```

All effects are positive and sum to identity. The returned P-vector is
Z_y=2 sqrt(lambda) V c(y) for an active outcome and Z_*=0 otherwise. The character
moments imply exactly E_q Z=g(q). This is a jointly measurable vector estimator;
it does not assemble incompatible single-coordinate measurements.

Write z=U^T q. Active outcomes have total probability (1+||z||^2)/2, but the
estimator is never conditioned or renormalized by that probability. Its score
norm is exactly 2 sqrt(r lambda) on active outcomes, giving

```math
\mathrm{tr}\,\mathrm{Cov}_q(Z)
=2r\lambda+(2r-4)\lambda\|z\|^2.                \tag{C}
```

For r=1 the maximum is at z=0; for r=2 it is constant; for r>=3 it is at ||z||=1.
This proves (B). The construction has m+1<=4r+1 outcomes, not 2^r outcomes.
It preserves the complete P-entry output through V. It does NOT give a free
circuit for mapping the known tangent basis U into outcome labels.

## 4. Near-flat spectra and a check inside the existing circuit family

If the nonzero squared singular values lie in [lambda_-,lambda_+], then

```math
\lambda_-\max\{2r,4(r-1)\}\le\mathcal V(T)
\le\lambda_+\max\{2r,4(r-1)\}.                 \tag{D}
```

For the lower bound, transform any unbiased output into unweighted singular
coordinates and use the minimum singular value to compare squared errors.
For the upper bound use the POVM above and rescale its output by the actual
singular values. Thus no assumption that coordinate tangents are orthogonal is
needed. Formula (D) is not an exact anisotropic minimax formula.

For n even, one layer of the existing disjoint two-qubit six-generator blocks
has P=3n parameters. At all angles zero, each block's three nonzero computational
tangents is repeated twice. Blocks have disjoint nonvacuum support, so
r=3n/2 and every nonzero eigenvalue is lambda=2. Therefore

```math
\mathcal V(T)=4P-8,\quad
\mathcal V_{\mathrm{frame/Walsh}}(T)=4P.         \tag{E}
```

This is not a new ansatz. Each full-angle coordinate tangent has norm one; s=P.
There is a nonzero-signal maximizer (q in the tangent subspace), not just a zero
gradient witness.

The conclusion is stable on an n-independent parameter box. For a single block,
if all six angles have magnitude <=h, then the j-th reversed tangent differs
from its zero-angle value by at most 2jh (j=0,...,5). Thus
||T_block-T_block(0)||op <=sqrt(220)h. Its three nonzero singular values lie
between sqrt(2)-sqrt(220)h and sqrt(2)+sqrt(220)h. If h<1/sqrt(110) they remain
positive. Different blocks remain orthogonal after ordinary circuit reversal.
Formula (D) then applies globally with
lambda_+/-=(sqrt(2)+/-sqrt(220)h)^2 and the same rank r.

For large r, the full-mask upper bound is at most
r/(r-1)/(1-sqrt(110)h)^2 times the unrestricted unbiased optimum. No growing
statistical advantage over frame/Walsh readout is available in this region.

## 5. Accuracy, computation, and novelty boundaries

For K i.i.d. copies measured by the same fixed unbiased protocol, the mean has
MSE=V(q)/K. K>=V_max/(delta epsilon^2) is a sufficient high-probability budget.
Theorems (A)-(E) are NOT exact confidence-sample-complexity lower bounds. They
also do not establish a minimax value for arbitrary biased multi-copy procedures.
For example, the biased zero estimator has worst squared error 4 lambda_max,
which can be much smaller than a one-copy unbiased risk when r is large.

The optimal POVM depends on the state-space singular basis and the parameter
basis. With no structure, describing U and V costs Nr and Pr real entries;
forming them and implementing the isometry are additional work. No efficient
synthesis, online decoder, quantum advantage, or publication-level novelty
follows from the small outcome count. Statistical optimality is separated from
implementation costs in STRUCTURE.md and resources.json.

The exact flat-spectrum combination is internally derived and checked, with a
bounded source comparison. It has not received external review or novelty
clearance. Semiparametric, local-asymptotic, and single-copy globally unbiased
problems must not be conflated simply because their risk formulas look similar.
