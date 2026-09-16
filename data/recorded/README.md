# Recorded fixed-data evidence

These compact files were recovered byte-for-byte from retained GitHub Actions
artifacts, whose SHA-256 values match the original remote receipts. They are
historical outputs, not new runs and not regenerated replacements.

- [Overlap diagnostics](PF-07/diagnostics.json) and
  [example program](PF-07/example_program.json): artifact 10407601098,
  run 34995694899, source commit 7f9e9c0aadeba872af8012691e88a47df5c9a361.
- [Fixed comparison](PF-08/summary.json), [small table](PF-08/small_comparison.csv),
  [scaling table](PF-08/scaling_tradeoff.csv), and
  [quantum-only projection](PF-08/quantum_projection.json): artifact 10425249412,
  run 35042241177, source commit a16593730f570a33fb6c2ee6da6fd94ad4ac7500.
  [Its exact input](PF-08/input_pf07_diagnostics.json) preserves that run's metadata.

[The migration manifest](../../maintenance/repository-polish/MIGRATION.json)
records each original archive member, archive hash, destination, and file hash.
Current reproduction writes fresh outputs under runs/ and never edits these
records. Source packet paths, dates, and hashes remain untouched.
