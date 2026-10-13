# Science reservation contract v3 — the pending-science signal

Author: MAESTRO35 (reservation owner), 2026-10-11. Supersedes SR v2 (unchanged) after Astra spec r4 NO-GO (`astra_spec_r4_verdict.md`, U1–U8). Binds `phase1_spec_v5.md` AC17, AC21, §3, §10, §11, §13. Operator-approved shape (`operator_answers_20261011T0518Z.md`): a note before a science run waits, removed when it ends; the research engine (RE) is gone within 30 s; science gates unchanged. Proposed; not built.

**Design change from v2.** R1 (`astra_spec_r1_verdict.md:17`) requires refusal while science is pending, and, on newly pending science, cancellation and termination of owned RE Python and Neo4j within the shutdown bound, with no waiting Python watcher. It does not require the RE to observe. v3 therefore has **one enforcer, on the science side**: `pending` itself terminates the RE and confirms that it is gone. The v2 watcher, controller thread, heartbeat and registry are removed, and with them the leader-identity (U1) and startup/registry (U4) failure surfaces. RE publication stays lock-ordered, so cancellation before publication needs no observer.

## 0. Guarantees and premises

- **G1 (ordering):** RE admission and every RE publication check the state while holding `<root>/lock` (§3). After a `pending` publish, the RE can no longer admit or publish.
- **G2 (yield):** a `pending` invocation returns within **30 s of its start** (one origin, one terminal deadline, §4). Exit 0 means published, then confirmed by a process inventory taken **after** the publish that no RE-owned process is alive. Any other outcome by the deadline is exit 3 (HALT: do not launch). The coordinator starts only after exit 0, so no RE process coexists with dispatched science. The RE adds at most 30 s to a launch.
- **G3 (no false idle):** no failure (crash, partial write, unreadable state, hung command, clock change, unmounted volume) yields IDLE (§2, §5).
- **P-coop (cooperative premise, not enforced):** every science launch runs `pending` first and `release` only through §3. The existing gates (`tools/c10w_p2_gate.py`, `tools/run_c10v_stage.sh`) stay byte-identical and are not substitutes: C10W refuses while RE Python is alive; C10V filters science command patterns and sees neither RE Python nor Java.
- **P-memit:** all science code, models and results live on `/Volumes/memit`. If memit is gone, no science can launch, so the writer living on memit (`tools/science_reservation.sh`) adds no failure mode that matters to science.

## 1. Authority, files, owners

- Root (constant): `/Volumes/memit/llm-database-poc-mirror/science_reservations/`, outside every worktree.
- `<root>/AUTHORITY`: exact bytes `llmdb-science-reservations v3\n` (30 bytes).
- `<root>/active/`: one entry per pending or running launch. `<root>/log/`: released entries, never read for admission.
- `<root>/lock`: the shared lock file. `/usr/bin/lockf -k` (sh) and `fcntl.flock` (Python) exclude each other on this APFS volume (probe 2026-10-11 05:19Z, both directions).
- **Sole writer:** `tools/science_reservation.sh`, run as `/bin/sh tools/science_reservation.sh <verb> …`. The RE never writes under `<root>`; it only takes and releases the lock.
- **Reservation owner:** MAESTRO. A builder launches science only from a brief that names the writer steps.
- **Covered coordinators:** `tools/run_c10w_p2.sh`, `tools/run_c10v_stage.sh`, `tools/mathlab_admit.py` admissions, `tools/new1_supervisor.py`/`tools/new1_dispatch.sh`, `tools/run_c10z_v7_diag.py`, `experiments/track_c/autoresearch_c10/v13_launcher.py`, and any launch that loads a model or uses MPS. Adding one means a new contract version.
- **Inputs (validated before any mutation; a violation exits 2 with nothing written):** `launch_id` matches `^[A-Za-z0-9_.-]{1,64}$`. `coordinator` is one of the covered paths, or `commission` (§7 only). Entry schema, one `key=value` per line, in this order: `schema=3`, `launch_id`, `coordinator`, `owner`, `state=pending|running`, `tokens=` (space-separated argv tokens, §3 `running`), `created_utc`, `updated_utc`. UTC values are for humans only.

## 2. RE ownership (inventory-based)

