#!/usr/bin/env python3
"""Refine seed classification, retaining every inventory row and short reason.
Generic Qwen/RunPod/covariance mentions and C10 hash substrings do not establish program relevance.
Source rows + compact codes in classification_refined.tsv; full candidate paths in candidates_refined.tsv.
"""
import csv,json,re,collections,gzip
from pathlib import Path
OUT=Path(__file__).resolve().parents[1];ROOT=Path('/Volumes/backups')
raw={r['inventory_row']:r for r in csv.DictReader((OUT/'candidates.tsv').open(),delimiter='\t')}
STRONG=re.compile(r'(?i)MEMIT|LARQL|compute_z|LLM.as.Database|AlphaEdit')
TOOLDIRS={'agent-deployment-framework','agent-sdk-workshop','indydevdan-harness-research','meta-harness-architecture-template','layer-05-runtime-operations','soe-skills-all','codex-app-intel-repackager-main','src'}
SCINAME=re.compile(r'(?i)^(architecture-profile|causal_trace|cfb-|cross_architecture|d3_multi_target|deep-research-report|framework_finding|gemma4_editing|grace-patches|llm[-_]|memit|molab_feasibility|organize_llm|probe[-_](set|band)|re_evaluate_bands|reproducibility_manifest|revised_sweep|aggregate_verdict|rome-patches|s212a|s28_v2|session[_-]2|stage_[12]|t[123]_|t_branch|ConnectedPapers)')
TOOLNAME=re.compile(r'(?i)^(0[1-9]-(?!data-layer)|s\d+[-_]|ADR-|Spec_|Implementation_Plan|Project_Workflow|P6-CK|Adversarial_Review|CLAUDE_2|RuFlo|SKILL|agent|aisecops|framework.*skill|.*harness|.*skill|.*workflow|.*orchestrat|.*council|.*framework|.*context.engineer|open-source.*|git-repos-audit|human-workflow|kb-structure|dynamic-workflow|Scaling_170)')
VENDOR=re.compile(r'(^|/)(node_modules|\.git|\.venv|venv|__pycache__|\.next|\.cache|vendor|dist|build)(/|$)')
counts=collections.Counter();pcounts=collections.Counter()
with gzip.open(OUT/'classification_refined.tsv.gz','wt',newline='') as f,(OUT/'candidates_refined.tsv').open('w',newline='') as g:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');v=csv.writer(g,delimiter='\t',lineterminator='\n')
 w.writerow(['inventory_row','class','reason_code']);v.writerow(['inventory_row','path','class','reason_code','signals'])
 for i,r in enumerate(csv.DictReader((OUT/'inventory.tsv').open(),delimiter='\t'),1):
  key=str(i);rel=r['path'];name=Path(rel).name;top=rel.split('/')[0];m=raw.get(key);kind='unrelated';reason='O';signals=m['signals'] if m else ''
  if name=='.DS_Store' or name.startswith('._'):reason='M'
  elif VENDOR.search(rel):reason='V'
  elif top in {'llm-as-database','_archive_stale_pre_s2_5b'}:kind='program';reason='P'
  elif '/' not in rel and SCINAME.search(name):kind='program';reason='N'
  elif m and STRONG.search(signals):kind='program';reason='C'
  elif top in TOOLDIRS:kind='adjacent';reason='T'
  elif '/' not in rel and TOOLNAME.search(name):kind='adjacent';reason='T'
  elif m and m['class']=='program' and top=='seo-growth-engine' and '/skills/' in rel:kind='adjacent';reason='T'
  if name in {'96-7_3-diagnosis-prompt.md','96-7_3-diagnostic-prompt.md','50-mega-prompts.pdf'}:kind='unrelated';reason='O'
  if name=='CLAUDE.md' and '/' not in rel:kind='program';reason='C'
  w.writerow([i,kind,reason]);counts[kind]+=1;pcounts[(top if '/' in rel else '(root)',kind)]+=1
  if kind!='unrelated':v.writerow([i,rel,kind,reason,signals])
(OUT/'classification_state.json').write_text(json.dumps({'counts':dict(counts),'by_top':{'|'.join(k):v for k,v in pcounts.items()},'manual_review':'PENDING; rules are reasoned triage, not final content/gap decisions'},indent=2))
(OUT/'reason_codes.json').write_text(json.dumps({'P':'Dedicated LLM-as-Database research folder or its stale historical archive','N':'Specific program experiment/research/artifact filename; root titles inspected where ambiguous','C':'Specific program content signature (MEMIT/LARQL/compute_z/LLM-as-Database/AlphaEdit); interpretation still requires review','T':'Agent/Claude tooling, harness/skill source or design/research; adjacent to program, actual use not established for all clones','V':'Generated dependency, environment or unrelated checkout git internals','M':'Filesystem metadata','O':'Different project/domain or incidental generic-model/hash reference; no specific program signal'},indent=2))
print(dict(counts))
