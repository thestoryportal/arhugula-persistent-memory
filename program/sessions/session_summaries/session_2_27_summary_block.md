# Session 2.27 — Summary Block

**Session type:** Execution (T.1-β-BAND; pod-side, Llama-3.2-3B)
**Predecessor:** S2.26 (T.1-α-MEMIT-AKD; AKD eliminated; CLOSED 2026-06-15)
**Closed:** 2026-06-15
**Verdict:** `BAND-INVARIANT → CEILING-IS-CONFIG-INDEPENDENT` (Route A)
**Headline finding:** The eight-axis ceiling **survives the EasyEdit community-standard `[4,5,6,7,8]` band**, single-variable, on cfb-v3. `0/5` cleared, same four-orders-of-magnitude miss as `[2–6]`. This is the **9th axis — and the first config-variation axis.** The "wrong layer band" escape hatch is closed.
**Edit dispatched:** YES — one MEMIT joint-overlay 5-fact edit at `[4–8]`. Reversed bit-exact (Copy-Unmount drift `0.00e+00`). Model left clean.

---

## 1. What S2.27 set out to do, and the result

**Designed purpose (D-S226-S227-1):** P0 at S2.26 found our canonical band `[2,3,4,5,6]` disagrees with the EasyEdit community-standard `[4,5,6,7,8]` for this exact model — overlap only `{4,5,6}`, we edit `{2,3}` the standard excludes and miss `{7,8}` it includes. Every one of the eight prior ceiling axes ran on `[2–6]`. With AKD eliminated (S2.26), the band became the strongest cheap unruled-out structural explanation. S2.27 re-ran MEMIT on cfb-v3 with the band as the **single** changed variable.

**Result:** `CELL8_CONSISTENCY 0/5`. The band swap moved nothing. The ceiling is config-independent across this band axis.

Per-fact post-edit `P(target_new)` at the canonical prompt:

| fact | target_new | tid | P(target_new) | top-1 now | cleared |
|---|---|---|---|---|---|
| cfb-v3-001 | guitar | 17418 | 7.34e-04 | 279 (` the`) | False |
| cfb-v3-002 | piano  | 27374 | 4.47e-06 | 813 (` his`) | False |
| cfb-v3-003 | violin | 63137 | 5.45e-05 | 279 (` the`) | False |
| cfb-v3-004 | harp   | 4960  | 1.24e-03 | 813 (` his`) | False |
| cfb-v3-005 | flute  | 96812 | 8.54e-04 | 1077 (` her`) | False |

Every `P(target_new)` is 3–6 orders of magnitude below the 0.5 band; top-1 never left the natural answer (` his`/` her`/` the`). `delta_vs_2_6_floor ≈ 0`.

---

## 2. The mechanism signature is identical to `[2–6]` (the load-bearing diagnostic)

The dispatch log shows the **same internal-vs-external split** that defines the ceiling on every prior axis. MEMIT's `compute_z` drove the internal objective hard on every fact, then the external probe registered nothing:

- guitar: internal `avg prob` `1.1e-08 → 7.1e-04` (~63,000× internal gain) → external `7.3e-04`, top-1 unmoved
- piano: `1.4e-08 → 7.3e-04` → external `4.5e-06`
- violin: `1.6e-08 → 1.1e-03` → external `5.5e-05`
- harp: `2.9e-06 → 4.7e-03` (~1,600×) → external `1.2e-03`
- flute: `1.5e-08 → 5.7e-04` → external `8.5e-04`

The optimizer worked; the model still won't say the new fact when asked. This is the architectural-invariant ceiling signature, reproduced under the community-standard band. The band reconfigured the mechanism correctly — log shows `Rewrite layer is 8` (top of `[4–8]`) and `Tying optimization objective to 27`, both correct for the new band — and the outcome did not change.

---

## 3. Single-variable integrity — how "band-only" was enforced and proven

Every "held-constant" pillar was mechanically certified, not assumed:

