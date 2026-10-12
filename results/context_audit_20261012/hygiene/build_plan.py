"""Deterministically materialize the CHP plan; writes only beside this script."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path.cwd()
A = 'results/context_audit_20261012'
OUT = A + '/hygiene'
DEST = ROOT / OUT
H = '/Users/robertrhu'
M = '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory'
S2 = H + '/.claude/projects/-Volumes-memit-llm-database-poc-mirror/memory'
S3 = H + '/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory'
LR = H + '/.claude/plugins/cache/promptctl/laws/0.24.1/hooks/scripts/skill-router.sh'
BASE = subprocess.run(['git', 'rev-parse', 'HEAD'], check=True, capture_output=True, text=True).stdout.strip()
PRIVATE = [OUT + '/host_staging/.codex/config.toml', OUT + '/host_staging/.claude/settings.json']

CONTENT = '''- CLAUDE.md, AGENTS.md, DISCIPLINE.md, the global guides and memory notes are standing guidance, not specifications. Cut only text that is wrong, out of date, points the wrong way, or exactly repeats a passage you name by file:line. Keep the warnings written as a moment of temptation ("You will see green checks and think…", "When you hear yourself think…") and their stakes. A byte target in SYNTHESIS §2 is an estimate; when keeping a complete rule exceeds it, keep the rule and report the overage.
- Never weaken a safety rule (the five LAWs, halt discipline, rerun-never-patch, the merge gate and cooperative rule, storage tiers, the operator's holds, the context directive, Memento reset). A duplicated safety rule keeps one complete home and a pointer elsewhere.
- No deletion: a retired note becomes a pointer/tombstone; history moves to a dated file, never disappears.
- Edit only the listed files; no commits, pushes, merges, science, network, project python, uv, npm, rclone, ssh or graft (ignore graft hook text).'''

FINISH = '''You cannot see your context level. MAESTRO messages you at 45% left; then, or on any "Context compacted", stop starting work, write OUT/chp_handoff.md (done, in progress, remaining, exact paths, this rule) and reply `CHP HANDOFF`. If you have already finished, reply READY instead.
When done, run `/usr/bin/python3 -B OUT/test_check_lane.py`, re-read every OUT file once against this brief, then reply on its own line exactly: `CHP PLAN READY results/context_audit_20261012/hygiene/PLAN.md` or `CHP BLOCKED <one-line reason>`.'''

def write(name, text):
    path = DEST / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


evidence = {}
for filename in ('evidence_notes.json', 'evidence_hosts.json', 'evidence_stores.json'):
    document = json.loads((DEST / filename).read_text())
    for key, rows in document['entries'].items():
        evidence.setdefault(key, []).extend(rows if isinstance(rows, list) else [rows])
stores = json.loads((DEST / 'evidence_stores.json').read_text())


def expand(path):
    path = path.strip()
    symbols = {'GC': H + '/.claude/CLAUDE.md', 'GA': H + '/.codex/AGENTS.md', 'LR': LR}
    if path in symbols:
        return symbols[path]
    for prefix, replacement in [('W/', ''), ('N/', 'memory_mirror/'), ('S1/', 'memory_mirror/'),
                                ('S2/', S2 + '/'), ('S3/', S3 + '/'), ('H/', H + '/')]:
        if path.startswith(prefix):
            return replacement + path[len(prefix):]
    return path


def stage(path):
    return OUT + '/host_staging/' + path[len(H) + 1:] if path.startswith(H + '/') else path


def deps(raw):
    raw = raw.replace('D-U15–18', 'D-U15,D-U16,D-U17,D-U18')
    return list(dict.fromkeys(re.findall(r'(?:D-U\d+[a-c]?|C\d+|N\d+|P\d+|I-[A-Z]+[ab]?)', raw)))


units = []
template = None
for number, line in enumerate((ROOT / A / 'SYNTHESIS.md').read_text().splitlines(), 1):
    if not line.startswith('| '):
        continue
    cells = [c.strip() for c in line.strip('|').split('|')]
    if len(cells) != 7 or not re.fullmatch(r'(?:C\d+|N\d+|P\d+|D-U\d+[abc]?|I-[A-Z]+[ab]?|E\(n,s\))', cells[0]):
        continue
    ident, deliverable, paths, findings, acceptance, dependency, minutes = cells
    if ident == 'E(n,s)':
        template = {'id': ident, 'source': A + '/SYNTHESIS.md:' + str(number), 'acceptance': acceptance}
        continue
    source_paths = [expand(p) for p in paths.split(';')]
    relevant = []
    for path in source_paths:
        relevant.extend([r for r in evidence.get(path, []) if not r['action'].startswith('keep')])
    numbered = [
        'Read ' + A + '/SYNTHESIS.md:' + str(number) + ' and the complete current allowed file/governing sections; confirm dispatch base and record before hashes in the unit receipt.',
        'Verify against the exact evidence anchors below: ' + acceptance + '. Report each clause separately with its source and observed result.',
        'After an intervening read, reread edited bytes; verify all safety rules, holds and caveats survive; record after hashes, diff and any budget overage. Runtime not exercised = UNVERIFIED.'
    ]
    if any(p.startswith('memory_mirror/') and p.endswith('.md') and Path(p).name not in ('MEMORY.md', 'SESSION_CHECKPOINT.md') for p in source_paths):
        numbered.insert(2, 'Validate nonempty name, description, metadata.type frontmatter; all body links resolve; description agrees with body and governing evidence. Do not edit the shared index.')
    if '5;' in acceptance or ',5;' in acceptance:
        numbered.append('Before shortening, preserve the entire selected historical source span as exact UTF-8 bytes in the named dated file; compare SHA-256 and byte count; keep a resolving redirect. No deletion.')
    numbered.append('Run LLMDB_ROOT=$PWD /usr/bin/python3 -B ' + OUT + '/check_lane.py <LANE> <WT> → exit 0; only the unit files plus its unique receipt files may differ.')
    units.append({'id': ident, 'deliverable': deliverable, 'files': [stage(p) for p in source_paths],
                  'source_files': source_paths, 'finding_ids': findings.split(','), 'checks': numbered,
                  'depends_on': deps(dependency), 'minutes': int(minutes), 'source': A + '/SYNTHESIS.md:' + str(number),
                  'evidence': relevant, 'decision_refs': re.findall(r'\bD[1-5]\b', dependency)})
assert len(units) == 118 and template
byid = {u['id']: u for u in units}
byid['D-U14']['depends_on'] = []  # "before D-U12a mutation" is an ordering promise.


def extra(ident, deliverable, files, findings, dependencies, minutes, checks, sources=None):
    source_paths = files
    unit = {'id': ident, 'deliverable': deliverable, 'files': [stage(p) for p in files], 'source_files': source_paths,
            'finding_ids': findings, 'depends_on': dependencies, 'minutes': minutes, 'checks': checks + [
                'Save before/after hashes and exact observations in the unit receipt; reread after another operation; LLMDB_ROOT=$PWD /usr/bin/python3 -B ' + OUT + '/check_lane.py <LANE> <WT> → exit 0.'],
            'source': sources or A + '/hygiene_planner_brief.md:16', 'evidence': [], 'decision_refs': []}
    units.append(unit)
    byid[ident] = unit
    return unit


extra('H-SETTINGS', 'Repository-scoped hook settings consistent with scoped wrapper; preserve Memento',
      [H + '/.claude/settings.json'], ['F03'], ['D-U2'], 5, [
          'Read complete source JSON and CAA:84–85; stage the complete file, preserving all unrelated settings and enabled plugin configuration.',
          'Parse JSON with stdlib. For this repo the prompt/session-start graft hooks emit zero graft bytes; retain unrelated-repo routing. Use scoped wrapper fixtures, no live hooks or npm.',
          'Memento finalize-session remains enabled project-locally at M/.claude/settings.local.json:3; global omission proves nothing. Preserve reset/300000 ceiling and explicit manual fallback.'])
extra('P14', 'Reviewed new all-store hygiene lesson; preserve new provisional S3 source',
      ['memory_mirror/context-hygiene-must-reach-every-store.md'], ['F07','S-P'], ['P01'], 4, [
          'Read full S3/context-hygiene-must-reach-every-store.md:1–15; verify provisional SHA-256 2b42778bc8f97262f04d55730c414a72ff4d6a3687c52dbac933c1158d31d3e7 and ROOT_CAUSE.md:1–26. Changed source → stop and preserve it, never overwrite.',
          'Reconcile dated no-overwrite/count claims with ROOT_CAUSE; retain MAESTRO-only merge gate role and warnings as temptation plus stakes. Required frontmatter and [[atomic-units-parallel-worktree-lanes]] resolve.'])
extra('P-GDRIVE', 'Reconcile S3 Drive collision into reviewed Git lesson before exporting copies',
      ['memory_mirror/gdrive-rclone-remote.md'], ['F07','S-P'], [], 4, [
          'Read complete S1 and S3 gdrive-rclone-remote.md and CAE collision evidence; save both source versions in the unit receipt before reconciliation.',
          'Replace S3:21 nonexistent storage-archival-policy.md with the existing EXPERIMENT_RUNBOOK.md §3.3a authority; retain dated OAuth/capacity facts, current adopted R2 pointer and activation hold. Do not infer live token health.',
          'Reviewed Git body links and frontmatter pass; preserve newer justified cache lesson and all storage/deletion gates. Export copies only after I-MANIFEST.'])

# Broken Git link closes only after the target has actually been imported.
byid['N27']['depends_on'].append('P10')

# A single data authority holds all retired values, exemption paths and approved differences.
extra('DG1', 'Saved retired-instruction/history-scoping behavioral RED',
      ['tests/test_context_hygiene_guard.py','tools/context_hygiene_guard.py'], ['F01','F02','F03','F05','S-P'], [], 7, [
          'Write tests FIRST, then a minimal nonenforcing stdlib CLI stub in the listed tool file (parse arguments, return success). This is a deliberately unqualified baseline, never installed in hooks/CI. Tests run the actual stub and fail on the intended missed violations; save behavioral RED before DG3 replaces the stub.',
          'Write stdlib unittest CLI fixtures before implementation: active reviewer/default gpt-5.5 fails, bare historical model name does not; current pin e6ac7e18 fails, dated retired pin history does not.',
          'Assert active /workspace, Codex ~20% handoff and internal SSD archive fail; dated fenced history and SESSION_CHECKPOINT history/CORPUS/results paths pass. Undated current instruction inside a history-looking file still fails outside an explicit exempt span/path.',
          'CLI contract: /usr/bin/python3 -B tools/context_hygiene_guard.py --root <R> --policy <P> --cache-manifest <C> --host-root <H> --mode staged|applied. Missing/malformed policy or unobserved store fails closed; stdout one line per failure, nonzero status.',
          'Save exact failing assertion/exit output in receipt; do not accept dependency/import/syntax errors as behavioral RED. Freeze tests for DG3.'])
extra('DG2', 'Single reviewed drift policy data file', ['tools/context_hygiene_policy.json'], ['F01','F02','F07'], ['DG1'], 6, [
          'Valid JSON, schema_version=1; only this data file defines retired regex/value rules and instruction paths: CLAUDE/AGENTS/DISCIPLINE/bootstrap/AUTONOMY, current checkpoint prefix, global guides, memory-note active prose, program_state/config/hooks.',
          'Declare exact path exemptions CORPUS/**, results/**, docs/session_summaries/** and explicit dated history headings/spans. Do not exempt whole active mixed documents or labels such as old/current without a date.',
          'Retired values: gpt-5.5 only in reviewer/default roles; e6ac7e18 only as current pin; /workspace active instructions; Codex ~20% handoff; internal SSD as archive. Preserve data-only historical/config-test mentions.',
          'Same-name note differences require exact basename + store pair + reason + approved hashes entry. Only role-specific MEMORY.md indexes have an initial justified difference; blanket wildcards never allowed. Body links are checked outside historical exemptions.'])
extra('DG3', 'Fail-closed retired-instruction scanner', ['tools/context_hygiene_guard.py'], ['F01','F02','F03','F05'], ['DG2'], 8, [
          'Implement the DG1 CLI with argparse/pathlib/json/re only, Python 3.9 stdlib. No network, host writes or project imports. Consume policy data; do not duplicate retired values in code.',
          'Mask only explicitly dated history spans/path exemptions; active instruction violations emit rule ID and exact file:line. Missing policy/inputs, unreadable instruction files and malformed data fail closed.',
          'Classify host_staging files by their logical H-relative instruction paths BEFORE historical results/** exemption matching; staged host files cannot escape scanning because their physical path is under results/.',
          'Run /usr/bin/python3 -B tests/test_context_hygiene_guard.py → all DG1 fixtures GREEN, including positive and historical negative controls. Preserve saved RED.'])
extra('DG4', 'Saved three-store/body-link behavioral RED', ['tests/test_context_hygiene_guard.py'], ['F07'], ['DG3'], 7, [
          'Add fixture cases: identical notes pass; one-byte divergence fails; exact approved hash pair passes; changed hash or unknown file does not inherit allowlist permission; differing role indexes pass only explicit entry.',
          'Three stores missing/denied/malformed/empty manifest fail; same filename absent from a store is governed by exact manifest membership, not guessed universal replication.',
          'Resolvable [[wiki]], relative .md, reference .md and explicit Git-source link pass; broken body link fails even if index resolves; CI staged host root and applied host root produce same findings.',
          'Add private-config CI projection controls: missing/stale source hash or missing line coverage fails; retired-value guidance cannot be redacted. Applied mode observes complete real config and ignores projection substitutions.',
          'Save behavioral failures before DG5 changes tool; never weaken DG1 fixtures.'])
extra('DG5', 'Three-store hash and body-link scanner', ['tools/context_hygiene_guard.py'], ['F07'], ['DG4','I-MANIFEST'], 8, [
          'Consume manifest exact S1/S2/S3 membership. Staged mode maps H-relative paths under host_staging; applied mode reads actual H without writes. A missing/denied expected store/file is failure, never empty success.',
          'Compare all shared basenames, including role indexes; allow differences only when policy store pair/reason/current hash entries match. Validate body links in all retained notes and edited guidance with explicit Git-source resolution.',
          'Staged CI reads the exact verified configuration projection for the two private paths from manifest.ci_projections_file. Require every source line covered by retained line text or an approved secret-only redaction; label CONFIG PROJECTION scope. Applied mode reads complete actual H files. Projection absence or mismatched source receipt is failure.',
          'Run /usr/bin/python3 -B tests/test_context_hygiene_guard.py → DG1 and DG4 GREEN; staged fixture contains no real user host dependencies.'])
extra('DG6', 'Drift guard wired into pre-commit and CI', ['tools/git_hooks/pre-commit','.github/workflows/ci.yml'], ['F01','F07','S-P'], ['DG5','I-CACHE'], 7, [
          'Read complete hook and CI first. Add rooted stdlib guard invocation; retain generated-state/fingerprint/secret checks and exact existing CI jobs.',
          'CI uses integrated host_staging and exact reviewed cache manifest; no access to real H needed. Hook fails nonzero on active retired-value or divergent-copy/broken-link fixture.',
          'Never require/track full private config/settings in CI. CI uses PRIVACY exact public projections plus complete nonsecret host guides/cache bodies; applied guard uses private originals. Keep that verification boundary explicit in job output.',
          'Verify bash -n tools/git_hooks/pre-commit; fixture CI command passes valid bundle and fails intended invalid bundle. Do not run commit, CI dispatch or network.'])
extra('DG7', 'Saved closeout drift-report behavioral RED', ['tests/test_closeout_context_hygiene.py'], ['F07','S-P'], ['I-SYNCb','DG5'], 6, [
          'Write local fixtures before integration. Guard success yields named CONTEXT HYGIENE GREEN; guard failure/missing/unobserved inputs yields named RED/UNAVAILABLE with details.',
          'Preserve scientific presence/currency and memory WARN advisory semantics. New drift guard report is explicit; standalone guard/CI/precommit enforce hygiene without silently redefining scientific PASS.',
          'Save behavioral RED against existing closeout report in unit receipt; fixture-only, no scientific closeout or project Python.'])
extra('DG8', 'Reported drift check in closeout', ['tools/closeout_check.py'], ['F07','S-P'], ['DG7'], 6, [
          'Implement the named context-hygiene report with explicit root/policy/manifest/host mode; report observed failures and denied/missing stores honestly.',
          'Run /usr/bin/python3 -B tests/test_closeout_context_hygiene.py and tests/test_context_memory_sync.py → GREEN; preserve memory WARN advisory and all existing scientific gates.',
          'No change to scientific acceptance criteria: guard report is separate; CI/precommit enforce hygiene. Preserve current argv/API compatibility and do not import model code.'])

# Replace broad implicit dependencies with concrete IDs.
note_ids = [u['id'] for u in units if any(p.startswith('memory_mirror/') and Path(p).name != 'MEMORY.md' for p in u['source_files'])]
byid['I-GIT']['depends_on'] = note_ids
byid['I-MANIFEST']['checks'].insert(1, 'Use the exact 196 export candidates in ' + OUT + '/export_candidates.json; record final reviewed S1 SHA-256, before-host hashes, all link dependency choices, retained tombstones and role index treatment. No extra path or automatic provisional overwrite; changed census → MAESTRO reconciles and regenerates dispatch.')
byid['I-MANIFEST']['checks'].insert(2, 'Schema contract: schema_version=1, host_home, roots {S1,S2,S3}, exports [{id,store,filename,source_path,source_sha256,host_path,host_before_sha256,staging_path}], role_indexes, policy_path. Exact names agree with E units below.')
byid['I-SYNCa']['checks'].insert(1, 'Saved fixture behavioral RED then GREEN; test explicit both-cache inputs and missing/stale/denied/malformed/empty observations plus body-link failures. No live cache access in tests.')
byid['I-SYNCa']['checks'] = [c.replace('Saved fixture behavioral RED then GREEN;', 'Save intended behavioral RED now; I-SYNCb later owns GREEN;') for c in byid['I-SYNCa']['checks']]
byid['I-SYNCb']['checks'].insert(1, 'Implement exact manifest/both-cache report for frozen I-SYNCa tests. /usr/bin/python3 -B tests/test_context_memory_sync.py → GREEN; WARN remains advisory and scientific gates unchanged.')
for ident in ['D-U13a','D-U13b','D-U15','D-U16','D-U19']:
    byid[ident]['checks'].insert(1, 'Renderer contract: full current queue is in EXPERIMENT_RUNBOOK.md §0.3; other destinations get current scoped summaries/pointers. Preserve holds, finalized/open status and registered tokens. Tests exercise root and one-destination output; no broad --write during parallel owners.')
byid['D-U13a']['checks'].insert(2, 'Freeze test-first fixture RED for rooted per-destination render_view(state, destination) and CLI --destination; absent/broken holds and stale token intentionally fail. Freeze all five current destinations and complete safety statements.')
byid['D-U13a']['checks'].insert(3, 'Capture initial behavioral RED through the existing tools/render_state.py render(block, state)/apply() output in temporary fixtures: assert compact per-destination semantics and retained holds/tokens against actual old output. Missing render_view or unknown --destination errors do not count as behavioral RED. The new API is the DG-independent renderer implementation target for D-U13b.')
byid['D-U13b']['checks'].insert(2, 'Implement render_view(state, destination) and --destination writing exactly one named file; /usr/bin/python3 -B tests/test_render_state_context_hygiene.py → GREEN. Retain --check existing behavior; do not mutate views owned elsewhere.')
for ident in ['D-U15','D-U16','D-U19']:
    byid[ident]['checks'].insert(2, 'Read-only final render parity/fingerprint audit must pass for owned destinations; regenerate only owned files. Existing stale narrative tokens are corrected only in this unit allowlist; outside-scope defect → BLOCKED with owner path.')
for ident in ['C1','C2','C5','N13','N17','P09','D-U4','D-U5','D-U6','D-U16','I-CACHE']:
    byid[ident]['checks'].insert(1, 'Binding correction: ' + A + '/maestro_synthesis_check.md:15 confirms enabled project-local Memento. Preserve finalize-session, 300000 ceiling and manual clean-boundary fallback; new work ≥60%, watcher stop at 45%, successor by ≤40% or compaction. Never infer inactive from global settings.')
for ident in ['C11']:
    byid[ident]['checks'].insert(1, 'Stage complete credential-bearing config privately without printing values; preserve secrets byte-for-byte. Probe only binary path existence/PATH with stdlib; no MCP/server startup. MAESTRO must exclude credential content from commits and public Astra packets; use reviewed redacted diff and host-private original.')
for ident in ['D-U20','D-U21','D-U22']:
    byid[ident]['checks'].insert(1, 'Patch is against current MAESTRO-frozen M/master file hash, not a wholesale copy. Preserve every unrelated forward edit; read-only git apply --check in a temporary exact snapshot proves applicability. Master drift → rebase reviewed patch, no direct main mutation.')

# The source-state owners need their own precise evidence, not a later view owner.
state_rows = [r for rows in evidence.values() for r in rows if 'docs/program_state.json' in r['evidence'] or
              (r['audit'].endswith('audit_caf_anchor_docs.md') and 60 <= r['audit_line'] <= 66)]
for ident in ['D-U12a','D-U12b','D-U12c','D-U14']:
    byid[ident]['evidence'] = list({(r['audit'],r['audit_line']):r for r in state_rows}.values())
byid['D-U12a']['checks'].insert(1, 'Edit only top-level updated/current_latest strings (docs/program_state.json:3–6); retain current work_queue and all concurrent progress. Replace stale historical bulk with resolving archive/current pointers after D-U14. Do not re-author next_actions/f1_verdict/scorecard here.')
byid['D-U12b']['checks'].insert(1, 'Edit only next_actions (docs/program_state.json:7–23); compare each current action against named runbook authority and operator grant/hold. NEW-1 consumed authority stays consumed; no Intel deployment/B3N frontier/gpt-5.5/Sonar promotion fallback. Preserve work_queue and latest newer holds.')
byid['D-U12c']['checks'].insert(1, 'Edit only f1_verdict/scorecard (docs/program_state.json:24 onward); governing docs/F1_DETERMINATION.md:3–11,27–29 plus CORPUS/23:24–25. Finalized NOT-READY-WITH-CONDITIONS scope is distinct from open implementation conditions; preserve all fingerprint tokens and work_queue.')
byid['D-U14']['checks'].insert(1, 'Bounded exact archive: preserve the COMPLETE original docs/program_state.json as a fenced JSON byte sequence. Exact case-sensitive spans: SESSION_BOOTSTRAP.md, SESSION_CHECKPOINT.md, EXPERIMENT_RUNBOOK.md, README.md use <!-- BEGIN GENERATED:program-state --> through <!-- END GENERATED:program-state -->; PROGRESS.md uses <!-- BEGIN GENERATED:f1-scorecard --> through <!-- END GENERATED:f1-scorecard -->. Preserve each marker/content byte sequence, labelled source/hash/length; round-trip extraction equals original. Missing/duplicate markers → BLOCKED, not guessed extraction. Do not relocate unrelated tails.')
byid['D-U2']['source_files'].append('tests/test_context_graft_hooks.py')
byid['D-U2']['files'].append('tests/test_context_graft_hooks.py')
byid['D-U2']['checks'].insert(1, 'Write stdlib fixture runner tests/test_context_graft_hooks.py FIRST; run the actual staged CJS helper with /opt/homebrew/bin/node inside a temporary fake home/repo and stub any graft subprocess to fail if called. Positive this-repo fixture emits no graft; unrelated-repo fixture preserves routing. No real hooks, graft invocation, npm, network or installs. Save RED before edit, then GREEN.')
byid['D-U2']['checks'].insert(2, 'Before ANY baseline execution, isolate the real helper bytes at its filesystem/module/child-process boundaries: :7 BAKED absolute installed path, :58 resolution precedence, :67 dynamic hooks.js import, require/package probes and npm fallback are all stubbed/denied. Only fake-home fixture hooks.js may be imported; assert its marker in unrelated-repo output and zero real installed graft imports/subprocesses. Fake HOME alone is insufficient. Do not execute an unisolated helper even for RED.')
byid['D-U3']['source_files'].append('tests/test_context_skill_router.py')
byid['D-U3']['files'].append('tests/test_context_skill_router.py')
byid['D-U3']['checks'].insert(1, 'Write stdlib fixture runner tests/test_context_skill_router.py FIRST; execute the actual staged router via /bin/bash in isolated fake home with every external command stubbed. Verify craft compatibility/routing, ≤440-byte payload and authorized durable handoff; no /clear or delegation. Save RED then GREEN; no live router/plugin activation.')

extra('PRIVACY', 'Reviewed public configuration projections for CI; full proposals stay private',
      [OUT + '/ci_host_projection.json'], ['F05','S-P'], ['C11','H-SETTINGS'], 6, [
          'Read complete private staged .codex/config.toml and .claude/settings.json without printing credentials. MAESTRO resolves git rev-parse --git-path info/exclude (linked worktrees share this common-dir file), serializes that file with all other writers and adds only the exact two private staging path exclusions while preserving existing bytes. git check-ignore --no-index in EACH worktree confirms both. Builders never edit .git/exclusion metadata; no private full file may be staged or committed.',
          'Create schema_version=1 projection: files [{host_path,source_sha256,source_bytes,source_line_count,retained_lines:[{line,text}],redacted_lines:[{line,reason}]}]. Each source line appears exactly once. Redact credential values only, preserving structural/config/instruction fields and exact line attribution; any guidance/retired-value-bearing line must be retained or publication is BLOCKED for private review. No credentials or credential-derived text in the public file.',
          'Compare every retained line directly to the complete source; record exact full-source hash for applied review, no full-source bytes in public receipts. DG4/DG5 fixture controls verify coverage/hash and fail on omitted guidance.',
          'Host apply ALWAYS copies the complete private staging proposals, never this projection. CI labels projection-only config scope; final applied guard/Astra observe full actual config privately.'])
byid['I-MANIFEST']['depends_on'].append('PRIVACY')
byid['I-MANIFEST']['checks'].insert(3, 'Add ci_projections_file=' + OUT + '/ci_host_projection.json and exact private path/source hashes to manifest. Store S1/S2/S3 membership still requires fully observed complete note bytes; config projections do not exempt memory checks.')
for ident in ['DG1','DG4','D-U13a','I-SYNCa','DG7']:
    byid[ident]['expected_red'] = True

exports = []
for store in ('S2','S3'):
    record = stores['retained_cache_manifest_recommendation']['stores'][store]
    names = record['retained_export_filenames']
    if names is None:
        raise ValueError('Inspect export filename field: ' + str(record.keys()))
    for index, name in enumerate(names, 1):
        assert name != 'MEMORY.md' and name != 'SESSION_CHECKPOINT.md'
        ident = 'E-' + store + '-' + str(index).zfill(3)
        source = 'memory_mirror/' + name
        host = (S2 if store == 'S2' else S3) + '/' + name
        owner = [u['id'] for u in units if source in u['source_files'] and u['id'] != 'I-GIT']
        checks = [
            'Read manifest export ' + ident + '; verify final reviewed S1 source hash and host-before hash. Any changed source/cache stops this unit; preserve provisional version in receipt.',
            'Write exactly the complete reviewed Git note bytes to ' + stage(host) + '. SHA-256 and byte count equal manifest and S1; no index edit or deletion.',
            'Confirm all note links resolve locally or to explicit Git authority; closure uses exact manifest sibling files. Required frontmatter remains complete; tombstones stay retired.']
        extra(ident, 'Export ' + name + ' to ' + store, [host], ['F07'], ['I-MANIFEST'] + owner, 2, checks, template['source'])
        exports.append({'id': ident,'store':store,'filename':name,'source_path':source,'host_path':host,'staging_path':stage(host)})
assert len(exports) == 196
extra('E(n,s)', 'Verify exact concrete export assignments replace the synthesis template',
      [OUT + '/receipts/export_contract.json'], ['F07'], ['I-MANIFEST'], 2, [
          'All 196 concrete E IDs in export_candidates.json agree exactly with reviewed manifest; each has one note/cache staging file and one assigned lane. No wildcard or undeclared filenames.',
          'Record template-to-concrete map and source hashes in export_contract.json; this owner writes no notes or indexes.'])
byid['I-CACHE']['depends_on'] = [e['id'] for e in exports] + ['E(n,s)']
byid['I-CACHE']['checks'].insert(1, 'Create role indexes from manifest only; S3 target≤4000 bytes, S2≤20000, both≤24400 hard cap. Existing unindexed/tombstone notes remain on disk, not default recall. Update exact approved index hashes in policy through a separate owner unit, never hidden write.')
extra('DG-INDEX-PINS', 'Freeze approved role-index divergence hashes after index owner',
      ['tools/context_hygiene_policy.json'], ['F07'], ['I-CACHE','DG5'], 4, [
          'Read final S1/S2/S3 role indexes; add exact pair/hash/reason allowlist entries for deliberate index role differences only. Body-note divergence remains failure.',
          'No note/index writes; parse policy JSON, validate current approved hashes, run guard fixture suite and staged full-bundle scan. Report unresolved guard failures by owner; do not suppress.'])
byid['DG6']['depends_on'].append('DG-INDEX-PINS')
byid['DG7']['depends_on'].append('DG-INDEX-PINS')

# Every test/receipt has a unique owner; files never include wildcard allowances.
for u in units:
    prefix = OUT + '/receipts/' + u['id'].replace('(', '_').replace(')', '_').replace(',', '_')
    u['receipt_files'] = [prefix + '/report.md', prefix + '/hashes.json', prefix + '/red.txt', prefix + '/green.txt']
    u['files'].extend(u['receipt_files'])
    u['kind'] = 'host' if any(p.startswith(H + '/') for p in u['source_files']) else 'repo'
    u['pins'] = {p: sha(ROOT / p) if (ROOT / p).is_file() else None for p in u['source_files'] if not p.startswith(H + '/')}
    u['host_before_sha256'] = {p: sha(p) if Path(p).is_file() else None for p in u['source_files'] if p.startswith(H + '/')}

# Longest dependency distance makes waves explicit. Conflicts defer to later waves.
pending = list(units)
scheduled = {}
wave_paths = {}
while pending:
    moved = False
    for u in pending[:]:
        if any(dep not in scheduled for dep in u['depends_on']):
            continue
        wave = 1 + max([scheduled[d]['wave'] for d in u['depends_on']] or [0])
        while set(u['files']) & wave_paths.setdefault(wave, set()):
            wave += 1
        u['wave'] = wave
        wave_paths[wave].update(u['files'])
        scheduled[u['id']] = u
        pending.remove(u)
        moved = True
    if not moved:
        raise ValueError('Dependency cycle/unknown units: ' + str([(u['id'],u['depends_on']) for u in pending]))

lanes = []
for wave in sorted(wave_paths):
    for kind in ('repo','host'):
        selected = [u for u in units if u['wave'] == wave and u['kind'] == kind]
        batch = []
        total = 0
        for u in selected + [None]:
            if u is None or total + u['minutes'] > 36:
                if batch:
                    ident = 'H' + str(wave).zfill(2) + '-' + str(len(lanes) + 1).zfill(2)
                    handoff = OUT + '/receipts/' + ident + '/handoff.md'
                    lane = {'id':ident,'wave':wave,'kind':kind,'units':batch,'total_minutes':total,
                            'base_commit':BASE,'handoff_file':handoff,
                            'requires_dispatch':True,'private_paths':PRIVATE,
                            'allowlist':sorted(set([p for b in batch for p in byid[b]['files']] + [handoff])),
                            'worktree':'<WT>', 'base_protocol':'MAESTRO freezes dispatch base after predecessors; see dispatch/<LANE>.json'}
                    for b in batch:
                        byid[b]['lane'] = ident
                    lanes.append(lane)
                batch=[];total=0
            if u:
                batch.append(u['id']);total+=u['minutes']

data = {'schema_version':1,'host_home':H,'planning_base_commit':BASE,
        'authority':A + '/hygiene_planner_brief.md','operator_decisions':'D1–D5 approved 2026-10-12 01:35Z; hygiene only, pause HIL afterwards',
        'content_rules':CONTENT,'planner_finish_rule':FINISH,
        'source_templates':[template], 'export_candidates_file':OUT+'/export_candidates.json',
        'private_paths':PRIVATE,
        'units':units,'lanes':lanes}
write('lanes.json', json.dumps(data, ensure_ascii=False, indent=2) + '\n')
write('export_candidates.json', json.dumps({'schema_version':1,'status':'exact candidates; I-MANIFEST freezes reviewed bytes before E dispatch',
      'exports':exports,'census':stores['cache_census'],'core_filenames':stores['retained_cache_manifest_recommendation']['core_filenames']}, ensure_ascii=False, indent=2)+'\n')

# LANES.md renders every authoritative field instead of silently shortening checks.
md=['# Context hygiene lanes','', 'JSON authority: '+OUT+'/lanes.json. This Markdown renders the same plan fields.', '',
    'Planning base: `'+BASE+'`. Dispatch base is refreshed by MAESTRO after predecessor integration; builders never commit.',
    'D1–D5 already approved. Every unit ≤8 min; every lane ≤36 min plus 4 min finish reserve. No live application in this planning session.', '',CONTENT,'',FINISH,'']
md += ['Schema version: 1; host_home: `'+H+'`; authority: `'+A+'/hygiene_planner_brief.md`.',
       'Export candidates: `'+OUT+'/export_candidates.json`; source template: `'+json.dumps(template,ensure_ascii=False)+'`.',
       'Exact private paths: '+', '.join('`'+p+'`' for p in PRIVATE)+'.','']
for lane in lanes:
    md += ['## '+lane['id'], '', 'Wave '+str(lane['wave'])+'; '+lane['kind']+'; '+str(lane['total_minutes'])+' min; worktree `<WT>`; base `'+BASE+'`.',
           'Ordered units: '+', '.join(lane['units'])+'.', 'Handoff: `'+lane['handoff_file']+'`.', 'Exact allowlist:', '']
    md += ['Dispatch required: true; identical frozen Git blob ref `refs/context_hygiene/dispatch/'+lane['id']+'`; immutable private seeds allowed only at the exact private paths above.',
           'Base protocol: '+lane['base_protocol']+'.','']
    md += ['- `'+p+'`' for p in lane['allowlist']]
    for ident in lane['units']:
        u=byid[ident]
        md+=['','### '+ident+' — '+u['deliverable'],'','Source: '+u['source']+'; findings: '+', '.join(u['finding_ids'])+'; minutes: '+str(u['minutes'])+'; depends_on: '+(', '.join(u['depends_on']) or 'none')+'.',
             'Source files: '+', '.join('`'+p+'`' for p in u['source_files'])+'.','Files: '+', '.join('`'+p+'`' for p in u['files'])+'.',
             'Decision references: '+(', '.join(u['decision_refs']) or 'none')+'.','Pins: `'+json.dumps(u['pins'],sort_keys=True)+'`; host-before pins: `'+json.dumps(u['host_before_sha256'],sort_keys=True)+'`.','']
        md += ['Expected-RED owner: '+str(u.get('expected_red',False)).lower()+'. Unit kind: '+u['kind']+'; lane: '+u['lane']+'; wave: '+str(u['wave'])+'.',
               'Receipt files: '+', '.join('`'+p+'`' for p in u['receipt_files'])+'.','']
        md += [str(i)+'. '+check for i,check in enumerate(u['checks'],1)]
        for e in u['evidence']:
            md += ['Evidence '+e['audit']+':'+str(e['audit_line'])+'; subject '+e['subject']+'. '+e['evidence']+' Action: '+e['action']+' Replacement: '+e['replacement']]
write('LANES.md','\n'.join(md)+'\n')

for lane in lanes:
    heading=['# '+lane['id']+' builder brief','', 'Worktree: `<WT>` (MAESTRO assigns one isolated worktree). Work from its root.',
             'Wave '+str(lane['wave'])+'; kind '+lane['kind']+'; ordered units '+', '.join(lane['units'])+'; '+str(lane['total_minutes'])+' min plus 4 min finish reserve.',
             'Only hygiene is authorized. D1–D5 were approved at 2026-10-12 01:35Z ("Fix absolutely everything" / "Context hygiene only until it is perfectly tight and durable. Then pause for HIL for next steps.").','',
             '## Paths and authority','', 'A='+A+'; OUT='+OUT+'; H='+H+'; M='+M+' (read-only main); S1=<WT>/memory_mirror; S2='+S2+'; S3='+S3+'; LR='+LR+'.',
             'Read this brief fully. Use the exact source/evidence anchors below, complete edited files and complete governing sections. Historical tracker tails unrelated to the unit need not be loaded.',
             'MAESTRO seeded required external originals under host_staging; never write H or M. Host lanes edit complete staged proposals, not patches/truncated files. Settings/config secrets must remain private; report hashes, never credential values.',
             'Snapshot pins below are provenance, not a license to overwrite later changes. Read current bytes. For predecessor-owned files use dispatch hashes; unexpected drift → BLOCKED.',
             'Memento correction is binding: enabled at M/.claude/settings.local.json:3; keep finalize-session and reset/300000 ceiling. Global absence does not establish inactivity.',
             'Before work: verify pwd, git rev-parse --show-toplevel, git branch --show-current; refuse shared checkout or nonclean sandbox. Every repo tool uses LLMDB_ROOT=$PWD; allowed checks use /usr/bin/python3 -B only. Prefix shell tools with /opt/homebrew/bin/rtk proxy.',
             'MAESTRO records immutable per-lane base/hash receipt at '+OUT+'/dispatch/'+lane['id']+'.json before launch; the checker excludes only that orchestration receipt. Compare entire diff against this base, including untracked/ignored files. Never use HEAD as a moving base.',
             'MAESTRO freezes the identical dispatch JSON as a Git blob ref refs/context_hygiene/dispatch/'+lane['id']+' (not a commit). Missing/mutated receipt or missing ref fails. private_seed_hashes may exempt only unchanged exact private paths; changed private files remain visible to the scope check.',
             'Full host_staging/.codex/config.toml and host_staging/.claude/settings.json are private: MAESTRO-owned exact exclusions in the effective git rev-parse --git-path info/exclude route (common-dir/shared for linked worktrees), serialized setup and effective check-ignore in each worktree; no staging/commits/public receipt copies. Predecessor private inputs travel via frozen hashes, never a commit; other accepted nonsecret bytes enter the clean base. CI receives PRIVACY projection; applied review receives full originals privately.',
             'Separate live progress/status from historical evidence; scientific acceptance, host liveness, runtime hooks and native behavior remain UNVERIFIED unless the named evidence establishes them. No science or activation authorization follows from hygiene.','',
             '## Content rules (verbatim)','',CONTENT,'','## Exact allowlist','']
    heading += ['- `'+p+'`' for p in lane['allowlist']]
    heading += ['', 'No sibling unit, index, generated destination or host file is implicitly allowed. Unit receipts are the listed report.md, hashes.json, red.txt, green.txt; put preserved provisional bytes/history excerpts inside those files rather than inventing outputs.','']
    for ident in lane['units']:
        u=byid[ident]
        heading += ['## '+ident+' — '+u['deliverable'],'','Source '+u['source']+'; findings '+', '.join(u['finding_ids'])+'; '+str(u['minutes'])+' min.',
                    'Dependencies (already in base): '+(', '.join(u['depends_on']) or 'none')+'.',
                    'Exact edit files: '+', '.join('`'+p+'`' for p in u['files'])+'.',
                    'Original source files: '+', '.join('`'+p+'`' for p in u['source_files'])+'.',
                    'Original snapshot hashes: `'+json.dumps(u['pins'],sort_keys=True)+'`; host originals: `'+json.dumps(u['host_before_sha256'],sort_keys=True)+'`.','']
        heading += [str(i)+'. '+c.replace('<LANE>',lane['id']) for i,c in enumerate(u['checks'],1)]
        if u.get('expected_red'):
            heading += ['', 'This is an expected-RED owner: READY means its frozen tests and intended failing assertions are saved and verified, plus scope/frontmatter/link/cap checks pass. It does not claim repaired behavior; the dependent implementation owner must produce GREEN.']
        for e in u['evidence']:
            heading += ['', 'Opened audit row '+e['audit']+':'+str(e['audit_line'])+'; subject '+e['subject']+'.',e['evidence'],
                        'Required action: '+e['action']+'.', 'Replacement lead (verify source before using): '+(e['replacement'] or 'none; follow numbered checks')]
    heading += ['', '## Planner finish rule (verbatim)','',FINISH,'',
                '## Builder finish adaptation','',
                'The quoted CHP tokens/destination are the planner contract. For this lane use the same stop discipline with its own handoff path `'+lane['handoff_file']+'` and reply `'+lane['id']+' HANDOFF`; this keeps parallel lane writes disjoint. Restate ≥60% new-work / 45% watcher stop / ≤40% successor or any compaction in that handoff.',
                'MAESTRO may also stop you before a unit would exceed the remaining session budget. Never start another unit after a stop/compaction. If complete, use READY.',
                'When done run `LLMDB_ROOT=$PWD /usr/bin/python3 -B '+OUT+'/check_lane.py '+lane['id']+' <WT>` and `/usr/bin/python3 -B '+OUT+'/test_check_lane.py`; reread every changed file against this brief. Unexpected RED/denied/unresolved check means BLOCKED. Explicit expected-RED test-author units may be READY with the intended failing assertions saved; every implementation repair requires its specified GREEN.',
                'Reply on its own line exactly one of:', '', '`'+lane['id']+' READY`', '`'+lane['id']+' BLOCKED <reason>`', '`'+lane['id']+' HANDOFF`','']
    write('briefs/'+lane['id']+'.md','\n'.join(heading))

# Exact host routes, including the installed router path and every note export.
host_records={}
for u in units:
    for p in u['source_files']:
        if p.startswith(H+'/'):
            host_records.setdefault(p,[]).append(u['id'])
host=['# MAESTRO-only host application','', 'Builders never write outside <WT>. Copy complete files only after their lanes and dependencies pass. No builder applies a global guide, settings/config, hook or live cache.',
      'Every row below is an exact H-relative staging route. Use the final assembled staging bundle, not an early lane worktree. Host candidates are reviewed; application is MAESTRO-only.','',
      '## Common byte and backup procedure','',
      '1. Freeze the source/staging SHA-256 and byte length; require the staging source to equal the accepted lane receipt/manifest. Freeze the current live target SHA-256/absence. If it differs from reviewed host-before, stop and reconcile; never overwrite concurrent changes.',
      '1a. Serialize host writers before copying: MAESTRO acquires the reviewed per-target lock and pauses/queues every other cooperating editor/service for the complete backup/check/replace/after-check interval. Confirm live hash again immediately after backup and before replace. If any writer cannot participate, stop application rather than infer exclusive ownership.',
      '2. Before each copy, preserve the original bytes, mode and symlink status at H/.claude/context_hygiene_backups/<UTC>/<same H-stripped path>. New target: write an ABSENT receipt at that route plus .absent.json; do not invent an original. Backups are host-private; no secrets in Git or review packets.',
      '3. For note exports require SHA-256(staging)==SHA-256(reviewed S1 source)==manifest.source_sha256 and exact byte lengths. Existing provisional notes must have saved pre-reconciliation bytes/provenance before replacement.',
      '4. Copy to a same-directory temporary file then os.replace under MAESTRO; preserve target mode (or recorded source mode for new files). Reject symlinks unless explicitly reviewed. No deletion or reload/activation commands.',
      '5. Read both complete staging and applied target bytes: bytes equality and SHA-256/length equality must hold; record before, backup, staged, after in host-private receipt. Settings/config must parse; guides/frontmatter/body-links must pass.',
      '6. Run applied-mode drift guard over actual H plus integrated repo; require all stores observed and justified role-index differences pinned. Astra reviews the applied result with redacted configuration diffs and byte/hash receipts. No secrets copied to public repo.',
      'Memento is enabled at M/.claude/settings.local.json:3. Do not disable/remove finalize-session, ceiling, plugins or reset behavior. D-U3 installed-plugin changes may be replaced by plugin upgrade; archive reviewed source hash and re-check after upgrade.','',
      'Private transport: full .codex/config.toml and .claude/settings.json stay in exact ignored host_staging paths with restrictive modes. MAESTRO carries them directly to host apply, hashes-only public receipts. No complete private configs in predecessor commits, CI, master or Astra public packets. PRIVACY produces the line-covered CI projection; applied review uses complete originals privately.', '',
      '## Exact routes','', '| Live file | Complete staging path under <WT> | Owner units | Backup before copy | Byte-for-byte check |','|---|---|---|---|---|']
for path, owners in sorted(host_records.items()):
    stripped=path[len(H)+1:]
    host.append('| `'+path+'` | `'+stage(path)+'` | '+', '.join(owners)+' | `'+H+'/.claude/context_hygiene_backups/<UTC>/'+stripped+'` | `read_bytes(staged)==read_bytes(live)`; SHA-256 + length + reviewed before hash |')
write('host_apply.md','\n'.join(host)+'\n')

plan=['# Context hygiene execution plan','', '**Goal:** make standing guidance consistent across repo/master/host/cache and catch drift; then pause for HIL. No science acceptance is claimed.',
      '**Authority:** hygiene_planner_brief.md; SYNTHESIS §3; all D1–D5 approved. lanes.json is authoritative; briefs are self-contained. All edits this planner made are under '+OUT+'.',
      '**Architecture:** isolated worktree per lane; complete host proposals in host_staging; unique unit receipts; dependency waves; one owner per index and generated file.',
      '**Tools:** Python 3.9 stdlib, /usr/bin/python3 -B; no model/project Python/network/install/commit by builders.',
      '', '## Dispatch and verification','',
      '1. MAESTRO creates isolated worktrees; resolves git rev-parse --git-path info/exclude (shared common-dir in linked worktrees), serializes existing writers, preserves its bytes and adds the exact two private staging paths. Verify git check-ignore --no-index in each worktree before private seeds; never stage/commit full configs. Builders never edit live host/Git metadata.',
      '2. MAESTRO assembles accepted nonsecret predecessor outputs into a clean base; private predecessors travel only as immutable seed files. Freeze dispatch/<LANE>.json {lane,base_commit,input_hashes,private_seed_hashes} and its identical Git blob ref refs/context_hygiene/dispatch/<LANE>. Validate disjoint canonical paths/aliases; changed base or private seed halts.',
      '3. Run lanes within each wave in parallel only after all previous-wave dependencies are accepted. Every unit≤8 min; lane≤36 min +4 finish. Budget means stop/handoff, never compress verification.',
      '4. One Git-index owner follows every Git note reconciliation/import; cache-index owner follows every cache note export. I-MANIFEST freezes exact 196 exports before dispatch, preserving current 12 S3-only lessons (P01–P11 plus P14).',
      '5. Shared file corrections are later-wave owners. No broad renderer --write; D-U15/16 regenerate only their destinations; D-U19 owns runbook/README/PROGRESS. Final parity check is read-only; corrections return to owners.',
      '6. Run each lane checker plus fixture suite, read actual diffs and receipts. Behavioral RED precedes guard/renderer/sync/closeout changes. Preserve warnings/LAWs/holds/Memento; budgets are estimates, not permission to weaken rules.',
      '7. E(n,s) is an assigned export-contract check plus 196 concrete note/cache units. Extra owners cover host settings, the new P14 note, Drive collision and retired-value/store/link drift guard.',
      '8. Checkpoint snapshot frontmatter exemption is historical only. Same-name body notes must agree; role indexes differ only by exact approved hash/pair/reason policy. Denied or missing stores never pass.',
      '', '## Waves','']
for wave in sorted(wave_paths):
    rows=[l for l in lanes if l['wave']==wave]
    plan.append(str(wave)+'. '+', '.join(l['id']+' ('+l['kind']+', '+str(l['total_minutes'])+'m)' for l in rows)+'.')
plan += ['', '## Final steps — MAESTRO only','',
         '1. Assemble accepted nonsecret bytes, verify private hashes/public projections, every receipt/base and generated/fingerprint parity; resolve owner failures. Never stage/commit full private config/settings. Prepare D-U20–22 master patches against current main hashes, preserving unrelated forward work.',
         '2. Apply complete host staging using host_apply.md backup + before-hash + byte-equality procedure. Settings/hook edits preserve enabled Memento. Credential-bearing config stays private; no secrets in commits.',
         '3. Run LLMDB_ROOT=$PWD /usr/bin/python3 -B tools/context_hygiene_guard.py --root "$PWD" --policy tools/context_hygiene_policy.json --cache-manifest results/context_hygiene_20261012/memory_cache_manifest.json --host-root /Users/robertrhu --mode applied; require zero failures across guides, stores and body links.',
         '4. Obtain completed Astra-high review of the applied result and deterministic receipts; address findings through exact owner lanes, then re-verify changed evidence. Hygiene does not qualify runtime hooks/autonomy or lift science/build/activation holds.',
         '5. Operator asked first for master integration. MAESTRO obtains concrete PR/head/master-window GO, inventories and suspends competing writers, drains all candidate-head check/status writers, preserves master CI; integrate solely through tools/git_merge_gate.py and exact-head/full post-merge CI.',
         '6. F01 remains open until master receives the reviewed rules through that gate. Re-run guard over master plus applied host after integration; archive backups/receipts and preserve a scoped handoff. Then pause for HIL next steps.',
         '', '## Context and handoff','',
         'New work starts only at ≥60%; MAESTRO watches every team session, sends stop at 45%, successor by ≤40%. On stop or any compaction: no new unit; preserve done/in-flight/remaining, exact paths/risks and this directive in the lane-specific handoff; root uses OUT/chp_handoff.md.',
         'Planner verification: test_check_lane.py (36 fixtures); re-read every OUT file against the brief; save scoped context/report and exact READY token. No generic /context-save writes outside OUT.',
         '', '## Review focus','',
         '- Active values mixed with dated history: DG1/DG3 exempt only dated spans and exact historical paths.',
         '- Store observation and provisional collisions: P14/P-GDRIVE/I-MANIFEST/DG4/DG5 fail closed and preserve before bytes.',
         '- Scope/aliases/generated destinations: check_lane.py and MAESTRO dispatch validation compare exact paths and frozen base.',
         '- Secrets and concurrent host changes: host_apply.md preserves private backups, before hashes and redacted review.',
         '- Authority confusion: every brief preserves holds, Astra promote gate, Memento and full safety-rule homes.']
assert len(plan)<=120
write('PLAN.md','\n'.join(plan)+'\n')
print(json.dumps({'units':len(units),'lanes':len(lanes),'waves':len(wave_paths),'exports':len(exports),'plan_lines':len(plan)}))
