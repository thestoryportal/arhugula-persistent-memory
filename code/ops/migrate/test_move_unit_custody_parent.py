"""move_unit run writes custody files below a folder that holds a unit source (Step 368, ruling R2).

A folder that holds a unit source guards the rename of that unit; it does not stop a custody file below it. The
custody folder must still be outside every unit folder, every target and every folder the run creates.
"""
from __future__ import annotations

import os
import shutil
import tempfile
import unittest
from unittest import mock

from ops.migrate.test_move_unit_run import CUSTODY, Base, Fixture, Unit, git

LOG = b"step 1 loss 0.5\n"
NOTES = b"notes\n"


def folder_unit(p: str, m: str) -> Unit:
    return Unit("u", "MV-101", f"{p}/u", f"{m}/kept/u", {"run.log": LOG, "notes.txt": NOTES})


def file_unit(p: str, m: str) -> Unit:
    return Unit("run.log", "MV-101", f"{p}/run.log", f"{m}/kept/run.log", {"": LOG})


class AboveFixture(Fixture):
    """P (the fixture base) holds M and one unit source below P, which enters M below M/kept. The custody folder
    is M/program/migrations/icm21/units/S220, so it lies below the unit's source parent P."""

    def __init__(self, base: str, kept: bool = False, unit=folder_unit):
        self.base = os.path.realpath(tempfile.mkdtemp(prefix="fx", dir=base))
        self.m = self.mk("m")
        git(self.m, "init", "-q", "--template=", "-b", "master")
        self.put("m/README.md", b"readme\n")
        self.put("m/experiments/c10r/README.md", b"c10r\n")
        self.custody = self.mk("m/program/migrations/icm21/units/S220")
        self.decoy = self.mk("decoy")
        self.put("decoy/a.json", b'{"decoy": true}\n')
        self.gen = 0
        self.units = [unit(self.base, self.m)]
        for rel, data in self.units[0].files.items():
            self.put(os.path.normpath(os.path.join(self.units[0].source, rel)), data)
        if kept:
            self.mk("m/kept")
        git(self.m, "add", "--", "README.md", "experiments/c10r/README.md")
        git(self.m, "commit", "-q", "-m", "fixture")
        self.seal()


class CustodyBelowSourceParent(Base):
    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp(prefix="moverun"))
        self.addCleanup(shutil.rmtree, self.tmp)
        self.fx = AboveFixture(self.tmp)
        self.u = self.fx.units[0]

    def test_custody_below_the_source_parent_is_written_and_the_unit_moves(self):
        self.assertTrue(self.fx.custody.startswith(os.path.dirname(self.u.source) + "/"))
        self.assertTrue(self.fx.m.startswith(os.path.dirname(self.u.source) + "/"))
        result = self.run_ok()
        self.assertEqual([(a["action"], a["source"], a["target"]) for a in result["actions"]], [
            ("mkdir", None, f"{self.fx.m}/kept"),
            ("mv", self.u.source, self.u.vtarget),
            ("git-add", None, f"{self.u.vtarget}/notes.txt"),
            ("git-add", None, f"{self.u.vtarget}/run.log")])
        self.assertEqual(result["custody"], [os.path.join(self.fx.custody, name) for name in CUSTODY])
        self.assertEqual(self.fx.custody_files(), sorted(CUSTODY))
        self.assertFalse(os.path.lexists(self.u.source))
        for rel, data in self.u.files.items():
            with open(os.path.join(self.u.vtarget, rel), "rb") as fh:
                self.assertEqual(fh.read(), data)
        check = self.fx.moves_check()
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        staged = self.fx.stage_check()
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)


    def test_a_file_unit_whose_target_parent_is_created_writes_custody_and_moves(self):
        self.fx = AboveFixture(self.tmp, unit=file_unit)
        self.u = self.fx.units[0]
        result = self.run_ok()
        self.assertEqual([(a["action"], a["target"]) for a in result["actions"]], [
            ("mkdir", f"{self.fx.m}/kept"), ("mv", self.u.vtarget), ("git-add", self.u.vtarget)])
        self.assertEqual(self.fx.custody_files(), sorted(CUSTODY))
        self.assertFalse(os.path.lexists(self.u.source))
        with open(self.u.vtarget, "rb") as fh:
            self.assertEqual(fh.read(), LOG)
        staged = self.fx.stage_check()
        self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)


