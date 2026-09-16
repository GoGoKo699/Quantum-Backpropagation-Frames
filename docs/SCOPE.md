# Scope and assumptions

[Home](../README.md) · [Tutorial](TUTORIAL.md) · [Proof](THEORY.md) · [Limitations](COMPARISONS.md)

The task is to extract a complete classical gradient from a supplied quantum
response and known tangent directions. At a fixed parameter point, a real
state-preparation circuit $U$ has Jacobian $J$. With
$T=U^{\mathsf T}J$ and $q=U^{\mathsf T}OU|0\rangle$, the gradient is
$g=2T^{\mathsf T}q$ when the objective and access meet the real-response contract.
The abstract theorem starts with known $T$ and a supplied reference-response
state; it does not grant an uncharged circuit for constructing either one.

## Exact statistical contract

- $T$ is a known real matrix of size $N \times P$ with $T^{\mathsf T}|0\rangle=0$.
- $q$ ranges over the **entire real unit sphere** in dimension $N$.
- One copy of $(|0,0\rangle+|1,q\rangle)/\sqrt2$ is supplied per record.
- One fixed overall POVM and real vector score may depend on $T$, not $q$.
  Unbiasedness holds for every allowed $q$; second moments are finite.
- Random settings, their labels, ancillas, and decoder randomness are part of
  the overall POVM. Unbiasedness is not imposed separately on each setting.
- Loss is the trace of the single-copy covariance of the full original
  $P$-vector. The exact formula additionally requires equal nonzero
  eigenvalues of $T^{\mathsf T}T$.

The [proof](THEORY.md) supplies all quantifiers, both lower bounds, and an
attaining measurement. The [compiler route](COMPILERS.md) separately charges
implementation for the existing disjoint and overlapping-interval families.
The interval construction is a bounded-risk readout, not an exact minimax
construction for arbitrary coordinate support.

## Error and computational accounting

For $K$ independent records, a trace-variance bound $B$ implies mean squared
Euclidean error of the sample mean at most $B/K$. Markov's inequality gives

```math
K\ge\frac{B}{\delta\varepsilon^2}
\quad\Longrightarrow\quad
\Pr\bigl[\|\widehat g-g\|_2\le\varepsilon\bigr]\ge1-\delta.
```

This is a sufficient prescription, not an exact optimal confidence law.
Coordinatewise, relative, and whole-vector error are different tasks.
Full-angle parameter normalization is retained; changing units is not a speedup.

Count response preparation, controls and inverses, readout gates, measurements,
physical bit scanning, classical decoding, tangent-table construction, precision,
memory, program storage or regeneration, and $P$ output writes. Logical
all-to-all arbitrary-rotation counts are not routed hardware timings. Dense
simulators validate small identities; they are not the scalable compiler path.

## Frozen boundary

The current contribution is the exact theorem, sparse attainer, and existing
charged realizations, with supporting comparisons. No new ansatz,
arbitrary-spectrum exact optimum, complex or mixed-state extension, coherent
reuse, optimizer analysis, hardware/noise/routing study, or favorable-price
search is implied.

The original goal of a strongest-method end-to-end improvement remains unmet.
A complete presentation of the theorem does not replace that milestone.
Novelty is unresolved beyond the bounded source comparisons already recorded.
Manuscript preparation and submission are separate work.
