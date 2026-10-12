# Astra spec r4 verdict — research-engine phase 1
Verdict: NO-GO

## r3 findings status

Review-document filenames below resolve under `results/research_engine_phase1_20261011/`.

T1. RESOLVED — The shared lock now orders reservation publication against RE admission and pointer replacement. This closes the original check-to-publication race while a reservation remains active. Evidence: `science_reservation_contract_v2.md:40–55`. The timeout-path yield defect is separate: U2.

T2. PARTIAL — Internal-volume ownership records and controller supervision address important gaps, but termination requires a living leader, contradicting orphan recovery. Startup and registry failure handling remain incomplete. Evidence: `science_reservation_contract_v2.md:19,50–67`; U1/U4.

T3. PARTIAL — Relative timers, monotonic heartbeat decisions and command caps replace the unbounded observation/UTC design. They do not establish the stated end-to-end deadlines. Evidence: `science_reservation_contract_v2.md:8,40–43,59–72,87`; U5.

T4. PARTIAL — Locked duplicate checking fixes concurrent duplicate creation. Whole-host classification does not prove a launch has ended or cannot spawn another worker. Evidence: `science_reservation_contract_v2.md:40–46`; U3.

T5. RESOLVED — Cooperative adoption, incomplete backstop coverage, differing gate behavior and an explicit launch delay are now acknowledged. The numerical delay guarantee remains under T3. Evidence: `science_reservation_contract_v2.md:8–10`; `phase1_spec_v4.md:213`.

T6. RESOLVED — Commissioning now creates the production root and obtains real termination evidence before promote. Evidence: `science_reservation_contract_v2.md:93–101`; `phase1_spec_v4.md:75–77,194`.

T7. PARTIAL — All nine formula identities and bottle hashes are supplied, and the repeat comparison is specified. However, the referenced DuckDB installation file contains non-requirements text and terminal escape bytes. Evidence: `preinstall_identity_20261011.tsv:3–11`; `phase1_spec_v4.md:242–244`; `duckdb_1.5.5_hashes.txt:1,38`; U7.

## Findings

U1. [severity: blocking] **Leader loss disables the promised orphan termination.** Evidence: `science_reservation_contract_v2.md:59–67,87,90`. Signals require the leader’s current `lstart` to match its recorded identity. After the controller dies, that comparison cannot succeed, although its Java child can remain alive in the group. This also occurs during ordinary enforcement: TERM removes the controller, a child ignores TERM, and the +20 s KILL is prohibited by the same identity rule. Consequence: controller-loss, both-dead and TERM-resistant-child guarantees cannot all be implemented as written. Correct absence checking would produce UNVERIFIED rather than the required termination. Ownership suitable for signalling surviving members must remain provable after leader exit; simply removing the identity check would introduce unsafe signalling.

U2. [severity: blocking] **The lock-timeout path checks absence before establishing the reservation.** Evidence: `science_reservation_contract_v2.md:40–43,50–59`. A permitted sequence is: the initial lock attempt times out → enforcement removes the old RE and confirms absence → a new RE acquires the now-free lock, observes IDLE and admits → the writer acquires the lock and publishes `pending`. This branch specifies enforcement before publication, without a second confirmation afterward. Consequence: its justification that “no RE process remains” is stale, and science can receive clearance while the new RE is alive. Lock ordering still prevents that RE from publishing while the entry remains active; it does not prove G2. The timeout path needs the same post-publication absence requirement as the ordinary path, within one overall deadline.

U3. [severity: blocking] **A clear classifier snapshot is not sufficient authority to release a reservation.** Evidence: `science_reservation_contract_v2.md:46`; `tools/c10w_p2_gate.py:22,43–59`; `experiments/track_c/autoresearch_c10/v13_launcher.py:84–102`. The classifier recognizes selected compute executables and an exact tmux session name; it does not establish that every launch-owned descendant has ended. The covered v13 launcher starts a Claude child before starting its Python watcher. If the launcher dies in that interval, the surviving Claude child can be absent from both classifier results yet remain capable of spawning work. Furthermore, the classifier snapshot precedes lock acquisition. Consequence: `release` can remove the last entry while the launch remains capable of dispatch, producing false IDLE and allowing RE admission/publication. Preserve the existing classifiers, but additionally require launch completion/quiescence evidence that excludes subsequent dispatch.

U4. [severity: blocking] **Startup has an undefined, potentially unbounded handshake, and the registry lacks a complete fail-closed lifecycle.** Evidence: `science_reservation_contract_v2.md:19,50–52,59–65`. The launcher waits for two sequence advances before the controller records its identity, while watcher observations already require that identity to check controller liveness. No startup state, readiness timeout or watcher-exit outcome is specified. Pending science present at startup can also cause the watcher to terminate before two advances. Separately, enforcement enumerates sessions “not `closed`,” but there is no rule establishing when a session may become closed or how missing/malformed ownership records affect clearance. Consequence: startup can wait indefinitely instead of returning the required refusal, and registry enumeration is not yet a sufficient proof that all RE processes are absent. Freeze registration-before-spawn, bounded readiness, registry-error refusal and closed-only-after-confirmed-absence rules. Also define watcher placement: “every RE process” in the controller group conflicts with an enforcer that must survive that group’s termination to write its receipt.

