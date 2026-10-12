# D-C10r-exp2ctl replay-clone lock review

**Verdict: FIX-FIRST.** The v3.1 replay can run with the proposed permissions on a fresh clone. However, the lock does not establish its stated protection against replacement: existing files at DEST root can still be unlinked or replaced through the writable parent, and the Git baseline remains writable. Fix those gaps before treating `LOCK PASS` as a frozen-clone guarantee.

Review only: no model, GPU, lock invocation, tokenizer precheck, or replay was run. Git observations below used `/usr/bin/git` with `GIT_OPTIONAL_LOCKS=0`. The spent `_r2` clone was inspected without changing it; it is not a rerun destination.

## 1. Post-lock writes and compatibility

The relevant distinction is whether a path exists **when the lock runs**. Files and directories subsequently created by the replay retain their ordinary writable permissions; `lock_clone.py` does not continuously relock them.

| Step | Writes, replacements, or removals inside DEST | Would the proposed lock break the stated fresh-clone procedure? |
|---|---|---|
| Setup | Creates the checkout and `.venv` link; patches `edit.py`; writes `replay_diff.txt`, `replay_diff.sha256`, and `replay_setup.json`. | No: all occur before locking. See `setup_replay.sh:16–36`. Setup must not be repeated against the locked clone. |
| Tokenizer precheck | Writes `tokenizer_precheck.json.tmp`, then renames it to `tokenizer_precheck.json`. On a recheck, unlinks the previous pass record first. | No: the first record is absent at lock time, and DEST stays writable. Even a previously locked pass record can be unlinked through that writable parent. See `tokenizer_precheck.py:78–95`. It does not replace a source or setup record. |
| Runner | Creates `replay_launch.json`, then replaces it through a `.tmp` file after dispatch; creates `run.log`, `run.pid`, `fingerprint.log`, `preflight.log`, and `process_exclusion.jsonl`; appends process observations; unlinks its PID file; creates and later replaces `runner_receipt.json`; creates `reader.log` and `run.rc`. Failure before dispatch can remove newly reserved files. | No: these paths must be absent before dispatch and are created after locking. Root-level temporary-file replacement is explicitly required. See `run_replay.sh:29–31,45–48,69–70,150–166,191–201,217–231`. |
| Recipe and editor runtime | `prepare.py` writes and removes `.hparams_<PID>.json` at DEST root. `evaluate()` creates `runs/<timestamp>_<commit>/`, writes three arm `.pt` files and `edits.json`. The frozen patch appends three arm records to that run's `replay_provenance.jsonl`. | No: all are created after locking. References: `92acd03:prepare.py:111–119,190–223`; patch `read_replay.py:163–169` (realized `_r2/edit.py:210–211`). The existing recipe, scorer, and setup files are only read. |
| Scorer (`prepare.py --score`) | Creates `score.json` in the new run directory, then removes the three existing arm `.pt` files. | No: those existing weight files and their directory were created after the lock. See `92acd03:prepare.py:238–245,249–295`. |
| Reader | Reads source, setup/launch/receipt files, score/provenance/process records, tokenizer data, and fidelity inputs; prints its report. Its stdout destination is opened by the runner. | No: the reader itself has no filesystem write/chmod operation. See `read_replay.py:243–294,559–730`. |

No reviewed replay path writes `results.tsv` or `prepare.log`; those names are not present in the pinned tracked tree. Nothing in the replay writes under `graft/`. The runner exports `PYTHONDONTWRITEBYTECODE=1` and uses `-B`, inherited by the editor/scorer, so it does not need to create DEST's `__pycache__`. The precheck's sibling Python imports reside in the program worktree, not DEST. The imported harness changes cwd to the program's engine directory and directs model/cache access outside DEST (`c10e_bandknob.py:1–8,45–48`).

**Answer:** no post-lock step needs to mutate a file or subdirectory that the stated fresh setup has already locked. Some steps do mutate existing files created later in the same invocation; those are not locked. Do not rerun the recursive lock after runtime outputs have been created.

## 2. File modes and Git

Only the lock's own `writable_left()` checks Unix write bits (`lock_clone.py:38–47`). The frozen-checkout and fidelity checks compare source bytes, Git state/diffs, hashes, paths, and runtime identities; they do not require source mode 0644 (`read_replay.py:243–294`). Setup checks interpreter executability outside the locked file set.

**Confirmed empirically:** `/usr/bin/git ls-tree -r 92acd0378d23f4935df9a8bccc0137b36695a40f` lists **16 tracked files, all mode 100644**. The spent `_r2` has **19 regular files at 0444 and three subdirectories at 0555**, excluding `.git` and the `.venv` symlink. Its `core.filemode` is `true`. `/usr/bin/git diff --raw HEAD --` reports `100644 100644` on every changed file, and `git diff --summary HEAD --` is empty. Thus removing write bits does not produce a tracked mode change or alter the permitted patch diff.

