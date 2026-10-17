"""The tuple-drop operator of guard_mutants.py: one component of a compared tuple is dropped.

  tuple-drop  in a Compare with one operator whose two sides are tuple displays of the same length
              n >= 2, with no starred element, one mutant per index i removes element i from both
              sides (tag: i). n - 1 >= 2 elements stay a tuple; one element left stays a plain
              expression, in parentheses when it is not SIMPLE or spans lines (not a 1-tuple).

The whole Compare is replaced and is the anchor. The comparison operator is the source text between the
two sides, as written, with a space added on a side that has none (`(a,b)in(c,d)` -> `b in d`).
"""
from __future__ import annotations

import ast

from mutant_ops import SIMPLE


def _side(src, elts: list, i: int) -> bytes:
    rest = [e for j, e in enumerate(elts) if j != i]
    if len(rest) > 1:
        return b"(" + b", ".join(src.text(e) for e in rest) + b")"
    text = src.text(rest[0])
    return text if isinstance(rest[0], SIMPLE) and len(text.splitlines()) == 1 else b"(" + text + b")"


def tuple_drop(tree, src, add):
    """Element i dropped from both tuple displays of a one-operator Compare."""
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Compare) and len(node.ops) == 1):
            continue
        left, right = node.left, node.comparators[0]
        if not (isinstance(left, ast.Tuple) and isinstance(right, ast.Tuple)
                and len(left.elts) == len(right.elts) >= 2):
            continue
        if any(isinstance(e, ast.Starred) for e in left.elts + right.elts):
            continue
        op = src.data[src.span(left)[1]:src.span(right)[0]]
        op = (b"" if op[:1].isspace() else b" ") + op + (b"" if op[-1:].isspace() else b" ")
        for i in range(len(left.elts)):
            new = _side(src, left.elts, i) + op + _side(src, right.elts, i)
            add(node, "tuple-drop", str(i), f"drop element {i} of both tuples", *src.span(node), new)


OPERATORS = (tuple_drop,)
