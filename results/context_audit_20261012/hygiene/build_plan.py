"""Deterministically materialize the CHP plan; writes only beside this script."""
import json
from pathlib import Path

ROOT = Path.cwd()
A = 'results/context_audit_20261012'
OUT = A + '/hygiene'
DEST = ROOT / OUT
H = '/Users/robertrhu'
M = '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory'
S2 = H + '/.claude/projects/-Volumes-memit-llm-database-poc-mirror/memory'
S3 = H + '/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory'
LR = H + '/.claude/plugins/cache/promptctl/laws/0.24.1/hooks/scripts/skill-router.sh'
PRIVATE = [OUT + '/host_staging/.codex/config.toml', OUT + '/host_staging/.claude/settings.json']

def write(name, text):
    path = DEST / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file() or path.read_text(encoding='utf-8') != text:
        path.write_text(text, encoding='utf-8')


def stage(path):
    return OUT + '/host_staging/' + path[len(H) + 1:] if path.startswith(H + '/') else path


# The reviewed predecessor is immutable; restoration appends explicit work.
from restoration_plan import assemble, render_map
data = assemble(ROOT)
units, lanes = data['units'], data['lanes']
byid = {u['id']:u for u in units}
BASE = data['planning_base_commit']
MASTER_CORRECTION = data['master_authority_correction']
CONTENT, FINISH = data['content_rules'], data['planner_finish_rule']
template = data['source_templates'][0]
exports = json.loads((DEST / 'export_candidates.json').read_text())['exports']
wave_paths = {lane['wave']:set() for lane in lanes}
spec = json.loads((DEST / 'restoration_spec.json').read_text())
write('lanes.json', json.dumps(data, ensure_ascii=False, indent=2) + '\n')
write('restoration_map.md', render_map(data, spec))

# LANES.md renders every authoritative field instead of silently shortening checks.
md=['# Context hygiene lanes','', 'JSON authority: '+OUT+'/lanes.json. This Markdown renders the same plan fields.', '',
    'Planning base: `'+BASE+'`. Dispatch base is refreshed by MAESTRO after predecessor integration; builders never commit.',
    'D1–D5 already approved. Every unit ≤8 min; every lane ≤36 min plus 4 min finish reserve. No live application in this planning session.', '',CONTENT,'',FINISH,'']
md += ['Schema version: 1; host_home: `'+H+'`; authority: `'+A+'/hygiene_planner_brief.md`.',
       'Export candidates: `'+OUT+'/export_candidates.json`; source template: `'+json.dumps(template,ensure_ascii=False)+'`.',
       'Exact private paths: '+', '.join('`'+p+'`' for p in PRIVATE)+'.','']
md += ['Master authority receipt: `'+OUT+'/master_authority_receipt.json`.',MASTER_CORRECTION,'']
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
        if u.get('master_authority'):
            md += ['Master authority: `'+json.dumps(u['master_authority'],sort_keys=True)+'`.','']
        md += [str(i)+'. '+check for i,check in enumerate(u['checks'],1)]
        for e in u['evidence']:
            md += ['Evidence '+e['audit']+':'+str(e['audit_line'])+'; subject '+e['subject']+'. '+e['evidence']+' Action: '+e['action']+' Replacement: '+e['replacement']]
md += ['', '## Restoration owner lane acceptance', '']
for ident, duties in data['restoration_owner_addenda'].items():
    md += ['- ' + ident + ': ' + duty for duty in duties]
