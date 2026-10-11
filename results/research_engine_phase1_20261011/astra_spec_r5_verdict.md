# Astra spec r5 verdict — research-engine phase 1
Verdict: NO-GO

## r4 findings status

Review-document filenames below resolve under `results/research_engine_phase1_20261011/`. **SR3** means `science_reservation_contract_v3.md`.

U1. RESOLVED — Each surviving matching PID is identified independently; escalation no longer requires a living leader. Case 8 explicitly covers an orphan JVM ignoring TERM. Evidence: SR3:28–34,62,83. Completeness of the matched process population remains V3.

U2. RESOLVED — Clearance now requires an inventory after publication, including the lock-timeout branch, and explicitly terminates an intervening admission. Evidence: SR3:61–66,82; `phase1_spec_v5.md:53`.

U3. PARTIAL — Tokens and inspection under the lock improve release, but registration order, coordinator identity storage and pending-entry completion remain undefined. Evidence: SR3:24,54–55,92; `phase1_spec_v5.md:57`. See V2.

U4. RESOLVED — The circular readiness handshake and registry lifecycle are removed. Their specific defects disappear. Evidence: SR3:5,28–34; `phase1_spec_v5.md:195–197`. Replacement failure coverage remains incomplete; see V1/V3.

U5. PARTIAL — One invocation-based deadline replaces the conflicting timers, but firing a timer at 30 seconds does not bound subsequent termination, receipt output and return. Evidence: SR3:59–64,70–71; `phase1_spec_v5.md:53`. See V4.

U6. PARTIAL — Exit 4 now requires post-check absence. P-memit addresses writer availability during complete volume loss only conditionally; the unusable-root exception still has no reservation protecting science against authority restoration. Evidence: SR3:13,61–64,87. See V5.

U7. RESOLVED — The clean requirements lock is pinned, and the supplied parse/resolve receipt records exit 0 against that hash. Evidence: `phase1_spec_v5.md:246`; `duckdb_1.5.5.lock.txt:1–36`; `duckdb_lock_parse_receipt_20261011.txt:2–8`. I verified the file hash, not an installation.

U8. PARTIAL — Launch-ID/coordinator constraints and post-creation crash controls return. The entry schema omits identity fields required by release, and case 16 does not cover failed creation or all claimed mutation failures. Evidence: SR3:24,54–55,90–91; `phase1_spec_v5.md:57`. See V2/V8.

## Findings

V1. [severity: blocking] **Removing the watcher leaves required failure-triggered termination without a mechanism.** Evidence: `astra_spec_r1_verdict.md:17`; `phase1_spec_v4.md:51`; `science_reservation_contract_v2.md:61–63,83`; SR3:5,46,59–72,91; `phase1_spec_v5.md:53,215`.

R1 does not mandate an RE-side watcher. A functioning science-side enforcer can satisfy its ordinary pending-launch requirement. However:

- An admitted RE can remain working when the authority becomes invalid without any `pending` invocation. SR3 specifies checks at admission/publication, not bounded detection and termination during work. V4 AC17 explicitly required that outcome.
- Kill the sole writer after its pending entry is durable but before it signals the RE. The reservation prevents subsequent admission/publication, but no surviving mechanism must terminate the existing Python/JVM within the shutdown bound. Case 16 checks retained SCIENCE state only.

Consequence: publication exclusion is preserved in these examples, but cancellation and bounded termination are not. A failed writer withholding launch permission prevents immediate science overlap; that is weaker than the retained termination obligation.

V2. [severity: blocking] **Release still lacks a complete launch lifecycle and usable identity record.** Evidence: SR3:24,54–55,99–101; `experiments/track_c/autoresearch_c10/v13_launcher.py:81–102`.

The frozen schema contains neither `coordinator_pid` nor `coordinator_lstart`, although release requires the recorded pair. No rule requires `running` and descendant-token registration to complete before dispatch-capable descendants start. The cited v13 launcher generates its session ID internally and starts Claude before its watcher.

A pending entry also has no defined terminal/cancelled state. Commissioning explicitly calls `pending`, then `release`, without `running`; the required coordinator identity therefore has no specified source.

Consequence: refusing missing identity makes the prescribed commissioning release undefined; treating missing identity/tokens as empty can reopen the r4 surviving-Claude gap. A locked process inventory also cannot distinguish a completed launch from a pending launch whose coordinator has not started yet. Clearing the latter permits IDLE and RE admission before that previously cleared science launch starts. Freeze registration, completion/cancellation and release eligibility as explicit transitions.

V3. [severity: blocking] **The ownership patterns contradict the prescribed runtime invocations, and completeness is asserted rather than established.** Evidence: SR3:28–34,63; `phase1_spec_v5.md:27–31,159,197,244,248`.

The documented `verify` and `agent` commands use a relative `tools/research_engine/cli.py` and contain no session token. The Python ownership pattern requires an absolute script path and the token. Thus those exact commands either must refuse, contradicting their prescribed use, or create RE Python processes invisible to enforcement.

Anchoring protects against ordinary Codex/Claude executables carrying a quoted brief. Conversely, a JVM missing the property and any helper outside the two patterns are invisible. The provisioning smoke checks one JVM invocation; it does not establish ownership for every start/error path. “The RE spawns nothing else” also needs reconciliation with the required committed-byte `git show` capture path.

Consequence: zero pattern matches is not yet proof of zero owned processes. Freeze consistent invocations, ownership for permitted helpers, and startup refusal/containment for missing or malformed identity. Commissioning must independently account for the launched processes, not use the same matcher as both implementation and oracle.

V4. [severity: blocking] **The deadline mechanism does not establish invocation-to-return ≤30 seconds or bounded cessation of writer activity.** Evidence: SR3:52,59–64,71,86.

