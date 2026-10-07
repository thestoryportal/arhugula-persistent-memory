# D-C10r-exp2ctl clone lock — round 2

**Verdict: FIX-FIRST — one probe correction.** V2 closes the round-1 protection gaps and preserves the replay's required write paths. However, its chmod probe assumes the spent clone's 0444 mode. Make that probe request an actual mode change before using it to accept or reject a fresh clone.

Reviewed `lock_clone.py` SHA256 `24e377ce1598b46999f315e4fd91eda26ff5ae0f545bb71a17aef130ace73db5`, the round-1 review, and the replay driver/pinned scorer. Review only: no freeze/probes, tokenizer precheck, model, GPU, or replay was run. Read-only Git commands used `/usr/bin/git` with `GIT_OPTIONAL_LOCKS=0`.

## Blocking finding: fresh-clone chmod probe can be a no-op

At `lock_clone.py:80`, the probe is:

```python
("chmod .gitignore", lambda: os.chmod(gi, 0o644)),
```

The spent `_r2` still has `.gitignore` mode **0444** from v1; I independently checked it. That probe therefore requests a real change there. V2's `freeze()` sets flags but does not change permissions (`lock_clone.py:45–48`). A normal fresh checkout of this tracked 100644 file has mode **0644**, making the same probe request its existing mode.

A successful no-op is not evidence that immutability failed, but `refused()` labels every successful call `SUCCEEDED (lock not effective)` and makes `main()` exit 2. Apple's XNU `vnode_authattr()` requests the mode-change authorization only when old and requested modes differ, so refusal of an unchanged mode is not an acceptance invariant to rely on. [Apple XNU mode authorization](https://github.com/apple-oss-distributions/xnu/blob/main/bsd/vfs/vfs_subr.c#L10359-L10374).

**Inference:** the reported `_r2` PASS does not establish that this probe accepts a correctly frozen fresh 0644 checkout. No fresh-clone chmod operation was executed in this review.

**Exact fix:** replace the line with a request that toggles the owner's write bit:

```python
("chmod .gitignore", lambda: os.chmod(
    gi, stat.S_IMODE(os.lstat(gi).st_mode) ^ stat.S_IWUSR)),
```

This requests 0444 → 0644 on the spent clone and 0644 → 0444 on a fresh clone. It always changes a permission bit, preserves the other bits, and retains the existing permission-error requirement. Do not accept successful actual chmod or weaken `refused()`.

## Round-1 items resolved

| Item | V2 assessment |
|---|---|
| Root-file replacement and root directory-entry replacement | Resolved for incidental writers: existing files and directory entries receive `UF_IMMUTABLE`, while DEST remains unflagged (`29–48`). Root writability no longer permits replacing a protected entry merely through parent permissions. |
| Children before directories; complete coverage | Confirmed with the pure `entries()` function: **69 unique paths**, matching the live tree, with every included child before its parent and DEST excluded. No freeze/probe function was invoked. |
| Writable Git baseline | Resolved: `.git` and its existing descendants are included. Independent `lstat` checks found **all 69 entries flagged**, including `.git`, config, index, HEAD, graft directories/cache, and setup/source files. |
| Runtime symlink | Resolved: `.venv` itself is included and `chflags(..., follow_symlinks=False)` protects its entry. Traversal does not enter its target; the target directory remains unflagged. |
| Replacement, unlink, nested writes, and positive control | Implemented at `62–100`: byte-identical replacement attempts, unlink, append-open, creation in `.git`/`graft`, and creation/replacement/content-check/removal of new root output. Probe temporaries are cleaned after refused renames. The chmod test needs the correction above. |
| Failure handling | Unflagged entries or probe misses prevent `LOCK PASS` and exit 2 (`110–118`). A flag-setting exception also stops execution rather than silently proceeding. |

The reported 69-entry dry-run PASS is operator-supplied evidence; I independently confirmed the resulting flags and absence of residual probe files, without repeating the write probes. `_r2` remains content-invalid from its earlier graft changes and must not be the rerun destination.

## Replay compatibility and Git

All required post-lock outputs remain **new, unflagged entries**: the tokenizer pass record and its temporary file (`tokenizer_precheck.py:82–95`); runner receipts, logs, PID/exit/process records and their replacements/removals (`run_replay.sh:45–48,150–166,191–231`); root `.hparams_<PID>.json`; and new `runs/<timestamp>_<commit>/` weights, manifest, provenance, and score. Scorer removal of arm weights operates on files created after locking (`92acd03:prepare.py:111–119,190–223,292–295`; patch `read_replay.py:163–169`). No required write targets a pre-existing frozen source/setup/Git/graft entry. Do not run the lock again after precheck or output creation.

I successfully read HEAD/tree/scorer and ran raw/summary diffs against the immutable `.git`. The pinned tree still has 16 files at 100644; raw diffs retain `100644 100644`, and the mode-change summary is empty. V2 does not chmod snapshot files, and the source/fidelity checks do not compare BSD immutable flags.

The stated wrapper export of `GIT_OPTIONAL_LOCKS=0` is sufficient: the precheck's Git subprocesses inherit it; the runner/editor/scorer/reader preserve `os.environ` when constructing child environments (`run_replay.sh:129,154,157,222`; `92acd03:prepare.py:222`). The wrapper itself was not supplied for inspection, so this assessment uses the operator's stated invocation requirement.

**After the one-line correction:** proceed with fresh `_r3` setup → v2 lock/acceptance → tokenizer precheck → replay, keeping `GIT_OPTIONAL_LOCKS=0` exported throughout the post-lock window. Require that clone's own `LOCK PASS` and existing frozen-source/precheck gates before dispatch. No recipe, scorer, pass criterion, or frozen-diff relaxation is needed. The scope remains protection from incidental writers; an owner deliberately clearing `uchg` is outside it.
