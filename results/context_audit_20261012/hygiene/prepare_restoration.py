"""Freeze explicit CHP2 restoration units and their row dispositions; no live repairs."""
import hashlib
import json
from pathlib import Path

ROOT = Path.cwd()
A = 'results/context_audit_20261012'
OUT = A + '/hygiene'
DEST = ROOT / OUT
H = '/Users/robertrhu'
M = '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory'
B = 'results/compute_storage_brainstorm_20261011T054507Z'
S2 = H + '/.claude/projects/-Volumes-memit-llm-database-poc-mirror/memory'
S3 = H + '/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory'
BASE = json.loads((DEST / 'chp2_baseline_lanes.json').read_text())
OLD = {u['id']: u for u in BASE['units']}
exports = json.loads((DEST / 'export_candidates.json').read_text())['exports']
units, rows, patches, owner_addenda = [], [], {}, {}


def stage(path):
    return OUT + '/host_staging/' + path[len(H) + 1:] if path.startswith(H + '/') else path


def patch(ident, dep):
    patches.setdefault(ident, {'depends_on_add': []})['depends_on_add'].append(dep)


def row(source, reader, disposition, ident=None, check=None):
    entry = {'source': source, 'reader': reader, 'disposition': disposition}
    if ident:
        entry['unit'] = ident
    if check:
        entry['check'] = check
    rows.append(entry)


def covered(source, reader, ident, check):
    row(source, reader, 'COVERED', ident, check)


def new(ident, title, paths, wave, minutes, dependencies, checks, sources, expected_red=False, lane=None):
    if isinstance(sources, str):
        sources = [sources]
    receipt = OUT + '/receipts/' + ident
    files = [stage(p) for p in paths]
    u = {'id': ident, 'deliverable': title, 'files': files + [receipt + '/' + n for n in ('report.md','hashes.json','red.txt','green.txt')],
         'source_files': paths, 'finding_ids': ['RESTORE-' + ident], 'depends_on': dependencies,
         'minutes': minutes, 'checks': ['Read the complete current allowed files and ' + ', '.join(sources) + '; freeze dispatch and before hashes. Preserve concurrent work and all earlier owner repairs.'] + checks + [
             'Save numbered observations and before/after hashes in the unique receipts; reread after an intervening operation. Run LLMDB_ROOT=$PWD /usr/bin/python3 -B ' + OUT + '/check_lane.py <LANE> <WT> → exit 0. No live host/Git mutation or activation; unrun behavior stays UNVERIFIED.'],
         'source': sources[0].rsplit(':',1)[0], 'source_refs': sources, 'evidence': [], 'decision_refs': [],
         'receipt_files': [receipt + '/' + n for n in ('report.md','hashes.json','red.txt','green.txt')],
         'kind': 'host' if any(p.startswith(H + '/') for p in paths) else 'repo', 'wave': wave,
         'pins': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() if (ROOT / p).is_file() else None for p in paths if not p.startswith(H + '/')},
         'host_before_sha256': {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() if Path(p).is_file() else None for p in paths if p.startswith(H + '/')}}
    if expected_red:
        u['expected_red'] = True
    if lane:
        u['append_to_lane'] = lane
    units.append(u)
    return u


def addendum(ident, text):
    owner_addenda.setdefault(ident, []).append(text)


pres = A + '/PRESERVATION.md'
hyp = A + '/operator_hypothesis_worktree_vs_main.md'
section = 0
p2, p3, p4 = [], [], []
for n, line in enumerate((ROOT / pres).read_text().splitlines(), 1):
    if line.startswith('## '):
        section = int(line.split()[1].rstrip('.'))
    if line.startswith('| ') and not line.startswith('|---'):
        cells = [c.strip() for c in line.strip('|').split('|')]
        if section == 2 and cells[0].startswith('10-'):
            p2.append((n,cells))
        elif section == 3 and cells[0].startswith(('S1/','S3/')):
            p3.append((n,cells))
        elif section == 4 and cells[0] not in ('Worktree (suffix relative to M unless absolute)',):
            p4.append((n,cells))
assert (len(p2),len(p3),len(p4)) == (41,80,7)

# Shared index/view owners keep their IDs and original checks. Supplemental duties
# are lane addenda, supplied by explicit dependency units rather than changed tests.
new('R-GA-ROUTES', 'Program-specific roles, operator scope and phone-readable routing in the global Codex reader',
    [H + '/.codex/AGENTS.md'], 3, 7, ['D-U24','P01','P04','P10'], [
    'In the complete staged reader add a repo-scoped route: interactive tmux Sol builders/sweeps, separate Astra-high binding gates, ordinary method/word-list decisions resolved by the team; no builder commits/pushes/merges. Cite model-and-compute-allocation, sol-for-sweeps-astra-for-gates and CLAUDE.md roles; do not change unrelated repos or personal memory.',
    'Add recommendation-first plain language, operator-led one-domain-at-a-time brainstorming and atomic isolated worktrees; retain no-current-save-outside-brief rule and 60/45/40 plus blind-builder MAESTRO messages. Source conflict for budget changes remains OPEN; no new frozen-cap/spend permission.',
    'Read staged file as a fresh Codex reader: each program role, phone route, brainstorm boundary and current hygiene-only hold is discoverable by a resolving explicit Git pointer; verify staged-before diff preserves generic safety.'],
    [pres + ':' + str(p2[i-1][0]) for i in (3,6,9,12,31,33,40)])
new('R-ROOT-GUIDE', 'Root Codex reader preserves blind-builder, InfraNodus and LabViz holds',
    ['AGENTS.md'], 2, 6, ['C2','P10'], [
    'Replace the visible-context assumption with an explicit MAESTRO watcher/message at 45%, new work ≥60%, successor ≤40% or any compaction; every handoff restates it. Do not weaken enabled Memento/reset rules.',
    'In the existing research-tools section name the surviving 10-08 InfraNodus standing prose approval. Credentials, actual denial, scope, spend and no-activation boundaries remain separate; no repeated scope question.',
    'Route program roles, LabViz historical multi-model coverage/settled choices and current v3 writing/review → Astra spec gate → static wireframe → operator review → separate BUILD GO through resolving current authorities. Preserve science/activation and hygiene-only holds.'],
    [pres + ':' + str(p2[i-1][0]) for i in (10,14,17,29,39)])