At +30 seconds the timer starts killing the working subshell, writing the HALT receipt and arranging exit. Receipt output occurs after the deadline trigger; stdout or a filesystem write can block. Capping external commands does not automatically bound shell redirection/builtin output. Killing one subshell also does not specify termination of its outstanding external descendants or release of inherited lock descriptors.

Consequence: a verb can exceed the promised bound, or return HALT while a surviving descendant retains the lock or completes a mutation. Define a terminal path that includes receipt failure and descendant handling within the budget. Test blocked output and outstanding mutation children, not only hanging `ps`/`ls`.

V5. [severity: blocking] **Exit-4 clearance can become stale when the authority is repaired.** Evidence: SR3:13,42–46,61–64,87; `phase1_spec_v5.md:53,215`.

Permitted sequence: the marker is invalid → `pending` confirms no RE and returns 4 without publishing → MAESTRO records the receipt → the authority is restored to valid, empty IDLE before the coordinator starts → a new RE admits → the previously cleared science launch starts. No reservation or restoration rule excludes this sequence.

Consequence: science can launch while RE processes live despite the earlier affirmative absence receipt. P-memit does not cover this example: the volume remains mounted. Even accepting its fresh-launch premise during total volume loss, it does not protect the interval after recovery. The exception needs persistent exclusion or a rule preventing reuse of its clearance after restoration.

V6. [severity: condition] **The admission backstop retains the brief-text false-positive problem that ownership matching avoids.** Evidence: SR3:34,50,54–55.

Section 3a rejects any command containing a covered coordinator path as a fixed string. The contract itself acknowledges that Codex/Claude argv can contain whole briefs. A review or orchestration brief mentioning `tools/run_c10v_stage.sh` therefore blocks RE admission without being a science coordinator. Release tokens can similarly match descriptive text.

Consequence: the fixture positive control can pass while ordinary orchestration makes host admission or release persistently refuse. Freeze command-identity semantics for this additional backstop and include a brief containing complete coordinator paths, not merely the RE token.

V7. [severity: condition] **The explicit prohibition on automatic resume disappeared without being identified in §17.** Evidence: `phase1_spec_v4.md:213`; `phase1_spec_v5.md:215–217,285–290`.

V4 says “No automatic resume.” Its replacement omits that requirement. The retained prohibitions on services, autostart and schedules do not explicitly prohibit a running controller from restarting yielded work.

Consequence: requirement preservation cannot be claimed. Restore the prohibition or explicitly account for its removal. Separately, V1 identifies the substantive authority-loss termination weakening hidden within the advertised watcher removal.

V8. [severity: condition] **The restored fault controls do not cover the full failure guarantee.** Evidence: SR3:11,44,50,52,63,76–93; `phase1_spec_v5.md:57`.

Case 16 begins after successful temporary-file creation. It does not exercise creation failure, rename failure or durability-command failure. With an initially valid empty authority, failure before creating an entry can leave IDLE, contrary to the unrestricted G3/AC21 wording. This need not authorize science if failed `pending` blocks dispatch, but that distinction must be explicit.

Likewise, the explicit empty-inventory rejection belongs to §3a; pending clearance instead uses “zero RE-owned processes.” Its cases cover hanging observations, not empty or malformed successful output.

Consequence: passing the listed fixtures would not establish the stated failure guarantee. Define these outcomes and require a successfully validated inventory before absence clearance.

## Required before freeze

- Resolve V1–V5 in the contract and reconcile AC17/AC21 with the resulting mechanisms.
- Complete the release schema and lifecycle, including pending cancellation, registration before descendant dispatch, and commissioning release.
- Resolve V6–V8 and preserve the omitted no-resume requirement.
- Add deterministic controls for writer death after publication, authority loss without a writer invocation, release before coordinator start, death before token registration, authority restoration after exit 4, untagged runtime processes, blocked receipt output, surviving command descendants, failed mutations and invalid inventories.
- Freeze the concrete CLI/receipt shapes and the existing reviewed-key/source/scope/decision-ID obligations required by `phase1_spec_v5.md:31,73–75`.

AC17/AC21 and SR §6 cases 1–18 are **partly checkable but insufficient**. The state, lock-ordering, orphan, identity-mismatch and clock controls provide useful deterministic predicates. Release cases 4/17 depend on the missing lifecycle; deadline cases 6/7/11 depend on V4; case 12 omits restoration; case 16 proves retained reservation state, not termination after enforcer loss.

SR §7 commissioning remains mandatory before promote. Its real-process receipt cannot be replaced by fixtures (`SR3:95–103`; `phase1_spec_v5.md:78,215`). One successful pending invocation does not establish the omitted failure paths.

No renewed operator choice or R2–R4 review is required.

## What I checked and did not check

Read the r1/r4 verdicts, SR v2/v3, v5, the complete v4→v5 diff, DuckDB lock/parse receipt, and relevant classifier/coordinator code.

All functional diff hunks are within the advertised reservation/provisioning areas, including commissioning renumbering. That does **not** establish semantic preservation: authority-loss termination and the explicit no-resume prohibition were lost.

The supplied SR3, v5 and DuckDB lock SHA-256 values matched before and after review. The lock hash is `f8ffcdeadaded28928249cf8b468a25e9cf25e8a1a6b028b22deed8757c28636`.

This was static, read-only review. Counterexamples are inferred protocol interleavings, not observed implementation failures. I ran no tests, installations, services, process signals, science or commissioning; edited no files; and wrote no context-save artifacts. Host argv shapes, termination, resource enforcement and the claimed sub-millisecond PID-reuse window remain unverified.

🌱 graft reported ~194,282 tokens saved, 1 successful call; its results supplied no review evidence.