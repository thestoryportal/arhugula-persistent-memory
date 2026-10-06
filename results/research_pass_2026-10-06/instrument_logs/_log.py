#!/usr/bin/env python3
"""Append one query record to an instrument log and classify hit ids as seen/new.
Usage: _log.py <instrument> <query> <id1,id2,...> [note]
Seen = any arXiv id in docs/RESEARCH_PASS_CORPUS_INVENTORY_2026-10-06.md or in
results/infranodus_research_arc_2026-10-05/part2/_arxiv_pass_log.json."""
import json, re, sys, datetime, pathlib
root = pathlib.Path(__file__).resolve().parents[3]
logdir = pathlib.Path(__file__).resolve().parent
def seen_set():
    s = set()
    inv = (root/'docs/RESEARCH_PASS_CORPUS_INVENTORY_2026-10-06.md').read_text()
    s |= set(re.findall(r'\b(\d{4}\.\d{4,5})', inv))
    pl = root/'results/infranodus_research_arc_2026-10-05/part2/_arxiv_pass_log.json'
    if pl.exists():
        s |= set(re.findall(r'\b(\d{4}\.\d{4,5})', pl.read_text()))
    return s
SEEN = seen_set()
def main():
    inst, query, ids = sys.argv[1], sys.argv[2], [i for i in sys.argv[3].split(',') if i]
    note = sys.argv[4] if len(sys.argv) > 4 else ''
    f = logdir/f'{inst}.json'
    data = json.loads(f.read_text()) if f.exists() else {'instrument': inst, 'queries': []}
    rec = {'t': datetime.datetime.now().isoformat(timespec='seconds'), 'query': query,
           'hits': [{'id': i, 'status': 'seen' if re.sub(r'v\d+$','',i) in SEEN else 'new'} for i in ids],
           'note': note}
    data['queries'].append(rec)
    f.write_text(json.dumps(data, indent=1))
    print(f"{inst}: {len(ids)} hits, new={sum(h['status']=='new' for h in rec['hits'])}")
if __name__ == '__main__':
    main()
