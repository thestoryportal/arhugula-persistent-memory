"""Serialize BK4 editorial decisions from BK1–BK3 evidence; writes only audit folder.

This is an audit-data formatter, not a matcher or a scientific runner. Editorial
sets below identify document relationships after review; overlap scores never
automatically decide identity, uniqueness, or chronology. Run with python3 -B.
"""
import csv
import collections
import hashlib
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
ROOT = OUT.parents[1]
BACKUPS = Path('/Volumes/backups')


def tsv(name):
    with (OUT / name).open() as f:
        return list(csv.DictReader(f, delimiter='\t'))


def jsonl(name):
    with (OUT / name).open() as f:
        for number, line in enumerate(f, 1):
            yield number, json.loads(line)


QUEUE = tsv('program_search_queue.tsv')
MATCHES = {j['inventory_row']: j for j in tsv('matches.tsv')}
SAME = {j['inventory_row']: j for j in tsv('program_same_name_review.tsv')}
DOC = {str(j['row']): j for _, j in jsonl('program_document_review.jsonl')}
CONTENT = collections.defaultdict(list)
ANCHOR = collections.defaultdict(list)
for n, j in jsonl('program_content_evidence.jsonl'):
    CONTENT[j['inventory_row']].append((n, j))
for n, j in jsonl('program_anchor_evidence.jsonl'):
    ANCHOR[j['row']].append((n, j))
COPIES = {j['inventory_row']: j['copies'] for _, j in jsonl('program_byte_copies.jsonl')}
EXACT = {str(j.get('inventory_row', j.get('row'))): j for _, j in jsonl('program_exact_receipts.jsonl')}
REFERRALS = [j for _, j in jsonl('program_referral_receipts.jsonl')]

