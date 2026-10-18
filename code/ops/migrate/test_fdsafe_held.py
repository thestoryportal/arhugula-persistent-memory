"""Behavioral coverage for the descriptor-transferring create API."""
import errno
import os
import unittest

import fault_kit as FK
from ops.migrate import fdsafe
from test_fdsafe import Base, open_fds


class HeldCreate(Base):
    def create(self, parent, name="report", data=b"report bytes"):
        held = fdsafe.create_held(parent, name, data, [self.held()])
        self.addCleanup(fdsafe.close, held.fd, name)
        return held

    def test_live_path_follows_rename_into_another_directory(self):
        parent = self.held(self.mkdir("out"))
        held = self.create(parent)
        moved = os.path.join(self.mkdir("other"), "renamed")
        os.rename(os.path.join(parent.path, held.name), moved)
        self.assertEqual(fdsafe.live_path(held.fd, held.name), moved)
        self.assertEqual(os.fstat(held.fd).st_ino, os.stat(moved).st_ino)

    def test_short_writes_complete_and_existing_file_is_never_overwritten(self):
        parent = self.held(self.mkdir("out"))
        with FK.one_byte_writes():
            held = self.create(parent, data=b"complete contents")
        path = fdsafe.live_path(held.fd, held.name)
        with open(path, "rb") as stream:
            self.assertEqual(stream.read(), b"complete contents")
        self.refusal(lambda: self.create(parent, data=b"replacement"), errno.EEXIST)
        with open(path, "rb") as stream:
            self.assertEqual(stream.read(), b"complete contents")

    def test_prechecks_match_create_file(self):
        parent, root = self.held(self.mkdir("out")), self.held()
        for name, where, roots in [(n, parent, [root]) for n in ("", ".", "..", "a/b", "a\0b")] + [
                ("report", parent, []), ("report", root, [root])]:
            with self.subTest(name=name, parent=where.path, roots=len(roots)):
                old = self.refusal(lambda: fdsafe.create_file(where, name, b"bytes", roots))
                new = self.refusal(lambda: fdsafe.create_held(where, name, b"bytes", roots))
                self.assertEqual(str(new), str(old))
                self.assertEqual(new.errno, old.errno)
        self.assertEqual(os.listdir(parent.path), [])
        self.assertEqual(os.listdir(root.path), [])

    def test_write_failure_closes_descriptor_and_preserves_refusal(self):
        parent, root = self.held(self.mkdir("out")), self.held()
        before = open_fds()
        with FK.inject_oserror("write", 1, errno.EIO):
            error = self.refusal(lambda: fdsafe.create_held(parent, "report", b"bytes", [root]), errno.EIO)
        self.assertIn("left in place, incomplete", str(error))
        self.assertEqual(open_fds(), before)


if __name__ == "__main__":
    unittest.main()


class OneLineRefusal(unittest.TestCase):
    def test_breaks_escaped_and_other_text_unchanged(self):
        escapes = (("\n", r"\n"), ("\r", r"\r"), ("\v", r"\x0b"), ("\f", r"\x0c"),
                   ("\x1c", r"\x1c"), ("\x1d", r"\x1d"), ("\x1e", r"\x1e"),
                   ("\x85", r"\x85"), ("\u2028", r"\u2028"), ("\u2029", r"\u2029"))
        for char, escaped in escapes:
            with self.subTest(char=repr(char)):
                path = "a" + char + "b"
                error = fdsafe.Refusal(path, "r" + char, errno.EIO)
                self.assertEqual(error.path, path)
                self.assertEqual(str(error), f"{path!r}: r{escaped} [EIO]")
                self.assertEqual(len(str(error).splitlines()), 1)
        for text in ("plain", "back\\slash", "tab\tand\0null", "café"):
            with self.subTest(text=text):
                self.assertEqual(str(fdsafe.Refusal(text, text)), f"{text!r}: {text}")


class HeldOpenWrite(Base):
    def test_empty_open_and_complete_short_writes(self):
        parent, root = self.held(self.mkdir("out")), self.held()
        held = fdsafe.open_held(parent, "report", [root])
        self.addCleanup(fdsafe.close, held.fd, "report")
        self.assertIsInstance(held, fdsafe.Held)
        path = os.path.join(parent.path, "report")
        self.assertEqual(os.stat(path).st_ino, os.fstat(held.fd).st_ino)
        with open(path, "rb") as stream:
            self.assertEqual(stream.read(), b"")
        with FK.one_byte_writes():
            fdsafe.write_held(held, b"complete contents")
        with open(path, "rb") as stream:
            self.assertEqual(stream.read(), b"complete contents")
        self.assertEqual(os.fstat(held.fd).st_size, len(b"complete contents"))

    def test_open_prechecks_match_create_file(self):
        parent, root = self.held(self.mkdir("out")), self.held()
        for name, where, roots in [(n, parent, [root]) for n in ("", ".", "..", "a/b", "a\0b")] + [
                ("report", parent, []), ("report", root, [root])]:
            with self.subTest(name=name, parent=where.path, roots=len(roots)):
                old = self.refusal(lambda: fdsafe.create_file(where, name, b"bytes", roots))
                new = self.refusal(lambda: fdsafe.open_held(where, name, roots))
                self.assertEqual(str(new), str(old))
                self.assertEqual(new.errno, old.errno)
        self.assertEqual(os.listdir(parent.path), [])
        self.assertEqual(os.listdir(root.path), [])

    def test_failed_write_leaves_descriptor_open_for_caller(self):
        parent, root = self.held(self.mkdir("out")), self.held()
        held = fdsafe.open_held(parent, "report", [root])
        self.addCleanup(fdsafe.close, held.fd, "report")
        with FK.inject_oserror("write", 1, errno.EIO):
            error = self.refusal(lambda: fdsafe.write_held(held, b"bytes"), errno.EIO)
        target = os.path.join(parent.path, "report")
        self.assertEqual(str(error), f"{target + ' (left in place, incomplete)'!r}: Input/output error [EIO]")
        self.assertEqual(os.fstat(held.fd).st_size, 0)
        fdsafe.write_held(held, b"retry")
        with open(target, "rb") as stream:
            self.assertEqual(stream.read(), b"retry")