class CustodyStillOutside(Base):
    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp(prefix="moverun"))
        self.addCleanup(shutil.rmtree, self.tmp)
        self.fx = AboveFixture(self.tmp)
        self.u = self.fx.units[0]

    def refuses_unwritten(self, path, *words):
        self.assert_refused(self.main(*self.fx.args()), path, *words)
        self.assert_unmoved()
        self.assert_sources_in_place()

    def test_custody_inside_the_unit_folder_refuses(self):
        self.fx.custody = self.fx.mk("u/custody")
        self.refuses_unwritten("custody_dir", "overlaps")
        self.assertEqual(os.listdir(self.fx.custody), [])

    def test_custody_raced_into_the_unit_folder_refuses(self):
        # [LAW:behavior-not-structure] The core passes the path; a link put on its parent after the core leads
        # the write into the unit folder, and the unit folder's root is what refuses it.
        folder = os.path.dirname(self.fx.custody)
        inside = self.u.source + "/units"
        real, fired = os.open, []

        def then_link(path, *args, **kwargs):
            if path == self.fx.custody and not fired:
                fired.append(True)
                os.rename(folder, inside)
                os.symlink(inside, folder)
            return real(path, *args, **kwargs)
        with mock.patch.object(os, "open", then_link):
            result = self.main(*self.fx.args())
        self.assertEqual(fired, [True])
        self.assert_refused(result, self.fx.custody + "/leaves.json", "inside root", self.u.source)
        self.assertEqual(os.listdir(inside + "/S220"), [])
        self.assertFalse(os.path.lexists(self.fx.target(self.u)))

    def test_custody_inside_an_existing_target_parent_refuses(self):
        self.fx = AboveFixture(self.tmp, kept=True)
        self.fx.custody = self.fx.mk("m/kept/custody")
        self.refuses_unwritten(self.fx.custody + "/leaves.json", "inside root", f"{self.fx.m}/kept")
        self.assertEqual(os.listdir(self.fx.custody), [])

    def test_custody_inside_dot_git_refuses(self):
        self.fx.custody = self.fx.mk("m/.git/custody")
        self.refuses_unwritten(self.fx.custody + "/leaves.json", "inside root", f"{self.fx.m}/.git")
        self.assertEqual(os.listdir(self.fx.custody), [])

    def test_custody_at_or_below_a_folder_the_run_creates_refuses(self):
        for custody, path, word in ((f"{self.fx.m}/kept", "custody_dir", "overlaps"),
                                    (f"{self.fx.m}/kept/custody", f"{self.fx.m}/kept/custody", "[ENOENT]")):
            with self.subTest(custody=custody):
                self.fx.custody = custody
                self.refuses_unwritten(path, word)
                self.assertFalse(os.path.lexists(f"{self.fx.m}/kept"))


class SourceParentGuardsTheRename(Base):
    """The outside-M fixture with its custody folder inside u2's source parent P (beside M)."""
    kind = "outside"

    def test_a_rebound_source_parent_refuses_the_rename_after_custody_below_it(self):
        u2 = self.fx.units[1]
        parent = os.path.dirname(u2.source)
        self.fx.custody = self.fx.mk("p/custody")
        parked = self.fx.base + "/parked-p"
        real, made = os.mkdir, []

        def then_rebind(name, *args, **kwargs):
            result = real(name, *args, **kwargs)
            if name == "p":
                made.append(os.path.dirname(self.fx.target(u2)))
                # The same unit, in a new folder at its source parent's path.
                os.rename(parent, parked)
                os.mkdir(parent)
                os.rename(parked + "/u2", u2.source)
            return result
        with mock.patch.object(os, "mkdir", then_rebind):
            result = self.main(*self.fx.args())
        self.assertIn(os.path.dirname(self.fx.target(u2)), made)
        self.assertEqual(sorted(os.listdir(parked + "/custody")), sorted(CUSTODY))
        self.assert_refused(result, parent, "moved")
        self.assertFalse(os.path.lexists(self.fx.target(u2)))
        self.assertEqual(sorted(os.listdir(u2.source)), sorted(u2.files))
        for rel, data in u2.files.items():
            with open(os.path.join(u2.source, rel), "rb") as fh:
                self.assertEqual(fh.read(), data)


if __name__ == "__main__":
    unittest.main()
