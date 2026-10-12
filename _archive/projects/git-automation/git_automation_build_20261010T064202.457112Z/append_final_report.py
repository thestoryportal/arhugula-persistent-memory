"""One-time report assembly from recorded build evidence; no Git actions."""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

root = Path.cwd()
rel = Path("results/git_automation_build_20261010T064202.457112Z")
out = root / rel
B = chr(96)


def read(name):
    return json.loads((out / name).read_text())


def link(name):
    return f"[{name}]({rel.name}/{name})"


ci = read("assetfree_ci_r2.json")
h = read("real_hygiene_final_stdout.json")
g = read("real_gate_final_stdout.json")
scope = read("scope_audit.json")
dry = read("real_dry_final_snapshot.json")
assert ci["hashes"] == ci["snapshot_owned_hashes"]
assert all(hashlib.sha256((root / p).read_bytes()).hexdigest() == sha for p, sha in ci["hashes"].items())
assert [step["exit_code"] for step in ci["steps"]] == [0, 0, 0]
for number, count in ((1, 56), (2, 80)):
    log = (out / f"assetfree_ci_r2_{number}.log").read_text()
    assert re.search(rf"Ran {count} tests in [0-9.]+s\n\nOK\n$", log)
    assert len(re.findall(r"(?m)^test_", log)) == count
    assert "Traceback" not in log and "\nFAILED" not in log
    assert ci["steps"][number]["test_summary"][0][0] == str(count)
assert not h["ok"] and not g["ok"] and h["actions"] == [] and g["merge_sha"] is None
assert all(dry["unchanged"].values())
assert "Final verdict: **PROCEED" in (out / "astra_final_review.md").read_text()

