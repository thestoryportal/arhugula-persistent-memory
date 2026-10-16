"""Step 36: dashboard_tickets_data.snapshot on temporary folders, a temporary git repo and an injected gh runner."""
import calendar
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest
import unittest.mock

from apps.dashboard import dashboard_tickets_data as d

HEADER = "utc\tticket\tevent\trc\tdetail\n"
GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
               GIT_COMMITTER_EMAIL="t@t", GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)


def utc(text):
    return float(calendar.timegm(time.strptime(text, "%Y-%m-%dT%H:%M:%SZ")))


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def ticket(tid, deps=(), **extra):
    data = {"id": tid, "goal": "goal " + tid, "deps": list(deps), "astra": False,
            "write": ["code/" + tid.lower() + ".py"], "test": "true", "out": "none"}
    data.update(extra)
    return json.dumps(data)


def git(repo, *argv):
    subprocess.run(["git", "-C", str(repo), "-c", "core.hooksPath=" + os.devnull] + list(argv),
                   check=True, capture_output=True, env=GIT_ENV)


VERDICT_T001 = """VERDICT: NO-GO

1. **BLOCKING — first defect is real.**
   detail line that is not a finding.

2. **BLOCKING verification gap — second defect.** [x.py:3](x.py:3)

Non-blocking notes:

- **Not blocking: one.**
- two
  continued under two

| Mutant | Change | Killed / survived |
|---|---|---|
| M01 | Delete guard | **Killed** |
| M02 | Delete check | Survived† |
| M03 | Delete other | killed — 3 failures |
| M04 | Setup failed | Blocked |
"""

RULING_T001 = """# T001 MAESTRO ruling: GO (2026-10-15 MDT)

Kill set: M01, M03. Astra's table already shows M02 killed.
"""

VERDICT_GO = """VERDICT: GO

BLOCKING findings: none.

| ID | Mutation | Ticket | Seam |
|---|---|---|---|
| M10 | Delete check | Survived | **Killed** — assertion |
| M11 | Delete other | Survived | — |
"""

PRS = [
    {"number": 12, "headRefName": "tk/T002", "state": "OPEN", "createdAt": "2026-10-16T08:10:00Z",
     "mergedAt": None, "statusCheckRollup": [{"__typename": "CheckRun", "status": "IN_PROGRESS", "conclusion": ""}]},
    {"number": 5, "headRefName": "tk/T002", "state": "CLOSED", "createdAt": "2026-10-16T08:01:00Z",
     "mergedAt": None, "statusCheckRollup": []},
    {"number": 11, "headRefName": "tk/T006", "state": "MERGED", "createdAt": "2026-10-16T07:00:00Z",
     "mergedAt": "2026-10-16T07:30:00Z", "statusCheckRollup": [{"__typename": "CheckRun", "status": "COMPLETED", "conclusion": "SUCCESS"}]},
    {"number": 9, "headRefName": "tk/T001", "state": "MERGED", "createdAt": "2026-10-16T06:00:00Z",
     "mergedAt": "2026-10-16T06:20:00Z", "statusCheckRollup": [{"__typename": "StatusContext", "state": "FAILURE"}]},
]


