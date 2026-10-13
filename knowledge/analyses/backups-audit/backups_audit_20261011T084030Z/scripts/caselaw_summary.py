#!/usr/bin/env python3
"""Caselaw metadata/name census only. Never opens a data file."""
import os,json,collections
from pathlib import Path
OUT=Path(__file__).resolve().parents[1];ROOT=Path('/Volumes/backups/datasets/caselaw')
rows=[];names=[];errors=[];total=0;size=0
for d,ds,fs in os.walk(ROOT,followlinks=False,onerror=lambda e:errors.append(str(e))):
 count=0;byte=0
 for n in sorted(fs):
  s=os.lstat(Path(d)/n);count+=1;byte+=s.st_size
  if len(names)<30:names.append(str((Path(d)/n).relative_to(ROOT)))
 total+=count;size+=byte;rows.append((str(Path(d).relative_to(ROOT)),count,byte))
text='Caselaw metadata-only census. Counts/bytes are direct files per directory (not recursive totals). No file contents read or hashed.\nTotal files: '+str(total)+'\nTotal bytes: '+str(size)+'\n\nDIRECTORY\tFILES\tBYTES\n'+'\n'.join('\t'.join(map(str,r)) for r in rows)+'\n\nNAME SAMPLE\n'+'\n'.join(names)+'\n\nERRORS\n'+json.dumps(errors)+'\n'
(OUT/'caselaw_summary.txt').write_text(text);print(text[:4000])
