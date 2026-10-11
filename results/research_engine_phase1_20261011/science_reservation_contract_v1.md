# Science reservation contract v1 — the pending-science signal

Author: MAESTRO35 (reservation owner), 2026-10-11. Resolves Astra spec r2 S1 / "Required before freeze" (`astra_spec_r2_verdict.md`). Binds `phase1_spec_v3.md` §11, §13, AC17, AC21. Proposed; not built.

## Why this exists

Every science coordinator already refuses to start while any non-exempt Python runs (`tools/c10w_p2_gate.py:73–84`; `tools/run_c10v_stage.sh:7`; `memory_mirror/gpu-gate-refuses-any-venv-python.md`). That gate sees only *running* processes. A science launch spends its *pending* time in a poll-until-clear loop, invisible to anyone. The research engine (RE) must yield during that wait, so the wait needs a published, machine-readable state. This contract adds one: a reservation directory that MAESTRO writes before any science launch starts waiting. Science gates, classifiers and exemptions stay byte-identical.

## 1. Authority and scope

- **Root (frozen constant):** `/Volumes/memit/llm-database-poc-mirror/science_reservations/`. Outside every worktree, so all worktrees and sessions see one state.
- **Marker:** `<root>/AUTHORITY`, exact bytes `llmdb-science-reservations v1\n` (30 bytes). Identity and version of the authority.
- **Active set:** `<root>/active/`. One entry per pending or running science launch.
- **Released log:** `<root>/log/`. Released reservations, append-only, never read for admission.
- **Sole writer:** `tools/science_reservation.sh` (POSIX `/bin/sh`, invoked as `/bin/sh tools/science_reservation.sh …`). It is the only program that creates, rewrites or releases entries. The RE never writes under `<root>`; it cannot suppress, age out or delete a reservation.
- **Reservation owner:** MAESTRO. Every science launch goes through MAESTRO or a brief MAESTRO wrote that names the writer step.
- **Covered coordinators (every one, no exception):** `tools/run_c10w_p2.sh` (+ `tools/c10w_p2_gate.py`), `tools/run_c10v_stage.sh`, `tools/mathlab_admit.py` admissions, `tools/new1_supervisor.py` / `tools/new1_dispatch.sh`, `tools/run_c10z_v7_diag.py`, `experiments/track_c/autoresearch_c10/v13_launcher.py`, and any future launch that loads a model or uses MPS. A launch path not in this list still requires a reservation; adding a coordinator updates this list in a new contract version.

## 2. States

The RE computes exactly one of three states per observation:

| State | Condition (all must hold for IDLE; first failing row decides otherwise) |
|---|---|
| UNAVAILABLE → refuse code4 | root missing/unreadable; `AUTHORITY` missing, unreadable or not the exact 30 bytes; `active/` missing or not listable; the listing command exits non-zero. |
| SCIENCE (pending or running) → refuse/cancel code5 `SCIENCE_PRIORITY` | `active/` lists **any** entry: a well-formed reservation, a `.tmp.*` file, a dotfile, a directory, a malformed or unreadable file. Content is recorded in receipts but never needed to decide. |
| IDLE | marker exact, `active/` listable and empty (`ls -A` prints nothing, exit 0). |

Do NOT implement any of these (each turns a failure into "idle"):
- `ls active/*.json` (a glob that misses dotfiles and tmp files, and in sh expands to the literal pattern when empty).
- treating an unparseable entry as absent, or skipping entries older than N minutes.
- treating a missing `active/` directory as an empty one.

Entry format (written only by the writer; one `key=value` per line): `schema=1`, `launch_id=<[A-Za-z0-9_.-]{1,64}>`, `coordinator=<path from §1>`, `owner=<session name>`, `state=pending|running`, `created_utc=<ISO-8601 Z>`, `updated_utc=<ISO-8601 Z>`.

## 3. Transitions and validity

- `pending <launch_id> <coordinator>`: refuse if `active/<launch_id>` exists. Write `active/.tmp.<launch_id>`, fsync, `mv` to `active/<launch_id>` (same-filesystem rename: atomic). The tmp file is itself non-idle, so publication begins at tmp creation. Run this **before** starting the coordinator's poll-until-clear loop.
- `running <launch_id>`: rewrite the same entry through tmp + `mv` with `state=running`. Run it when the coordinator dispatches.
- `release <launch_id>`: `mv active/<launch_id> log/<launch_id>.<release_utc>`. Run it after the coordinator exits, whether it succeeded or failed, or immediately if the launch is abandoned.
- **Multiple launches:** one entry each; releasing one leaves the others; the state is IDLE only when the set is empty.
- **Freshness:** entries never expire. A stale entry (its launch died) keeps the state SCIENCE until MAESTRO confirms that launch's processes are gone and releases it. Staleness can only block.
- **Restart:** entries persist on memit across reboot and process death. memit unmounted → root missing → UNAVAILABLE.
- **Writer failure:** any writer step that exits non-zero leaves the launch unreserved; MAESTRO does not start the coordinator until `pending` succeeds.

