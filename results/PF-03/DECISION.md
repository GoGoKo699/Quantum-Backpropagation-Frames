# PF-03 integration decision

**COMPLETE. READY FOR MERGE REVIEW. The read-only integration gate passed;
no merge has been performed.**

Verified run: 34963997457, job 104364016530, source commit
739a84854e467450586fc07493171152c418f205. See REMOTE_VALIDATION.json for the
reviewed receipt, source hashes and artifact identity.

The merge candidate preserves PF-01/PF-02 history, original logs, input archives,
the maintained real/finite API, and exact terminal-readout compilers. PF-03 fixes
scalar conversion and minimum-round boundary selection, then updates current
status and CI. Estimator mathematics and the declared cost model are unchanged.

The complete gate passed: 36 test methods, PF-01 diagnostics, both supplied
validators, 109 frozen-file checks, and unchanged 144-scenario/4320-row PF-02
acceptance results. The checkout was clean before and after. Subsequent changes
to code require revalidation; passing metadata-only commits do not change the
recorded scientific conclusion.

The inherited winners remain 96 full-direct, 24 full-greedy and 24 no-mask.
Zero positive-round parity wins is retained, not converted into a success or a
universal no-go theorem. The result remains limited to the specified sufficient
budgets, cases and work model.

Open an unmerged pull request to main. Main, audit/PF-01 and repair/PF-02 remain
untouched. The next operational decision is authorization to merge the reviewed
candidate. A new scientific study requires a separate justified work order;
this review does not start a sweep, manuscript, release or licensing action.
