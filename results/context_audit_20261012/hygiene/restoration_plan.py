"""Append restoration work without rebuilding or renumbering predecessor units."""
import copy
import hashlib
import json
from pathlib import Path


def assemble(root):
    out = Path(root) / 'results/context_audit_20261012/hygiene'
    spec = json.loads((out / 'restoration_spec.json').read_text())
    baseline_path = Path(root) / spec['baseline_file']
    assert hashlib.sha256(baseline_path.read_bytes()).hexdigest() == spec['baseline_sha256'], 'baseline bytes changed'
    for relative, digest in spec['source_hashes'].items():
        assert hashlib.sha256((Path(root) / relative).read_bytes()).hexdigest() == digest, 'restoration authority changed: ' + relative
    data = json.loads(baseline_path.read_text())
    byid = {u['id']:u for u in data['units']}
    by_lane = {lane['id']:lane for lane in data['lanes']}
    for ident, change in spec['patches'].items():
        byid[ident]['depends_on'] = list(dict.fromkeys(byid[ident]['depends_on'] + change['depends_on_add']))
    additions = copy.deepcopy(spec['units'])
    for u in additions:
        assert u['id'] not in byid
        byid[u['id']] = u
    for u in additions:
        ident = u.pop('append_to_lane', None)
        if ident:
            lane = by_lane[ident]
            assert lane['wave'] == u['wave'] and lane['kind'] == u['kind']
            lane['units'].append(u['id'])
            lane['total_minutes'] += u['minutes']
            assert lane['total_minutes'] <= 36
            lane['allowlist'] = sorted(set(lane['allowlist'] + u['files']))
            u['lane'] = ident
    for wave in sorted({u['wave'] for u in additions if 'lane' not in u}):
        for kind in ('repo','host'):
            batch = []
            total = 0
            selected = [u for u in additions if 'lane' not in u and u['wave']==wave and u['kind']==kind]
            for unit in selected + [None]:
                if unit is None or total + unit['minutes'] > 36:
                    if batch:
                        ident = 'H' + str(wave).zfill(2) + '-R' + str(len(data['lanes'])+1).zfill(2)
                        handoff = 'results/context_audit_20261012/hygiene/receipts/' + ident + '/handoff.md'
                        lane = {'id':ident,'wave':wave,'kind':kind,'units':[u['id'] for u in batch],
                            'total_minutes':total,'base_commit':data['planning_base_commit'],
                            'handoff_file':handoff,'requires_dispatch':True,'private_paths':data['private_paths'],
                            'allowlist':sorted({handoff} | {p for u in batch for p in u['files']}),
                            'worktree':'<WT>','base_protocol':'MAESTRO freezes dispatch base after predecessors; see dispatch/<LANE>.json'}
                        data['lanes'].append(lane)
                        for u in batch:
                            u['lane'] = ident
                    batch, total = [], 0
                if unit:
                    batch.append(unit)
                    total += unit['minutes']
    data['units'].extend(additions)
    data['restoration_authority'] = 'results/context_audit_20261012/hygiene_restoration_brief.md'
    data['restoration_sources'] = spec['source_hashes']
    data['restoration_rows'] = spec['rows']
    data['restoration_owner_addenda'] = spec['owner_addenda']
    data['restoration_baseline'] = {'path':spec['baseline_file'],'sha256':spec['baseline_sha256']}
    data['restoration_supplemental_exports'] = spec['supplemental_exports']
    data['restoration_final_steps'] = spec['final_steps']
    return data


