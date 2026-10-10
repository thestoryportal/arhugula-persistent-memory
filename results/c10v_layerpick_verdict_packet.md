# Advisor / objective-review prompt (reusable — Claude & Codex)

You are an **independent, adversarial reviewer** of a research step in the LLM-as-Database program. You are not the author. **Do not rubber-stamp.** Your job is to find where the work is wrong, over-claimed, confounded, or drifting from the goal — *before* it is leaned on.

You will be given ONE of: a **test/experiment design** (before it runs), a **finding/result** (before it is declared conclusive or written to CORPUS), or an **approach** the author is about to commit to — together with its evidence (artifact paths + numbers) and the relevant context.

Run this review and answer concisely and specifically:

1. **Real criterion.** Does this answer the question's *actual* criterion, or a flattering adjacent one? (e.g. is the metric matched to the claim — top-1 for read-correctness, distributional for distributional; is the gate's true requirement being met or a softer proxy?)
2. **Confounds & over-claims.** Hunt for confounds, leakage, Goodhart, and over-statement. Is `EVIDENCE-SHOWS` blurred with `I-INFER`? Is "the mechanism works" being passed off as "the contract is met" (**mechanics ≠ contract**)? Is design-viability being passed off as empirical evidence?
3. **Cite or flag.** Every factual claim must cite an artifact (path + exact number) or be labeled **`UNVERIFIABLE`**. Call out any claim that isn't grounded. Verify that external repos/IDs/claims were actually checked before being relied on.
4. **The overturning test.** What is the *cheapest* experiment or control that could **falsify** this finding/design? If it hasn't been run, that is the gap.
5. **Drift check.** Does this advance the F1 readiness determination (or a live §0.3 falsifier)? If not, say so.

Be a skeptic; the author will weigh your input heavily but evidence remains binding over your opinion. The answer format for THIS review is fixed in §7 below.

---

# What to review: the VERDICT of step 4 (D-C10v-layerpick, pass1), before it is written to CORPUS

Worktree root = `.` below (`/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`). Read-only review. **Verify every number against the files; do not trust this brief.** `results/c10v_layerpick/pass1.json` is 530 KB — extract fields with python/jq, do not read it whole.

Type: a finding before it is declared and written to CORPUS. Nothing has been written to CORPUS, the ledger, the runbook or the scoreboard for this run yet.

## 0. Run facts and files

- Stages: step0 (pid 19153, `results/c10v_layerpick/step0.json` `.when_utc` = `2026-10-08T02:22:26Z`; log `results/c10v_layerpick_logs/step0.log` ends `C10V_STEP0: READY` / `STAGE_EXIT=0`) → LAW#5 (pid 79246, `law5.json` `.when_utc` = `02:49:56Z`) → pass1 (pid 79246; `pass1_started.json` `.when_utc` = `02:54:27Z`; `pass1_complete.json` `.when_utc` = `2026-10-08T03:32:38Z` = 2026-10-07 21:32:38 MDT). `results/c10v_layerpick_logs/pass1.log` ends `C10V_PASS1_COMPLETE` then `STAGE_EXIT=0` (log line 363). pass2 not run.
- Model: `pass1.json` `.model` = `Qwen/Qwen2.5-3B`, revision `3aab1f19…`, `float16`, `mps`.
- Pre-registration (authority): `docs/C10V_LAYERPICK_PREREG.md` v2 FROZEN.
- Reader: `experiments/track_c/c10v_layerpick_read.py` (last commit 9120bd6). Run as `env LLMDB_ROOT=. .venv/bin/python -B experiments/track_c/c10v_layerpick_read.py results/c10v_layerpick --root .` → rc 0, output saved at `/private/tmp/claude-501/c10v_pass1_read.json`. **The packet author re-ran the reader (read-only, stdlib) → rc 0, output byte-identical (`cmp`).** The reader also re-hashes every source in `identity.json` `.source_sha256` against the current tree (`read.py:416–418`, `CURRENT_SOURCE`) — so the hashed sources are unchanged since the run. `run.json` `.readings` equals the reader output exactly (checked by python `==`).
- Go basis: delegated go, runbook `EXPERIMENT_RUNBOOK.md:363` (D-C10v-go) — "to be disclosed again at close-out".
- Implementation rulings that bear on the reading: `EXPERIMENT_RUNBOOK.md:349` (D-C10v-implfix: "δ stays as frozen (measured in-process; 0.0 is a measurement, not a defect)"; pass1 records `selection_agreement_n` instead of halting); `:350` (advisory A1 "contender boundary at winner−δ … cannot change a result at δ = 0").
- Git: `law5.json`, `pass1.json`, `pass1_started.json`, `pass1_complete.json`, `run.json` are **untracked** (`git status --short results/c10v_layerpick`); `step0.json` and `identity.json` are not listed, i.e. tracked.

