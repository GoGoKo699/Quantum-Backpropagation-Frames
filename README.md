# Quantum Backpropagation Frames

**How accurately can one quantum experiment return a complete classical gradient?**

A circuit's tangent directions are known, but its response to an objective is
encoded in an unknown quantum state. Measuring the response directly loses the
signs needed for a gradient. Interfering it with a known reference makes signed
overlaps observable. Each measurement record contributes a vector of ordinary
numbers; averaging records estimates **all original coordinate derivatives**.

This repository gives an exact single-copy statistical limit, a measurement
attaining it, and explicit circuits for two structured tangent families. It
contains full proofs, supported Python implementations, executable examples,
and preserved numerical evidence.

## Choose a route

| Goal | Start here |
|---|---|
| Understand in about five minutes | Continue below, then read [scope](docs/SCOPE.md) |
| Learn in 20–30 minutes | [Worked tutorial](docs/TUTORIAL.md): probabilities, signed records, averaging |
| Verify or reuse | [Theorem and proof](docs/THEORY.md), [circuits](docs/COMPILERS.md), [implementation](docs/IMPLEMENTATION.md), [reproduction](docs/REPRODUCIBILITY.md) |

The [evidence index](docs/EVIDENCE.md) connects each claim to its proof, code,
tests, fixed data, and qualifications. [Comparisons and limitations](docs/COMPARISONS.md)
explain what the result establishes and where it stops.

## The result

Let the known real matrix $T$ have $N$ rows and $P$ columns, with a zero reference
row. For an unknown real unit vector $q$, the output is the complete
$P$-component gradient $g(q)=2T^{\mathsf T}q$. One experiment receives one copy of

```math
|\Omega(q)\rangle=
\frac{|0\rangle|0\rangle+|1\rangle|q\rangle}{\sqrt 2}.
```

The first register is a reference qubit; the second has dimension $N$. A
measurement and its classical decoder may depend on $T$, but are fixed
independently of $q$. Their mean must equal $g(q)$ for **every real unit response**,
and their second moments must be finite. Randomized settings and extra ancillas
are included in this overall measurement; individual settings need not be
unbiased separately.

If the $r$ nonzero eigenvalues of $T^{\mathsf T}T$ all equal $\lambda$, the smallest
possible worst-response sum of coordinate variances is exactly

```math
\lambda\max\{2r,\,4(r-1)\}.
```

A joint measurement with **at most $2r+1$ effects** attains it. The zero score for
an inactive outcome is part of the experiment: it still counts in the sample
average. The outcome count is an upper bound, not a minimality claim.

For the existing disjoint one-layer circuit on an even number $n$ of system
qubits ($N=2^n$), at zero angles $P=3n$, $r=P/2$,
and $\lambda=2$. Its explicit linear-size realization has risk $4P-8$, compared
with the no-mask benchmark $4P$. This additive constant gap is not an asymptotic
runtime advantage. A separate overlapping-interval construction has logical
circuit size $O(n2^w)$ and total variance at most
$4\,\mathrm{tr}(T^{\mathsf T}T)$, where $w$ is maximum interval width; it is not a
generic minimax compiler.

## Run a complete example

From a full clone, with Python 3.12 or 3.13:

```bash
git clone https://github.com/GoGoKo699/Quantum-Backpropagation-Frames.git
cd Quantum-Backpropagation-Frames
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python examples/flat_readout.py
```

The two-qubit example returns the six-coordinate mean
`[0, 1, 0, 0, 0, 1]`, inactive probability `0.375`, and trace variance `13`;
the worst-response value is `16`. These are exact moment calculations evaluated
numerically, not a hardware experiment. The [tutorial](docs/TUTORIAL.md) works
through the same calculation by hand. [Reproduction](docs/REPRODUCIBILITY.md)
includes the larger compiler-only example and bounded full verification.

## What remains limited

The exact theorem concerns real pure responses, a supplied phase reference,
one copy, universal unbiasedness, and trace variance in the original parameter
normalization. It does not optimize biased estimators, collective measurements,
extra coherent access, or high-confidence sample complexity. A concentration
conversion gives a sufficient sample budget only. Circuit construction,
physical bit processing, classical tables, program storage or regeneration,
and final output all have costs.

**No strongest-method end-to-end advantage or final novelty clearance is
established.** The fixed parity comparison found zero positive-round parity
winners in 144 scenarios; its negative result remains accessible. Research
scope is frozen around the existing theorem and constructions.

## Cite, contact, and reuse

Use [CITATION.cff](CITATION.cff) and identify the commit you used. There is no
associated release or article asserted by this citation. Questions and
corrections belong in [GitHub Issues](https://github.com/GoGoKo699/Quantum-Backpropagation-Frames/issues).

Original code and associated documentation are available under the
[MIT License](LICENSE), Copyright (c) 2026 Ruge Lin. Citation is appreciated,
not an extra license condition. [Methods and provenance](docs/PROVENANCE.md)
describe source preservation, attribution, and substantive AI assistance.