- **Model** — Checkpoint #4 bit-exact gate vs the S2.22 GRACE-engine baseline: `drift_max=0.00e+00`. Cross-engine, cross-session, bit-identical forward pass. (Extends the Llama-3.2-3B determinism chain to checkpoint #4.)
- **Engine** — SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` verified (REUSE, no re-clone).
- **Patches** — `memit-patches v2.5` P-5/P-6/P-7 all `true` (verified, no re-apply). P-7's `>8192` branch fired (`npos=131072`) → `_t100_` filenames → edit-time cache hits on all five layers (log: `Loading cached …_t100_100000.npz` ×5, zero "computing locally").
- **Reuse caches L4/L5/L6** — SHA-256 byte-identical to S2.26 §12 (`CELL3_COV_REUSE_OK 3/3`).
- **New caches L7/L8** — `C-S227-1` byte-equality gate: both exactly `268,436,642` bytes (`CELL5_BYTE_EQ_OK`), same envelope (`wikipedia`/`100000`/`float32`/`t100`), computed by a 2-line diff of the proven S2.24 script.
- **Hparams** — `C-S227-2` upgraded to a **full 20-field** diff between freshly-built `[2–6]` and `[4–8]` `MEMITHyperParams` objects: only `layers` differs (`CELL6_SINGLE_VAR_OK`).
- **Reversal** — Copy-Unmount restored L4–L8 to `drift_max=0.00e+00` across all 5 facts (`CELL10_UNMOUNT_OK`); 5th validated layer-range for Copy-Unmount.
- **Post-session caches** — all 7 (L2–L8) byte-intact (`CELL12_COV_INTEGRITY_OK 7/7`).

The band is the sole variable, and it is proven so at the byte and field level.

---

## 4. Two execution findings worth recording

### 4.1 The tied-embedding adaptation is the load-bearing 3B hparam, and the runbook under-specified it (`D-S227-LMHEAD-1`)

The first Cell 8 dispatch **aborted** at `compute_z` with `LookupError: lm_head.weight`. Llama-3.2-3B has tied embeddings (`config.tie_word_embeddings=True`); there is no distinct `lm_head.weight` — the output projection is `model.embed_tokens.weight`. The fix was setting `lm_head_module="model.embed_tokens"` (`C-S224-1`), applied **identically to both** the `[2–6]` comparand and the `[4–8]` config so single-variable discipline held; the all-20-field diff was re-verified after the fix and still showed only `layers` changed.

**Finding:** the v0.1 runbook Cell 6 / §0.7 named `v_loss_layer=27` and `lm_head_module=model.embed_tokens` as the 3B adaptations, but the authored Cell 6 draft initially carried only `v_loss_layer` (the S2.24 grep window that informed authoring truncated before the `lm_head` override). The S2.24 reproduction grep later confirmed S2.24 itself loaded the 8B JSON and overrode `v_loss_layer` visibly — the `lm_head` override was the empirically-required-but-easily-dropped one. **`lm_head_module=model.embed_tokens` is the single most load-bearing 3B adaptation: without it the dispatch cannot run at all.** Any future 3B (or tied-embedding-model) MEMIT runbook MUST set it explicitly; `v_loss_layer` is necessary but the dispatch fails *first* on `lm_head`.

### 4.2 The S2.24 hparam construction is "load 8B JSON, override minimally"

The proven 3B config is **not** a bespoke dict — it is `json.load(hparams/MEMIT/Llama-3.1-8B.json)` + `v_loss_layer=27` + `lm_head_module=model.embed_tokens`. All other 18 fields (clamp_norm_factor, v_num_grad_steps=25, mom2_*, rewrite_module_tmp, etc.) are inherited verbatim from the 8B canonical JSON. The 8B JSON already carries `layers=[2,3,4,5,6]` as its base value (so the band is a base-JSON property, not an adaptation). This construction pattern is the canonical way to build a scale-variant MEMIT config and should be the documented idiom for any future Llama-class port.

---

## 5. What this resolves

**RESOLVES `C-S226-3` (the band confound on all prior axes), AGAINST the band hypothesis.** The `[2–6]` vs `[4–8]` disagreement is no longer an open structural confound: the ceiling holds on the community-standard band, single-variable. The eight-axis ceiling was **not** a layer-band artifact.

**STRENGTHENS the ceiling — promotes it from "model property under our band choice" to "config-independent across the band axis."** This is the **9th axis**, and notably the **first config-variation axis** (all eight priors varied corpus/target/locus/probe/write-engine/hparam-value/model-scale; none varied the edit-layer band itself). The most attractive remaining "it's-just-a-misconfig" escape hatch is closed.

**DOES NOT make a model-family-universality claim beyond MEMIT-on-base-Llama.** T.3 (alt architecture: Mistral/Qwen) remains OPEN and out-of-scope WS1. The ceiling is now a robust MEMIT-on-base-Llama property across scale (8B→3B, S2.24) and across the two contested layer bands (S2.27).

---

## 6. Decisions made

- **D-S227-VERDICT-1** (load-bearing): S2.27 closes as `BAND-INVARIANT → CEILING-IS-CONFIG-INDEPENDENT`, Route A. `0/5` at `[4–8]`, single-variable, all integrity gates green. 9th axis; first config-variation axis.
- **D-S227-LMHEAD-1** (load-bearing): `lm_head_module="model.embed_tokens"` is a MANDATORY 3B (tied-embedding) MEMIT adaptation and the *first* point of dispatch failure if omitted — it precedes `v_loss_layer` in failure order. Recorded as the canonical highest-priority 3B adaptation. Runbook Cell 6 spec amended in practice (see §8).
- **D-S227-HPARAM-IDIOM-1**: the canonical scale-variant MEMIT config idiom is "load the 8B JSON, override `v_loss_layer` + `lm_head_module` only." Documented for future Llama-class ports.
- **D-S227-V13-1** (forward): the v1.3 `framework_finding_memit_ceiling_archival` amendment is now triggered — Axis 9 (band-invariance) is additive to the v1.0 PERMANENT + v1.1 + (Axis 7) lineage. Authored at S2.28 entry (see §9).

---

## 7. Constraints established

- **C-S227-1** (validated): each newly computed covariance cache MUST be byte-size-equal to the existing band set (`268,436,642`) before the band may be dispatched. EMPIRICALLY HELD this session (L7/L8 both exact). Carry forward as the standing cache-extension gate.
- **C-S227-2** (validated): the MEMIT hparam config MUST diff against the established-band comparand across ALL `MEMITHyperParams` fields (not a hand-picked subset) and show exactly one changed field (`layers`) for a band-only run. The full-field form caught nothing this session but is the correct discipline (the 5-field eyeball form would have missed the `lm_head` issue's single-variable implications had it differed between bands).
- **C-S227-3** (NEW): for any tied-embedding model (`config.tie_word_embeddings=True`), `lm_head_module` MUST point at the tied embedding parameter (`model.embed_tokens`), verified by a `named_parameters()` presence check, BEFORE dispatch. `lm_head.weight` will not exist and `compute_z` raises `LookupError` at the first fact.

---

## 8. Runbook amendment applied in practice (carry to v0.2 if re-authored)

The executed runbook was `t1_band_4_8_runbook v0.1`. Two in-flight corrections, to fold into a v0.2 if the band runbook is ever re-run:

1. **Cell 6 MUST set `lm_head_module="model.embed_tokens"`** as a first-class 3B adaptation alongside `v_loss_layer=27`, and SHOULD precede dispatch with a tied-embedding presence check (now `C-S227-3`). v0.1 Cell 6 listed only `v_loss_layer` in the changed-fields table; `lm_head_module` was the load-bearing omission.
2. **A path-setup cell** (`os.chdir(MEMIT_ROOT)` + `sys.path.insert`) is required before the first `from memit import …` in a fresh kernel; v0.1 assumed engine importability. (S2.24 cov script carried this; the notebook did not inherit it.)
3. **Baseline path** on the pod is `/workspace/architecture_profile/llama_3_2_3b_baselines.json` (not `/workspace/…` root); v0.1 Cell 4 guessed the root.

These are notebook-mechanics corrections; none affected the single-variable integrity of the result.

---

## 9. Forward routing — S2.28

**S2.28 = v1.3 framework_finding amendment authoring + deeper-arm scoping (authoring session, not execution).**

Rationale: Route A triggers the v1.3 additive amendment (`D-S227-V13-1`). With the band confound eliminated, the ceiling is a config-independent MEMIT-on-base-Llama property across scale and band. The deeper arms the S2.26 matrix pre-named (per-layer sweep, sequential-vs-joint dispatch) are now **lower priority** — they probe *within* the MEMIT-on-base-Llama regime that is already 9-axis-confirmed, and would each be a 10th/11th axis of the same class rather than a new hypothesis class. The higher-value forward move is the cross-architecture axis.

Scope of S2.28 (authoring):
- Author `framework_finding_memit_ceiling_archival v1.3` (ADDITIVE; v1.0 PERMANENT + v1.1 + Axis 7 + **Axis 9 band-invariance** preserved verbatim; v1.2 lineage intact). Record the internal-vs-external signature reproduction and the `delta_vs_2_6_floor ≈ 0` result.
- Author the `t_branch_decision_document` amendment (v1.2 ADDITIVE) recording band-confound elimination and the deeper-arm deprioritization.
- Scope the cross-architecture axis (T.3: Mistral-7B / Qwen-7B) as the next *hypothesis-class* axis vs. the within-regime deeper arms — surface the cost/value tradeoff for operator routing. NOTE: T.3 is currently flagged out-of-scope WS1; S2.28 surfaces whether the 9-axis result warrants re-scoping it in.

**Deferred (unchanged):** per-layer sweep + sequential-vs-joint dispatch (within-regime deeper arms; lower priority post-Route-A); OQ-S225-BASE-INSTRUCT-1 (base-vs-instruct); KnowEdit external-validity. cfb-v4-highAKD preserved as durable alternate-domain asset (D-S226-CFBV4-PRESERVE-1).

---

## 10. Hypothesis-class ledger (post-S2.27)

- **Layer-band placement (`[2–6]` vs community-standard `[4–8]`):** **ELIMINATED S2.27** — ceiling holds on `[4–8]`, single-variable, `0/5`. (Was the leading structural hypothesis at S2.26.)
- **Ceiling = genuine MEMIT-on-base-Llama property:** **9-axis confirmed** (8 prior + Axis 9 band-invariance), across scale (8B→3B) and band (`[2–6]`/`[4–8]`).
- AKD / key-collision: ELIM S2.26. T.1 alt model (Llama scale): RESOLVED → generalizes 8B→3B (S2.24). A/B/C/D: ELIM (S2.12-A / S2.11-B / S2.13-C / S2.15-D2). T.2 ROME: ELIM S2.18. T.2 GRACE: hparam-conditional elim S2.22.
- **T.3 alt arch (Mistral/Qwen):** OPEN; out-of-scope WS1 — but S2.28 surfaces whether the 9-axis config-independent result warrants re-scoping it in as the next hypothesis-class axis.
- **Within-regime deeper arms (per-layer sweep, sequential-vs-joint):** OPEN, DEPRIORITIZED post-Route-A (same-class 10th/11th axes).

---

## 11. Block / cell execution record

| cell | surface | result |
|---|---|---|
| 0 | A | `CELL0_DEPS_OK` transformers=4.45.2 accelerate=0.34.2 torch=2.4.1+cu124; engine present; 5/5 caches present (268436642 each); GPU 4090 6666 MiB. |
| 1 | A | `MEMIT_ENGINE_SHA 80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` — verified (REUSE). |
| 2 | A | `CELL2_PATCH_STATE_OK` — P-5 (`wikimedia/wikipedia`+`20231101.en`), P-6 (`f"_t{batch_tokens}"`), P-7 (`100 if …>8192 else None`) all confirmed in live engine. |
| 3 | A | `CELL3_COV_REUSE_OK 3/3` — L4 `f5fb935a…` / L5 `cac4f814…` / L6 `1509023884…` byte-identical to S2.26 (L6 hex prefix confirmed, not a transcription quirk). |
| 4 | B | `CHECKPOINT_4_3B_OK drift_max=0.00e+00` — 38-probe forward pass bit-identical to S2.22 GRACE baseline; path `/workspace/architecture_profile/llama_3_2_3b_baselines.json`. |
| 5 | A→B | `CELL5_BYTE_EQ_OK L7 size=268436642 L8 size=268436642` (sha L7 `637f2355…` / L8 `6eea5539…`); `CELL5_COV_EXTEND_OK 7/7`. L7 13.5 min / L8 14.6 min; 2-line diff of proven S2.24 script. |
| 6 | B | `CELL6_SINGLE_VAR_OK` (all 20 fields) `diff={layers: [2,3,4,5,6] -> [4,5,6,7,8]}`; `LAYER_BOUND_OK [4..8] < 28`. lm_head fix applied (6c) after first dispatch LookupError. |
| 7 | B | `CELL7_BASELINE_OK` — 5 requests built; unmount comparands 4× ` his`(813) + ` her`(1077) recorded. |
| 8 | B | first dispatch `LookupError: lm_head.weight` → 6c fix → re-dispatch `DONE 0.3 min`; all 5 caches loaded cached (no local compute); `CELL8_CONSISTENCY 0/5`. |
| 10 | B | `CELL10_UNMOUNT_OK drift_max=0.00e+00` — 5/5 facts bit-exact restore; 5th validated Copy-Unmount layer-range. |
| 12 | A | `CELL12_COV_INTEGRITY_OK 7/7` — all L2–L8 byte-intact post-session. |
| 13 | B | `CELL13_MANIFEST_OK` — sessions[2.27] appended. |
| 9, 11 | — | folded into Cells 8/10 (consistency surface produced inline at Cell 8; verdict gate rendered inline). |

---

## 12. NV / environment carry-forward

- **Pod SSH target (unchanged S2.26):** host `103.196.86.67`, port `16437`, key `~/.ssh/id_ed25519`, user `root`. Direct TCP (`-e "ssh -p 16437 -i ~/.ssh/id_ed25519"`), not the RunPod gateway alias. Mirror archive: `/Volumes/memit/llm-database-poc-mirror/`.
- Pod `ee00aa7bcadb` warm; same instance as S2.24/S2.25/S2.26. Deps intact.
- Engine `/workspace/memit_dry_run/memit` SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` (verified this session, Cell 1).
- **7 durable 3B caches** now at `/workspace/covariance_caches/meta-llama_Llama-3.2-3B/wikipedia_stats/`, each `268,436,642` bytes: L2 `7c6dafdc…` / L3 `1dd366b5…` / L4 `f5fb935a…` / L5 `cac4f814…` / L6 `1509023884…` / **L7 `637f235541bef1be…`** / **L8 `6eea553955c288f6…`** (L7/L8 NEW this session).
- New on NV this session: L7+L8 caches; `/workspace/archive/s_series_scripts/t1_beta_cov_compute_l78.py` (2-line diff of `t1_alpha_cov_compute.py`); `/workspace/archive/s_series_scripts/t1_beta_cov_progress_l78.json`; `/workspace/archive/s_series_scripts/t1_beta_cov_l78.log`; notebook `s227_t1_beta_band.ipynb`; manifest `sessions["2.27"]`.
- Baseline file path (pin for forward sessions): `/workspace/architecture_profile/llama_3_2_3b_baselines.json`.
- Hparam base: `/workspace/memit_dry_run/memit/hparams/MEMIT/Llama-3.1-8B.json` + overrides `v_loss_layer=27`, `lm_head_module=model.embed_tokens`.

