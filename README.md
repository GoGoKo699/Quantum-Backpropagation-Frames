# Quantum Backpropagation Frames

**How accurately can a shared quantum measurement estimate every coordinate of a gradient?**

A single shot returns a random record, not an exact gradient. This repository
studies the smallest possible total variance of that record, a measurement
attaining the limit, and what it costs to implement and decode it.

**[Start the worked tutorial](docs/TUTORIAL.md)** ·
[Reading and verification map](docs/RESEARCH_MAP.md) ·
[Run the example](#run-a-complete-example)

## The physical problem

At a fixed parameter point, a circuit's tangent directions are known, while its
response to an objective is encoded in an unknown quantum state. The derivatives
are signed overlaps between those tangents and the response. Interference with
a known reference makes those signs observable. Each outcome contributes a
vector of classical numbers; averaging independent records estimates **all
original coordinate derivatives**, including redundant parameter directions.

The reference and tangent data are part of the access contract. Preparing them,
performing the measurement, processing its bits, and writing the gradient are
separate costs. A statistically optimal measurement need not be a cheap circuit.

## Relationship to previous research

The question grew out of [Hopf-QBP](https://github.com/GoGoKo699/Hopf-QBP), which
uses the geometry of a particular state parameterization for gradient readout.
Here the focus shifts to a measurement question: **given known tangent queries,
what error is unavoidable, and which measurement attains it?** The theorem and
implementations stand on their own; no Hopf parameterization or accompanying
manuscript is required.

The scientific setting is **finite-copy quantum estimation and task-specific
measurement design**. Reference interference, reusable classical-shadow records,
POVM outcome processing, and dual measurement frames are established tools.
This work studies a particular globally unbiased minimax problem within that
literature, rather than introducing those tools or claiming a general solution
to quantum backpropagation. [Related work](docs/RELATED_WORK.md) explains the
precise relationships; the [primary-source map](literature/README.md) identifies
the papers and inspected statements.

## The result

Let $T$ be a known real $N\times P$ tangent matrix with a zero reference row,
and let $q$ be an unknown real unit response. The target is the full classical
gradient $g(q)=2T^{\mathsf T}q$. Each experiment receives one copy of

```math
|\Omega(q)\rangle=
\frac{|0\rangle|0\rangle+|1\rangle|q\rangle}{\sqrt2}.
```

A fixed joint measurement and decoder may depend on $T$, not on $q$. Their
mean must equal the target for **every real unit response**, with finite second
moments. Ancillas and randomized settings are allowed; individual settings need
not be unbiased separately.

If the $r$ nonzero eigenvalues of $T^{\mathsf T}T$ all equal $\lambda$, the least
possible worst-response sum of coordinate variances is exactly

```math
\lambda\max\{2r,\,4(r-1)\}.
```

A measurement with **at most $2r+1$ effects** attains it. An explicit disjoint
local-circuit family realizes the optimum with linear-size logical circuits.
A separate overlapping-interval compiler has size $O(n2^w)$ and variance at
most $`4\,\mathrm{tr}(T^{\mathsf T}T)`$, where $n$ is the number of system qubits
and $w$ is maximum tangent interval width; it is not a generic minimax compiler.

**Boundary.** This is a real pure-response, universally unbiased, single-copy
variance result—not an optimum for biased or collective estimation, an exact
high-confidence sample complexity, or a strongest-method end-to-end speedup.
Novelty is not finally cleared. The [scope](docs/SCOPE.md),
[full proof](docs/THEORY.md), and [comparisons](docs/COMPARISONS.md) state the
quantifiers, resource assumptions, and retained negative evidence.

## Follow the tutorial

The [self-contained tutorial](docs/TUTORIAL.md) takes about 20–30 minutes. It
assumes states, gates, the Born rule, and vector algebra—not prior expertise in
quantum estimation. Start at the beginning, or enter at the step you need:

| Step | What to read and understand |
|---|---|
| **1. Set up the task** | [The experiment](docs/TUTORIAL.md#1-the-experiment-and-the-question) and [two-qubit example](docs/TUTORIAL.md#2-a-complete-two-qubit-example): why six parameters give six output entries despite only three independent tangent directions. |
| **2. Follow one record** | [Reference interference](docs/TUTORIAL.md#3-make-the-reference-interfere-with-the-response) and [signed decoding](docs/TUTORIAL.md#4-turn-the-bits-into-a-six-entry-record): calculate every outcome probability and see why zero records still count. |
| **3. Understand the limit** | [Error and averaging](docs/TUTORIAL.md#5-quantify-the-error-before-discussing-optimality), [the theorem](docs/TUTORIAL.md#6-the-exact-theorem-and-its-assumptions), and [the attaining measurement](docs/TUTORIAL.md#7-the-attaining-measurement-in-any-equal-spectrum-model): distinguish one-response risk, worst-case optimality, and confidence. |
| **4. Run and check** | [Execute the example](docs/TUTORIAL.md#8-run-the-same-example), read [what extends](docs/TUTORIAL.md#9-what-extends-and-what-remains-outside-the-claim), then answer the [self-check](docs/TUTORIAL.md#10-self-check), with solutions. |

After the tutorial, follow **[proof](docs/THEORY.md) →
[circuit construction](docs/COMPILERS.md) →
[implementation](docs/IMPLEMENTATION.md)**. The [scientific map](docs/RESEARCH_MAP.md)
connects these steps to every active guide and the supporting verification routes.

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

The example reports the six-coordinate mean `[0, 1, 0, 0, 0, 1]`, inactive
probability `0.375`, and trace variance `13`; the optimal worst-response value
is `16`. These are analytic moments checked numerically against the compiled
circuit, not a hardware run. It also decodes a finite set of illustrative trials.
The [128-qubit compiler-only example](examples/compile_large.py) demonstrates the
larger implementation without allocating a global quantum state.

## Verify, reuse, and explore

| What you want to check | Where to go |
|---|---|
| **Assumptions and mathematical claims** | [Scope](docs/SCOPE.md) and [theorem with full proof](docs/THEORY.md); [circuits and charged costs](docs/COMPILERS.md) separate measurement existence from implementation. |
| **Code and conventions** | [Implementation guide](docs/IMPLEMENTATION.md): supported modules, input contracts, parameter order, bit order, full-angle rotations, and numerical limits. |
| **Evidence behind a claim** | [Evidence index](docs/EVIDENCE.md): proof → code → tests → recorded data, including original source packets and faithful reading copies. |
| **Reproduction and figures** | [Reproduction guide](docs/REPRODUCIBILITY.md): clean installation, examples, full verification, expected results, and deterministic figure/data regeneration. |
| **Earlier work and comparisons** | [Related work](docs/RELATED_WORK.md), [primary sources](literature/README.md), and [comparisons and limitations](docs/COMPARISONS.md), including the fixed negative parity result—not only favorable examples. |

For secondary guides, data provenance, preserved records, and contributor checks,
use the [complete reading and verification map](docs/RESEARCH_MAP.md).
[Current status](docs/STATUS.md) distinguishes available results from unresolved
claims; [methods and provenance](docs/PROVENANCE.md) document attribution,
source preservation, and substantive AI assistance.

## Cite, contact, and reuse

Use [CITATION.cff](CITATION.cff) and identify the commit you used; no associated
release or article is asserted. Questions and corrections belong in
[GitHub Issues](https://github.com/GoGoKo699/Quantum-Backpropagation-Frames/issues).

Original code and associated documentation use the [MIT License](LICENSE),
Copyright (c) 2026 Ruge Lin. Citation is appreciated, not an extra license
condition; [licensing details](docs/LICENSING.md) explain third-party boundaries.