parts = [f'''
## Final build acceptance — GIT AUTOMATION BUILD DONE

Recorded {datetime.now(timezone.utc).isoformat()}. **136/136 asset-free CPU tests PASS (56 automation + 80 repository); generated-state check PASS.** Final exact CI command sequence: **{ci["total_wall_s"]:.3f} s** locally against the workflow **480 s / 8 min** job cap. This is measured macOS Python 3.11.16 / Apple Git 2.54.0 evidence; Linux Actions startup/runtime remains UNVERIFIED. No real commits, pushes, merges, branch deletions, worktree removals, fetches, or conflict resolutions were performed by MB4. Test mutations were confined to disposable bare remotes/clones/worktrees under /private/tmp.

### Final design and MAESTRO operating contract

{B}tools/git_hygiene.py{B} defaults to one dry run. Apply performs one origin fetch, inventories local and freshly advertised remote branches, and requires complete bounded open-PR protection evidence. MERGED means the tip is an ancestor of the reviewed origin/master. Master/remote default, attached worktree branches, and open PR heads remain protected. UNMERGED branches are reported with unique-commit count/date/remote presence and are never deleted. Unknown remote/PR/process visibility refuses admission.

Worktrees are separately eligible only when merged, fully clean (including untracked, ignored and submodule content), unlocked, non-current, non-default, non-detached, non-PR, and without any observed process cwd inside. Removal is nonforce; prune happens once only after an admitted removal. Branches are then reclassified. Per-worktree disk bytes are retained before/after; original and completed action evidence survive a later refusal. A second successful apply has no cleanup actions, although each explicit apply still performs its one fetch.

Local deletion uses {B}git branch -d{B} with a temporary invocation-only reference-transaction guard. Git supplies zero old OIDs for this deletion; the prepared hook reads the actual tip while Git holds the ref lock and compares it with the reviewed SHA. The existing configured hook is chained with its state/input and veto respected. Remote deletion uses {B}git push origin --delete{B} with a temporary pre-push guard requiring the advertised old SHA and only the requested deletion; receive-pack also compares that advertised old OID atomically. The existing pre-push hook is chained; persistent hooks/config are not rewritten. Branch rechecks refresh remote/master, PR protection, attachments and tip without repeating full branch metadata/disk scans for each branch. Five-branch fixture cleanup performs at most three full inspections.

{B}tools/git_merge_gate.py{B} is the MAESTRO merge entrypoint: OPEN same-repository PR targeting master; immutable head/base recorded; current-root engine fingerprint and committed-head engine fingerprint; current master included in the head; only master + live attached worktree branches + selected PR branch; all exact-head current checks/statuses and latest workflow runs terminal-success, including required CI/cpu linked to the actual run. No checks means not-started and bounded backoff, never green. Head/base/master/mergeability are rechecked after the final inventory immediately before server-side {B}gh pr merge <n> --merge --match-head-commit <sha>{B}. Draft ready happens only after preconditions pass. Dirty unrelated WIP does not prevent a server-side merge. Conflicts/unknown mergeability refuse for operator resolution.

After the server returns an exact-head merge commit and master points to it, master push CI is verified separately on that merge SHA, with native cpu linkage to that CI run. Only then does the gate execute one hygiene apply. A red master run or cleanup refusal exits nonzero with the recorded merge SHA; nothing automatically retries, re-runs, resolves conflicts or rolls back. A common-dir nonblocking lock serializes cooperating apply invocations. {B}GIT_OPTIONAL_LOCKS=0{B} prevents read-only status index refresh. Stdout is JSON; stderr lists checks/classifications and one final PASS/REFUSE reason.

| Bound | Frozen value |
|---|---|
| Hygiene default total deadline | 300 s |
| Merge gate default total deadline | 1200 s |
| Per CI phase wait | 480 s, also bounded by total deadline |
| Per subprocess | min(30 s, remaining deadline), then process-group termination and <=2 s reap |
| CI backoff | 1, 2, 4, 8, then at most 10 s; finite monotonic deadline |
| REST inventory pagination | At most 20 pages of 100; cap reached refuses incomplete evidence |
| Actions job | 8 min, one CPU job |

Timing CLI arguments must be finite, positive and <=1200 s; invalid inputs yield JSON plus one-line refusal before dispatch. There are no schedules, cron/launchd services, daemons, watchers, workflow chains or automatic retry loops. MAESTRO runs one hygiene apply and one merge-gate apply at arc closeout; these commands were **not executed on the real repo** in this build:

~~~sh
LLMDB_ROOT="$PWD" python3 -B -S tools/git_hygiene.py --apply
LLMDB_ROOT="$PWD" python3 -B -S tools/git_merge_gate.py 21 --apply
~~~

The only-path rule is a MAESTRO operating contract. Canonical CLAUDE/AGENTS/permission changes are MAESTRO-owned and were not edited by this builder. Client checks/locks cannot atomically prevent independent external master writes, newly opened PRs, or a process entering a worktree after observation. Server-enforced branch protection, private/free-plan/403 claims, live Actions and PR #21 state are UNVERIFIED here because GitHub access failed.

### RED / GREEN audit

| Receipt/log | Observed result |
|---|---|
''']
for name, desc in [
    ("red", "42 FAIL before both implementation modules existed; production absence recorded before/after"),
    ("green_attempt_1", "42 tests, 1 FAIL: wrong-post-master fixture moved the base before merge; fixture corrected, no production workaround"),
    ("red_r2", "2 targeted tests, 1 FAIL: gh exit-1 no-checks must enter bounded not-started polling"),
    ("green_r2", "45 PASS, 31.623 s"),
    ("red_r3", "10 targeted cases; 22 failing assertions/subtests and 2 errors; production hashes unchanged"),
    ("red_r3_cli", "1 isolated CLI case, 15 failing subtests; empty temporary root, production unchanged"),
    ("green_r3", "54 tests, 5 FAIL: local guard assumed nonzero hook old OID; not acceptance"),
    ("green_r4", "54 PASS, 44.505 s after actual hook-interface diagnosis"),
    ("red_r5", "3 cases, 5 failing subtests: wrong CI-run cpu links and unreadable/deleted lsof placeholders; real child control passed"),
    ("green_r5", "56 PASS, 44.408 s"),
    ("assetfree_ci", "State PASS; 56+80 PASS, 47.438 s; first exact workflow snapshot"),
    ("assetfree_ci_r2", f'State PASS; 56+80 PASS, {ci["total_wall_s"]:.3f} s; final refreshed source snapshot'),
]:
    parts.append(f"| {link(name + '.json')} | {desc} |\n")
