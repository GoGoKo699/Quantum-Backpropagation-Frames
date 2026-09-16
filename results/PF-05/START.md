# PF-05 start checkpoint

Status: IN PROGRESS.
Branch: `audit/PF-05-optimal-readout`.
Pinned scientific baseline: `996d60ab06e872ec44a0ab447917f2e198b4241b` on `research/PF-04-boundary`.
Main at start: `1986fe53a65062120f1be9da14c28fa48b12484d`.

The user authorized the proposed targeted proof and novelty audit after PF-04.
This is an internal independently implemented audit, not external peer review.

## Bounded task

1. Independently verify the exact all-POVM single-copy result for equal nonzero
   tangent singular values, its general lower bound, finite attaining POVM,
   parameter redundancy, and near-flat corollary. Check the exact estimator,
   real-response, normalization, phase-reference, and universal-unbiasedness
   contracts. Do not infer high-confidence sample optimality from variance.
2. Search and inspect primary optimal-estimation literature. Record actual
   versions and theorem/section locators. Distinguish a new finite minimax
   statement from a direct application of established inequalities or local,
   asymptotic, and state-dependent results. A failed search is not novelty proof.
3. Write new diagnostic code without importing PF-04 formula functions. Include
   explicit Born probabilities, positivity/completeness, redundant and complex
   measurement effects, null output directions, and deliberate out-of-contract
   comparisons. No new ansatz, broad cost sweep, or arbitrary-spectrum campaign.
4. Record KEEP / NARROW / CORRECT / ALREADY-KNOWN / OPEN dispositions and one
   justified next decision. Preserve all earlier packets, code, hashes, and
   the negative PF-02 result. Run the inherited integration gate and the new
   bounded checks with read-only CI.

The uploaded PF-04 ZIP is a local input, not a full repository checkout. Its
SHA-256 is `0d5b7c910a563d9f0ebbf5908945cdd93d725cc3b8c45b4eb33fa6e5c2eaaf41`.
The packet files will be checked against the manifest read at the pinned remote
commit before use. Local and remote verification will be recorded separately.

Stop after the audit packet and evidence. Do not merge, release, change the
license, draft a manuscript, or start another scientific work order.
