PROCEED-WITH-CHANGES

# Advisor review: D-C10v-layerpick verdict packet (step 4, pass1)

Reviewer: independent advisor (Opus), read-only. Every number below was recomputed from the JSON with stdlib python (`/usr/bin/python3 -I`); no `.venv` python and no model code was run. Root `<wt>` = `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`.

## Summary judgement

The labels are right. Under `docs/C10V_LAYERPICK_PREREG.md:64–72`, B, B0 and Bshuf are all NULL:
- Every recipe passes validity (`pass1.json .recipes.<R>.validity` = `{"ok": true, "reasons": []}` for all four).
- The counts are B 12, B0 12 and Bshuf 10 (`.recipes.<R>.arms.A7_coined_coined.para_full_n`). All three are inside [5, 18], and the gains over A are +1/+1/−1.
- B's `described_as` miss (86.17 < 90.0 − 3) cannot produce TRADEOFF without a PARTIAL- or LEAD-sized gain (`:71`). It is reported, not a label qualifier.
- No write ratio exceeds 1.5 (0.6435 / 0.8674 / 1.0874, recomputed from `.delta_norms.A7_coined_coined`).

`run.json .readings` matches. sha256(pass1.json) = `bf8f162a…119f` = `run.json .pass_sha256.pass1` = `pass1_complete.json .record_sha256`. Every gate value, per-fact vector, per-template split, by-layer table, margin count, HSIC value and proxy median in the packet reproduces exactly. The packet is careful work.

Three things need to change before CORPUS:
1. The headline over-claims a null effect.
2. A disclosure the runbook binds to close-out is missing.
3. Two pre-registered "reported" readouts are left out, and one of them is the most informative mechanistic result of the run.

## BLOCKING

**B1. The headline turns "not advanced" into an effect claim.** The proposed headline (packet §6) says "placing each fact at its argmax-G band layer **does not move held-out recall**". The prereg allows a miss to mean only "*this candidate configuration was not advanced* — one selector, one map, one solve budget, one seed, N = 24" (`:11`). It also says NULL "does not close … per-fact selection in general" (`:82`). The data are a +1/72 difference, one seed, no interval. The headline also hides the secondary readouts that did move, adversely: canon 9 → 7 and `tf_pertok_cont` 60.8 → 54.0 (`.arms.A7_coined_coined`). The program's own precedent words a sub-margin result as "below the pre-registered +10 margin" (CORPUS/53, runbook :49).

Replace the headline with:

> `CORPUS/56 — C10V layer pick (step 4): NULL ⟨D-C10v-layerpick@<commit>⟩ — per-fact single-layer placement at the argmax-G band layer (B) scored 12/72 held-out A7 para_full against the same-process band 4–8's 11/72 (+1; inside the [5, 18] envelope and below the +10 margin), with fixed layer 8 (B0) 12/72 and the shuffled map (Bshuf) 10/72, so B beat neither control and the selector was not credited; B also missed the described_as locality gate (86.17 vs ≥ 87.0). This configuration is not advanced; not depth closure, not §8.9 closure, no F1 change, no LOKI or WilKE evidence. C10 OPEN/BLOCKING; F1 unchanged.`

In the one-line verdict, replace "The candidate is not advanced" with "This candidate configuration (one selector, one map, one seed, N = 24) is not advanced (prereg :11)".

**B2. The delegated-go disclosure must appear in the CORPUS/56 body.** `EXPERIMENT_RUNBOOK.md:363` (D-C10v-go) says the go was delegated and is "to be disclosed again at close-out (as for step 3 r3)". The precedent it names discloses the equivalent deviation in the CORPUS body (`CORPUS/54_C10U_MINT2.md:13`). The packet leaves this open (Q10), and leaving it out would break a recorded ruling. Add to the CORPUS/56 provenance paragraph:

> `Go basis: the prereg's "runs only on the operator's go" (:3, :86) was met by a DELEGATED go (EXPERIMENT_RUNBOOK.md:363, D-C10v-go: the operator's standing approval under D-C10r-rulings-8 and the overnight queue directive D-C10r-rulings-9), disclosed here as that ruling requires. Its caveat that step 3's r3 ratification was still owed was resolved before pass1 completed by the operator's own "Yes on all 5" (EXPERIMENT_RUNBOOK.md:364, D-C10r-rulings-12 Q2). Pass artifacts are committed in d8af793.`