parts.append(f'''

All RED receipts retain pre/post source hashes. Initial module-absence RED, targeted regression RED and final GREEN were observed before acceptance. The initial invalid-CLI regression also performed unintended read-only inventory on the real root before validation existed; it was narrowed to a temporary empty root before implementation. No apply/merge was dispatched. Only the final dry-run snapshot proves unchanged index bytes/mtime; earlier dry runs were not qualified for optional index refresh.

The actual zero-old-OID diagnosis is {link("local_hook_diagnostic.json")}. Regressions exercise advanced remote tips before advertisement and during receive; advanced local unmerged tips; custom hook veto; dirty/ignored/submodule/in-use worktrees; complete PR pagination; absent/pending/failed/conflicting checks; moved head/base; extra merged/unmerged branches; candidate engine changes; separate red master CI; preserved WIP; dry-run immutability; idempotent cleanup; final-verification error retention; CLI deadlines; both workflow branch filters; disabled optional index locks; and bounded full inspection count.

A fresh GPT-6-Astra reviewer inspected source/receipts and closed eight findings with **PROCEED — build/fixture acceptance** in {link("astra_final_review.md")}; {link("astra_design_review.md")} records the design review. This is a GPT-family fallback with weaker independence, not cross-family approval or a binding program ruling. Initial {B}claude auth status{B} probe returned exit 1 and {B}loggedIn:false{B}; no authenticated Claude review was claimed. Reviewer changed only its two review artifacts. The final refreshed CI snapshot retains the same four approved source hashes.

Primary references: [GitHub commit statuses](https://docs.github.com/en/rest/commits/statuses) returns status rows without a SHA field; the status URL is bound to the requested immutable SHA. [Git reference-transaction hooks](https://git-scm.com/docs/githooks) documents locked prepared transactions. [Linux lsof source](https://raw.githubusercontent.com/lsof-org/lsof/master/lib/dialects/linux/dproc.c) emits unreadable-cwd placeholders; production rejects paths that do not resolve to actual directories. The real lsof child positive control scopes only its test runner to self+child; production remains global and refuses incomplete visibility.

### CI selection and exact pins

Triggers are only push branches [master] and pull_request branches [master]. Pull-request checkout explicitly uses the PR head SHA. One ubuntu-24.04 CPU job has timeout 8 minutes, Python 3.11, thread limits 1, empty CUDA device selection and bytecode suppression. Every Python command uses -B -S, disabling all site packages; no pip dependency installation, model or GPU is needed. Git and lsof must be present.

| Selected command (each with LLMDB_ROOT=$PWD) | Final result | Why selected |
|---|---|---|
| {B}python3 -B -S tools/render_state.py --check{B} | PASS, {ci["steps"][0]["wall_s"]:.3f} s | Five generated blocks checked using code/docs |
| {B}python3 -B -S -m unittest discover -s tests -p test_git_automation.py -v{B} | 56 PASS, {ci["steps"][1]["wall_s"]:.3f} s wall | Disposable Git fixtures and new safety/CI contracts |
| {B}python3 -B -S -m unittest -v tools.test_c10w_p2_gate tools.test_dashboard_live tools.test_dashboard_gpu_detector{B} | 80 PASS = 13+27+40, {ci["steps"][2]["wall_s"]:.3f} s wall | Existing stdlib process/admission/dashboard regressions |

Selected candidates were actually tried individually in {link("ci_candidates.json")}. The first GPU-detector candidate failed because extraction omitted small experiment source files; it was not a model/asset failure. Adding tracked experiment code, while retaining absent large assets, yielded 40 PASS in {link("candidate_3_fullcode.json")}. The exact final workflow commands passed in {link("assetfree_ci_r2.json")}; complete logs are assetfree_ci_r2_0.log, _1.log, _2.log.

Excluded entrypoints:

- {B}tests/test_new1_geometry.py{B}, {B}tests/test_new1_supervisor.py{B}, {B}tests/test_new1_construction_diag.py{B}, {B}tests/test_new1_identity_diag.py{B}: NEW-1 follow-up is explicitly on hold and separate from this Git baseline.
- {B}tools/test_backup_gdrive.py{B}, {B}tools/test_backup_gdrive_addendum.py{B}: backup work/tests are under active MB3 ownership and outside this intake.
- {B}tools/test_dashboard_mathlab.py{B}: concurrent protected WIP; MathLab is outside this build.
- {B}tools/labviz/test_mathlab.py{B}, {B}tools/labviz/test_labviz.py{B}: separate visualization acceptance workflow, not this CPU Git baseline.
- {B}tools/test_dashboard_report.py{B}: its separate suite was not admitted as a candidate while provider sources changed concurrently; some provider paths are exercised by the selected dashboard tests.

These exclusions are scope/qualification choices, not empirical claims that every unselected suite requires models or cannot pass. Live scientific scripts, model/torch/MPS/CUDA suites, browser/Node checks and external backup/merge operations are outside CI.

The snapshot contains small tracked code/docs and the four new source files, with no model, hf_cache, covariance_caches, .venv or real results tree. Python is supplied externally from the local interpreter but -S proves no site-package dependency. Exact file identities are in assetfree_ci_r2_manifest.json. Concurrent docs/dashboard changes detected after the initial snapshot were copied only into the temporary snapshot; the full CI sequence was rerun once. assetfree_ci_r2_refreshed.json records these identities. The real current generated-state check also passed (current_state_check.json). Existing dashboard tests emit unclosed-file ResourceWarnings; these were retained, not suppressed or fixed outside scope. Final automation tests have no such warnings.

| Pin | Value |
|---|---|
| actions/checkout v4.2.2 | {B}11bd71901bbe5b1630ceea73d27597364c9af683{B} |
| actions/setup-python v5.6.0 | {B}a26af69be951a213d495a4c3e4e4022e16d87065{B} |
| Python CI minor / measured local | 3.11 / 3.11.16 |
| Runner | ubuntu-24.04 (live UNVERIFIED) |
| Required workflow / job | CI / cpu |
| Target branch / merge mode | master / merge commit with exact-head guard |
| Engine SHA256 / _cov_cpu sites | {B}d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65{B} / 3 |

Action SHAs were checked against official release commit links: [checkout commit](https://github.com/actions/checkout/commit/11bd71901bbe5b1630ceea73d27597364c9af683), [setup-python commit](https://github.com/actions/setup-python/commit/a26af69be951a213d495a4c3e4e4022e16d87065).

| Final file | SHA-256 |
|---|---|
''')
for path, sha in ci["hashes"].items():
    parts.append(f"| {B}{path}{B} | {B}{sha}{B} |\n")
