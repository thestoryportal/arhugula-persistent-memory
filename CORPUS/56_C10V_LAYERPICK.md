# 56 — Per-fact layer pick (step 4), pass1: NULL — not advanced under the preregistered rules

**VERDICT (CORPUS/56 — C10V layer pick, step 4): NULL ⟨D-C10v-layerpick@3bcae852⟩ — not advanced under the preregistered rules.** The frozen argmax-G placement candidate did not meet the preregistered advancement threshold in pass1: B 12/72, fixed-layer-8 B0 12/72, shuffled-map Bshuf 10/72, versus band 4–8 A 11/72. B's +1 is inside the [5, 18] envelope and below the +10 margin, so B beat neither control and the selector was not credited; B also missed the `described_as` locality gate (86.17 against ≥ 87.0). This configuration (one selector, one map, one solve budget, one seed, N = 24) is not advanced (prereg :11). Not depth closure, not §8.9 closure, no F1 change, no LOKI or WilKE evidence. C10 OPEN/BLOCKING; F1 unchanged.

_Record 2026-10-07 (pass1 completed 2026-10-08T03:32:38Z = 2026-10-07 21:32:38 MDT). Decision-ID D-C10v-layerpick. Pre-registration `docs/C10V_LAYERPICK_PREREG.md` v2 FROZEN (step 4 of the research-pass sequence, H-8). Run directory `results/c10v_layerpick/`, run_id c10v-bea2183a…, source digest 97470c0e…; stages step0 (pid 19153, 02:22:26Z) → LAW#5 (pid 79246, 02:49:56Z) → pass1 (pid 79246, 02:54:27Z → 03:32:38Z); `results/c10v_layerpick_logs/pass1.log` ends `C10V_PASS1_COMPLETE` then `STAGE_EXIT=0` (lines 362–363 of the current file; stage logs other than step0.log are gitignored by `*.log`). pass2 not run. Model Qwen/Qwen2.5-3B@3aab1f19, float16, MPS (`pass1.json` `model`). Engine unmodified, fingerprint d941a9fb…3d65 ok, `_cov_cpu` 3 (`pass1.json` `fingerprint`; the same block in step0, law5 and pass1_started). Reader `experiments/track_c/c10v_layerpick_read.py` (last commit 9120bd6); its output equals `run.json` `readings`; it re-hashes all 71 pinned sources in `identity.json` `source_sha256` against the tree (Astra re-ran it: rc 0, byte-identical). Record integrity: sha256(`pass1.json`) = bf8f162a…119f = `run.json` `pass_sha256.pass1` = `pass1_complete.json` `record_sha256`. **Artifact provenance:** all seven run JSONs (identity, step0, law5, pass1_started, pass1, pass1_complete, run) are committed in d8af793 (the verdict packet's "untracked" line is stale). **Go basis:** the prereg's "runs only on the operator's go" (:3, :86) was met by a DELEGATED go (EXPERIMENT_RUNBOOK.md:363, D-C10v-go: the operator's standing approval under D-C10r-rulings-8 and the overnight queue directive D-C10r-rulings-9), disclosed here as that ruling requires. Execution proceeded under the delegated go recorded in D-C10v-go, rather than a separate C10V-specific operator instruction. **Step-3 ratification note:** D-C10v-go's caveat that step 3's r3 ratification was still owed was resolved before pass1 completed, by the operator's own "Yes on all 5" (EXPERIMENT_RUNBOOK.md:364, D-C10r-rulings-12 Q2, ~21:08 MDT; pass1 ran 20:54–21:32 MDT). Verdict reviews: GPT-6-Astra high and Opus advisor, both PROCEED-WITH-CHANGES; every BLOCKING item is folded below (see Reviews). Lineage: CORPUS/37–39 and 44 (earlier layer configurations not advanced) ⟨D-C10l-covgeom@af2e38f7⟩, CORPUS/55 ⟨D-C10w-oracle@6a735469⟩ (step 5, interim)._

## What was tested

