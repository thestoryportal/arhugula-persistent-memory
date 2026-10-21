"""Behavioral checks for caller-controlled descent in fdsafe.walk."""
import errno
import os
import shutil
import stat
import tempfile
import unittest

import fault_kit as FK
from ops.migrate import fdsafe


def named(name):
    def match(first, *args, **kwargs):
        if isinstance(first, int):
            first = os.path.basename(fdsafe.live_path(first, name))
        return first == name
    return match


class Descend(unittest.TestCase):
    def setUp(self):
        self.root = os.path.realpath(tempfile.mkdtemp(prefix="fdsafe-descend-"))
        self.addCleanup(shutil.rmtree, self.root)
        self.b = os.path.join(self.root, "a", "b")
        os.makedirs(self.b)
        for rel in ("a/b/c", "a/leaf", "z"):
            with open(os.path.join(self.root, rel), "wb") as fh:
                fh.write(b"bytes")

    def held(self):
        root = fdsafe.hold_root(self.root)
        self.addCleanup(root.close)
        return root

    def test_bound_never_opens_or_scans_b(self):
        root = self.held()
        for operation in ("open", "scandir"):
            with self.subTest(operation=operation):
                seen = []
                with self.assertRaisesRegex(
                        FK.FaultKitError,
                        rf"^fault_kit: {operation} attack fired 0 times "
                        r"\(0 matched calls, wanted call 1\)$"), \
                        FK.inject_oserror(operation, 1, errno.EIO, match=named("b")) as fault:
                    fdsafe.walk(root, lambda e: seen.append(e.rel),
                                descend=lambda e: "/" not in e.rel)
                self.assertEqual(seen, ["a", "a/b", "a/leaf", "z"])
                self.assertEqual(fault.fired, 0)
                with self.assertRaises(fdsafe.Refusal) as cm, \
                        FK.inject_oserror(operation, 1, errno.EIO, match=named("b")) as control:
                    fdsafe.walk(root, lambda e: None)
                self.assertEqual(control.fired, 1)
                self.assertEqual(cm.exception.errno, errno.EIO)
                self.assertEqual(cm.exception.path, self.b)

    def test_unreadable_directory_can_be_visited_without_entering(self):
        root = self.held()
        os.chmod(self.b, 0)
        try:
            seen = []
            fdsafe.walk(root, lambda e: seen.append(e.rel),
                        descend=lambda e: "/" not in e.rel)
            self.assertEqual(seen, ["a", "a/b", "a/leaf", "z"])
            with self.assertRaises(fdsafe.Refusal) as cm:
                fdsafe.walk(root, lambda e: None)
            self.assertEqual(cm.exception.errno, errno.EACCES)
            self.assertEqual(cm.exception.path, self.b)
        finally:
            os.chmod(self.b, 0o755)

    def test_default_matches_always_true_and_walks_all(self):
        root = self.held()
        default, explicit = [], []
        fdsafe.walk(root, lambda e: default.append(e.rel))
        fdsafe.walk(root, lambda e: explicit.append(e.rel), descend=lambda e: True)
        self.assertEqual(default, explicit)
        self.assertEqual(default, ["a", "a/b", "a/b/c", "a/leaf", "z"])

    def test_descend_once_after_visit_only_for_directories(self):
        calls = []

        def descend(entry):
            self.assertTrue(stat.S_ISDIR(entry.st.st_mode))
            calls.append(("descend", entry.rel))
            return entry.rel == "a"

        fdsafe.walk(self.held(), lambda e: calls.append(("visit", e.rel)), descend=descend)
        self.assertEqual(calls, [
            ("visit", "a"), ("descend", "a"),
            ("visit", "a/b"), ("descend", "a/b"),
            ("visit", "a/leaf"), ("visit", "z"),
        ])

    def test_descend_exception_propagates_unchanged_and_closes_fds(self):
        root = self.held()
        boom = ValueError("boom")
        seen = []

        def descend(entry):
            if entry.rel == "a/b":
                raise boom
            return True

        before = len(os.listdir("/dev/fd"))
        with self.assertRaises(ValueError) as cm:
            fdsafe.walk(root, lambda e: seen.append(e.rel), descend=descend)
        self.assertIs(cm.exception, boom)
        self.assertNotIsInstance(cm.exception, fdsafe.Refusal)
        self.assertEqual(seen, ["a", "a/b"])
        self.assertEqual(len(os.listdir("/dev/fd")), before)


if __name__ == "__main__":
    unittest.main()
