# Current work order

**ID:** PF-06  
**Title:** Sparse optimal-readout compiler feasibility  
**Status:** COMPLETE WITH FINDINGS; remote run inspected and artifact verified.  
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

The predeclared small gate/Born tests and compiler-only sizes passed. A fixed
second-overlapping-layer example shows where the one-layer selector is invalid.
The strongest-method scaling separation was NOT established: the cheap no-mask
baseline already has the same asymptotic work order. Comparisons retain the
common full-gradient error/confidence contract and allow optimized synthesis
and aggregation on every side.

GitHub run 34989964380, attempt 1, job 104451763981 passed on scientific-code
commit 02f6a689bc3a929e99f0d79537698e291c082348. It verified 36 inherited tests,
109 frozen files, all previous diagnostics/validators and the unchanged PF-02
144 scenarios/4320 candidate rows. It verified 11 PF-06 hashes and all 17 new
diagnostic groups. The full artifact was downloaded and SHA-256 verified after
inspecting the job log. See results/PF-06/REMOTE_VALIDATION.json. CI is read-only
and left the checkout unchanged. This receipt does not claim later code was run.

Read results/PF-06/REPORT.md, PROOF.md, RESOURCES.md, SOURCE_NOTES.md and
DECISION.md. Stop after this completed packet. No merge, public release, license,
manuscript, new ansatz, price-winner search, unrestricted theorem or follow-on
study was performed. A broader overlapping-support compiler is a research
question, not an implemented result or a dispatched task.
