#!/usr/bin/env python3
"""Systematic read-only loss search, with bounded lines and explicit scope."""
import collections
import csv
import json
from pathlib import Path
import re
import subprocess

OUT=Path(__file__).resolve().parents[1]
ROOT=OUT.parents[1]
PAT=re.compile(r'\blost\b|wip(?:e|ed|ing)|\bpod\b|runpod|not.recover|missing|balance.laps|decommission',re.I)

def main():
    files=[ROOT/'SESSION_CHECKPOINT.md',ROOT/'EXPERIMENT_RUNBOOK.md',ROOT/'REPRODUCIBILITY.md']
    files += [p for d in ('CORPUS','docs','memory_mirror') for p in (ROOT/d).rglob('*') if p.is_file() and p.suffix.lower() in {'.md','.txt','.json','.yaml','.yml','.rst'}]
    files += [p for p in (ROOT/'results').rglob('*') if p.is_file() and p.name.lower().startswith('readme') and p.suffix.lower() in {'.md','.txt','.rst'} and not p.is_relative_to(OUT)]
    counts=collections.Counter();hits=0;fragments=0
    with (OUT/'loss_evidence_search.tsv').open('w') as out:
        writer=csv.writer(out,delimiter='\t',lineterminator='\n')
        writer.writerow(['path','line','text_json'])
        for p in sorted(set(files)):
            counts[p.relative_to(ROOT).parts[0]]+=1
            with p.open('r',errors='replace') as f:
                n=1
                while True:
                    line=f.readline(65536)
                    if not line:break
                    if PAT.search(line):
                        # JSON escaping preserves tabs/newlines and avoids malformed TSV.
                        writer.writerow([str(p.relative_to(ROOT)),n,json.dumps(line.rstrip('\n'))]);hits+=1
                    if len(line)==65536 and not line.endswith('\n'):fragments+=1
                    n+=line.count('\n')
    state={'scope_files':dict(counts),'files':sum(counts.values()),'matched_lines_or_fragments':hits,'long_line_fragments':fragments,'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'limits':'Working tree snapshot, readable text extensions in requested directories and results README files; all matching lines retained. Generic missing/pod references are leads, not recorded loss verdicts.'}
    (OUT/'loss_evidence_state.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(state))

if __name__=='__main__':main()
