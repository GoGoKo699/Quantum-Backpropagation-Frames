# Current work order

**ID:** PF-06  
**Title:** Sparse optimal-readout compiler feasibility  
**Status:** COMPLETE WITH FINDINGS; final code verified remotely.  
**Branch:** research/PF-06-sparse-compiler  
**Baseline:** 070b2728dbdc022d35b9bb9a36bf8938e8bd9408

The user authorized the bounded study recommended after PF-05. The start
checkpoint is results/PF-06/START.md. Main remains at
1986fe53a65062120f1be9da14c28fa48b12484d; prior branches and evidence are unchanged.

Constructed: an explicit CNOT/R_y/X/H implementation of the sparse reference
measurement for the existing disjoint one-layer six-rotation family. At zero
angles it attains the audited 4P-8 single-copy universally unbiased trace-risk
optimum. At nonzero one-layer angles it remains unbiased with an explicit
variance bound; unequal-spectrum optimality is not claimed. Tangent preparation,
physical outcome classification, all gate controls and final P-vector mapping
are charged. No singular-basis oracle or additional work qubits are supplied.
The final classifier scans one emitted bit string; see SCANNER_NOTE.md.

The predeclared small gate/Born tests and compiler-only sizes passed. A fixed
second-overlapping-layer example shows where the one-layer selector is invalid.
The strongest-method scaling separation was NOT established: the cheap no-mask
baseline already has the same asymptotic work order. Comparisons retain the
common full-gradient error/confidence contract and allow optimized synthesis
and aggregation on every side.

Final GitHub run 34990914564, attempt 1, job 104455018629 passed on scientific-code
commit 664d1a1db95a20d6a8bd356acbedd296869fcf5e. It verified 36 inherited tests,
109 frozen files, all previous diagnostics/validators and the unchanged PF-02
144 scenarios/4320 candidate rows. It verified 12 PF-06 hashes and all 17 new
diagnostic groups. The completed job steps and downloaded full artifact were
inspected; artifact SHA-256 and generated JSON/logs were verified. See
results/PF-06/REMOTE_VALIDATION.json. CI is read-only and left the checkout
unchanged. Earlier local and remote records remain identifiable in Git history
and the delivery. The receipt applies only to its stated scientific-code commit.

Read results/PF-06/REPORT.md, PROOF.md, RESOURCES.md, SOURCE_NOTES.md and
DECISION.md. Stop after this completed packet. No merge, public release, license,
manuscript, new ansatz, price-winner search, unrestricted theorem or follow-on
study was performed. A broader overlapping-support compiler is a research
question, not an implemented result or a dispatched task.
