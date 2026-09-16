# PF-06 start checkpoint

Status: IN PROGRESS. The user authorized the compiler-feasibility study recommended after PF-05.

Pinned source: `070b2728dbdc022d35b9bb9a36bf8938e8bd9408` on `audit/PF-05-optimal-readout`.
Working branch: `research/PF-06-sparse-compiler`.
Main baseline: `1986fe53a65062120f1be9da14c28fa48b12484d`, unchanged.

## Bounded work

Construct an executable sparse reference-response measurement on the existing six-rotation nearest-neighbor family, starting with its disjoint one-layer subfamily. Charge the tangent construction, coherent reference/basis operations, computational-basis outcome scan, accumulation, and complete output. Exact optimality is claimed only where the existing flat-spectrum theorem applies; nonzero-angle checks must retain unbiasedness and disclose any weaker variance guarantee. Examine deeper overlapping circuits only to identify the boundary of the construction, not to launch an arbitrary-spectrum study.

The numerical grid is fixed before the comparison: small gate/Born tests at one through four two-qubit blocks, zero and seeded angles; scalable compiler-only checks at block counts 1,2,4,8,16,32,64,128,256. Include the cheapest eligible no-mask and grouped reversed-test constructions and the maintained full-mask/other appropriate comparators. Do not price basis access or tangent tables as free, do not use favorable objective selection as a winning-method argument, and do not equate POVM outcome count with physical measurement cost.

Preserve all previous archives, results, maintained APIs and tests. Add self-contained proof/compilation notes, diagnostics, resources and a bounded decision under results/PF-06. Run existing integrity/regression checks and the new diagnostics. CI remains read-only and records the actual executed source. No merge, release, licensing change, manuscript, new ansatz, unrestricted novelty claim or follow-on study is authorized.
