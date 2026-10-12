"""Stdlib lane boundary checker. Usage: check_lane.py LANE WORKTREE."""
import ast
import io
import hashlib
import json
import re
import subprocess
import sys
import tokenize
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
STAGING = 'results/context_audit_20261012/hygiene/host_staging'


def git(root, *args):
    result = subprocess.run(['git', '--no-optional-locks', '-C', str(root)] + list(args),
                            capture_output=True)
    if result.returncode:
        raise ValueError(result.stderr.decode('utf-8', errors='replace').strip().replace('\n', ' '))
    return result.stdout


def frontmatter_ok(body):
    lines = body.splitlines()
    if not lines or lines[0] != '---':
        return False
    try:
        end = lines.index('---', 1)
    except ValueError:
        return False
    fields = {}
    seen = set()
    parent = ''
    for index, line in enumerate(lines[1:end], 1):
        match = re.match(r'^(\s*)([\w.]+):\s*(.*?)\s*$', line)
        if not match:
            continue
        indent, key, value = match.groups()
        if not indent:
            parent = key
        qualified = parent + '.' + key if indent else key
        if not indent and key == 'metadata.type':
            continue
        if qualified in ('name', 'description', 'metadata', 'metadata.type'):
            if qualified in seen:
                return False
            seen.add(qualified)
        # Empty/null scalars cannot satisfy a required field.
        value = value.split(' #', 1)[0].strip().strip('\"\'')
        if value in ('|', '>', '|-', '>-', '|+', '>+'):
            following = []
            for entry in lines[index + 1:end]:
                if entry.strip() and len(entry) - len(entry.lstrip()) <= len(indent):
                    break
                following.append(entry.strip())
            value = ' '.join(following).strip()
        if value and value.lower() not in ('null', '~'):
            fields[qualified] = value
        if key == 'metadata' and value.startswith('{'):
            inline = re.search(r'[\"\']?\btype[\"\']?:\s*[\"\']?([\w-]+)', value)
            if inline:
                fields['metadata.type'] = inline.group(1)
    return all(fields.get(key) for key in ('name', 'description', 'metadata.type'))


def body_links(body):
    for match in re.finditer(r'\[\[([^]\n]+)\]\]', body):
        target = match.group(1).split('|', 1)[0].split('#', 1)[0].strip()
        if target:
            yield (target if target.endswith('.md') else target + '.md'), True
    destinations = []
    for match in re.finditer(r'\]\(\s*', body):
        start = match.end()
        if start < len(body) and body[start] == '<':
            end = body.find('>', start + 1)
            if end != -1:
                destinations.append(body[start + 1:end])
            continue
        depth = 0
        index = start
        while index < len(body):
            character = body[index]
            if character == '\\':
                index += 2
                continue
            if character == '(':
                depth += 1
            elif character == ')':
                if depth == 0:
                    break
                depth -= 1
            elif character.isspace() and depth == 0:
                break
            index += 1
        destinations.append(body[start:index])
    # HTML hrefs and reference definitions share relative-path semantics.
    patterns = [r'^\s*\[[^]\n]+\]:\s*(<[^>]+>|\S+)',
                r'href=[\"\']([^\"\']+)[\"\']']
    for pattern in patterns:
        for match in re.finditer(pattern, body, re.MULTILINE):
            destinations.append(match.group(1).strip('<>'))
    for raw in destinations:
        parsed = urlsplit(raw)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        if unquote(parsed.path).endswith('.md'):
            yield unquote(parsed.path), False


def prose(body, suffix):
    if suffix != '.py':
        return body
    # Python fixtures contain deliberately invalid URLs as string inputs, not links
    # in the file's body. Its actual documentation and comments still count.
    parsed = ast.parse(body)
    text = []
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node)
            if doc:
                text.append(doc)
    text += [token.string.lstrip('#').strip() for token in tokenize.generate_tokens(io.StringIO(body).readline)
             if token.type == tokenize.COMMENT]
    return '\n'.join(text)


