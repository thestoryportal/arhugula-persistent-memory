"""LabvizMoves wire seam that icm21_check.py loads by file path.

D2 (IMPLEMENTATION_PLAN.md:194-208) replaces only LabvizMoves validation:
each MapInputs value is MapBinding = {path:relpath, sha256:sha} at one fixed
repo-relative path, read beneath the caller's explicit admitted root.
Every other Binding keeps the sealed schema's absolute-path contract.
Failures are ValueError, so wire() records each example as an observed FAIL.
"""
import hashlib
from pathlib import Path
import re

ABOUT = 'Derived from sealed path map and approved ICM v2.1 relocations.'
MAP_INPUTS = {'sealed': '_index/path-map.tsv',
              'relocations': '_index/icm21-path-map.tsv'}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def exact_keys(value, keys, what):
    require(type(value) is dict, what + ' is not an object')
    require(set(value) == set(keys), what + ' keys are not exact')


def read_input(root, relative):
    """Read a fixed map input beneath root, refusing any symlink component below root."""
    path = root
    for part in Path(relative).parts:
        path = path / part
        require(not path.is_symlink(), relative + ': symlink component')
    require(path.is_file(), relative + ': missing input')
    return path.read_bytes()


def validate_labviz_moves(value, schema, fixtures, root):
    definitions = schema['$defs']
    require(root is not None, 'LabvizMoves needs an admitted root')
    root = Path(root)
    exact_keys(value, definitions['LabvizMoves']['required'], 'LabvizMoves')
    require(value['about'] == ABOUT, 'LabvizMoves about is not the D2 identity')
    exact_keys(value['derived_from'], definitions['MapInputs']['required'], 'MapInputs')
    for key, binding in value['derived_from'].items():
        exact_keys(binding, ('path', 'sha256'), 'MapBinding')
        path, sha = binding['path'], binding['sha256']
        require(type(path) is str and re.fullmatch(definitions['relpath']['pattern'], path)
                is not None, 'MapBinding path is not a relpath')
        require(path == MAP_INPUTS[key], 'MapBinding path is not ' + MAP_INPUTS[key])
        require(type(sha) is str and re.fullmatch(definitions['sha']['pattern'], sha)
                is not None, 'MapBinding sha256 is not a sha')
        require(hashlib.sha256(read_input(root, path)).hexdigest() == sha,
                path + ': digest mismatch')
    moves = value['moves']
    require(type(moves) is dict and all(type(target) is str and target
                                        for target in moves.values()), 'invalid MoveMap')
