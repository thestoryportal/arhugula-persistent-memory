#!/usr/bin/env python3
"""Read-only BK2 PROGRAM search; writes only the containing audit folder.

No UNIQUE or chronology verdict is inferred. Search hits are evidence for
semantic review. Large text is processed as bounded lines, never read whole.
ZIP members are inspected only when their uncompressed size <= 200 KiB.
"""
import collections
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import time
import zipfile

OUT = Path(__file__).resolve().parents[1]
REPO = OUT.parents[1]
BACKUP = Path('/Volumes/backups')
MIRROR = Path('/Volumes/memit/llm-database-poc-mirror')
LIMIT = 200 * 1024
TEXT = {'.md', '.txt', '.yaml', '.yml', '.json', '.py', '.bib', '.html', '.bak', '.ipynb', '.rst'}
SKIP = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', '.next', '.cache', 'hf_cache', 'covariance_caches', '.Spotlight-V100', '.Trashes', '.TemporaryItems', '.fseventsd'}


def rows(name):
    with (OUT / name).open(newline='') as f:
        yield from csv.DictReader(f, delimiter='\t')


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(65536), b''):
            h.update(b)
    return h.hexdigest()


def clean(line):
    return re.sub(rb'\s+', b'', line)


def fingerprint(lines):
    digest = hashlib.sha256()
    keys = {}
    headings = []
    n = 1
    continuation = False
    for line in lines:
        norm = clean(line)
        digest.update(norm)
        complete = line.endswith(b'\n') or len(line) < 65536
        if not continuation and complete and 35 <= len(norm) <= 65536:
            key = hashlib.sha256(norm).hexdigest()
            keys.setdefault(key, n)
        if not continuation and len(headings) < 8 and (line.startswith(b'#') or re.search(rb'<title>|<h[123][ >]', line, re.I)):
            headings.append({'line': n, 'text': line.decode('utf-8', 'replace').strip()[:400]})
        n += line.count(b'\n')
        continuation = not complete
    return digest.hexdigest(), keys, headings


def file_fingerprints(path):
    if path.suffix == '.skill':
        with zipfile.ZipFile(path) as z:
            for info in z.infolist():
                if info.is_dir():
                    continue
                if info.file_size > LIMIT:
                    raise ValueError('ZIP member exceeds bounded-read limit: ' + info.filename)
                body = z.read(info)
                if b'\0' not in body[:8192]:
                    yield info.filename, fingerprint(io.BytesIO(body)), info.file_size
    else:
        with path.open('rb') as f:
            probe = f.read(8192)
            if b'\0' in probe:
                return
            f.seek(0)
            # readline(size) bounds even minified single-line JSON/HTML.
            yield '', fingerprint(iter(lambda: f.readline(65536), b'')), path.stat().st_size


