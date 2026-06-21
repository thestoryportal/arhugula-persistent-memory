#!/usr/bin/env python3
"""GENERATED-BLOCK renderer — the 'generate what's mechanical' half of the anti-drift design.

Single canonical source: docs/program_state.json. This renders its content into
<!-- BEGIN GENERATED:<block> --> ... <!-- END GENERATED:<block> --> regions across the
high-drift context docs, so structured status is AUTO-UPDATED (one edit + one command),
never hand-copied into 14 places. Complements the narrative-reference fingerprints in
tools/closeout_check.py. (Reconciled design, Opus advisor + gpt-5.5 cross-family, 2026-06-21.)

Usage:
  python3 tools/render_state.py --write   # refresh all generated blocks from program_state.json
  python3 tools/render_state.py --check   # exit 1 if any block is stale (used by the pre-commit hook)
"""
import sys, os, json, re

ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
STATE = os.path.join(ROOT, "docs/program_state.json")

# which generated block goes in which file, and the anchor line to insert after if absent
TARGETS = [
    ("SESSION_CHECKPOINT.md", "program-state", "# SESSION CHECKPOINT"),
    ("EXPERIMENT_RUNBOOK.md", "program-state", "### §0.3 — CURRENT POSITION"),
    ("README.md",             "program-state", "# "),
    ("SESSION_BOOTSTRAP.md",  "program-state", "_Updated 2026-06-18"),
    ("PROGRESS.md",           "f1-scorecard",  "## ⑤ DISTANCE TO F1"),
]

EDIT_NOTE = "_auto-generated from `docs/program_state.json` — DO NOT edit between the markers; run `python3 tools/render_state.py --write`._"


def _state():
    return json.load(open(STATE, encoding="utf-8"))


def render(block, s):
    if block == "program-state":
        acts = "\n".join(f"  {i+1}. {a}" for i, a in enumerate(s["next_actions"]))
        return (f"**📍 PROGRAM STATE (updated {s['updated']})** — {EDIT_NOTE}\n\n"
                f"- **North star:** {s['north_star']}\n"
                f"- **Latest:** {s['current_latest']}\n"
                f"- **F1 status:** {s['f1_verdict']}\n"
                f"- **Next actions (priority):**\n{acts}")
    if block == "f1-scorecard":
        sc = s["scorecard"]
        return (f"**F1 READINESS SCORECARD (updated {s['updated']})** — {EDIT_NOTE}\n\n"
                f"- **Deployment data path:** {sc['deployment_path']}\n"
                f"- **Governance:** {sc['governance']}\n"
                f"- **Robustness:** {sc['robustness']}\n"
                f"- **Critical path:** {sc['critical_path']}\n"
                f"- **Verdict:** {s['f1_verdict']}")
    raise KeyError(block)


def apply(path, block, anchor, content, write):
    full = os.path.join(ROOT, path)
    try:
        txt = open(full, encoding="utf-8").read()
    except FileNotFoundError:
        return None, f"NO FILE {path}"
    begin, end = f"<!-- BEGIN GENERATED:{block} -->", f"<!-- END GENERATED:{block} -->"
    new_region = f"{begin}\n{content}\n{end}"
    pat = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.S)
    if pat.search(txt):
        new = pat.sub(lambda m: new_region, txt)
    else:
        # insert after the anchor line (first occurrence)
        i = txt.find(anchor)
        if i < 0:
            return None, f"ANCHOR MISSING in {path}: {anchor!r}"
        nl = txt.find("\n", i)
        nl = len(txt) if nl < 0 else nl
        new = txt[:nl + 1] + "\n" + new_region + "\n" + txt[nl + 1:]
    stale = (new != txt)
    if stale and write:
        open(full, "w", encoding="utf-8").write(new)
    return stale, None


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    if mode not in ("--check", "--write"):
        print(__doc__); sys.exit(2)
    s = _state()
    stale, errs = [], []
    for path, block, anchor in TARGETS:
        st, err = apply(path, block, anchor, render(block, s), write=(mode == "--write"))
        if err:
            errs.append(err); continue
        tag = ("WROTE " if (st and mode == "--write") else ("STALE " if st else "ok    "))
        print(f"  [{tag}] {path}  (GENERATED:{block})")
        if st and mode == "--check":
            stale.append(path)
    for e in errs:
        print(f"  [ERR] {e}")
    if errs:
        print("❌ render error (anchor/file missing) — fix TARGETS or the doc."); sys.exit(2)
    if mode == "--check" and stale:
        print(f"❌ {len(stale)} STALE generated block(s) vs docs/program_state.json — run `tools/render_state.py --write`: {stale}")
        sys.exit(1)
    print("✅ generated blocks WRITTEN." if mode == "--write" else "✅ all generated blocks current.")
    sys.exit(0)


if __name__ == "__main__":
    main()