The `_r2` diff still includes five changed graft files in addition to `edit.py`; those are content changes, not permission changes. Locking does not repair an already invalid checkout. Use the new `_r3` from the brief.

The conclusion is specific to this pinned tree: setting an executable tracked file to 0444 would remove an executable bit that Git can track. There are no such files here.

## 3. Skips and missed writer paths

**Root replacement is the blocking gap.** `lock_clone.py:8–13` claims a writer cannot replace a tracked file by rename, but `lock():33–34` deliberately leaves DEST writable. Rename/unlink authorization depends on the parent directory; 0444 protects an inode's contents, not its directory entry. An ordinary same-user writer outside this review sandbox can create a root temporary file and replace `.gitignore`, `.ignore`, `edit.py`, `prepare.py`, or a setup record with it. It can also rename the root `graft` directory away and create a replacement directory. The precheck and runner's legitimate `.tmp` replacements demonstrate that this root capability is required by the current layout.

Observed `_r2` filesystem state: DEST is 0755, owned by uid 501, as are its locked source files; their immutable flags are zero. `ls -ledO` shows no extra ACL protection on the inspected entries. This managed review sandbox separately denies writes to `_r2`, so a failed write from this session would not prove the host lock works. No destructive replacement probe was performed.

The current probes test append-open on `.gitignore` and creation inside `graft/.cache`, not root replacement or chmod. They support the two narrow permissions checks, not the broader guarantee. The inspected Graft implementation directly rewrites root ignore files and writes its graph/cache data, so the proposed modes address those known default write shapes. A same-owner process can also undo ordinary chmod permissions; they are not an immutable snapshot.

**`.git`: operationally unnecessary to leave writable; incompletely protected.** The replay uses read operations (`rev-parse`, `ls-tree`, `show`, and `diff`), not commits/checkouts. Skipping `.git` is compatible with execution, but leaves its config, index, HEAD, objects, and replacement refs mutable. That matters because `inspect_replay()` obtains its expected source from Git. A custom Graft `--dir` under `.git` would also remain writable. I found no default `.git` writer in the inspected Graft paths; the custom path is a capability, not an observed cause of the previous failures.

**`.venv`: skip the target, protect the link entry.** Traversing its shared runtime target would risk removing interpreter executability or changing a runtime used elsewhere. The runner correctly verifies the resolved runtime (`run_replay.sh:124`). However, DEST's writable root also permits replacement of the symlink itself. Protecting that entry must not follow the link or modify the shared virtual environment. Runtime-target immutability remains outside this clone lock's scope.

## 4. Exact fixes and acceptance

For this macOS rerun, retain writable DEST and its future outputs, but make the **pre-existing snapshot entries** immutable:

1. In `lock_clone.py`, apply macOS `UF_IMMUTABLE` (`uchg`) to existing regular files and subdirectories, including the root source/setup files and `graft` directory entry. Apply directory flags after processing their children. Preserve existing flags, and fail clearly if the filesystem refuses them. The relevant operation is:

   ```python
   os.chflags(path, os.lstat(path).st_flags | stat.UF_IMMUTABLE,
              follow_symlinks=False)
   ```

2. Remove `.git` from the traversal exclusion and protect its existing files/directories too. Set `GIT_OPTIONAL_LOCKS=0` for the setup audit/precheck/runner/reader's read-only Git operations so optional index refreshes are not attempted against frozen metadata. Leave DEST itself and paths created after locking writable.
3. Continue to avoid traversing `.venv`, but protect the symlink entry with the same no-follow flag operation. Do not change the target's files or modes.
4. Extend the lock check to verify immutable flags and test root replacement/unlink/chmod and nested-cache replacement against disposable canaries seeded before locking. Require a positive control showing that a new ordinary root output can still be created, replaced, and removed. Run those checks as the actual host runner user, without this review sandbox's independent write denial. A failed protection or positive-control check must halt before precheck/dispatch.

Then require the fresh clone's frozen audit to remain exactly the setup audit; run the brief's precheck and dispatch sequence once. Do not relax the frozen-source check, remove tracked graft artifacts, or change the frozen recipe/scorer to accommodate the lock.

`uchg` protects against ordinary incidental writers, including direct writes and atomic replacement; the owning user can deliberately clear it. This fix is not a security boundary against a process intentionally undoing protections. Its filesystem behavior and replay compatibility need the above no-model acceptance checks before a GPU run; they were not exercised in this review.
