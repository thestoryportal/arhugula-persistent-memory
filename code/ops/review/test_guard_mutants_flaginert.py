"""Step 328: flag-drop (mutant_ops/base.py) makes no mutant for a flag that cannot change the open.

A flag is inert when getattr(os, name, None) == 0 in the running interpreter (O_RDONLY), in a `|` chain, in
`flags |= ...` and in the getattr(os, "O_X", d) form; a flag that os lacks is not inert. In a `|` chain that
also names O_CREAT and O_EXCL, O_NOFOLLOW is inert: open fails EEXIST on any symlink there anyway. Every other
flag-drop mutant keeps its id, change and source bytes. The suite makes no git call and writes no file.
"""
from __future__ import annotations

import os
import unittest
from unittest import mock

import guard_mutants as gm
from mutant_ops import base

OP = "flag-drop"

FIXTURE = b"""\
import os
A = os.O_RDONLY | os.O_NOFOLLOW
B = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
C = getattr(os, "O_RDONLY", 0) | os.O_APPEND
flags |= os.O_RDONLY
flags |= getattr(os, "O_RDONLY", 0)
D = os.O_CREAT | getattr(os, "O_EXCL", 0) | getattr(os, "O_NOFOLLOW", 0)
E = os.O_CREAT | os.O_NOFOLLOW
F = os.O_EXCL | os.O_NOFOLLOW
G = (os.O_CREAT | os.O_EXCL) | f(os.O_NOFOLLOW | os.O_EXCL)
flags |= os.O_NOFOLLOW
H = os.O_GUARD_ABSENT | getattr(os, "O_GUARD_ABSENT", 0)
flags |= os.O_GUARD_ABSENT
"""

# (id, change, the mutated line) of every mutant flag-drop makes on FIXTURE: the tool before Step 328 made
# exactly these plus the six inert ones (2:4 O_RDONLY, 3:43 O_NOFOLLOW, 4:4, 5:9, 6:9 O_RDONLY, 7:44 O_NOFOLLOW).
KEPT = (
    ("f.py:2:18:flag-drop:O_NOFOLLOW", "drop O_NOFOLLOW", b"A = (os.O_RDONLY)"),
    ("f.py:3:4:flag-drop:O_WRONLY", "drop O_WRONLY", b"B = (os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW)"),
    ("f.py:3:18:flag-drop:O_CREAT", "drop O_CREAT", b"B = (os.O_WRONLY | os.O_EXCL | os.O_NOFOLLOW)"),
    ("f.py:3:31:flag-drop:O_EXCL", "drop O_EXCL", b"B = (os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW)"),
    ("f.py:4:33:flag-drop:O_APPEND", "drop O_APPEND", b'C = (getattr(os, "O_RDONLY", 0))'),
    ("f.py:7:4:flag-drop:O_CREAT", "drop O_CREAT",
     b'D = (getattr(os, "O_EXCL", 0) | getattr(os, "O_NOFOLLOW", 0))'),
    ("f.py:7:17:flag-drop:O_EXCL", "drop O_EXCL", b'D = (os.O_CREAT | getattr(os, "O_NOFOLLOW", 0))'),
    ("f.py:8:4:flag-drop:O_CREAT", "drop O_CREAT", b"E = (os.O_NOFOLLOW)"),
    ("f.py:8:17:flag-drop:O_NOFOLLOW", "drop O_NOFOLLOW", b"E = (os.O_CREAT)"),
    ("f.py:9:4:flag-drop:O_EXCL", "drop O_EXCL", b"F = (os.O_NOFOLLOW)"),
    ("f.py:9:16:flag-drop:O_NOFOLLOW", "drop O_NOFOLLOW", b"F = (os.O_EXCL)"),
    ("f.py:10:5:flag-drop:O_CREAT", "drop O_CREAT", b"G = (os.O_EXCL | f(os.O_NOFOLLOW | os.O_EXCL))"),
    ("f.py:10:18:flag-drop:O_EXCL", "drop O_EXCL", b"G = (os.O_CREAT | f(os.O_NOFOLLOW | os.O_EXCL))"),
    ("f.py:10:33:flag-drop:O_NOFOLLOW", "drop O_NOFOLLOW", b"G = (os.O_CREAT | os.O_EXCL) | f((os.O_EXCL))"),
    ("f.py:10:49:flag-drop:O_EXCL", "drop O_EXCL", b"G = (os.O_CREAT | os.O_EXCL) | f((os.O_NOFOLLOW))"),
    ("f.py:11:9:flag-drop:O_NOFOLLOW", "drop O_NOFOLLOW", b"flags |= 0"),
    ("f.py:12:4:flag-drop:O_GUARD_ABSENT", "drop O_GUARD_ABSENT", b'H = (getattr(os, "O_GUARD_ABSENT", 0))'),
    ("f.py:12:24:flag-drop:O_GUARD_ABSENT", "drop O_GUARD_ABSENT", b"H = (os.O_GUARD_ABSENT)"),
    ("f.py:13:9:flag-drop:O_GUARD_ABSENT", "drop O_GUARD_ABSENT", b"flags |= 0"),
)


def made(data: bytes, rel: str = "f.py") -> list:
    """The flag-drop mutants of data, each checked to parse."""
    return gm.parsed(gm.mutants_for(rel, data, gm.WHOLE, (base.flag_drop,)))


def tags(data: bytes) -> list[str]:
    return sorted(m.id.split(":", 4)[4] for m in made(data))


