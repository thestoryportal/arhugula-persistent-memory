DONE

# D-C10u-mint2 r3 — facts sheet for the §8.1 post-observation deviation note

This sheet supports `results/c10u_mint2_r3_deviation_note_draft.md`. Every value below was read on 2026-10-07 from the file or command named next to it. Abbreviations: R = the repository root (this worktree); PREREG = `docs/C10U_MINT2_PREREG.md` (read with `cat -n`); RB = `EXPERIMENT_RUNBOOK.md`; READ = `results/c10u_mint2/r3_read_after_replicateF.json`; ARMS = `experiments/track_c/c10u_mint2_arms.py`; RD = `experiments/track_c/c10u_mint2_read.py`. Record fields were extracted with `python3 -I` and `json.load`.

Pins checked:
- `shasum -a 256` gives RD = `1223789a0941e46c…` and PREREG = `c54f443c70fecd12…`. Both equal `identity.source_sha256` in the p4-save diagnostic and in every r3 record.
- `git log -- RD` shows the last change to RD in `afbf8e9` (2026-10-07 10:01:24 MDT).

## Final readings (READ)

**Block F**
- `F.direction` = "ROUTING-BLOCKED-UNDERFIT".
- `F.reasons` = modifier s0/s1/s2 "admission UNDERFIT n_ge_0.98" = 17/24, 13/24, 14/24, for both r0 and r1.
- `F.reproduction[0]` and `[1]`: ok = true, counts {0: 46, 1: 37, 2: 40}, median 40, multi_checked = true.
- `F.comparability_ok` = true; `F.raw_direction` = null; `F.replication_pending` = false; `F.controls_pending` = false.

**Block F arms**

| arm | label | binding | reference | gain | failed gates | replica |
|---|---|---|---|---|---|---|
| mint1_s0 | LEAD | 46 | 14 | 32 | none | identical |
| mint1_s1 | LEAD | 37 | 14 | 23 | none | identical |
| mint1_s2 | TRADEOFF | 40 | 14 | 26 | `generic_ppl` (all others true) | identical |

- The `replica.label` "LEAD-NOT-REPLICATED" seen for s0 and s1 is the nested read without a replica (RD:386, :391–392).
- Seed 2's perplexity: `generic_ppl_post` was 22.074 in `r3/F_r0_mint1_s2.json`, against the multi's 21.522 in `r3/F_r0_multi_snone.json`. The rule (RD:130) is post ≤ ref + 0.5 = 22.022, so the gate fails by 0.052.
- A1 `para_full_n` = 68 in every F record (the floor) and 70 in every V2 record. LAW#5 ok in every record (expr_delta ≤ 0.0002).

**Block V2**
- `V2.direction` = "NOT-COMPARABLE"; `V2.comparability_ok` = false; `V2.reasons` = []; `V2.replication_pending` = true; `V2.controls_pending` = false.

| arm | label | binding | reference | gain | detail |
|---|---|---|---|---|---|
| mint1_s0 | LEAD-NOT-REPLICATED-NOT-COMPARABLE | 51 | 31 | +20 | |
| mint1_s1 | LEAD-NOT-REPLICATED-NOT-COMPARABLE | 46 | 31 | +15 | |
| mint1_s2 | LEAD-NOT-REPLICATED-NOT-COMPARABLE | 38 | 31 | +7 | |
| mint2_s0 | TRADEOFF-NOT-COMPARABLE | 30 | 31 | −1 | gates described_as = false, sibling = false; all_positions_fit = false; underfit subject Fluvane; masked_value_n 23 |
| mint2_s1 | UNDERFIT-NOT-COMPARABLE | — | — | — | `r3/V2_r0_mint2_s1.json` admission.P3.n_ge_0.98 = 20 |
| mint2_s2 | UNDERFIT-NOT-COMPARABLE | — | — | — | `r3/V2_r0_mint2_s2.json` admission.P3.n_ge_0.98 = 21 |

- `V2.arms.mint1_s*.replication_pending` = true.

