#!/usr/bin/env python3
"""CLOSE-OUT GATE — verify a Decision-ID has been propagated to ALL canonical trackers.

This is the WRITE-side gate of the read<->write context loop (DISCIPLINE §1.1).
Run it at experiment close BEFORE declaring done or writing SESSION_CHECKPOINT.
A RED gate means the experiment is NOT done — propagate the D-ID, then re-run.
Checking coverage is the SCRIPT's job, not the operator's.

Usage:
  python3 tools/closeout_check.py D-B1-2        # exit 0 = all green, 1 = gaps
  python3 tools/closeout_check.py --list        # print the required tracker set

Why this exists: the close-out set was prose-only with no enforcement, so under a
long session the scattered trackers (CORPUS/00-03, EVIDENCE_INDEX, EXPERIMENT_REGISTRY,
PROGRESS, HYPOTHESIS_REGISTER) silently lapsed while the salient ones (CORPUS/NN, §0.3,
checkpoint, memories) got updated. This makes the full set mechanical + non-skippable.
"""
import sys, os, glob, filecmp

ROOT = os.environ.get("LLMDB_ROOT", "/workspace")

# The COMPLETE canonical tracker set (corrects the under-specified DISCIPLINE §1.1 list).
REQUIRED = [
    ("EXPERIMENT_RUNBOOK.md",            "living roadmap (also §0.3/§12/§13 — section checks below)"),
    ("SESSION_CHECKPOINT.md",            "fresh-context handoff"),
    ("PROGRESS.md",                      "F1 readiness scorecard (①/③/④/⑤)"),
    ("EVIDENCE_INDEX.md",                "evidence index"),
    ("docs/EXPERIMENT_REGISTRY.md",      "experiment registry"),
    ("CORPUS/00_MASTER_EVIDENCE.md",     "master evidence ledger"),
    ("CORPUS/03_STATUS_LEDGER.md",       "status ledger"),
    ("CORPUS/01_PROVENANCE_MANIFEST.md", "provenance (claim->artifact->numbers)"),
    ("CORPUS/02_VANDV_CHAIN.md",         "V&V chain (hypothesis->criterion->verdict)"),
]
_hr = sorted(glob.glob(os.path.join(ROOT, "docs/HYPOTHESIS_REGISTER_*.md")))
if _hr:
    REQUIRED.append((os.path.relpath(_hr[-1], ROOT), "hypothesis register (latest)"))


def _read(path):
    try:
        return open(os.path.join(ROOT, path), encoding="utf-8", errors="replace").read()
    except FileNotFoundError:
        return None


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "--list"):
        print(__doc__)
        print("Required trackers (Decision-ID must appear in each):")
        for p, d in REQUIRED:
            print(f"  - {p:42s} {d}")
        print("  - CORPUS/NN_*.md                            the experiment writeup (>=1 file)")
        print("  - EXPERIMENT_RUNBOOK.md  §0.3 + §12 + §13   (section-level)")
        print("  - memory_mirror/  in sync with live memory  (advisory)")
        sys.exit(0 if (len(sys.argv) > 1 and sys.argv[1] == "--list") else 2)

    tok = sys.argv[1]
    missing = []
    print(f"CLOSE-OUT GATE for {tok}\n" + "=" * 52)

    for path, desc in REQUIRED:
        txt = _read(path)
        ok = (txt is not None and tok in txt)
        tag = "GREEN  " if ok else ("MISSING" if txt is not None else "NO FILE")
        print(f"  [{tag}] {path}  — {desc}")
        if not ok:
            missing.append(path)

    # CORPUS writeup: >=1 CORPUS/NN_*.md must reference the D-ID
    corpus_hits = [os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "CORPUS/*.md"))
                   if tok in open(p, errors="replace").read()]
    print(f"  [{'GREEN  ' if corpus_hits else 'MISSING'}] CORPUS/NN writeup — {corpus_hits or 'none reference the D-ID'}")
    if not corpus_hits:
        missing.append("CORPUS/NN writeup")

    # Runbook section-level (§0.3 next-actions, §12 dashboard, §13 changelog are distinct gates in one file)
    rb = _read("EXPERIMENT_RUNBOOK.md") or ""
    def span(a, b):
        i = rb.find(a)
        if i < 0:
            return ""
        j = rb.find(b, i + 1)
        return rb[i:j if j > 0 else len(rb)]
    for name, ok in [("§0.3 next-actions", tok in span("### §0.3", "### §0.4")),
                     ("§12 dashboard",     tok in span("## §12", "## §13")),
                     ("§13 changelog",     tok in (rb.split("## §13")[-1] if "## §13" in rb else ""))]:
        print(f"  [{'GREEN  ' if ok else 'MISSING'}] EXPERIMENT_RUNBOOK.md {name}")
        if not ok:
            missing.append(f"runbook {name}")

    # Memory mirror sync (advisory — warns, does not fail the gate)
    live = "/root/.claude/projects/-workspace/memory"
    mir = os.path.join(ROOT, "memory_mirror")
    if os.path.isdir(live) and os.path.isdir(mir):
        d = filecmp.dircmp(live, mir)
        drift = sorted(f for f in (set(d.left_only) | set(d.diff_files)) if f.endswith(".md"))
        print(f"  [{'GREEN  ' if not drift else 'WARN   '}] memory_mirror sync" +
              (f" — unmirrored/changed: {drift}" if drift else ""))

    print("=" * 52)
    if missing:
        print(f"❌ CLOSE-OUT INCOMPLETE — {len(missing)} gap(s): {missing}")
        print(f"   The experiment is NOT done. Propagate {tok} to each gap, then re-run this check.")
        sys.exit(1)
    print(f"✅ CLOSE-OUT COMPLETE — {tok} propagated to all canonical trackers.")
    sys.exit(0)


if __name__ == "__main__":
    main()