patch('D-U5','R-ROOT-GUIDE')

new('R-AUTONOMY-READER', 'Overnight note preserves current hygiene-only and gated MAESTRO merge boundaries',
    ['memory_mirror/operator-overnight-autonomy-2026-10-06.md'], 2, 5, ['N10','N06'], [
    'Retain the 10-06 and 10-08 quoted grants as dated history. Immediately qualify current initiative: context hygiene only until tight/durable, then pause HIL; no science, activation, unrelated builds or frozen/spend amendments.',
    'Replace old blanket never-merge/operator-merges reader wording with MAESTRO-only cooperative reservation/drain/merge-gate and concrete operator GO; builders never commit/push/merge. Preserve the unresolved budget source conflict explicitly OPEN.',
    'Verify body and description agree, frontmatter/links resolve, and a new reader cannot treat the older continue-through-night quote as lifting the latest hold.'],
    [pres + ':' + str(p2[i-1][0]) for i in (8,12,21,22,41)])

new_notes = [
 ('R-RETEST-NOTE','autoresearch-retest-minted-token-planning-only.md',25,
  ['Preserve the exact ruling at results/autoresearch_reaim/operator_ruling_retest_20261011.md:6–18: correct Arm R is AutoResearch, not C10W. A dated supersession correction in the named historical DS reader is owned by R-ARM-R-READER; do not infer a new run from that correction. Planning approval/minted token is not run GO; distinguish Arm M and all freeze/new-authorization conditions.',
   'Create nonempty name/description/metadata.type frontmatter and a resolving authority link. No recipe, budget or science acceptance changes.']),
 ('R-RECOVERY-NOTE','hw1-choice7-recovery-required.md',28,
  ['Read decisions_log.md:95–101,191 and adopted r2_git_drive_redesign_v4.md recovery clauses fully. Preserve seven daily/four weekly recovery history and old-version restore; recovery is required, not optional.',
   'Describe the adopted design obligation separately from implementation/commissioning/activation acceptance. Frontmatter/description/links must agree; do not re-author S1–S12 thresholds.']),
 ('R-REVIEW-FIRST','operator-review-report-before-questions.md',30,
  ['Preserve review-first condition from maestro47_takeover_20261011.md:8 and successor 20261012T002451Z-56625.md:2. SUMMARY adoption choices remain blocked until the operator says review is complete; elapsed time or historical ready text is not approval.',
   'Create a resolving current-source pointer; no question to the operator during this planning session. Queue enforcement is owned by R-QUEUE.']),
 ('R-HOLD-NOTE','operator-context-hygiene-hold.md',41,
  ['Record exactly the latest operator direction: Fix absolutely everything; Context hygiene only until it is perfectly tight and durable. Then pause for HIL for next steps. The hold applies to all other ready/running science/build/activation queues.',
   'Do not erase earlier grants or claim they were revoked permanently; record a current pause and explicit HIL resume boundary. Name/description/metadata.type and resolving sources required.']),
 ('R-R2-ADOPT-NOTE','r2-v4-adoption-reader-boundaries.md',38,
  ['Read r2_redesign_operator_adoption.md:9–11, r2_redesign_operator_ruling.md:5–11, r2_redesign_operator_r8_answers.md:8–23 and adopted v4 in full. Name Git pull by Intel, no shared memit, Intel slow uploads, approved M3-initiated source-read push; account question No; copy overlap Yes does not authorize cleanup/restore overlap.',
   'Route numeric peak/support-writer acceptance to the complete adopted v4 S1–S12 source, retaining fail-closed budget/ownership boundaries. Adoption activates nothing. Old Gate-1, UID and shared-drive recipes are historical only; all implementation/commissioning/storage/deletion/activation gates survive.'])]
for ident,name,idx,checks in new_notes:
    new(ident, 'Standalone preserved ruling: ' + name, ['memory_mirror/' + name],1,4,[],checks,pres + ':' + str(p2[idx-1][0]))

# Preserve the named stale readers as history; add a resolving current amendment.
for version, idx in ((1,28),(2,37),(3,37)):
    path = B + '/r2_git_drive_redesign_v' + str(version) + '.md'
    new('R-R2-V' + str(version), 'Historical R2 redesign reader redirect v' + str(version),
        [path,'docs/session_summaries/r2_redesign_v' + str(version) + '_before_hygiene_20261012.md'],1,4,[],[
        'Before editing, archive the complete original UTF-8 bytes in the exact dated file; record SHA-256/length and round-trip equality. Add only a dated superseded-reader banner; leave the historical design and its scientific contract text intact.',
        'Banner routes to adopted r2_git_drive_redesign_v4.md and its adoption receipt; v1 recovery-optional text is superseded by required HW1 choice 7; v1/v2 account requirements and v3 destructive-overlap generalization are superseded. Source-read copy permission never covers cleanup/restore; adoption is design only.',
        'Verify the preserved original body is byte-identical, all redirects resolve, no retired freeze is reactivated, and no scientific/native acceptance is inferred.'],pres + ':' + str(p2[idx-1][0]))

new('R-ARM-R-READER','Historical inventory-scope reader corrects Arm R and active-arc inference',
    [B+'/r2_inventory_scope_decision.md','docs/session_summaries/r2_inventory_scope_before_hygiene_20261012.md'],1,4,[],[
    'Archive the complete historical decision bytes/hash/length and verify round-trip equality before adding only a dated reader correction. Preserve its exact ruling/history, never amend a frozen clearance contract.',
    'The corrected reader cites operator_ruling_retest_20261011.md:6–18: Arm R is AutoResearch, not C10W. Basename absence from program state does not prove inactivity; old DS selection was rejected by astra_r2i_verdict.md:48–56. Adopted v4 supersedes the old shared-drive planning lineage; no profile/run/activation permission follows.',
    'Verify original body byte preservation, resolving current ruling/adoption pointers, explicit historical rejection and current hygiene-only hold.'],pres + ':' + str(p2[24][0]))