## (a) Authority for r3 — VERIFIED

- PREREG:172 reads: "**r2 is the last attempt.** Any LAW#3 miss in r2 (…) closes `D-C10u-mint2` as HALTED through the close-out gate; there is no r3 unless the operator records a new ruling."
- RB:347 is D-C10u-r3go, headed "(… ~09:00 MDT; program rulings under D-C10r-rulings-9)". Its item (1): r2 closes HALTED-HARNESS. Item (2): one read-then-fix in commit 0a6aed3; "any further HALT in r3 stops step 3 for an operator report". Item (5): the reader fix, "not a second blind fix".
- RB:342 is D-C10r-rulings-9 (2026-10-07 ~05:45 MDT). Quoted: "work autonomously, delegate (subagents, tmux Claude sessions, Codex, sometimes Gemini), manage every session's context with Memento; LAWs and the operator's standing directives unchanged. Program rulings under that approval: …". Its item (4) covers only r1 HALTED and "r2 only from a fresh OUT_DIR after both reviews". It says nothing about an attempt after r2.
- RB:338 is D-C10r-rulings-8 (2026-10-06 ~23:55). Quoted: "Your recommendations are given blanket approval for no HIL autonomously until I explicitly intervene ... Continue through the night."
- RB:343 is D-C10u-Aenv (~07:30 MDT, after rulings-9). It says r2 "is the LAST attempt".
- RB:351 is D-C10r-rulings-10, the only row marked "DECIDED (operator)" (checked with `grep -n "DECIDED (operator)" RB`). It is timed ~15:55 MDT and does not mention step 3 r3. `grep -n "\br3\b" RB` finds r3 only in the program rows :347 and :349; the matches at :338, :339 and :943 refer to other experiments.
- RB:350 is D-C10w-p1budget (revised 15:05). Quoted: "the program does NOT write its own budget authorization — the auto-mode safety classifier refused that step as weakening a safeguard, and both reviewers said the raise must come from the actual authority."
- `results/c10u_mint2_r2_halt_analysis_2026-10-07.md:3` reads: "harness defect, not a science gate". Lines :10–14 describe the empty-log false HALT.
- Timing: `r3/reproduce_started.json` `when_utc` = 2026-10-07T16:01:40.327312Z (10:01:40 MDT). Commit 0a6aed3 is at 08:55:37 MDT; commit afbf8e9 at 10:01:24 MDT.

## (b) Baseline windows and multi counts — VERIFIED

Fields `recipe.arms.candidate.para_full_n` / `canon_full_n` / `para_first_n` (the same values as `arm.*`):

| record | para_full | canon | para_first | A1 | ctx sha256 |
|---|---|---|---|---|---|
| r1: `results/c10u_mint2/F_r0_multi_snone.json` | 10 | 8 | 55 | 69 | `aa476792…` |
| r2: `results/c10u_mint2/r2/F_r0_multi_snone.json` | 10 | 9 | 52 | 69 | `dd73fdc9…` |
| r3 r0: `results/c10u_mint2/r3/F_r0_multi_snone.json` | 14 | 8 | 53 | 68 | `8638d12c…` |
| r3 r1: `results/c10u_mint2/r3/F_r1_multi_snone.json` | 14 | 8 | 53 | 68 | `8638d12c…` |

- The original window (PREREG:77) is para_full [11, 18], canon [5, 10], para_first [48, 62]. The A4 window (PREREG:175; RD:21) is [5, 18], [5, 10], [42, 59]. NULL band (RD:22) = (11, 18). Per-seed reproduction windows (RD:23) = {0: (32, 56), 1: (24, 44), 2: (26, 46)}.
- r2's 10 is outside the original window and inside A4. r3's 14/8/53 is inside both.
- r3 mint-1(frozen) `arm.para_full_binding_n` = 46/37/40 in both r0 and r1, inside the per-seed windows.

## (c) P3 admission screen — VERIFIED

