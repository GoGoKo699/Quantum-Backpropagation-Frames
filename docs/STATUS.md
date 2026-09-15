# Current status

**Date:** 2026-09-15.  
**Stage:** Private repository initialization from preserved source packets.  
**Research status:** Working derived result with reproduced finite diagnostics;
no external proof review, exhaustive novelty clearance, or established
end-to-end advantage over the strongest comparator.

## Available baseline

The exact bytes of two supplied ZIP files and their 22 extracted files are
preserved. Their 20 supplied content-hash entries and inherited circuit-fixture
identity were checked. Source identities are in `provenance/INPUTS.json`.

The parity packet is the current candidate theorem and implementation. The
matched-readout audit is a comparator fixture, not a performance claim for a
hard application. Both use dense calculations for small diagnostic cases;
this import does not reconstruct absent large-system compiler experiments.

## Original starter validation

See `validation/bootstrap/REPORT.md` for the actual run scope and artifacts.

| Item | Status |
|---|---|
| Archive and extracted-file integrity | Passed |
| New repository/wrapper tests | 9 passed |
| Supplied parity validate.py | Passed; 8 check groups |
| Supplied matched validate.py | Passed; 6 residual groups |
| Regeneration of all matched comparison and cost tables | Not executed in bootstrap |
| Remote GitHub CI | Configured, not executed |
| Remote state during original starter preparation | Not created at that earlier stage |
| New literature search or scientific extension | Not performed in bootstrap |

The reruns took place in temporary copies. Original validation.json files and
source hashes were not changed. The new wrapper also rejects nonfinite or
out-of-tolerance reported residuals in the matched validator, which otherwise
reports some values without final numerical assertions.

## Initialization update

The user has created the private remote. The project framing has been corrected
to describe a self-contained research problem; the source packets are unchanged.
Fresh initialization checks are recorded under `validation/initialization/`.
GitHub Actions outcomes must be checked against the actual remote commit.

## Next work

Execute work_orders/CURRENT.md after recording the real repository baseline.
It is a bounded independent proof/novelty/matched-cost audit. It has not been
completed by reproducing the existing code.

## Not established

The 4 tr(G) benchmark is not universal measurement optimality. The phase-rank
witness is not a general CNOT lower bound. No novel primitive, hardware speedup,
noise robustness, trainability, or guaranteed PRL outcome is claimed. Earlier
spectral/coherence assertions are not promoted into the verified baseline.
