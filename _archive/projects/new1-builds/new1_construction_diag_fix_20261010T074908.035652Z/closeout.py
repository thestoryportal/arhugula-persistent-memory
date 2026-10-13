"""Write build-only final manifest; consumes prior static audit and helper review."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(os.environ['LLMDB_ROOT']).resolve()
HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


baseline = json.loads((HERE / 'baseline.json').read_text())
audit = json.loads((HERE / 'audit.json').read_text())
helper = (HERE / 'helper_review.md').read_text()
assert 'PROCEED' in helper and 'not binding Astra' in helper, 'helper review missing/cannot be promoted'
for name, expected in audit['owned_sha256'].items():
    assert sha(ROOT / name) == expected, ('changed after static audit', name)
for name, expected in audit['green']['sha256'].items():
    assert expected in helper, ('helper did not bind tested source', name)
assert audit['test_total'] == 165 and audit['protected_unchanged_count'] == 16
assert audit['prior_evidence_unchanged_count'] == 26
launch = (HERE / 'launch_command.txt').read_text().rstrip('\n')
assert launch == audit['launch_command']
assert audit['owned_sha256']['results/mathlab_staging/new1_construction_diag_scope.md'] in launch
assert audit['owned_sha256']['tools/new1_construction_diag.py'] in launch
checkpoint = f'''# MB5 Task 3 context checkpoint — {datetime.now(timezone.utc).isoformat()}

Done: reproduced Astra r1 finding 3 under the real watchdog before production changes; cancellation-safe creation/registration, explicit post-registration release, independent 5-s launch bound, parent/deadline liveness guard, all four GREEN suites, append-only scope revision, source/static audit, read-only helper review and revised pinned launch.
In flight: none after final readback. No real diagnostic was run.
Exact deliverables: tools/new1_identity_diag.py; tools/new1_construction_diag.py; tests/test_new1_construction_diag.py; results/mathlab_staging/new1_construction_diag_scope.md.
Fresh receipts: {HERE.relative_to(ROOT)}/. Original build directory remains untouched, exact 26-file/hash match.
Tests: 165 PASS (43 construction + 27 identity + 34 geometry + 61 supervisor), 9.225 s, command wall 9.531034583 s, exit 0. Final tested SHAs: {json.dumps(audit['green']['sha256'], sort_keys=True)}.
Scope SHA: {audit['owned_sha256']['results/mathlab_staging/new1_construction_diag_scope.md']}.
Next: MAESTRO4 submits the exact candidate to binding GPT-6-Astra re-review, then alone performs a single approved launch from launch_command.txt with fresh admission and namespace. The prior Astra NO-GO is preserved; helper PROCEED is build-only and not binding Astra.
Open risks: full-size L4 numeric/native runtime, actual input hashes/admission/RSS/threads/backend and host niceness adjustment remain NOT RUN / UNVERIFIED. No retry, arithmetic/gate/cap/output/outcome amendment or result repair is authorized. Preserve original HALTs and concurrent worktree changes.
Restrictions persist: no commit/push/merge/deletion/launchd/network/Drive/Graft/model/MPS, protected docs, git tool family, .github or dashboard-test edits. No global memory updates.
BINDING context directive (operator 2026-10-09): watch Context N% left in every root/team session. Before approximately 20%, stop starting new work, write done/in-flight/exact paths/next step/open risks into the relevant report, notify the orchestrator and request a fresh successor. Every handoff restates this rule; never approach full-window compaction.
'''
(HERE / 'context_checkpoint.md').write_text(checkpoint)
receipts = {str(path.relative_to(HERE)): sha(path) for path in HERE.rglob('*')
            if path.is_file() and path.name not in ('final_manifest.json', 'readback.json')}
proof = {'schema': 'new1-construction-diag-launch-fix-build-only-v1',
         'utc': datetime.now(timezone.utc).isoformat(),
         'status': 'BUILD-GREEN; LIVE-NOT-RUN; BINDING-REVIEW-PENDING',
         'scope_revision': '2026-10-10 MAESTRO4/Astra r1 finding 3',
         'baseline_owned_sha256': baseline['owned_sha256'],
         'final_owned_sha256': audit['owned_sha256'],
         'identity_old_sha256': baseline['owned_sha256']['tools/new1_identity_diag.py'],
         'identity_new_sha256': audit['owned_sha256']['tools/new1_identity_diag.py'],
         'test_counts': audit['test_counts'], 'test_total': audit['test_total'],
         'green_receipt': {'path': 'green_third.json', 'sha256': sha(HERE / 'green_third.json'),
                           'log': 'green_third.log', 'log_sha256': sha(HERE / 'green_third.log'),
                           'test_elapsed_s': 9.225, 'command_wall_s': audit['green']['elapsed_s'], 'exit_code': 0},
         'red_receipts': ['red_launch.log', 'red_complete.log', 'red_exited_cleanup.log', 'red_released_liveness.log'],
         'static_audit': audit, 'helper_review': {'path': 'helper_review.md', 'sha256': sha(HERE / 'helper_review.md'),
                                               'scope': 'read-only GPT-family second reader; not binding Astra'},
         'launch_command': launch, 'launch_executed': False,
         'input_pins_rehashed': False, 'real_admission_run': False,
         'real_numerical_measurement_run': False, 'host_nice_adjustment_verified': False,
         'prior_build_directory_untouched': True, 'protected_files_unchanged': True,
         'git_mutations': False, 'receipt_sha256': receipts,
         'build_receipt_budget_bytes': baseline['disk_budget_bytes'],
         'baseline_free_bytes': baseline['free_bytes'],
         'context_checkpoint': 'context_checkpoint.md'}
rendered = (json.dumps(proof, indent=2) + '\n').encode()
size = sum(path.stat().st_size for path in HERE.rglob('*') if path.is_file() and path.name != 'final_manifest.json')
assert size + len(rendered) + 16384 < baseline['disk_budget_bytes'], 'build receipts exceed planned budget'
proof['planned_final_receipt_bytes_below'] = size + len(rendered) + 16384
(HERE / 'final_manifest.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps({'final_manifest_sha256': sha(HERE / 'final_manifest.json'),
                  'scope_sha256': audit['owned_sha256']['results/mathlab_staging/new1_construction_diag_scope.md'],
                  'test_total': audit['test_total'], 'launch_command': launch,
                  'planned_final_receipt_bytes_below': proof['planned_final_receipt_bytes_below']}, indent=2))