- PREREG:90: "**Validity (any failure → INVALID):** P1; P2 (a)(b)(c); P3 admission screen; …"
- PREREG:72: "any value under 0.98 marked **UNDERFIT** … otherwise the block's direction reading is **ROUTING-BLOCKED-UNDERFIT**".
- PREREG:115: "P3 screen < 22/24 → UNDERFIT, no behavioural run".
- RD:105: `outcome = "UNDERFIT" if not p3["ok"] else ("INVALID" if reasons else "ADMITTED")`.
- ARMS:771–779: the non-admitted branch writes a record with `pid: None` and `outcome: step["outcome"]`, then returns without model work.
- RD:282–317 (`nonadmitted_validity`); RD:320–324 (validator dispatch on outcome); RD:377–379 (arm label UNDERFIT); RD:559–567 (block ROUTING-BLOCKED-UNDERFIT, with reasons naming each arm).
- `results/c10u_mint2_readerfix_advisor.md:65` names the :90 vs :72/:115 tension. `results/c10u_mint2_r3fix_advisor.md:13–19` (A1) records that the r2-era reader read a non-admitted record as invalid.
- r3 records with outcome UNDERFIT (pid null): `F_r{0,1}_modifier_s{0,1,2}.json` and `V2_r0_mint2_s{1,2}.json`. No r3 arm label is INVALID (READ).

## (d) P4 eligibility in a ROUTING-BLOCKED block — VERIFIED

- ARMS:945 skips only ("INVALID", "HALT-LAW3", "INCOMPLETE", "NOT-COMPARABLE"). ARMS:950 skips `outcome == "UNDERFIT"` originals. ARMS:956–957 raises a ValueError when nothing is selected.
- `results/c10u_mint2_readerfix2_advisor.md:57–60` (A6): "The operator should still confirm that P4 on a direction-blocked block is intended."
- No operator confirmation of A6 was found in RB §5.2. Evidence: `grep -n "A6\|p4_configurations"` over RB and SESSION_CHECKPOINT finds nothing about A6, and RB:351 (the only operator row) does not mention P4.
- In r3, every F modifier record is UNDERFIT (r0 and r1) and V2 is NOT-COMPARABLE, so the selection was empty.

## (e) The A1 rule — VERIFIED (found)

- RB:347, D-C10u-r3go (5): "**Rule recorded (advisor A1; the prereg is silent on it):** a V2 block whose multi or mint-1 reference arm is not DONE (incl. a non-admitted mint-1 seed, so no mint-1 median) reads **-NOT-COMPARABLE** (fail-closed), and P4 refuses it."
- Source: `results/c10u_mint2_readerfix2_advisor.md:7` and `:17–20` (A1, "Ledger the interpretation"). Code: RD:474–479 (`_comparability`, returns False at :476–477 when an arm is not DONE).
- `git log -S"Rule recorded (advisor A1" -- RB` gives `afbf8e9`, 2026-10-07 10:01:24 −0600. Its message: "A1 rule (missing mint-1 median -> NOT-COMPARABLE) recorded under D-C10u-r3go".
- r3 started at 16:01:40 UTC (10:01:40 MDT), 16 s later.
- Not exercised in r3: `r3/V2_r0_multi_snone.json` and `r3/V2_r0_mint1_s{0,1,2}.json` all have outcome DONE.

## (f) Advisories A2–A5 of `results/c10u_mint2_readerfix2_advisor.md` — VERIFIED (disposition partially UNVERIFIABLE)