parts.append(f'''

### Real read-only dry runs

Receipts: {link("real_hygiene_final_receipt.json")}, {link("real_gate_final_receipt.json")}; full stdout JSON and stderr logs are separately retained. {link("real_dry_final_snapshot.json")} proves root/branch/HEAD/refs/worktree registrations/index SHA256/index mtime unchanged over these final invocations. Recorded HEAD: {B}{dry["after"]["head"]}{B}; cached origin/master: {B}{h["master_sha"]}{B}. Later coordinator commits are separate concurrent activity.

~~~sh
LLMDB_ROOT="$PWD" python3 -B -S tools/git_hygiene.py --dry-run --timeout 180
LLMDB_ROOT="$PWD" python3 -B -S tools/git_merge_gate.py 21 --dry-run --timeout 180 --ci-wait 2
~~~

Hygiene exited **1 / REFUSE in {dry["receipts"][0]["wall_s"]:.3f} s**: GitHub DNS could not resolve; the open-PR API could not connect. It reported **47 branches: 34 local (31 MERGED, 3 PROTECTED), 13 cached remote (11 MERGED, 2 PROTECTED)**. Every deletion eligibility is false because remote/PR protection is unverified; actions are empty. The **31 local and 11 cached remote merged branches are conditional candidates**, not authorized deletion recommendations; open-PR/default/remote existence must first be verified. No branch with unique commits is eligible.

| Kind | Branch | Classification | Unique vs cached master | Last commit date | Tip | Protection / remote presence |
|---|---|---|---|---|---|---|
''')
for row in h["branches"]:
    protection = "; ".join(row["protected_reasons"]) or "none observed; PRs UNVERIFIED"
    parts.append(f'| {row["kind"]} | {B}{row["name"]}{B} | {row["classification"]} | {row["unique_commits"]} | {row["last_commit_date"]} | {B}{row["sha"][:12]}{B} | {protection}; remote existence UNVERIFIED |\n')
parts.append(f'''

Protected but unmerged: research-pass/2026-10-06 local has **9** unique commits; worktree-c10k-route-a local and cached remote each have **293** unique commits at this snapshot. MAESTRO must bring unmerged-branch decisions to the operator; these branches are never deleted by hygiene.

| Worktree path | Branch / state | Bytes before -> after | Eligible | Keep reasons |
|---|---|---|---|---|
''')
for row in h["worktrees"]:
    parts.append(f'| {B}{row["path"]}{B} | {B}{row["branch"] or "DETACHED"}{B} | {row["size_before_bytes"]} -> {row["size_after_bytes"]} | NO | {"; ".join(row["keep_reasons"])} |\n')
