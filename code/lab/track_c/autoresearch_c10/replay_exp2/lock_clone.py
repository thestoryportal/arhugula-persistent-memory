#!/usr/bin/env python3
"""Freeze a freshly set-up replay clone against incidental writers (D-C10r-rulings-7; halt
experiments/c10r/runs/autoresearch_replay_c10_exp2loc/halts/c10r_exp2ctl_halt_diagnostic.json: graft rewrote tracked files between setup and dispatch).
v2 after Codex FIX-FIRST (experiments/c10r/reviews/c10r_exp2ctl_lock_codex_review.md): mode bits alone left root replacement open.

Run right after setup_replay.sh and before tokenizer_precheck.py, then run the precheck/runner with
GIT_OPTIONAL_LOCKS=0 in the environment (frozen .git cannot take optional index refreshes):
    .venv/bin/python code/lab/track_c/autoresearch_c10/replay_exp2/lock_clone.py <DEST>

Every entry that exists under DEST at lock time (regular files, directories including .git, and the .venv symlink
entry itself, never its target) gets the macOS user-immutable flag (UF_IMMUTABLE, `uchg`), children before their
directory. That forbids in-place writes, rename-over, unlink and chmod of those entries. DEST itself stays writable,
because the runner and the recipe create, replace and remove NEW files there (receipts, logs, `.hparams_*.json`,
`runs/`). The owner can clear the flag deliberately; this guards against incidental writers, not adversaries.

Acceptance, all before any precheck or dispatch (exit 2 on any miss):
  - every pre-existing entry carries UF_IMMUTABLE;
  - refused: append to .gitignore; rename a byte-identical copy over .gitignore and over graft/.cache/ask-index.json;
    unlink .gitignore; chmod .gitignore; create a file in graft/ and in .git/ (identical copies, so even a wrongly
    permitted replacement would leave the bytes unchanged, and the run is halted anyway);
  - permitted (positive control): create, replace by rename, and remove a new root file.
"""
import os, sys, stat, errno
from pathlib import Path

POSITIVE = ".lock_positive_control"


def entries(dest):
    """Every pre-existing entry under DEST except DEST itself, children before parents; never descends into .venv."""
    out = []
    for root, dirs, files in os.walk(dest, topdown=False, followlinks=False):
        r = Path(root)
        if r != dest and r.relative_to(dest).parts[0] == ".venv":
            continue
        for name in files + dirs:
            p = r / name
            if r == dest and name == ".venv":
                out.append(p)           # the symlink entry itself
                continue
            out.append(p)
    return out


def freeze(paths):
    for p in paths:
        flags = os.lstat(p).st_flags
        os.chflags(p, flags | stat.UF_IMMUTABLE, follow_symlinks=False)


def refused(label, fn):
    """True when the operation raises a permission error, as a frozen entry must."""
    try:
        fn()
    except OSError as e:
        if e.errno in (errno.EPERM, errno.EACCES):
            return None
        return f"{label}: unexpected {type(e).__name__} {e}"
    return f"{label}: SUCCEEDED (lock not effective)"


def probes(dest):
    misses = []
    gi = dest / ".gitignore"
    gi_bytes = gi.read_bytes()

    def copy_then_rename(src_bytes, target):
        tmp = dest / ".lock_probe_tmp"
        tmp.write_bytes(src_bytes)
        try:
            os.rename(tmp, target)
        finally:
            if tmp.exists():
                tmp.unlink()

    checks = [
        ("append .gitignore", lambda: open(gi, "a").close()),
        ("rename over .gitignore", lambda: copy_then_rename(gi_bytes, gi)),
        ("unlink .gitignore", lambda: os.unlink(gi)),
        ("chmod .gitignore", lambda: os.chmod(gi, stat.S_IMODE(os.lstat(gi).st_mode) ^ stat.S_IWUSR)),   # always a real change (Codex lock review round 2)
        ("create in .git", lambda: (dest / ".git" / ".lock_probe").write_text("x")),
    ]
    cache_file = dest / "graft" / ".cache" / "ask-index.json"
    if cache_file.is_file():
        checks.append(("rename over graft/.cache/ask-index.json", lambda: copy_then_rename(cache_file.read_bytes(), cache_file)))
    if (dest / "graft").is_dir():
        checks.append(("create in graft", lambda: (dest / "graft" / ".lock_probe").write_text("x")))
    for label, fn in checks:
        miss = refused(label, fn)
        if miss:
            misses.append(miss)
    # positive control: a NEW root file can be created, replaced by rename, and removed
    try:
        a, b = dest / POSITIVE, dest / (POSITIVE + ".tmp")
        a.write_text("1"); b.write_text("2"); os.rename(b, a)
        if a.read_text() != "2":
            misses.append("positive control: replacement did not take effect")
        a.unlink()
    except OSError as e:
        misses.append(f"positive control failed: {type(e).__name__} {e}")
    return misses


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: lock_clone.py <DEST>")
    dest = Path(sys.argv[1]).resolve()
    if not (dest / "replay_setup.json").is_file():
        sys.exit(f"REFUSED: {dest} has no replay_setup.json (run setup_replay.sh first)")
    paths = entries(dest)
    freeze(paths)
    unflagged = [str(p.relative_to(dest)) for p in paths if not os.lstat(p).st_flags & stat.UF_IMMUTABLE]
    misses = probes(dest)
    if unflagged or misses:
        print(f"LOCK FAILED: unflagged {unflagged[:10]} ({len(unflagged)}); probes {misses}")
        sys.exit(2)
    print(f"LOCK PASS: {len(paths)} pre-existing entries immutable (incl. .git and the .venv link entry); "
          f"root replacement, unlink, chmod and nested writes refused; new root files still work")


if __name__ == "__main__":
    main()