U5. [severity: blocking] **The 28 s/~30 s arithmetic does not cover the complete operations, and case 11 has a conflicting deadline.** Evidence: `science_reservation_contract_v2.md:8,40–43,59–63,72,87,91`; `phase1_spec_v4.md:213`. Specific gaps:

- Enforcement timers begin after publication; publication includes temporary-file creation, rename and `/bin/sync`. The 2 s cap explicitly covers enforcement/observation commands, without defining a total bound for this mutation sequence.
- The timeout branch can consume 2 s initial acquisition + 25 s enforcement + 2 s reacquisition = 29 s before publication overhead and receipt completion.
- Watcher-loss detection permits 3 s without sequence progress, followed by confirmation up to 25 s later. Case 11 instead requires termination within 25 s of watcher death.
- Per-command caps do not impose an aggregate deadline on registry traversal, repeated observations and receipt output.

Consequence: implementations cannot derive the promised total delay from these local bounds. Specify one elapsed-time origin and terminal deadline covering every branch, with an explicit bounded HALT outcome; align the tests to that deadline.

U6. [severity: blocking] **The unusable-root exception does not explicitly require successful termination before science proceeds.** Evidence: `science_reservation_contract_v2.md:8,42–44,67,72–73`. Normal pending publication distinguishes confirmed absence from UNVERIFIED and prohibits launch in the latter case. The unusable-root branch instead runs enforcement and returns code4 with “science may proceed after MAESTRO records this,” without conditioning that permission on confirmed absence. A timed-out process observation or unsignallable orphan therefore has an ambiguous clearance outcome. Consequence: recording the exception can be read as permission to overlap surviving RE work. Require an affirmative absence receipt on this branch too. In addition, only the watcher is copied off memit (`:19,50`); the writer remains `tools/science_reservation.sh` (`:20`). Registry relocation alone does not establish that a fresh writer invocation remains available after loss of the volume containing that script.

U7. [severity: condition] **The DuckDB hash artifact is not ready to serve directly as the prescribed installation input.** Evidence: `duckdb_1.5.5_hashes.txt:1,38`; `phase1_spec_v4.md:244`. Line 1 is an uncommented descriptive heading containing parenthetical prose. Line 38 begins with an actual ANSI escape sequence before its apparent comment. Consequence: the referenced bytes are not a clean requirements file; the specification neither supplies nor freezes an extraction step. Produce and freeze a machine-consumable hash lock, retaining the receipt separately, and verify its parsing before installation. This finding is based on byte inspection; I did not invoke an installer.

U8. [severity: condition] **Some explicit v3 controls and SR v1 input constraints disappeared.** Evidence: `science_reservation_contract_v1.md:34,81`; `science_reservation_contract_v2.md:40–46,78–91`; the AC21 replacement in the v3→v4 diff (`phase1_spec_v4.md:55`). SR v2 no longer specifies the launch-ID grammar/entry schema, and AC21/the enumerated cases omit the former explicit failed-write/no-IDLE control. G3 retains the broad failure guarantee, but it does not replace a checkable fault-injection case. Consequence: malformed launch IDs and interrupted writer mutations are underspecified at freeze. Restore explicit validated inputs and writer-failure controls, including failures around creation, rename and durability completion.

## Required before freeze

- Resolve U1–U6 in the contract, including the ownership, startup, release and deadline state transitions.
- Freeze the corrected DuckDB installation artifact and restore U8’s missing constraints/controls.
- Extend AC17/AC21 with deterministic interleavings for leader exit before escalation; a new admission between timeout-path enforcement and publication; surviving nonmatching launch descendants; startup watcher exit; malformed/missing registry records; and unusable-root enforcement failure.
- Make deadline tests cover invocation-to-return/HALT, not only publication-to-confirmation.

AC17/AC21 and SR §7 cases 1–15 are **partly checkable, but insufficient and internally inconsistent as a complete acceptance contract**. Cases 1–10 provide useful state, ordering and lifecycle controls; cases 11 and 14 conflict with the leader-dependent signalling rule; case 15 lacks the interleaving in U2. Case 11’s timing also conflicts with §5. Passing the current fixtures would not establish G1–G3.

SR §8 commissioning remains mandatory before promote. Its real Python/Neo4j receipts cannot be replaced by fixture results, and its ordinary successful `pending` scenario cannot establish the missing failure-path guarantees (`science_reservation_contract_v2.md:95–101`).

No renewed decision on the operator’s two approved choices is requested.

## What I checked and did not check

Read the r3 verdict, SR v1/v2, v4, the complete v3→v4 diff, the identity manifest, DuckDB hash file, provisioning receipt, operator answers and relevant classifier/launcher code.

All functional v4 edits occur in sections named by §16. The additional changes are the version preamble and §16 itself. However, full requirement preservation cannot be claimed: the explicit controls/input constraints in U8 disappeared, and the deadline guarantees remain unsupported. The move from zero claimed delay to a bounded launch delay is disclosed, rather than an unnamed section change.

Both supplied SHA-256 pins matched before and after review. SR v1 and spec v3 also match the hashes recorded in r3.

This was static, read-only contract review. Counterexamples are inferred permitted interleavings, not observed implementation failures. I did not rerun the host lock probe, execute tests, install packages, start services, signal processes, run science, edit files or write context-save artifacts. R2–R4 and the operator’s choices were not re-reviewed.

🌱 graft reported ~204,718 tokens saved (~$0.13), 1 successful call; its results supplied no review evidence.