handoff = H + '/.claude/memento/handoffs/maestro8_takeover_20261010.md'
new('R-ACTIVATION-HANDOFF','Old activation handoff visibly routes to its superseding hold',
    [handoff],1,4,[],[
    'Stage the complete existing handoff; preserve original dated prose and record its complete pre-amendment bytes/hash in the receipt. Add a dated top reader amendment pointing to maestro9_takeover_20261010.md:40 and current adopted-v4/Drive activation authority.',
    'The old Turn on, keep fixing quote no longer grants activation for the defective build; separate later exact activation approvals remain separately evaluated. Latest hygiene-only hold is immediately visible. No host copy or activation.'],pres + ':' + str(p2[21][0]))

new('R-LABVIZ-READER','Wireframe and coverage note preserves current v3 hold and solved Figma setup',
    ['memory_mirror/labviz-wireframe-before-spec-approval.md','memory_mirror/lab-view-and-live-telemetry.md'],2,6,[],[
    'Read PS:230–231, settled LabViz choice ledger and cited handoffs completely before editing. Keep historical coverage over all tested models, no fresh replay/science authority, and no replacement of the settled frontend topic.',
    'Standing note must route to current v3 writing/review; Astra spec approval precedes static wireframe and operator visual review, separate BUILD GO thereafter. Record configured/signed-in Figma as dated setup evidence, not live health; S3 role-index correction stays with I-CACHE.',
    'Validate both notes frontmatter/description/body links and preservation of the dashboard/LabViz BUILD hold.'],[pres + ':' + str(p2[i-1][0]) for i in (10,29,32,39)])

new('R-STORE-CENSUS','Preserved sole-store lessons have exact discovery and retirement routes',
    ['results/context_hygiene_20261012/sole_store_preservation.json'],2,7,[],[
    'Read every one of the 80 PRESERVATION §3 rows and every named sole-store note in full; record exact expanded path, current SHA-256/bytes, original audit state, current retained/retired/historical state, desired recall route and explicit Git authority. Denied/missing/changed provisional source stops, never counts as empty success.',
    'For all 31 non-retired S1-only notes route approved current discovery through I-GIT and role-selected cache exports; preserve deliberate de-index decisions such as N59, using explicit Git/history discovery instead of reactivation; for all 36 retired notes preserve exact tombstones and resolving evidence, exclude from active recall, do not reactivate. Historical memory checkpoint belongs to D-U11 with a resolving archive pointer.',
    'For 12 S3-only notes verify P01–P11/P14 import and concrete S2/S3 export ownership before index promotion. Automatic attachment/recall remains UNVERIFIED. CM personal memory is not a fourth program mirror and receives no writes.',
    'Record body-hash collisions without size/mtime winners; route Drive to P-GDRIVE, watcher to N12/D-U10/P11 and final role indexes to I-GIT/I-CACHE. Output exact rows, not a filename-count proxy.'],pres + ':121')

new('R-INFLIGHT','Preserve current uncommitted decision and history exposure without touching parallel work',
    ['results/context_hygiene_20261012/inflight_preservation.json'],1,6,[],[
    'Read-only inventory the exact §4 tracked decision paths (drive_intel_dedup_layout_v2.md, activation_plan_intel_v1.md, tools/test_dashboard_mathlab.py), hygiene bundle, NEW-1 diagnostic context/history, results/labviz_codex_brief.md and its named implementation reports. Record tracked/untracked/ignored state, current path/hash/bytes, owner and preservation route; hashes/absence/denial explicitly labelled.',
    'Preserve current bytes and raw scoped Git diffs in unique receipts; no modification, staging, commits or deletion of parallel files. Historical ~20% checkpoints remain dated and cannot authorize current handoff behavior. MAESTRO reconciles and commits only reviewed nonsecret owner-approved bytes before successor/master integration.',
    'Snapshot counts and commit identities are dated observations, never current constants. Latest durable corrections must reach queue/index summaries through R-QUEUE/P14 and their export owners.'],pres + ':226')

new('R-QUEUE','Queue readers enforce hygiene pause, review-first dependency and current host roles',
    ['docs/program_state.json'],4,8,['D-U12c','R-REVIEW-FIRST','R-HOLD-NOTE','R-R2-ADOPT-NOTE'],[
    'Edit only work_queue and its active needs_from_you/notes fields; do not rewrite the finalized F1/scorecard/next_actions repaired by existing owners. Before edit preserve the complete source hash/bytes; use deterministic stdlib JSON editing. Retain every item, dependency and historical note.',
    'For every non-hygiene science/build/activation item advertise GATED by the current context-hygiene hold rather than runnable readiness. Preserve actual progress separately; do not claim a running host process stopped. SUMMARY choice prompts depend on operator review completion and cannot be released by blocked_by=[] or elapsed time.',
    'Replace current no-merge-since-Oct-4 claim with dated cached-origin/master vs stale-local-M distinction; no hardcoded divergence as a live constant. Correct Neo4j-on-M3/second-memit-copy current routes to D-HW-2 Intel support/Git pull/adopted v4; retain activation/fresh-run gates.',
    'Read before/after structured queue: IDs/counts/progress/notes survive; only scoped hold/current-reader fields differ. No READY run permission in the active paused queue. D-U13a/b and D-U15/16/19 own renderer/views and must receive this final state.'],[pres + ':' + str(p2[i-1][0]) for i in (26,27,30,34,41)],lane='H04-16')
patch('D-U13a','R-QUEUE')

