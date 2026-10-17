"""Value-replace operators of guard_mutants.py: a value that a test may never look at.

  value-empty    the value of an Assign, AnnAssign or Return that is a non-empty dict, list, set or
                 tuple display, or a dict, list or set comprehension, becomes the empty value of its
                 kind ({}, [], set(), ()). One mutant per value, anchored at the value.
  codec-lenient  a call X.decode(...) or X.encode(...) with no errors argument (no errors= keyword, no
                 second positional argument, no *args or **mapping) gets errors="replace". One mutant
                 per call, anchored at the call; its argument list is rewritten from the argument texts,
                 so a trailing comma, a comment or a newline before ")" still gives a source that parses.
                 A call inside an f-string gets no mutant: Python 3.11 refuses the f-string's own quote
                 in its expressions, so the inserted text may not parse there.
"""
from __future__ import annotations

import ast

EMPTY = {ast.Dict: ("dict display", b"{}"), ast.DictComp: ("dict comprehension", b"{}"),
         ast.List: ("list display", b"[]"), ast.ListComp: ("list comprehension", b"[]"),
         ast.Set: ("set display", b"set()"), ast.SetComp: ("set comprehension", b"set()"),
         ast.Tuple: ("tuple display", b"()")}
CODECS = frozenset({"decode", "encode"})
LENIENT = b'errors="replace"'


def value_empty(tree, src, add):
    """A non-empty collection display or comprehension assigned or returned becomes the empty value."""
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign, ast.Return)):
            continue
        value = node.value
        kind = EMPTY.get(type(value))
        if kind is None or (isinstance(value, ast.Dict) and not value.keys) \
                or (isinstance(value, (ast.List, ast.Tuple)) and not value.elts):
            continue
        label, empty = kind
        add(value, "value-empty", "", f"{label} -> {empty.decode()}", *src.span(value), empty)


def codec_lenient(tree, src, add):
    """X.decode(...) or X.encode(...) without an errors argument gets errors="replace"."""
    in_fstring = {id(n) for f in ast.walk(tree) if isinstance(f, ast.JoinedStr) for n in ast.walk(f)}
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in CODECS):
            continue
        if id(node) in in_fstring:
            continue
        if len(node.args) > 1 or any(isinstance(a, ast.Starred) for a in node.args) \
                or any(k.arg in ("errors", None) for k in node.keywords):
            continue
        parts = [src.text(p) for p in node.args + node.keywords]  # source order: no *args, so args come first
        a = src.at(node.func.end_lineno, node.func.end_col_offset)
        b = src.at(node.end_lineno, node.end_col_offset)
        add(node, "codec-lenient", "", f'{node.func.attr}(): add {LENIENT.decode()}', a, b,
            b"(" + b", ".join(parts + [LENIENT]) + b")")


OPERATORS = (value_empty, codec_lenient)
