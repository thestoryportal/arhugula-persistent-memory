"""Step 427 growth rules; host paths are inert registry operands only."""
import csv
from dataclasses import astuple, replace
from pathlib import Path
import re
import tempfile
import unittest

from ops.migrate.root_readers_core import Check, Install, Record, Replace, parse_registry

REGISTRY = Path(__file__).parents[3] / "program/migrations/icm21/root-readers.tsv"
H = "/Users/robertrhu"
MK = "-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory"
RK = "-Volumes-memit-arhugula-persistent-memory"
PROJECTS = H + "/.claude/projects/"
UUID = r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}"

# [LAW:one-source-of-truth] Both registry suites use these same growth patterns.
GROWTH = (
    ("transcript", re.compile(re.escape(PROJECTS) + "(?:" + re.escape(MK)
     + "|" + re.escape(RK) + ")/" + UUID + r"(?:\.jsonl)?"),
     "Outside-M row 30: frozen evidence operand; keeps original paths"),
    ("settings-bak", re.compile(re.escape(H + "/.claude/settings.json.bak") + r"[^/]*"),
     "restore source only; a restore after the switch brings M back"),
    ("codex-sqlite", re.compile(re.escape(H + "/.codex/") + r"[^/]+\.sqlite(?:-wal|-shm)?"),
     "Outside-M inventory: historical record; no live reader"),
    ("bytecode", re.compile(r"(?:[^/]+/)*__pycache__"),
     "Inside-M U2: __pycache__ bytecode; co_filename text only; regenerated"),
)
LANE_REASON = ("Outside-M row 53: merged-lane residue; its .venv link text names M "
               "and dangles after the switch; no reader runs this lane")
STATIC = (
    Record("/Volumes/memit/llmdb-lanes/T088/.venv", LANE_REASON),
    Record("/Volumes/memit/llmdb-lanes/T090/.venv", LANE_REASON),
    Record(H + "/.zsh_history", "Home-level shell history; history only"),
)


def is_growth(row):
    return isinstance(row, Record) and any(pattern.fullmatch(row.prefix)
                                          for _, pattern, _ in GROWTH)