class Fixture:
    def __init__(self, root):
        self.root = Path(root)
        lean = self.root / "LEAN"
        self.recut = lean / "recut"
        self.team = lean / "teamdash"
        self.repo = self.root / "repo"
        for tid, deps in (("T001", ()), ("T002", ("T001",)), ("T003", ("T001",)), ("T004", ("T001",)),
                          ("T005", ("T004",)), ("T006", ())):
            write(self.recut / "tickets" / (tid + ".json"), ticket(tid, deps))
        write(self.recut / "PLAN.md", "plan\n")
        write(self.team / "tickets" / "T007.json", ticket("T007", ("T005",), astra=True))
        write(self.recut / "ledger.tsv", HEADER
              + "2026-10-16T06:00:00Z\tT001\tdispatch\t0\tlane x base y\n"
              + "2026-10-16T06:21:00Z\tT001\tmerged\t0\tPR #9 MERGED; main checkout at z\n"
              + "2026-10-16T08:00:00Z\tT002\tdispatch\t0\tlane a base b\n"
              + "not-a-time\tT002\tstart\t0\tbroken\n"
              + "2026-10-16T08:05:00Z\tT002\tclose\t0\thttps://github.com/o/r/pull/12\n"
              + "2026-10-16T08:06:00Z\tT002\tshort\n")
        write(lean / "metrics" / "tickets.csv",
              "ticket,series,pr,state,dispatch_mdt,pr_created_mdt,merged_mdt\n"
              "T004,recut,,OPEN,10-15 21:24:50,10-15 21:25:52,\n"
              "T004,other,,OPEN,10-14 01:00:00,,\n")
        os.utime(lean / "metrics" / "tickets.csv", (utc("2026-10-16T00:00:00Z"),) * 2)
        reviews = self.recut / "reviews"
        write(reviews / "T001" / "verdict.md", VERDICT_T001)
        write(reviews / "T001" / "RULING.md", RULING_T001)
        write(reviews / "T002" / "r1" / "verdict.md", "VERDICT: NO-GO\n\n1. **BLOCKING — r1 finding.**\n")
        write(reviews / "T002" / "r2" / "verdict.md", "VERDICT: NO-GO\n\n1. **BLOCKING — r2 finding.**\n")
        write(reviews / "T002" / "verdict.md", VERDICT_GO)
        write(reviews / "T007" / "verdict.md", "no verdict line here\n")
        self.repo.mkdir()
        git(self.repo, "init", "-q", "-b", "main")
        for subject in ("T001: first", "T006: sixth", "unrelated"):
            git(self.repo, "commit", "-q", "--allow-empty", "-m", subject)
        git(self.repo, "update-ref", "refs/remotes/origin/master", "HEAD")
        self.before = time.time()
        git(self.repo, "branch", "tk/T003")
        git(self.repo, "branch", "tk/T002")
        self.after = time.time()
        self.calls = []

    def gh(self, prs=PRS, rc=0, out=None):
        def run(argv):
            self.calls.append(list(argv))
            return rc, (json.dumps(prs) if out is None else out), ("boom" if rc else "")
        return run

    def snap(self, gh=None, repo=None, folders=None):
        return d.snapshot(folders or [self.recut, self.team], now=1000.0,
                          repo=repo or self.repo, gh=gh or self.gh())