md += ['', 'Restoration source/disposition authority: ' + OUT + '/restoration_map.md; supplemental exact exports: ' + OUT + '/restoration_spec.json.']
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
             MASTER_CORRECTION,
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
        if u.get('master_authority'):
            heading += ['', 'Master source pins: `'+json.dumps(u['master_authority'],sort_keys=True)+'`.']
        for e in u['evidence']:
            heading += ['', 'Opened audit row '+e['audit']+':'+str(e['audit_line'])+'; subject '+e['subject']+'.',e['evidence'],
                        'Required action: '+e['action']+'.', 'Replacement lead (verify source before using): '+(e['replacement'] or 'none; follow numbered checks')]
    for ident in lane['units']:
        for duty in data['restoration_owner_addenda'].get(ident, []):
            heading += ['', '## Restoration acceptance for existing owner ' + ident, '', duty]
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
      '**Master correction:** origin/master=5ccbb836 already includes cleanup 6aa22ab5/PR #21 and PR #22. M/local master=557a58bc is stale; use git show origin/master:<path>. See master_authority_correction.md and receipt. Earlier “cleanup never reached master” claims are withdrawn.',
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
         '1. Follow PRESERVE-INFLIGHT in restoration_map.md before integration; assemble accepted nonsecret bytes, verify private hashes/public projections and receipt/render parity; resolve owner failures. Never commit full private config/settings. D-U20–22 use the frozen origin/master guide hashes, not stale M; MAESTRO rechecks the actual remote head and preserves commits unique to both sides.',
         '2. Apply complete host staging using host_apply.md backup + before-hash + byte-equality procedure. Settings/hook edits preserve enabled Memento. Credential-bearing config stays private; no secrets in commits.',
         '3. Run staged/CI fixture guard and actual applied observation (report ROOT_STALE_MAIN/HOOK_BYTES_DIFFER honestly; keep affected roots held until final refresh). Run LLMDB_ROOT=$PWD /usr/bin/python3 -B tools/context_hygiene_guard.py --root "$PWD" --policy tools/context_hygiene_policy.json --cache-manifest results/context_hygiene_20261012/memory_cache_manifest.json --host-root /Users/robertrhu --mode applied; require zero guide/store/body failures; root/hook failures keep affected paths held and final restoration OPEN until authorized refresh.',
         '4. Obtain completed Astra-high review of applied bytes/receipts with explicitly OPEN root/refresh obligations; final acceptance additionally reviews changed applied root/hook receipts after refresh; address findings through exact owner lanes, then re-verify changed evidence. Hygiene does not qualify runtime hooks/autonomy or lift science/build/activation holds.',
         '5. Operator asked first for master integration. MAESTRO obtains concrete PR/head/master-window GO, inventories and suspends competing writers, drains all candidate-head check/status writers, preserves master CI; integrate solely through tools/git_merge_gate.py and exact-head/full post-merge CI.',
         '6. M-REFRESH-FINAL: AFTER integration, ASK THE OPERATOR before refreshing M local master; verify CORPUS/44–61 and every imported docs/historical_backups/20261011 file by integrated hashes, then actual root and shared core.hooksPath guard. Follow M-REFRESH: preserve/serialize M local work before a reviewed refresh, or keep M launch-held and use a current isolated checkout. F01 stale-folder exposure stays open until that route is corrected; remote cleanup absence is already withdrawn. Re-run guard over actual master/applied host/current launch checkout, archive receipts, then pause for HIL.',
         '7. OPERATOR WORKTREES: present every exact stale-worktree path and dated status in restoration_map.md; operator decides refresh/deletion. No automatic cleanup; recheck current status and preserve bytes before any separately authorized action.',
         '8. PAUSE-HIL: require zero final applied failures and completed Astra-high acceptance, archive receipts and scoped CHP2 context; then pause for next steps. No science/build/activation authorization follows.',
         '', '## Context and handoff','',
         'New work starts only at ≥60%; MAESTRO watches every team session, sends stop at 45%, successor by ≤40%. On stop or any compaction: no new unit; preserve done/in-flight/remaining, exact paths/risks and this directive in the lane-specific handoff; CHP2 uses OUT/chp2_handoff.md.',
         'Planner verification: test_check_lane.py (36 fixtures), test_restoration_plan.py and verify_plan.py; re-read every OUT file against the brief; save scoped context/report and exact READY token. No generic /context-save writes outside OUT.',
         '', '## Review focus','',
         '- Active values mixed with dated history: DG1/DG3 exempt only dated spans and exact historical paths.',
         '- Store observation and provisional collisions: P14/P-GDRIVE/I-MANIFEST/DG4/DG5 fail closed and preserve before bytes.',
         '- Scope/aliases/generated destinations: check_lane.py and MAESTRO dispatch validation compare exact paths and frozen base.',
         '- Secrets and concurrent host changes: host_apply.md preserves private backups, before hashes and redacted review.',
         '- Authority confusion: every brief preserves holds, Astra promote gate, Memento and full safety-rule homes.']
plan[8:8] = ['**Restoration authority:** hygiene_restoration_brief.md and restoration_map.md; original units/checks retained; owner lane addenda bind; supplemental exports have a separate exact manifest.', '']
assert len(plan)<=120
write('PLAN.md','\n'.join(plan)+'\n')
print(json.dumps({'units':len(units),'lanes':len(lanes),'waves':len(wave_paths),'exports':len(exports),'plan_lines':len(plan)}))
