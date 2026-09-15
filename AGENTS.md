# Research workspace instructions

Read README.md, docs/SCOPE.md, docs/STATUS.md, docs/CLAIMS.md, and
work_orders/CURRENT.md before work. These files provide project context;
explicit current user instructions take precedence.

## Scientific discipline

Keep the complete classical gradient and the stated error norm fixed during
comparisons. Do not silently weaken assumptions, change parameter normalization,
replace whole-vector accuracy by coordinatewise variance, or supply preprocessing
or oracle access for free. Separate algebra, finite computation, asymptotics,
novelty, logical cost, and hardware claims.

The source packets are working evidence, not blanket proof certificates.
Results must be self-contained: state their assumptions and cite the scientific
sources actually used. Do not frame the project as an extension of, or contrast
with, another ansatz merely because that work inspired the discussion.
Earlier conversation-level claims have not all been imported. Do not invent
missing files, tests, source matches, external review, or remote operations.

## Files and reproducibility

- Preserve provenance/input_archives and the imported research directories
  byte-for-byte. Their hashes are recorded in provenance/INPUTS.json.
- Reproduce imported scripts through tools/reproduce.py, which uses isolated
  copies. Never overwrite imported validation.json files with a rerun.
- Put new scientific changes on a descriptive branch. Preserve interim reports,
  source versions, seeds, commands, and negative results. Do not force-push.
- New experiments belong in a new explicit workstream directory. A later
  migration to a shared package needs a file map and equivalence checks.
- Run the integrity and repository tests before reporting completion.
- A local test is not a GitHub Actions run. A small residual is not an interval
  proof or novelty check. Inspect logs and outputs, not just process exit codes.

## Authority and work bounds

Work only in the repository and branch authorized for the current task. No public release, tag,
license selection, or manuscript is implied by this import. Execute the current
bounded work order and report its status rather than expanding into unrelated
research. For requested remote changes, confirm real repository and branch
state through the available connection; never infer successful writes.

## Reporting style

State the task, concrete result, evidence, limitation, and next decision. Explain
operations before abstract labels when it improves understanding. Preserve all
scientific qualifications. Use standard GitHub math blocks in new documents;
avoid fragile math in headings. Do not rewrite unchanged source artifacts merely
to make their style uniform.