An RE process is any process in `/bin/ps -axww -o pid=,lstart=,command=` whose command matches one of two frozen, anchored patterns:
- Python: `^<W>/.venv-research-engine/bin/python -I -B <W>/tools/research_engine/cli\.py( .*)? --llmdb-re-session=[0-9a-f]{16}( .*)?$`
- Neo4j JVM: `^/opt/homebrew/(Cellar/openjdk@21/21\.0\.12\.1|opt/openjdk@21)/\S*/bin/java .* -Dllmdb\.re\.session=[0-9a-f]{16}( .*)?$` (set through `server.jvm.additional` in the session's `neo4j.conf`).

`<W>` is the absolute worktree path, frozen at freeze. Every RE process carries its session token in that exact form, and the RE spawns nothing else. Ownership holds without any living parent, registry or memit file. Provisioning smoke (v5 §13) must show the running JVM's command line matching the pattern; otherwise provisioning stops and this contract is revised.

Do NOT match on the bare token anywhere in a command line: Codex and Claude processes carry whole briefs in argv, and a brief that mentions the token would be killed. Before signalling a PID, the writer re-reads `ps -p <pid> -o lstart=,command=` and signals only if both still match the inventory row. The remaining reuse window, between that re-read and the signal, is sub-millisecond; it is recorded as a residual, not claimed away.

## 3. States, lock and verbs

State, decided only while holding the lock (RE admission and publication; writer verbs):

| State | Condition |
|---|---|
| UNAVAILABLE → code4 | root missing/unreadable; marker not exactly the 30 bytes; `active/` missing, not a directory or not listable; lock not obtained within 1 s (RE) or 2 s (writer); any command killed by its 2 s cap. |
| SCIENCE → code5 `SCIENCE_PRIORITY` | `ls -A <root>/active/` exits 0 with any output (entry, `.tmp.*`, dotfile, directory, malformed file). |
| IDLE | marker exact; `active/` listed with exit 0 and empty output. |

RE admission additionally requires, under the lock, a clear exclusion check (§3a). RE publication (pointer rename) requires IDLE under the lock and nothing else. The RE holds the lock at most 1 s, with bulk fsync done before taking it.

Do NOT: glob `active/*`; parse entries to decide state; skip old or unparseable entries; treat a missing directory or a timed-out listing as empty; compare wall-clock times.

**§3a exclusion check** (one inventory, taken under the lock): clear when (i) `blocking_processes` and `blocking_tmux`, imported unchanged from `tools/c10w_p2_gate.py` and run by `/usr/bin/python3 -I`, report nothing other than RE-owned PIDs; (ii) no command contains a covered coordinator path as a fixed string. An empty inventory or a probe failure is not clear.

Verbs (`lockf -k -t 2 <root>/lock`; every mutation inside the lock is `set -C` create of `active/.tmp.<launch_id>.<writer_pid>`, `mv`, `/bin/sync`, each capped at 2 s):
- `pending <launch_id> <coordinator>` — §4.
- `running <launch_id> <coordinator_pid> [token…]`: rewrite the entry with `state=running` and `tokens` = the coordinator's script path plus every given argv token that identifies the launch's descendants (for `v13_launcher.py`, the child `--session-id` value, `v13_launcher.py:22`).
- `release <launch_id>`: under the lock, require (a) no process whose command contains any of the entry's `tokens`, (b) the coordinator PID with its recorded `lstart` absent, (c) a clear §3a(i) classifier, all from one inventory taken under the lock. Then `mv` the entry to `log/<launch_id>.<utc>`. Otherwise exit 3 and the entry stays. This catches surviving descendants started in new sessions (`new1_supervisor.py:532`, `v13_launcher.py:47,87`): every process that can dispatch science compute is either a covered coordinator (matched by path or token) or a compute executable (matched by the classifier). An error only keeps the reservation, which only delays the RE.

## 4. `pending` (the single enforcer)

1. At invocation, before anything else, start the deadline timer: a background `sleep 30` that, when it fires, kills the working subshell, writes `HALT deadline` to the receipt and makes the verb exit 3. All other waits are relative `sleep`s or 2 s-capped commands.
2. Validate inputs (§1); on failure exit 2.
3. Take the lock (`-t 2`). Got it: refuse with exit 2 if `active/<launch_id>` exists, else publish; release the lock. Not got: go to step 4 first, then retake the lock (`-t 2`) and publish; a second failure is exit 3 (HALT, nothing published). If the root is unusable, skip publishing and record UNAVAILABLE.
4. Enforcement loop, once per second: one capped inventory; TERM each RE-owned PID (§2 re-check) not yet signalled; from invocation +20 s, KILL each remaining RE-owned PID.
5. Finish when an inventory taken **after** the publish (or after the UNAVAILABLE record) shows zero RE-owned processes. Exit 0 if published; exit 4 if the root was unusable ("RE blocked; science may proceed after MAESTRO records this receipt"). Otherwise the deadline fires: exit 3, and the entry stays if it was published.
6. Receipt to stdout and `<root>/log/pending.<launch_id>.<utc>.txt` (or stdout only if the root is unusable): every inventory's RE rows, signals with time offsets from invocation, outcome.

A new RE admitted in the lock-timeout window (between step 4's kills and the publish) is found by the post-publish inventory in step 5 and terminated, and it cannot publish (G1). RE SIGTERM handlers persist diagnostics and halt without publishing; Neo4j shuts down on its own TERM. No `neo4j stop` or other unbounded command is used.

## 5. Time and failure rules

- Decisions use relative `sleep`s and command caps only; G2's single origin is invocation. Wall-clock jumps change nothing.
- Every external command is capped at 2 s (background `sleep 2; kill -KILL`); a capped-out command is a failure, never an empty result.
- RE: a lock wait over 1 s, or any state-check failure, means code4 refusal or abort before publication.

## 6. Frozen AC17/AC21 cases

Fixtures use a temp root, a fake `ps`/`ls` (able to hang), an injectable inventory and a fake clock, all through test-only parameters; the production root and patterns are constants.
1. Valid IDLE plus clear §3a at start → admitted (positive control).
2. Pending at start → code5. 3. Running at start → code5.
4. Two launches; release one → SCIENCE; release both → IDLE.
5. Race: the RE paused inside its lock-held admission, then inside publication; a concurrent `pending` blocks on the lock; the RE step completes first or sees SCIENCE. None completes after the publish.
6. IDLE → pending during work → exit 0 only after a post-publish inventory shows no RE process; elapsed ≤30 s from invocation.
7. Lock-timeout path: a stuck holder → enforcement → a new RE admitted before the publish → terminated before exit 0.
8. Leader exits first; an orphan JVM-pattern child ignores TERM → KILL from +20 s → exit 0 (no leader needed).
9. Non-RE process whose argv contains the token text in another form (a brief) → never signalled.
10. `lstart` changed between inventory and signal → not signalled; recorded.
11. Hanging `ps`/`ls` → capped; persistent hang → deadline → exit 3 by 30 s.
12. Unusable root (marker wrong, `active/` a file, root renamed) → enforcement still runs; exit 4 only with a clean post-check inventory, else exit 3.
13. Malformed, `.tmp.*`, dotfile and subdirectory entries → SCIENCE.
14. Concurrent duplicate `pending` with one `launch_id` → exactly one publishes; the other exits 2.
15. Invalid `launch_id`/`coordinator` → exit 2, nothing written.
16. Writer killed after tmp create, after `mv` and before `sync`, after `sync` → never IDLE; state is SCIENCE until released.
17. `release` with a surviving descendant matching a token (new-session child, v13 `--session-id` child) → exit 3, entry kept; dead coordinator but live classifier hit → exit 3.
18. Clock jumps ±1 h → no outcome changes.

## 7. Commissioning gate (before Astra promote)

After BUILD1 GREEN and MAESTRO's fixture verification:
1. Choose a window with no science pending.
2. MAESTRO creates `<root>` (marker, `active/`, `log/`, `lock`). From then on every science launch uses the writer (operator-approved).
3. Start a real RE session (Python plus Neo4j, carrying the §2 patterns). Run `pending commission-<utc> commission`; require exit 0 with a receipt showing the real PIDs terminated, ≤30 s.
4. `release` it, then file the receipts under `P/builds/<id>/commissioning/`.

One attempt. A failure is a HALT; the root stays, and the RE stays blocked because promote is missing. Astra promote reviews these receipts; fixtures cannot replace them.
