# Repository setup

Repository: `GoGoKo699/Quantum-Backpropagation-Frames`.

The repository description is:

> Frame-based quantum gradient readout: representation theorems,
> parity-phase compilation, and reproducible resource analysis.

The default branch is `main`. Original code and associated documentation use
the [MIT License](LICENSE), Copyright (c) 2026 Ruge Lin. No release or version
tag has been created by adding the license. Visibility and public-readiness
must be verified separately; a license is not a security review.

## Use an existing checkout

```bash
git clone https://github.com/GoGoKo699/Quantum-Backpropagation-Frames.git
cd Quantum-Backpropagation-Frames
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python tools/verify_inputs.py
python -m unittest discover -s tests -v
```

Use normal authorized GitHub authentication. No credentials are included here.
Record `git rev-parse HEAD` and `git status --short` before scientific work.
Start the bounded work order on a new descriptive branch; do not force-push.

The original starter's creation-pending notes are historical. Current scope and
status are in `docs/SCOPE.md` and `docs/STATUS.md`. The archive hashes in
`provenance/INPUTS.json` identify the scientific input independently of the
repository commit.
