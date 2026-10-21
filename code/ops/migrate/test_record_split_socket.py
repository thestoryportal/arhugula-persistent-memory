"""T375: idle sockets are payload; no socket content is opened or attested."""
import hashlib
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ops.migrate import record_split as R


class SocketUnit(unittest.TestCase):
    def setUp(self):
        base = tempfile.mkdtemp(prefix="sk", dir="/tmp")
        self.addCleanup(shutil.rmtree, base)
        self.base = Path(base).resolve()
        self.unit = self.base / "u"
        self.unit.mkdir()
        # Create in reverse path order so the expected document also checks sorting.
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.bind(str(self.unit / "s.sock"))
        (self.unit / "a.txt").write_bytes(b"record\n")

    def document(self):
        try:
            return json.loads(R.render(self.unit, R.split_unit(self.unit, [])))
        except R.Refusal as exc:
            self.fail(f"idle socket unit must split: {exc}")


class SocketSplit(SocketUnit):
    def test_whole_document_has_sorted_file_and_payload_socket(self):
        self.assertEqual(self.document(), {
            "root": str(self.unit), "leaves": [
                {"path": "a.txt", "class": "tracked-record", "kind": "file", "size": 7,
                 "sha256": hashlib.sha256(b"record\n").hexdigest(), "link": None},
                {"path": "s.sock", "class": "governed-payload", "kind": "socket",
                 "size": None, "sha256": None, "link": None}]})

    def test_no_socket_open_with_regular_file_positive_control(self):
        events = []
        active = True

        def audit(event, args):
            if active and event == "open":
                events.append(args[0])

        # [LAW:behavior-not-structure] Observe actual opens; the same scan supplies the live control.
        sys.addaudithook(audit)
        try:
            self.document()
        finally:
            active = False
        names = [os.path.basename(os.fsdecode(p)) for p in events if isinstance(p, (str, bytes))]
        self.assertIn("a.txt", names, events)
        self.assertNotIn("s.sock", names, events)

    def test_fifo_beside_socket_still_refuses(self):
        os.mkfifo(self.unit / "z.pipe")
        with self.assertRaises(R.Refusal) as caught:
            R.split_unit(self.unit, [])
        self.assertEqual(str(caught.exception), "'z.pipe' is a special file")

    def test_socket_inside_nested_git_still_refuses(self):
        inner = self.unit / "inner"
        inner.mkdir()
        subprocess.run(["git", "init", "-q", str(inner)], check=True, capture_output=True,
                       env={**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"})
        (self.unit / "s.sock").rename(inner / ".git/s.sock")
        with self.assertRaises(R.Refusal) as caught:
            R.split_unit(self.unit, [])
        self.assertEqual(str(caught.exception),
                         "'inner/.git/s.sock' inside a nested .git is a link or special file; Git would follow it")

    def test_attested_socket_still_refuses(self):
        att = self.base / "att.json"
        att.write_text(json.dumps({"attested_by": "operator", "regenerate": "make output",
                                   "leaves": [{"path": "s.sock", "sha256": hashlib.sha256(b"").hexdigest()}]}))
        with self.assertRaises(R.Refusal) as caught:
            R.split_unit(self.unit, [att])
        self.assertEqual(str(caught.exception), f"{att}: attested 's.sock' is not a regular file")


if __name__ == "__main__":
    unittest.main()
