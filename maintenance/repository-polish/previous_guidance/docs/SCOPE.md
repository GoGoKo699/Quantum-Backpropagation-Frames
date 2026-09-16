# Project scope and frozen paper boundary

## Agreed scientific goal

Develop frame-based quantum backpropagation by characterizing and compiling
shared measurements for complete classical gradients. A first positive result
may concern one concrete family with nonorthogonal tangents; arbitrary
parameterized circuits are not required.

At a fixed parameter point the requested output is the complete classical raw
gradient with explicit whole-vector error and confidence:

```math
\Pr[\|\widehat g-g\|_2\le\varepsilon]\ge1-\delta.
```

Coordinatewise variance, infinity-norm accuracy, unbiasedness and single-copy
trace risk are different contracts. A quantum gradient state or one directional
derivative does not complete this output task. Parameter normalization cannot
be changed silently to manufacture an improvement.

The original ultimate success requirement includes a provable end-to-end
improvement over an applicable strong existing gradient method under matched
access, accuracy and costs. This milestone is UNMET. Neither the exact variance
theorem nor the paper-scope freeze removes it or marks it completed.

Count preparations, controls, inverses, reference phase, coherent resources,
quantum gates, classical preprocessing/decoding, memory and all P output entries.
Do not supply a gradient, eigenbasis, QRAM or equally expensive intermediate
object for free. A weak comparator cannot establish the desired advantage.

## Current mathematical results

PF-04/PF-05 analyze the real pure reference-response family with one supplied
copy per experiment, a fixed overall POVM/decoder universally unbiased over all
unit responses, and finite second moments. Their exact equal-spectrum all-POVM
optimum is a single-copy trace-risk result, not an optimal confidence theorem.
The sparse attaining measurement has at most 2r+1 outcomes; a generic eigenbasis
is not a free input to an efficient implementation.

PF-06 realizes the exact optimum on the existing one-layer flat local family.
PF-07 gives a row-norm reference compiler for overlapping interval tangents with
variance <=4 tr(G) and O(n2^w) logical gates. It does not extend exact anisotropic
optimality or eliminate width-dependent work. These packet contracts, rather
than the earlier parity-only scope paragraph, govern their own claims.

The historical parity packet retains its narrower reference-preserving real
frame/Walsh and quadratic-phase-rank bounds. Those are not general POVM or CNOT
lower bounds. All original packets are preserved with their qualifications.

## Candidate Letter and hard stopping rule

Read PAPER_SCOPE.md. Exploration stops after PF-08's fixed comparison. The
candidate core is the exact measurement limit, its attainer and a charged local
realization. Extensions already obtained may support this story; further
ansatz, complex/mixed/coherent, optimization or hardware programs are excluded.
Only defects in the frozen claim, exact-source equivalence, significance and
self-contained consolidation remain publication-critical work.

PRL remains an ambition, not an acceptance prediction. Scope freeze is not a
submission GO. A theorem-centered paper may be evaluated on its own merits,
with the original unmet advantage milestone stated honestly. Do not launch more
research automatically if that narrower contribution fails the novelty or
significance test. Future explicit user instructions may change the boundary.

No manuscript, merge, release, tag, visibility change or license selection is
authorized merely by completing this packet or passing CI. Work stays in this
repository; no source-of-inspiration project is a result dependency.