(The last sentence also corrects packet §0's stale "untracked" line. `git log -1 -- results/c10v_layerpick/pass1.json` returns d8af793.)

**B3. Two pre-registered readouts are missing.** `:76` lists three items as "Reported, not gated": the realised count by assigned layer (present), the Spearman (present), and "the proxy's prediction error on the canonical activation change" (missing). `:54`, with fold item A-8 at `:102`, pre-registers A1's remaining ratios to answer "whether realisation at the keyed position separates A1 from A7 at all — never measured". The packet reports A7 only. Recomputed from `pass1.json .recipes.<R>.arms.<arm>.extra.proxy.rows[*]`, as medians over 24 facts (held-out = medians over the 72 `rho_per_prompt[1:]` values):

| recipe | A1 ρ canon / held-out | A7 ρ canon / held-out | A7 prediction_error (realised − group G) median, median abs, max abs |
|---|---|---|---|
| A | 0.031 / 0.207 | 0.030 / 0.195 | +0.040, 0.040, 0.062 |
| B0 | 0.067 / 0.207 | 0.067 / 0.208 | −0.007, 0.010, 0.036 |
| B | 0.053 / 0.182 | 0.057 / 0.181 | +0.011, 0.016, 0.035 |
| Bshuf | 0.087 / 0.201 | 0.078 / 0.208 | +0.005, 0.016, 0.062 |

(`prediction_error` = `realised_fraction − group_G_diagonal`, `c10v_layerpick_arms.py:428`; weight application fp16, `.extra.proxy.weight_application`.)

Add to CORPUS/56 under "Reported, not gated" (keep the `EVIDENCE-SHOWS` / `I-INFER` split):

> `EVIDENCE-SHOWS: under band A, A1 (70/72) and A7 (11/72) leave the same residual at the keyed position (median remaining ratio canonical 0.031 vs 0.030, held-out 0.207 vs 0.195); the same holds under B0, B and Bshuf. G predicts the realised canonical fraction to a median |error| of 0.010–0.016 for the single-layer recipes (max 0.036 for B, fp16 application). I-INFER: the A1/A7 behavioural gap does not come from how much residual the write installs at the keyed position, and G is an accurate proxy for a quantity that does not track held-out recall here — mechanics ≠ contract.`

This answers Q8. The per-fact readouts were pre-registered (`:54`). Only the median summary is the author's choice, and it should be labelled as such, not left out.

## Non-blocking notes

**N1. δ = 0, so the margin rule never applied (Q3).** `step0.json .delta` = 0.0. `.G_table == .G_table_repeat` and `.winning_margins[0] == [1]` exactly, so no winner was absorbed into "nearest 8". The prereg's own expectation (`:36`, "a concentrated map (stop fires) or hair-width variation (absorbed by δ)") failed in both forms: the map spreads 15/5/2/1/1 (`.concentration` 15), and the near-ties stand (3 margins < 2e-3, 11 < 1e-2; minimum Vorlex 8.9e-4). The 24/24 cross-process agreement (`pass1.json .selection_agreement_n`) used frozen contexts (`.ctx_sha256` equal; `arms.py:493`), so how stable the selector is under context resampling was never measured. This does not change a NULL, but a reader of the entry needs it to understand which map was tested. Suggested sentence:

> `The margin rule was inactive (δ measured as 0.0, bit-identical in-process repeat; D-C10v-implfix, runbook :349), so B is the raw argmax map, 11 of 24 winners leading by < 0.01 in G; the map's stability under context resampling was not measured (pass1 reused step 0's contexts).`

**N2. `-CONTROL-ONLY` (Q2).** `:68` reads Bshuf "by the same rules as their own candidates", so its prereg label is NULL (`run.json .readings.Bshuf.base_label`). Print `NULL (shuffled-map control; reader string NULL-CONTROL-ONLY, c10v_layerpick_read.py:386–388)`. Do not present the suffix as a prereg label.

**N3. B's collateral profile, reported as observations rather than tested contrasts (Q4).** B's numbers differ from A's as follows, none of which gates a NULL:

| readout | A | B |
|---|---|---|
| A1 `para_full_n` | 70 | 68 (exactly at the `:66` floor) |
| A2 `para_full_n` | 71 | 70 |
| A7 canon | 9 | 7 |
| `tf_pertok_cont` | 60.8 | 54.0 |
| `described_as` | 90.0 | 86.17 |

All values are from `.recipes.<R>.arms.*`. CORPUS should carry one line ("B's A1 = 68/72, at the validity floor; A2 70; canon 7/24 vs A's 9; no gate beyond described_as failed"). Without it, "same locality and write size" (H-V1, `:15`) reads cleaner than the run was.

**N4. Spearman (Q7).** The recorded statistic correlates G at the assigned layer with the binary 3/3 edge vector, which has 2 positives for B0, 1 for B and 2 for Bshuf (`.readings.<R>.per_edge_3of3`; `read.py:375`). With one positive, B's −0.316 reduces to where a single fact ranks. Against per-fact hit counts 0–3 (the "per-fact outcomes" of `:76`), recomputed with the reader's tie-ranking:

| recipe | vs hit counts | vs 3/3 edges (recorded) |
|---|---|---|
| B0 | −0.387 | −0.479 |
| B | −0.056 | −0.316 |
| Bshuf | +0.142 | +0.196 |

Report both, with the count of positives. Neither is gated.

**N5. B0 is the program's first single-layer arm (`:42`).** Layer 8 alone scored 12/72 against the band's 11/72 at 0.64 of the band's summed write norm, with all locality gates held. It is NULL and earns nothing under `:78`. It is still a new observation, and CORPUS should record it as one: "a single layer-8 write matched the band 4–8 count at about two-thirds of its write norm (one seed)". It should not be stated as a claim.

**N6. Where the gates live (Q5).** `run.json` pins `pass1.json` by sha256 (`.pass_sha256.pass1`), and `read.py:448–450` enforces that. `pass1.json` carries `.fingerprint` (`ok`, `d941a9fb…3d65`, `_cov_cpu` 3), `.published_map_sha256`, and `.step0` (G table, δ, `ctx_sha256`). Reading "run record" as that hash-pinned pair satisfies `:66`. In CORPUS, cite `pass1.json .fingerprint` and `step0.json .delta/.map_sha256/.ctx_sha256` directly rather than `run.json` alone.

**N7. LAW#5 (iii)–(v) are not vacuous, but (iii) is weak (Q6).**
- (iii) With the identity map, the wrapper takes the single-group branch (`arms.py:287`) and calls the original `my_edit` with a deep-copied hp of the same layers, the same `P` objects, fresh zero caches (`:295`; `capture_write` already passes zeros) and a rebuilt override dict. It is the same computation by construction. It proves the plumbing (override rebuild, hp copy, projector selection) is inert. It does **not** exercise grouped execution.
- (iv) This check catches a wrong projector index, which is what it was built for.
- (v) This is the substantive test (`:370` onward). Layer 6 is written first, from pristine weights. Layer 5 is written after layer 6, and it reproduces its lone write bit-exactly only if the descending-order premise holds. An ascending order would have failed it.
- The exact zeros mean the arithmetic is bit-deterministic within one process on this machine; they are not a self-comparison.

CORPUS should describe (iii) as "wrapper plumbing inert", not "grouped path inert".

**N8. Next step (Q9).** `:78` says "the sequence moves to gate A / step 5". Step 5 P1 is closed as CORPUS/55, and P2 has the GPU under D-C10r-rulings-12 Q1 (`EXPERIMENT_RUNBOOK.md:364`) and D-C10w-p2go (commit d8af793). Write "not advanced; the sequence continues with step 5 (P2 running, D-C10r-rulings-12/D-C10w-p2go)". This keeps the prereg's wording traceable.

**N9. The by-layer table points the same way as the controls.** This is an inference, not a test. Bshuf's layer-6 group (15 facts reassigned) scored 10 hits, against 7 for B's own layer-6 group (`.readings.<R>.by_layer["6"]`). B's two layer-8 facts scored 0, while B0 put every fact at layer 8 and scored 12. Report this only as the pre-registered by-layer readout, not as evidence against G.

**N10. Drift check.** This is a write-path (§C) placement candidate, explicitly not F1-moving (`:82`). The result correctly declines a step and does not reroute anything. No drift.

**Overturning test (for the record, not required under NULL):** the cheapest falsifier of "this configuration is not advanced" is a second seed or context resample of step 0 plus B. It would test whether the near-tie map (N1) is a representative draw. The prereg does not require it under NULL, and it should not be run ahead of step 5.

## Proposed one-sentence CORPUS verdict

> D-C10v-layerpick = **NULL**: per-fact single-layer placement at the argmax-G band layer (B, raw argmax since the measured δ was 0.0) scored 12/72 held-out A7 para_full against the same-process band 4–8's 11/72, inside the [5, 18] envelope and below the +10 margin, and beat neither fixed layer 8 (B0, 12/72) nor the shuffled map (Bshuf, 10/72). Every validity gate and LAW#5 (i)–(v) passed, B missed the described_as locality gate (86.17 vs ≥ 87.0), and no replication was triggered. This one-selector, one-map, one-seed, N = 24 configuration is not advanced, and depth and per-fact selection in general are not closed.