| item | lines | content | state in r3 |
|---|---|---|---|
| A2 | :22–37 | unchecked bookkeeping fields | No code change (RD hash = r3 pin). nonadmitted_validity still checks only P3.ok, n_ge_0.98 and outcome (RD:298–301). |
| A3 (a) | :41–42 | empty `reasons` for a NOT-COMPARABLE from a DONE screen miss | Occurred: READ `V2.reasons` = []; RD:551–552 lists only non-DONE arms. Dispositioned in RB:349 (D-C10u-r3skipV2 (d)): "reporting gap, verdict unaffected; fix queued for any future attempt". |
| A3 (b) | :43 | generic HALT-LAW3 text | Not exercised (all F mint-1 records DONE). |
| A4 | :45–50 | non-admitted control drops raw ranges | Code unchanged: RD:529 still includes ctl. Not exercised (no `mint1_48` records in r3; READ `V2.controls_pending` false). |
| A5 | :52–55 | mixed DONE/UNDERFIT replica pair accepted | Code unchanged: RD:337. Not exercised (r0/r1 outcome pairs equal, and r1 records' `step0_file` points at the r0 step-0 file, ARMS:770, :774). |

- Formal ledger disposition of A2, A4 and A5: **UNVERIFIABLE (none found).** `grep` for readerfix2_advisor, A2–A5 and related strings over RB, SESSION_CHECKPOINT.md and `results/c10u_mint2_*` found only the A1 rule (RB:347) and the A3a disclosure (RB:349). The note states "no disposition recorded".

## (g) V2 replication waiver — VERIFIED

- RB:349, D-C10u-r3skipV2 (~14:45 MDT, "program ruling under D-C10r-rulings-9; post-observation prereg deviation"), "DECIDED — SKIP `replicate-V2`". Its four conditions (a)–(d) are quoted in the note.
- `r3/V2_r0_multi_snone.json`: para_full 31, canon 24, para_first 49, A1 70. 31 > 18 and 24 > 10; 49 is inside [42, 59].
- mint-1(V2) bindings 51/46/38, median 46 ≥ 30.
- READ `V2.reasons` = []; RD:551–552.
- mint-2 s0: binding 30, reference 31, gain −1, TRADEOFF. described_as and sibling are false. RD:344–345 gives LEAD-sized at ≥ 30 and TRADEOFF when the gates are not clean.
- mint-1(V2) s2: binding 38, gain +7, label LEAD-… by the absolute ≥ 30 rule (PREREG:92; RD:344).
- `V2.replication_pending` = true, and each `V2.arms.mint1_s*.replication_pending` = true.
- The replicate-F log ends with `STAGE_EXIT=0` (`tail -2 results/c10u_mint2_logs/r3/replicate-F.log`).
- Reviews: `results/c10u_mint2_r3_v2rep_astra.md:1` and `results/c10u_mint2_r3_v2rep_advisor.md:1` both give "VERDICT: SKIP-REPLICATE-V2-WITH-CONDITIONS". Advisor :18 assumed the replica "would re-measure 31 and 24 in a fresh process" and measure the ±4–5 envelope; item (h) shows that a replica under this design reproduces bit-identically. The note marks this as an inference.

## (h) Block-F replica bit-identical — VERIFIED

**Command.** A Python leaf-flattening diff of `r3/F_r0_<x>.json` against `r3/F_r1_<x>.json`, for x in multi_snone, mint1_s0..2, modifier_s0..2 and the `_started` files:

| record | leaves | differing leaves |
|---|---|---|
| multi_snone | 3,706 | 3: pid 64278→33511, replicate 0→1, when_utc |
| mint1_s0 | 6,424 | 3: pid 41161→2286, replicate, when_utc |
| mint1_s1 | 6,424 | 3: pid 55239→16167, replicate, when_utc |
| mint1_s2 | 6,424 | 3: pid 64907→30679, replicate, when_utc |
| modifier_s0 | 3,443 | 1: replicate |
| modifier_s1 | 3,447 | 1: replicate |
| modifier_s2 | 3,446 | 1: replicate |
| `_started` files (87 leaves each) | 87 | 2: pid, replicate |

**Mechanism (code read).**
- ARMS:769: `read_context` (`contexts_F.json`), shared by both replicates.
- ARMS:782: `set_contexts` before LAW#5. ARMS:173–180: `set_contexts` assigns `CONTEXT_TEMPLATES_CACHE`.
- ARMS:770 and ARMS:746–757: `require_step0` uses `record_name(block, 0, …)`, i.e. the r0 step 0.
- ARMS:797–800: loads `rows_file` and `zs_file` from step 0. ARMS:816: `Z_OVERRIDE` built from those z rows. ARMS:818–820: the multi captures its own z on the frozen contexts.
- `r3/F_r1_modifier_s*.json` `step0_file` = `…/r3/step0/F_r0_modifier_s*.json`.
- `ls r3/inits r3/zs` shows only `*_r0_*` files.

**Stochastic source.**
- `memit_dry_run/memit/memit/memit_main.py:304–320`: `get_context_templates` calls `generate_fast` once per process when the cache is None.
- `memit_dry_run/memit/util/generate.py:116–119`: topk, then `torch.multinomial`. `grep "seed"` over generate.py finds no seeding.
- `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:32` (F-A4): "Cross-process `delta_norms` vary by up to 4.35 % … because the engine samples its context templates per process (… unseeded top-k multinomial)". Its line citation `generate.py:40–43` is stale; the sampling is at :116–119.
- `CORPUS/45_C10L_MINT_TOKEN.md:61`: "the ±5/72 per-process envelope is respected within a configuration and exceeded (12) between the two N seeds". The processes were N seed 0 46/42 and G 39/38 (:52–54). :54 notes "fresh process, same `inits/G.pt`", so the inits were the same and only the contexts were resampled.

**Prereg text.**
- PREREG:78: "a fresh-process block on the same frozen context set and the same inits — it measures the ±4–5 process envelope (`CORPUS/45:61`)".
- PREREG:67: the frozen context set per block.
- PREREG:119: "the `Z_OVERRIDE` capture and the context-set freeze are the two new behaviours".
- PREREG:103: "a replication block on the same inits is not an independent seed draw".

**Cross-attempt observations.** Field `arm.para_full_binding_n`; init `provenance.row_pairing.rows_sha256`:

| seed | r1 | r2 | r3 | rows sha256 |
|---|---|---|---|---|
| 0 | 40 | 34 | 46 | `2c1d09e7…` in all three |
| 1 | 36 | 35 | 37 | `f50f9ea5…` in all three |
| 2 | 41 | 37 | 40 | `9d5cc3c8…` in all three |

- ctx sha256 differs per attempt (`aa476792…`, `dd73fdc9…`, `8638d12c…`).
- `identity.source_digest` differs per attempt (`54dc4fcb…`, `f6a8482b…`, `67c73b97…`), a confound.
- Modifier s0 step 0: r2 `r2/step0/F_r0_modifier_s0.json` P3 17, underfit [1, 5, 8, 12, 13, 16, 20]; r3 `r3/step0/F_r0_modifier_s0.json` 17, underfit [7, 8, 12, 13, 17, 20, 22].

## (i) p4-save — VERIFIED

- `results/c10u_mint2_logs/r3/p4-save.log` line 1: "HALT: P4 requires replicated LEAD/PARTIAL mint-2 or modifier configuration; diagnostic: …/c10u_mint2_halt_diagnostic_eeebb090db424457a2f80452aba8ed73.json". Line 2: "STAGE_EXIT=1".
- Diagnostic: stage "p4-save", when_utc 2026-10-07T22:02:37.430380Z, reason as above, exception ValueError. The traceback runs ARMS:1103 → ARMS:990 → ARMS:957.
- `ls -a results/c10u_mint2/r3 | grep -iE "p4|edited"` matches nothing, so no started marker or artefact exists. The marker would be written at ARMS:1015.
- PREREG:86: "P4 runs on the mint-2 and arm-B configurations that carry a LEAD or PARTIAL label."
- RB:344 (D-C10u-r2go (2)): a refusal raised before `_started.json` and before model work is procedural.
- RB:349 (d): "`p4-save` expected to refuse = P4 NOT TRIGGERED (no eligible configuration), not a PASS".

## Not verified

- Whether MPS kernels are deterministic in general. Only this run's bit-identity was observed.
- Whether the operator has ratified r3 anywhere outside the repository. Nothing was found in RB §5.2: UNVERIFIABLE from the repository.
