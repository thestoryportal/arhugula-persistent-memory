#!/usr/bin/env python3
"""CLOSE-OUT GATE — verify a Decision-ID is propagated to ALL canonical trackers,
AND (currency layer) that each tracker reflects the CURRENT result content.

WRITE-side gate of the read<->write context loop (DISCIPLINE §1.1). Run at experiment
close AFTER updating SESSION_CHECKPOINT and all required trackers, BEFORE declaring done; rerun after any subsequent tracker edit. RED = NOT done.

Two layers:
  1. PRESENCE — the Decision-ID string appears in each canonical tracker.
  2. CURRENCY (fingerprint) — for D-IDs registered in code/gates/closeout_fingerprints.json,
     the gate hashes the canonical SOURCE span and requires the token '<D-ID>@<8hex>'
     in every tracker. When the source content changes, the hash changes, so any tracker
     still carrying the OLD token reads STALE (not GREEN) -> forces re-propagation of a
     REFINED result, not just first-close presence. (Built 2026-06-21 after a green gate
     hid 7 ledgers frozen at a superseded 'k<=2' value while the result had moved to 'k<=1'.)
  D-IDs absent from the registry fall back to presence-only (back-compatible).

Usage:
  python3 code/gates/closeout_check.py D-D1-2     # exit 0 = all green, 1 = gaps/stale
  python3 code/gates/closeout_check.py --fp D-D1-2  # print the current fingerprint token to embed
  python3 code/gates/closeout_check.py --list     # print the required tracker set
"""
import sys, os, glob, filecmp, json, hashlib, re

# code/gates/closeout_check.py -> the repo root is three levels up; env overrides.
ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REQUIRED = [
    ("program/runbook/",            "living roadmap (also §0.3/§12/§13 — section checks below)"),
    ("program/checkpoints/",            "fresh-context handoff"),
    ("program/PROGRESS.md",                      "F1 readiness scorecard (①/③/④/⑤)"),
    ("program/EVIDENCE_INDEX.md",                "evidence index"),
    ("program/registers/EXPERIMENT_REGISTRY.md",      "experiment registry"),
    ("evidence/CORPUS/00_MASTER_EVIDENCE.md",     "master evidence ledger"),
    ("evidence/CORPUS/03_STATUS_LEDGER.md",       "status ledger"),
    ("evidence/CORPUS/01_PROVENANCE_MANIFEST.md", "provenance (claim->artifact->numbers)"),
    ("evidence/CORPUS/02_VANDV_CHAIN.md",         "V&V chain (hypothesis->criterion->verdict)"),
]
_hr = sorted(glob.glob(os.path.join(ROOT, "program/registers/HYPOTHESIS_REGISTER_*.md")))
if _hr:
    REQUIRED.append((os.path.relpath(_hr[-1], ROOT), "hypothesis register (latest)"))


def _read(path):
    full = os.path.join(ROOT, path)
    # A monolith split into a folder of parts reads as its parts in name order: byte for byte the original.
    if os.path.isdir(full):
        parts = sorted(n for n in os.listdir(full) if n.endswith(".md"))
        return "".join(open(os.path.join(full, n), encoding="utf-8", errors="replace").read() for n in parts) if parts else None
    try:
        return open(full, encoding="utf-8", errors="replace").read()
    except FileNotFoundError:
        return None


def _load_registry():
    try:
        return json.load(open(os.path.join(ROOT, "code/gates/closeout_fingerprints.json"), encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        return {}


def compute_fp(spec):
    """Hash the canonical source span -> 8 hex. None if the source/anchor is missing."""
    txt = _read(spec.get("source", ""))
    if txt is None:
        return None, "source file missing"
    start = spec.get("anchor_start")
    if start:
        i = txt.find(start)
        if i < 0:
            return None, f"anchor_start not found: {start!r}"
    else:
        i = 0  # whole-file (from start)
    end = spec.get("anchor_end")
    j = txt.find(end, i + 1) if end else -1
    span = txt[i: j if j > 0 else len(txt)]
    # strip stamped fingerprint markers so hashing the source is immune to its own tokens
    span = re.sub(r"⟨[^⟩]*⟩", "", span)
    span = re.sub(r"\bD-[A-Za-z0-9-]+@[0-9a-f]{6,}\b", "", span)
    norm = re.sub(r"\s+", " ", span).strip()
    return hashlib.sha1(norm.encode("utf-8")).hexdigest()[:8], None


def status(txt, tok, fptok):
    """(label, ok). STALE = D-ID present but the current fingerprint token absent."""
    if txt is None:
        return "NO FILE", False
    if tok not in txt:
        return "MISSING", False
    if fptok and fptok not in txt:
        return "STALE  ", False
    return "GREEN  ", True


def currency_scan(tok, spec):
    """Return (fptok, stale_paths, err). Checks every doc REFERENCING tok carries the current token."""
    fp, err = compute_fp(spec)
    if err:
        return None, [], err
    fptok = f"{tok}@{fp}"
    # surfacing/entry/repro docs also participate so a result/state ties across the whole graph
    EXTRA = ["README.md", "program/SESSION_BOOTSTRAP.md", "_system/governance/REPRODUCIBILITY.md", "evidence/CORPUS/README.md"]
    scope = ([p for p, _ in REQUIRED]
             + [os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "evidence/CORPUS/*.md"))]
             + EXTRA)
    stale, seen = [], set()
    for path in scope:
        if path in seen:
            continue
        seen.add(path)
        txt = _read(path)
        if txt is None or tok not in txt:
            continue
        if fptok not in txt:
            stale.append(path)
    return fptok, stale, None