## 1. What was pre-registered (verbatim, `docs/C10V_LAYERPICK_PREREG.md`)

Hypotheses — `:15` H-V1 (lone-write placement; "The selector is credited only if B beats both B0 and Bshuf (§3)"), `:16` H-V0 (null — the prior: "The band already installs ≈ 97 % of the canonical residual norm"), `:17` H-V2 (trade-off; B0 is the strength control).

Selector and stop rule:

> `:33` **Rule:** `ℓ*(i) = argmax_ℓ G_ℓ[i, i]`, subject to a margin: the winner counts only if `G_ℓ*[i, i] − G_runner-up[i, i] ≥ δ`, where δ is **measured**, not chosen: step 0 is computed twice in the process (forward passes on MPS, solves on CPU) and δ = the largest absolute change in any `G_ℓ[i, i]` between the two computations; a fact whose margin is below δ takes the layer nearest 8 (the band's z-layer). The margined map must be identical across the two computations, else **"map not reproducible"** and the arm is not run.

> `:35` **Stop rule:** if `ℓ*` takes one value on ≥ 20/24 facts the arm is not run and the result is logged as **"concentrated map; candidate not advanced"** (an expenditure screen — it permits four differing assignments and its ability to predict usefulness is unverifiable). Otherwise the map `{subject → ℓ*}` is written to `results/c10v_layerpick/step0.json`, hashed into the run record, and fixed.

Readings (§3, `:62–:78`), verbatim:

> `:64` **Decision order:** validity first (INVALID ends the reading for that recipe); then the count; then the locality and write-size gates; then the label; then attribution; then replication.

> `:66` **Validity (any failure → INVALID for that recipe):** fingerprint d941a9fb and `_cov_cpu == 3`; LAW#5 (i)–(v) INERT; map reproduced in-process; A1 ≥ 68 and A2 ≥ 68 **under that recipe** (a control failure is INVALID, never TRADEOFF); recipe A A7 `para_full` in [5, 18]/72 and canon in [5, 10]/24; `Z_OVERRIDE_HITS` = non-empty groups per arm; map hash, `G` table, δ and template hashes in the run record; `para_full_string` = `para_full`.

> `:68` **Binding count:** B's A7 `para_full` /72 (B0 and Bshuf read by the same rules as their own candidates), per held-out template (3 × 24), per-fact 24-vector with the per-edge rule (pass iff 3/3) and the assigned layer per fact.
> `:69` - **LEAD** if B's count ≥ 30/72 and every locality gate holds.
> `:70` - **PARTIAL** if B's count > 18/72 (outside the identical-baseline envelope), B's count − A's ≥ 10/72, B's count < 30, and every gate holds. A count inside [5, 18] is NULL whatever the gain.
> `:71` - **TRADEOFF** if a PARTIAL- or LEAD-sized gain comes with a locality or write-size gate miss (controls are validity, above).
> `:72` - **NULL** otherwise (this configuration not advanced).

> `:74` **Locality gates (vs recipe A, same process):** L1 ≤ A + 1 (of 12); same-frame fictional ≤ A + 1 (of 6); `described_as` ≥ A − 3; L3 ≥ 29/30; generic perplexity ≤ A + 0.5; relation-label flips reported (no threshold in the contract). **Write-size qualifier:** Σ over groups and layers ‖ΔW_B‖ against Σ over layers ‖ΔW_A‖ above 1.5 adds **-LARGE-WRITE**; a LARGE-WRITE label contradicts H-V1's "same write size" and **does not pass gate A**.

> `:76` **Attribution (the selector is credited only here):** a LEAD or PARTIAL on B carries the label for the selector only if B's count exceeds **both** B0's and Bshuf's by ≥ 10/72 (the contract's gain margin); otherwise the label carries **-PLACEMENT-NOT-ATTRIBUTED** (it belongs to the grouped single-layer recipe, or to B0 if B0 itself labels). **Replication (gate A):** the second process must satisfy every validity and locality gate and the same count rule, else **-NOT-REPLICATED** and nothing is adopted. The historical envelope and two processes do not give a calibrated false-positive rate; the labels buy or decline a next step, nothing more. **Reported, not gated:** the realised count by assigned layer; Spearman of `G[i, i]` at the assigned layer against the per-fact outcomes; the proxy's prediction error on the canonical activation change (fp16 application noted).