## 4. Ordering (no idle-check race)

RE session start, in this order:
1. Start the watcher (§5) and wait for its first heartbeat.
2. Write the RE's own session record under `P/runtime/control/` (never under `<root>`).
3. Admission check: state IDLE **and** the running-compute backstop (§5) is clear. Else refuse code5/code4 and stop the watcher.
4. Begin work.

Science publishing `pending` before step 3 is refused at step 3. Publishing at any time after step 1 is seen by the watcher within one poll. No window exists in which a pending entry is unobserved while RE work runs. Science never waits on the RE: the coordinator's own gate does not consult the RE, and the RE's yield is bounded by §5.

## 5. Observation and enforcement (non-Python)

- **Watcher:** `tools/research_engine/watch.sh`, run as `/bin/sh tools/research_engine/watch.sh <session_dir>` at observed niceness ≥10. It is the only waiting process for observation; no Python watcher exists.
- **Poll:** every 1 s: (a) the §2 state, (b) the backstop: `/bin/ps -axww -o pid=,command=` matched against the §1 coordinator command paths (fixed-string list frozen in the script), (c) write `heartbeat` (UTC) to `<session_dir>/watch/heartbeat`. Observation latency ≤ 1 s + one poll's runtime.
- **Admission backstop (one-shot, Python allowed):** the existing pure classifier `blocking_processes` from `tools/c10w_p2_gate.py`, imported unchanged, run over a `/bin/ps` inventory excluding RE-owned PIDs. Any hit refuses code5. Expect frequent refusals while Codex builders run Python; that is correct.
- **Owned processes:** every RE process (importer, query client, Neo4j JVM) is recorded at spawn in `<session_dir>/owned.pids` as `pid lstart command`. The watcher signals only PIDs whose current `ps -o lstart=` matches the recorded value (no PID-reuse kills).
- **Trigger:** first poll that sees SCIENCE, UNAVAILABLE, or a backstop hit. Record `trigger_utc` (= **start of the 30 s deadline**) and, for a reservation, its `created_utc`.
- **Termination:** SIGTERM all owned non-Neo4j PIDs; `neo4j stop` for the owned server; at `trigger_utc + 25 s` SIGKILL any owned PID still alive; confirm each owned PID absent via `/bin/ps -p` by `trigger_utc + 30 s`. Write `<session_dir>/watch/termination_receipt.txt`: trigger reason, reservation entries seen, trigger_utc, per-PID signal/time/confirmed-absent, final verdict `TERMINATED` or `UNVERIFIED`. Any PID not confirmed absent → `UNVERIFIED`, which blocks the session.
- **Watcher exit:** after the receipt, or when the RE session ends normally. No automatic resume.
- **Watcher loss:** RE Python processes read `heartbeat` each second; older than 3 s or unreadable → halt code4 without publishing.
- **Accepted overlap:** science publication-to-confirmed-termination is ≤ 31 s (≤1 s observation + 30 s deadline). During it, a Java-only phase may coexist with a just-admitted science job; Neo4j is capped at 2 GB RSS and niceness ≥10 (v3 §11).

## 6. Frozen AC17/AC21 cases

Fixture cases (temp root passed through the test-only parameter; the production root is a constant):
1. Valid IDLE at start → admitted (positive control: an always-refusing implementation fails this).
2. Pending at start → code5.
3. Running at start → code5.
4. Two pending; release one → still code5; release both → IDLE.
5. IDLE → pending during work → trigger, all owned fixture PIDs terminated, receipt `TERMINATED`, ≤ 30 s from trigger_utc.
6. Authority loss during work (marker removed; `active/` replaced by a file; root renamed) → code4 halt + termination.
7. Malformed entry, `.tmp.*` entry, dotfile, subdirectory → code5, never IDLE.
8. Watcher heartbeat stale → RE halts code4.
9. Owned PID whose lstart no longer matches → not signalled; receipt records the mismatch.
10. A PID that ignores SIGTERM → SIGKILL at +25 s, confirmed absent.
11. Writer: duplicate `pending` refused; `running` and `release` are atomic renames; a writer failure leaves no partial entry visible as IDLE.

Host acceptance (MAESTRO verification, not fixture): with the real root, publish `pending` for a dry `launch_id` (no science run), confirm a live RE session's real Python and Neo4j PIDs terminate within 30 s with a `TERMINATED` receipt, then `release`. A fixture pass cannot discharge this.

## 7. Adoption (changes how science launches are made)

From MAESTRO's creation of `<root>` (after BUILD1 promote) onward, every science launch is: `pending` → the coordinator's unchanged gate loop → `running` at dispatch → `release` at exit. Until `<root>` exists, the RE state is UNAVAILABLE and RE dispatch on the host is blocked. That is the fail-closed default.
