"""Resolve exact old paths. Split headings use GitHub-style anchor slugs."""
import argparse
from collections import Counter
import csv
import html
from html.parser import HTMLParser
import io
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
from urllib.parse import unquote

from markdown_it import MarkdownIt

# These three split destinations come from phase3/splits.json.
SPLITS = {
    'program/EXPERIMENT_RUNBOOK.md': 'program/runbook',
    'program/SESSION_CHECKPOINT.md': 'program/checkpoints',
    'knowledge/specs/llm-as-database-v1_2-integrated-spec.md':
        'knowledge/specs/integrated-spec-v1_2',
}
MAP_HEADER = ['old', 'new', 'disposition', 'unit']
ANCHOR_HEADER = ['monolith', 'anchor', 'part', 'current_anchor']


def read_path_map(data: bytes, minimum: int = 0) -> dict[str, str]:
    if data.splitlines()[:1] != [b'old\tnew\tdisposition\tunit']:
        raise ValueError('_index/path-map.tsv: expected exact header old\tnew\tdisposition\tunit')
    rows = csv.reader(io.StringIO(data.decode('utf-8')), delimiter='\t')
    if next(rows, None) != MAP_HEADER:
        raise ValueError('_index/path-map.tsv: expected header old\tnew\tdisposition\tunit')
    result = {}
    for number, row in enumerate(rows, 2):
        if len(row) != 4 or not row[0]:
            raise ValueError(f'_index/path-map.tsv: malformed row {number}')
        if row[0] in result:
            raise ValueError(f'_index/path-map.tsv: repeated old path {row[0]}')
        result[row[0]] = row[1]
    if len(result) < minimum:
        raise ValueError(f'_index/path-map.tsv: {len(result)} rows; need at least {minimum}')
    return result


def heading_slug(heading: str) -> str:
    text = re.sub(r'^ {0,3}#{1,6}\s+', '', heading).strip()
    text = re.sub(r'\s+#+\s*$', '', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'!?\[([^]]*)\]\([^)]*\)', r'\1', text)
    text = html.unescape(text).lower()
    text = ''.join(c for c in text if c in '-_' or
                   not unicodedata.category(c).startswith(('P', 'S', 'C')))
    return text.replace(' ', '-')


class _InlineText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def _rendered_slug(inline, parser, env):
    text = _InlineText()
    text.feed(parser.renderInline(inline, env))
    return heading_slug('# ' + ''.join(text.parts))


def heading_entries(lines, counts=None):
    if counts is None:
        counts = {}
    parser = MarkdownIt('commonmark')
    env = {}
    tokens = parser.parse('\n'.join(lines), env)
    for index, token in enumerate(tokens):
        if token.type != 'heading_open':
            continue
        level = int(token.tag[1:])
        line = '#' * level + ' ' + tokens[index + 1].content
        base = _rendered_slug(tokens[index + 1].content, parser, env)
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


def read_anchor_map(data: bytes, root: Path) -> dict[tuple[str, str], tuple[str, str]]:
    header = '\t'.join(ANCHOR_HEADER)
    if data.splitlines()[:1] != [header.encode('utf-8')]:
        raise ValueError(f'_index/anchor-map.tsv: expected exact header {header}')
    rows = csv.reader(io.StringIO(data.decode('utf-8')), delimiter='\t')
    next(rows)
    result = {}
    for number, row in enumerate(rows, 2):
        if len(row) != 4 or not all(row):
            raise ValueError(f'_index/anchor-map.tsv: malformed row {number}')
        monolith, anchor, part, current_anchor = row
        key = (monolith, anchor)
        if key in result:
            raise ValueError(f'_index/anchor-map.tsv: repeated anchor {monolith}#{anchor}')
        path = Path(part)
        if path.is_absolute() or '..' in path.parts or not (root / path).is_file():
            raise ValueError(f'_index/anchor-map.tsv: missing or invalid part {part}')
        result[key] = (part, current_anchor)
    return result


