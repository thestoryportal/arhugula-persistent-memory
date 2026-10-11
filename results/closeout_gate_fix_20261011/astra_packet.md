# Review packet — close-out gate §13 span fix (MAESTRO30, 2026-10-11)

You are the cross-family reviewer (read-only). Verdict: ACCEPT / ACCEPT-WITH-CONDITIONS / REJECT, with numbered findings (file:line).

## Defect
`tools/closeout_check.py` located the runbook §13 changelog with `rb.split("## §13")[-1]`. Every `### §13 changelog — <date>` entry heading also contains the substring `## §13`, so the gate saw only the text after the NEWEST entry heading. Each new D-ID's changelog entry therefore turned every older D-ID's §13 check MISSING (observed: D-NEW1-b, D-NEW1-fid, D-C10z-a4).

## Fix
Extracted the three runbook spans into a pure `runbook_sections(rb)`; headings now match only at line start (`re.M`, `^` + escaped heading), and §13 is the span from `## §13` to end of file. §0.3/§12 use the same anchored matcher (same boundaries as before when headings are unique).

## Evidence
- Red-first: the extraction with OLD semantics failed 2/5 new tests (changelog span holds all entries; deeper `####` heading does not open a section); the fix passes 5/5.
- Gate output before/after on the real runbook for 5 D-IDs: the ONLY changed lines are the §13 row and the summary (D-NEW1-b, D-NEW1-fid, D-C10z-a4 go MISSING→GREEN, rc 1→0; D-NEW1-c stays green; D-C10r-rulings-18 §13 goes GREEN but stays rc 1 on 10 other trackers — unrelated, genuine).

## Questions for you
1. Does the fix make the gate pass anything it should not (e.g. a D-ID mentioned only in §13's preamble before the first entry, or in a later level-2 section after §13 if one existed)? Is "§13 = to end of file" correct for this runbook? Check `EXPERIMENT_RUNBOOK.md` for any `## ` heading after `## §13`.
2. Any other caller relies on the old behavior (pre-commit hook `tools/git_hooks/`, render_state, dashboard)?
3. Are the tests behavior-level and sufficient?

## Diff
```diff
diff --git a/tools/closeout_check.py b/tools/closeout_check.py
index 3a731ed4..2a313e3a 100644
--- a/tools/closeout_check.py
+++ b/tools/closeout_check.py
@@ -111,6 +111,23 @@ def currency_scan(tok, spec):
     return fptok, stale, None
 
 
+def runbook_sections(rb):
+    # [LAW:one-type-per-behavior] Headings are matched at line start, so "### §13 changelog" never stands in
+    # for "## §13": a substring match let each newest §13 entry hide every older D-ID from the gate.
+    def heading(h, start=0):
+        m = re.compile(r"^" + re.escape(h), re.M).search(rb, start)
+        return m.start() if m else -1
+    def span(a, b):
+        i = heading(a)
+        if i < 0:
+            return ""
+        j = heading(b, i + 1) if b else -1
+        return rb[i:j if j > 0 else len(rb)]
+    return {"§0.3 next-actions": span("### §0.3", "### §0.4"),
+            "§12 dashboard":     span("## §12", "## §13"),
+            "§13 changelog":     span("## §13", None)}
+
+
 def main():
     reg = _load_registry()
 
@@ -223,15 +240,7 @@ def main():
 
     # Runbook section-level spans (each must carry the D-ID + current fingerprint)
     rb = _read("EXPERIMENT_RUNBOOK.md") or ""
-    def span(a, b):
-        i = rb.find(a)
-        if i < 0:
-            return ""
-        j = rb.find(b, i + 1)
-        return rb[i:j if j > 0 else len(rb)]
-    for name, seg in [("§0.3 next-actions", span("### §0.3", "### §0.4")),
-                      ("§12 dashboard",     span("## §12", "## §13")),
-                      ("§13 changelog",     rb.split("## §13")[-1] if "## §13" in rb else "")]:
+    for name, seg in runbook_sections(rb).items():
         label, ok = status(seg, tok, fptok)
         print(f"  [{label}] EXPERIMENT_RUNBOOK.md {name}")
         if not ok:
```

## New test file tools/test_closeout_check.py
```python
"""Runbook section spans for the close-out gate: each span is bounded by its own heading level."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import closeout_check as cc

RUNBOOK = """# Runbook
### §0.3 — next actions
D-OLD-1 next
### §0.4 — tracker list
D-NOT-IN-03
## §12 — LIVE STATUS DASHBOARD
D-DASH
## §13 — CHANGELOG (append-only)
### §13 changelog — 2026-06-18
D-OLDEST entry
### §13 changelog — 2026-10-10
D-MIDDLE entry
### §13 changelog — 2026-10-11
D-NEWEST entry
"""


class RunbookSections(unittest.TestCase):
    def setUp(self):
        self.s = cc.runbook_sections(RUNBOOK)

    def test_changelog_span_holds_every_entry_not_only_the_newest(self):
        for tok in ("D-OLDEST", "D-MIDDLE", "D-NEWEST"):
            self.assertIn(tok, self.s["§13 changelog"])

    def test_dashboard_span_ends_at_the_changelog(self):
        self.assertIn("D-DASH", self.s["§12 dashboard"])
        self.assertNotIn("D-OLDEST", self.s["§12 dashboard"])

    def test_next_actions_span_ends_at_0_4(self):
        self.assertIn("D-OLD-1", self.s["§0.3 next-actions"])
        self.assertNotIn("D-NOT-IN-03", self.s["§0.3 next-actions"])

    def test_deeper_heading_does_not_open_a_section(self):
        s = cc.runbook_sections("#### §0.3 decoy\nD-DECOY\n" + RUNBOOK)
        self.assertNotIn("D-DECOY", s["§0.3 next-actions"])

    def test_missing_heading_gives_empty_span(self):
        s = cc.runbook_sections("# no sections here\nD-X\n")
        self.assertEqual(set(s.values()), {""})


if __name__ == "__main__":
    unittest.main()
```
