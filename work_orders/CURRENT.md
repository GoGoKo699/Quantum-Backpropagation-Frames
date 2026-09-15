# Current work order

**ID:** PF-07  
**Title:** Known-reference compilation for overlapping tangent intervals  
**Status:** Local study complete with findings; committed code awaiting remote verification.  
**Branch:** research/PF-07-overlap-reference  
**Baseline:** 0633ff37de69debbad93b78b146bb128be12106e

The user authorized the next compiler study after PF-06. The bounded scope and
predeclared physical grids are in results/PF-07/START.md. Main and all prior
branches remain unchanged. No merge, release or manuscript is authorized.

Constructed: unique first-nonzero-site aggregation of overlapping local tangent
rows, descending controlled suffix preparation, an elementary fast-Walsh CNOT/Ry
compiler, and sparse original-coordinate decoding. It uses no extra work
qubits or global support-address union. The charged input is the local tangent
table list, constructed with the existing causal compiler. The reference circuit
cost is O(n2^w), with explicit classical preprocessing, physical-bit scanning,
program-storage/regeneration and complete-output costs.

The logical estimator remains universally unbiased with total variance <=4s.
This is NOT an arbitrary-spectrum optimum: coordinate-support null directions
can saturate the bound. The exact PF-06 overlapping-layer counterexample is
recovered. Reversing the required suffix order is explicitly shown to fail.
No strongest-method scaling separation or price winner is claimed. Current
optimized sparse-state methods and aggregate-first readout baselines remain
eligible; the source comparison is bounded, not novelty clearance.

The local packaged-source run passed 26 groups, including 30 existing-circuit
points, 191 gate/Born/gradient cases, 60 finite differences, 21 complete-envelope
checks and ten compiler-only sizes through n=256. Full statevector tests stop
at eight system qubits. Read-only CI reruns the inherited integration gate,
PF-04/PF-05/PF-06 checks and this packet. The actual verified commit and artifact
will be recorded only after completion in results/PF-07/REMOTE_VALIDATION.json.

Read REPORT.md, PROOF.md, RESOURCES.md, SOURCE_AUDIT.md and DECISION.md under
results/PF-07. Stop after recording the completed packet and verification. This
work does not dispatch another study or strengthen the prior advantage claims.
