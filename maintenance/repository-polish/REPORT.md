# Repository consolidation and validation record

This engineering record is outside the primary scientific route. The work
consolidates the frozen results; it is not a new scientific campaign, manuscript,
release, or novelty clearance.

## Baselines and integration

The live initial refs matched the handoff:

| Ref | Commit | Tree |
|---|---|---|
| Licensed main | 40f60b4061d7cd7434552b7947f4d118750daf06 | 46caea86462feffb1fbbfe741b4f1a14f0d1230f |
| Integrated scientific baseline | 1986fe53a65062120f1be9da14c28fa48b12484d | ef3c19cce5cc4d05cf66a7032943f04f687a7cd6 |
| Completed scope branch | a24bf0f182835416d87a4521fff2673b29431f81 | 68d93dedec8088facab3372a80435c00ce798b38 |

There were nine branch heads, no tags, one already merged PR, and no open PRs.
All heads and their ancestry were fetched via GitHub Git-data APIs because
this environment's direct GitHub Git transport was unavailable. All 32 original
commit objects, 31 distinct root trees, and 273 blobs were reconstructed with
exact Git object hash verification; git fsck passed. This is a complete verified
object database, not a source ZIP presented as a clone.

A normal two-parent merge integrated the research with licensed main. Only
README prose conflicted; both source parents and MIT material were retained.
The local integration checkpoint is 2322b03; its remote equivalent is
88e019ec8de8951d67bd36359d33079aa33c926f. Both have tree
5a25c1a2eb3a3206d8369af0304e4dc19dccb94f and the two requested parents.
Different transport-created commit metadata does not alter file identities.
The working remote branch is publication/repository-polish. No source branch,
remote history, or tag was rewritten or deleted.

## Safety and license coverage

GitHub reported the repository **already public** at the first live check and
recognized the standard MIT License. No visibility change was necessary.
LICENSE retains Copyright (c) 2026 Ruge Lin and no mandatory-citation condition.
The root license applies to original project material; citations do not license
papers, and dependencies retain their own licenses.

[History scan](HISTORY_SAFETY.json) covers all initial reachable branch/PR objects,
commit text, both ZIP archives and extracted contents. Pattern categories include
private keys, service tokens, cloud credentials, signed URLs, and credential
assignments. No matching exposure was found. Contextual review of source packets,
provenance and notices identified original research/code and scholarly references,
with no incorporated paper reproduction or conflicting third-party notice found.
Author names and intentionally public Git author metadata were retained.

[Remote surface review](REMOTE_SAFETY.json) covers the merged PR and its two
comments, 30 Actions runs, 29 available logs, and all 18 retained artifacts
(451 archive members). Every downloaded artifact matched GitHub's SHA-256.
No exposure or redistribution concern was found. Job 104292371080 in skipped
run 34941928929 has no steps or artifact and its log returned 404 BlobNotFound.
The connector does not expose the commit-comment collection. No inaccessible
content is claimed reviewed. This is a bounded pattern and contextual review,
not a guarantee that every possible secret or rights issue is absent.

## Migration and evidence preservation

[MIGRATION.json](MIGRATION.json) identifies every initial source ref, preserved
file hash, old guidance copy, maintained-code source, and recovered artifact
member. Original scientific packets, ZIP bytes, numerical records, manifests,
retired workflow text, and substantive negative results remain at their existing
paths. Historical paths, timestamps, and hashes are not rewritten.

Thirteen active guidance files were copied byte-for-byte before replacement.
Their original relative links remain historical; current navigation uses the
canonical docs. Journal-specific planning remains in those archived sources
but is removed from active guidance. The scientific freeze is unchanged.

The supported qbp_frames package copies established numerical algorithms and
adds explicit validation and equivalence tests. Original implementations remain
reference fixtures. The repaired round threshold and terminal-outcome relabeling
remain intact. Package installation does not require historical directories.

Eight compact original overlap/analysis artifact members were recovered into
[data/recorded](../../data/recorded/) with their exact bytes and original member
paths recorded. Durable scientific evidence therefore does not depend solely
on expiring Actions artifacts. Their metadata still describes the original runs.

## Verification coverage

The combined baseline passed the inherited gate in a clean local clone: 36
repository tests, 109 frozen-file comparisons, both supplied validators, and
all 144 scenarios/4320 candidate rows. Winner categories remain 96 full_direct,
24 full_greedy, 24 no_mask, and zero positive-round parity. Numerical row
tolerance remains 1e-12 relative and absolute; categorical fields match exactly.
The unchanged later suites passed 8/10/17/26 diagnostic groups and eight fixed
analysis checks on 30 small points and ten compiler cases.

Final current-tree validation, exact-head CI, rendered-page review, and merged
verification are recorded below as they are completed. A historical green run
or a local source inspection is not substituted for those checks.

## Repository metadata

The current connector can create Git objects and PRs but exposes no repository
settings write for description/topics. Suggested description:

> Single-copy limits and constructive measurements for quantum-gradient readout, with reproducible proofs, circuits, and resource analysis.

Suggested topics: quantum-information, quantum-computing, quantum-gradients,
quantum-estimation, quantum-measurements, reproducible-research, python.
No journal target or unsupported advantage claim is included.

The current licensing explanation moved from LICENSE_STATUS.md to docs/LICENSING.md
to avoid GitHub detecting it as a second license. Its original bytes remain in
the guidance archive; the operative MIT text is unchanged.

The maintained disjoint histogram decoder now validates raw integer entries
before binary64 conversion and sums absolute counts exactly. Regression probes
cover oversized and summed counts at 2^53; valid endpoints remain accepted.
