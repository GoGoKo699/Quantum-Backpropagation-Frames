# PF-05 proof audit and a sparse attaining measurement

Internal independent rederivation. Source baseline: PF-04 at
`996d60ab06e872ec44a0ab447917f2e198b4241b`. The prior packet is unchanged.

## 1. Decision and exact contract

KEEP the PF-04 equal-spectrum theorem. No counterexample or missing hypothesis
was found within its declared contract. The simpler construction below changes
the sufficient outcome count, not the minimax value. It is not a claim of
minimal outcome count or an efficient general circuit.

Let T be a known real N-by-P matrix, T^T e_0=0, and s=tr(T^T T)>0. The unknown
q ranges over the entire real unit sphere. One supplied copy is

```math
|\Omega(q)\rangle=(|a\rangle+|b_q\rangle)/\sqrt2,
\qquad |a\rangle=|0,0\rangle,\quad |b_q\rangle=|1,q\rangle.
```

The output is the original P-vector g=2T^Tq. A POVM and its real vector score
may depend on T but not q. Unbiasedness holds for every q for one fixed complete
measurement/decoder. Random settings are included in the outcome; separate
conditional unbiasedness is not assumed. Second moments must be finite.

No extra oracle call, collective measurement on several copies, data-dependent
score fitted to the unknown response, or arbitrary biased estimator is covered.
The phase-referenced preparation is part of the supplied input. The theorem is
about one-copy trace covariance, not exact high-confidence sample complexity.

## 2. General measurements and first-moment constraints

Compression to H_0=span(a,b_0,...,b_{N-1}) preserves probabilities and scores.
For a Hermitian effect E, entrywise Re E is real symmetric positive semidefinite:
its quadratic form is nonnegative on real vectors, hence on complex vectors by
splitting real/imaginary parts. Completeness and probabilities on real Omega
are preserved. Thus allowing complex physical measurements does not evade the
real-effect proof.

For continuous outcomes, use the scalar dominating measure tr E. The density is
a finite-dimensional PSD matrix and admits rank-one refinement. Finiteness of
second moments on the model implies finiteness on H_0: summing the densities of
Omega(+e_x) and Omega(-e_x) over x gives a strictly positive operator on H_0.
The finite-outcome sums below therefore also apply as integrals. Refinement
retains the same score and is only a proof device.

For coordinate j define M_j=int z_j dE and Q_j=int z_j^2 dE. Universal unbiasedness
and comparison of q with -q require

```math
M_j=\begin{pmatrix}\alpha_j&2t_j^{\mathsf T}\\
2t_j&-\alpha_j I_N\end{pmatrix}.
```

The odd polynomial in q fixes the off-diagonal block. The even quadratic form
must be constant on the unit sphere and therefore is scalar. There is no
operator-equality assertion outside H_0.

The standard operator moment inequality is Q_j >= M_j^2 [S1]. For discrete
outcomes, Vv=(sqrt(E_w)v)_w is an isometry and D_j multiplies outcome w by z_j(w).
Then Q_j-M_j^2=V^*D_j(I-VV^*)D_jV >=0. The same dilation gives the integral case.
At the valid unit response q=e_0, g=0 and

```math
\langle\Omega(e_0)|M_j^2|\Omega(e_0)\rangle
=\alpha_j^2+2\|t_j\|^2.
```

Hence every admissible measurement satisfies trace Cov_{e_0}(Z)>=2s. The retained
full-quadratic-mask estimator gives an upper bound 4s. The general 2s-to-4s
sandwich is an application of established estimation machinery, not a new
Cramer-Rao principle.

## 3. The second lower bound and exact flat-spectrum value

Write T=sqrt(lambda) U V^T, with U and V having r orthonormal columns and
U^T e_0=0. Orthogonal projection of any output onto range(V) cannot increase
squared error. This justifies working with r scores for target 2sqrt(lambda)U^Tq
even when P>r and coordinate tangents are redundant or nonorthogonal.

Refine real effects as |v_w><v_w| and set x_w=<a|v_w>,
y_w=(<b_{u_i}|v_w>)_i, with score z_w in R^r. Completeness and first moments give

```math
\sum_w x_w^2=1,\qquad \sum_w\|y_w\|^2=r,\qquad
\sum_w x_w z_w^{\mathsf T}y_w=2r\sqrt\lambda.
```

Cauchy-Schwarz in two ways gives

```math
A:=\sum_w x_w^2\|z_w\|^2\ge4r\lambda,
\qquad B:=\sum_w\|y_w\|^2\|z_w\|^2\ge4r^2\lambda.
```

Average the risk over q=+/-u_i, i=1,...,r. Their averaged density has reference
weight 1/2 and weight 1/(2r) on each tangent basis vector; each target norm
squared is 4lambda. Thus the average risk is (A+B/r)/2-4lambda, at least
4(r-1)lambda. Combining with the reference response gives