def main():
    start = time.time()
    candidates = {r['inventory_row']: r for r in rows('candidates_refined.tsv') if r['class'] == 'program'}
    inventory = {str(i): r for i, r in enumerate(rows('inventory.tsv'), 1) if str(i) in candidates}
    initial = {r['inventory_row']: r for r in rows('matches.tsv') if r['class'] == 'program'}
    blobs = {r['git_blob_id']: r for r in rows('history_blobs.tsv')}
    head_start = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()
    queries = {}
    inverted = collections.defaultdict(set)
    norms = collections.defaultdict(set)
    wanted_sizes = collections.defaultdict(set)
    wanted_sha = collections.defaultdict(set)
    for key, r in inventory.items():
        wanted_sizes[int(r['bytes'])].add(key)
        wanted_sha[r['sha256']].add(key)
        if initial[key]['match'] == 'EXACT':
            continue
        for member, (norm, lines, headings), size in file_fingerprints(BACKUP / r['path']):
            q = key + ('!' + member if member else '')
            queries[q] = {'inventory_row': key, 'member': member, 'normalized_sha256': norm, 'lines': lines, 'headings': headings, 'bytes': size}
            norms[norm].add(q)
            for linehash in lines:
                inverted[linehash].add(q)
    exact_receipts = []
    by_commit = collections.defaultdict(list)
    for key, r in initial.items():
        if r['match'] == 'EXACT':
            by_commit[r['commit']].append((key, r))
    for commit, group in by_commit.items():
        p = subprocess.run(['git', 'ls-tree', '-z', commit, '--'] + [r['repo_or_mirror_path'] for _, r in group], cwd=REPO, capture_output=True, check=True)
        observed = {}
        for record in p.stdout.split(b'\0'):
            if record:
                meta, path = record.split(b'\t', 1)
                observed[path.decode('utf-8', 'surrogateescape')] = meta.split()[2].decode()
        for key, r in group:
            got = observed.get(r['repo_or_mirror_path'])
            if got != inventory[key]['git_blob_id']:
                raise RuntimeError('EXACT receipt failed: ' + inventory[key]['path'])
            exact_receipts.append({'inventory_row': key, 'backup': inventory[key]['path'], 'blob': got, 'commit': commit, 'path': r['repo_or_mirror_path'], 'verified': True})
    with (OUT / 'program_exact_receipts.jsonl').open('w') as f:
        for receipt in exact_receipts:
            f.write(json.dumps(receipt) + '\n')
    hits = collections.defaultdict(list)
    bytehits = collections.defaultdict(list)
    search_counts = collections.Counter()
    errors = []
    def examine(source, member, fp, size, custody, blob=''):
        norm, linekeys, headings = fp
        matches = collections.defaultdict(list)
        for linehash, source_line in linekeys.items():
            for q in inverted.get(linehash, ()):
                matches[q].append((queries[q]['lines'][linehash], source_line))
        for q in norms.get(norm, ()):
            matches.setdefault(q, [])
        for q, pairs in matches.items():
            ratio = len(pairs) / max(1, len(queries[q]['lines']))
            identical = norm == queries[q]['normalized_sha256']
            if not identical and len(pairs) < 2:
                continue
            entry = {'source': source, 'member': member, 'custody': custody, 'blob': blob, 'bytes': size, 'normalized_identical': identical, 'query_line_coverage': round(ratio, 5), 'matched_lines': len(pairs), 'line_pairs': pairs[:20], 'headings': headings}
            hits[q].append(entry)
            hits[q].sort(key=lambda x: (x['normalized_identical'], x['query_line_coverage'], x['matched_lines'], x['custody'] == 'worktree'), reverse=True)
            del hits[q][8:]
    for directory, dirs, files in os.walk(MIRROR, followlinks=False, onerror=lambda e: errors.append(str(e))):
        if Path(directory) == OUT:
            dirs.clear()
            continue
        dirs[:] = [d for d in dirs if d not in SKIP]
        for name in files:
            p = Path(directory) / name
            try:
                if not p.is_file():
                    continue
                size = p.stat().st_size
                search_counts['filesystem_names_seen'] += 1
                custody = 'worktree' if p.is_relative_to(REPO) else 'mirror-outside-worktree'
                if size in wanted_sizes:
                    digest = sha(p)
                    search_counts['size_filtered_files_hashed'] += 1
                    for key in wanted_sha.get(digest, ()):
                        bytehits[key].append({'path': str(p), 'custody': custody, 'sha256': digest})
                if p.suffix.lower() not in TEXT | {'.skill'}:
                    continue
                # Huge numeric data are not research-text documents. Same-size
                # byte search above still covers them; record the text exclusion.
                if p.suffix.lower() in {'.json', '.ipynb'} and size > 2 * 1024 * 1024:
                    search_counts['large_json_text_excluded'] += 1
                    continue
                for member, fp, member_size in file_fingerprints(p):
                    examine(str(p), member, fp, member_size, custody)
                    search_counts['filesystem_text_or_members_searched'] += 1
            except (OSError, zipfile.BadZipFile, ValueError) as e:
                errors.append(str(p) + ': ' + str(e))
        if search_counts['filesystem_names_seen'] and search_counts['filesystem_names_seen'] % 20000 < len(files):
            print(json.dumps(dict(search_counts)), flush=True)
    for oid, r in blobs.items():
        path = r['representative_history_path']
        if int(r['bytes']) > LIMIT or Path(path).suffix.lower() not in TEXT | {'.skill'}:
            search_counts['historical_blob_text_excluded'] += 1
            continue
        p = subprocess.run(['git', 'cat-file', 'blob', oid], cwd=REPO, capture_output=True, check=True)
        if Path(path).suffix == '.skill':
            try:
                with zipfile.ZipFile(io.BytesIO(p.stdout)) as z:
                    for info in z.infolist():
                        if info.is_dir() or info.file_size > LIMIT:
                            continue
                        examine(path, info.filename, fingerprint(io.BytesIO(z.read(info))), info.file_size, 'reachable-history', oid)
            except zipfile.BadZipFile:
                errors.append('Historical invalid ZIP ' + oid)
        elif b'\0' not in p.stdout[:8192]:
            examine(path, '', fingerprint(io.BytesIO(p.stdout)), int(r['bytes']), 'reachable-history', oid)
        search_counts['historical_blobs_searched'] += 1
    with (OUT / 'program_content_evidence.jsonl').open('w') as f:
        for q, query in queries.items():
            entry = {k: v for k, v in query.items() if k != 'lines'}
            entry.update(query=q, backup=inventory[query['inventory_row']]['path'], query_distinct_lines=len(query['lines']), hits=hits[q])
            f.write(json.dumps(entry, ensure_ascii=True) + '\n')
    with (OUT / 'program_byte_copies.jsonl').open('w') as f:
        for key, copies in bytehits.items():
            f.write(json.dumps({'inventory_row': key, 'backup': inventory[key]['path'], 'copies': copies}) + '\n')
    with (OUT / 'program_search_queue.tsv').open('w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['inventory_row', 'backup', 'initial_match', 'search_evidence', 'best_source', 'line_coverage', 'semantic_review'])
        for key, r in inventory.items():
            qhits = [h for q, items in hits.items() if queries[q]['inventory_row'] == key for h in items]
            qhits.sort(key=lambda x: (x['normalized_identical'], x['query_line_coverage']), reverse=True)
            best = qhits[0] if qhits else {}
            if initial[key]['match'] == 'EXACT':
                status = 'EXACT-VERIFIED'
            elif bytehits[key]:
                status = 'FILESYSTEM-BYTE-IDENTICAL'
            elif best.get('normalized_identical'):
                status = 'NORMALIZED-CONTENT-IDENTICAL'
            elif best:
                status = 'CONTENT-RELATED-REVIEW'
            else:
                status = 'SEARCH-NO-MATCH-REVIEW'
            source = bytehits[key][0]['path'] if bytehits[key] else best.get('source', '')
            w.writerow([key, r['path'], initial[key]['match'], status, source, best.get('query_line_coverage', ''), 'PENDING; no UNIQUE/newer judgment'])
    state = {'head_start': head_start, 'head_end': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(), 'program_count': len(inventory), 'exact_receipts': len(exact_receipts), 'queries_including_zip_members': len(queries), 'counts': dict(search_counts), 'errors': errors, 'seconds': round(time.time() - start, 2), 'status': 'search evidence complete; semantic/version review pending', 'limits': 'Directory symlinks not followed; environment/dependency/cache dirs excluded; history text only blobs <=200 KiB; large filesystem JSON >2 MiB not text-indexed; no UNIQUE verdict.'}
    (OUT / 'program_content_state.json').write_text(json.dumps(state, indent=2))
    print(json.dumps(state), flush=True)


if __name__ == '__main__':
    main()
