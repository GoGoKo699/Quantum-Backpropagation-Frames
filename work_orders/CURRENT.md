# Current work order

**ID:** PF-03  
**Title:** Integration review of the completed PF-02 repair  
**Branch:** review/PF-03-integration  
**Baseline:** 8781c8fad5de5742b743178268b8e4f0e4b4f089

Scope authorized by the user: inspect and prepare the repair and negative
acceptance record for integration, without merging or expanding the research.
See results/PF-03/START.md, REPORT.md, and DECISION.md. Remote verification is
identified separately in REMOTE_VALIDATION.json once checked.

The integration gate must pass the full test suite, frozen-source checks,
supplied diagnostics and an unchanged rerun of all 144 PF-02 scenarios and
4320 candidate rows. Read-only CI publishes artifacts, not evidence commits.

Corrections: exact round-threshold selection, consistent ValueError for scalars
outside the supported range, current reader-facing status, and one maintained
CI gate. Original research, provenance, PF-01/PF-02 reports, compilers and priced
acceptance code remain unchanged.

Stop after a recorded integration recommendation and an unmerged pull request.
Main, audit/PF-01 and repair/PF-02 remain untouched. No release, license change,
manuscript, new ansatz, broader sweep or new theoretical claim is authorized.
Any next scientific task or merge requires explicit authorization.
