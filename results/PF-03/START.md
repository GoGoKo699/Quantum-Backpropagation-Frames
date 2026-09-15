# PF-03 integration review

Status at this checkpoint: IN PROGRESS.

User authorization: proceed with the recommended integration review of PF-02.
This does not authorize a merge, release, license change, manuscript, new ansatz,
or an expanded advantage search.

Review branch: `review/PF-03-integration`.
Pinned source: `8781c8fad5de5742b743178268b8e4f0e4b4f089` (`repair/PF-02`).
Proposed merge target: `main`, starting at `da0d8c771350b695206b6f06194277538833adb4`.
No existing pull requests were present at start. The source and target branches
will remain unchanged; only the review branch receives corrections.

Scope: inspect the maintained API and compiler contracts, preserve PF-01/PF-02
reports and source archives, rerun the existing tests and the same bounded
acceptance grid, make integration-facing documentation and CI accurate, and
record a recommendation with an unmerged pull request if the review passes.

Container network access to github.com fails DNS resolution. The authorized
GitHub connection supplies remote state and writes. Local focused checks use
provided archives and byte-verified retrieved source, not an authenticated git
checkout. Full pinned-tree verification will run in GitHub Actions with a
read-only token and publish logs as artifacts; it must not auto-commit evidence
or change historical result files.
