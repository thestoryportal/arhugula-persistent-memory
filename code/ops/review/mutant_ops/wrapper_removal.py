"""Two wrapper-removal operators of guard_mutants.py. Each walks the whole tree and calls add once per mutant.

  call-unwrap  the value of an Assign, AnnAssign or Return that is a call to a function defined at module
               level in the same file (a `def` or `async def` directly in the module body, called by its
               plain name), with at least one positional argument, no keywords and no starred argument,
               becomes its arguments: the one argument itself (in parentheses when it is not SIMPLE or
               spans lines), or a tuple of them. Anchor: the Call. Example: `row = make_row(a, b)` ->
               `row = (a, b)`.
  with-null    each item of a `with` statement (not `async with`) whose context expression is a call
               becomes `__import__("contextlib").nullcontext()`; any `as` target stays as written. One
               mutant per item, anchored at its context expression (ast.withitem has no position).
"""
from __future__ import annotations

import ast

from mutant_ops import SIMPLE

NULL = b'__import__("contextlib").nullcontext()'


def _alone(node: ast.AST, src) -> bytes:
    """node's text, in parentheses unless it is SIMPLE and on one line (a bare multi-line piece may not parse)."""
    text = src.text(node)
    return text if isinstance(node, SIMPLE) and node.lineno == node.end_lineno else b"(" + text + b")"


def call_unwrap(tree, src, add):
    """A same-file module-level function call that is an assigned or returned value becomes its arguments."""
    names = {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign, ast.Return)):
            continue
        call = node.value
        if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and call.func.id in names
                and call.args and not call.keywords
                and not any(isinstance(arg, ast.Starred) for arg in call.args)):
            continue
        if len(call.args) == 1:
            new, what = _alone(call.args[0], src), "its argument"
        else:
            new, what = b"(" + b", ".join(_alone(arg, src) for arg in call.args) + b")", "a tuple of its arguments"
        add(call, "call-unwrap", "", f"{call.func.id}(...) -> {what}", *src.span(call), new)


def with_null(tree, src, add):
    """A `with` item whose context expression is a call becomes a nullcontext."""
    for node in ast.walk(tree):
        if isinstance(node, ast.With):
            for item in node.items:
                expr = item.context_expr
                if isinstance(expr, ast.Call):
                    func = " ".join(src.text(expr.func).decode("utf-8").split())
                    add(expr, "with-null", "", f"with {func}(...) -> nullcontext()", *src.span(expr), NULL)


OPERATORS = (call_unwrap, with_null)
