"""callsite-flag-drop: one flag of a module-level os.O_* constant dropped at one os.open call site.

  callsite-flag-drop  an `os.open` call whose flags argument (args[1], or `flags=` when there is no
                      second positional argument) is a plain NAME gets one mutant per distinct flag X
                      of NAME's chain: the argument becomes `(NAME & ~os.X)`. NAME qualifies when the
                      file binds it exactly once, by `NAME = <chain>` in module scope (the module body
                      and the bodies of its if/try/with/for/while/match statements, not a def, class
                      or lambda), and <chain> is a `|` chain whose every operand is a plain `os.O_*`.

The anchor is the call (its first line), so with --base a changed call site is in scope even when the
constant's line is not, and the ids never meet flag-drop's (anchored at the definition's operands):
`<rel>:<line>:<col>:callsite-flag-drop:<flag>`. Any other binding of NAME in the file (assignment,
augmented or annotated assignment, del, import, def, class, argument, loop or with target, except or
match name, comprehension or walrus target, global or nonlocal) gives no mutant: the name at the call
might not be the chain.
"""
from __future__ import annotations

import ast
import collections

from mutant_ops import _is_bitor, _operands, _os_flag

OP = "callsite-flag-drop"


def _bound(node: ast.AST):
    """The names node binds (or declares global or nonlocal)."""
    if isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load):
        yield node.id
    elif isinstance(node, ast.arg):
        yield node.arg
    elif isinstance(node, ast.alias):
        yield (node.asname or node.name).split(".")[0]
    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.ExceptHandler,
                           ast.MatchAs, ast.MatchStar)):
        yield node.name
    elif isinstance(node, (ast.Global, ast.Nonlocal)):
        yield from node.names
    elif isinstance(node, ast.MatchMapping):
        yield node.rest


def _module_scope(body: list[ast.stmt]):
    for stmt in body:
        yield stmt
        if not isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for inner in ("body", "orelse", "finalbody"):
                yield from _module_scope(getattr(stmt, inner, []))
            for part in getattr(stmt, "handlers", []) + getattr(stmt, "cases", []):
                yield from _module_scope(part.body)


def _chain(value: ast.AST) -> list[str]:
    """The distinct flags of a `|` chain of plain os.O_* attributes, else []."""
    ops = _operands(value) if _is_bitor(value) else []
    if all(isinstance(o, ast.Attribute) and _os_flag(o) for o in ops):
        return list(dict.fromkeys(o.attr for o in ops))
    return []


def _constants(tree: ast.Module) -> dict[str, list[str]]:
    count = collections.Counter(name for node in ast.walk(tree) for name in _bound(node))
    found = {}
    for stmt in _module_scope(tree.body):
        if isinstance(stmt, ast.Assign) and (flags := _chain(stmt.value)):
            for target in stmt.targets:
                if isinstance(target, ast.Name) and count[target.id] == 1:
                    found[target.id] = flags
    return found


def callsite_flag_drop(tree, src, add):
    """One flag of a once-bound module-level os.O_* chain dropped at an os.open call that names it."""
    constants = _constants(tree)
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "open"
                and isinstance(node.func.value, ast.Name) and node.func.value.id == "os"):
            continue
        if node.args and isinstance(node.args[0], ast.Starred):
            continue  # args[1] might not be the second argument
        arg = node.args[1] if len(node.args) > 1 else next((k.value for k in node.keywords if k.arg == "flags"), None)
        if isinstance(arg, ast.Name):
            for flag in constants.get(arg.id, []):
                new = f"({arg.id} & ~os.{flag})"
                add(node, OP, flag, f"{arg.id} -> {new}", *src.span(arg), new.encode("utf-8"))


OPERATORS = (callsite_flag_drop,)
