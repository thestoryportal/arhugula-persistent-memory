---
name: test-first-one-round-builds
description: "Operator rule 2026-10-07 ~06:10 MDT: concise, accurate, bug-free code the first time — tests derived from the prereg written before the code, run green before hand-off — so review loops shrink; applies to me, Codex and every subagent."
metadata:
  node_type: memory
  type: feedback
  originSessionId: ef74c20d-d259-4cb7-9e93-31d8d916f184
  modified: 2026-10-07T12:00:43.542Z
---

The operator's words: "be accurate and concise when coding... all of you. Review loops that go on and on are to be reduced by testing forward development and precision quality, concise bug free code the first time, not after a back and forth that slows down this powerful important work."

**Why:** step-1 and step-3 drivers each took several Codex FIX-FIRST rounds plus advisor rounds before a run (e.g. D-C10s-sharedz driver v3 after three Codex rounds); today a tuple/list check in `c10u_mint2_arms.py:45–54` raised a false HALT that a round-trip unit test would have caught.

**How to apply:** every build brief (Codex or subagent) must say: (1) derive a test list from the pre-registration's numbered criteria, gates and labels BEFORE writing code, and write those tests first; (2) include round-trip tests for every persisted record (write → read → compare JSON-normalised), boundary tests for every threshold (value at, just inside, just outside), and a HALT-path test for every gate; (3) read the source you depend on with line numbers (LAW#4) before coding; (4) smallest code that satisfies the prereg, no speculative options; (5) run the full selftest suite green and paste its output in the report before saying DONE; (6) the reviewer then checks the prereg-to-test mapping first. One implementation round is the target; a second round only for a real defect. Related: [[model-and-compute-allocation]], [[operator-overnight-autonomy-2026-10-06]].

**Gate replays (2026-10-07, step-5 halt, advisor A4):** a replay of a gate must run EVERY `require` in the replayed function — the pre-run MMLU replay skipped the distinctness check and missed the college_physics duplicate that halted step 0. Build replays (and real-data tests) by calling the production function on real cached inputs and counting require sites hit, not by re-implementing a subset.

**Launch-path exec bit (2026-10-08):** ASTRA run 1 failed at launch with exit 126 — `tools/run_c10z_stage.sh` was committed 644 and the attempt wrapper exec'd it; the selftests copied the script text and ran it via bash, so 216 green tests never touched the execute bit. Every build brief must require: each script the launch path executes directly is committed 100755, with a test asserting os.access X_OK and the git index mode.

**Retract refuted steers fully (2026-10-08):** I warned builders to add attention masks on an unconfirmed hypothesis; after it was refuted my correction said "keep the mask tests (harmless)", and C10X then shipped a pre-hook injecting masks into the frozen harness scorers (a LAW#5 science-path change) and broke Amendment T4 statement-identity. Rule: send hypothesis-driven warnings to builders only after confirmation; if one is refuted, tell them to REVERT every change made for it, near any frozen path especially.

**Halt diagnostics must be self-explaining (2026-10-08):** all three new drivers halted with records that omitted the deciding evidence — ASTRA Z0 (no sigma), C10X X2-vii (no residual magnitudes), C10Y calibration (ValueError text, no traceback) — each costing a probe or rerun to diagnose. Every brief must require: halt/INSTRUMENT-ERROR records carry traceback.format_exc(), the phase, and the measured values compared against the failed threshold, written before raising; with a test per gate.

**Validate records at every stage boundary (2026-10-08):** C10X re-run 1 measured both arms for ~2 h, then halted writing its final record because harness-scorer flags (tensor/numpy bools) are not JSON; fixtures used Python bools. Briefs must require plain-JSON coercion where scorer values enter records, strict-JSON validation of the record at each stage boundary (fail fast with the field path), and regression tests with the real harness return types.

**Persist before the gate (2026-10-09).** Two drivers lost the very statistic that failed: ASTRA saved dstats after V7 (halt at :1107 before save at :1113), and C10Y wrote `{}` placeholders for every instrument record when instrument_prefix halted (all four calibrations). Every build brief must require: completed and partial records plus the gate's offending inputs written (exclusive create, fsync) BEFORE the gate evaluates, explicit NOT-RUN status for skipped checks, and a forced-halt regression test that loads them back. A halt you can't inspect costs a whole re-run to diagnose.
