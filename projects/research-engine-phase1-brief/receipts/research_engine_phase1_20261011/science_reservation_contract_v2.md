# Science reservation contract v2 — the pending-science signal

Author: MAESTRO35 (reservation owner), 2026-10-11. Supersedes SR v1 (`science_reservation_contract_v1.md`, unchanged) after Astra spec r3 NO-GO (`astra_spec_r3_verdict.md`, T1–T7). Binds `phase1_spec_v4.md` AC17, AC21, §3, §10, §11, §13. Operator approved the step's shape (`operator_answers_20261011T0518Z.md`): a note before a science run waits, removed when it ends; the research engine (RE) is gone within 30 s; science gates unchanged. Proposed; not built.

## 0. Guarantees and premises

- **G1 (ordering):** every RE admission and every RE publication is linearized either before or after each `pending` publication by one shared lock (§3). None happens after a `pending` publication.
- **G2 (yield):** `pending` returns 0 only after it has confirmed that no RE-owned process is alive, at most 28 s after its own publication (§5). The coordinator starts its gate loop only after that return, so no RE process coexists with a dispatched science job. The RE adds at most 28 s to a science launch, plus up to 2 s lock wait (§3). That is the whole delay; a failure beyond it is a HALT (§5), never a longer silent wait.
- **G3 (no false idle):** no failure (crash, partial write, unreadable state, unmounted volume, hung command, clock change) is read as IDLE (§2, §6).
- **Premise P-coop (cooperative, not enforced):** every science launch runs `pending` first. Nothing mechanical forces a coordinator to do so. The existing gates (`tools/c10w_p2_gate.py`, `tools/run_c10v_stage.sh`) stay byte-identical and are not a substitute: C10W refuses while RE Python is alive; C10V filters science command patterns and does not see RE Python or Java. The watcher's coordinator-path backstop (§5) is supplemental and incomplete.

## 1. Authority, files, owners

- **Root (constant):** `/Volumes/memit/llm-database-poc-mirror/science_reservations/`, outside every worktree.
- `<root>/AUTHORITY`: exact bytes `llmdb-science-reservations v2\n` (30 bytes).
- `<root>/active/`: one entry per pending or running launch.
- `<root>/log/`: released entries; never read for admission.
- `<root>/lock`: the shared lock file. Locked with flock semantics: `/usr/bin/lockf -k` (sh) and `fcntl.flock` (Python) exclude each other on this APFS volume (probe 2026-10-11 05:19Z, both directions).
- **RE registry (constant, internal volume):** `/Users/robertrhu/.llmdb-research-engine/sessions/<session_id>/`. Holds `session` (`pgid`, `leader_pid`, `leader_lstart`, `watcher_pid`, `watcher_lstart`, `state=admitted|working|closed`), the watcher's `seq` counter, the internal copy of the watcher, and receipts. It lives off memit so that enforcement survives memit loss. Receipts are copied into `P/builds/<id>/` at session end. Budget ≤10 MB; a runtime registry, not an archive.
- **Sole writer:** `tools/science_reservation.sh`, run as `/bin/sh tools/science_reservation.sh <verb> …`. The RE never writes under `<root>` except to take and release `<root>/lock`.
- **Reservation owner:** MAESTRO; a builder launches science only from a brief that names the writer steps.
- **Covered coordinators:** `tools/run_c10w_p2.sh`, `tools/run_c10v_stage.sh`, `tools/mathlab_admit.py` admissions, `tools/new1_supervisor.py`/`tools/new1_dispatch.sh`, `tools/run_c10z_v7_diag.py`, `experiments/track_c/autoresearch_c10/v13_launcher.py`, and any launch that loads a model or uses MPS. Adding one means a new contract version.

## 2. States (decided by the RE, under the lock for admission and publication)

| State | Condition |
|---|---|
| UNAVAILABLE → code4 | root missing/unreadable; `AUTHORITY` not exactly the 30 bytes; `active/` missing, not a directory, or not listable; lock not obtained within 1 s; any observation command killed by its 2 s cap. |
| SCIENCE → code5 `SCIENCE_PRIORITY` | `ls -A <root>/active/` exits 0 and prints anything: entry, `.tmp.*`, dotfile, directory, malformed or unreadable file. |
| IDLE | marker exact, `active/` listed with exit 0 and empty output. |