# Two separately frozen RED fixtures, before either implementation.
new('R-ROOT-RED','Behavioral RED: a tool or brief resolves stale main as its repo root',
    ['tests/test_context_hygiene_roots.py'],2,6,['DG1'],[
    'Write stdlib CLI fixtures against the EXISTING DG1 actual non-enforcing CLI stub, using temporary fixture Git repos and plumbing-created commits/refs only. Run its accepted CLI with --root <fixture main>: local master behind cached origin/master must emit ROOT_STALE_MAIN and nonzero. Save the intended missed-staleness assertion; missing new flag/API, syntax/import failure is not RED.',
    'Positive controls: current isolated worktree passes even when fixture main is stale; main equal to cached origin/master passes; main divergent/ahead-unreviewed/missing cached ref/denied Git observation fail closed. Record local ref observation as cached, never fetched/live remote evidence.',
    'Include existing CLI input cases for a brief/tool/env root resolving through an alias/symlink to the stale main; approved current worktree route remains usable. Fixtures never read/write real M/H or execute science. Freeze fixture hashes for R-ROOT-GREEN.'],hyp + ':20',expected_red=True)
new('R-HOOK-RED','Behavioral RED: shared core.hooksPath points to different hook bytes',
    ['tests/test_context_hygiene_hook_roots.py'],2,6,['DG1'],[
    'Write stdlib CLI fixtures against EXISTING DG1 actual non-enforcing CLI stub: linked worktrees share fixture .git/config core.hooksPath pointing at fixture main/tools/git_hooks. Change exactly one configured hook byte while worktree hook stays fixed; actual guard must fail HOOK_BYTES_DIFFER with both paths/hashes. Save intended missed-mismatch assertion, not absent-API failure.',
    'Complete same hook inventory and bytes passes; missing/extra hook, missing config target, unreadable files, unsafe symlink, ambiguous config scope or unresolved relative core.hooksPath fails closed. A reviewed worktree-relative equivalent may pass only after resolving actual effective Git path and comparing complete inventories.',
    'Use temporary Git plumbing only. Never execute a hook or change the real shared config/main folder. Include pre-commit and post-commit plus every other tools/git_hooks file, not just filename/presence checks. Freeze fixtures for R-HOOK-GREEN.'],hyp + ':22',expected_red=True)
new('R-ROOT-POLICY','Single policy authority for main/worktree roots, hooks and restoration cache membership',
    ['tools/context_hygiene_policy.json'],2,5,['R-ROOT-RED','R-HOOK-RED','DG2'],[
    'Extend existing data authority with exact real M path, main ref master, cached comparison origin/master, explicit root-bearing tool/brief/env fields, hook source tools/git_hooks, shared-config provenance and effective hooksPath resolution. No duplicated retired-value or root constants in implementation.',
    'Policy references restoration_cache_manifest.json alongside the unchanged exact 196 baseline exports. Define exact membership and observed-source hashes; no blanket missing-store exemptions. CI/staged fixtures use explicit synthetic repo metadata and label non-host scope; applied mode requires actual read-only config/ref/hook observations.',
    'Parse valid JSON, preserve every prior policy rule/allowlist/history exemption; malformed/missing root observation fails closed. Root/hook checks are structural and never exempted by historical results paths or private config projection.'],[hyp + ':20',hyp + ':22'])
new('R-ROOT-GREEN','Fail loudly before reading a stale main root; guard every declared tool/brief route',
    ['tools/context_hygiene_guard.py'],3,8,['R-ROOT-RED','R-ROOT-POLICY','DG3'],[
    'Implement the frozen ROOT_STALE_MAIN fixtures with read-only stdlib subprocess Git observations. Canonicalize root/aliases before source reads; inspect each declared tool/brief/env root, including inherited LLMDB_ROOT. Main behind origin/master fails loudly with resolved root and both ref SHAs; missing/denied/malformed/diverged observations never imply current.',
    'Guard authoritative input-root resolution at the boundary: tools/briefs may name a verified current worktree; a main route must prove currentness. Unchecked launch routes remain held by MAESTRO; do not silently rewrite roots or automatically refresh a checkout. No network, checkout, reset, Git metadata mutation or hook execution.',
    'Run /usr/bin/python3 -B tests/test_context_hygiene_roots.py → GREEN through actual CLI, then the existing DG1 suite; preserve original RED and existing assertions. Later DG4/DG5 owners retain these GREEN controls. Combine baseline and supplemental cache manifest membership for full observed-body checks, retaining projection boundaries.'],hyp + ':20')
new('R-HOOK-GREEN','Guard complete shared hooksPath bytes against the current worktree',
    ['tools/context_hygiene_guard.py'],3,8,['R-HOOK-RED','R-ROOT-GREEN','R-ROOT-POLICY'],[
    'Resolve shared common Git dir/config and effective core.hooksPath using read-only Git interfaces; compare complete relative-path/type/byte/hash inventories against this worktree tools/git_hooks. Main-selected mismatches fail HOOK_BYTES_DIFFER with evidence. Denied/missing/extra/symlink-ambiguous observations fail closed; no real config changes.',
    'Run /usr/bin/python3 -B tests/test_context_hygiene_hook_roots.py, tests/test_context_hygiene_roots.py and tests/test_context_hygiene_guard.py → GREEN. Keep both separately saved RED fixtures and verify previous store/link/history assertions unchanged.',
    'Staged CI uses deterministic complete synthetic shared-config/hook fixture metadata, never inferred actual host success. Applied mode inspects real shared bytes; master refresh may change hooks for all worktrees, so guard must rerun after any reviewed refresh. Integration caller rejects unresolved root/hook results.'],hyp + ':22')
# Extend only existing lane runs; retain all original unit fields/checks/waves.
for u in units:
    if u['id'] in ('R-ROOT-RED','R-HOOK-RED','R-ROOT-POLICY'):
        u['append_to_lane']='H02-12'
    if u['id'] in ('R-ROOT-GREEN','R-HOOK-GREEN'):
        u['append_to_lane']='H03-15'
patch('DG3','R-ROOT-POLICY')
patch('DG4','R-HOOK-GREEN')
patch('DG5','R-HOOK-GREEN')
patch('DG6','R-HOOK-GREEN')
patch('DG7','R-HOOK-GREEN')
patch('DG-INDEX-PINS','R-HOOK-GREEN')
addendum('DG5','Preserve the already GREEN R-ROOT/R-HOOK behavior when implementing store/link/projection checks. Run tests/test_context_hygiene_roots.py and tests/test_context_hygiene_hook_roots.py with DG1/DG4 tests; no structural root/hook exemptions in historical paths or CI projection. Supplemental manifest file may be future-produced, but only complete fixture membership passes; missing real inputs fail.')