**Mirror sync (run from MBP after close; direct TCP):**
```bash
rsync -av --exclude 'hf_cache' \
  -e "ssh -p 16437 -i ~/.ssh/id_ed25519" \
  root@103.196.86.67:/workspace/ \
  /Volumes/memit/llm-database-poc-mirror/workspace/
# SHA-256 spot-check the two new caches post-sync:
#   L7 637f235541bef1be…  L8 6eea553955c288f6…
```

---

## 13. S2.28 kickoff (successor)

**Scope:** Authoring — v1.3 framework_finding amendment + t_branch amendment + cross-architecture-axis scoping. NOT execution (no pod required).

**Entry preconditions:** `session_2_27_summary_block.md` (this) + `framework_finding_memit_ceiling_archival v1.2` (the amendment target; v1.0 PERMANENT + v1.1 + Axis 7 preserved) + `t_branch_decision_document v1.1` (amendment target) + the v1.0/v1.1 ceiling lineage for additive integrity.

**Deliverables:**
1. `framework_finding_memit_ceiling_archival v1.3` — ADDITIVE; adds **Axis 9 (band-invariance)**; preserves v1.0 PERMANENT verbatim. Records: `[4–8]` single-variable `0/5`, internal-vs-external signature reproduction, `delta_vs_2_6_floor ≈ 0`, first config-variation axis.
2. `t_branch_decision_document v1.2` — ADDITIVE; records band-confound elimination + within-regime deeper-arm deprioritization.
3. Cross-architecture-axis scoping note — T.3 (Mistral-7B / Qwen-7B) vs within-regime deeper arms; cost/value tradeoff; recommendation on whether the 9-axis result re-scopes T.3 into WS1. Per standing directive, Claude makes the call and surfaces it for the record.

**Execution guidance (carry forward verbatim):** authoring session — full artifacts end-to-end, no placeholders, additive-only on PERMANENT artifacts (v1.0 integrity preserved verbatim). Claude makes all routing calls and proceeds; surfaces load-bearing/irreversible decisions for the record without blocking.

---

*End S2.27 summary block.*