Do NOT implement:
- `ls active/*` or any glob (misses dotfiles; in sh an empty glob expands to the literal pattern).
- parsing entries to decide state, or skipping old or unparseable entries.
- treating a missing `active/` as empty, or a timed-out listing as empty.
- reading wall-clock time to decide anything (§6).

## 3. Writer verbs and the lock

Each verb takes `<root>/lock` with `/usr/bin/lockf -k -t 2`. Inside the lock, it creates entries with `set -C` (O_EXCL) at a tmp name unique to the writer PID, then `mv`, then `/bin/sync`. The RE holds the lock only to (a) check the state at admission and record `state=admitted`, and (b) check the state and rename the publication pointer. Both are bounded at 1 s, with all bulk fsync done before the lock is taken.

- `pending <launch_id> <coordinator>`. Under the lock: refuse with exit 2 if `active/<launch_id>` exists; otherwise publish the entry (`state=pending`, coordinator, owner, `created_utc` for humans). Release the lock, then run §5 enforcement. Exit 0 = published and confirmed that no RE process is alive. Exit 3 = published, RE survival UNVERIFIED: HALT, do not launch, the entry stays. Exit 4 = root or lock unusable (below).
- If the lock is not obtained within 2 s: run §5 enforcement first (a dead holder's flock is released by the kernel), then take the lock (`-t 2`) and publish. G1 holds because no RE process remains to admit or publish. The total stays within G2.
- If the root is unusable: run §5 enforcement, then exit 4 with `RE blocked (UNAVAILABLE); science may proceed after MAESTRO records this`. A broken authority blocks the RE, never science.
- `running <launch_id> <coordinator_pid>`: under the lock, rewrite the entry atomically with `state=running`, the pid and its `lstart` (receipt only).
- `release <launch_id>`: refuse with exit 3 while the existing classifier reports anything. That means `blocking_processes` and `blocking_tmux` imported unchanged from `tools/c10w_p2_gate.py`, run once by `/usr/bin/python3 -I` over a `/bin/ps -axww -o pid=,command=` inventory, with an empty inventory or probe failure counting as a refusal. Otherwise, under the lock, `mv` the entry to `log/<launch_id>.<utc>`. This catches surviving children of a dead coordinator, including those started in a new session (`new1_supervisor.py:532`, `v13_launcher.py:47,87`). It errs toward keeping the reservation, which only delays the RE. Stale-entry recovery uses the same verb.

## 4. RE session ordering

1. The launcher copies `tools/research_engine/watch.sh` to the registry, checks its sha256 against the frozen hash, and starts the copy at niceness ≥10. It waits until `seq` has advanced twice.
2. The controller (RE Python, group leader through `os.setsid()`) records `pgid`, `leader_pid` and `leader_lstart`. Every RE process, including Neo4j started as `neo4j console`, is its descendant in that group; the provisioning smoke test confirms the JVM's PGID.
3. Admission under the lock: IDLE, and the classifier (§3) is clear except for RE-owned PIDs. Record `state=admitted`, then release the lock. Otherwise refuse code5/code4 and stop the watcher.
4. Work. Publication only through the locked check-and-rename (§3).

A `pending` publication before step 3 is refused at step 3. A publication after step 3 is cancelled by the watcher and by the writer's enforcement before any further publication, because publication takes the lock and sees SCIENCE.

## 5. Enforcement (non-Python, bounded, two independent paths)

**Writer path (guarantor of G2), inside `pending`.** Right after publishing, start relative timers (`sleep 20`, `sleep 25` in background subshells, which are immune to wall-clock changes). Each second, list every registry session not `closed`. For each live group (leader PID with matching `lstart`), send `kill -TERM -<pgid>`. At +20 s send `kill -KILL -<pgid>`. Confirm absence with `/bin/ps -g <pgid>` (capped at 2 s) by +25 s. Write `pending_receipt.txt` to the registry and stdout. The +25 s confirmation plus lock and publish overheads give the 28 s bound.

**Watcher path (graceful, diagnostic).** `watch.sh` (internal copy, `/bin/sh`). Each poll runs one observation subshell hard-capped at 2 s by a background `sleep 2; kill -KILL` killer, then sleeps 1 s. The observation covers the §2 state, the coordinator-path backstop (fixed strings from §1 over `/bin/ps -axww -o pid=,command=`), and the controller's liveness (`leader_pid` + `lstart`); it then increments `seq`. A trigger is SCIENCE, UNAVAILABLE, a timeout, a backstop hit, or controller loss. On a trigger it sends `kill -TERM -<pgid>`, with KILL at +20 s and confirmation by +25 s on relative timers. It writes `termination_receipt.txt` (reason, entries seen, per-PID signals, confirmed absent, verdict `TERMINATED`/`UNVERIFIED`), then exits. No `neo4j stop` or other unbounded command runs on either path; Neo4j shuts down on its group's TERM.

**Controller path (watcher loss).** A thread in the controller reads `seq` each second on `time.monotonic`. If `seq` doesn't advance for 3 s, the controller sets a stop flag (no new spawns) and terminates its own group except itself, with KILL at +20 s and confirmation by +25 s. It writes the receipt, then exits code4 without publishing. This thread is part of the controller's own process, not a separate waiting process.

**Both die:** orphans stay in the registry. They are harmless until the next `pending`, whose writer path kills them, and the next admission refuses while any registry group is alive.

**Owned-process identity:** signals go to a process group only after the leader's current `lstart` matches the recorded value. Residual risk: the PID could be reused between that check and the signal (a sub-millisecond window). It is recorded in receipts, not claimed away.

## 6. Time and failure rules

- Decisions use relative `sleep` timers, the `seq` counter and `time.monotonic` only. UTC appears in receipts for humans and is never compared.
- Every external command on an enforcement or observation path is capped at 2 s; hitting the cap counts as UNAVAILABLE.
- memit loss: UNAVAILABLE for the RE; the writer and watcher still read the registry from the internal volume; the watcher runs from its internal copy.

## 7. Frozen AC17/AC21 cases

Fixtures use a temp root and a temp registry through test-only parameters; production paths are constants. A fake `ps`/`ls` can hang, and a fake clock can jump.
1. Valid IDLE at start → admitted (positive control).
2. Pending at start → code5. 3. Running at start → code5.
4. Two launches; release one → SCIENCE; release both (classifier clear) → IDLE.
5. Publication race: test hooks pause the RE inside its lock-held admission, then inside publication; a concurrent `pending` blocks on the lock, and the RE's step completes before it or sees SCIENCE. No admission or publication completes after `pending`'s publish.
6. IDLE → pending during work → `pending` exits 0 only after every owned fixture PID is confirmed absent, ≤28 s after its publish; the watcher receipt says `TERMINATED`.
7. Authority loss during work (marker changed, `active/` replaced by a file, root renamed) → code4 halt plus termination; the registry stays readable.
8. Malformed, `.tmp.*`, dotfile and subdirectory entries → SCIENCE.
9. Concurrent duplicate `pending` for one `launch_id` → exactly one exit 0, the other exit 2.
10. Coordinator dead, child alive in a new session → `release` exit 3; the entry stays.
11. Watcher killed during a phase with only a stand-in "Java" child → the controller terminates the group within 25 s. Controller killed → the watcher terminates the group. Both killed → the next `pending` terminates the orphans.
12. Hanging `ps`/`ls` → capped at 2 s → UNAVAILABLE trigger; a hanging child ignoring TERM → KILL at +20 s.
13. Wall clock jumps ±1 h mid-session → no deadline or heartbeat decision changes.
14. Leader `lstart` mismatch → no signal; the receipt records it.
15. Lock held by a stuck RE beyond 2 s → `pending` enforces, then publishes, within G2.

## 8. Commissioning gate (before Astra promote)

After BUILD1 GREEN and MAESTRO's fixture verification, and before promote:
1. Choose a window with no science pending.
2. MAESTRO creates `<root>` (marker, `active/`, `log/`, `lock`). From that moment every science launch uses the writer (operator-approved).
3. Start a real RE session (Python plus Neo4j). Run `pending commission-<utc> none`; require exit 0 with a writer receipt and a watcher `TERMINATED` receipt, ≤28 s.
4. `release` it, then file the receipts under `P/builds/<id>/commissioning/`.

One attempt. A failure is a HALT with the root left in place: the RE stays blocked because promote is missing, and science is unaffected. Astra promote reviews these receipts; a fixture pass cannot replace them.