class TicketsData(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.f = Fixture(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def by_id(self, snap):
        return {(t["label"], t["id"]): t for t in snap["tickets"]}

    def test_contract_shape_and_json(self):
        snap = self.f.snap()
        self.assertEqual(json.loads(json.dumps(snap)), snap)
        self.assertEqual(snap["generated_epoch"], 1000.0)
        self.assertEqual(snap["folders"], [{"path": str(self.f.recut), "label": "recut", "tickets": 6},
                                           {"path": str(self.f.team), "label": "teamdash", "tickets": 1}])
        keys = {"id", "label", "goal", "deps", "wave", "astra", "write", "test", "out", "state", "pr", "ci",
                "times", "time_source", "reviews", "ruling", "events"}
        for t in snap["tickets"]:
            self.assertEqual(set(t), keys)
            self.assertEqual(set(t["times"]), {"dispatch", "pr_open", "merged"})
        t7 = self.by_id(snap)[("teamdash", "T007")]
        self.assertEqual((t7["goal"], t7["deps"], t7["astra"], t7["write"]),
                         ("goal T007", ["T005"], True, ["code/t007.py"]))
        waves = {t["id"]: t["wave"] for t in snap["tickets"]}
        self.assertEqual(waves, {"T001": 1, "T002": 2, "T003": 2, "T004": 2, "T005": 3, "T006": 1, "T007": 4})

    def test_each_state(self):
        t = self.by_id(self.f.snap())
        states = {k[1]: v["state"] for k, v in t.items()}
        self.assertEqual(states, {"T001": "merged", "T002": "pr", "T003": "running", "T004": "ready",
                                  "T005": "waiting", "T006": "merged", "T007": "waiting"})
        self.assertEqual([(t[("recut", i)]["pr"], t[("recut", i)]["ci"]) for i in ("T001", "T002", "T006", "T003")],
                         [(9, "fail"), (12, "pending"), (11, "pass"), (None, "none")])

    def test_each_time_source(self):
        t = self.by_id(self.f.snap())
        t1, t2, t3, t4, t5, t6 = (t[("recut", "T00%d" % i)] for i in range(1, 7))
        # ledger beats reflog (tk/T002 exists) and gh (createdAt); gh fills merged for T001 only below the ledger
        self.assertEqual(t2["time_source"], "ledger")
        self.assertEqual(t2["times"], {"dispatch": utc("2026-10-16T08:00:00Z"),
                                       "pr_open": utc("2026-10-16T08:05:00Z"), "merged": None})
        self.assertEqual(t1["times"], {"dispatch": utc("2026-10-16T06:00:00Z"),
                                       "pr_open": utc("2026-10-16T06:00:00Z"), "merged": utc("2026-10-16T06:21:00Z")})
        self.assertEqual(t3["time_source"], "reflog")
        self.assertTrue(int(self.f.before) <= t3["times"]["dispatch"] <= self.f.after + 1)
        self.assertEqual(t4["time_source"], "history")  # series row "recut", not "other"; MDT = UTC-6
        self.assertEqual(t4["times"], {"dispatch": utc("2026-10-16T03:24:50Z"),
                                       "pr_open": utc("2026-10-16T03:25:52Z"), "merged": None})
        self.assertEqual(t6["time_source"], "gh")
        self.assertEqual(t6["times"], {"dispatch": None, "pr_open": utc("2026-10-16T07:00:00Z"),
                                       "merged": utc("2026-10-16T07:30:00Z")})
        self.assertEqual((t5["time_source"], t5["times"]), ("none", {"dispatch": None, "pr_open": None, "merged": None}))
        self.assertEqual([(e["event"], e["rc"]) for e in t2["events"]], [("dispatch", 0), ("close", 0)])
        self.assertEqual(t2["events"][1], {"t": utc("2026-10-16T08:05:00Z"), "event": "close", "rc": 0,
                                           "detail": "https://github.com/o/r/pull/12"})

    def test_broken_ledger_row_is_reported_and_rest_kept(self):
        snap = self.f.snap()
        bad = [e for e in snap["errors"] if "ledger" in e]
        self.assertEqual(len(bad), 2, snap["errors"])
        self.assertIn(":5:", bad[0])
        self.assertIn(":7: expected 5", bad[1])
        self.assertEqual(len(snap["tickets"]), 7)

    def test_review_rounds_top_level_and_r_dirs(self):
        t = self.by_id(self.f.snap())
        r1 = t[("recut", "T001")]["reviews"]
        self.assertEqual(r1, [{"round": 1, "verdict": "NO-GO",
                               "blocking": ["1. BLOCKING — first defect is real.",
                                            "2. BLOCKING verification gap — second defect. [x.py:3](x.py:3)"],
                               "notes": 2, "mutants": {"killed": 2, "survived": 1},
                               "path": str(self.f.recut / "reviews" / "T001" / "verdict.md")}])
        self.assertEqual(t[("recut", "T001")]["ruling"],
                         {"path": str(self.f.recut / "reviews" / "T001" / "RULING.md"), "kill_set": ["M01", "M03"],
                          "summary": "T001 MAESTRO ruling: GO (2026-10-15 MDT)"})
        r2 = t[("recut", "T002")]["reviews"]
        self.assertEqual([(r["round"], r["verdict"], r["blocking"], r["mutants"]) for r in r2],
                         [(1, "NO-GO", ["1. BLOCKING — r1 finding."], {"killed": 0, "survived": 0}),
                          (2, "NO-GO", ["1. BLOCKING — r2 finding."], {"killed": 0, "survived": 0}),
                          (3, "GO", [], {"killed": 1, "survived": 1})])
        self.assertTrue(r2[0]["path"].endswith("T002/r1/verdict.md"))
        self.assertEqual(t[("recut", "T002")]["ruling"], {"path": None, "kill_set": [], "summary": ""})
        # teamdash has no reviews/ of its own: recut/reviews is searched
        self.assertEqual([(r["round"], r["verdict"]) for r in t[("teamdash", "T007")]["reviews"]], [(1, "NONE")])
        self.assertEqual(t[("recut", "T003")]["reviews"], [])

    def test_gh_failure_is_reported_and_snapshot_returns(self):
        for gh in (self.f.gh(rc=1), self.f.gh(out="not json"), self.f.gh(out='{"a": 1}')):
            snap = self.f.snap(gh=gh)
            self.assertEqual(len(snap["tickets"]), 7)
            self.assertEqual(len([e for e in snap["errors"] if e.startswith("gh")]), 1, snap["errors"])
            t = self.by_id(snap)
            self.assertEqual(t[("recut", "T002")]["state"], "running")
            self.assertEqual(t[("recut", "T006")]["time_source"], "none")

    def test_gh_missing_binary_is_an_error(self):
        def run(argv):
            raise FileNotFoundError("gh")
        snap = self.f.snap(gh=run)
        self.assertEqual(len([e for e in snap["errors"] if e.startswith("gh")]), 1, snap["errors"])

    def test_gh_called_once_per_snapshot(self):
        self.f.snap()
        self.assertEqual(len(self.f.calls), 1)
        argv = self.f.calls[0]
        self.assertEqual(argv[:6], ["gh", "pr", "list", "--state", "all", "--limit"])
        self.assertEqual(argv[6], "300")

    def test_git_failure_is_reported_and_tickets_kept(self):
        notgit = Path(self.tmp.name) / "notgit"
        notgit.mkdir()
        snap = self.f.snap(repo=notgit)
        self.assertEqual(len(snap["tickets"]), 7)
        self.assertTrue([e for e in snap["errors"] if e.startswith("git")], snap["errors"])
        t = self.by_id(snap)
        self.assertEqual(t[("recut", "T001")]["state"], "ready")
        self.assertEqual(t[("recut", "T002")]["state"], "pr")

    def test_bad_ticket_file_and_missing_folder_are_errors_not_drops(self):
        write(self.f.recut / "tickets" / "T009.json", "{broken")
        write(self.f.recut / "tickets" / "T010.json", "[1]")
        missing = Path(self.tmp.name) / "LEAN" / "gone"
        snap = self.f.snap(folders=[self.f.recut, missing])
        ids = [t["id"] for t in snap["tickets"]]
        self.assertIn("T009", ids)
        self.assertIn("T010", ids)
        self.assertTrue([e for e in snap["errors"] if "T009.json" in e], snap["errors"])
        self.assertTrue([e for e in snap["errors"] if "T010.json: not a JSON object" in e], snap["errors"])
        self.assertTrue([e for e in snap["errors"] if "gone" in e], snap["errors"])
        self.assertEqual(snap["folders"][1], {"path": str(missing), "label": "gone", "tickets": 0})

    def test_undecodable_sources_are_errors(self):
        bad = b"\xff\xfe\x00broken"
        for path in (self.f.recut / "ledger.tsv", self.f.root / "LEAN" / "metrics" / "tickets.csv",
                     self.f.recut / "reviews" / "T001" / "verdict.md", self.f.recut / "reviews" / "T001" / "RULING.md"):
            path.write_bytes(bad)
        snap = self.f.snap()
        self.assertEqual(len(snap["tickets"]), 7)
        for word in ("ledger", "history", "verdict.md", "RULING.md"):
            self.assertTrue([e for e in snap["errors"] if word in e], (word, snap["errors"]))

    def test_dependency_cycle_is_an_error(self):
        write(self.f.team / "tickets" / "T007.json", ticket("T007", ("T008",)))
        write(self.f.team / "tickets" / "T008.json", ticket("T008", ("T007",)))
        snap = self.f.snap()
        self.assertTrue([e for e in snap["errors"] if "cycle" in e], snap["errors"])
        self.assertEqual(len(snap["tickets"]), 8)

    def test_bad_gh_time_is_an_error(self):
        prs = [dict(p, createdAt="yesterday") for p in PRS if p["number"] == 11]
        snap = self.f.snap(gh=self.f.gh(prs=prs))
        self.assertTrue([e for e in snap["errors"] if e.startswith("gh pr #11")], snap["errors"])
        self.assertEqual(self.by_id(snap)[("recut", "T006")]["pr"], 11)

    def test_git_launch_failure_and_unparsed_reflog_are_errors(self):
        real = d.subprocess.run

        def no_git(argv, **kw):
            if argv[0] == "git":
                raise FileNotFoundError("git")
            return real(argv, **kw)
        with unittest.mock.patch.object(d.subprocess, "run", no_git):
            snap = self.f.snap()
        self.assertEqual(len([e for e in snap["errors"] if e.startswith("git")]), 2, snap["errors"])
        real_git = d.git
        with unittest.mock.patch.object(d, "git", lambda repo, *a: "junk\n" if a[0] == "reflog" else real_git(repo, *a)):
            snap = self.f.snap()
        self.assertTrue([e for e in snap["errors"] if "reflog" in e], snap["errors"])
        self.assertEqual(self.by_id(snap)[("recut", "T003")]["time_source"], "none")

        def reflog_fails(repo, *a):
            if a[0] == "reflog":
                raise d.SourceError("git reflog failed (rc 128): fixture")
            return real_git(repo, *a)
        with unittest.mock.patch.object(d, "git", reflog_fails):
            snap = self.f.snap()
        self.assertEqual(len([e for e in snap["errors"] if e.startswith("git reflog failed")]), 2, snap["errors"])

    def test_bad_history_csv_is_an_error(self):
        write(self.f.root / "LEAN" / "metrics" / "tickets.csv",
              "ticket,series,dispatch_mdt,pr_created_mdt,merged_mdt\nT004,recut,garbage,,\n")
        snap = self.f.snap()
        self.assertTrue([e for e in snap["errors"] if "tickets.csv" in e], snap["errors"])
        self.assertEqual(self.by_id(snap)[("recut", "T004")]["time_source"], "none")


if __name__ == "__main__":
    unittest.main()
