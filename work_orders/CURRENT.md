# Current work order

**ID:** PF-07  
**Title:** Known-reference compilation for overlapping tangent intervals  
**Status:** COMPLETE WITH FINDINGS; remote job and downloaded artifact verified.  
**Branch:** research/PF-07-overlap-reference  
**Baseline:** 0633ff37de69debbad93b78b146bb128be12106e

The user authorized the next compiler study after PF-06. The bounded scope and
predeclared physical grids are in results/PF-07/START.md. Main and all prior
branches remain unchanged. No merge, release or manuscript was performed.

Constructed: unique first-nonzero-site aggregation of overlapping local tangent
rows, descending controlled suffix preparation, an elementary fast-Walsh CNOT/Ry
compiler, and sparse original-coordinate decoding. It uses no extra work
qubits or global support-address union. The charged input is the local tangent
table list, constructed with the existing causal compiler. The reference circuit
cost is O(n2^w), with explicit classical preprocessing, physical-bit scanning,
program-storage/regeneration and complete-output costs.

The logical estimator is universally unbiased with total variance <=4s.
This is NOT an arbitrary-spectrum optimum: coordinate-support null directions
can saturate the bound. The exact PF-06 overlapping-layer counterexample is
recovered. Reversing the required suffix order is explicitly shown to fail.
No strongest-method scaling separation or price winner is claimed. Current
optimized sparse-state methods and aggregate-first readout baselines remain
eligible; the source comparison is bounded, not novelty clearance.

GitHub run 34995694899, attempt 1, job 104471232631 passed on scientific-code
commit 7f9e9c0aadeba872af8012691e88a47df5c9a361. It verified 36 inherited tests,
109 frozen files, the previous diagnostics and unchanged PF-02 144 scenarios /
4320 candidate rows. PF-04, PF-05 and PF-06 checks passed unchanged. All eleven
PF-07 packet hashes and 26 new groups passed, including 30 circuit points,
191 gate/Born cases, 60 finite differences, 21 full-envelope checks and ten
compiler-only sizes through n=256. Full statevector tests stop at eight system
qubits. The completed steps and downloaded full artifact were inspected, its
SHA-256 verified, and actual generated JSON/logs parsed. Receipt:
results/PF-07/REMOTE_VALIDATION.json. CI is read-only and left the checkout clean.
This receipt applies only to the stated code commit, not later changed code.

Read REPORT.md, PROOF.md, RESOURCES.md, SOURCE_AUDIT.md and DECISION.md under
results/PF-07. Stop with the completed packet. No follow-on task, broader sweep,
new ansatz, integration, manuscript, licensing change or publication is started.