def render_map(data, spec):
    baseline = json.loads(Path(spec['baseline_file']).read_text())
    old = {u['id']:u for u in baseline['units']}
    units = {u['id']:u for u in data['units']}
    lines = ['# CHP2 restoration map','',
        'Authority: results/context_audit_20261012/hygiene_restoration_brief.md. All repairs below are planned; this session changes only OUT. No host, Git, science or activation work ran.',
        'The starting bundle already had MAESTRO’s uncommitted origin/master correction and M-REFRESH: 329 units, 33 lanes, nine waves. chp2_baseline_lanes.json and chp2_input_manifest.json preserve it; this extension does not replace it with the earlier 328-unit commit.',
        'PRESERVATION aliases: W=this worktree; M=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory; H=/Users/robertrhu; S1=memory_mirror; S2=H/.claude/projects/-Volumes-memit-llm-database-poc-mirror/memory; S3=H/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory; GA=H/.codex/AGENTS.md; HF=H/.claude/memento/handoffs; PS=docs/program_state.json; B=results/compute_storage_brainstorm_20261011T054507Z.',
        'One disposition per row. A source row with multiple readers has multiple precise rows here. COVERED checks are the numbered original unit checks quoted below; NEW unit checks are in LANES.md/lanes.json. A plan or static fixture is not proof of live recall, host operation, current remote state or scientific acceptance.',
        'Correction 2 in operator_hypothesis_worktree_vs_main.md:24–25 binds: findings 44–61 already exist on cached origin/master; local M is stale. The history import is still branch-only in that snapshot. Never propagate the withdrawn “GitHub master has no findings” claim.',
        '', '## Source rows and dispositions','',
        '| Source file:line | Stale or missing reader path | Disposition |','|---|---|---|']
    for row in spec['rows']:
        disposition = row['disposition']
        if disposition == 'COVERED':
            unit = units[row['unit']]
            check = unit['checks'][row['check']-1]
            disposition += ' ' + row['unit'] + ' (check ' + str(row['check']) + ': ' + check + ')'
        elif disposition == 'NEW':
            disposition += ' ' + row['unit']
        lines.append('| ' + ' | '.join(str(s).replace('|','&#124;').replace('\n',' ') for s in (row['source'],row['reader'],disposition)) + ' |')
    lines += ['', '## Every allowed change to an existing unit','']
    for ident in sorted(spec['patches']):
        newdeps = [d for d in units[ident]['depends_on'] if d not in old[ident]['depends_on']]
        if newdeps:
            lines.append('- ' + ident + ': add depends_on ' + ', '.join(newdeps) + '; retain every original field/check/pin/file/ID/wave.')
    lines += ['', 'No existing unit file list, numbered check, deliverable, time, source, pin or wave changed. Existing lanes H02-12, H03-15 and H04-16 append the new RED/policy, GREEN, and queue/manifest units respectively; their totals become 30m, 30m and 35m. New lanes keep their own IDs and disjoint edit sets. All original 196 export candidates remain unchanged; supplemental exports use their own manifest.',
        '', '## Existing owner lane additions','']
    for ident, duties in spec['owner_addenda'].items():
        lines.append('- ' + ident + ': ' + ' '.join(duties))
    lines += ['', 'These lane additions are explicit restoration acceptance duties; they do not rewrite original unit checks. I-GIT/I-CACHE keep the only index edit ownership, D-U15/16/19 keep generated destination ownership, and D-U13b keeps the renderer. R-QUEUE changes source queue fields after D-U12c in the same lane.',
        '', '## Final steps and operator decisions','']
    for ident, text in spec['final_steps'].items():
        lines.append('- ' + ident + ': ' + text)
    lines += ['', 'OPERATOR WORKTREES — recommendation: preserve and keep stale folders launch-held; review refresh individually after main integration. The following are dated PRESERVATION snapshot statuses, not current measurements. Refresh or delete any folder only after the operator decides the exact path/action; deletion additionally needs exact path/size/method approval.', '',
        '| Exact worktree path | Dated status | Source |','|---|---|---|']
    for item in spec['worktree_question']:
        lines.append('| ' + item['path'] + ' | ' + item['status'] + ' | ' + item['source'] + ' |')
    lines += ['', '## Context protocol and saved state','',
        'New work starts only at ≥60%. You cannot see your context level; MAESTRO watches every team session and messages at 45%. On that message or any Context compacted stop starting work, preserve done/in-flight/remaining, exact paths/risks and this rule in OUT/chp2_handoff.md; reply CHP2 HANDOFF. Use a fresh successor by ≤40%; if already finished use READY. This directive survives every handoff.',
        'Scope/context-save: save only inside OUT; no generic skill checkpoint, telemetry, commit or personal-memory writes. chp2_session_context.md records completion/next execution steps; future builders follow their own lane tokens.', '']
    return '\n'.join(lines)