new('R-ROOT-CALLER-RED','Actual renderer and closeout reader-root refusal fixtures before owner integration',
    ['tests/test_context_root_readers.py'],5,6,['R-HOOK-GREEN','R-ROOT-ROUTES'],[
    'In temporary complete fixture worktrees run the EXISTING actual tools/render_state.py --check and tools/closeout_check.py --list with inherited LLMDB_ROOT set to a fixture main behind cached origin/master. Supply byte-current generated views/complete state so baseline read-only commands succeed for the wrong root; assert ROOT_STALE_MAIN/nonzero before any source read and save intended behavioral RED.',
    'Positive verified-current-worktree controls pass; hook-byte mismatch fails before read. Copy actual tool bytes into the isolated fixture; do not execute scientific closeout, --write, a live hook, real host/main or model imports. Existing accepted flags only; missing new API/argument failure is not RED.',
    'Freeze fixture hashes for renderer owner D-U13b and closeout owner DG8. Those owners integrate the central resolver in their existing files and run this suite GREEN; tests check actual consumer refusal, not mere policy presence.'],hyp + ':20',expected_red=True)
patch('D-U13b','R-ROOT-CALLER-RED')
patch('DG8','R-ROOT-CALLER-RED')
new('R-ROOT-ROUTES','Exact launch-root and historical R2 source-route inventory for MAESTRO',
    ['results/context_hygiene_20261012/root_routes.json'],2,6,[],[
    'Inventory every current tool/brief repo-root route using read-only text/Git observations; name resolved root, source file:line, owner, dispatch gate and current/held status. Include guard CLI --root, inherited LLMDB_ROOT, render_state and closeout callers; no unobserved root is marked safe.',
    'Record PRESERVATION §6 exact-match origin as process/closure obligations, D3 selection and later A1 amendment, not proven GPU-note causation or file equality. The unfrozen legacy M3 source folder is UNKNOWN, not a license to select M; adopted v4 Git-pull reader replaces that retired shared-drive route.',
    'Root/hook guard GREEN is a mandatory MAESTRO preflight for each resolved tool/brief root before dispatch; unchanged science entrypoints are not edited/activated. Preserve all registration/exclusion safety boundaries.'],[hyp + ':20',pres + ':246',pres + ':247'])
addendum('DG6','Root/hook integration acceptance (after R-HOOK-GREEN): the rooted hook/CI invocation must include every declared root from root_routes.json and both cache manifests through policy. A stale main or changed shared hook byte produces nonzero. CI fixture metadata is explicit; actual applied Git/hook bytes cannot be replaced by CI proof. Never execute hooks to test them.')
addendum('D-U13b','Root-reader acceptance: before any root-selected source read/write, run the reviewed R-ROOT-GREEN resolver contract using the existing root/env CLI boundary; run tests/test_context_root_readers.py GREEN against the actual renderer after its R-ROOT-CALLER-RED fixture. Named main roots fail when stale; do not redirect silently. Root fixtures establish local behavior only; no science/native qualification.')
addendum('DG8','Closeout root-reader acceptance: actual root/env observations must pass R-ROOT-GREEN/R-HOOK-GREEN; run tests/test_context_root_readers.py GREEN against actual read-only closeout after R-ROOT-CALLER-RED; stale main/shared-hook differences are named RED/UNAVAILABLE, without changing scientific presence/currency or memory WARN semantics.')
patch('D-U13b','R-ROOT-ROUTES')

# Supplemental exports preserve all original 196 assignments/checks.
extra_exports = []
needed = {name for _,name,_,_ in new_notes}
needed.update(Path(cells[0].split(':')[0]).name for _,cells in p3 if cells[0].startswith('S3/'))
needed.update(['context-management-every-session.md','work-queue-tab-keep-current.md','operator-decision-scope.md','plain-language-to-operator.md','readme-plain-words-summary.md',
    'operator-overnight-autonomy-2026-10-06.md','commit-forward-work-without-asking.md','lab-view-and-live-telemetry.md',
    'backup-via-memitbackup-app.md','infranodus-standing-approval.md','approved-deletes-ask-then-rmtree.md',
    'c10y-deferred-behind-drive-backup.md','intel-exists-to-offload-the-m3.md','remove-shared-resource-before-policing-it.md',
    'labviz-wireframe-before-spec-approval.md','sol-builders-blind-to-context.md','sol-for-sweeps-astra-for-gates.md',
    'stale-predecessor-watchers-steal-events.md','atomic-units-parallel-worktree-lanes.md','interactive-codex-brainstorm-sessions.md'])
for store, folder in [('S2',S2),('S3',S3)]:
    existing = {e['filename']:e for e in exports if e['store'] == store}
    for name in sorted(needed):
        source = 'memory_mirror/' + name
        owners = [u['id'] for u in BASE['units'] + units if source in u['source_files']]
        if name in existing:
            for owner in owners:
                if owner not in OLD[existing[name]['id']]['depends_on']:
                    patch(existing[name]['id'],owner)
            continue
        ident = 'R-E-' + store + '-' + str(len([e for e in extra_exports if e['store'] == store])+1).zfill(3)
        host = folder + '/' + name
        new(ident,'Supplemental ruling export ' + name + ' to ' + store,[host],5,2,['R-CACHE-MANIFEST'] + owners,[
            'Read exact supplemental manifest row; verify final Git source SHA-256/bytes and reviewed host-before SHA-256/absence. Changed inputs stop rather than overwrite a provisional note.',
            'Stage the complete reviewed Git note; SHA-256 and bytes must equal source/manifest. Frontmatter/body links resolve, existing tombstones/history retained; no index, live-cache or baseline export edit.'],pres + ':72')
        extra_exports.append({'id':ident,'store':store,'filename':name,'source_path':source,'host_path':host,'staging_path':stage(host)})