# Direct document lineages/partial-source relationships, explicitly adjudicated.
# All are nonidentical historical sources, with gap rows retaining their deltas.
RELATED = set('102 133 140 146 231 246 271 272 273 303 347 348 360 370 373 385 387 388 395 451 454 463 465 466 467 468 488 489 472 480'.split())
DOWNGRADE = {
    '89': 'Separate E11 agent-harness council; backup :108 and :137 explicitly exclude wholesale LLM-as-DB council carryover. Reference only.',
    '17851': 'ADF augmentation-seat activation page; backup :186-190 uses this program as an example. Reference only.',
    '17852': 'ADF approach comparison; backup :234-254 offers graph-state integration as one alternative. Reference only.',
    '17856': 'ADF context/session-memory infographic; backup :577-593 explicitly says it is not an LLM-as-database design. Reference only.',
}
SPEC = 'research_and_specs/llm-as-database-v1_2-integrated-spec.md'
MANIFEST = 'reproducibility_manifest_merged_s236.json'
SPECIAL_COUNTERPART = {
    '102': MANIFEST, '133': 'research_and_specs/predecessor_design/memit-llama-deep-research-distillation.md',
    '140': 'docs/framework_findings/framework_finding_memit_ceiling_archival_v1_1.md',
    '146': 'docs/framework_findings/framework_finding_memit_ceiling_archival_v1_1.md',
    '244': 'docs/t_branch_decision_document_v1_1.md',
    '272': 'docs/runbooks/stage_1_sect_runbook_v1_7.md',
    '273': 'docs/runbooks/stage_1_sect_runbook_v1_7.md', '489': MANIFEST,
    '321': 'skills/aisecops-specialist.skill!aisecops-specialist/SKILL.md',
    '454': 'skills/state-consistency-theorist.skill!state-consistency-theorist/SKILL.md',
}
NOTES = {
    '98': 'Actual nine-trial May-1 aggregate, different from May-4 fifteen-trial cohort. Never replace later aggregate.',
    '102': 'Early GPT-J Block-1 architecture/provenance seed; 139 backup-only JSON paths versus merged manifest. Different seed structure, not a newer complete manifest.',
    '119': 'D.1 causal-tracing protocol for Llama-3.1-8B; forward-only hooks and clean/noisy activation restoration. Shared SECT boilerplate is not this protocol.',
    '132': 'D.3 multi-target delta runbook: five jointly optimized facts, three replicates and shared specificity. Base SECT inheritance is not preservation of this delta.',
    '133': 'Full public-cache search report; summary/near-match facts in distillation :156-174. Different source narrative with exported citation markers; external claims unverified. No cache bytes.',
    '140': 'Original S2.16 MEMIT-ceiling v1.0; v1.1 :3-8 and :43-45 explicitly refer to the original as a separate retained record. Preserve original lineage, not latest scientific status.',
    '146': 'Original S2.16 MEMIT-ceiling v1.0; v1.1 :3-8 and :43-45 explicitly refer to the original as a separate retained record. Preserve original lineage, not latest scientific status.',
    '170': 'Raw repository URL list. Four URLs absent from source_urls counterpart plus two URL variants; current same-name source is a synthesis. No external verification in audit.',
    '195': 'Historical v2 filesystem organizer source; regex families, suffix deduplication and proposed reorganization. Audited as text; do not execute.',
    '196': 'Historical v1 organizer source. Audited as text; do not execute.',
    '203': 'S2.11-B probe-band recalibration protocol, multiple alternate consistency predicates and Trial-0 reevaluation. Protocol history, not a current acceptance amendment.',
    '215': 'S2.11-B re-evaluation source applying candidate bands to Stage-2 trial JSONs. Source read only; no computation of experimental verdicts.',
    '218': 'S2.11-B revised sweep JSON; spec_ref and source identify 42 trials/14 configurations, not the original sweep result. No matching full record found.',
    '231': 'S2.12-A substitution patch: fact/probe literals overlap v1.4 runbook; application-order and change history remain distinct.',
    '244': 'S2.17 closed-session record of v1.6 hardening and T.2 ROME authoring. Later branch decision refers to session; it is not this complete summary.',
    '245': 'S2.18 closed-session ROME record, Trial-0 pathologies, OQ closures and forward routing. Generic shared text is not this session record.',
    '246': 'S2.18 forensic appendix; source patches overlap rome-patches-canonical.md, with distinct cell trajectory, pathology and diagnostic history.',
    '271': 'v1.4-to-v1.5 substitution patch: code/literals absorbed in v1.5, but patch narrative and authoring instructions form a separate history artifact.',
    '272': 'Full v1.6 SECT anchor, later than full v1.5 but explicitly superseded by repo v1.7 delta :13-15. v1.7 :40-64 and :519 relies on inherited v1.6 cells; preserve full anchor as history.',
    '273': 'Full v1.6 SECT anchor, later than full v1.5 but explicitly superseded by repo v1.7 delta :13-15. v1.7 :40-64 and :519 relies on inherited v1.6 cells; preserve full anchor as history.',
    '303': 'Early T.2 ROME v0.1 runbook; v0.2 counterpart absorbs later empirical and multi-token fixes. Older full authoring state.',
    '318': 'Exported GAP-4 conversation on path-conditional delegation tokens and HIL interfaces. Export framing and detailed discussion not found as a matching document.',
    '332': 'CFB v1.1 GPT-J sports corpus and empirical-capture annotations. Later v2/v3 corpora use different facts/targets; generic YAML keys are not content identity.',
    '339': 'Two-member framework-spec-writer package: project-specific authoring rules plus artifact templates. Both members content-searched; integrated-spec boilerplate is not package preservation.',
    '347': 'GS10 Warden consolidation: substantive C-BOOT-1/3/4/6/7 clauses at backup :174-180 are preserved in v1.2; the full session narrative remains a distinct source.',
    '348': 'GS10 older-schedule probe-generalization summary: probe_sub_type and judge_config definitions at backup :83-87 are present in v1.2; partial clause preservation, not full session identity.',
    '360': 'GS4 ceremony-authorization summary: ceremony token types and signature-verification rule at backup :91-106 are present in v1.2; partial clause preservation.',
    '370': 'GS8 calibration/source-store summary: migration corpus, fidelity measurement and class-hop epsilon protocol at backup :47-57 are present in v1.2; session remains distinct history.',
    '373': 'GS9 provenance/ledger summary: FRESH/STALE and IC-EXT-PROV1/2 at backup :80-81 and :157-163 are present in v1.2; partial substantive preservation.',
    '383': 'IC amendment bundle with insertion targets and interface review rationale. Common spec-block templates do not prove this full bundle was preserved.',
    '385': 'Original 13-cell Kaggle reference notebook; actual patch code overlaps canonical patches, with notebook-specific execution sequence and environment history.',
    '387': 'Integrated spec v1.0 predecessor; substantive baseline retained in v1.2 with amendments. Preserve original historical specification without replacing governing v1.2.',
    '388': 'Integrated spec v1.1 predecessor; substantive baseline retained in v1.2 with amendments. Preserve original historical specification without replacing governing v1.2.',
    '395': 'MEMIT patches earlier revision (filename v2.4; header :4 still v2.3); current v2.5 incorporates later S2.8/S2.9 clauses. Filename alone is not authority.',
    '398': 'Session-2 MEMIT specialist summary: write-engine choice, tiers, larql and verification. Low shared template hit in security summary is wrong-session evidence.',
    '412': 'Pre-S2.6 fork summary records production/provenance of five .npz caches. It is a summary, not those caches; generic shared summary separators rejected.',
    '413': 'GPT-J CFB v1.1 probe set and captured revisions. Later high-AKD probe set is a different cohort; generic YAML fields rejected as identity.',
    '416': 'Nineteen MD5 checksum entries for early program artifacts. Expected checksums do not restore any referenced bytes.',
    '442': 'S2.6 original summary: Cells 0-8 PASS and Cell-9 Trial-0 HALT/root-cause/P-7 record. Generic summary separator matches rejected.',
    '454': 'Older SCT Markdown skill; current archive replaces placeholder with 89 lines of interface-contract content. Distinct revision, not normalized equality.',
    '463': 'Full Session-1 schema conversation; schema summary counterpart :1 and matched sections retain a subset. Conversation provenance and full turns remain separate.',
    '464': 'Full Session-2 MEMIT conversation; security-session template hits rejected. Distinct engine-design exchange, not a matching security transcript.',
    '465': 'Full Session-3 threat-model conversation; summary preserves substantial threat/spec blocks, not the complete original exchange.',
    '466': 'Full Session-4 validation conversation; validation summary preserves substantial blocks, not complete original exchange.',
    '467': 'Full Session-5 consistency conversation; 2PC summary preserves substantial blocks, not complete original exchange.',
    '468': 'Full Session-6 orchestration conversation; requirements matrix preserves capability evaluation, not complete original exchange.',
    '469': 'Full Session-7 council-synthesis conversation and successive drafting turns. Small v1.2/template overlaps do not establish preservation of this conversation.',
    '488': 'Earlier canonical patches v2.0 document; current v2.5 retains core patches and adds later mechanisms/process constraints.',
    '489': 'Early v2.0 manifest: no backup-only leaves against merged manifest; metadata changes only, plus many later counterpart leaves. Historical subset.',
    '17853': 'ADF-to-ArhuGula architecture integration sketch, backup :228-241: frozen base/vindex read path, validated larql-to-MEMIT writes and Git-overlay transaction synchronization. No matching sketch found.',
    '17857': 'ADF-to-ArhuGula handoff-learning page, backup :451-452 cognitive-state mapping rules. Labviz index.html is wrong subject; no matching page found.',
}


