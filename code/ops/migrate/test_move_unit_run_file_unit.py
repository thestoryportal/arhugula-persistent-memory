"""move_unit run on file units, end to end (T215 A3 seam, ticket T363).

Each unit's root is one regular file: unit_manifest and record_split inventory it, move_unit plans it, and run
moves it with fdsafe.rename, stages it, and writes custody that icm21_check moves (post) and stage_check accept.
A file unit holds no folder of its own, so its roots are its parent folders only.
"""
from __future__ import annotations

import os
import errno
import json

import fault_kit as FK
import shutil
import tempfile
import unittest
from unittest import mock

from ops.migrate import fdsafe, move_unit
from test_move_unit_run import Base, Fixture, Unit, git

TRACKED = b'{"model": 1}\n'
LOG = b"step 1 loss 0.5\n"


class FileFixture(Fixture):
    """M with two file units: a tracked JSON file inside M that stays in M, and an untracked log outside M
    that enters M."""

    def __init__(self, base: str):
        self.base = os.path.realpath(tempfile.mkdtemp(prefix="fx", dir=base))
        self.m = self.mk("m")
        git(self.m, "init", "-q", "--template=", "-b", "master")
        self.put("m/README.md", b"readme\n")
        self.put("m/experiments/c10r/README.md", b"c10r\n")
        self.custody = self.mk("m/program/migrations/icm21/units/S220")
        self.decoy = self.mk("decoy")
        self.put("decoy/a.json", b'{"decoy": true}\n')
        self.gen = 0
        self.units = [Unit("model.json", "MV-101", f"{self.m}/old/model.json", f"{self.m}/kept/model.json",
                           {"": TRACKED}, tracked=("",)),
                      Unit("run.log", "MV-102", f"{self.base}/p/run.log", f"{self.m}/kept/run.log", {"": LOG})]
        for unit in self.units:
            self.put(unit.source, unit.files[""])
        git(self.m, "add", "--", "README.md", "experiments/c10r/README.md", "old/model.json")
        git(self.m, "commit", "-q", "-m", "fixture")
        self.seal()