parts.append(f'''

All five worktrees are kept. Sizes are per-path allocated bytes from du -sk; the main checkout contains the nested current worktree, so those sizes must not be added. No disk was reclaimed.

PR #21 gate exited **1 / REFUSE in {dry["receipts"][1]["wall_s"]:.3f} s**. PR metadata/current candidate SHA and live checks could not be read; actual admission remains UNVERIFIED. Current-root engine fingerprint is PASS; committed PR fingerprint is NOT-RUN. All nine dry-run check slots are printed:

| Gate check | Recorded status | Detail |
|---|---|---|
''')
for name, value in g["checks"].items():
    reason = value.get("reason") or ("current-root PASS; immutable candidate NOT-RUN" if name == "fingerprint" else "")
    parts.append(f'| {name} | {value["status"]} | {reason} |\n')
parts.append(f'''

No draft-ready, merge, post-merge wait, fetch or cleanup occurred. PR-green/master-green were never inferred from absence/API failure. Live conflict/draft/private/default-branch/branch-protection facts remain UNVERIFIED; origin URL is locally verified as https://github.com/thestoryportal/arhugula-persistent-memory.

### Scope, handoff and open boundaries

scope_audit.json compares {scope["protected_files_examined"]} protected files with the start snapshot. It records {len(scope["protected_drift"])} concurrent differences; MB4 did not write these paths or revert them:

''')
for path in scope["protected_drift"]:
    parts.append(f"- {B}{path}{B}\n")
parts.append(f'''

Allowed builder writes are the workflow, two Git tools, dedicated test file, this report, its evidence directory and its location pointer. The reviewer writes only its two review artifacts. CLAUDE.md, NEW-1 sources/prereg, protected MathLab test and unrelated file families were not edited by MB4; concurrent WIP was preserved. Baseline HEAD and subsequent coordinator HEADs are separately recorded; there is no claim the entire shared tree stayed unchanged. Every repo shell command explicitly set LLMDB_ROOT=$PWD. No model/GPU/MPS/NEW-1 run occurred.

Done: A–E implemented; RED/GREEN retained; 136 final CPU tests and generated-state check PASS; source/action/engine pins retained; two real read-only refusal receipts; eight review findings closed; full branch/worktree inventory above. In-flight builder work: none after final receipt/source validation. Exact paths: .github/workflows/ci.yml, tools/git_hygiene.py, tools/git_merge_gate.py, tests/test_git_automation.py, results/git_automation_build_report.md, results/git_automation_build_20261010T064202.457112Z/.

Next: MAESTRO folds in its canonical operating/permission rules, obtains live GitHub CI/PR evidence, reviews protected unmerged branches, and invokes the explicit tools under that policy. This build performs no real mutation and makes no server-enforcement or Linux runtime claim. Open risks: unavailable live GitHub/Actions/PR #21 acceptance, external races beyond cooperative locks, platform-wide lsof visibility, pre-existing dashboard ResourceWarnings and concurrent source/doc drift. Future admission always needs actual current exact-head and merge-SHA checks.

**BINDING context directive (operator 2026-10-09, carried through every handoff):** watch Context N% left for root and team sessions. Before approximately 20% remains, stop starting new work, write done/in-flight/exact paths/next step/open risks into the task report, notify MAESTRO3 and request a fresh successor. Every handoff restates this rule; do not approach full-window compaction. A context-save closeout checkpoint is retained locally in the evidence directory; no global memory write or git checkpoint commit is made.
''')
section = "".join(parts)
report = root / "results/git_automation_build_report.md"
assert "## Final build acceptance — GIT AUTOMATION BUILD DONE" not in report.read_text()
with report.open("a") as handle:
    handle.write(section)
assert report.read_text().endswith(section)
print(json.dumps(dict(report=str(report), bytes=report.stat().st_size, tests=136, wall_s=ci["total_wall_s"], legacy_resource_warnings=(out / "assetfree_ci_r2_2.log").read_text().count("ResourceWarning: unclosed file")), indent=2))
