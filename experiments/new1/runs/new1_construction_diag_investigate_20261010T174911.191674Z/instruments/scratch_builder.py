import hashlib
from pathlib import Path
from investigation_io import write_bytes, write_json


def build(source, dest, files, replacements, link_venv=True):
    source, dest = Path(source).resolve(), Path(dest).resolve()
    if dest == source or source.is_relative_to(dest): raise RuntimeError('invalid scratch destination')
    dest.mkdir(parents=True, exist_ok=False)
    rows = {}
    for name in sorted(set(files) | set(replacements)):
        origin = Path(replacements.get(name, source/name)).resolve()
        data = origin.read_bytes()
        write_bytes(dest/name, data)
        rows[name] = {'source':str(origin),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
    if link_venv: (dest/'.venv').symlink_to(source/'.venv', target_is_directory=True)
    write_json(dest/'scratch_manifest.json', rows)
    return rows


def guard(modules, tree):
    tree = Path(tree).resolve(); rows = {}
    for module in modules:
        path = Path(module.__file__).resolve()
        if not path.is_relative_to(tree): raise RuntimeError('module resolves outside scratch: '+str(path))
        rows[module.__name__] = {'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    return rows
