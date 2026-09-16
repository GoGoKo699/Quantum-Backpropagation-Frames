# Reading and verification map

[Home](../README.md) · [Tutorial](TUTORIAL.md) · [Evidence](EVIDENCE.md)

The main route is **physical problem → worked example → exact theorem →
attaining measurement → executable circuits → comparisons**. Read it in that
order to learn the method, or use the checks below to enter at a particular
claim. No development history or unfinished manuscript is a prerequisite.

## Learn the result

| Guide | Purpose |
|---|---|
| [Worked tutorial](TUTORIAL.md) | Complete two-qubit probabilities, signed records, averaging, implementation, and self-check answers. |
| [Scope and assumptions](SCOPE.md) | The supplied state, universal unbiasedness, whole-vector loss, and exact restrictions. |
| [Relationship to previous research](RELATED_WORK.md) | Established measurement tools versus the particular minimax problem; links to research origin. |
| [Primary-source map](../literature/README.md) | Literature organized by scientific relationship, with exact source locators. |

## Prove, construct, and compare

| Guide | Purpose |
|---|---|
| [Theorem and full proof](THEORY.md) | Both lower bounds, the sparse attaining POVM, general bounds, and nearby spectra. |
| [Constructive circuits](COMPILERS.md) | Disjoint realization and overlapping-interval reference preparation, with quantum and classical costs. |
| [Comparisons and limitations](COMPARISONS.md) | Local versus universal unbiasedness, variance versus runtime, eligible baselines, and negative findings. |
| [Claim summary](CLAIMS.md) | A compact statement of the supported claims and their boundaries. |
| [Concise technical core](source-readings/core-result.md) | A faithful reading copy of the preserved theorem-and-construction synopsis. |

The [evidence index](EVIDENCE.md) links each result to its original proof,
independent diagnostic, implementation, numerical record, and qualification.
It also routes readers to the [local-tangent derivation](source-readings/local-tangent-structure.md),
[disjoint proof](source-readings/disjoint-proof.md), and
[interval proof](source-readings/interval-proof.md). These reading copies preserve
the source mathematics while fixing markup; the original files remain linked.

## Run, reproduce, and inspect the evidence

| Resource | Purpose |
|---|---|
| [Implementation guide](IMPLEMENTATION.md) and [package guide](../qbp_frames/README.md) | Supported imports, contracts, bit/parameter conventions, numerical limits, and links to the maintained source. |
| [Small executable example](../examples/flat_readout.py) | The tutorial's complete gradient, Born-probability checks, and finite-record decoder. |
| [Large compiler-only example](../examples/compile_large.py) | A 128-qubit circuit compilation, explicitly not a large-state simulation. |
| [Reproduction guide](REPRODUCIBILITY.md) | Exact commands for smoke checks, full verification, inherited suites, and figure regeneration. |
| [Recorded-data guide](../data/recorded/README.md) | Durable data, recovered artifact members, source receipts, and integrity boundaries. |
| [Figure formulas and provenance](REPRODUCIBILITY.md#figure-and-table-provenance) | Analytic plotted values, source hashes, and the deterministic regeneration script. |

For a particular number, start from its claim in [Evidence](EVIDENCE.md), then
follow the linked data and generating program. The
[negative parity comparison](COMPARISONS.md#what-the-negative-comparison-establishes)
and [fixed overlap comparison](COMPARISONS.md#what-the-overlap-comparison-establishes)
lead to their original reports and tables. The [preserved result packets](../results/)
and [original research inputs](../research/) are available for deeper inspection,
not as a substitute for the canonical explanation.

## Status, attribution, and reuse

[Current status](STATUS.md) states what is implemented and what remains
unresolved. [Scope of the current contribution](PAPER_SCOPE.md) records the
scientific stopping point; it is not a manuscript or publication claim.
[Methods and provenance](PROVENANCE.md) cover research origin, the Hopf-QBP link,
source preservation, and substantive AI assistance. Use [CITATION.cff](../CITATION.cff)
for attribution and [MIT](../LICENSE) with [licensing details](LICENSING.md) for reuse.

## For contributors and reproducibility reviewers

The [working rules](../AGENTS.md), [current work boundary](../work_orders/CURRENT.md),
and [repository setup](../SETUP_GITHUB.md) describe safe maintenance without
restarting archived studies. The [engineering migration record](../maintenance/repository-polish/REPORT.md)
and [checked migration map](../maintenance/repository-polish/MIGRATION.json)
record preserved bytes, supported-code copies, and actual validation coverage.
The [root reproduction entry](../REPRODUCIBILITY.md) points to the same current
verification guide. The [read-only workflow](../.github/workflows/validation.yml)
and [validation runner](../tools/validate.py) implement those checks.
