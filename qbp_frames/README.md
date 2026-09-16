# Maintained Python interface

Install with `python -m pip install .` from the repository root, then import
`qbp_frames`. NumPy is the only runtime dependency.

See the canonical [implementation guide](../docs/IMPLEMENTATION.md) for supported
interfaces, parameter order, bit conventions, strict input contracts, numerical
limits, examples, and resource accounting. See [reproduction](../docs/REPRODUCIBILITY.md)
for the complete validation route.

The numerical and circuit source packets remain immutable evidence. Supported
imports use package-local modules and do not require a checkout of those packets
at runtime. The private parity reference copy preserves its original bytes;
validation is provided by `qbp_frames.parity`.
