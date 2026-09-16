# Frozen technical core for expert review

This is a result synopsis, not a manuscript and not a novelty claim. Sources are
the unchanged PF-04 proof, PF-05 independent audit and PF-06/PF-07 compilers.

## Model

Known real T has columns t_j, T^T|0>=0 and s=tr(T^T T)>0. Unknown q is a real
unit vector. One experiment receives one copy of

```math
|\Omega(q)\rangle=(|0,0\rangle+|1,q\rangle)/\sqrt2,
\qquad g(q)=2T^{\mathsf T}q.
```

Output is the full original P-dimensional coordinate vector. A POVM and decoder
are fixed independently of q (they may depend on T), universally unbiased over
all real unit q, and have finite second moments. Random settings and ancillas
are included in the overall POVM; conditional unbiasedness for each setting is
NOT required for the all-measurement bound. The loss is single-copy covariance
trace, not local Cramer-Rao risk or exact high-probability sample complexity.

## Exact theorem and attaining construction

If the r nonzero eigenvalues of T^T T are equal to lambda, write
T=sqrt(lambda) L V^T with orthonormal columns of L and V. Then

```math
\inf_{E,Z:\,\mathbb E_q Z=g(q)}\sup_{\|q\|=1}
 \operatorname{tr}\operatorname{Cov}_q Z
=\lambda\max\{2r,4(r-1)\}.
```

The two lower bounds use q=|0> and the signed tangent-axis responses. These
are global-unbiasedness bounds, not an assumption that tangent observables
commute. The original full proofs remain in PF-04/PF-05.

Put a=|0,0> and b_i=|1,L e_i>. The effects

```math
E_{i,\sigma}=\frac{(|a\rangle+\sigma\sqrt r|b_i\rangle)
 (\langle a|+\sigma\sqrt r\langle b_i|)}{2r},
\qquad
E_*=I-|a\rangle\langle a|-\sum_i|b_i\rangle\langle b_i|
```

with scores Z_(i,sigma)=2 sigma sqrt(r lambda) V e_i and Z_*=0 attain the bound.
There are at most 2r+1 effects; minimal outcome count is NOT claimed. For
z=L^Tq the variance is 2r lambda+(2r-4)lambda ||z||^2. No postselection is allowed.

## Implementation and interpretation

PF-06 supplies an explicit O(P)-size realization at the existing disjoint
one-layer zero-angle family, with lambda=2, r=P/2, exact risk 4P-8. It prepares
only a known reference rather than requesting a tangent eigenspace oracle.
PF-07 extends row-norm reference preparation to overlapping interval tangents:

```math
c_x=\|T_{x,:}\|/\sqrt s,\qquad
Z(b,x)=2(-1)^b T_{x,:}^{\mathsf T}/c_x,
\qquad
\operatorname{tr}\operatorname{Cov}_q Z\le4s.
```

Its explicit gate count is O(n2^w), from charged local tables. The general
reference is only a bounded-risk construction; it is not claimed to attain the
flat theorem when coordinate support exceeds tangent span. The classical
streaming, full physical bit scan, preprocessing, program storage and P outputs
must be retained in any cost claim.

The older frame/Walsh optimum is 4r lambda. At r>=3 the ratio to the all-POVM
optimum is r/(r-1); it approaches one. This is a limitation on possible worst-
case single-copy variance gains within the stated estimator model, NOT a
universal impossibility theorem for quantum backpropagation or runtime speedup.

## Boundaries that must be visible in any paper

Real pure responses; exact supplied-reference access; one-copy universal
unbiasedness; whole-vector trace risk; parameter normalization fixed. Extra
coherent calls, collective measurements, biased/adaptive estimators, complex
responses and mixed states require different claims. A Markov conversion gives
a sufficient full-vector confidence bound for independent averages; it does
not make the theorem an optimal-tail sample complexity result. Generic L/V
access is not free. Novelty and broad physical significance remain to be settled.