def build_anchor_map(root: Path, mapping: dict[str, str]) -> bytes:
    rows = []
    for old, monolith in sorted(mapping.items()):
        if monolith not in SPLITS:
            continue
        folder = SPLITS[monolith]
        parts = sorted((root / folder).glob('[0-9]*.md'))
        source = subprocess.run(['git', 'show', f'3f1a3b95:{old}'], cwd=root,
                                capture_output=True, text=True)
        if source.returncode or not source.stdout:
            raise ValueError(f'_index/anchor-map.tsv: cannot read 3f1a3b95:{old}: '
                             + source.stderr.strip())
        entries = list(heading_entries(source.stdout.splitlines()))
        # All three lossless splits start each part at a level-two heading.
        boundaries = sum(bool(re.match(r'^ {0,3}##\s+', heading))
                         for heading, slug in entries)
        if not parts or boundaries != len(parts):
            raise ValueError(f'_index/anchor-map.tsv: {old}: {boundaries} section '
                             f'boundaries do not match {len(parts)} parts')
        position = -1
        sections = [[] for _ in parts]
        for heading, slug in entries:
            if re.match(r'^ {0,3}##\s+', heading):
                position += 1
            sections[max(position, 0)].append((heading, slug))
        for path, historical in zip(parts, sections):
            part = path.relative_to(root).as_posix()
            pinned = subprocess.run(['git', 'show', f'4e679b15:{part}'], cwd=root,
                                    capture_output=True, text=True)
            if pinned.returncode or not pinned.stdout:
                raise ValueError(f'_index/anchor-map.tsv: cannot read 4e679b15:{part}: '
                                 + pinned.stderr.strip())
            current = list(heading_entries(pinned.stdout.splitlines()))
            if len(historical) != len(current):
                raise ValueError(f'_index/anchor-map.tsv: {part}: heading counts '
                                 f'differ at the pin: {len(historical)} != {len(current)}')
            raw_counts = Counter(heading_slug(heading) for heading, _ in current)
            # Both lists are frozen. Live edits must not change section identity.
            for (heading, slug), (pinned_heading, current_anchor) in zip(historical, current):
                raw_slug = heading_slug(pinned_heading)
                if raw_slug != current_anchor:
                    raise ValueError(f'_index/anchor-map.tsv: {part}: pinned raw slug '
                                     f'{raw_slug} differs from fragment {current_anchor}')
                if raw_counts[raw_slug] > 1:
                    raise ValueError(f'_index/anchor-map.tsv: {part}: pinned raw slug '
                                     f'{raw_slug} occurs more than once')
                level = re.match(r'^ {0,3}(#{1,6})\s+', heading).group(1)
                pinned_level = re.match(r'^ {0,3}(#{1,6})\s+', pinned_heading).group(1)
                if level != pinned_level:
                    raise ValueError(f'_index/anchor-map.tsv: {part}: heading level '
                                     f'differs at the pin for {slug}')
                rows.append((monolith, slug, part, current_anchor))
    data = ('\t'.join(ANCHOR_HEADER) + '\n' + ''.join(
        '\t'.join(row) + '\n' for row in sorted(rows))).encode('utf-8')
    read_anchor_map(data, root)
    return data


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
            part, current_anchor = sealed[(monolith, slug)]
            lines = (root / part).read_text(encoding='utf-8').splitlines()
            parser = MarkdownIt('commonmark')
            env = {}
            parser.parse('\n'.join(lines), env)
            matches = [fragment for heading, fragment in heading_entries(lines)
                if _rendered_slug(re.sub(r'^#{1,6} ', '', heading), parser, env)
                == current_anchor]
            if not matches:
                raise ValueError(f'Unknown anchor for {path}: {anchor}; '
                                 'heading changed after the pin')
            if len(matches) > 1:
                raise ValueError(f'Unknown anchor for {path}: {anchor}; '
                                 f'{len(matches)} live headings match the pinned heading')
            return f'{part}#{matches[0]}'
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
