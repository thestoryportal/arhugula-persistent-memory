#!/usr/bin/env python3
"""Serialize BK3's reviewed comparison outcomes for the 58 basename candidates.

This resolves basename comparisons, not final CONTENT/UNIQUE or gap counts.
"""
import csv
import json
from pathlib import Path

OUT=Path(__file__).resolve().parents[1]
ROOT=OUT.parents[1]

def rows(name):
    with (OUT/name).open(newline='') as f:yield from csv.DictReader(f,delimiter='\t')

def main():
    q={r['inventory_row']:r for r in rows('program_search_queue.tsv')}
    copies={}
    for line in (OUT/'program_byte_copies.jsonl').open():
        r=json.loads(line);copies[r['inventory_row']]=r['copies']
    archives={}
    for line in (OUT/'program_archive_comparisons.jsonl').open():
        r=json.loads(line);archives[r['row']]=r
    decisions={
        '52':('OLDER','CLAUDE.md','Pod-era execution anchor; closest historical version has two changed and eight added lines. Current operating model moved to interactive M3 Pro execution. program_pair_diffs.jsonl row 52.'),
        '98':('DIFFERENT-COHORT','stage_1_sect/aggregate_verdict.json','Backup captured 2026-05-01: nine trials. Worktree captured 2026-05-04: Stage 1 v3 fifteen trials. Parsed JSON difference receipt in program_json_diffs.jsonl.'),
        '170':('DIVERGENT-URL-LIST','research_and_specs/llm_research_tools_repos.source_urls.txt','Backup raw URLs vs source list: six removed lines and two added lines. Four URLs lack exact preservation there; two are repository-URL variants. Main same-name file is a rewritten research synthesis. program_pair_diffs.jsonl row 170.'),
        '216':('DIVERGENT-MANIFEST','reproducibility_manifest_merged_s236.json','491 equal leaves, six metadata changes, 181 backup-only leaves under sessions, 896 counterpart-only leaves. Mixed history; do not order whole manifests by authored timestamp. program_pair_diffs.jsonl row 216.'),
        '220':('OLDER','docs/rome-patches-canonical.md','Backup v0.1 first synthesis from S2.17; current v0.2 explicitly absorbs S2.18 empirical findings and supersedes v0.1. program_pair_diffs.jsonl row 220.'),
        '285':('JSON-SEMANTIC-IDENTICAL','/Volumes/memit/llm-database-poc-mirror/stage_2_sweep/stage_2_sweep_verdict.json','Parsed object equality: all 436 leaves equal; formatting differs. Counterpart is outside assigned worktree. program_json_diffs.jsonl.'),
        '295':('OLDER','docs/runbooks/t1_alt_model_3b_memit_akd_runbook_v0_1.md','One-line substantive change: backup requires operator filling placeholders; current artifact set is fully authored. Current counterpart :437; program_pair_diffs.jsonl row 295.'),
        '321':('DIVERGENT-SKILL','skills/aisecops-specialist.skill!aisecops-specialist/SKILL.md','Generic basename initially matched an unrelated code-review skill. Real counterpart is AISecOps role payload: one placeholder line replaced by 55 lines of interface contracts. program_pair_diffs.jsonl row 321.'),
        '406':('DIVERGENT-SKILL','skills/orchestration-comparativist.skill!orchestration-comparativist/SKILL.md','Backup contains 93 additional lines headed Orchestration-Owned Interface Contracts, including IC-HIL-RETURN. No whole-document chronology inferred from this addition. program_pair_diffs.jsonl row 406.'),
        '415':('OLDER-SUBSET','reproducibility_manifest_merged_s236.json','All 338 backup leaves preserved unchanged; worktree adds 1055 leaves. This is a semantic subset, not full-file equality. program_pair_diffs.jsonl row 415.'),
        '17857':('WRONG-SUBJECT-BASENAME','research_and_specs/llm-as-database-v1_2-integrated-spec.md','Backup is an ADF-to-ArhuGula contract handoff learning page, with larql mapping rules at backup :451-452. Initial labviz/index.html basename candidate is unrelated. Final relevance/content disposition still required.')
    }
    output=[]
    for m in rows('matches.tsv'):
        if m['class']!='program' or m['match']!='SAME-NAME':continue
        key=m['inventory_row'];r=q[key];e=r['search_evidence']
        if e=='FILESYSTEM-BYTE-IDENTICAL':
            counterpart=copies[key][0]['path'];outcome='FILESYSTEM-BYTE-IDENTICAL'
            note='Actual SHA256 byte-copy search; all custody/copy locations retained in program_byte_copies.jsonl. No reachable-history identity claimed.'
        elif key in archives:
            a=archives[key];counterpart=a['counterpart']
            if a['logical_members_equal'] and all(x['byte_equal'] for x in a['members']):
                outcome='ARCHIVE-PAYLOAD-IDENTICAL';note='All archive members and logical names compared; identical complete single SKILL.md payload; container bytes differ. program_archive_comparisons.jsonl.'
            else:
                outcome='DIVERGENT-ARCHIVE';note='Every member compared; semantic contracts differ. No whole-archive identity or chronology inferred from container timestamps. Full member diffs in program_archive_comparisons.jsonl.'
        elif e=='NORMALIZED-CONTENT-IDENTICAL':
            outcome='WHITESPACE-CONTENT-IDENTICAL';counterpart=r['best_source'];note='Normalized full text identity in program_content_evidence.jsonl; for role Markdown the counterpart is SKILL.md inside the named archive, not the initial same-name council review.'
        elif key in decisions:
            outcome,counterpart,note=decisions[key]
        else:raise ValueError('Unreviewed basename candidate '+key)
        output.append({'inventory_row':key,'backup':r['backup'],'initial_counterpart':m['repo_or_mirror_path'],'reviewed_comparison':outcome,'actual_counterpart':counterpart,'evidence_and_interpretation':note})
    if len(output)!=58:raise ValueError('Expected exactly 58 comparisons')
    with (OUT/'program_same_name_review.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(output[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(output)
    print(json.dumps({'same_name_rows_reviewed':len(output),'limits':'Comparison outcomes only; final content/rename adjudication and gap recommendations still pending.'}))

if __name__=='__main__':main()
