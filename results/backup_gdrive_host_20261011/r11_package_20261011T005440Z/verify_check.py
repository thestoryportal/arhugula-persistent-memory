"""Fail-closed content-check receipt validation; stdlib only."""
import argparse
import json
from pathlib import Path
import re
import sys

def inspect(root):
    root = Path(root)
    result = dict(differing=0, missing=0, errors=0, unchecked=0, incomplete=0)
    reasons = []
    def fault(reason):
        result['incomplete'] += 1
        reasons.append(reason)
    def read(name):
        try:
            text = (root/name).read_text(encoding='utf-8')
            if '\x00' in text or (text and not text.endswith('\n')):
                fault('truncated or non-text '+name)
            return text
        except (OSError, UnicodeError) as exc:
            fault(name+': '+str(exc)); return ''
    if read('exit_code.txt') != '0\n': fault('nonzero or malformed check exit')
    if read('inventory.exit_code.txt') != '0\n': fault('nonzero or malformed inventory exit')
    population = read('inventory.txt').splitlines()
    if not population or len(set(population)) != len(population): fault('empty or duplicate inventory')
    objects = {}
    buckets = {'*':set(), '+':set(), '!':set(), '=':set(), '-':set()}
    for line in read('combined.txt').splitlines():
        if len(line) < 3 or line[0] not in buckets or line[1] != ' ':
            fault('malformed combined entry: '+line); continue
        path = line[2:]
        if path in objects: fault('duplicate combined object: '+path)
        objects[path] = line[0]; buckets[line[0]].add(path)
    for sigil, name, key in (('*','differ.txt','differing'),('+','missing-on-dst.txt','missing'),('!','error.txt','errors')):
        rows = read(name).splitlines()
        if len(rows) != len(set(rows)) or set(rows) != buckets[sigil]: fault('inconsistent '+name)
        result[key] = len(set(rows) | buckets[sigil])
    if set(population) != set(objects): fault('combined report does not cover complete checked inventory')
    if buckets['-']: fault('destination-only entries in one-way report')
    log = read('check.log')
    read('stdout.txt'); stderr = read('stderr.txt')
    summaries = re.findall(r'\b(\d+) differences found\b',log)
    matches = re.findall(r'\b(\d+) matching files\b',log)
    if len(summaries) != 1: fault('missing or ambiguous terminal differences summary')
    elif int(summaries[0]) != result['differing']+result['missing']: fault('difference summary/report mismatch')
    if len(matches) != 1 or int(matches[0]) != len(buckets['=']): fault('matching summary/report mismatch')
    result['unchecked'] = sum(map(int,re.findall(r'\b(\d+) hashes could not be checked\b',log)))
    result['errors'] = max(result['errors'],sum(map(int,re.findall(r'\b(\d+) errors while checking\b',log))))
    severity = r'^(?:\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} )?(?:ERROR|CRITICAL|FATAL)\b'
    if (re.search(severity,log+'\n'+stderr,re.I|re.M) or
            re.search(r'could not check hash|Failed to (?:check|open|read)',log+'\n'+stderr,re.I)):
        result['errors'] = max(1,result['errors'])
    result['pass'] = not any(result.values())
    result['reasons'] = reasons
    result['failed_objects'] = sorted(buckets['*']|buckets['+']|buckets['!'])
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('run',type=Path)
    value = inspect(parser.parse_args().run)
    print(('PASS ' if value['pass'] else 'FAIL ')+json.dumps(value,sort_keys=True))
    sys.exit(0 if value['pass'] else 1)