new('R-CACHE-MANIFEST','Exact supplementary ruling membership; original 196 export contracts unchanged',
    ['results/context_hygiene_20261012/restoration_cache_manifest.json'],4,5,['I-MANIFEST','I-GIT'],[
    'Read final baseline memory_cache_manifest.json and supplemental exact candidates in OUT/restoration_spec.json. Preserve the exact original 196 candidates/contracts; write separate schema_version=1 baseline_manifest_sha256 plus supplemental exports with final source_sha256/bytes and host-before hashes/absence.',
    'Validate all supplementary note/link targets and store roots observed; no missing/denied/empty source is accepted. Role-index requirements combine both memberships; CM is excluded. No guessed filenames, wildcards or overwriting private configs.',
    'Both manifests are required by the final policy/guard and I-CACHE lane addendum; SHA/source/member divergence fails. No silent union by mtime/size; changed census goes back to MAESTRO review.'],pres + ':72',lane='H04-16')
for u in units:
    if any(p.startswith('memory_mirror/') for p in u['source_files']):
        patch('I-GIT',u['id'])
patch('I-GIT','R-STORE-CENSUS')
for u in units:
    if u['id'].startswith('R-E-'):
        patch('I-CACHE',u['id'])
patch('I-CACHE','R-CACHE-MANIFEST')
addendum('I-GIT','Restoration discovery acceptance: read R-STORE-CENSUS exact rows and all new ruling notes. Every retained lesson has one accurate resolving discovery pointer; de-indexed/retired notes remain preserved with explicit dated discovery, never current directives. Preserve the 24,400-byte cap and role-specific index boundaries.')
addendum('I-CACHE','Restoration recall acceptance: read BOTH memory_cache_manifest.json (original exact 196) and restoration_cache_manifest.json (supplemental exact membership). Wait for all new R-E owners. Index current role-selected safety/holds/rulings, including configured Figma/date and required watcher routing; preserve tombstones, index caps and explicit Git-source discovery for non-replicated lessons. Freeze final approved divergence hashes through DG-INDEX-PINS only.')
addendum('D-U15','Restoration startup acceptance: no active rented/CUDA/obsolete Intel deployment; route the historical evidence, LabViz v3/BUILD hold and current hygiene-only boundary to current authorities. Preserve archived source bytes and per-destination generated ownership.')
addendum('D-U16','Restoration checkpoint acceptance: consumed NEW-1 permission remains consumed; current v4 is design-only and hygiene-only hold covers all parallel scopes. Old LabViz/activation grants are dated history with resolving current hold pointers.')
addendum('D-U19','Restoration view acceptance: consume R-QUEUE final active hold/review-first/host-role state; regenerate only owned files and require parity. SUMMARY questions stay blocked pending explicit review completion; current queue cannot advertise paused science/build/activation as runnable.')
addendum('M-REFRESH','Required final refresh evidence: after operator-approved gate integration, separately ask before refreshing M local master. Inventory/preserve all local/untracked/ignored work and competing writers. Require CORPUS/44–61 and every imported docs/historical_backups/20261011 file (144 at source commit 7e03fd45) to exist with integrated source hashes; compare full inventories, no count-only PASS. Re-run actual root and shared hooksPath guard after refresh; if not authorized/preservable, keep M held and restoration OPEN.')
patch('M-REFRESH','R-INFLIGHT')

# Each stale reader in a §2 row receives its own exact disposition.
def exp_ref(store,name):
    item = next(e for e in exports + extra_exports if e['store']==store and e['filename']==name)
    return item['id']

def cache(source,store,name):
    ident=exp_ref(store,name)
    if ident in OLD:
        covered(source,store + '/' + name,ident,2)
    else:
        row(source,store + '/' + name,'NEW',ident)