```math
\mathcal V(T)\ge\lambda\max\{2r,4(r-1)\}.
```

These inequalities do not select a canonical shadow decoder, assume projective
measurement, or rely on local/asymptotic unbiasedness.

## 4. A 2r+1-outcome measurement attains the bound

Define, for i=1,...,r and sigma=+/-1,

```math
E_{i,\sigma}=\frac1{2r}
(|a\rangle+\sigma\sqrt r|b_{u_i}\rangle)
(\langle a|+\sigma\sqrt r\langle b_{u_i}|),
\qquad E_*=I-|a\rangle\langle a|-\sum_i|b_{u_i}\rangle\langle b_{u_i}|.
```

Return Z_{i,sigma}=2sigma sqrt(r lambda) V e_i and Z_*=0. Pairwise summation
cancels cross terms and proves completeness; every effect is positive. This
is one joint measurement, not classical random selection of incompatible
coordinate observables with a free importance correction.

Putting z=U^Tq, the Born probabilities are

```math
p(i,\sigma\mid q)=\frac{(1+\sigma\sqrt r\,z_i)^2}{4r},
\qquad p(*\mid q)=\frac{1-\|z\|^2}{2}.
```

Summing signed outcomes gives E_q Z=2sqrt(lambda)Vz exactly. Every active score
has squared norm 4r lambda, and active probability is (1+||z||^2)/2. Therefore

```math
\mathrm{tr}\,\mathrm{Cov}_q(Z)
=2r\lambda+(2r-4)\lambda\|U^{\mathsf T}q\|^2.
```

The maximum is lambda max{2r,4(r-1)}. Both ||U^Tq||=0 and 1 are possible. This
closes the lower bound. The PF-04 character measurement has the same trace risk;
it need not have the same covariance matrix. No minimal-outcome theorem follows.

## 5. Explicit dilation does not give free basis access

On the active space an isometry is

```math
W|a\rangle=\frac1{\sqrt{2r}}\sum_i(|i,+\rangle+|i,-\rangle),
\qquad W|b_{u_i}\rangle=(|i,+\rangle-|i,-\rangle)/\sqrt2.
```

Its columns are orthonormal. Route the complementary input to a failure sector
and measure in the output basis. This proves implementability abstractly, not a
gate-count bound. The tangent-basis isometry, ancillary routing, uniform
reference splitting, and the output map V must all be constructed and charged.

Once that measurement is supplied, accumulate r signed channel counts in O(K)
classical updates and map them through V once. A generic dense V costs O(Pr)
for the final multiplication and storage, in addition to Omega(P) output writes.
No general efficient tangent-basis circuit or strongest-method advantage is
claimed. A small number of measurement outcomes does not bound synthesis cost.

## 6. Boundaries tested rather than silently generalized

- The estimator is not postselected: dropping the complementary outcome and
  dividing by active probability changes the target. For ||U^Tq||^2=1/4 the
  active probability is 5/8 and such division introduces a bias factor 8/5.
- An imaginary response q=i u_i is outside the real model. The same sparse
  measurement has trace risk 4r lambda for the real target, not the pure-real
  theorem's value. This is not a counterexample on the declared domain.
- The mixture of the 2r axis reference-state densities has target zero and
  sparse-estimator risk 4r lambda. Each constituent has risk 4(r-1)lambda.
  Convexifying the unknown state model therefore changes the variance problem.
- A zero output has worst-case squared error 4lambda, and for r>=3 beats the
  one-copy unbiased minimax value if bias is permitted. No all-estimator MSE
  theorem is inferred.
- Local pure-state Fisher information equals 2I in an orthonormal chart for q.
  The locally unbiased trace bound for the target is 2lambda(r-||U^Tq||^2).
  At a tangent axis this is 2(r-1)lambda, smaller than the universal finite-copy
  bound for r>=3. A score constructed at that axis is biased elsewhere. This
  explains, rather than contradicts, the real-state compatibility result [S2].

Independent tests explicitly realize these distinctions. The local Fisher
example at r=3, lambda=1 has risk 4 at its chosen point and nonzero bias at the
opposite point, whereas the global universally unbiased minimax risk is 8.

## 7. Same-family corollary and stopping point

The PF-04 disjoint-block corollary also survives. At zero angles the existing six
Pauli rotations have three singular values sqrt(2); each distinct tangent occurs
twice. Across even n qubits, P=3n, r=P/2 and lambda=2, giving optimum 4P-8 versus
frame/Walsh 4P. The perturbation bound sqrt(220)h follows by bounding column j's
change by 2jh for j=0,...,5 and summing squares. It has an n-independent small
angle domain. Our independent two-qubit matrix calculations check this premise.

No arbitrary-spectrum optimum, generic efficient POVM compiler, hardware claim,
sharp confidence law or novelty certificate was established in this audit.
