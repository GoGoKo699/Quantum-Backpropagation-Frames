# Current work order

**ID:** PF-06  
**Title:** Sparse optimal-readout compiler feasibility  
**Status:** Local study complete with findings; remote verification pending.  
**Branch:** research/PF-06-sparse-compiler  
**Baseline:** 070b2728dbdc022d35b9bb9a36bf8938e8bd9408

The user authorized the bounded study recommended after PF-05. The start
checkpoint is results/PF-06/START.md. Main remains at
1986fe53a65062120f1be9da14c28fa48b12484d; neither it nor prior branches is modified.

Constructed: an explicit CNOT/R_y/X/H implementation of the sparse reference
measurement for the existing disjoint one-layer six-rotation family. At zero
angles it attains the audited 4P-8 single-copy universally unbiased trace-risk
optimum. At nonzero one-layer angles it remains unbiased with an explicit
variance bound; unequal-spectrum optimality is not claimed. Tangent preparation,
physical outcome classification, all gate controls and final P-vector mapping
are charged. No singular-basis oracle or additional work qubits are supplied.

The small gate/Born tests, finite differences, aggregate decoder and predeclared
compiler-only sizes passed locally. A second-overlapping-layer example shows
where the one-layer selector is invalid. The strongest-method scaling separation
was NOT established: the cheap no-mask baseline already has the same asymptotic
work order. All comparisons retain the common full-gradient error/confidence
contract and allow optimized synthesis and aggregation on every side.

Read results/PF-06/REPORT.md, PROOF.md, RESOURCES.md, SOURCE_NOTES.md and
DECISION.md. Remote CI runs inherited integration/PF-04/PF-05 checks plus the
PF-06 source hashes and elementary circuit study, without repository write
permissions. A receipt will identify the actually executed source after review.

Stop after preserving code, evidence, source attributions, matched costs and the
bounded decision. No merge, public release, license, manuscript, new ansatz,
price-winner search, unrestricted theorem or follow-on study is performed.