def inside(path, root):
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def check_lane(lane_id, worktree, plan_path=None):
    failures = []
    root = Path(worktree).resolve()
    try:
        plan = json.loads(Path(plan_path or HERE / 'lanes.json').read_text())
        matches = [lane for lane in plan['lanes'] if lane['id'] == lane_id]
        if len(matches) != 1:
            return ['PLAN unknown or duplicated lane: ' + lane_id]
        lane = matches[0]
        # MAESTRO freezes a dispatch base after incorporating earlier waves.
        dispatch = root / 'results/context_audit_20261012/hygiene/dispatch' / (lane_id + '.json')
        base = lane.get('base_commit')
        receipt = {}
        if lane.get('requires_dispatch') and not dispatch.exists():
            return ['BASE missing frozen dispatch receipt']
        if dispatch.exists():
            frozen = git(root, 'show', 'refs/context_hygiene/dispatch/' + lane_id)
            if frozen != dispatch.read_bytes():
                return ['BASE dispatch differs from MAESTRO-frozen Git blob ref']
            receipt = json.loads(frozen)
            if receipt.get('lane') != lane_id:
                return ['BASE dispatch lane mismatch']
            base = receipt['base_commit']
        if not isinstance(base, str) or not re.fullmatch(r'[0-9a-f]{40}', base):
            return ['BASE missing frozen 40-character commit']
        if Path(git(root, 'rev-parse', '--show-toplevel').decode().strip()).resolve() != root:
            return ['BASE WORKTREE must be repository root']
        git(root, 'cat-file', '-e', base + '^{commit}')
    except (OSError, ValueError, KeyError, TypeError) as error:
        return ['BASE/PLAN ' + str(error).replace('\n', ' ')]

    allowlist = set(lane['allowlist'])
    for path in allowlist:
        pure = PurePosixPath(path)
        if pure.is_absolute() or '..' in pure.parts or any(c in path for c in '*?['):
            failures.append('PLAN invalid exact path: ' + path)
    try:
        changed = set(git(root, 'diff', '--no-renames', '--name-only', '-z', base, '--').decode().split('\0'))
        changed.update(git(root, 'ls-files', '--others', '--exclude-standard', '-z').decode().split('\0'))
        # Ignored new files are also writes; isolated sandboxes must start clean.
        changed.update(git(root, 'ls-files', '--others', '--ignored', '--exclude-standard', '-z').decode().split('\0'))
        changed.discard('')
    except (ValueError, UnicodeError) as error:
        return failures + ['SCOPE cannot inventory diff: ' + str(error).replace('\n', ' ')]
    if dispatch.exists():
        changed.discard(dispatch.relative_to(root).as_posix())
    for path, digest in receipt.get('private_seed_hashes', {}).items():
        if path not in lane.get('private_paths', []):
            failures.append('BASE undeclared private seed: ' + path)
            continue
        seed = root / path
        if not seed.is_file() or seed.is_symlink() or not inside(seed, root):
            failures.append('BASE missing/unsafe private seed: ' + path)
            continue
        if path not in allowlist:
            if hashlib.sha256(seed.read_bytes()).hexdigest() == digest:
                changed.discard(path)
    for path in sorted(changed - allowlist):
        failures.append('SCOPE outside allowlist: ' + path)

    stage = root / STAGING
    for relative in sorted(changed & allowlist):
        path = root / relative
        if path.is_symlink() or not inside(path, root):
            failures.append('SYMLINK unsafe edited path: ' + relative)
            continue
        if not path.exists():
            failures.append('DELETION forbidden: ' + relative)
            continue
        if path.suffix not in ('.md', '.py', '.json', '.toml', '.sh', '.cjs', '.yml', '.yaml') and path.name != 'pre-commit':
            continue
        try:
            body = path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as error:
            failures.append('READ ' + relative + ': ' + str(error).replace('\n', ' '))
            continue
        is_host = lane['kind'] == 'host' and inside(path, stage)
        note = relative.startswith('memory_mirror/') or (is_host and 'memory' in path.relative_to(stage).parts)
        if note and path.name not in ('MEMORY.md', 'SESSION_CHECKPOINT.md') and not frontmatter_ok(body):
            failures.append('FRONTMATTER missing name/description/metadata.type: ' + relative)
        try:
            linked_prose = prose(body, path.suffix)
        except (SyntaxError, tokenize.TokenError) as error:
            failures.append('READ malformed source: ' + relative + ': ' + str(error).replace('\n', ' '))
            continue
        for target, wiki in body_links(linked_prose):
            if target.startswith('/'):
                # Absolute repo/host links are permitted only when resolved in the sandbox.
                host_home = plan.get('host_home', '/Users/robertrhu')
                if is_host and target.startswith(host_home + '/'):
                    candidates = [stage / target[len(host_home) + 1:]]
                else:
                    candidates = [Path(target)]
            else:
                candidates = [path.parent / target]
                if wiki:
                    candidates += [root / target, root / 'memory_mirror' / target]
            if not any(candidate.is_file() and inside(candidate, root) for candidate in candidates):
                failures.append('LINK unresolved ' + relative + ' -> ' + target)

    indexes = [root / 'memory_mirror/MEMORY.md']
    if lane['kind'] == 'host' and stage.exists():
        indexes += list(stage.glob('.claude/projects/*/memory/MEMORY.md'))
    for index in indexes:
        try:
            if index.exists() and index.stat().st_size > 24400:
                failures.append('CAP >24400 bytes: ' + index.relative_to(root).as_posix())
        except OSError as error:
            failures.append('CAP observation failed: ' + str(error).replace('\n', ' '))
    return failures


def main():
    if len(sys.argv) != 3:
        print('USAGE check_lane.py LANE WORKTREE')
        return 2
    try:
        failures = check_lane(sys.argv[1], Path(sys.argv[2]))
    except (OSError, ValueError, KeyError, TypeError) as error:
        failures = ['CHECK ' + str(error).replace('\n', ' ')]
    for failure in failures:
        print(failure)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
