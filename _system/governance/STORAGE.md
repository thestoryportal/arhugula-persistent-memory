# STORAGE — the three disk tiers and the deletion rules
Job: where bulk data lives, the disk-budget rule before any bulk write, and what may never be deleted.
Routed from the root `CLAUDE.md` (twin: `AGENTS.md`). Moved verbatim from the pre-v2 `CLAUDE.md`.

## Storage discipline (three tiers; HARD)

- **memit is a workbench, not a warehouse** (operator policy 2026-10-09, `program/runbook/` §3.3a — live status and how-to there). *Git* holds every science record: JSON, manifests, hashes, `evidence/CORPUS/`, code, the vendored engine. The *`memit` volume* (`/Volumes/memit/llm-database-poc-mirror`) is the hot working tier: bulk sits on the bench only while an analysis needs it. *Google Drive* (rclone remote `gdrive:`, authorized 2026-10-10; setup/re-auth `_system/memory/gdrive-rclone-remote.md`) is the warehouse — irreplaceable bulk and the memit backup. The Mac's internal SSD is **not** an archive tier, and the `Development`/`backups` volumes share memit's physical disk.
- **A full bench fails silently and kills someone else's job.** The C10Y pre-cast wrote 105 GB of float64 packets, filled memit, and killed ASTRA attempt 4's start; parking it on `~/Backups` was then ruled "not acceptable" by the operator. When you hear yourself think *"write the packets now, sort out space later"* or *"just park it on the internal SSD for now — it has room"* — that is the moment. It has room; it is still not an archive. Instead: every scope states a disk budget (bytes/packet × count), every dispatch waits for free ≥ projected writes + 20 GiB, irreplaceable bulk goes to Drive with its SHA-256s committed, and regenerable bulk is deleted — with operator approval — once its reading is confirmed (hashes in git first).
- **Close what you open.** When a lane or worktree closes, delete it locally and remotely (worktree and branch). Do the same for failed setups, probes, runs, and tmp or scratch dirs that no work still reads. At every close of work that wrote files, MAESTRO checks free space and the places that work wrote (growth locations: `program/runbook/` §3.3b). If space is still held, trace the source at once. The T330 prober left a full 5.7 GB clone in its review folder; memit fell under the 20 GiB floor and the re-ship stopped. Nothing failed loudly. When you think *"the ticket is closed, its work dir can wait"*, that is the moment: remove it now, or name the reader that still needs it. Send storage sweeps to a Sonnet or Haiku 5.5 subagent.
- **A tool that makes clones, temp dirs or documents** writes the minimum it needs (a sparse clone, not a full one), to a path it prints, and removes that output itself when nothing reads it. A `mktemp -d` with no cleanup is a defect: record it as a Known gap in `TICKETS.md` and fix the tool.
- **NEVER** delete `evidence/CORPUS/`, `_system/memory/`, the engine, the active model line, or any reproducibility manifest; **NEVER** overwrite a manifest in place; **NEVER** pristine-restore the engine without explicit instruction. These are deny-listed → if you believe one is needed, HALT and record the need for operator action.
  - **Science data comes first and is removed last.** Results, runs, manifests, notebooks, model payloads, covariance and dataset caches have provenance and priority over all other data. Never remove any of it without explicit operator approval for that exact path. In a pruning batch, science goes last.
  - **Reclaim eligibility is not execution permission.** The §3.3 reclaim candidates (superseded non-Qwen model/cov caches, halted-experiment artifacts) and §3.3a regenerable bulk may be *proposed* for deletion without a HALT, but each deletion runs only after explicit approval: verify contents, size and committed hashes; ask the operator naming the exact path, size and the `python3 shutil.rmtree` method; on Yes, assert the target, delete exactly that path, and verify removal (`_system/memory/approved-deletes-ask-then-rmtree.md` — Bash `rm` is deny-listed).
  - **Removal order.** (1) Preserve: copy unique scripts and artifacts that matter to the work into their ICM home. (2) Extract: copy observability and trace data (logs, timings, ledgers, receipts) that exists nowhere else. (3) Remove regenerable non-science. (4) Science last. Record each removal in a ledger. Provenance and the first audit: `knowledge/analyses/storage-audit-20261017.md`.
- Write big canonical docs via shell/python and **re-read after an intervening operation**: on the RunPod FUSE volume, Edit-tool writes silently reverted (2026-06-18, `_system/memory/verify-canonical-state-edits-persist.md`); recurrence on the local memit volume is UNVERIFIED, so the habit stays.

## ICM placement and preservation

Inventory each source before a move. Include ignored and untracked files.
Record source path, byte count, digest, Git state, object kind and destination.
Record symlink text and hard-link relationships. Do not follow links silently.
Record nested Git roots, branch tips and dirty files.
Stop writers that can change the batch. Recheck the source before execution.
Stop on a changed hash, destination collision, root escape or ambiguous link.
Never overwrite an existing destination.
Preserve whole experiment and sweep units.
Keep scientific records in Git regardless of size or former ignore status.
Scientific check and launch JSON, manifests, notebooks and used logs are records.
Scientific notebook checkpoints are versions, not private runtime.
Compare and preserve them with their experiment provenance.
Ignored bulk is limited to attested regenerable non-record output.
Do not route scientific records into bulk. Verify Git durability after placement.
An equal file is a comparison result. It is not deletion permission.
Keep old copies and ignored leftovers until every file has a custody record.
A file found only inside a removal target is preserved before the removal (see Removal order).
Move unmatched old copies to an approved external preservation location.
Do not install a full old repo copy inside the canonical repo.
Promote unique files only after their owner and destination are approved.
Repair references in a separate approved batch.
Record the old and new paths, before and after digests, checks and rollback.
This refinement uses inventory, preserve and move. Never delete in this arc.
Any later purge requires its own accepted plan and approval.

## Models

Store each model under `models/<model-name>/`.
Use the identity in its source manifest to select the directory name.
Keep base payloads under `base/<format>/`.
Keep edited payloads under `variants/<variant>/<format>/`.
Keep model provenance under `manifests/`.
Record upstream identity, revision, format, size, digest and license source.
Record each variant's base digest and the experiment that produced it.
A model CONTEXT.md links to the active variant and its source manifests.
Keep weight bytes ignored. Track their small identity and custody records.
Route research, raw runs, findings and evidence to their ICM homes.
Link to them from the model guide. Do not store copies beside the weights.
Keep covariance and datasets under data with an explicit model binding.
Preserve cache layouts until their readers can use the new model location.
A locator must name the exact payload and digest. It must not create a second authority.
Check all model readers and manifests before changing a model path.
Protect the active model line. Do not delete a model during this refinement.
