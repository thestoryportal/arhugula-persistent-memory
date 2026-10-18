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
