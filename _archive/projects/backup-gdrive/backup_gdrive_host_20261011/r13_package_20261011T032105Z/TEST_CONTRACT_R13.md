# MB45 frozen behavioral test contract

Written before r13 implementation. RED uses byte-identical K12 candidate.py and
check_plan.py in before/. For staged/commit controls ONLY, the RED adapter calls
K12's existing verify, whose working-tree acceptance is the defect. PR binding
and gate-report helpers are absent in K12: their REDs are assertion failures on
missing APIs (exit 2), explicitly distinct from contamination accepted (exit 0).
No assertion is weakened for GREEN; required refusals must exit 1 with the
named reason. New clean staged/commit/PR controls must pass. All 27 unmodified
K12 methods also run against r13's candidate/checker and copied accepted inputs.

Every synthetic git repository and its local bare origin lives in a mktemp
directory under /private/tmp; only those repositories permit writing git.
/usr/bin/python3 -B, isolated HOME and BACKUP_TEST_NO_RCLONE=1 are mandatory.
No real candidate, network, native launch or Drive acceptance is claimed.
Budget: all copied receipts plus tests and temporary Git trees under 100 MB.

Plan v4 must contain each of the eleven integration rows in exact order, with
the binding check immediately preceding the merge gate and the gate comparison
immediately afterward. Missing/empty/reordered rows fail. Historical v3 and
single-row K12 checker controls retain their accepted r12 semantics.
