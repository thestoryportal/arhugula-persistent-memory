"""Resolve exact old paths. Split headings use GitHub-style anchor slugs."""
import argparse
import html
import os
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote

if __package__:
    from .build_index import read_path_map, read_anchor_map
else:
    from build_index import read_path_map, read_anchor_map

# These three split destinations come from phase3/splits.json.
SPLITS = {
    'program/EXPERIMENT_RUNBOOK.md': 'program/runbook',
    'program/SESSION_CHECKPOINT.md': 'program/checkpoints',
    'knowledge/specs/llm-as-database-v1_2-integrated-spec.md':
        'knowledge/specs/integrated-spec-v1_2',
}


def heading_slug(heading: str) -> str:
    text = re.sub(r'^ {0,3}#{1,6}\s+', '', heading).strip()
    text = re.sub(r'\s+#+\s*$', '', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'!?\[([^]]*)\]\([^)]*\)', r'\1', text)
    text = html.unescape(text).lower()
    text = ''.join(c for c in text if c in '-_' or
                   not unicodedata.category(c).startswith(('P', 'S', 'C')))
    return text.replace(' ', '-')


def heading_entries(lines, counts=None):
    if counts is None:
        counts = {}
    fenced = False
    for line in lines:
        if line.lstrip().startswith(('```', '~~~')):
            fenced = not fenced
            continue
        if fenced or not re.match(r'^ {0,3}#{1,6}\s+', line):
            continue
        base = heading_slug(line)
        slug = base
        while slug in counts:
            counts[base] = counts.get(base, 0) + 1
            slug = f'{base}-{counts[base]}'
        counts[slug] = 0
        yield line, slug


def anchors(folder: Path):
    counts = {}
    result = {}
    for part in sorted(folder.glob('[0-9]*.md')):
        for heading, slug in heading_entries(
                part.read_text(encoding='utf-8').splitlines(), counts):
            result[slug] = part.name
    return result


def resolve(old: str) -> str:
    root = Path(os.environ['LLMDB_ROOT'])
    mapping = read_path_map((root / '_index/path-map.tsv').read_bytes())
    path, marker, anchor = old.partition('#')
    if path in SPLITS:
        target = SPLITS[path]
    elif path in mapping:
        target = mapping[path]
        target = SPLITS.get(target, target)
    else:
        raise ValueError(f'Unknown old path: {path}')
    if not target:
        raise ValueError(f'No new path is assigned in _index/path-map.tsv: {path}')
    if target in SPLITS.values() and marker:
        slug = unquote(anchor)
        monolith = next(name for name, folder in SPLITS.items() if folder == target)
        sealed = read_anchor_map((root / '_index/anchor-map.tsv').read_bytes(), root)
        if (monolith, slug) in sealed:
            return f'{sealed[(monolith, slug)]}#{anchor}'
        parts = anchors(root / target)
        if slug not in parts:
            raise ValueError(f'Unknown anchor for {path}: {anchor}')
        return f'{target}/{parts[slug]}#{anchor}'
    return target + (f'#{anchor}' if marker else '')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('old')
    args = parser.parse_args()
    try:
        print(resolve(args.old))
        return 0
    except (ValueError, OSError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
