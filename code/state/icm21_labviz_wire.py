"""LabvizMoves wire seam that icm21_check.py loads by file path.

D2 (IMPLEMENTATION_PLAN.md:194-208) replaces only LabvizMoves validation:
each MapInputs value is MapBinding = {path:relpath, sha256:sha} at one fixed
repo-relative path, read beneath the caller's explicit admitted root.
Every other Binding keeps the sealed schema's absolute-path contract.
Failures are ValueError, so wire() records each example as an observed FAIL.
"""
import errno
import hashlib
import os
from pathlib import Path
import re
import stat

ABOUT = 'Derived from sealed path map and approved ICM v2.1 relocations.'
MAP_INPUTS = {'sealed': '_index/path-map.tsv',
              'relocations': '_index/icm21-path-map.tsv'}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def exact_keys(value, keys, what):
    require(type(value) is dict, what + ' is not an object')
    require(set(value) == set(keys), what + ' keys are not exact')


def open_at(parent, name, flags, relative):
    """Open name relative to the parent fd; map a refused component to the input's ValueError."""
    try:
        return os.open(name, flags, dir_fd=parent)
    except OSError as error:
        if error.errno not in (errno.ELOOP, errno.ENOTDIR, errno.ENOENT):
            raise
        # macOS reports O_DIRECTORY|O_NOFOLLOW on a symlink as ENOTDIR; lstat only names
        # the reason, since the open has already refused the component.
        link = flags & os.O_NOFOLLOW and (error.errno == errno.ELOOP or (
            error.errno == errno.ENOTDIR
            and stat.S_ISLNK(os.stat(name, dir_fd=parent, follow_symlinks=False).st_mode)))
        raise ValueError(relative + (': symlink component' if link else ': missing input')) from None


def read_input(root, relative):
    """Read a fixed map input beneath root, refusing any symlink component below root.

    Each component is opened relative to its parent's fd with O_NOFOLLOW, and the bytes
    come from the leaf fd that fstat checked, so a component swapped by name after the
    check is never followed.
    """
    *parents, leaf = Path(relative).parts
    fds = [open_at(None, root, os.O_RDONLY | os.O_DIRECTORY, relative)]
    try:
        for part in parents:
            fds.append(open_at(fds[-1], part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                               relative))
        fds.append(open_at(fds[-1], leaf, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, relative))
        require(stat.S_ISREG(os.fstat(fds[-1]).st_mode), relative + ': missing input')
        with open(fds[-1], 'rb', closefd=False) as handle:
            return handle.read()
    finally:
        for fd in fds:
            os.close(fd)


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
