# PF-03 integration review

Review branch: `review/PF-03-integration`.
Pinned source: `8781c8fad5de5742b743178268b8e4f0e4b4f089` (completed PF-02).
Target at start: `main`, `da0d8c771350b695206b6f06194277538833adb4`.

## Decision scope

Recommend integrating the maintained repair, exact terminal compilers and the
negative PF-02 acceptance record after the read-only gate passes. No merge is
performed by this review. Actual verification is tied to the source commit in
RUN.json and the reviewed GitHub run receipt, not inferred from this text.

This is an implementation/integration review, not a new proof or novelty audit,
a parameter search, or an attempt to rescue the parity advantage claim.

## Findings and corrections

### 1. Round thresholds could select too few or too many rounds

PF-02 used ceil((log(beta-1)-log(2)-log(eta))/log(4)). Binary64 logarithm rounding
can cross a power-of-four boundary. Two reproduced examples for beta=2 are:

| eta | Old result | Minimum correct result |
|---|---:|---:|
| nextafter(1/32, 0), hex 0x1.fffffffffffffp-6 | 2 | 3 |
| 2**(-25), an exact threshold | 13 | 12 |

The maintained helper now compares integer ratios for the validated binary64
inputs, finding the least k with beta-1 <= 2 eta 4**k without a logarithm or
floating-point quotient. This also handles subnormal eta and large finite beta.
It does not certify a numerically estimated beta as a rigorous upper bound.

Oversized integer scalars such as beta=10**400 previously escaped as
OverflowError. They now raise ValueError consistently with the supported API.
The original real/finite array repair remains intact. Mathematical formulas,
measurement moments and terminal compilers are unchanged.

### 2. Reader-facing status had not incorporated PF-01 and PF-02

The root README, status, claim register, API guide and work order now distinguish
accepted restricted algebra, maintained input repair and failed finite parity
acceptance. The 144 scenarios and their 4320 cost rows are retained as historical
results under their original normalized-work and Markov-budget qualifications.
No global optimality, runtime advantage or novelty is implied by integration.

### 3. Historical write-enabled workflows were not suitable as the main gate

The completed one-time initialization/PF-01/PF-02 workflows are preserved byte
for byte as text in retired_workflows/. Their active workflow paths are removed.
One read-only workflow now validates review/main pushes and pull requests. It
uses contents: read, does not retain checkout credentials, and publishes logs
as artifacts even on failure. It never commits to any branch.

This follows GitHub's official minimum-token-permission and artifact guidance:
https://docs.github.com/en/actions/tutorials/authenticate-with-github_token
https://docs.github.com/en/actions/tutorials/store-and-share-data

## Reproduction and preservation

Six new test methods cover 1611 exact threshold/neighbor checks, 25 scalar-extreme
checks, 500 seeded exact-minimality checks, two oversized-scalar rejections,
unchanged estimator outputs, and CI configuration. Seed: 2026091568. These six
methods passed locally using byte-verified PF-02 adapter source and the supplied
archives. This local run is not the full remote suite.

The read-only integration gate additionally requires:

- all repository tests (the 30 inherited methods plus six new methods);
- existing PF-01 diagnostics and both supplied validators;
- the same PF-02 acceptance grid, compared row by row to its saved remote run;
- exact categorical results and 1e-12 relative/absolute numerical agreement;
- frozen Git trees and on-disk blobs before and after, and a clean checkout.

Frozen paths include all research, provenance, PF-01/PF-02 results, startup logs,
the historical initialization manifest, the terminal compiler and PF-02 tests.
New artifacts go only below runs/. No historical timestamp or numerical record
is overwritten. PACKAGE_MANIFEST.json remains the original initialization
snapshot; it is not presented as a live manifest after documentation updates.

The container cannot resolve github.com. Local checks therefore used supplied
archives and retrieved source verified against its Git blob SHA, rather than a
complete authenticated checkout. Full-tree and full-suite checks are performed
in the remote checkout. REMOTE_VALIDATION.json, when added after inspection,
identifies the actual completed run; logs remain in its artifact.

## Acceptance boundary

PF-02's prices and kernel-operation prescriptions are a fixed illustrative cost
model, not a measured instruction-level or hardware audit. Integration checks
preserve that model and its zero-parity-win result, not its universality. No
strongest-method advantage or PRL-readiness assessment is made here.

See DECISION.md for the merge-review disposition. Main and both source branches
remain unchanged; no release, license, manuscript or new research phase starts.