def compact_path(path):
    prefix = str(ROOT) + '/'
    return path[len(prefix):] if path.startswith(prefix) else path


def first_title(row, backup):
    if row in DOC:
        for x in DOC[row]['extracts']:
            s = x['text'].strip()
            if s.startswith('#') and not s.startswith(('# ===', '# ---', '# _____')):
                return s.lstrip('# ').strip()[:180]
        ex = DOC[row]['extracts']
        if ex and backup.endswith('.json'):
            return 'Historical structured program record: ' + Path(backup).name
    return Path(backup).name


def best_hit(row):
    hits = [h for _, j in CONTENT[row] for h in j['hits']]
    # Prefer verified full identity, then a selected-worktree counterpart.
    hits.sort(key=lambda h: (h.get('normalized_identical', False), h.get('custody') == 'worktree', h.get('query_line_coverage', 0)), reverse=True)
    return hits[0] if hits else None


def serialize():
    all_rows = []
    wanted = {j['backup'] for j in QUEUE} | {str(Path(j['backup']).relative_to(BACKUPS)) for j in REFERRALS}
    inventory = {}
    with (OUT / 'inventory.tsv').open() as f:
        for i, j in enumerate(csv.DictReader(f, delimiter='\t'), 1):
            if j['path'] in wanted:
                inventory[str(i)] = j
    assert len(inventory) == 298
    for q in QUEUE:
        row, backup = q['inventory_row'], q['backup']
        inv = inventory[row]
        initial = q['initial_match']
        evidence = ['program_search_queue.tsv inventory_row=' + row]
        evidence += [f'program_content_evidence.jsonl:{n}' for n, _ in CONTENT[row]]
        evidence += [f'program_anchor_evidence.jsonl:{n}' for n, _ in ANCHOR[row]]
        counterpart, custody, comparison = '', '', ''
        if initial == 'EXACT':
            match, comparison = 'EXACT', 'HISTORICAL-BYTE-IDENTICAL'
            m = MATCHES[row]
            counterpart, custody = m['repo_or_mirror_path'], 'reachable-history; commit=' + m['commit']
            evidence += ['program_exact_receipts.jsonl inventory_row=' + row, 'bk3_identity_verification.json']
        elif row in SAME and row not in {'321', '17857'}:
            match = 'SAME-NAME'
            s = SAME[row]
            comparison, counterpart = s['reviewed_comparison'], s['actual_counterpart']
            evidence.append('program_same_name_review.tsv inventory_row=' + row)
        elif q['search_evidence'] == 'FILESYSTEM-BYTE-IDENTICAL':
            match, comparison = 'CONTENT', 'FILESYSTEM-BYTE-IDENTICAL'
            counterpart = COPIES[row][0]['path']
        elif q['search_evidence'] == 'NORMALIZED-CONTENT-IDENTICAL':
            match, comparison = 'CONTENT', 'WHITESPACE-CONTENT-IDENTICAL'
        elif row in RELATED or row == '321':
            match, comparison = 'CONTENT', 'DIVERGENT-HISTORICAL-SOURCE'
        else:
            match, comparison = 'UNIQUE', 'NO-DOCUMENT-COUNTERPART-IN-SEARCH-SCOPE'
        hit = best_hit(row)
        if not counterpart and match == 'CONTENT' and hit:
            counterpart = hit['source'] + ('!' + hit['member'] if hit['member'] else '')
        if row in SPECIAL_COUNTERPART:
            counterpart = SPECIAL_COUNTERPART[row]
        if not counterpart:
            counterpart = SPEC + ' (thematic context; no matching document)'
        if not custody:
            if row in COPIES:
                custody = 'mirror-outside-worktree; all copies in program_byte_copies.jsonl'
            elif counterpart.startswith(str(ROOT) + '/') or (not counterpart.startswith('/') and 'thematic' not in counterpart):
                custody = 'worktree counterpart; see path/member; not necessarily original-file Git custody'
            else:
                custody = 'mirror-outside-worktree' if counterpart.startswith('/') else 'context only'
        final_class = 'adjacent' if row in DOWNGRADE else 'program'
        if row in DOWNGRADE:
            comparison = 'ADJACENT-REFERENCE'
        divergent = comparison in {'OLDER', 'DIFFERENT-COHORT', 'DIVERGENT-URL-LIST', 'DIVERGENT-MANIFEST', 'DIVERGENT-SKILL', 'DIVERGENT-ARCHIVE', 'DIVERGENT-HISTORICAL-SOURCE'}
        gap = final_class == 'program' and (match == 'UNIQUE' or divergent)
        notes = NOTES.get(row, '')
        if row in SAME:
            notes = (notes + ' ' + SAME[row]['evidence_and_interpretation']).strip()
        if not notes:
            if match == 'UNIQUE':
                notes = 'Distinct historical source document; whole-mirror same-size bytes, normalized/distinct-line and phrase searches did not establish a document counterpart. Shared titles, spec templates and generic snippets are not preservation of its session/version rationale.'
            elif comparison == 'DIVERGENT-HISTORICAL-SOURCE':
                notes = 'Related source/descendant contains substantive portions; full source record and revision differences remain distinct. See saved pair/member diffs.'
            else:
                notes = 'Identity/comparison evidence retained; no scientific rerun or current acceptance inferred.'
        if row in DOWNGRADE:
            notes = DOWNGRADE[row]
        recommendation = 'import as superseded history' if gap else 'ignore'
        if row in {'170', '133', '17853', '17857'} or final_class == 'adjacent':
            recommendation = 'reference only'
        # One proposed destination per payload. No destination is created.
        target = 'docs/historical_backups/20261011/' + backup if recommendation.startswith('import') else 'none; retain backup reference'
        all_rows.append(dict(inventory_row=row, backup_path=str(BACKUPS / backup), relative_backup=backup,
                             bytes=int(inv['bytes']), sha256=inv['sha256'], git_blob_id=inv['git_blob_id'],
                             original_class='program', final_class=final_class, initial_match=initial,
                             final_match=match, comparison=comparison, what_it_is=first_title(row, backup),
                             counterpart=compact_path(counterpart), custody=custody, recorded_loss='none',
                             recommendation=recommendation, suggested_target=target, gap_table=gap,
                             notes=notes, evidence=evidence, copies=COPIES.get(row, [])))
    for j in REFERRALS:
        row = str(j['row']); inv = inventory[row]
        assert j['verified'] and j['sha256'] == inv['sha256']
        all_rows.append(dict(inventory_row=row, backup_path=j['backup'], relative_backup=inv['path'],
                             bytes=int(inv['bytes']), sha256=inv['sha256'], git_blob_id=inv['git_blob_id'],
                             original_class='adjacent', final_class='program', initial_match=MATCHES[row]['match'],
                             final_match='EXACT', comparison='HISTORICAL-BYTE-IDENTICAL', what_it_is='Project-specific council role archive',
                             counterpart=j['path'], custody='reachable-history; commit=' + j['commit'],
                             recorded_loss='none', recommendation='ignore', suggested_target='none; historical Git copy exists',
                             gap_table=False, notes=j['reason'], evidence=['program_referral_receipts.jsonl row=' + row], copies=[]))
    assert len(all_rows) == 298 and len({x['inventory_row'] for x in all_rows}) == 298
    # Keep one suggested destination for repeated backup payloads without dropping table rows.
    targets = {}
    for j in sorted(all_rows, key=lambda x: (' (1)' in x['relative_backup'], len(x['relative_backup']))):
        if j['recommendation'].startswith('import'):
            j['suggested_target'] = targets.setdefault(j['sha256'], j['suggested_target'])
    all_rows.sort(key=lambda x: int(x['inventory_row']))
    with (OUT / 'program_final_dispositions.jsonl').open('w') as f:
        for j in all_rows:
            f.write(json.dumps(j, ensure_ascii=False) + '\n')
    fields = ['inventory_row','backup_path','bytes','sha256','original_class','final_class','initial_match','final_match','comparison','what_it_is','counterpart','custody','recorded_loss','recommendation','suggested_target','gap_table','notes']
    with (OUT / 'program_final_dispositions.tsv').open('w') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', extrasaction='ignore'); w.writeheader(); w.writerows(all_rows)
    unique = [j for j in all_rows if j['final_match'] == 'UNIQUE' and j['final_class'] == 'program']
    for j in unique:
        assert CONTENT[j['inventory_row']] and ANCHOR[j['inventory_row']]
    final_counts = collections.Counter(j['final_match'] for j in all_rows if j['final_class'] == 'program')
    summary = dict(original_program=292, reviewed_with_referrals=298,
                   final_classes={'program':294,'adjacent':10027,'unrelated':509275},
                   final_program_matches=dict(sorted(final_counts.items())),
                   original_cohort_matches=dict(collections.Counter(j['final_match'] for j in all_rows if j['original_class']=='program')),
                   original_content_pending_matches=dict(collections.Counter(j['final_match'] for j in all_rows if j['initial_match']=='CONTENT-PENDING' and j['original_class']=='program')),
                   gap_rows=sum(j['gap_table'] for j in all_rows), gap_distinct_sha256=len({j['sha256'] for j in all_rows if j['gap_table']}),
                   new_latest_versions=0, content_newer_than_full_v1_5_but_superseded_rows=['272','273'],
                   loss_restoration_identified=0, relevance_overrides=DOWNGRADE)
    assert sum(final_counts.values()) == 294
    (OUT / 'bk4_final_counts.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary, indent=2))
    return all_rows, summary


def render(rows, summary):
    def cell(value):
        return str(value).replace('|', '\\|').replace('\n', ' ').replace('\r', ' ')

    def table(headers, items):
        return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                         ['| ' + ' | '.join(cell(v) for v in values) + ' |' for values in items])

    control = json.loads((OUT / 'positive_control.json').read_text())
    gaps = [j for j in rows if j['gap_table']]
    references = {j['inventory_row']: n for n, j in enumerate(rows, 1)}
    original = [j for j in rows if j['original_class'] == 'program']
    covered = collections.Counter(j['comparison'] for j in rows if j['final_class'] == 'program')
    report = '''# External backups audit — BK4 final report

The audit identifies historical documents and revision gaps worth preserving. It does **not identify backup bytes that restore a specifically recorded RunPod loss**. There are 102 PROGRAM documents classified UNIQUE within the comparison scope, and 148 gap-table file rows (146 distinct SHA-256 payloads), including nonidentical predecessors, partial-content matches and divergent revisions. These are archival recommendations, not scientific acceptance or import authorization.

MAESTRO's scope decision was **A first: the original 292 PROGRAM files (94 EXACT, 58 SAME-NAME, 140 CONTENT-PENDING); B: saved loss evidence and per-candidate mapping; C: group review of the original 10,029 ADJACENT files; D: final report and packaging**. BK3C completed C in commit `7dcf95794ea9880d132a6d4bea18fc4774233d1f`. Its untouched [adjacent_groups.tsv](adjacent_groups.tsv) and [adjacent_dispositions.md](adjacent_dispositions.md) are the C evidence; [adjacent_progress.md](adjacent_progress.md) records coverage. BK4 completed A/B adjudication and D serialization. No imports, source moves/deletions, commits, pushes, installs, experiments, model runs or tmux actions were performed by BK4. All BK4 writes are in this audit folder.

## Coverage and final counts

The volume census and inventory cover **519,596 non-caselaw file entries**: 519,336 regular files and 260 file symlinks. The regular inventory hashed 18,086,613,160 bytes. Of the symlinks, 207 readable referents were hashed; 53 dangling/nonfile targets have explicit blank hashes, not UNIQUE verdicts. Caselaw separately has 41,442 files / 82,397,163,971 bytes, reviewed by names/directory metadata only. Four operator OS folders were excluded. See [census.json](census.json), [caselaw_summary.txt](caselaw_summary.txt), [inventory_complete.json](inventory_complete.json), [symlink_state.json](symlink_state.json), and [symlinks.tsv](symlinks.tsv).

| Cohort | PROGRAM | ADJACENT | UNRELATED | Total |
| --- | --- | --- | --- | --- |
| BK2 original triage | 292 | 10,029 | 509,275 | 519,596 |
| BK4 final relevance | 294 | 10,027 | 509,275 | 519,596 |

Six original adjacent role packages move to PROGRAM; four original program files move to ADJACENT. The original cohorts remain intact in prior artifacts. The final disposition artifacts explicitly carry original and final classes for all 298 reviewed files; the unchanged remainder retains its original class. “Unrelated” is a reasoned volume triage, not a full semantic reading of half a million files.

'''
    report += table(['Final PROGRAM match', 'Files', 'Meaning'], [
        ('EXACT',100,'94 original + six referrals; actual Git blob/commit/path identity, not necessarily current working-tree presence'),
        ('SAME-NAME',56,'Correct-subject basename relationship plus saved byte/whitespace/JSON/member or revision comparison; includes 40 semantic/byte copies, one older manifest subset, 15 substantive differences'),
        ('CONTENT',36,'Renamed/normalized copies or reviewed substantive partial-source/descendant relationships; equality and divergence are separately recorded'),
        ('UNIQUE',102,'No document counterpart established after actual byte, normalized/distinct-line and phrase searches plus semantic review; bounded claim as described below'),
        ('Total',294,'Final relevance cohort')])
    report += '\n\n' + table(['Original A cohort', 'Adjudication'], [
        ('94 EXACT','All locations revalidated by BK3; receipts and source hashes retained'),
        ('58 SAME-NAME','56 remain SAME-NAME; generic SKILL.md resolves to CONTENT via AISecOps payload; index.html resolves to scoped UNIQUE integration page'),
        ('140 CONTENT-PENDING','35 CONTENT + 105 scoped UNIQUE before relevance overrides; four of those UNIQUE triage documents move to ADJACENT')])
    report += '\n\nFinal comparison subtypes are recorded without conflating formatting identity with historical EXACT:\n\n'
    report += table(['Comparison', 'Final PROGRAM files'], sorted(covered.items()))
    report += '''

Full file-level decisions, custody, evidence pointers, loss mappings and suggested destinations are in [program_final_dispositions.tsv](program_final_dispositions.tsv) and [program_final_dispositions.jsonl](program_final_dispositions.jsonl). Counts are serialized in [bk4_final_counts.json](bk4_final_counts.json); [scripts/bk4_finalize.py](scripts/bk4_finalize.py) retains the editorial relationships and regenerates these artifacts/report from the saved evidence. The formatter does not infer uniqueness from a filename or an overlap threshold.

## Required positive control and identity evidence

'''
    report += f'''The real backup `{control['backup_path']}` and worktree `{control['repo_path']}` are byte-identical: **{control['bytes']:,} bytes**, SHA-256 `{control['sha256']}`, Git blob `{control['git_blob_id']}`. The shared matcher returned **EXACT** at commit `{control['location']['commit']}`, path `{control['location']['path']}`; **UNIQUE fallback calls = {control['unique_fallback_calls']}**. Its actual `git ls-tree` receipt and explicit byte check are saved in [positive_control.json](positive_control.json). This demonstrates recognition of a known duplicate; it does not prove exhaustive negative search.

'''
    report += '''All 94 original EXACT locations have commit/path/blob receipts in [program_exact_receipts.jsonl](program_exact_receipts.jsonl), revalidated in [bk3_identity_verification.json](bk3_identity_verification.json). BK3 rehashed all 292 program backup sources with zero changes. Non-Git filesystem copies are deliberately not called historical EXACT. The 35 byte-copy sources all have preservation elsewhere in the mirror; see [program_byte_copies.jsonl](program_byte_copies.jsonl). That does not establish custody in this worktree or Git. In particular, nine early SECT trial JSONs and `llm-as-database/capture_token_ids.py` have byte copies outside the worktree; they are not a newly restored cache/model. Their import consideration is a custody choice, not a uniqueness gap. `stage_2_sweep_verdict.json` has parsed-JSON equality with the mirror copy (436 equal leaves), while `aggregate_verdict.json` describes a different, earlier nine-trial cohort. The latter is in the gap table.

All 58 initial same-name comparisons are in [program_same_name_review.tsv](program_same_name_review.tsv). [program_archive_comparisons.jsonl](program_archive_comparisons.jsonl) compares every member of the 12 non-byte-copy skill archives. The single-member orchestration archive has complete payload/name identity despite different ZIP bytes. Other packages have meaningful role-contract differences; 100% long-line coverage is not full identity. [program_pair_diffs.jsonl](program_pair_diffs.jsonl) preserves available whole-body differences and parsed manifests; [program_document_review.jsonl](program_document_review.jsonl) preserves bounded section extracts. No skill or source script from the backup was executed.

## Content chronology and documentary gaps

**No backup is established as newer than the repo's latest relevant revision.** The two SHA-identical `stage_1_sect_runbook_v1_6` copies explicitly postdate full v1.5 in content (`/Volumes/backups/stage_1_sect_runbook_v1_6.md:12,44` versus `architecture_profile/runbooks/stage_1_sect_runbook_v1_5.md:12`). However, `docs/runbooks/stage_1_sect_runbook_v1_7.md:13-15` explicitly supersedes v1.6; :40-64 and :519 explain inherited v1.6 cells and the later multi-token absorption. Recommend retaining one v1.6 payload as a superseded **full anchor**, alongside the later delta. Do not replace the current runbook or call the backup globally newest. The v1.7 artifact's provisional execution status at :27-36 is preserved as a documentary caveat, not changed by this audit.

The original ceiling finding v1.0 is also useful lineage. `docs/framework_findings/framework_finding_memit_ceiling_archival_v1_1.md:3-8,43-45` says the original is a separate retained record and directs readers to it. The backup carries that original S2.16 document, rather than the later ROME amendment. Later framework findings exist, so it is an original-history recommendation, not the latest governing finding. This is a documented reference/dependency gap; there is no cited record that these particular document bytes were lost with RunPod.

The root manifest has **181 backup-only session leaf values**, six changed metadata values, and 896 counterpart-only leaves against `reproducibility_manifest_merged_s236.json`: mixed provenance history, not a whole-file chronology ordering. The llm-as-database manifest's 338 leaves are all preserved unchanged in the merged manifest (1,055 additional counterpart leaves). The archived v2.0 manifest has no backup-only leaves, with two metadata changes. The architecture seed is a distinct earlier GPT-J structure (139 backup-only paths). See saved pair/JSON diffs. The root URL list and orchestration Markdown skill carry unmatched revision details; additional clauses alone do not prove they are newer.

Council transcripts, gap backlogs/schedules/session records, friction analyses, initial compatibility/calibration protocols, notebooks and session prompts are **historical source documents**. Some portions are present in the integrated spec or descendant summaries; those rows are CONTENT/divergent. Shared decorative separators, version-print code, YAML keys and spec templates were rejected as counterparts for the remaining original documents. These documents may fill archival context gaps; they do not supply unrun calibration results or amend current acceptance criteria.

## Recorded losses and per-file mapping

The systematic saved search is [loss_evidence_search.tsv](loss_evidence_search.tsv): **508 requested-scope files / 1,053 matching lines**, with scope/state in [loss_evidence_state.json](loss_evidence_state.json) and read-context synthesis in [loss_evidence.md](loss_evidence.md). It covers CORPUS/, SESSION_CHECKPOINT.md, EXPERIMENT_RUNBOOK.md, REPRODUCIBILITY.md, docs/, memory_mirror/, and 37 results/ READMEs. Generic “lost/missing/pod” hits include recall loss and fixture process lifecycles; those are not storage-loss records.

| Recorded event | Exact source | What the backup audit establishes |
| --- | --- | --- |
| RunPod balance lapsed; working volume lost | SESSION_CHECKPOINT.md:1053; EXPERIMENT_RUNBOOK.md:89,446,991; REPRODUCIBILITY.md:7 | Named losses are Qwen covariance caches, downloaded HF models, B3 edited model/GGUF, llama.cpp/LARQL builds and run logs. The same record says Workstream-1 docs and the patched engine were recovered via PRs #1/#2. No candidate identified as those lost bytes. |
| Vendored engine preserved | REPRODUCIBILITY.md:9 | Git engine custody is distinct from gitignored downloaded data/stats. Documentation is not a cache. |
| Later local baseline/model/cache regeneration | SESSION_CHECKPOINT.md:1051; EXPERIMENT_RUNBOOK.md:87 | Recorded local redownload/covariance regeneration and C2/A1 reproduction are not recovery from this SSD. |
| Later local B3 export/serving regeneration | SESSION_CHECKPOINT.md:1049; EXPERIMENT_RUNBOOK.md:85 | Later explicit completion qualifies the older generated next-action still referring to regeneration. |
| Pod-era InfraNodus graph export proof lost | memory_mirror/infranodus-discourse-lens-not-coverage-tool.md:20 | No candidate established as that export proof. A shared HTML/CSS anchor in planning pages is unrelated boilerplate. |

**Every gap-table row maps to “none”**: no specific recorded loss is linked to those actual bytes. This does not assert that no documents were ever lost. The public-cache search report is not a cache; the nineteen-entry MD5 list is not its referenced artifacts; the pre-S2.6 summary's five-cache production statement is not five .npz files. No missing model/tensor/covariance/build/scientific run result is claimed restored. The recommendations preserve history or retain references only; imports remain the operator's decision.

## BK3C referrals and relevance overrides

'''
    report += table(['Backup', 'Final class/match', 'Reason and evidence'], [
        (j['backup'], 'PROGRAM / EXACT', j['path'] + ' at commit ' + j['commit'] + '; program_referral_receipts.jsonl') for j in REFERRALS])
    report += '''

The seventh referral, `/Volumes/backups/s3-spec-writer-architecture.md`, remains **ADJACENT / reference only**: :1-7 scopes a different slate and :66-73 drops prior LLM-as-DB council artifacts from its inputs. It is not restored program science. BK3C's original C result is **67 groups / 10,029 unique members**, zero missing/extra/duplicate rows or byte/SHA mismatches; 62 groups reference only, one unclear (credential metadata only), two program-review referrals, two ignore. Group dispositions are not per-member CONTENT/UNIQUE matches. The credential file's contents remain unread.

Four A-cohort demotions have these final dispositions:

'''
    report += table(['Backup', 'Final disposition/evidence'], [(next(j['backup_path'] for j in rows if j['inventory_row']==r), reason) for r,reason in DOWNGRADE.items()])
    report += '''

The two remaining fallback HTML pages, `09-design-architecture.html` and `index.html`, stay PROGRAM as explicit integration/handoff sketches, with the program-specific source lines recorded in their gap rows. Their generic HTML/CSS overlap with an InfraNodus report is not a document match and not recovery of the lost export proof. The four demotions are an audit addendum; BK3C's committed files were not edited.

## GAP TABLE

One row per final PROGRAM file classified UNIQUE or carrying substantive divergent revision/source content, including older predecessors. Formatting-only copies and manifest subsets with no backup-only content are omitted. There are **148 file rows / 146 distinct payload hashes**. Proposed import destinations are new historical-document paths; repeated payloads share a destination. These are suggestions only: nothing has been copied there. The title/decision below is supplemented by full notes and evidence pointers in the exact line of `program_final_dispositions.jsonl` given in the “what it is” cell.

'''
    report += table(['Backup path','Bytes','SHA-256','What it is','Closest repo/mirror counterpart','Recorded loss it fills','Recommendation','Suggested target path'], [
        (j['backup_path'],j['bytes'],j['sha256'],j['final_match'] + ' / ' + j['what_it_is'] + '. ' + j['notes'][:250] + f" [details: program_final_dispositions.jsonl:{references[j['inventory_row']]}]",
         j['counterpart'],j['recorded_loss'],j['recommendation'],j['suggested_target']) for j in gaps])
    report += '''

## Open questions for MAESTRO

1. Which historical sources should the operator approve for import? Prioritize the full v1.6 runbook anchor, original v1.0 ceiling finding, mixed root manifest session leaves, original calibration/compatibility protocols and original session/council records. Retain dated provenance, gated/unrun status and later supersession. A table recommendation is not approval.
2. Should mirror-only byte copies (especially the nine trial JSONs, capture source and parsed-equal sweep JSON) receive Git/clone custody? Their bytes already exist elsewhere in the mirror; this audit recommends deciding custody separately from alleged lost-artifact recovery. All copy paths are saved in program_byte_copies.jsonl.
3. Should the separate E11 council/ADF references remain in the contextual collection? They are useful integration history, with different subjects from program science. Keep credential content outside any document import decision; no credential inspection is required to accept this audit.
4. If broader negative proof is needed, authorize a separate comparison pass over omitted dependency/cache trees, large numeric JSON/IPYNB content, symlink alias paths, or unreachable Git objects. That is additional scope, not evidence that a UNIQUE label here is universally exhaustive.

## Comparison limits and custody

- **Bounded negative claims:** UNIQUE means no matching document established within the saved research-text/history/mirror search scope, after actual content and semantic review. It is not a statement about every byte in every external or unreachable repository. Counterparts labelled thematic context are not asserted matches. Partial merged clauses remain CONTENT/divergent, never full identity.
- **Search shape:** BK2 scanned 60,926 filesystem names, hashed 680 same-sized candidate files independent of basename, searched 41,383 research text/member entries and 12,054 historical blobs. BK3's corrected supplemental scan searched 41,399 text/archive files and 12,475 historical blobs, including larger research text. All 164 file/member phrase queries have nonempty anchors; 51 have hits, 113 none, zero errors. These query counts are not file verdicts. The earlier BK3 unique-anchor-only run was superseded. See program_content_state.json, program_anchor_state.json and their evidence JSONL files.
- **Omissions:** 101 filesystem and 22 historical numeric JSON/IPYNB files over 2 MiB were excluded from phrase indexing; cache/dependency trees were excluded from research-text comparisons. Same-sized byte matching is separate. Reachable all-ref history has 14,697 indexed blobs/18,055 paths; reflog-only/unreachable objects were not indexed. This audit does not certify raw scientific archives excluded by these filters. No full-body reads of source documents over roughly 200 KiB were used; those have streamed/bounded sections, and pair diffs explicitly mark whole-diff unavailability.
- **Concurrent state:** BK1/BK2/BK3 evidence and BK4 follow-up reads span concurrent MAESTRO commits. The reachable blob index is BK1's frozen snapshot; mirror text/counterparts are not one immutable snapshot. Current counterpart reads and source/packaging rechecks are recorded in bk4 receipts. A copy outside the assigned worktree establishes preservation there, not current Git custody. Directory symlinks were not followed during name traversal; referents were encountered physically where present, but aliases may be absent.
- **Triage/C scope:** Every top-level folder is covered by census; root, llm-as-database, stale archive, both Drive folders, src and the empty arhugula-vm-data were considered. Bulk unrelated/dependency data was not semantically read per-file. Caselaw was names/metadata only, not hashed or read. BK3C's group coverage is complete for its original adjacent cohort; actual use by this program of all third-party clone members is unproven. Its match triage remains 49 EXACT-index candidates / 1,167 SAME-NAME / 8,813 CONTENT-PENDING before overrides, not final per-file uniqueness. Moving six proven EXACT referrals and adding four contextual files does not turn group review into content/rename adjudication of 10,027 files.
- **Truth boundary:** Embedded dates, status/verdict fields and exported citations describe historical artifacts. No experiment, calibration, external URL/paper result, embedded code or archival claim was independently reproduced by this audit. File mtime was used only as inventory metadata, never chronology proof. No “all duplicates,” “nothing lost,” scientific PASS or current native/host acceptance is implied.

## Packaging and acceptance receipts

`inventory.tsv` remains in place and is explicitly **excluded from MAESTRO's committed set**: **157,756,604 bytes**, SHA-256 **`5bf9ac37fe26bd62477f4ec7d32a0cf4cbbb2fd8427f039741b98b6762f4af4f`**. BK3 produced `inventory.tsv.gz` with `gzip -9 -k` and verified decompressed SHA equality to the original. Its size is **37,526,654 bytes**. BK4 reruns `gzip -t` and checks the unchanged compressed/original hashes; no regeneration is needed.

All audit-folder files other than the intentionally excluded raw inventory are the proposed committed set. A final explicit file manifest and independent receipts in [bk4_commit_manifest.tsv](bk4_commit_manifest.tsv) and [bk4_verification.json](bk4_verification.json) verify every file **≤45,000,000 bytes**, total **≤200,000,000 bytes**, report/gap row reconciliation, protected BK3C bytes, raw/gzip hashes, source hashes and loss-citation text. Finalization is complete only if those receipts report PASS. The raw folder is larger than 200 MB because the operator explicitly required retaining the noncommitted raw TSV alongside its compressed committed copy.

The binding context directive remains: start a new step only at ≥60% context; at ≤40% or any compaction stop starting work, append a complete successor handoff to progress.md, and reply with the assigned HANDOFF token. A completed audit leaves an audit-folder context save and append-only progress closeout so this rule survives.
'''
    (OUT / 'audit_report.md').write_text(report)


if __name__ == '__main__':
    render(*serialize())