for idx,(line,cells) in enumerate(p2,1):
    src=pres+':'+str(line)
    if 'M/' in cells[2] or cells[2].startswith('M ') or 'M lacks' in cells[2] or 'M/root' in cells[2] or 'M startup' in cells[2] or 'M only' in cells[2]:
        row(src,'stale M reader(s): ' + cells[2].split(';')[0],'MAESTRO-ONLY M-REFRESH-FINAL (operator first; integrated main guidance/CORPUS/history and hooks verified)')
    routes={
      1:[('SESSION_BOOTSTRAP.md:100','D-U15',4)],
      2:[('.codex/config.toml:9','C8',2),('S2/MEMORY.md:38','I-CACHE',4)],
      3:[('GA program roles/interactive builders','R-GA-ROUTES',None),('experiments/AGENTS.md:15','C3',2)],
      4:[],5:[],6:[('GA phone/recommendation-first route','R-GA-ROUTES',None)],7:[],
      8:[('S1/operator-overnight-autonomy-2026-10-06.md:20','R-AUTONOMY-READER',None)],
      9:[('GA MAESTRO/builder completion roles','R-GA-ROUTES',None)],
      10:[('AGENTS.md current LabViz scope/hold route','R-ROOT-GUIDE',None),('S1/lab-view-and-live-telemetry.md','R-LABVIZ-READER',None)],
      11:[('S1/rerun-never-patch.md spent-attempt caveat','N07',2)],
      12:[('S1/operator-overnight-autonomy-2026-10-06.md:20 source conflict','R-AUTONOMY-READER',None),('GA unresolved-budget boundary','R-GA-ROUTES',None)],
      13:[],14:[('AGENTS.md InfraNodus prose scope','R-ROOT-GUIDE',None)],
      15:[('origin/master:AGENTS.md old threshold','D-U21',2),('S2/MEMORY.md:1','I-CACHE',3),('GA:141 scoped save','C7',2)],
      16:[('S1/context-management-every-session.md:13','N17',3),('origin/master old context threshold','D-U20',2)],
      17:[('AGENTS.md blind-builder watcher','R-ROOT-GUIDE',None),('S1/sol-builders-blind-to-context.md','P09',3)],
      18:[('S1/never-idle-arm-completion-watch.md:16','N13',3),('S1/codex-watch-anchor-tokens-read-context-from-rollout.md','D-U10',2),('S1/stale-predecessor-watchers-steal-events.md','P11',2)],
      19:[],20:[],
      21:[('S1/commit-forward-work-without-asking.md:13','N06',2),('S1/operator-overnight-autonomy-2026-10-06.md:20','R-AUTONOMY-READER',None)],
      22:[('HF/maestro8_takeover_20261010.md:33','R-ACTIVATION-HANDOFF',None),('S1/operator-overnight-autonomy-2026-10-06.md','R-AUTONOMY-READER',None)],
      23:[('SESSION_CHECKPOINT.md:53','D-U16',4),('S1/rerun-never-patch.md single-use authority','N07',2)],
      24:[('PS next_actions:15 C10Y route','D-U12b',2),('S1/c10y-deferred-behind-drive-backup.md description','N48',2)],
      25:[('B/r2_inventory_scope_decision.md Arm R misidentification','R-ARM-R-READER',None),('S1 missing standalone re-test ruling','R-RETEST-NOTE',None)],
      26:[('PS:50 no-merge claim','R-QUEUE',None)],
      27:[('PS:13 Neo4j on M3; PS:14 old second-memit route','R-QUEUE',None)],
      28:[('B/r2_git_drive_redesign_v1.md:115','R-R2-V1',None),('S1 missing HW1 choice7 recall','R-RECOVERY-NOTE',None)],
      29:[('AGENTS.md older broad BUILD routing','R-ROOT-GUIDE',None),('S1/labviz-wireframe-before-spec-approval.md','R-LABVIZ-READER',None)],
      30:[('PS needs_from_you blocked_by=[]','R-QUEUE',None),('S1 missing report-review-first recall','R-REVIEW-FIRST',None)],
      31:[('S1 interactive brainstorm contract','P04',2),('GA operator-led brainstorm','R-GA-ROUTES',None)],
      32:[('S1 wireframe/hold sequence','R-LABVIZ-READER',None),('S3/MEMORY.md:13 configured Figma status','I-CACHE',4)],
      33:[('S1 Sol sweeps/Astra gates','P10',2),('GA sweep/loop escalation','R-GA-ROUTES',None)],
      34:[('PS:14 second-memit-copy','R-QUEUE',None),('old integration/profile active reader redirects','R-R2-ADOPT-NOTE',None)],
      35:[('S1 current storage guarantee/peak numeric authority route','R-R2-ADOPT-NOTE',None)],
      36:[('S1/remove-shared-resource-before-policing-it.md M3-only shorthand','N27',2),('S3 same shorthand corrected by export','E-S3-001',None)],
      37:[('B/r2_git_drive_redesign_v1.md UID','R-R2-V1',None),('B/r2_git_drive_redesign_v2.md UID','R-R2-V2',None),('B/r2_git_drive_redesign_v3.md cleanup/restore overlap','R-R2-V3',None)],
      38:[('S1 adopted-v4 vs old Gate-1/activation reader','R-R2-ADOPT-NOTE',None)],
      39:[('SESSION_CHECKPOINT.md old startup build-all grant','D-U16',4),('S1 LabViz current v3 sequence','R-LABVIZ-READER',None)],
      40:[('S1/parallel-builders-name-each-others-files.md','N60',2),('S1 isolated atomic units','P01',2),('GA isolated-worktree contract','R-GA-ROUTES',None)],
      41:[('PS ready/running without per-item hygiene pause','R-QUEUE',None),('S1/operator-overnight-autonomy-2026-10-06.md broad initiative','R-AUTONOMY-READER',None)]}
    for reader,ident,check in routes[idx]:
        if ident == 'E-S3-001' and check is None:
            ident=exp_ref('S3','remove-shared-resource-before-policing-it.md'); check=2
        if ident in OLD:
            covered(src,reader,ident,check)
        else:
            row(src,reader,'NEW',ident)
    cache_names={5:['operator-decision-scope.md'],6:['plain-language-to-operator.md'],7:['readme-plain-words-summary.md'],8:['operator-overnight-autonomy-2026-10-06.md'],
       9:['commit-forward-work-without-asking.md'],10:['lab-view-and-live-telemetry.md'],12:['operator-overnight-autonomy-2026-10-06.md'],13:['backup-via-memitbackup-app.md'],
       14:['infranodus-standing-approval.md'],16:['context-management-every-session.md'],17:['sol-builders-blind-to-context.md'],18:['stale-predecessor-watchers-steal-events.md'],
       20:['approved-deletes-ask-then-rmtree.md'],21:['commit-forward-work-without-asking.md','operator-overnight-autonomy-2026-10-06.md'],
       24:['c10y-deferred-behind-drive-backup.md'],25:['autoresearch-retest-minted-token-planning-only.md'],26:['work-queue-tab-keep-current.md'],
       27:['r2-v4-adoption-reader-boundaries.md','intel-exists-to-offload-the-m3.md'],28:['hw1-choice7-recovery-required.md'],29:['labviz-wireframe-before-spec-approval.md'],30:['operator-review-report-before-questions.md'],
       31:['interactive-codex-brainstorm-sessions.md'],32:['labviz-wireframe-before-spec-approval.md'],33:['sol-for-sweeps-astra-for-gates.md'],
       34:['remove-shared-resource-before-policing-it.md','r2-v4-adoption-reader-boundaries.md'],35:['r2-v4-adoption-reader-boundaries.md'],36:['intel-exists-to-offload-the-m3.md'],
       38:['r2-v4-adoption-reader-boundaries.md'],39:['labviz-wireframe-before-spec-approval.md'],40:['atomic-units-parallel-worktree-lanes.md'],41:['operator-context-hygiene-hold.md']}
    for name in cache_names.get(idx,[]):
        for store in ('S2','S3'):
            cache(src,store,name)
    if idx == 12:
        row(src,'unresolved experiment-budget vs frozen/spend authority','OPERATOR Does the recorded budget latitude amend a particular frozen cap? Keep existing caps/holds until an exact new ruling; this hygiene plan does not reopen it now.')
    if idx == 33:
        row(src,'CM separate personal memory; no dedicated exact phrase found','MAESTRO-ONLY retain explicit program reader/packet routes; personal memory writes require a separate direct operator request')

