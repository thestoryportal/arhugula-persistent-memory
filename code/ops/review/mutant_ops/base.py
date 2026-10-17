"""The seven guard operators of guard_mutants.py. Each walks the whole tree and calls add once per mutant."""
from __future__ import annotations

import ast
import os

from mutant_ops import NEVER, RE_FUNCS, SIMPLE, _is_bitor, _operands, _os_flag, _plain_else, _quantifiers, _write_call


def raise_remove(tree, src, add):
    """A `raise` directly in an `if` (or its plain `else`) body becomes `pass`."""
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            for stmt in node.body + _plain_else(node):
                if isinstance(stmt, ast.Raise):
                    add(stmt, "raise-remove", "", "raise -> pass", *src.span(stmt), b"pass")


def negate_if(tree, src, add):
    """An `if` whose body (or plain `else`) has a raise or return gets `not (...)`."""
    for node in ast.walk(tree):
        if isinstance(node, ast.If) and \
                any(isinstance(s, (ast.Raise, ast.Return)) for s in node.body + _plain_else(node)):
            test = src.text(node.test)
            add(node, "negate-if", "", "if X -> if not (X)", *src.span(node.test), b"not (" + test + b")")


def flag_drop(tree, src, add):
    """One os.O_* flag (or getattr(os, "O_*", ...)) dropped from a `|` chain or from `flags |= os.O_*`.

    No mutant for an inert flag, whose drop cannot change the open: (1) a flag with
    getattr(os, name, None) == 0 in the running interpreter (O_RDONLY), in every form above; a flag that os
    lacks is not inert. (2) O_NOFOLLOW in a `|` chain that also names O_CREAT and O_EXCL: open fails EEXIST on
    any symlink there, whatever O_NOFOLLOW says."""
    inner = {id(side) for n in ast.walk(tree) if _is_bitor(n) for side in (n.left, n.right) if _is_bitor(side)}
    for node in ast.walk(tree):
        if not ((_is_bitor(node) and id(node) not in inner) or
                (isinstance(node, ast.AugAssign) and isinstance(node.op, ast.BitOr))):
            continue
        ops = [node.value] if isinstance(node, ast.AugAssign) else _operands(node)
        names = {_os_flag(o) for o in ops}
        for i, operand in enumerate(ops):
            flag = _os_flag(operand)
            if flag is None or _inert(flag, names):
                continue
            rest = [o for j, o in enumerate(ops) if j != i]
            parts = [src.text(o) if isinstance(o, SIMPLE) else b"(" + src.text(o) + b")" for o in rest]
            new = b"(" + b" | ".join(parts) + b")" if parts else b"0"
            target = node.value if isinstance(node, ast.AugAssign) else node
            add(operand, "flag-drop", flag, f"drop {flag}", *src.span(target), new)



def _inert(flag: str, names: set) -> bool:
    """flag_drop's rules (1) and (2); names are the flags of flag's `|` chain (only flag itself for `|=`)."""
    return getattr(os, flag, None) == 0 or (flag == "O_NOFOLLOW" and {"O_CREAT", "O_EXCL"} <= names)


def regex_zero(tree, src, add):
    """One quantifier of a re.<fn>() literal pattern widened to lower bound 0."""
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name) and node.func.value.id == "re"
                and node.func.attr in RE_FUNCS):
            continue
        pat = node.args[0] if node.args else next((k.value for k in node.keywords if k.arg == "pattern"), None)
        if not (isinstance(pat, ast.Constant) and isinstance(pat.value, (str, bytes))):
            continue
        text = pat.value if isinstance(pat.value, str) else pat.value.decode("latin-1")
        for start, end, repl in _quantifiers(text):
            new = text[:start] + repl + text[end:]
            value = new if isinstance(pat.value, str) else new.encode("latin-1")
            add(pat, "regex-zero", str(start), f"{text[start:end]} -> {repl} at {start}",
                *src.span(pat), repr(value).encode("utf-8"))


def except_class(tree, src, add):
    """An `except` class (or tuple) other than `Exception` becomes `Exception`."""
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is not None \
                and not (isinstance(node.type, ast.Name) and node.type.id == "Exception"):
            add(node, "except-class", "", f"{src.text(node.type).decode()} -> Exception",
                *src.span(node.type), b"Exception")


def except_remove(tree, src, add):
    """One `except` clause can never match (NEVER): removal, kept compilable."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.ExceptHandler):
            continue
        if node.type is None:
            at = src.at(node.lineno, node.col_offset) + len("except")
            add(node, "except-remove", "", "bare except never matches", at, at, b" " + NEVER.encode())
        else:
            add(node, "except-remove", "", f"except {src.text(node.type).decode()} never matches",
                *src.span(node.type), NEVER.encode())


def write_loop(tree, src, add):
    """A loop that calls write/pwrite/writev becomes its first such call."""
    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            call = _write_call(node)
            if call is not None:
                add(node, "write-loop", "", "loop -> one call", *src.span(node), src.text(call))


OPERATORS = (raise_remove, negate_if, flag_drop, regex_zero, except_class, except_remove, write_loop)
