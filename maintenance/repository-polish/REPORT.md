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

## Executed current-tree verification

[LOCAL_VALIDATION.json](LOCAL_VALIDATION.json) records the full gate on local
commit 8fdc51a661dccfbca4e853c4cee815d2d1350117, tree
905cbc4325909515654a875882cc4c3a9d75f519. Command:

```bash
python tools/validate.py --mode full --output runs/complete-local
```

It passed 53 repository tests (36 inherited, 12 supported-package tests, five
validation tests), original 109 frozen checks, 187 preserved-file identities,
12 then-recorded guidance copies, four maintained-code maps, the 144/4320
acceptance regression, all 8/10/17/26 diagnostic groups, eight final analysis
checks, both examples, and byte-identical figure/data regeneration. Runtime was
37.61 seconds with Python 3.12.14, NumPy 2.3.5, Matplotlib 3.10.8, and PyYAML
6.0.3. The checkout was clean before and after. The later licensing relocation
adds a thirteenth preserved guidance copy without changing scientific code.

[FRESH_QUICKSTART.json](FRESH_QUICKSTART.json) records a separate full local clone
of the verified object database, an ordinary isolated venv, and the exact README
`python -m pip install -e .` installation. The installer selected NumPy 2.5.3
under Python 3.12.14. Both examples passed from the clone and from an unrelated
working directory; outputs matched and the clone remained clean. A separate
wheel installation also ran without any research/results directories available
as runtime imports. CITATION.cff passed the complete official CFF 1.2.0 JSON
Schema with format checking; its schema hash is in the receipt.

[CI_CANDIDATE.json](CI_CANDIDATE.json) records independently inspected GitHub run
[35054584006](https://github.com/GoGoKo699/Quantum-Backpropagation-Frames/actions/runs/35054584006),
job 104661958048, on PR head 816ec9ccd260540a4f2c2d58af6afaef12a0e593.
The actual PR merge checkout has the same tree 905cbc4325909515654a875882cc4c3a9d75f519.
The full gate passed on Python 3.13.15; all logs and generated outputs were
inspected, and downloaded artifact 10430046808 matched SHA-256
ae0bfe94627e6d5fb877165c2b2dd19e390ad6060e2cfdec0767df06555ab80a.
This is fresh GitHub CI, separate from the local pass and historical receipts.
Only nonblocking action-runtime deprecation notices appeared.

## Rendered review and new-reader walkthrough

The actual GitHub README, tutorial, theory, compilers, implementation,
comparisons, reproduction, evidence index, scope, and methods/provenance pages
were opened in the browser. Desktop viewport was 1363 by 936 CSS pixels; document
content width was 929 pixels. Rendered headings, tables, code fences, navigation,
equations, and the analytic SVG were inspected. The pages had no reported
MathJax error elements or overflowing math/table/code containers at that width.

DOM inspection also checked literal dollar delimiters outside math/code. This
caught Markdown consuming a few inline norm/subscript expressions and
hyphen-adjacent formulas despite the absence of MathJax errors. They were changed
to display math or ordinary phrases for final reinspection. The source checker
alone is not counted as visual validation.

The browser provides no working viewport-resize or device-emulation control in
this session; attempted UI shortcuts did not alter its viewport. Narrow/mobile
rendering is therefore **not verified**. No local approximation is reported as
GitHub mobile rendering.

The new-reader walkthrough followed the physical question, two-qubit
probabilities, signed six-coordinate records, inactive-trial normalization,
exact theorem and exclusions, runnable example, and direct proof/evidence links.
The tutorial's mean [0,1,0,0,0,1], inactive mass 3/8, risk 13, worst risk 16, and
no-mask benchmark 24 agree with executable output. The larger demonstration
emits 1658 gates for 128 qubits and returns 384 original coordinates. It is
explicitly compiler-only. Neither route requires development chronology or an
external manuscript.

## Integration review

The complete change inventory was checked against licensed main and the frozen
research head. All original research/results/provenance/validation trees,
PACKAGE_MANIFEST.json, terminal compiler, and inherited tests are unchanged from
the appropriate source baseline. LICENSE matches licensed main exactly.
Maintained code was compared with original fixtures; an independent review
identified the count-boundary fix described above, now covered by regression.

PR [2](https://github.com/GoGoKo699/Quantum-Backpropagation-Frames/pull/2) contains
separate research-integration, canonical-content, supported-package, and
validation commits. Main has no branch-protection rule or ruleset at inspection;
the task nevertheless requires passing the current validation job before merge.
Subsequent exact-head and merged-tree checks are associated with that PR and
GitHub commit statuses; earlier receipts never stand in for a changed tree.

## Main verification and inline-math repair

PR 2 merged normally as a5f0f69a0fa7e6a6fad792ae5ad01939b699bdbd, tree
002e7388cefaae4d7ec648ccc8c0553a698933a1. Its independent main-push run
[35055668821](https://github.com/GoGoKo699/Quantum-Backpropagation-Frames/actions/runs/35055668821)
passed the full gate: 53 tests, all inherited diagnostics and fixed-data
analysis, the 144/4320 acceptance record, examples, and deterministic figures.
Logs and outputs were inspected; downloaded artifact 10430572819 was 150228
bytes with verified SHA-256
32993bd46f26deb9f4e659ee513a6126782b101078911b4bf73385c4e3061948.
The checkout remained clean, actual visibility was public, MIT was recognized,
and all eight original non-main branch heads were unchanged.

The final main-page screenshot exposed a second Markdown interaction: escaped
punctuation in inline TeX could lose its backslash, rendering a spacing command
as a comma and altering brace or norm delimiters. The bounded follow-up uses
[GitHub's protected inline-math syntax](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions)
for the 20 affected expressions in README, theory, compilers, and comparisons.
The TeX expressions themselves are byte-identical. No scientific code, formula,
data, or archived evidence changes. The follow-up receives the documentation
gate and direct GitHub rendering inspection; the full main run above remains
the validation of its unchanged executable and scientific-data tree.

## Visible math-error panels

A subsequent reader report exposed an error missed by the earlier automated
browser inspection: GitHub emits some math failures as a `flash-error` panel
inside `math-renderer`, rather than as `mjx-merror` or `MathJax_Error`. The
earlier absence of those two selectors was therefore insufficient evidence of
successful rendering. Direct inspection reproduced the canonical disjoint
tangent formula failure and six failures in its archived proof.

The canonical math now uses the TeX less-than command instead of a literal
less-than character. Four directly linked source documents have reproducible
reading copies under `docs/source-readings/`; their only content changes are
renderer-compatible mathematical markup. The original packets, source hashes,
historical manifests, and numerical evidence remain byte-identical. Active
proof links lead to the reading copies, which identify and expose their
original source text. `tools/render_source_readings.py --check` verifies the
exact derivation from pinned source hashes.

The documentation gate now checks fenced math as well as inline math for the
reported hazards. Regression cases cover the actual forbidden macro and
less-than failures. Browser review must check `math-renderer .flash-error`,
ordinary MathJax errors, and unfinished renderers, then inspect the affected
formulas visually. Source lint alone is not a successful rendering check.