Every earlier layer sweep gave all 24 facts the same layer set. Step 4 asks whether the edited layer should differ per fact (H-V1, prereg :15). Step 0 computes, for each fact and each band layer 4–8, the lone-write coefficient `G` of its key (a selection proxy, prereg :31–32) and assigns each fact to its argmax layer. Four recipes then ran in one process, each with the A1, A2 and A7 arms: **A** the fixed band 4–8 (the harness as it stands); **B0** every fact at layer 8; **B** the per-fact map; **Bshuf** the map's assignments shifted among subjects with group sizes kept (18 of 24 assignments changed, `pass1.json` `shuffled_changed_n`). B0 and Bshuf are the controls that decide attribution: the selector is credited only if B beats both by ≥ 10/72 (prereg :76).

**The map.** Layer 6: 15 facts, 5: 5, 8: 2, 4: 1, 7: 1 (`step0.json` `map`); concentration 15 < 20, so the stop rule did not fire (`concentration`, prereg :35). The margin rule was inactive: δ was measured as 0.0 (bit-identical in-process repeat, `G_table` = `G_table_repeat`; `arms.py:169–176` recomputes the keys on each repeat), which the program ruled a measurement, not a defect (D-C10v-implfix, EXPERIMENT_RUNBOOK.md:349). B is therefore the raw argmax map: 3 of 24 winners lead by < 0.002 in G, 6 by < 0.005 and 11 by < 0.01 (minimum 0.00089, Vorlex, layer 5 over layer 6; `step0.json` `winning_margins`). The map reproduced exactly under frozen contexts: pass1 recomputed step 0 in its own process and agreed 24/24 (`selection_agreement_n`), but it reused step 0's contexts (`arms.py:493`; `ctx_sha256` 91c1a4e7… in both), so robustness to context resampling was not measured. These narrow margins do not by themselves show the map is unstable. This bounds the NULL to this near-tie map; it does not invalidate it. Map hash f2bdd9df…6183 (`step0.json` `map_sha256` = `pass1.json` `published_map_sha256`). Reported comparison (not a gate): `max_ℓ G` 0.947–0.995 against the band's installed share 0.956–0.983 per subject (`installed_share_comparison`).

## Validity (prereg :66) — every recipe VALID