> `:78` **What each buys.** LEAD on B, attributed and replicated → the map becomes a candidate default for later arms, behind the step-1 shared target if that led. LEAD or PARTIAL on B0 (replicated) → a single-layer placement lead, not a selector lead; folded into the sequence as its own note. PARTIAL on B, attributed and replicated → arm C as its own pre-registration. NULL, "concentrated map", "map not reproducible", NOT-ATTRIBUTED or NOT-REPLICATED → not advanced; the depth question joins CORPUS/37–39 and 44 as not advanced on this harness — not closed; the sequence moves to gate A / step 5. TRADEOFF → report; step 5 next.

> `:82` No label in CORPUS/37–50 changes (CORPUS/44's ρ_c wording is corrected through the CORPUS gate, not here). LEAD is a write-path placement lead, not §8.9 contract closure, not route closure, not an F1 change, and not evidence about LOKI or WilKE. NULL does not close depth, per-fact selection in general, or selectors other than `G`. Nothing about which positions or components carry the value. Key side, target definition and context templates stay as the engine has them. The engine is untouched; the harness gains at most the explicit map seam (review item a).

Also: `:11` "A miss, at any stage, means *this candidate configuration was not advanced* — one selector, one map, one solve budget, one seed, N = 24." `:86` "Codex GPT-6-Astra (high) at the verdict and at the promote gate if LEAD."

## 2. Gates (validity, `:66`) — recorded values

| Gate (prereg `:66` unless noted) | Recorded value | Source (file → key) | Status |
|---|---|---|---|
| Engine fingerprint d941a9fb | `sha256` = `d941a9fbc7b09c41…3d65`, `ok` = true | `step0.json`, `law5.json`, `pass1_started.json`, `pass1.json` → `.fingerprint.sha256` / `.ok` | PASS |
| `_cov_cpu == 3` | 3 | same four files → `.fingerprint._cov_cpu` | PASS |
| Fingerprint **in run.json** | run.json has **no `fingerprint` object**; it carries the engine hash only as `.identity.source_sha256["memit_dry_run/memit/memit/memit_main.py"]` = `d941a9fb…3d65`. `_cov_cpu` is not in run.json. | `run.json` → `.identity` (keys: run_id, created_utc, source_sha256, source_digest, preflight_controls_reference) | PARTIAL — see Q5 |
| Identity consistency | `identity.json` == `.identity` of run, step0, pass1, law5, pass1_started, pass1_complete (python `==`, all True); `run_id` `c10v-bea2183a…`; `source_digest` `97470c0e…` | each file → `.identity` | PASS |
| Record integrity | `pass1_complete.json .record_sha256` = `run.json .pass_sha256.pass1` = sha256(pass1.json) = `bf8f162a…119f` | as named | PASS |
| Map reproduced in-process (δ) | `delta` = **0.0**; `map_reproduced` = true; `G_table == G_table_repeat` exactly; `status` = `READY`; `concentration` = 15 (< 20, stop rule not fired) | `step0.json` → `.delta`, `.map_reproduced`, `.G_table(_repeat)`, `.status`, `.concentration` | PASS (δ = 0 — see Q3) |
| Map reproduced across processes (not a prereg gate; D-C10v-implfix) | `selection_agreement_n` = 24; pass1 recomputed step 0 in pid 79246; `pass1.json .step0` differs from `step0.json` only in `pid`, `when_utc` (G table bit-identical). Contexts were **frozen** from step0 into pass1 (`arms.py:493`, `load_harness(root, frozen["ctx"])`); `ctx_sha256` `91c1a4e7…` in both. | `pass1.json` → `.selection_agreement_n`, `.step0`, `.ctx_sha256` | recorded |
| Map hash, G table, δ, template hashes in the run record | `published_map_sha256` = `step0 .map_sha256` = `f2bdd9df…6183`; G table, δ, `ctx_sha256` present in `pass1.json .step0` and `step0.json`; **not** inside `run.json` itself (run.json pins pass1.json by hash) | `pass1.json`, `step0.json` | PASS if "run record" = pass1.json (see Q5) |
| LAW#5 (i) standing gate | `expr_delta` 0.0003 (< 0.05), `loc_delta` 0.03 (< 3), `ok` true, `standing_override_hits` 0 | `law5.json` → `.law5.standing.*`, `.law5.standing_override_hits` | INERT |
| LAW#5 (ii) floor | `relative_by_layer` 4–8 all 0.0; `relative_max` 0.0; `behavior_count_deltas` canon 0, para 0; `tolerance` = 0.0001 (= the 1e-4 clamp, since 10 × floor = 0) | `law5.json` → `.law5.floor.*`, `.law5.tolerance` | INERT |
| LAW#5 (iii) active identity map | `relative_by_layer` 4–8 all 0.0; `behavior_equal` true; `active_group_layers` [[4,5,6,7,8]] | `law5.json` → `.law5.identity.*` | INERT |
| LAW#5 (iv) single-layer path | `relative_by_layer` {"8": 0.0}; `active_group_layers` [[8]]; `projector_indices` [4] | `law5.json` → `.law5.singleton.*` | INERT |
| LAW#5 (v) multi-group | `relative_by_layer` {"6": 0.0, "5": 0.0}; groups layer 6 (15 subjects, projector 2) then layer 5 (projector index 1) | `law5.json` → `.law5.multigroup.*` | INERT |
| LAW#5 proof = pass record | `pass1.json .law5` == `law5.json .law5` (True) | — | PASS |
| Per-recipe LAW#5 gate | A, B0, B, Bshuf: `law5_gate` = {expr_delta 0.0003, loc_delta 0.03, ok true} | `pass1.json` → `.recipes.<R>.law5_gate` | PASS |
| Recipe A envelope (known-baseline reproduction, LAW#3) | A7 `para_full_n` = **11** ∈ [5, 18]; `canon_full_n` = **9** ∈ [5, 10] | `pass1.json` → `.recipes.A.arms.A7_coined_coined.para_full_n`, `.canon_full_n` | PASS. Lineage: CORPUS/37:23 baseline [4,8] A7 para_full 13.9 % (10/72), canon 29.2 % (7/24); here 15.3 % / 37.5 % |
| Controls A1 ≥ 68, A2 ≥ 68 under each recipe (`para_full_n`) | A: 70 / 71; B0: 70 / 71; **B: 68** / 70; Bshuf: 70 / 71 | `.recipes.<R>.arms.A1_single.para_full_n`, `.A2_coherent2.para_full_n` | PASS (B's A1 exactly at the floor — see Q4) |
| `Z_OVERRIDE_HITS` = non-empty groups | A 1 (1 group), B0 1 (1 group), B 5 (5 groups), Bshuf 5 (5 groups), every arm | `.recipes.<R>.wrapper.<arm>.z_override_hits`, `.groups` | PASS |
| `para_full_string` = `para_full` | A7: A 15.3/15.3, B0 16.7/16.7, B 16.7/16.7, Bshuf 13.9/13.9; `para_string_n` = `para_full_n` in every arm | `.recipes.<R>.arms.<arm>.para_full_string`, `.para_full`, `.para_string_n` | PASS |
| Recipe validity block | A, B0, B, Bshuf: `{"ok": true, "reasons": []}` | `.recipes.<R>.validity` | PASS |
| Covariance cache identity | `cov_cache_sha256` of B0, B, Bshuf == A's | `.recipes.<R>.cov_cache_sha256` | PASS |
| Preflight controls reference (not the binding LAW#3) | `results/c10q_stacked/passS.json`, A1 70, A2 71, ok | `identity.json` → `.preflight_controls_reference` | recorded |

No gate value required by `:66` is missing from the artifacts. The one place the brief's expectation and the artifacts differ: the fingerprint is not stored as such in `run.json` (Q5).

## 3. Reader output and per-reading numbers

Reader output (`/private/tmp/claude-501/c10v_pass1_read.json` = `run.json .readings / .replication_needed / .scope`):

| Reading | `label` | `base_label` | `count_label` | `binding` (A7 para_full_n /72) | `gain` vs A (11) | `write_ratio` | `attributed` | `gate_A` | `reasons` |
|---|---|---|---|---|---|---|---|---|---|
| B0 | NULL | NULL | NULL | 12 | +1 | 0.6435 | null | false | [] |
| B | NULL | NULL | NULL | 12 | +1 | 0.8674 | null | false | [] |
| Bshuf | **NULL-CONTROL-ONLY** | NULL | NULL | 10 | −1 | 1.0874 | null | false | [] |

`replication_needed` = false. `scope` = "candidate placement only; not depth closure, §8.9 closure, F1 change, LOKI or WilKE evidence" (`read.py:407`).

Locality gates (reader `.readings.<R>.locality_gates`; raw values from `pass1.json .recipes.<R>.arms.A7_coined_coined`):

| Gate (`:74`) | A (reference) | B0 | B | Bshuf |
|---|---|---|---|---|
| L1 flips ≤ A + 1 (`locality_axes.L1_flipped_to_edited_value`/12) | 0 | 0 ✓ | 0 ✓ | 0 ✓ |
| same-frame flips ≤ A + 1 (`extra.same_frame.flips`/6) | 1 | 1 ✓ | 1 ✓ | 1 ✓ |
| `described_as` ≥ A − 3 = 87.0 (`locality_described_as`) | 90.0 | 90.11 ✓ | **86.17 ✗** | 87.37 ✓ (margin 0.37) |
| L3 ≥ 29/30 (`locality_axes.L3_top1_agree`) | 30 | 30 ✓ | 30 ✓ | 30 ✓ |
| generic ppl ≤ A + 0.5 = 22.002 (`locality_axes.generic_ppl_post`; pre 21.755) | 21.502 | 21.71 ✓ | 21.713 ✓ | 21.698 ✓ |
| relation-label flips (reported; `extra.relation_labels.<k>.flips`) bystander / objective-anchored | 9 / 23 | 9 / 22 | 7 / 23 | 6 / 22 |

Write size (`pass1.json .recipes.<R>.delta_norms.A7_coined_coined.<layer>.delta_norm`, summed): A 86.121 (4: 15.856, 5: 11.927, 6: 11.867, 7: 19.275, 8: 27.196); B0 55.422 (layer 8 only); B 74.700 (8: 16.315, 7: 9.713, 6: 27.687, 5: 16.133, 4: 4.852); Bshuf 93.648. Ratios 0.6435 / 0.8674 / 1.0874 match the reader's `write_ratio`; none > 1.5, so no -LARGE-WRITE.

Other A7 readouts (`pass1.json .recipes.<R>.arms.A7_coined_coined`): `canon_full_n` A 9, B0 7, B 7, Bshuf 6; `para_first_n` 45 / 45 / 44 / 42; `tf_pertok_cont` 60.8 / 59.0 / 54.0 / 52.8; `cond_full_given_first` 0.244 / 0.267 / 0.273 / 0.238.

Per held-out template (`.readings.<R>.per_template`): B0 [3, 3, 6]; B [3, 3, 6]; Bshuf [2, 4, 4].

Per-fact A7 para_full hits, 0–3 per fact, subject order = `step0.json .subjects` (computed by the packet author from `pass1.json .recipes.<R>.detail.A7_coined_coined[*].para_full_hits`):

```
A      300000000301120000000100   (sum 11)
B0     300010000301020010000100   (sum 12)
B      300020000200000021000101   (sum 12)
Bshuf  300000000202000030000000   (sum 10)
B map  668656566564666566865667   (assigned layer, step0.json .map)
```

B0 and B have the same total and the same per-template split, but the per-fact vectors differ on 7 of 24 facts (e.g. fact 9 Brinduun: B0 3, B 2; fact 13 Oxbarrow: B0 2, B 0; fact 17 Kessivar: B0 0, B 1), and the write norms differ, so the two recipes are not one duplicated record. Fact 0 (Zorbland) is 3/3 under all four recipes. 3/3 edges (`.per_edge_3of3`): B0 2 (facts 0, 9), B 1 (fact 0), Bshuf 2 (facts 0, 16).

By assigned layer (`.readings.<R>.by_layer`): B — layer 4: 1 fact / 0 hits; 5: 5 / 4; 6: 15 / 7; 7: 1 / 1; 8: 2 / 0. Bshuf (same group sizes, `pass1.json .shuffled_changed_n` = 18 of 24 assignments changed) — 4: 1 / 0; 5: 5 / 0; 6: 15 / 10; 7: 1 / 0; 8: 2 / 0. B0 — 8: 24 / 12.

Reported, not gated (`:76`): `spearman_G_edge` B0 −0.479, B −0.316, Bshuf +0.196 (G at the assigned layer vs the binary 3/3 edge vector — `read.py:375`). HSIC diagnostic (`pass1.json .hsic`): `agreement_n` = 4/24 with ℓ*; `HSIC_b` by layer 4–8 = 0.00685, 0.00689, 0.00687, 0.00714, 0.00700. Proxy readouts, medians over 24 facts computed by the packet author from `pass1.json .recipes.<R>.arms.A7_coined_coined.extra.proxy.rows[*]`: realised fraction A 0.986, B0 0.935, B 0.976, Bshuf 0.954; remaining ratio canonical (`rho_per_prompt[0]`) A 0.030, B0 0.067, B 0.057, Bshuf 0.078; remaining ratio held-out (`rho_per_prompt[1:]`) A 0.195, B0 0.208, B 0.181, Bshuf 0.208.

Step 0 selector (`step0.json`): map counts layer 6: 15, 5: 5, 8: 2, 4: 1, 7: 1 (`.map`); `max_G` range 0.947–0.995 against `installed_share` 0.956–0.983 (`.installed_share_comparison`). Winning margins (`.winning_margins[0]`): minimum 8.9e-4 (Vorlex, layer 5 0.949064 vs layer 6 0.948172), 3 facts < 2e-3, 6 < 5e-3, 11 < 1e-2.

## 4. The label under the rules

Applying `:64` in order, to the numbers above:

1. **Validity (`:66`)** — every item in §2 passes for A, B0, B and Bshuf. No recipe is INVALID.
2. **Count (`:69–:70`)** — B 12, B0 12, Bshuf 10. None ≥ 30 (no LEAD). None > 18, so PARTIAL fails its first clause; `:70` also states "A count inside [5, 18] is NULL whatever the gain". The gains (+1, +1, −1) are far below 10 in any case.
3. **Locality and write size (`:74`)** — B misses `described_as` (86.17 < 87.0). By `:71` TRADEOFF requires "a PARTIAL- or LEAD-sized gain"; B has none, so the miss does not change the label. It must still be reported. No write ratio exceeds 1.5.
4. **Label (`:72`)** — NULL for B, B0 and Bshuf.
5. **Attribution (`:76`)** — applies only to a LEAD or PARTIAL on B; not reached (`attributed` null).
6. **Replication (`:76`)** — triggered only by PARTIAL/LEAD on B or B0 (`read.py:379–380`); not triggered (`replication_needed` false). pass2 correctly not run.
7. **What it buys (`:78`)** — "NULL … → not advanced; the depth question joins CORPUS/37–39 and 44 as not advanced on this harness — not closed".

The reader's labels match this hand derivation. The one label string not in the prereg vocabulary is Bshuf's `-CONTROL-ONLY` suffix (`read.py:386–388`). It was added after the implementation review (`results/c10v_layerpick_advisor_impl.md:132`; fix `results/c10v_layerpick_codex_fix1.md:22`; delta review `results/c10v_layerpick_fix1_delta_review.md:11`, FIXED). Its `base_label` is NULL.

**Disagreements between the reader and the prereg found by the packet author: none that change a label.** Q2, Q5 and Q7 note smaller points.

## 5. Scope limit (as the reader states it)

`read.py:407`, `run.json .scope`: **"candidate placement only; not depth closure, §8.9 closure, F1 change, LOKI or WilKE evidence"**. Prereg `:82` adds: "NULL does not close depth, per-fact selection in general, or selectors other than `G`." Prereg `:11`: one selector, one map, one solve budget, one seed, N = 24.

## 6. PROPOSED verdict and headline

**PROPOSED one-line verdict:** D-C10v-layerpick = **NULL**. Per-fact single-layer placement by the lone-write coefficient G (B) scored 12/72 held-out A7 `para_full` against the same-process band 4–8's 11/72 (+1). The fixed-layer-8 control (B0) also scored 12/72 and the shuffled map (Bshuf) 10/72. All three counts are inside the [5, 18] envelope. Every validity gate and LAW#5 (i)–(v) passed. B missed the `described_as` locality gate (86.17 vs ≥ 87.0), which does not change a NULL. The candidate is not advanced, no replication was triggered, and depth is not closed.

**PROPOSED CORPUS/56 headline:** `CORPUS/56 — C10V layer pick (step 4): NULL ⟨D-C10v-layerpick@<commit>⟩ — placing each fact at its argmax-G band layer does not move held-out recall (B 12/72, fixed layer 8 12/72, shuffled map 10/72, vs band 4–8 11/72). Candidate placement only: not depth closure, not §8.9 closure, no F1 change, no LOKI or WilKE evidence. C10 OPEN/BLOCKING; F1 unchanged.` (The "C10 OPEN/BLOCKING; F1 unchanged" tail follows the form of `EXPERIMENT_RUNBOOK.md:45, :49`. It is a program-state statement, not something this run measured.)

## 7. Questions for reviewers

- **Q1. Label.** Do `:64–:72` yield NULL for B and B0, and NULL for Bshuf, from the recorded numbers? Is treating B's `described_as` miss as "reported, label unchanged" correct under `:71`, or does `:64`'s order ("then the locality and write-size gates; then the label") require some qualifier on a NULL?
- **Q2. `-CONTROL-ONLY`.** This suffix is not in the prereg's label set (`:68` says Bshuf is "read by the same rules as their own candidates"). Should CORPUS print it, or print "NULL (control)" and cite `read.py:386`?
- **Q3. δ = 0.0 and the map's fragility.** δ was measured as exactly 0 (bit-identical in-process recompute; `arms.py:169–176` recomputes `compute_ks` per repeat, so this is not a cached reuse). The margin rule therefore never fired, and the map is the raw argmax: 3 of 24 winners lead by < 2e-3 in G and 11 by < 1e-2. The cross-process agreement of 24/24 used frozen contexts (`arms.py:493`), so the map's sensitivity to context resampling was never measured. The runbook ruled δ = 0 to be a measurement (`EXPERIMENT_RUNBOOK.md:349`). Does CORPUS need a sentence saying the NULL is for this near-tie map, and that the selector's stability is unmeasured? Under a NULL, does it matter at all?
- **Q4. B's A1 = 68/72**, exactly at the validity floor (`:66` "A1 ≥ 68"). The recipe is valid as written. Should CORPUS note that B's A1 was 2 below the other recipes' 70?
- **Q5. Where the gates live.** `run.json` has no `fingerprint` object and no `_cov_cpu`. It pins the engine only through `.identity.source_sha256[memit_main.py]`, and pins `pass1.json` by hash, which holds the fingerprint, map hash, G table, δ and `ctx_sha256`. Does that satisfy `:66` ("fingerprint d941a9fb and `_cov_cpu == 3`"; "map hash, `G` table, δ and template hashes in the run record") with "run record" read as `pass1.json`? Or must CORPUS cite the four `.fingerprint` blocks explicitly?
- **Q6. LAW#5 exact zeros.** Every relative distance in (ii)–(v) is 0.0, and the tolerance sits at the 1e-4 clamp. The comparisons are between separately computed tensors, each from restored weights (`arms.py:311–330`, `:349–350`, `:355`, `:363–364`, `:380–388`). So the zeros indicate bit-determinism on this machine, not a self-comparison. Please confirm (iii)–(v) are not vacuous. In particular, (iii) runs the wrapper with an identity map: does the wrapper path for that map differ from the original at all (`arms.py:262–300`)?
- **Q7. Spearman.** The reader correlates G with the binary 3/3 edge vector (`read.py:375`), which has 2, 1 and 2 positives (B0, B, Bshuf). With so few positives the statistic is close to degenerate, and `:76` says "per-fact outcomes", not 3/3 edges. Should CORPUS report it against per-fact hit counts (0–3), drop it, or report it with an n-of-positives caveat? It is reported, not gated.
- **Q8. Mechanics ≠ contract.** B's held-out remaining ratio is slightly lower than A's (median 0.181 vs 0.195), with no behavioural gain (12 vs 11). Should CORPUS mention this as a mechanical shift without effect, or leave it out as an unpre-registered median?
- **Q9. Next-step wording.** `:78` says "the sequence moves to gate A / step 5". Step 5 P1 has already run (CORPUS/55), and P2 is operator-authorized and takes the GPU at this stage boundary (`EXPERIMENT_RUNBOOK.md:364`). Should CORPUS say "step 5 P2 next" instead?
- **Q10. Disclosures.** The go was delegated (`EXPERIMENT_RUNBOOK.md:363`, to be disclosed at close-out). The pass artifacts are untracked in git. Should both appear in CORPUS/56 or in the close-out only?
- **Q11. Anything else** that should make any recipe INVALID, or that the proposed verdict or headline over-claims.

## 8. Answer format (required)

Write your report to the output path you were given (Astra: via `-o`).

1. **First line exactly one of:** `PROCEED` / `PROCEED-WITH-CHANGES` / `FIX-FIRST`.
2. **BLOCKING** — numbered items. Each gives file:line (or file → JSON key) evidence and **the exact change**: replacement text for the verdict or headline, or the exact correction to a number or label. Reserve BLOCKING for something that would make the CORPUS entry wrong, over-claimed or unverifiable.
3. **Non-blocking notes** — numbered, each with its evidence.
4. Your proposed one-sentence CORPUS verdict (if different from §6).

Do NOT rewrite the prereg, the reader or the driver; do NOT restate this brief.
