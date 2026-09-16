# Repository working rules

Read README.md, docs/SCOPE.md, docs/THEORY.md, docs/COMPARISONS.md,
docs/EVIDENCE.md, and work_orders/CURRENT.md before changing this repository.
Explicit current user instructions take precedence.

## Scientific boundary

Preserve the freeze adopted in PF-08: the exact real pure single-copy universal-
unbiasedness theorem, its sparse attaining POVM, and existing charged local
realizations. No automatic new research workstream, broader sweep, manuscript,
release, registry publication, or submission follows from successful checks.
The strongest-method end-to-end advantage goal remains unmet; novelty is not
finally cleared. Disclose substantive errors and contain them before extending
or changing the theorem's assumptions.

Keep original coordinate normalization, complete classical output, access,
error norm, and confidence fixed in comparisons. Separate the all-POVM theorem
from conditional-unbiasedness frame/Walsh results; separate trace variance from
exact confidence complexity. Charge preprocessing, physical bits, storage or
regeneration, finite precision, and output. Numerical residuals are not proofs,
novelty certificates, hardware timings, or external peer review.

## Evidence and implementation

Preserve research/, results/PF-01 through results/PF-08, existing provenance
records and input ZIPs, validation snapshots, and historical manifests byte for
byte. The migration map is maintenance/repository-polish/MIGRATION.json.
Original run paths, dates, and hashes must not be rewritten as current runs.
Use isolated layouts for archived programs. New execution output belongs in a
fresh ignored runs/ directory; never overwrite historical results.

Use qbp_frames for supported imports. Changes copied from fixtures require an
explicit source map and equivalence tests. Do not weaken tests, tolerances, or
negative results to obtain green checks. Dense diagnostic paths and scalable
compiler paths must be distinguished.

## Validation and integration

Run python tools/check_docs.py for reader changes and the bounded full gate
python tools/validate.py --mode full --output runs/<new-name> for relevant code,
data, and final integration. Inspect outputs and logs. A local run is not
GitHub CI; validate the actual PR head and merged tree. CI remains read-only,
uses standard hosted runners, and never persists write credentials.

Use a working branch and reversible commits. Preserve remote source branches
and history; never force-push. Merge only under explicit task authority and
passing required checks. The repository-furnishing task authorizes its own
reviewed merge; it does not authorize new science or a release.

## Reader experience

Lead with the physical task, example, theorem, measurement, realization, and
limitations. Keep full arguments in canonical Markdown. Use GitHub math blocks,
short equations, stable relative links, and no math in headings. Keep engineering
migration details and AI assistance disclosure in methods/provenance routes.
Do not insert approvals, chat checkpoints, journal targets, or model handoffs
into the primary scientific route.