| Gate | Recorded | Source |
|---|---|---|
| Engine fingerprint, `_cov_cpu` | d941a9fb ok, 3 | `pass1.json` `fingerprint` |
| LAW#5 (i)–(v) | INERT (detail below) | `law5.json` `law5` = `pass1.json` `law5` |
| Map reproduced in-process | δ 0.0, `map_reproduced` true, status READY | `step0.json` |
| A1 / A2 ≥ 68 under each recipe | A 70/71, B0 70/71, **B 68**/70, Bshuf 70/71 | `recipes.<R>.arms.A1_single`, `A2_coherent2` `para_full_n` |
| Recipe A A7 in [5, 18], canon in [5, 10] (LAW#3) | 11/72, 9/24 | `recipes.A.arms.A7_coined_coined` |
| `Z_OVERRIDE_HITS` = non-empty groups | A 1, B0 1, B 5, Bshuf 5 | `recipes.<R>.wrapper` |
| Map hash, G table, δ, template hashes | present | `pass1.json` `published_map_sha256`, `step0.G_table`, `step0.delta`, `ctx_sha256` (run.json pins pass1.json by hash; `_cov_cpu` is not in run.json itself) |
| `para_full_string` = `para_full` | equal in every arm | `recipes.<R>.arms.*` |
| Reader validity block | `{"ok": true, "reasons": []}` ×4 | `recipes.<R>.validity` |

B's A1 is 68/72, exactly at the inclusive floor and two below the other recipes' 70; it passes, and it is reported rather than called unchanged.

**LAW#5, as recorded.** (i) the standing gate: |Δexpr| 0.0003, Δloc 0.03, no override hits. (ii) floor, (iii) identity map, (iv) single layer, (v) two largest groups (layer 6 then layer 5): every recorded relative update distance is 0.0, with tolerance at the 1e-4 clamp (`law5.json`). These are recorded update-distance zeros under the tested conditions: separately computed tensors from restored weights in one process on this machine, not a self-comparison, and not a claim of universal determinism. (iii) shows the wrapper plumbing is inert (override rebuild, hparams copy, projector selection); it does not exercise grouped execution. (iv) checks the projector index. (v) is the substantive check: layer 5 written after layer 6 reproduces its lone write, as the descending-order design requires. The raw audit tensors and their absolute norms are not kept in `law5.json`, so a nonzero magnitude for each comparison is UNVERIFIABLE from that file alone. The four per-recipe standing-gate blocks are cached copies of one check (`arms.py:445–447`), not four checks.

## Reading under the prereg (:64–:78, in order)

| Recipe | A7 held-out `para_full` | vs A | Per template | 3/3 facts | Write ratio vs A | Label |
|---|---|---|---|---|---|---|
| A (reference) | 11/72 | — | 3 / 3 / 5 | 2 | 1 | — |
| B0 | 12/72 | +1 | 3 / 3 / 6 | 2 | 0.644 | NULL |
| B | 12/72 | +1 | 3 / 3 / 6 | 1 | 0.867 | NULL |
| Bshuf | 10/72 | −1 | 2 / 4 / 4 | 2 | 1.087 | NULL (shuffled-map control) |

Sources: `recipes.<R>.arms.A7_coined_coined.para_full_n`; `run.json` `readings.<R>` (`per_template`, `per_edge_3of3`, `write_ratio`, `label`). Summed A7 write norms: A 86.12, B0 55.42, B 74.70, Bshuf 93.65 (`delta_norms.A7_coined_coined`).

1. Validity: all four recipes valid (above).
2. Count: none ≥ 30 (no LEAD); none > 18, and a count inside [5, 18] is NULL whatever the gain (:70).
3. Locality and write size (:74): B misses `described_as` (86.17 < 90.0 − 3 = 87.0). TRADEOFF needs a PARTIAL- or LEAD-sized gain first (:71), so the miss does not change the label, but it stands as a recorded gate failure. No write ratio exceeds 1.5, so no -LARGE-WRITE.
4. Label (:72): NULL for B, B0 and Bshuf. Bshuf is printed **NULL (shuffled-map control)**: its prereg label is NULL (`run.json` `readings.Bshuf.base_label`); the reader appends `-CONTROL-ONLY` to mark its role (machine string `NULL-CONTROL-ONLY`, `c10v_layerpick_read.py:386–388`), which is not a prereg label.
5. Attribution (:76): reached only by a LEAD or PARTIAL on B; not reached (`attributed` null).
6. Replication (:76): triggered only by PARTIAL or LEAD on B or B0; not triggered (`replication_needed` false), so pass2 correctly did not run.
7. What it buys (:78): not advanced; the depth question joins CORPUS/37–39 and 44 as not advanced on this harness — not closed.

**Locality, A7 against A (`recipes.<R>.arms.A7_coined_coined`).** L1 flips 0/12 for all four; same-frame flips 1/6 for all four; `described_as` A 90.0, B0 90.11, **B 86.17 (miss)**, Bshuf 87.37; L3 30/30 for all four; generic perplexity A 21.502, B0 21.710, B 21.713, Bshuf 21.698 (limit 22.002; pre-edit 21.755). Relation-label flips (reported, no threshold), bystander / objective-anchored: A 9/23, B0 9/22, B 7/23, Bshuf 6/22.

**Secondary readouts and B's collateral profile (observations, not tested contrasts).** Canonical 9 / 7 / 7 / 6 of 24 (A / B0 / B / Bshuf); first token 45 / 45 / 44 / 42 of 72; `tf_pertok_cont` 60.8 / 59.0 / 54.0 / 52.8. B against A: A1 68 vs 70 (at the validity floor), A2 70 vs 71, canon 7 vs 9, `tf_pertok_cont` 54.0 vs 60.8, `described_as` 86.17 vs 90.0; no gate beyond `described_as` failed. H-V1's "same locality and write size" (:15) does not read cleaner than this.

**B0, the program's first single-layer arm (:42).** A single layer-8 write matched the band 4–8 count (12 vs 11/72) at 0.64 of its summed write norm, with every locality gate held (one seed). It is NULL and earns nothing under :78; it is recorded as an observation, not a claim.

## Reported, not gated (prereg :54, :76)

**Count by assigned layer** (`readings.<R>.by_layer`, facts / hits of 72): B — layer 4: 1 / 0; 5: 5 / 4; 6: 15 / 7; 7: 1 / 1; 8: 2 / 0. Bshuf (same group sizes) — 4: 1 / 0; 5: 5 / 0; 6: 15 / 10; 7: 1 / 0; 8: 2 / 0. B0 — 8: 24 / 12. Bshuf's layer-6 group scored more than B's (10 vs 7), and B's two layer-8 facts scored 0 while B0 scored 12 with every fact at layer 8. This is the pre-registered by-layer readout, not evidence against G.

**Per-fact hits** (0–3 per fact, subject order of `step0.json` `subjects`; `recipes.<R>.detail.A7_coined_coined[*].para_full_hits`): A `300000000301120000000100`, B0 `300010000301020010000100`, B `300020000200000021000101`, Bshuf `300000000202000030000000`; B's assigned layers `668656566564666566865667`. B0 and B have the same total and per-template split but differ on 7 of 24 facts.

**Spearman of G at the assigned layer against per-fact outcomes**, both codings (reader `:367–375` uses the binary 3/3 edge): against 3/3 edges (positives 2/24, 1/24, 2/24) B0 −0.479, B −0.316, Bshuf +0.196; against 0–3 hit counts B0 −0.387, B −0.056, Bshuf +0.142 (recomputed with the reader's tie ranking from `pass1.json`). With one positive, B's −0.316 reduces to where a single fact ranks; the change to −0.056 under the count coding shows how much the outcome coding matters. Neither is gated, and neither supports a claim about G's predictive value in general.

**Proxy prediction error on the canonical activation change (:76).** `prediction_error` = realised fraction ⟨Δh, r_i⟩/‖r_i‖² at the canonical keyed position − the group-only `G[i, i]` (`c10v_layerpick_arms.py:428`), weight application fp16 (`extra.proxy.weight_application`). A7, over 24 facts — median / median |error| / max |error|: A +0.040 / 0.040 / 0.062; B0 −0.007 / 0.010 / 0.036; B +0.011 / 0.016 / 0.035; Bshuf +0.005 / 0.016 / 0.062.

**A1-vs-A7 remaining ratio at the keyed position (:54, fold item A-8).** Median canonical remaining ratio over 24 facts / median held-out over the 72 pooled held-out prompt ratios (`extra.proxy.rows[*].rho_per_prompt`):

| Recipe | A1 canonical / held-out | A7 canonical / held-out |
|---|---|---|
| A | 0.031 / 0.207 | 0.030 / 0.195 |
| B0 | 0.067 / 0.207 | 0.067 / 0.208 |
| B | 0.053 / 0.182 | 0.057 / 0.181 |
| Bshuf | 0.087 / 0.201 | 0.078 / 0.208 |

The medians are this entry's summary choice; the per-fact values are the pre-registered readout. Across recipes the numbers are not in common coordinates (A measures against layer-8 targets, the B family against separately solved targets at the assigned layers, `arms.py:238–257, 413–430`), so the pooled residual-ratio diagnostic differed across recipe-specific target layers and did not establish a behavioural placement lead.

EVIDENCE-SHOWS: under band A, A1 (70/72) and A7 (11/72) leave the same residual at the keyed position (median remaining ratio canonical 0.031 vs 0.030, held-out 0.207 vs 0.195); the same holds under B0, B and Bshuf. G predicts the realised canonical fraction to a median |error| of 0.010–0.016 for the single-layer recipes (max 0.036 for B, fp16 application). I-INFER: the A1/A7 behavioural gap does not come from how much residual the write installs at the keyed position, and G is an accurate proxy for a quantity that does not track held-out recall here — mechanics ≠ contract. These proxy numbers are descriptive only.

**HSIC diagnostic** (A7, layer-8 pristine residuals, never selector or gate; `pass1.json` `hsic`): its per-fact argmax agrees with ℓ* on 4/24; `HSIC_b` by layer 4–8 = 0.00685, 0.00689, 0.00687, 0.00714, 0.00700.

## Not claimed

Not "placement does not move recall": the observed difference is +1/72 at one seed with no interval, and NULL is a decision not to spend further, not evidence of zero effect. Not depth closure, not per-fact selection in general, not selectors other than G (prereg :82). Not selector stability: the map's robustness to context resampling is unmeasured. Not §8.9 closure, not a route closure, not an F1 change, not evidence about LOKI or WilKE. No label in CORPUS/37–55 changes. Engine unmodified.

## Decision-ID and next step

D-C10v-layerpick: CLOSED NULL (pass1; candidate not advanced; replication not triggered).

Next: step 5 P2 running (D-C10r-rulings-12, D-C10w-p2go); steps 6–7 await its replicated reading. This is the current form of the prereg's "the sequence moves to gate A / step 5" (:78): step 5 P1 is recorded as interim (CORPUS/55) and P2 holds the GPU.

Overturning test (both reviewers; not required under NULL, and not to run ahead of step 5): a second seed or a fresh-context recomputation of step 0, then B on the new map. It would test whether this near-tie map is a representative draw; it could overturn a robustness claim, not this fixed-map decision.

## Reviews

- GPT-6-Astra high: `results/c10v_layerpick_verdict_astra.md` (copy of `/private/tmp/claude-501/reviews/c10v_verdict_astra.md`) — **PROCEED-WITH-CHANGES**, one BLOCKING.
- Opus advisor: `results/c10v_layerpick_verdict_advisor.md` (copy of `/private/tmp/claude-501/reviews/c10v_verdict_advisor.md`) — **PROCEED-WITH-CHANGES**, three BLOCKING.
- Packet reviewed: `results/c10v_layerpick_verdict_packet.md`.

How each BLOCKING item is resolved:
1. **Astra B1 + advisor B1 (overlap, merged) — headline over-claimed a null effect.** The packet's "does not move held-out recall" is gone. The headline is "not advanced under the preregistered rules" and carries Astra's exact sentence ("The frozen argmax-G placement candidate did not meet the preregistered advancement threshold in pass1: …") with the advisor's added facts (+1, inside [5, 18], below the +10 margin, beat neither control, selector not credited, `described_as` miss, "one selector, one map, one seed, N = 24", prereg :11). "Not claimed" states that NULL is not evidence of zero effect.
2. **Advisor B2 — delegated-go disclosure.** In the provenance paragraph: the advisor's go-basis text and Astra's sentence (Q10, given there as exact text), the step-3 ratification note (D-C10r-rulings-12 Q2, EXPERIMENT_RUNBOOK.md:364) and artifact provenance (d8af793), which corrects the packet's stale "untracked" line.
3. **Advisor B3 — two pre-registered readouts missing.** The proxy prediction error (:76) and the A1-vs-A7 remaining ratios (:54, A-8) are reported above with the advisor's EVIDENCE-SHOWS / I-INFER text; every number was recomputed from `pass1.json` and matches the advisor's table.

Non-blocking notes adopted: Bshuf printed as NULL (shuffled-map control) with the reader string cited (Astra 2, advisor N2); δ = 0 and conditional repeatability wording (Astra 3, advisor N1); B's A1 68/72 at the floor and its collateral profile (Astra 4, advisor N3); gate locations cited from `pass1.json` directly (Astra 5, advisor N6); LAW#5 wording, (iii) as plumbing only, cached standing gates, UNVERIFIABLE magnitudes (Astra 6, advisor N7); Spearman under both codings with positives (Astra 7, advisor N4); proxy medians pooled over 72 and not in common coordinates (Astra 8); next-step wording (Astra 9, advisor N8); B0 observation (advisor N5); by-layer readout as readout only (advisor N9); overturning test (Astra 11, advisor). Not adopted: Astra 10's log citation `pass1.log:376–377`; the current file has 363 lines and the two markers are at 362–363, as cited above.

_Verdict sentence merged from both reviews (Astra "Proposed one-sentence CORPUS verdict"; advisor "Proposed one-sentence CORPUS verdict"): D-C10v-layerpick pass1 = NULL: the valid frozen-map candidate B (per-fact single-layer placement at the argmax-G band layer, the raw argmax since the measured δ was 0.0) scored 12/72 held-out A7 `para_full` against the same-process band 4–8's 11/72, inside the [5, 18] envelope and below the +10 margin, beat neither fixed layer 8 (B0, 12/72) nor the shuffled map (Bshuf, 10/72), and missed the `described_as` locality gate (86.17 < 87.0); every validity gate and LAW#5 (i)–(v) passed, replication was not triggered, and this one-selector, one-map, one-seed, N = 24 configuration is not advanced under the preregistered rules; depth, per-fact selection in general and F1 remain open._


⟨D-C10l-covgeom@0caeca4f⟩
