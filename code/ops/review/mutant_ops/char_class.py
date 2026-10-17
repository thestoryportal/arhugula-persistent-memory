r"""class-drop: one item dropped from a character class of a re.<fn>() literal pattern.

  class-drop  in each literal pattern of a re.<fn>() call (regex-zero's calls and argument rules: fn in
              RE_FUNCS, the pattern is args[0] or the pattern= keyword, a str or bytes constant), each
              [...] class with two or more items gets one mutant per item, with that item removed.

An item is one character, one escape or one range (item-item). An escape is \x and 2 hex digits, \u and 4,
\U and 8, \N{...} (the last three in str patterns only), \ and up to 3 octal digits, or \ and one character.
The ^ right after [ is never an item; a ] right after [ or [^ is one, as is a - first or last in the class.
Outside a class a \ escapes the next character (\[ opens no class). A class that does not end, and anything
after it, gets no mutant. A mutant is kept only when its pattern compiles (re.compile, in the pattern's own
type) and the class there has exactly the other items, with the same negation: [a^b] never becomes [^b],
and a one-item class never becomes [] (its ] would be an item there).
Bytes patterns are read as latin-1. The mutant is anchored at the pattern constant, as regex-zero; its tag
is the dropped item's start offset in the pattern text: M45's [\x00-\x1f\x7f"] gives tags 1, 10 and 14.
"""
from __future__ import annotations

import ast
import re
import warnings

from mutant_ops import RE_FUNCS

WIDTH = {"x": 2, "u": 4, "U": 8}  # hex digits after \x, \u, \U
HEX = frozenset("0123456789abcdefABCDEF")
OCTAL = frozenset("01234567")


def _escape_end(text: str, i: int, wide: bool) -> int:
    """The end of the escape whose backslash is text[i]; past the end when the pattern ends in that backslash."""
    c, n = text[i + 1:i + 2], len(text)
    if c == "x" or (wide and c in ("u", "U")):
        digits, limit = HEX, i + 2 + WIDTH[c]
    elif wide and c == "N" and text[i + 2:i + 3] == "{":
        close = text.find("}", i + 3)
        return n if close < 0 else close + 1
    elif c in OCTAL:
        digits, limit = OCTAL, i + 4
    else:
        return i + 2
    j = i + 2
    while j < min(limit, n) and text[j] in digits:
        j += 1
    return j


def _atom_end(text: str, j: int, wide: bool) -> int:
    return _escape_end(text, j, wide) if text[j] == "\\" else j + 1


def _classes(text: str, wide: bool) -> list[tuple[int, bool, list[tuple[int, int]]]]:
    """(offset of [, negated, [(start, end) of each item]) of each class, up to the first that does not end."""
    found, i, n = [], 0, len(text)
    while i < n:
        if text[i] == "\\":
            i += 2
            continue
        if text[i] != "[":
            i += 1
            continue
        negated = text[i + 1:i + 2] == "^"
        j = first = i + 1 + negated
        items = []
        while j < n and (text[j] != "]" or j == first):
            start, j = j, _atom_end(text, j, wide)
            if text[j:j + 1] == "-" and j + 1 < n and text[j + 1] != "]":
                j = _atom_end(text, j + 1, wide)
            items.append((start, j))
        if j >= n:
            break
        found.append((i, negated, items))
        i = j + 1
    return found


def _compiles(pattern: str | bytes) -> bool:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # a FutureWarning (a possible nested set) is no failure
        try:
            re.compile(pattern)
        except Exception:  # re.error, and OverflowError for a too-large repeat: the pattern does not compile
            return False
    return True


def class_drop(tree, src, add):
    """One item of a [...] class of a re.<fn>() literal pattern dropped."""
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name) and node.func.value.id == "re"
                and node.func.attr in RE_FUNCS):
            continue
        pat = node.args[0] if node.args else next((k.value for k in node.keywords if k.arg == "pattern"), None)
        if not (isinstance(pat, ast.Constant) and isinstance(pat.value, (str, bytes))):
            continue
        wide = isinstance(pat.value, str)
        text = pat.value if wide else pat.value.decode("latin-1")
        for at, negated, items in _classes(text, wide):
            for k, (start, end) in enumerate(items):
                new = text[:start] + text[end:]
                rest = [text[a:b] for m, (a, b) in enumerate(items) if m != k]
                if (at, negated, rest) not in [(o, g, [new[a:b] for a, b in it]) for o, g, it in _classes(new, wide)]:
                    continue
                value = new if wide else new.encode("latin-1")
                if _compiles(value):
                    add(pat, "class-drop", str(start), f"drop {text[start:end]} at {start}",
                        *src.span(pat), repr(value).encode("utf-8"))


OPERATORS = (class_drop,)
