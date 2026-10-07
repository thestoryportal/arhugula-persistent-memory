# Pre-registration — D-C10r-exp2ctl v2: location control for the autoresearch loop's experiment 2 (v2 DRAFT, 2026-10-06)

**Status: v2 FROZEN 2026-10-06 ~19:00 (driver v3.1; advisor v3 PROCEED, `results/c10r_exp2ctl_advisor_v3.md`) — replaces the zero-preserve design** (`docs/C10R_EXP2_ZEROPRESERVE_PREREG.md`, now SUPERSEDED, kept as written). Same decision (D-C10r-exp2ctl, operator ruling 2026-10-06 ~16:10: one control of about an hour in the step-1 break), sharper question. Driver to be rebuilt by Codex against §2–§4, then a Claude advisor pass, then freeze. Nothing has run.

## 0. Why the design changed

Two reviews of v1 agreed that its run was nearly foregone. With `PRESERVE_WEIGHT = 0.0` the solve is the baseline's equation (`fd16592:edit.py:64,72` vs `92acd03:edit.py:97-99`), and the baseline's saved weights are bit-identical across three separate processes (A1/A2/A7 `saved_sha256` `2f72fee2…`, `f94e1be2…`, `c30664a9…` in `results/autoresearch_c10_equivalence_2026-10-06T0815.json`, `results/autoresearch_c10_equivalence.json` and the loop's baseline score; all nine full values verified in `results/c10r_exp2ctl_codex_redesign_v1.md` §1). So v1 would most likely print 7/72 by arithmetic, and it could not separate "preserving the value-token keys helps" from "experiment 2 simply made a larger change" (`dw_total` 88.974 → 131.421, +47.7 %).

**Reviewer disagreement, recorded.** The Claude advisor (`results/c10r_exp2ctl_advisor_v1.md`, FIX-FIRST) recommended spending the slot on v1 with a bit-identity gate and running a location control later. Codex (`results/c10r_exp2ctl_codex_redesign_v1.md`, gpt-6.1-sol max) recommended the location control as the one slot, keeping the zero-weight replay as a later identity diagnostic. **Program decision: the location control** — it is the only one-slot run that can falsify the claim the loop's win rests on; the zero-weight outcome is already predicted by the recorded identity evidence.

**The e2e map:** write layer, compile step (§8.1 D20 solve: the preserve side of the normal equations). Engine unmodified (d941a9fb); the loop's `prepare.py` and harness used as-is.

## 1. Question and hypotheses

- **H-location:** the gain needs the preserve keys to sit at the value-token positions.
- **H-geometry:** any count-matched preserve matrix (a generic constraint, or a larger update) is enough.
- **Premise stated, not tested:** the recorded 18/72 run (`runs/20261006-142644_nocommit`) executed `92acd03`; its score says `commit=nocommit`, so the link rests on the loop ledger (`results.tsv` row 4, dw 131.4 = 131.421).

## 2. Design (one edit + one scoring pass, ≈ 50 min GPU)

- **Isolation:** a standalone clone of the loop sandbox at `92acd0378d23f4935df9a8bccc0137b36695a40f`; the loop's checkout untouched; the loop stopped for the whole window.
- **The only science change:** `PRESERVE_WEIGHT` stays 1.0; the existing value-key capture (same forward pass, same inputs) gathers its `Kp` columns from **common words of the canonical prompt** instead of from the appended value tokens. Exact rule (frozen by pointer): `results/c10r_exp2ctl_codex_redesign_v1.md` §3.1 lines 84–123 — seven candidate word positions (The / capital / of / is / the / city / of) located by the tokenizer's offsets in each wrapped prefix; for fact `f`, template `q` and value length `m`, `start = (f + q) % 7`, indices `C[(start + j) % 7]` for `j < m`; exactly `m` distinct columns per fact, template, layer and arm, so the column count matches the real `Kp` everywhere (A1 144, A2 288, A7 792 per layer). Applied to all three arms. Checked read-only on the cached tokenizer for all 432 fact/template pairs (§3.5 of that file). **Amendment A1 (2026-10-06, after the advisor's v2 review, issue 6): an occurrence at absolute token position 0 is removed from the candidate list** (it is the attention-sink position — in the bare `{}` template "The" sits there; value tokens never can). The candidate list is then K = 6 or 7 occurrences; `start = (f + q) % K`, indices `cand[(start + j) % K]` for `j < m`; `m ≤ K` holds because the longest value is 6 tokens. Counts stay exactly matched.
- **Provenance and readout additions (inert, logging only):** executed `edit.py` hash; edit-time context-template list and hash; per-arm records with arm id and an invocation id; the position manifest; the value-position block's norms for audit only; per-layer pre-cast update norms and `‖P Kp‖_F` for both key sets.
- **Order in the break:** after step 1's stages (D-C10s-sharedz), before the loop relaunch.

## 3. Validity (any failure → INVALID, HALT, exit 2, no label)

