# Repository startup report

Date: 2026-09-15. This report documents repository initialization, not an
independent mathematical review of the supplied scientific derivation.

## Import and integrity

Both original input ZIPs were retained byte-for-byte. Every extracted file
matches its archive entry: 22 files across two packets. All 20 entries in the
supplied SHA256 manifests match. The inherited parity reference_circuit.py is
byte-identical to the matched audit core.py, and its provenance identifies the
correct source archive.

See `integrity.json` and `../../provenance/INPUTS.json`.

## Environment

- Python: 3.13.5
- NumPy: 2.3.5
- BLAS/OpenMP thread limits for diagnostic subprocesses: 1
- Main parity seed: 2026091551
- Main matched-validator seed: 2026091532
- New bounded smoke-test seed: 2026091552

## Executed commands

```text
python tools/verify_inputs.py --json validation/bootstrap/integrity.json
python -m unittest discover -s tests -v
python tools/reproduce.py parity --output validation/bootstrap/parity
python tools/reproduce.py matched --output validation/bootstrap/matched
```

All succeeded. The new repository suite contains nine tests. Logs and diagnostic
JSON are retained alongside this report. The wrapper copied packet files to
temporary directories and checked source identity again after each run.

### Complete supplied parity validator

Eight check groups passed. They include 75 complete-ensemble cases, 48 linear
phase-equivalence cases, 37,448 basis-input gadget checks, 288 rank-witness
cases, 1,332 shifted-decoder comparisons, 20 representation/eigenframe cases,
four fixed-measurement constraint-rank checks, and 15 non-Hopf risk examples.

Maximum covariance-interpolation residual:
`1.9761969838327786e-14`.

Maximum rank-witness formula residual:
`6.0254023992456496e-12`.

These are floating-point residuals, not symbolic or interval certificates.

### Supplied matched-readout validator

Six residual groups passed: grouped reverse-test means and second moments,
block-shadow means and second moments, and two aggregate-first identities.
The block checks enumerate the supplied one-, two-, and three-qubit stabilizer
ensembles of sizes 6, 60, and 1,080.

Largest reported residual:
`1.2434497875801753e-14`.

The wrapper checks that residuals are finite and no larger than `1e-8`; it also
checks the declared group and stabilizer counts. No full comparison-table
regeneration was requested or claimed. The matched proof/cost comparison is
still inherited evidence rather than a new scientific audit.

## Not executed or established

No new theory campaign, current-literature novelty search, hardware run,
remote repository creation, remote CI execution, commit, push, license
selection, or release occurred. No absent previous experiment was recreated
from prose. Importing and reproducing tests does not establish the project's
ultimate end-to-end advantage goal.

## Next action

Create the new private remote and import the starter. Record the actual remote
commit before scientific work. Then execute the bounded PF-01 audit, preserving
this startup report and the original packets.