class RegistryGrowth(unittest.TestCase):
    def setUp(self):
        self.rows = parse_registry(REGISTRY.read_text(encoding="utf-8"))

    def assert_reasons(self, rows):
        for row in (r for r in rows if isinstance(r, Record)):
            for name, pattern, reason in GROWTH:
                if pattern.fullmatch(row.prefix):
                    self.assertEqual(row.reason, reason, f"{name} reason: {row.prefix}")

    def assert_twins(self, rows):
        pattern = GROWTH[0][1]
        prefixes = {r.prefix for r in rows if isinstance(r, Record)
                    and pattern.fullmatch(r.prefix)}
        m_entries = {p.removeprefix(PROJECTS + MK + "/") for p in prefixes
                     if p.startswith(PROJECTS + MK + "/")}
        r_entries = {p.removeprefix(PROJECTS + RK + "/") for p in prefixes
                     if p.startswith(PROJECTS + RK + "/")}
        self.assertEqual(m_entries, r_entries, "transcript twin missing")

    def assert_no_live_coverage(self, rows):
        targets = [r.path for r in rows if isinstance(r, (Replace, Check))]
        targets += [r.dst for r in rows if isinstance(r, Install)]
        # W12(a): a broadened parent operand must not hide a live reader either.
        for row in (r for r in rows if isinstance(r, Record)):
            for target in targets:
                self.assertFalse(target == row.prefix or target.startswith(row.prefix + "/"),
                                 f"live coverage: {row.prefix} covers {target}")

    def assert_static(self, rows):
        for row in STATIC:
            self.assertTrue(row in rows, f"static row missing: {row.prefix}")

    def assert_console(self, rows):
        self.assertEqual([r for r in rows if isinstance(r, Check)
                          and r.check_id == "console-version"],
                         [Check(".venv/bin/tqdm", "console-version")], "console-version")

    def mutated_copy(self, rows):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        path = Path(scratch.name) / "registry.tsv"
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
            for row in rows:
                writer.writerow((row.kind, *astuple(row)[:-1]))
        return parse_registry(path.read_text(encoding="utf-8"))

    def test_growth_reasons(self):
        self.assert_reasons(self.rows)

    def test_transcript_twins(self):
        self.assert_twins(self.rows)

    def test_no_live_coverage(self):
        self.assert_no_live_coverage(self.rows)

    def test_static_rows(self):
        self.assert_static(self.rows)

    def test_console_version(self):
        self.assert_console(self.rows)

    def test_reason_mutants(self):
        for name, pattern, _ in GROWTH:
            with self.subTest(growth=name):
                victim = next(r for r in self.rows if isinstance(r, Record)
                              and pattern.fullmatch(r.prefix))
                rows = self.mutated_copy([replace(r, reason="wrong reason") if r == victim
                                          else r for r in self.rows])
                with self.assertRaisesRegex(AssertionError, "reason:"):
                    self.assert_reasons(rows)

    def test_twin_mutants(self):
        for key in (MK, RK):
            with self.subTest(project=key):
                victim = next(r for r in self.rows if isinstance(r, Record)
                              and GROWTH[0][1].fullmatch(r.prefix)
                              and r.prefix.startswith(PROJECTS + key + "/"))
                rows = self.mutated_copy([r for r in self.rows if r != victim])
                with self.assertRaisesRegex(AssertionError, "transcript twin missing"):
                    self.assert_twins(rows)

    def test_live_coverage_mutants(self):
        for kind, target in ((Replace, "path"), (Install, "dst"), (Check, "path")):
            live = next(r for r in self.rows if isinstance(r, kind))
            path = getattr(live, target)
            for operand in (path, str(Path(path).parent)):
                with self.subTest(kind=kind.__name__, operand=operand):
                    rows = self.mutated_copy((*self.rows, Record(operand, GROWTH[3][2])))
                    with self.assertRaisesRegex(AssertionError, "live coverage:"):
                        self.assert_no_live_coverage(rows)

    def test_static_mutants(self):
        for victim in STATIC:
            with self.subTest(operand=victim.prefix):
                self.assertTrue(victim in self.rows, f"static row missing: {victim.prefix}")
                rows = self.mutated_copy([r for r in self.rows if r != victim])
                with self.assertRaisesRegex(AssertionError, "static row missing:"):
                    self.assert_static(rows)

    def test_console_mutant(self):
        rows = self.mutated_copy([Check(".venv/bin/hf", "console-version")
                                  if isinstance(r, Check) and r.check_id == "console-version"
                                  else r for r in self.rows])
        with self.assertRaisesRegex(AssertionError, "console-version"):
            self.assert_console(rows)

    def test_growth_pattern_boundaries(self):
        uuid = "01234567-89ab-cdef-0123-456789abcdef"
        positives = (PROJECTS + MK + "/" + uuid, PROJECTS + RK + "/" + uuid + ".jsonl",
                     H + "/.claude/settings.json.bak", H + "/.claude/settings.json.bak-new",
                     H + "/.codex/future.sqlite", H + "/.codex/future.sqlite-wal",
                     H + "/.codex/future.sqlite-shm", "__pycache__", "code/new/__pycache__")
        negatives = (PROJECTS + MK + "/memory", PROJECTS + MK + "/" + uuid + "/child",
                     PROJECTS + RK + "/not-a-uuid.jsonl", H + "/.claude/settings.json",
                     H + "/.claude/settings.json.bak/child", H + "/.codex/sub/future.sqlite",
                     H + "/.codex/future.sqlite-journal", "/code/__pycache__",
                     "code/__pycache__/file.pyc", "code/__pycache__suffix")
        for path in positives:
            self.assertTrue(is_growth(Record(path)), path)
        for path in negatives:
            self.assertFalse(is_growth(Record(path)), path)


if __name__ == "__main__":
    unittest.main()
