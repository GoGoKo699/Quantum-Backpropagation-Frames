# Relationship to previous research

[Home](../README.md) · [Primary sources](../literature/README.md) ·
[Theorem](THEORY.md) · [Comparisons and limitations](COMPARISONS.md)

This work belongs to finite-copy quantum estimation and task-specific
measurement design. Complete-gradient readout supplies the application: the
known tangent directions specify which signed overlaps must be estimated.
The [canonical theorem](THEORY.md) starts with a known real query matrix and an
unknown reference-encoded response, not a particular state parameterization.
The [research origin](PROVENANCE.md#research-origin-and-related-repository)
is distinct from the prior work against which the result must be assessed.

## Established input and processing tools

**Reference interference and shared signed overlaps.**
[Zhao et al., Lemma F.16](https://arxiv.org/pdf/2604.07639v1#page=127)
construct interferometric classical shadows for estimating many real overlaps
with classically specified test vectors. The reference-response state is the
same interface used here; Eqs. (F64)-(F68) state the guarantee and mechanism.
Using normalized tangent vectors as the queries gives a gradient application
of that interface, not a new interference primitive. Their efficient decoding
requires suitable stabilizer-overlap evaluation. Their data-loading and
exponential-advantage results are not inherited by the present single-copy task.

**POVM scores and dual measurement frames.**
[D'Ariano and Perinotti](https://arxiv.org/abs/quant-ph/0610058v2)
already optimize the processing of measurement outcomes to estimate operator
averages. Their Eqs. (2)-(3) express observables through POVM scores, and
Eqs. (13)-(15) optimize ensemble-averaged error for a fixed measurement.
[Innocenti et al.](https://arxiv.org/abs/2301.13229v3), Sections II-III and
Appendix C, connect classical shadows to dual measurement frames and study
minimum-variance estimators. These scores can also be universally unbiased;
the distinction here is not simply unbiased versus biased processing.

A differential frame contains state-space tangent vectors. A measurement frame
contains operators representing observables and their estimators. The two can
be connected by a readout construction, but they are not interchangeable.
Neither introducing frames nor assigning reusable unbiased scores is claimed
as a new principle here.

## Which optimization problem is different?

The [exact result here](THEORY.md#the-exact-theorem-and-its-quantifiers) minimizes
worst-response, single-copy total variance over all joint POVMs and fixed vector
scores that are unbiased throughout the specified real pure response family.
Its closed form requires equal nonzero tangent sensitivities. The full original
coordinate vector is the target; individual random settings need not each be
unbiased separately.

The following distinctions matter when matching an existing theorem. A fixed-
measurement dual optimization need not optimize over all measurements. A
state-averaged objective need not equal a worst-response objective. A locally
unbiased decoder at one response need not be one fixed score valid throughout
the family. Pointwise dominance over every competitor is stronger than minimax
optimality within this specified class. These distinctions are explained in
[Comparisons](COMPARISONS.md#which-optimality-is-proved), with the
[original source locators](../results/PF-05/SOURCE_AUDIT.md).

In particular, existing real-state Fisher-optimal measurements prevent a claim
that this is the first unknown-state-independent optimal measurement. Existing
shadow and dual-frame methods prevent a claim that previous methods must
reconstruct the full state or use a nonoptimized canonical decoder. The
[eligible baselines](COMPARISONS.md#eligible-strong-baselines) retain their
permitted measurement, grouping, and classical-processing optimizations.

## The contribution and its boundary

The contribution presented here is the specific exact statistical limit, its
finite attaining POVM, and [charged structured realizations](COMPILERS.md).
The disjoint realization attains the flat-spectrum limit; the interval compiler
is a separate bounded-risk construction. Controlled rotations and conditional
state preparation are established ingredients, with attribution in the
[compiler source notes](../results/PF-06/SOURCE_NOTES.md) and
[overlap source comparison](../results/PF-07/SOURCE_AUDIT.md).

Novelty is not settled by different terminology or by the absence of an exact
wording match. An equivalent estimation theorem would remain relevant even if
it never mentioned gradients. The current source comparisons do not constitute
final novelty clearance, and the statistical result does not establish a
general backpropagation or strongest-method end-to-end speedup. This attribution
map changes neither the theorem's assumptions nor the frozen research scope.