class FileUnitRun(Base):
    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp(prefix="moverun"))
        self.addCleanup(shutil.rmtree, self.tmp)
        self.fx = FileFixture(self.tmp)
        self.model, self.log = self.fx.units

    def test_file_units_move_and_both_checks_pass(self):
        self.assertEqual([m["kind"] for m in self.fx.plan_doc["moves"]], ["file", "file"])
        result = self.run_ok()
        self.assertEqual([(a["action"], a["source"], a["target"]) for a in result["actions"]], [
            ("mkdir", None, f"{self.fx.m}/kept"),
            ("git-mv", self.model.source, self.model.vtarget),
            ("mv", self.log.source, self.log.vtarget),
            ("git-add", None, self.log.vtarget)])
        for unit, data in ((self.model, TRACKED), (self.log, LOG)):
            self.assertFalse(os.path.lexists(unit.source))
            with open(unit.vtarget, "rb") as fh:
                self.assertEqual(fh.read(), data)
        with open(os.path.join(self.fx.custody, "admitted.tsv"), "rb") as fh:
            self.assertEqual(fh.read(), b"R100\told/model.json\tkept/model.json\nA\tkept/run.log\n")
        check = self.fx.moves_check()
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        staged = self.fx.stage_check()
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)

    def test_file_inventory_has_no_folder_and_closes_its_fd(self):
        before = sorted(os.listdir("/dev/fd"))
        manifest, identity, folders = move_unit._inventory(self.log.source)
        self.assertEqual(folders, ())
        self.assertEqual(sorted(os.listdir("/dev/fd")), before)
        st = os.lstat(self.log.source)
        self.assertEqual(identity, (st.st_dev, st.st_ino))
        with open(self.fx.inp + "/manifest-run.log.json", "rb") as fh:
            self.assertEqual(json.loads(manifest), json.load(fh))

    def test_file_unit_changed_after_the_plan_is_not_moved(self):
        self.fx.rewrite(self.model.source, b'{"model": 2}\n')
        self.refuses_unmoved(self.model.source, "changed pre-digest")

    def test_file_unit_swapped_for_a_link_is_not_followed(self):
        os.rename(self.log.source, os.path.join(self.fx.base, "parked.log"))
        os.symlink(f"{self.fx.decoy}/a.json", self.log.source)
        self.refuses_unmoved(self.log.source, "[ELOOP]")

    def test_file_unit_replaced_after_its_inventory_is_not_moved(self):
        real, fired = os.mkdir, []

        def swap_after(path, *args, **kwargs):
            result = real(path, *args, **kwargs)
            if path == "kept" and not fired:
                fired.append(True)
                os.rename(self.log.source, os.path.join(self.fx.base, "parked.log"))
                with open(self.log.source, "xb") as fh:
                    fh.write(LOG)
            return result
        # [LAW:behavior-not-structure] Race a real filesystem effect after inventory, not the inventory itself.
        with mock.patch.object(os, "mkdir", swap_after):
            result = self.main(*self.fx.args())
        self.assertEqual(fired, [True])
        self.assert_refused(result, self.log.source, "inventoried as the unit source")
        self.assertFalse(os.path.lexists(self.log.vtarget))

    def test_fifo_raced_into_file_open_refuses_without_blocking(self):
        before = sorted(os.listdir("/dev/fd"))
        # [LAW:verifiable-goals] A missing nonblocking flag must fail at a bounded deadline.
        with FK.fifo_in_place(self.log.source, name="open", timeout=5.0,
                              match=lambda path, *a, **kw: path == self.log.source) as fault:
            result = self.main(*self.fx.args())
        self.assertEqual(fault.fired, 1)
        self.assert_refused(result, self.log.source, "neither a directory nor a regular file")
        self.assert_unmoved()
        self.assertEqual(sorted(os.listdir("/dev/fd")), before)

    def test_file_replaced_after_open_is_refused(self):
        before = sorted(os.listdir("/dev/fd"))
        real, fired = os.open, []

        def opened(path, *args, **kwargs):
            fd = real(path, *args, **kwargs)
            if path == self.log.source and not fired:
                fired.append(True)
                os.rename(path, path + ".parked")
                with open(path, "xb") as fh:
                    fh.write(LOG)
            return fd
        with mock.patch.object(os, "open", opened):
            result = self.main(*self.fx.args())
        self.assertEqual(fired, [True])
        self.assert_refused(result, self.log.source, "root path")
        self.assert_unmoved()
        self.assertEqual(sorted(os.listdir("/dev/fd")), before)

    def test_file_close_error_is_not_suppressed(self):
        real, opened = os.open, []

        def opening(path, *args, **kwargs):
            fd = real(path, *args, **kwargs)
            if path == self.log.source:
                opened.append(fd)
            return fd
        before = sorted(os.listdir("/dev/fd"))
        with mock.patch.object(os, "open", opening), FK.inject_oserror(
                "close", 1, errno.EIO, match=lambda fd: fd in opened) as fault:
            result = self.main(*self.fx.args())
        self.assertEqual(fault.fired, 1)
        self.assert_refused(result, self.log.source, "[EIO]")
        self.assert_unmoved()
        self.assertEqual(sorted(os.listdir("/dev/fd")), before)

    def test_source_lstat_error_names_the_source_and_errno(self):
        real, fired = os.lstat, []

        def lstat(path, *args, **kwargs):
            if path == self.log.source:
                fired.append(True)
                raise OSError(errno.EIO, os.strerror(errno.EIO))
            return real(path, *args, **kwargs)
        with mock.patch.object(os, "lstat", lstat):
            result = self.main(*self.fx.args())
        self.assertEqual(fired, [True])
        self.assert_refused(result, self.log.source, "[EIO]")
        self.assert_unmoved()


if __name__ == "__main__":
    unittest.main()