def runbook_sections(rb):
    # [LAW:one-type-per-behavior] Headings are matched at line start, so "### §13 changelog" never stands in
    # for "## §13": a substring match let each newest §13 entry hide every older D-ID from the gate.
    def heading(h, start=0):
        m = re.compile(r"^" + re.escape(h), re.M).search(rb, start)
        return m.start() if m else -1
    def span(a, b):
        i = heading(a)
        if i < 0:
            return ""
        j = heading(b, i + 1) if b else -1
        return rb[i:j if j > 0 else len(rb)]
    return {"§0.3 next-actions": span("### §0.3", "### §0.4"),
            "§12 dashboard":     span("## §12", "## §13"),
            "§13 changelog":     span("## §13", None)}


def main():
    reg = _load_registry()

    if len(sys.argv) >= 2 and sys.argv[1] == "--audit":
        keys = sorted(k for k in reg if not k.startswith("_"))
        print(f"CURRENCY AUDIT — {len(keys)} registered fingerprint(s)\n" + "=" * 56)
        any_stale = False
        for k in keys:
            fptok, stale, err = currency_scan(k, reg[k])
            if err:
                print(f"  [FP ERR] {k}: {err}"); any_stale = True; continue
            if stale:
                any_stale = True
                print(f"  [STALE ] {fptok} — {len(stale)} doc(s): {stale}")
            else:
                print(f"  [CURRENT] {fptok}")
        print("=" * 56)
        if any_stale:
            print("❌ AUDIT FAILED — re-propagate the STALE fingerprints (get tokens via --fp <ID>)."); sys.exit(1)
        print("✅ AUDIT CLEAN — every registered result/state is current across all referencing docs."); sys.exit(0)

    if len(sys.argv) >= 3 and sys.argv[1] == "--fp":
        tok = sys.argv[2]
        spec = reg.get(tok)
        if not spec:
            print(f"{tok}: no fingerprint registered (presence-only). Add it to code/gates/closeout_fingerprints.json to enable the currency check.")
            sys.exit(0)
        fp, err = compute_fp(spec)
        if err:
            print(f"{tok}: FINGERPRINT ERROR — {err}")
            sys.exit(2)
        print(f"{tok}@{fp}")
        print(f"  source: {spec['source']}  [{spec.get('anchor_start','<whole file>')!r} .. {spec.get('anchor_end','EOF')!r}]")
        print(f"  → embed the token '{tok}@{fp}' in every canonical tracker (alongside the result prose).")
        sys.exit(0)

    if len(sys.argv) >= 3 and sys.argv[1] == "--currency":
        # CURRENCY-ONLY: for every canonical doc that REFERENCES the D-ID, require the current
        # fingerprint token. Ignores absence (no presence requirement) — so it works for historical
        # D-IDs that legitimately aren't in §0.3 "current position". Flags present-but-STALE.
        tok = sys.argv[2]
        spec = reg.get(tok)
        if not spec:
            print(f"{tok}: not registered for fingerprinting — nothing to currency-check.")
            sys.exit(0)
        fptok, stale, err = currency_scan(tok, spec)
        if err:
            print(f"{tok}: FINGERPRINT ERROR — {err}")
            sys.exit(2)
        print(f"CURRENCY CHECK {fptok}  (source: {spec['source']})\n" + "-" * 56)
        for p in stale:
            print(f"  [STALE  ] {p}  (has {tok}, not {fptok})")
        if stale:
            print(f"❌ {len(stale)} STALE reference(s) — re-propagate {fptok}: {stale}")
            sys.exit(1)
        print(f"✅ all references to {tok} are CURRENT ({fptok}).")
        sys.exit(0)

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "--list"):
        print(__doc__)
        print("Required trackers (Decision-ID + current fingerprint must appear in each):")
        for p, d in REQUIRED:
            print(f"  - {p:42s} {d}")
        print("  - evidence/CORPUS/NN_*.md                            the experiment writeup (>=1 file)")
        print("  - program/runbook/  §0.3 + §12 + §13   (section-level)")
        print("  - _system/memory/  in sync with live memory  (advisory)")
        print(f"\nFingerprint-registered D-IDs (currency-checked): {sorted(k for k in reg if not k.startswith('_')) or 'none'}")
        sys.exit(0 if (len(sys.argv) > 1 and sys.argv[1] == "--list") else 2)

    tok = sys.argv[1]
    missing, stale = [], []
    print(f"CLOSE-OUT GATE for {tok}\n" + "=" * 56)

    spec = reg.get(tok)
    fptok = None
    if spec:
        fp, err = compute_fp(spec)
        if err:
            print(f"  [FP ERR] fingerprint source unreadable — {err}; falling back to presence-only")
        else:
            fptok = f"{tok}@{fp}"
            print(f"  content fingerprint: {fptok}   (source: {spec['source']})")
            print(f"  CURRENCY layer ON — trackers must carry '{fptok}', not just '{tok}'.")
    else:
        print(f"  (no fingerprint registered — PRESENCE-ONLY; add {tok} to code/gates/closeout_fingerprints.json for the currency check)")
    print("-" * 56)

    def record(label, path):
        if label.strip() == "STALE":
            stale.append(path)
        elif label.strip() not in ("GREEN",):
            missing.append(path)

    for path, desc in REQUIRED:
        label, ok = status(_read(path), tok, fptok)
        print(f"  [{label}] {path}  — {desc}")
        if not ok:
            record(label, path)

    # CORPUS writeup: >=1 evidence/CORPUS/NN_*.md must reference the D-ID AND be current
    corpus_files = {os.path.basename(p): open(p, errors="replace").read() for p in glob.glob(os.path.join(ROOT, "evidence/CORPUS/*.md"))}
    corpus_present = [n for n, t in corpus_files.items() if tok in t]
    corpus_current = [n for n in corpus_present if (not fptok or fptok in corpus_files[n])]
    if not corpus_present:
        print(f"  [MISSING] evidence/CORPUS/NN writeup — none reference the D-ID"); missing.append("evidence/CORPUS/NN writeup")
    elif not corpus_current:
        print(f"  [STALE  ] evidence/CORPUS/NN writeup — has {tok} but not {fptok}: {corpus_present}"); stale.append("evidence/CORPUS/NN writeup")
    else:
        print(f"  [GREEN  ] evidence/CORPUS/NN writeup — {corpus_current}")

    # Runbook section-level spans (each must carry the D-ID + current fingerprint)
    rb = _read("program/runbook/") or ""
    for name, seg in runbook_sections(rb).items():
        label, ok = status(seg, tok, fptok)
        print(f"  [{label}] program/runbook/ {name}")
        if not ok:
            record(label, f"runbook {name}")

    # Memory mirror sync (advisory). The live Claude memory moved off the pod (/root/.claude/projects/-workspace)
    # with D-HW-1; a missing live dir is reported, never skipped silently. MEMORY.md indexes legitimately differ
    # (the mirror also carries team-written entries), so the invariant checked for it is "every index link resolves".
    live = os.environ.get("LLMDB_LIVE_MEMORY",
                          os.path.expanduser("~/.claude/projects/-Volumes-memit-llm-database-poc-mirror/memory"))
    mir = os.path.join(ROOT, "_system/memory")
    if not os.path.isdir(live):
        print(f"  [WARN   ] memory_mirror sync — live memory dir not found: {live} (set LLMDB_LIVE_MEMORY)")
    else:
        d = filecmp.dircmp(live, mir)
        drift = sorted(f for f in (set(d.left_only) | set(d.diff_files)) if f.endswith(".md") and f != "MEMORY.md")
        print(f"  [{'GREEN  ' if not drift else 'WARN   '}] memory_mirror sync" +
              (f" — unmirrored/changed: {drift}" if drift else ""))
    index = os.path.join(mir, "MEMORY.md")
    links = re.findall(r"\]\(([^)]+\.md)(?:#[^)]*)?\)", open(index).read())
    dead = sorted({p for p in links if not os.path.isfile(os.path.join(mir, p))})
    print(f"  [{'GREEN  ' if not dead else 'WARN   '}] _system/memory/MEMORY.md links" +
          (f" — dead: {dead}" if dead else ""))

    print("=" * 56)
    if missing or stale:
        if missing:
            print(f"❌ {len(missing)} MISSING (no {tok}): {missing}")
        if stale:
            print(f"❌ {len(stale)} STALE (have {tok} but not {fptok} — content moved on, re-propagate): {stale}")
        print(f"   NOT done. Fix each, embed '{fptok or tok}', then re-run.")
        sys.exit(1)
    print(f"✅ CLOSE-OUT COMPLETE — {tok} present + current ({fptok or 'presence-only'}) in all canonical trackers.")
    sys.exit(0)


if __name__ == "__main__":
    main()
