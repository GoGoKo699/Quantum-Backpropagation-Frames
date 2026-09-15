# PF-02 start checkpoint

Status: IN PROGRESS. Authorized by the user's instruction to proceed after PF-01.

Parent baseline: `79423bc1e68b16ec8f0e8a45969240b1aa1c1c9f` on `audit/PF-01`.
Working branch: `repair/PF-02`. Main remains at `da0d8c771350b695206b6f06194277538833adb4`.

## Bounded task

1. Add a maintained, explicitly real and finite input interface for the parity calculations; do not alter the immutable research packets or archives. Reject invalid shapes, masks, rounds, phases, normalization, and nonfinite/complex arrays before coercion. Test valid-input equivalence and PF-01's four invalid-input probes.
2. Implement and verify an optimized exact full-mask readout with terminal linear outcome relabeling. Give parity both coherent and terminal-measurement implementations. Compare against no mask and an applicable local gradient method on the same existing local-circuit family.
3. Use the same complete-gradient norm, epsilon, delta, and access assumptions. Price quantum gates, sampling/synthesis, classical processing, measurement/reset, peak memory, preprocessing, and output. No claim of globally optimal synthesis or measured hardware advantage.
4. Record reproducible tests, source locators, costs and one acceptance decision under results/PF-02/. Do not start a new ansatz, theorem campaign, manuscript, tag, license, publication, or merge.

Local execution uses the supplied archives: direct network git access from the container failed (DNS). Remote reads/writes use the authorized GitHub connection. Local source identity will be checked independently against preserved hashes; local tests are not remote CI. Historical PF-01 records remain unchanged.
