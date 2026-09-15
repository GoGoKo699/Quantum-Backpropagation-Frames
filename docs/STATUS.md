# Current status

## Integration candidate

PF-01 is complete with findings on audit/PF-01; PF-02 is complete with findings
on repair/PF-02. PF-03 is the integration review on review/PF-03-integration.
Its source baseline is `8781c8fad5de5742b743178268b8e4f0e4b4f089`.
Main remains unchanged until an explicitly authorized merge.

| Layer | Accepted evidence | Limitation |
|---|---|---|
| Algebra | PF-01 retained the restricted reference-frame claims | Not universal POVM, gate, or hardware optimality; novelty open |
| Maintained implementation | PF-02 real/finite API and exact terminal compilers | Historical direct imports retain their original defects |
| Cost acceptance | 144 scenarios, 4320 candidate rows; parity wins 0 | Fixed small-instance model and sufficient budgets, not global optimality |
| Integration corrections | Exact round thresholds and scalar error normalization | Helper correctness, not a new estimator or advantage |
| Reproducibility | Read-only gate reruns tests, validators and the same PF-02 grid | No new parameter sweep or scientific extension |

The historical winners are full_direct: 96, full_greedy: 24, no_mask: 24.
Read results/PF-03/REPORT.md and DECISION.md for the integration disposition.
Actual execution evidence is tied to a source commit in the validation artifact;
results/PF-03/REMOTE_VALIDATION.json records the reviewed run once verified.

## Source and record policy

Both scientific input ZIPs and all 22 extracted files remain unchanged. PF-01,
PF-02 and the bootstrap/initialization records are frozen. Their past wording
and run environments are not rewritten to impersonate current runs.

PACKAGE_MANIFEST.json remains the initialization snapshot. The read-only gate
verifies frozen file identities against the exact PF-02 commit. New run logs,
results, source hashes and environment go to a fresh ignored runs/ directory,
not into existing evidence paths. Retired write-enabled workflows are retained
as text under results/PF-03/retired_workflows/ and are not executable workflows.

## Research position

Keep the parity compiler as a reproducible baseline. No positive strongest-method
advantage, novelty clearance, hardware performance, trainability or optimizer
convergence claim follows from the integration. A new scientific phase needs a
separately justified work order; no additional sweep is in progress.
