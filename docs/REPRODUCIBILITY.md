# Reproduce and verify

[Home](../README.md) · [Tutorial](TUTORIAL.md) · [Implementation](IMPLEMENTATION.md) · [Evidence](EVIDENCE.md)

The quickstart runs a complete small readout example. The full gate checks the
supported package, every inherited bounded diagnostic suite, the unchanged
acceptance grid, preserved evidence identities, and the scientific figure.
These are numerical and engineering checks alongside the [proof](THEORY.md),
not independent proof or a novelty certificate.

## Clean installation and smoke path

Use a full clone for verification; a source ZIP lacks the Git history required
by the inherited integrity gate. The package itself needs NumPy. A virtual
environment keeps installation separate from your existing environment.

```bash
git clone https://github.com/GoGoKo699/Quantum-Backpropagation-Frames.git
cd Quantum-Backpropagation-Frames
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install --no-deps .
python examples/flat_readout.py
python examples/compile_large.py
```

The small example prints `checks: passed`, target gradient
`[0, 1, 0, 0, 0, 1]`, zero-score probability `0.375`, trace risk `13`,
minimax risk `16`, and the no-mask benchmark `24`. Its illustrative 16-record
average is deliberately a finite sample, so it need not equal the target.

The larger example uses 128 system qubits and 384 original parameters. It emits
1,658 logical gates, including 891 controlled-X and 764 full-angle rotations,
and reports minimax risk `1528` against the no-mask benchmark `1536`.
It is a compiler demonstration; it does not allocate or simulate a 128-qubit
state, execute hardware, or establish a runtime advantage.

Python 3.12 is used for local checks and Python 3.13 for the GitHub workflow.
The recorded environment in each run identifies what actually executed.
No broad platform or hardware compatibility claim follows from these checks.

## Full bounded verification

Install the extra validation and figure dependencies, then choose a new output
directory. The checkout must be clean; committed edits and ignored `runs/` or
virtual-environment directories are fine.

```bash
python -m pip install -r requirements-dev.txt
python tools/validate.py --mode full --output runs/full-check
```

Read `runs/full-check/RUN.json` and the named logs. A successful run prints
`"status": "passed"`, the exact source commit/tree, test coverage, source
identities, and the acceptance results. Timing depends on the machine; the
inherited suites take tens of seconds in the recorded local environment,
excluding installation. No new search is run.

| Check | What it establishes |
|---|---|
| Repository tests | Existing repairs, supported interfaces, maintained/archive equivalence, and validation failure boundaries |
| Original input verifier | The two ZIP archives match their extracted files and supplied manifests |
| Inherited integration gate | At least the original 36 tests; original 109 frozen identities; imported parity/matched diagnostics; round-threshold repair |
| Acceptance regression | All 144 scenarios and 4,320 candidate rows agree with the preserved run |
| Measurement diagnostics | Original boundary study and independent audit: 8 and 10 check groups |
| Circuit diagnostics | Original disjoint and interval compiler suites: 17 and 26 check groups |
| Fixed-data analysis | 8 analysis tests on 30 regenerated small cases and 10 compiler-only cases |
| Current migration inventory | Preserved research packets, source archives, records, and copied guidance retain their recorded hashes |
| Figure and examples | Deterministic figure/data regenerate byte-for-byte; both supported examples execute |
| Reader routes | Active local links/anchors, code fences, MIT text and required citation fields |

The acceptance comparison requires identical categories and retains the
original absolute and relative numerical tolerance of `1e-12`. The unchanged
winners are 96 full-direct, 24 full-greedy and 24 no-mask; positive-round parity
wins zero scenarios. Each original scientific suite retains its own declared
tolerance. These checks do not select new cases or prices.

Errors stop validation with a nonzero exit code and a failed run record whenever
the output directory was created. The record names the failed command/log.
An existing output directory is rejected, preserving prior runs. Never edit an
original result or loosen a tolerance to make a rerun pass.

## Focused checks

For active documentation edits, no scientific sweep is necessary:

```bash
python tools/check_docs.py
python tools/validate.py --mode docs --output runs/docs-check
```

The second command also verifies the current migration inventory and original
packet manifests. Source checks do not establish successful GitHub rendering;
visual inspection is recorded separately in the engineering report.

To rerun the imported validators in isolated compatible layouts:

```bash
python tools/reproduce.py parity --output runs/parity-check
python tools/reproduce.py matched --output runs/matched-check
```

The wrapper copies each original packet into a temporary directory, runs it
there and saves fresh output. Its original `validation.json` remains intact.
The optional `matched-full` mode also regenerates the already supplied matched
comparison tables; it is not required by the main gate.

## Figure and table provenance

The one explanatory figure uses analytic probabilities and risks, not sampled
data. Its JSON companion includes the exact source-proof hashes and plotted
values. Regenerate it with:

```bash
python figures/generate_tutorial.py --output runs/figure-check
```

The full gate compares both new files byte-for-byte with
[`tutorial-readout.svg`](../figures/tutorial-readout.svg) and
[`tutorial-readout.json`](../figures/tutorial-readout.json), using the pinned
figure dependencies. Original numerical tables remain under their stable
[evidence paths](EVIDENCE.md); the complete gate regenerates the acceptance
tables and fixed final cost analysis from their original programs.

## Continuous integration and durable evidence

The single [validation workflow](../.github/workflows/validation.yml) runs on
pull requests and pushes to `main`; a manual dispatch forces the full gate.
It always produces the same `validate` job, so documentation-only changes do
not leave a required job pending. Documentation changes get link/license and
identity checks; executable, data, dependency and workflow changes run the full
gate. Feature-branch pushes do not duplicate pull-request runs.

The workflow uses a standard hosted runner, a read-only token, no persistent
write credentials and no automatic commits. Retired write-enabled workflows
remain historical text. Actions logs are useful receipts but expire: source
packets, original numerical records and compact identity manifests are retained
in the repository. A local pass and a historical CI pass are not a CI pass for
a changed tree. See the [engineering record](../maintenance/repository-polish/REPORT.md)
for the actually executed final commands and remote runs.
