# Primary-source map

[Home](../README.md) · [Theory](../docs/THEORY.md) · [Comparisons](../docs/COMPARISONS.md)

The tutorial and proofs are self-contained. These optional sources deepen the
estimation and implementation background. Exact source versions and inspected
locators are preserved in the [optimal-readout source audit](../results/PF-05/SOURCE_AUDIT.md),
[compiler source notes](../results/PF-06/SOURCE_NOTES.md), and
[overlap source audit](../results/PF-07/SOURCE_AUDIT.md).

| Topic | Primary source | Relation to this repository |
|---|---|---|
| Operator moment and estimation bounds | [Tsang, Albarelli and Datta, Quantum Semiparametric Estimation](https://arxiv.org/abs/1906.09871v7) | Established machinery behind the first lower bound; local nuisance-parameter guarantees have different quantifiers |
| Real-state compatibility | [Miyazaki and Matsumoto, Imaginarity-free quantum multiparameter estimation](https://arxiv.org/abs/2010.15465v3) | State-independent Fisher-optimal measurements do not automatically give one finite globally unbiased score |
| Measurement dominance | [Salmon, Strelchuk and Arvidsson-Shukur, Only Classical Parameterised States have Optimal Measurements under Least Squares Loss](https://arxiv.org/abs/2205.14142v2) | Pointwise dominance and minimax optimality are different claims |
| Decoder choice | [Fischer et al., Dual frame optimization](https://arxiv.org/abs/2401.18071v2) | Canonical shadow scores need not be optimal; fixed-measurement decoder optimization differs from all-POVM minimax |
| Equatorial and diagonal ensembles | [Real equatorial shadows](https://arxiv.org/abs/2311.14622), [diagonal-unitary designs](https://arxiv.org/abs/1206.4451) | Background for the narrower phase/Walsh route |
| Gradient access and comparison | [Reversed gradient tests](https://arxiv.org/abs/2408.05406), [quantum backpropagation criteria](https://arxiv.org/abs/2306.14962) | Match output norm, controls, memory, grouping, and classical costs |

The [preserved parity source notes](../research/parity_frames/SOURCES.md) and
[matched-readout packet](../research/matched_readout/README.md) give the wider
attribution record. They are historical source assessments, not a fresh
exhaustive literature search or a novelty certificate. No cited article is
redistributed under the repository's MIT license merely by being cited.