for line,cells in p3:
    src=pres+':'+str(line); note=cells[0].split(':')[0]; name=Path(note).name
    if name=='SESSION_CHECKPOINT.md':
        covered(src,note+' historical checkpoint, no S1 index pointer','D-U11',2)
    elif 'retired' in cells[1] or note.startswith('S1/'):
        row(src,note+' '+cells[1]+'; verify explicit preserved discovery route','NEW','R-STORE-CENSUS')
    else:
        source='memory_mirror/'+name
        owner=next(u for u in BASE['units'] if source in u['source_files'])
        covered(src,note+' sole-store import/recall gap',owner['id'],2 if owner['id']!='P14' else 3)
        for store in ('S2','S3'):
            cache(src,store,name)

parent=H+'/.local/share/openresearch/worktrees/0a1375d4-8f79-44be-bea6-2a27f6658761/'
worktree_questions=[]
for line,cells in p4:
    path=cells[0]
    if path.startswith('H/'):
        path=H+'/'+path[2:]
    elif path.startswith('Same OpenResearch parent/'):
        path=parent+path.split('/',1)[1]
    elif path.startswith('.claude/'):
        path=M+'/'+path.split(' ')[0]
    else:
        path=M
    status=cells[1]
    worktree_questions.append({'path':path,'status':status,'source':pres+':'+str(line)})
    row(pres+':'+str(line),path+' — '+status,'OPERATOR WORKTREES: keep launch-held until separately reviewed; choose preserve/refresh/delete only after current status recheck. No removal or refresh authorized by this plan.')
for anchor, reader, ident in [(226,'parallel tracked decisions/diffs','R-INFLIGHT'),(227,'untracked contracts/history and diagnostic ~20% checkpoint','R-INFLIGHT'),
  (228,'queue review-first and hygiene-only gating','R-QUEUE'),(229,'PS live no-merge regression','R-QUEUE'),(230,'S1 memory-paths two-store reader','D-U1'),
  (230,'closeout S2-only report','I-SYNCb'),(230,'.codex/hooks.json absent /workspace targets','C9'),(230,'H/.claude/settings.json graft emission','H-SETTINGS'),(230,'GA unconditional save','C7')]:
    if ident in OLD:
        covered(pres+':'+str(anchor),reader,ident,2)
    else:
        row(pres+':'+str(anchor),reader,'NEW',ident)
row(pres+':229','S3/context-hygiene-must-reach-every-store.md dated counts','COVERED','P14',2)
row(pres+':246','old GPU note not proved exact-match cause','NEW','R-ROOT-ROUTES')
row(pres+':247','unfrozen legacy M3 copy source folder','NEW','R-ROOT-ROUTES')
for line in (19,21):
    row(hyp+':'+str(line),'master integration plus missing CORPUS/44–61/history','MAESTRO-ONLY MASTER-INTEGRATION then M-REFRESH-FINAL; two concrete operator permissions, merge gate/full CI then preserved local refresh')
row(hyp+':20','actual renderer/closeout stale root readers','NEW','R-ROOT-CALLER-RED')
row(hyp+':20','any declared repo root resolving behind-origin main','NEW','R-ROOT-RED')
row(hyp+':22','shared .git/config core.hooksPath differs from worktree hooks','NEW','R-HOOK-RED')

# Add exact source-row evidence to new units, independently checked by verifier.
for u in units:
    linked=[r for r in rows if r.get('unit')==u['id']]
    for src in list(dict.fromkeys(u['source_refs']+[r['source'] for r in linked])):
        file,line=src.rsplit(':',1)
        text=(ROOT/file).read_text().splitlines()[int(line)-1]
        u['evidence'].append({'audit':file,'audit_line':int(line),'subject':text.strip(),
          'evidence':text.strip(),'action':u['deliverable'],'replacement':'Follow this unit numbered checks; preserved authority and latest holds bind.'})
    u['finding_ids'] += sorted({r['source'] for r in linked})

spec={'schema_version':1,'baseline_file':OUT+'/chp2_baseline_lanes.json',
 'baseline_sha256':hashlib.sha256((DEST/'chp2_baseline_lanes.json').read_bytes()).hexdigest(),
 'source_hashes':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in (pres,hyp,A+'/hygiene_restoration_brief.md')},
 'units':units,'patches':patches,'owner_addenda':owner_addenda,'rows':rows,'supplemental_exports':extra_exports,
 'worktree_question':worktree_questions,'original_counts':{'units':329,'lanes':33,'waves':9},
 'required_table_lines':{pres:[n for n,_ in p2+p3+p4],hyp:[19,20,21,22]},
 'final_steps':{'MASTER-INTEGRATION':'Operator asked first for concrete reviewed PR/head/master mutation-window GO; MAESTRO alone uses cooperative reservation/drain/exact-head merge gate and fully passing post-merge CI. Preserve commits unique to both sides.',
 'M-REFRESH-FINAL':'AFTER master integration ask the operator separately before refreshing the main folder local master. Preserve current M tracked/ignored/untracked bytes and all competing writers; follow M-REFRESH. Require CORPUS/44–61 and every docs/historical_backups/20261011 imported file (144 in the source receipt) to exist with integrated hashes. Verify actual root/hook guard after refresh. Without GO/preservation keep M launch-held and restoration OPEN.',
 'WORKTREES':'Present the exact seven worktree paths and dated statuses below. Refreshing/deleting them is the operator decision; recheck current tracked/untracked/ignored state before any proposal. No deletion/refresh is performed here.',
 'PRESERVE-INFLIGHT':'Before successors/master integration MAESTRO reconciles R-INFLIGHT owner-approved nonsecret decisions/history with concurrent sessions; no blanket git add, dropping modified/untracked work or deleting snapshots.',
 'PAUSE-HIL':'After full applied guard, completed Astra-high acceptance and approved integration/local restoration, save receipts/context and pause HIL. No science/build/activation begins from hygiene success.'}}
(DEST/'restoration_spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'new_units':len(units),'map_rows':len(rows),'new_exports':len(extra_exports),'original_units':329}))