class InertFlags(unittest.TestCase):
    def test_the_fixture_gives_exactly_the_kept_mutants_with_their_bytes(self):
        self.assertFalse(hasattr(os, "O_GUARD_ABSENT"))
        self.assertEqual(os.O_RDONLY, 0)
        got = {m.id: m for m in made(FIXTURE)}
        self.assertEqual(sorted(got), sorted(k[0] for k in KEPT))
        lines = FIXTURE.splitlines(keepends=True)
        for mid, change, line in KEPT:
            with self.subTest(mid=mid):
                m = got[mid]
                at = int(mid.split(":")[1])
                self.assertEqual((m.operator, m.line, m.change), (OP, at, change))
                self.assertEqual(m.source, b"".join(lines[:at - 1]) + line + b"\n" + b"".join(lines[at:]))

    def test_o_rdonly_makes_no_mutant_in_any_form(self):
        for src in (b"A = os.O_RDONLY | os.O_APPEND\n", b'A = getattr(os, "O_RDONLY", 0) | os.O_APPEND\n',
                    b'A = os.O_APPEND | getattr(os, "O_RDONLY")\n'):
            with self.subTest(src=src):
                self.assertEqual(tags(src), ["O_APPEND"])
        for src in (b"flags |= os.O_RDONLY\n", b'flags |= getattr(os, "O_RDONLY", 0)\n',
                    b"A = os.O_RDONLY | os.O_RDONLY\n"):
            with self.subTest(src=src):
                self.assertEqual(tags(src), [])

    def test_inert_means_zero_in_the_running_os_module(self):
        src = b'A = os.O_GUARD_X | os.O_APPEND\nflags |= os.O_GUARD_X\nB = getattr(os, "O_GUARD_X", 0) | os.O_APPEND\n'
        for value, want in ((0, ["O_APPEND", "O_APPEND"]), (1, ["O_APPEND", "O_APPEND"] + ["O_GUARD_X"] * 3),
                            (-1, ["O_APPEND", "O_APPEND"] + ["O_GUARD_X"] * 3)):
            with self.subTest(value=value), mock.patch.object(os, "O_GUARD_X", value, create=True):
                self.assertEqual(tags(src), want)
        with mock.patch.object(os, "O_RDONLY", 4):  # O_RDONLY is inert because it is 0, not by its name
            self.assertEqual(tags(b"A = os.O_RDONLY | os.O_APPEND\n"), ["O_APPEND", "O_RDONLY"])
        with mock.patch.object(os, "O_APPEND", 0):
            self.assertEqual(tags(b"A = os.O_RDONLY | os.O_APPEND | os.O_TRUNC\n"), ["O_TRUNC"])

    def test_a_flag_os_lacks_is_not_inert(self):
        self.assertFalse(hasattr(os, "O_GUARD_ABSENT"))
        src = b'A = os.O_GUARD_ABSENT | getattr(os, "O_GUARD_ABSENT", 0)\nflags |= os.O_GUARD_ABSENT\n'
        self.assertEqual(tags(src), ["O_GUARD_ABSENT"] * 3)
        with mock.patch.object(os, "O_GUARD_NONE", None, create=True):
            self.assertEqual(tags(b"flags |= os.O_GUARD_NONE\n"), ["O_GUARD_NONE"])
        with mock.patch.object(os, "O_GUARD_EMPTY", "", create=True):
            self.assertEqual(tags(b"flags |= os.O_GUARD_EMPTY\n"), ["O_GUARD_EMPTY"])

    def test_o_nofollow_is_inert_only_beside_o_creat_and_o_excl_in_the_same_chain(self):
        cases = (
            (b"A = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW\n", ["O_CREAT", "O_EXCL", "O_WRONLY"]),
            (b"A = os.O_NOFOLLOW | os.O_EXCL | os.O_CREAT\n", ["O_CREAT", "O_EXCL"]),
            (b'A = getattr(os, "O_CREAT", 0) | getattr(os, "O_EXCL") | getattr(os, "O_NOFOLLOW", 0)\n',
             ["O_CREAT", "O_EXCL"]),
            (b"A = (os.O_CREAT | os.O_EXCL) | os.O_NOFOLLOW\n", ["O_CREAT", "O_EXCL"]),
            (b"A = os.O_CREAT | os.O_NOFOLLOW\n", ["O_CREAT", "O_NOFOLLOW"]),
            (b"A = os.O_EXCL | os.O_NOFOLLOW\n", ["O_EXCL", "O_NOFOLLOW"]),
            (b"A = os.O_CREAT | f(os.O_EXCL) | os.O_NOFOLLOW\n", ["O_CREAT", "O_NOFOLLOW"]),
            (b"A = os.O_CREAT | os.O_EXCL | f(os.O_NOFOLLOW | os.O_APPEND)\n",
             ["O_APPEND", "O_CREAT", "O_EXCL", "O_NOFOLLOW"]),
            (b"A = os.O_CREAT | os.O_EXCL | os.O_DIRECTORY\n", ["O_CREAT", "O_DIRECTORY", "O_EXCL"]),
            (b"A = os.O_CREAT | os.O_EXCL\nflags |= os.O_NOFOLLOW\n", ["O_CREAT", "O_EXCL", "O_NOFOLLOW"]),
        )
        for src, want in cases:
            with self.subTest(src=src):
                self.assertEqual(tags(src), want)

    def test_the_t212_lines_give_no_inert_mutant(self):
        src = (b"DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW\n"
               b"CREATE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW\n")
        self.assertEqual(tags(src), ["O_CREAT", "O_DIRECTORY", "O_EXCL", "O_NOFOLLOW", "O_WRONLY"])

    def test_the_docstring_states_both_rules(self):
        doc = " ".join(base.flag_drop.__doc__.split())
        for needle in ("getattr(os, name, None) == 0", "O_RDONLY", "os lacks", "O_CREAT", "O_EXCL", "O_NOFOLLOW"):
            self.assertIn(needle, doc)


if __name__ == "__main__":
    unittest.main()