Codex §3.4 items 1–9 (lines 228–250) are adopted as the gate list; in short: frozen source + exact permitted diff, hashes recorded before launch; engine fingerprint run before dispatch with `LLMDB_ROOT` set to the program root; exactly three provenance records (A1, A2, A7) whose edit-time context hash equals `e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330` and scorer `templates_sha = e8605172dce0`; the count/position manifest and an identity check of the gather primitive on the same captured forward; an exclusive-GPU window enforced by a full process check before, after preflight and during the run; `seed = 0`, `edit_budget = 2700`, `edits.commit = "92acd03"`; `law5_ok` and `scope_ok` true; A1 and A2 each ≥ 68; one fresh run directory and one score bound to the invocation by a runner receipt; malformed input → INVALID; a fidelity manifest (interpreter, package versions, OS, configs, tokenizer/model revision).

**Mid-run process events (advisor v3, N1).** Before dispatch, any contender or probe failure refuses the launch (nothing consumed). During the run, a contender must be seen on 3 consecutive polls, or the probe must fail 3 times in a row, before the run is marked INVALID; the run is not stopped for it, and an INVALID mark is final at read time. The only process the runner ever stops is its own tree.

**Launch procedure (in the step-1 break):** (a) `bash experiments/track_c/autoresearch_c10/replay_exp2/setup_replay.sh` (standalone clone at 92acd03 in `/Volumes/memit/llm-database-poc-mirror/autoresearch_replay_c10_exp2loc`; refuses any diff but the frozen patch); (b) `.venv/bin/python experiments/track_c/autoresearch_c10/replay_exp2/tokenizer_precheck.py <DEST>` (tokenizer only, no model; the runner refuses without its fresh pass record); (c) with the loop stopped and no other model job, `REPLAY_EXCLUSIVE_WINDOW=paused-no-relaunch bash experiments/track_c/autoresearch_c10/replay_exp2/run_replay.sh <DEST>` (fingerprint, process check, MPS, then the ≈ 50-min edit + score; it invokes the reader and writes `run.rc`); (d) Codex at the verdict; the result goes to the register as a candidate note, not CORPUS.

## 4. Pre-registered readings (frozen)

Let H = held-out full reads /72; C = hits on the 16 facts whose value head is also a subject (Drennik, Vythorn, Vorlex, Kessivar, Halquin, Marsduq, Glimsto, Fluvane); O = the other 8 facts; D = `dw_total`. Recorded endpoints: baseline H 7, C 0, O 7, D 88.974; experiment 2 H 18, C 13, O 5, D 131.421.

**Primary label (H):** 0–7 **NO-GAIN-WITHOUT-VALUE-POSITIONS**; 8–17 **PARTIAL-GAIN**; ≥ 18 **FULL-GAIN-WITHOUT-VALUE-POSITIONS**.
**Secondary label (C):** 0 **NO-COLLISION-RECOVERY**; 1–12 **PARTIAL-COLLISION-RECOVERY**; ≥ 13 **FULL-COLLISION-RECOVERY**.
**Quality:** any failed locality guard → `quality = DEGRADED` beside the labels; it never turns a high H into support for H-location. **Comparability:** the reader prints, per layer, control/real ratios of the summed squared key norms and of ‖P Kp‖_F; if either ratio exceeds 10 or falls below 0.1 at any layer, `control not norm-comparable` is printed beside the labels and no mechanism reading is drawn.

**What the readings mean:**
- H ≥ 18 and C ≥ 13, guards pass → **H-location falsified for this gain**: the value positions are not needed; a generic preserve constraint or a larger update suffices. The loop's mechanism story does not stand; the candidate becomes "a preserve constraint helps".
- H ≤ 7, C = 0, guards pass, D ≥ 131.421 → **H-location survives**: a count-matched constraint at ordinary words, with an update at least as large, gives no gain. The head-trigger mechanism itself stays unproven.
- H ≤ 7 with D < 131.421 → size confound remains; no mechanism label.
- Anything else → partial or mixed, reported as such.

**No noise band.** The thresholds are the two recorded endpoints, not confidence limits. The ±4–5 cross-process spread in CORPUS/50 belongs to the unseeded harness; this seeded stack reproduces bit-for-bit, and the control's own run-to-run spread is unknown until repeated.

## 5. Not claimed, whatever the outcome

No CORPUS label changes. Not §8.9 closure, not a route change, not F1. Recorded as a register candidate note + runbook §5.2/§13 + `results/`, not a CORPUS entry (loop findings are candidates, docs/AUTORESEARCH.md). Experiment 2's own 18 is not reproduced here.

## 6. Halt discipline

One speculative fix after a `cat -n` read, then HALT with `architecture_profile/s_exp2ctl_halt_diagnostic.json`.

## 7. Review log

- driver v3 → live process check by the program (only the loop's tree flagged after the v3.1 contender fix) + offline suite 26 PASS → advisor v3 PROCEED (`results/c10r_exp2ctl_advisor_v3.md`; all 7 v2 issues fixed; N1 folded as the §3 text above) → **v2 FROZEN**.
- v2 driver (Codex) → advisor v2 FIX-FIRST (`results/c10r_exp2ctl_advisor_v2.md`: the process check would refuse on the operator's tools and kill its own editor's helper; refused launches consumed the clone; labels printed on INVALID; tokenizer equality unchecked; the sink position) → Amendment A1 + comparability rule (this text), driver v3.
- v1 (zero-preserve) → advisor FIX-FIRST (`results/c10r_exp2ctl_advisor_v1.md`) + Codex redesign (`results/c10r_exp2ctl_codex_redesign_v1.md`) → v2 (this draft): location control, gates from both reviews; reviewer disagreement on priority recorded in §0.
