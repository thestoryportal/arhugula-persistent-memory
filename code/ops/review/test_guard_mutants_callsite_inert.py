"""Step 329: callsite-flag-drop makes no mutant for a flag whose drop cannot change the open.

A flag is inert when `getattr(os, name, None) == 0` in the running interpreter (O_RDONLY here), and
O_NOFOLLOW is inert in a chain that also names O_CREAT and O_EXCL. The chain still qualifies: its other
flags keep their mutants with unchanged ids, changes and source bytes. The suite makes no git call and
creates no file.
"""
from __future__ import annotations

import os
import textwrap
import unittest
from unittest import mock

import guard_mutants as gm
from mutant_ops import callsite_flags

OP = "callsite-flag-drop"


def made(text: str | bytes) -> dict[str, gm.Mutant]:
    data = text.encode("utf-8") if isinstance(text, str) else text
    return {m.id: m for m in gm.parsed(gm.mutants_for("m.py", data, gm.WHOLE, callsite_flags.OPERATORS))}


def rows(text: str | bytes) -> set[tuple[str, str, bytes]]:
    return {(m.id, m.change, m.source) for m in made(text).values()}


class ZeroFlag(unittest.TestCase):
    def test_o_rdonly_is_zero_here(self):
        self.assertEqual(os.O_RDONLY, 0)  # the premise of the next tests on this interpreter

    def test_rdonly_beside_nofollow_gives_only_the_nofollow_mutant(self):
        text = "import os\nF = os.O_RDONLY | os.O_NOFOLLOW\nos.open(p, F)\n"
        self.assertEqual(rows(text), {(f"m.py:3:0:{OP}:O_NOFOLLOW", "F -> (F & ~os.O_NOFOLLOW)",
                                       text.replace("os.open(p, F)", "os.open(p, (F & ~os.O_NOFOLLOW))").encode())})

    def test_a_chain_of_zero_flags_gives_no_mutant(self):
        self.assertEqual(made("import os\nF = os.O_RDONLY | os.O_RDONLY\nos.open(p, F)\n"), {})

    def test_any_flag_that_is_zero_in_the_running_os(self):
        text = "import os\nF = os.O_GMTESTFLAG | os.O_NOFOLLOW\nos.open(p, F)\n"
        both = {f"m.py:3:0:{OP}:O_GMTESTFLAG", f"m.py:3:0:{OP}:O_NOFOLLOW"}
        self.assertFalse(hasattr(os, "O_GMTESTFLAG"))
        self.assertEqual(set(made(text)), both)  # a flag os lacks is not inert
        for value, expected in ((0, {f"m.py:3:0:{OP}:O_NOFOLLOW"}), (1 << 30, both), (None, both)):
            with self.subTest(value=value), mock.patch.object(os, "O_GMTESTFLAG", value, create=True):
                self.assertEqual(set(made(text)), expected)

    def test_rdonly_is_inert_by_value_not_by_name(self):
        text = "import os\nF = os.O_RDONLY | os.O_NOFOLLOW\nos.open(p, F)\n"
        with mock.patch.object(os, "O_RDONLY", 1 << 30):
            self.assertEqual(set(made(text)), {f"m.py:3:0:{OP}:O_RDONLY", f"m.py:3:0:{OP}:O_NOFOLLOW"})


EXCL = "import os\nF = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW\nos.open(p, F, 0o600)\n"


class NofollowBesideCreatExcl(unittest.TestCase):
    def test_no_nofollow_mutant_beside_creat_and_excl(self):
        self.assertEqual(rows(EXCL), {
            (f"m.py:3:0:{OP}:{flag}", f"F -> (F & ~os.{flag})",
             EXCL.replace("os.open(p, F,", f"os.open(p, (F & ~os.{flag}),").encode())
            for flag in ("O_WRONLY", "O_CREAT", "O_EXCL")})

    def test_any_order_of_the_chain(self):
        text = "import os\nF = os.O_NOFOLLOW | os.O_EXCL | os.O_WRONLY | os.O_CREAT\nos.open(p, F)\n"
        self.assertEqual(sorted(made(text)), [f"m.py:3:0:{OP}:{f}" for f in ("O_CREAT", "O_EXCL", "O_WRONLY")])

    def test_nofollow_keeps_its_mutant_without_both(self):
        for gone in ("O_CREAT", "O_EXCL"):
            text = EXCL.replace(f" | os.{gone}", "")
            with self.subTest(without=gone):
                self.assertIn(f"m.py:3:0:{OP}:O_NOFOLLOW", made(text))
        self.assertIn(f"m.py:3:0:{OP}:O_NOFOLLOW", made(EXCL.replace("O_CREAT | os.O_EXCL", "O_TRUNC")))

    def test_the_other_flag_beside_creat_and_excl_keeps_its_mutant(self):
        text = EXCL.replace("O_NOFOLLOW", "O_CLOEXEC")
        self.assertEqual(sorted(made(text)), [f"m.py:3:0:{OP}:{f}" for f in
                                              ("O_CLOEXEC", "O_CREAT", "O_EXCL", "O_WRONLY")])


class OtherFlagsUnchanged(unittest.TestCase):
    def test_both_call_sites_keep_their_live_mutants(self):
        text = textwrap.dedent("""\
            import os

            DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW


            def open_root(root):
                return os.open(root, DIR_FLAGS)


            def open_entry(dir_fd, name):
                fd = os.open(name, DIR_FLAGS, dir_fd=dir_fd)
                return fd
            """)
        want = set()
        for line, col, call in ((7, 11, "os.open(root, DIR_FLAGS)"), (11, 9, "os.open(name, DIR_FLAGS,")):
            for flag in ("O_DIRECTORY", "O_NOFOLLOW"):
                new = call.replace("DIR_FLAGS", f"(DIR_FLAGS & ~os.{flag})")
                want.add((f"m.py:{line}:{col}:{OP}:{flag}", f"DIR_FLAGS -> (DIR_FLAGS & ~os.{flag})",
                          text.replace(call, new).encode()))
        self.assertEqual(rows(text), want)

    def test_byte_offsets_with_utf8_and_crlf(self):
        text = 'import os\r\nF = os.O_RDONLY | os.O_NOFOLLOW\r\ns = "éé"; fd = os.open("é", F)\r\n'
        self.assertEqual(rows(text.encode("utf-8")), {
            (f"m.py:3:17:{OP}:O_NOFOLLOW", "F -> (F & ~os.O_NOFOLLOW)",
             text.replace('"é", F)', '"é", (F & ~os.O_NOFOLLOW))').encode("utf-8"))})

    def test_a_repeated_live_flag_gives_one_mutant(self):
        got = made("import os\nF = os.O_NOFOLLOW | os.O_RDONLY | os.O_NOFOLLOW\nos.open(p, F)\n")
        self.assertEqual(sorted(got), [f"m.py:3:0:{OP}:O_NOFOLLOW"])


class Docstring(unittest.TestCase):
    def test_the_module_docstring_states_the_inert_rule(self):
        doc = " ".join(callsite_flags.__doc__.split())
        for phrase in ("getattr(os, name, None) == 0", "O_NOFOLLOW when the chain also has O_CREAT and O_EXCL",
                       "makes no mutant for an inert flag"):
            with self.subTest(phrase):
                self.assertIn(phrase, doc)


if __name__ == "__main__":
    unittest.main()
