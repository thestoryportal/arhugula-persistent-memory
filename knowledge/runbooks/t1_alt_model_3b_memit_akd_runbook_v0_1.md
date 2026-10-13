# T.1-α-MEMIT-AKD Runbook — Llama-3.2-3B MEMIT — high-AKD discriminator — v0.1

**Status:** DECLARATIVE (authored S2.25; pod-side execution at S2.26)
**Iteration:** v0.1 first authoring (NEW runbook; not a revision)
**Engine:** MEMIT (canonical engine per `memit-patches-canonical v2.5`)
**Target model:** `meta-llama/Llama-3.2-3B` (fp16); pinned SHA `13afe5124825b4f3751f836b40dafda64c1ed062`
**Direct structural template:** `t1_alt_model_3b_memit_runbook v0.1` (the S2.24 3B-MEMIT runbook; structural inheritance with dual-corpus + AKD pre-flight extension)
**Basis:** S2.24 close (`session_2_24_summary_block.md`); OQ-S224-LIT-1 (PRIMARY); four-paper literature review (S2.24 §5)
**Specialist provenance:** memit-specialist (primary; engine + AKD-compute + dual-corpus dispatch), validation-contract-architect (verdict surface + AKD gate), state-consistency-theorist (cov-cache reuse + manifest), framework-spec-writer (routing matrix + finding-amendment scope)
**Persistence:** `/mnt/user-data/outputs/t1_alt_model_3b_memit_akd_runbook_v0_1.md`

---

## Part 0 — Orientation

### 0.1 What this runbook is — in one sentence

This runbook runs MEMIT on Llama-3.2-3B against **two corpora that differ in exactly one thing — how far apart their MEMIT "keys" sit** — to answer the single most decisive open question in the workstream (`OQ-S224-LIT-1`): is the seven-axis "architectural-invariant ceiling" a property of **the model**, or a property of **the low-AKD corpus** we have been running it on all along?

### 0.2 The concept you need before anything else: AKD (for the operator learning the system)

When MEMIT edits a fact, it does not edit "the fact" directly. It works in two halves:

- A **key** — a vector read out of the model when it processes the *subject* of the fact (technically: the activation at the subject's last token, at the edit layer). Think of the key as the "address" in the model's weights where this fact lives.
- A **value** — the vector MEMIT wants that address to now produce, so the model says the *new* target.

MEMIT writes by solving a least-squares problem: "adjust this MLP layer so that, for each key, it now emits the matching value." Here is the trap. If you batch 5 facts whose **keys are nearly identical** — nearly the same address — you are asking one linear layer to map *almost the same input* to *five different outputs*. That is close to mathematically impossible; the solver smears the updates together and efficacy collapses. The literature calls the spread of those keys **AKD — Average Keys Distance**. Low AKD = keys bunched together = MEMIT struggles. High AKD = keys spread apart = MEMIT has room to work.

**Why this matters right now:** cfb-v3 — the corpus that produced the 0/5 on both 8B and 3B — uses **5 clustered athletes and one identical template**. Five sport figures, processed through the identical sentence "X plays the instrument of", produce subject-last-token activations that sit almost on top of each other. **That is a textbook low-AKD setup.** We may have spent seven axes confirming a "model ceiling" that was actually a degenerate-corpus ceiling. This runbook finds out.

### 0.3 The experiment shape

Two corpora, everything matched except key separation:

| | cfb-v3 (control) | cfb-v4 (this experiment adds) |
|---|---|---|
| AKD | **LOW** (clustered subjects, 1 template) | **HIGH** (5 distinct domains, 5 templates) |
| Targets | guitar/piano/violin/harp/flute | **identical** (held fixed) |
| Model | Llama-3.2-3B base | identical |
| Hparams | canonical L2-6 | identical |
| Cov caches | the 5 durable 3B caches (C-S224-4) | **identical** (model-keyed, not corpus-keyed) |

If cfb-v4 (high AKD) clears the band where cfb-v3 (low AKD) failed 0/5 → **the ceiling is the corpus, not the model**, and the LLM-as-database thesis gets a forward path ("use well-separated keys"). If cfb-v4 also fails → the ceiling is deeper than AKD.

### 0.4 What "clears the band" means, concretely

Same predicate as S2.24: per fact, the post-edit consistency probe must show `P(target_new) > 0.5 AND top-1 == target_new`, aggregated as `≥3 of 5 facts at ≥2/3 trials` (OQ-S212A-2). On cfb-v3 every fact missed this by ~four orders of magnitude. The question is whether high AKD moves it.

### 0.5 Two-surface execution discipline

Inherited verbatim from `t1_alt_model_3b_memit_runbook v0.1` §0.3. **Surface A** = pod terminal (SSH). **Surface B** = JupyterLab notebook. Every cell header carries `[Surface A]` / `[Surface B]` / `[Surface A → B]`.

### 0.6 Block structure (DELTA from S2.24: two new pre-flight cells)

```
═══════════════════════════════════════════════════════════════════
  BLOCK PRE — Cheap pre-flight gates (Cells P0–P1)   ◄── NEW at S2.25
     P0  EasyEdit hparam diff (OQ-S224-EASYEDIT-1a) — desk check,
         no model load; confirms [2-6] band isn't a misconfig
     P1  AKD-compute on BOTH corpora — the independent-variable gate;
         HALTS if cfb-v4 is not actually high-AKD

  BLOCK A — Pre-flight (Cells 0–8)
     Pod bring-up, engine REUSE (no re-clone — engine live on NV),
     patch-state verify, hparam config, Checkpoint #3 bit-exact gate,
     dual-corpus allowlist + pre-edit baseline, cov-cache REUSE
     (no recompute — 5 durable 3B caches from S2.24)

  BLOCK B — Dual-corpus edit dispatch (Cells 9–13)
     B-v3  cfb-v3 LOW-AKD edit (confirmatory; expected 0/5)
     B-v4  cfb-v4 HIGH-AKD edit (the discriminator)
     Cell 13 AKD-verdict gate (extended routing matrix)

  BLOCK C — 15-trial loop (Cells 14–17) [verdict-conditional, cfb-v4]
     Route A halt / Route B 15-trial / Route C 3-trial preview

  BLOCK-END (Cells 18–20)
     Cov-cache integrity gate, NV inventory, manifest extension
═══════════════════════════════════════════════════════════════════
```

### 0.7 Engine-class note (what's REUSED from S2.24, what's NEW)

**Reused live on NV — no setup cost:**
- MEMIT engine SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b`, patched in place at `/workspace/memit_dry_run/memit` (S2.24 §8). **No re-clone.**
- The 5 fresh 3B covariance caches (`/workspace/covariance_caches/meta-llama_Llama-3.2-3B/wikipedia_stats/`, SHA-verified intact at S2.24 Cell 18). **No recompute** — they are model-keyed (wikipedia_stats), not corpus-keyed, so they serve both cfb-v3 and cfb-v4 at L2-L6 (C-S224-4). This saves ~45 min.
- The three 3B model-structure adaptations from S2.24 (D-S224-ADAPT-1): `v_loss_layer=27`, `lm_head_module="model.embed_tokens"` (tied embeddings, C-S224-1), and the fresh-3B cov caches. All carry forward verbatim.

**New at S2.25:**
- Block PRE (two cheap pre-flight gates).
- A second corpus (cfb-v4) and its paired probe set.
- A dual-corpus dispatch in Block B (run both, contrast the surfaces).

---

## Part I — Inheritance Map

### 1.1 Inheritance lineage

```
═══════════════════════════════════════════════════════════════════
        t1_alt_model_3b_memit_runbook v0.1   (DIRECT structural template)
                          │
                          │ structural inheritance
                          │   + Block PRE (AKD + EasyEdit gates)
                          │   + dual-corpus dispatch
                          ▼
        t1_alt_model_3b_memit_akd_runbook v0.1   ◄── (this artifact)
═══════════════════════════════════════════════════════════════════

Control-arm corpus (load-bearing): cfb-v3.yaml v1.0  (the LOW-AKD arm)
Experiment-arm corpus (NEW):       cfb-v4-highAKD.yaml v0.1  (HIGH-AKD)
```

### 1.2 Direct-inheritance surfaces

| Surface | Source | Mode |
|---|---|---|
| Cell decomposition (0–20) | `t1_alt_model_3b_memit_runbook v0.1` | verbatim, with dual-corpus substitution + Block PRE prepend |
| Patch / engine discipline | `memit-patches-canonical v2.5` §6–§7 | verbatim |
| 3B model-structure adaptations | S2.24 `D-S224-ADAPT-1` | verbatim (`v_loss_layer=27`, tied lm_head, fresh cov) |
| Hyperparameter envelope | S2.24 Cell 4 (canonical L2-6) | verbatim |
| Verdict surface taxonomy | `t1_alt_model_3b_memit_runbook v0.1` §Cell 10 | verbatim |
| Copy-Unmount mechanism | `memit-patches-canonical v2.5` (IC-S23-4) | verbatim (4th-config validated S2.24, C-S224-3) |
| Forward routing matrix | S2.24 §10 | REPLACED with AKD-verdict routing (§9 of this runbook) |

### 1.3 Cell delta map (vs `t1_alt_model_3b_memit_runbook v0.1`)

| Cell | Delta class | Notes |
|---|---|---|
| P0 | NEW — EasyEdit hparam diff | desk check; closes OQ-S224-EASYEDIT-1a / informs OQ-S224-2; no model load |
| P1 | NEW — AKD-compute (both corpora) | the independent-variable instrumentation + HARD gate |
| 0 | inherited verbatim | pod bring-up; deps likely already installed on live pod (verify) |
| 1 | REDUCED — engine REUSE | no re-clone; verify engine SHA + patch-state on the live NV engine |
| 1.5 | inherited verbatim | module introspection (re-confirm on reused engine) |
| 2 | REDUCED — patch-state verify | patches already applied in place at S2.24; verify, don't re-apply |
| 3 | APPLICABLE — cov-cache integrity gate | verify the 5 durable 3B caches present + SHA-match (REUSE, not recompute) |
| 4 | inherited verbatim | canonical hparams + 3B adaptations (v_loss_layer=27, tied lm_head) |
| 5 | inherited — Checkpoint #3 bit-exact gate | C-S220-3 gate; extends the 3B determinism chain to checkpoint #3 |
| 6 | EXTENDED — dual-corpus token verify | run for BOTH cfb-v3 and cfb-v4; allowlist `{cfb-v3-004, cfb-v4-004}` |
| 7 | EXTENDED — dual-corpus pre-edit baseline | capture for BOTH corpora |
| 8 | REUSE — no fresh compute | the expensive S2.24 Cell 8 is NOT repeated; caches reused (C-S224-4) |
| 9 | EXTENDED — dual-corpus dispatch | B-v3 (confirmatory) then B-v4 (discriminator) |
| 10 | EXTENDED — dual-corpus verdict surface | per-corpus consistency surface; contrast is the finding |
| 11 | inherited verbatim | Copy-Unmount between corpus dispatches AND at block close |
| 12 | inherited verbatim | per-trial JSON write (per corpus) |
| 13 | REPLACED — AKD-verdict gate | routes on the cfb-v3-vs-cfb-v4 CONTRAST, not a single surface |
| 14–17 | inherited — Block C on cfb-v4 only | 15-trial loop runs on the HIGH-AKD arm if Cell 13 routes B/C |
| 18 | APPLICABLE — cov integrity | verify the reused caches uncorrupted post-session |
| 19–20 | inherited verbatim | NV inventory + manifest extension |

---

## Part II — BLOCK PRE: cheap pre-flight gates (NEW at S2.25)

Both Block-PRE cells are **cheap and run before any edit is dispatched**, by operator decision (S2.25 ratification). They protect the expensive dispatch from two avoidable failure modes: a mis-set layer band (P0) and a corpus that failed to achieve high AKD (P1).

### Cell P0 — EasyEdit hparam diff  [Surface A]

**Specialist:** memit-specialist
**Purpose:** Resolve `OQ-S224-EASYEDIT-1a` and inform `OQ-S224-2`. Before attributing any result to AKD, rule out the alternative that the inherited `[2-6]` band (and `mom2_update_weight=15000`, `v_lr=0.5`, etc.) is simply the wrong config for Llama. EasyEdit (github.com/zjunlp/EasyEdit, MIT) ships community-standard Llama MEMIT hparams; diffing against them is a near-zero-cost sanity check.

**What this does, plainly:** downloads one config file from a maintained open-source repo and compares its numbers to ours. No model load, no GPU. If the numbers match, our config is the community standard and AKD is the clean variable. If they differ materially (especially the layer band), that difference is itself a finding — it would mean S2.24's 0/5 might be a layer-band artifact, and we'd want to know *before* this run.

**Cell body (operator reading order):**
1. Fetch EasyEdit's `hparams/MEMIT/llama-*.yaml` (the Llama MEMIT hparam file) — read-only, from the public repo.
2. Diff against the canonical config (`layers=[2,3,4,5,6]`, `mom2_update_weight=15000`, `v_lr=0.5`, `v_num_grad_steps=25`, `kl_factor=0.0625`, `v_loss_layer` — note theirs targets a different model so `v_loss_layer` / `lm_head` will differ legitimately; flag those as expected-different, not findings).
3. Classify each field: `MATCH` / `EXPECTED-DIFF (model-structure)` / `UNEXPECTED-DIFF`.
4. Print `CELLP0_HPARAM_DIFF_OK <n_match>/<n_fields> unexpected=<list>`.

**Halt conditions:**
- An `UNEXPECTED-DIFF` on the **layer band** specifically → **surface to operator before proceeding.** Not an auto-halt (the inherited band is defensible from S2.15-D2), but a layer-band disagreement with the community standard is load-bearing context for interpreting the AKD verdict, and the operator should ratify proceeding-anyway vs adding a layer-sweep arm.

---

### Cell P1 — AKD-compute on BOTH corpora  [Surface B]

**Specialist:** memit-specialist + validation-contract-architect
**Purpose:** Instrument the independent variable. Compute the MEMIT keys (subject-last-token activations at the edit layer) for all 5 facts of **each** corpus, then the mean pairwise Euclidean distance within each corpus. This is the number the entire session is about. It also retroactively quantifies, for the first time, whether cfb-v3 was in fact low-AKD all along (`OQ-S225-AKD-1`).

**What this does, plainly:** for each fact, run the subject through the model up to the edit layer and grab the activation vector at the subject's last token — that's the "key" / address. Do that for all 5 facts in a corpus, then measure how far apart those 5 addresses are on average. cfb-v3's should come out tiny (addresses bunched); cfb-v4's should come out large (addresses spread). If cfb-v4's is NOT large, the corpus authorship failed and we stop here — no point editing a corpus that didn't achieve the contrast.

**Cell body (operator reading order):**
1. Load Llama-3.2-3B at pinned SHA, fp16 (reuses the Cell 5 load if already up).
2. For each corpus ∈ {cfb-v3, cfb-v4}, for each of the 5 facts:
   - run the subject's prompt through the model, hook the edit layer (use the canonical edit layer for the AKD readout — report per-layer across `[2..6]` and the band mean).
   - extract the key = activation at the subject's last token (the same vector MEMIT's `compute_z` keys on).
3. Per corpus, compute mean pairwise Euclidean distance across the 5 keys (and report the full 5×5 distance matrix per layer for the record).
4. **AKD HARD gate (`C-S225-AKD-1`):** assert `mean_AKD(cfb-v4) > mean_AKD(cfb-v3)` by a clear margin at the band mean. The threshold is RELATIVE (set from the observed cfb-v3 floor), because key-space scale is model/layer-dependent — an absolute threshold would be meaningless. Recommend gate: `mean_AKD(cfb-v4) ≥ 5 × mean_AKD(cfb-v3)` as the "clearly separated" bar; operator ratifies the exact multiple from the observed numbers.
5. Print `CELLP1_AKD_OK cfb_v3_mean=<x> cfb_v4_mean=<y> ratio=<y/x> gate=<PASS|FAIL>`.

**Halt conditions:**
- `mean_AKD(cfb-v4) ≤ mean_AKD(cfb-v3)` or below the ratified margin → **HALT.** Corpus authorship failed to achieve high AKD; revise cfb-v4 subjects/templates and re-version before any edit dispatch. This is the gate that makes a wasted edit impossible.
- cfb-v3 mean-AKD NOT near-0 (i.e. cfb-v3 is unexpectedly high-AKD) → **surface to operator.** This would mean the low-AKD interpretation of the seven-axis ceiling is wrong, which reframes the whole session — pause and re-interpret before proceeding.

**Operator-facing readout note:** the cfb-v3 number here is itself a finding. If it is near-0 as predicted, that is the first direct measurement confirming the seven-axis ceiling ran on a degenerate-key corpus — record it prominently in the summary regardless of the cfb-v4 verdict.

---

## Part III — BLOCK A: Pre-flight (REUSE-heavy)

> Block A inherits `t1_alt_model_3b_memit_runbook v0.1` Cells 0–8 verbatim **except** for the reductions noted: engine and cov-caches are REUSED from the live S2.24 NV state, not rebuilt. Only the deltas are spelled out below; unchanged cell bodies carry forward by reference.

### Cell 0 — Pod bring-up + dependency verify  [Surface A]
Inherited. If the pod is the same instance as S2.24 (`ee00aa7bcadb`), deps are already present — **verify, don't reinstall**: print `CELL0_DEPS_OK <transformers> <accelerate>` and confirm `nvidia-smi` (RTX 4090 24 GiB) + `ls /workspace` (expect `covariance_caches/meta-llama_Llama-3.2-3B/`, the engine at `memit_dry_run/memit`). If a fresh pod, full install per S2.24 §11 prerequisite (note: fresh images ship WITHOUT rsync — and may lack the deps; reinstall).

### Cell 1 — Engine REUSE + SHA verify  [Surface A]
REDUCED. **No re-clone.** Verify the live engine at `/workspace/memit_dry_run/memit` is at SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` and the patches are applied in place (S2.24). Print `MEMIT_ENGINE_SHA <sha>` and `ENGINE_REUSE_OK`. Halt if SHA mismatch (engine drift).

### Cell 2 — Patch-state verify  [Surface A → B]
REDUCED. Patches were applied in place at S2.24; **verify, don't re-apply.** Confirm the patch markers present at each patch site (P-1/P-2/P-4/P-5/P-6/P-7 + Pad-Token); print `CELL2_PATCH_STATE_OK <patches_applied dict>`. Any missing marker → halt (engine state drifted since S2.24).

### Cell 3 — Cov-cache integrity gate (REUSE)  [Surface A]
APPLICABLE. Verify the 5 durable 3B caches are present at `/workspace/covariance_caches/meta-llama_Llama-3.2-3B/wikipedia_stats/` (each 268,436,642 bytes, (8192,8192) float32) and SHA-match the S2.24 Cell 18 provenance record. Print `COV_CACHE_3B_PRESENT — integrity OK 5/5` (REUSE confirmed). On MISMATCH → halt (caches corrupted since S2.24; would force a fresh ~45 min recompute — surface to operator).

### Cell 4 — Hyperparameter config (+ 3B adaptations)  [Surface B]
Inherited verbatim. Canonical L2-6 hparams (`mom2_update_weight=15000`, `v_lr=0.5`, `v_num_grad_steps=25`, `kl_factor=0.0625`) PLUS the S2.24 3B adaptations (`D-S224-ADAPT-1`): `v_loss_layer=27`, `lm_head_module="model.embed_tokens"` (tied embeddings per C-S224-1). Bound assertion `[2..6] < 28` (C-S224-2). Print `CELL4_HPARAM_OK` + `LAYER_BOUND_OK [2..6] < 28`.

### Cell 5 — Checkpoint #3 bit-exact gate  [Surface B]
Inherited. Load 3B at pinned SHA fp16; re-capture the 38-probe panel; run the C-S220-3 combined gate (top-1 strict equality + drift `< 1e-5`) against the baseline. PASS extends the 3B determinism chain to **Checkpoint #3** (S2.22 #1 GRACE → S2.24 #2 MEMIT → S2.25 #3 MEMIT-AKD). Print `CHECKPOINT_3_3B_OK drift_max=<value>`. FAIL → halt.

### Cell 6 — Dual-corpus token verify + allowlist  [Surface B]
EXTENDED. Run the Cell 6 token verification for **both** corpora. Targets are identical across corpora (guitar/piano/violin/harp/flute) — re-verify single-token property on the 3B tokenizer and confirm harp → `[4960, 79]` first-token-proxy in each. `MULTI_TOKEN_ALLOWLIST = {"cfb-v3-004", "cfb-v4-004"}`. SUBSET hard gate per corpus. Print `CELL6_TOKEN_VERIFY_OK` with per-corpus verdict_class maps.

### Cell 7 — Dual-corpus pre-edit baseline  [Surface B]
EXTENDED. Capture the pre-edit probe panel for both corpora's probe sets. Cross-check against Cell 5. Note: cfb-v4 facts use the FRESH subjects/templates — confirm none of the high-freq targets (guitar/piano) pre-floods above the 0.05 ceiling at its distinct template (the cfb-v4 acceptance band risk). Print `CELL7_BASELINE_OK` per corpus.

### Cell 8 — Cov-cache REUSE (no compute)  [Surface A]
REUSE. The expensive fresh-compute cell from S2.24 is **NOT repeated.** Confirm `cov_cache_compute_required = False` (caches present + integrity OK from Cell 3). Print `CELL8_COV_REUSE_OK 5/5 (no recompute; C-S224-4)`. This is the ~45 min saving.

---

## Part IV — BLOCK B: dual-corpus edit dispatch + AKD-verdict gate

### Cell 9 — Dual-corpus MEMIT dispatch  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist + state-consistency-theorist
**Purpose:** Dispatch the MEMIT joint-overlay 5-fact edit on **each** corpus and capture the post-edit surface. The order matters for cleanliness: run the control first (confirm the known 0/5 reproduces on cfb-v3 in this exact session/pod state), then the discriminator (cfb-v4). Copy-Unmount between them so each edit starts from the identical pristine model.

**Cell body (operator reading order):**
1. **B-v3 (control, confirmatory):** pre-edit panel → MEMIT 5-fact joint overlay at L2-L6 on cfb-v3 (reusing the durable caches) → post-edit panel. Expected: the S2.24 0/5 reproduces (huge internal `compute_z` progress, ~4-orders external miss, top-1 never the target). Print the per-fact consistency surface.
2. **Copy-Unmount** back to pristine (IC-S23-4 bit-exact gate; drift `< 1e-4`).
3. **B-v4 (discriminator):** pre-edit panel → MEMIT 5-fact joint overlay at L2-L6 on cfb-v4 (same caches, same hparams) → post-edit panel. **RE-EVALUATE gate at trial 0 for cfb-v4-004** (harp first-token-proxy). Print the per-fact consistency surface.
4. **Copy-Unmount** back to pristine.
5. Print `CELL9_DISPATCH_OK` with both per-corpus post-edit consistency surfaces side by side.

**Halt conditions:**
- Edit dispatch OOM on either corpus → halt (FAIL at environment; unexpected — S2.24 peaked 8.41 GiB).
- Cov-cache lookup miss at edit time (`_t100_` filename mismatch) → halt (P-7 dispatch regression).
- IC-S23-4 unmount band exceeded between dispatches → halt (Copy-Unmount regression; the two arms would no longer start from identical state).

### Cell 10 — Dual-corpus verdict surface  [Surface B]
EXTENDED. Aggregate each corpus's post-edit panel into the per-fact consistency/generalization/specificity surface. **The contrast IS the finding.** Print `CELL10_VERDICT_SURFACE` as a two-column table: cfb-v3 (control) vs cfb-v4 (high-AKD), per fact, with the `compute_z` internal-progress vs external-P(target) gap shown for each (the seven-axis fingerprint — does cfb-v4 close it?).

### Cell 11 — Copy-Unmount + post-unmount panel  [Surface B]
Inherited verbatim. Already exercised between the two dispatches in Cell 9; this cell is the final block-close unmount + post-unmount panel + IC-S23-4 HARD gate. Print `CELL11_UNMOUNT_OK drift_max=<value>` (validates Copy-Unmount 5th-config-class: MEMIT-3B-dual-corpus).

### Cell 12 — Per-trial JSON write  [Surface B]
Inherited verbatim, per corpus. Includes the `v1_7_proxy_annotation` for both `cfb-v3-004` and `cfb-v4-004`. Print `CELL12_JSON_WRITE_OK <path>` per corpus.

### Cell 13 — AKD-verdict gate (REPLACES S2.24 single-surface routing)  [Surface B]

**Specialist:** validation-contract-architect + memit-specialist + framework-spec-writer
**Purpose:** Route on the **contrast** between the two corpora, not a single surface. This is the cell that answers `OQ-S224-LIT-1`.

**Cell body (operator reading order):**
1. Read: cfb-v3 per-fact consistency PASS-rate, cfb-v4 per-fact consistency PASS-rate, and the Cell P1 AKD readout (the contrast must be interpreted against confirmed-high AKD — a cfb-v4 PASS only means "AKD" if AKD was in fact high, which P1 gated).
2. Apply the AKD-verdict gate:
   - **Route AKD-PASS (→ Block C on cfb-v4):** cfb-v4 clears or approaches the band for `≥3 of 5` facts while cfb-v3 reproduces ~0/5. **Ceiling localizes to corpus AKD, not the model.** Run Block C 15-trial loop on cfb-v4 to establish the PASS aggregate with replicates. Highest-value outcome.
   - **Route AKD-FAIL (→ HALT, single confirmatory pass):** cfb-v4 ALSO reproduces ~0/5 despite confirmed-high AKD. AKD is insufficient to explain the ceiling; it is a deeper model-family property (or a layer-band artifact — see P0). Block C runs at most one confirmatory pass.
   - **Route AKD-PARTIAL (→ 3-trial preview on cfb-v4):** cfb-v4 partially clears (1–2 facts). AKD contributing but not sufficient. Reduced 3-trial preview before committing.
3. Print `CELL13_ROUTE <AKD-PASS|AKD-FAIL|AKD-PARTIAL>` with the rationale (both per-corpus PASS-rates + the AKD ratio from P1).

**Calibration-criteria note (resolved):** `OQ-S222-CALIBRATION-CRITERIA-MISMATCH-1` was CLOSED at S2.24 (`D-S224-CALIB-1`): the runbook §3.2.2 `max(gen_p_target_new) > 0.3` movement predicate is canonical for generalization; the `probe-set-v3.yaml §126 drift < 0.05` predicate is a mislabeled LOCALITY predicate and is SUPERSEDED for generalization. This carries forward — no re-litigation. The paired `probe-set-v4-highAKD.yaml` must adopt the same disposition at authoring.

**Halt conditions:**
- Route AKD-FAIL → Block C ≤1 confirmatory pass (or halt per operator).
- AKD readout from P1 was a gate-FAIL that was overridden → verdict NOT ratifiable (a cfb-v4 result on a non-high-AKD corpus answers nothing); halt.

---

## Part V — BLOCK C: 15-trial loop (cfb-v4, verdict-conditional)

Inherits `t1_alt_model_3b_memit_runbook v0.1` Cells 14–17 verbatim, scoped to the **cfb-v4** arm (the discriminator). The cfb-v3 control does not need replicates — its 0/5 is established across two sessions and eight axes; a single confirmatory dispatch in Cell 9 suffices (mirrors `D-S224-BLOCKC-SKIP-1` rationale).

- **Cell 14 — Trial matrix:** 5 cfb-v4 facts × replicates per route (AKD-PASS: 3 → 15 trials; AKD-PARTIAL: 1 → 5 trials; AKD-FAIL: ≤1 confirmatory). SUBSET gate (Cell 6 cfb-v4 verdict set ⊇ trial set ⊇ allowlist). Print `CELL14_TRIAL_MATRIX <route> <n_trials>`.
- **Cell 15 — Trial loop body:** per trial: pre-edit → MEMIT edit (cfb-v4, canonical hparams, reused caches) → post-edit → RE-EVALUATE gate at trial 0 for cfb-v4-004 → Copy-Unmount + IC-S23-4 HARD gate → per-trial JSON. STRICT-fact bit-exact preservation for the 4 STRICT cfb-v4 facts (D-S217-4 / D-S218-7). Print `CELL15_TRIAL <id> verdict=<...>`.
- **Cell 16 — Per-fact aggregation:** `≥3 of 5 facts at ≥2/3 trials` (OQ-S212A-2). Print `CELL16_AGGREGATE consistency_pass_facts=<n>/5`.
- **Cell 17 — Gen/spec/unmount aggregation:** generalization mean drift (using the `max(gen_p_target_new) > 0.3` movement predicate per D-S224-CALIB-1), specificity drift, unmount HARD-gate status. Print `CELL17_AUX_AGGREGATE gen_drift=<...> spec_drift=<...> unmount=<PASS|FAIL>`.

---

## Part VI — BLOCK-END

- **Cell 18 — Cov-cache integrity gate:** re-checksum the 5 reused 3B caches; compare to S2.24 Cell 18 provenance (MEMIT is read-only on them; must still match). Print `CELL18_COV_INTEGRITY_OK 5/5 sha_match=True`. The caches remain a durable reusable asset (C-S224-4) for any successor high-AKD work.
- **Cell 19 — NV inventory:** list session outputs (`/workspace/t1_alt_model_3b_memit_akd_*/`, dual-corpus per-trial JSONs, AKD readout JSON, session log). Caches added: none (reuse). Print `CELL19_NV_INVENTORY_OK`.
- **Cell 20 — Manifest extension:** append `sessions["2.26"]` (execution session) to `reproducibility_manifest.json`: model SHA, engine SHA, patch-state, cov-cache provenance (reused), Checkpoint #3 drift, AKD readout (cfb-v3 + cfb-v4 means + ratio), dual-corpus verdict surface, Cell 13 route. Print `CELL20_MANIFEST_OK <entry_id>`.

---

## Part VII — Forward Routing Matrix — S2.26 Cell 13 → S2.27

```
═══════════════════════════════════════════════════════════════════
  AKD-PASS (cfb-v4 HIGH clears band ≥3/5; cfb-v3 LOW ~0/5):
    └── THE high-value outcome. The seven-axis "architectural-
        invariant ceiling" REFRAMES to a low-AKD-corpus ceiling.
    └── v1.3 framework_finding amendment: "ceiling is corpus-
        structural (low-AKD key collision), NOT model-invariant."
    └── WS3 guidance unlocked: LLM-as-database viable with well-
        separated keys (high-AKD corpus design).
    └── S2.27 = KnowEdit external-validity confirmation (literature-
        standard high-AKD benchmark) + base-vs-instruct control
        (OQ-S225-BASE-INSTRUCT-1), as SEPARATE single-variable arms.

  AKD-FAIL (cfb-v4 HIGH also ~0/5 despite confirmed-high AKD):
    └── AKD insufficient. Ceiling is deeper than key separation.
    └── v1.3 amendment: AKD ELIMINATED as sufficient explanation;
        ceiling survives key-separation under low-batch joint dispatch.
    └── S2.27 = per-layer sweep (Berkeley recipe — is [2-6] even the
        right band on 3B?) + sequential-vs-joint dispatch axis
        (OQ-S224-LIT-1 items 3-4), holding AKD high.

  AKD-PARTIAL (cfb-v4 1-2 facts clear):
    └── AKD contributing, not sufficient.
    └── S2.27 = dispatch-mode axis (sequential vs joint) holding AKD
        high, to isolate batch-interference as the residual factor.

  AKD-gate FAIL at P1 (cfb-v4 not actually high-AKD):
    └── No verdict. Corpus authorship halt; revise cfb-v4 + re-version.
═══════════════════════════════════════════════════════════════════
```

---

## Part VIII — Decision + Constraint Registry

### 8.1 Decisions (this runbook)

| ID | Statement |
|---|---|
| D-S225-Q1-1 | Corpus source: hand-authored high-AKD `cfb-v4-highAKD.yaml` (NOT KnowEdit) — clean single-variable contrast; KnowEdit deferred to S2.27 external-validity arm. (Operator-ratified 2026-06-15.) |
| D-S225-Q2-1 | AKD instrumentation added as Cell P1 pre-flight HARD gate on BOTH corpora. |
| D-S225-Q3-1 | Base-vs-instruct control DEFERRED (OQ-S225-BASE-INSTRUCT-1); S2.26 runs base-only, single-variable on AKD. |
| D-S225-Q4-1 | EasyEdit hparam diff added as Cell P0 desk-check pre-flight (no model load). |
| D-S225-Q5-1 | Fact count = 5 (matched pair with cfb-v3); targets held IDENTICAL across corpora; only keys vary. |
| D-S225-REUSE-1 | Engine + 5 cov caches + 3B adaptations REUSED live from S2.24 NV state; no re-clone, no recompute (C-S224-4). |
| D-S225-CTRL-1 | cfb-v3 runs as in-session confirmatory control (single dispatch, no replicates, per D-S224-BLOCKC-SKIP-1 rationale); Block C replicates scoped to cfb-v4 only. |

### 8.2 Constraints (this runbook)

| ID | Statement |
|---|---|
| C-S225-AKD-1 | Cell P1 AKD HARD gate: `mean_AKD(cfb-v4) > mean_AKD(cfb-v3)` by ratified relative margin (recommend ≥5×) at the L2-6 band mean; FAIL → HALT before any edit. |
| C-S225-1 | Targets held byte-identical to cfb-v3 across cfb-v4 (target-invariance under key-variance); any target substitution voids the clean contrast. |
| C-S225-2 | Both edits dispatch from bit-exact-identical pristine model state (Copy-Unmount between B-v3 and B-v4; IC-S23-4 gate between dispatches). |
| C-S225-3 | cfb-v4 result is verdict-ratifiable ONLY if P1 AKD gate PASSED (a result on a non-high-AKD corpus answers nothing). |
| C-S225-4 | Reused cov caches re-checksummed at Cell 3 (entry) AND Cell 18 (exit); any mismatch halts. |

### 8.3 Inherited carry-forward anchors (NOT re-numbered)

| Anchor | Source | Disposition |
|---|---|---|
| D-S224-ADAPT-1 | S2.24 3B model-structure adaptations | APPLICABLE at Cell 4 (`v_loss_layer=27`, tied lm_head) |
| C-S224-1 | tied embeddings → `model.embed_tokens` | APPLICABLE at Cell 4 |
| C-S224-2 | `v_loss_layer = n_layers − 1` per model | APPLICABLE at Cell 4 (3B = 27) |
| C-S224-3 | Copy-Unmount 4th-config validated | APPLICABLE at Cell 9 / 11 (extends to 5th config class) |
| C-S224-4 | 5 durable 3B cov caches reusable | APPLICABLE at Cell 3 / 8 / 18 (REUSE) |
| D-S224-CALIB-1 | generalization = movement predicate `max(gen_p_target_new) > 0.3` | APPLICABLE at Cell 13 / 17 |
| IC-S23-4 | unmount band HARD gate (drift < 1e-4) | APPLICABLE at Cell 9 / 11 / 15 |
| IC-S24-4 | 5×3 trial protocol | APPLICABLE at Cell 14 (cfb-v4 arm) |
| C-S220-3 | combined bit-exact gate | APPLICABLE at Cell 5 (Checkpoint #3) |
| D-V12-MULTITOKEN-1 | MULTI_TOKEN_ALLOWLIST absorption | APPLICABLE at Cell 6 / 9 / 15 (both -004 facts) |

---

## Part IX — Open Questions

| ID | Statement | Closes when |
|---|---|---|
| OQ-S225-AKD-1 | Does cfb-v3 measure as low-AKD on 3B at L2-6? (first direct measurement) | Cell P1 |
| OQ-S225-AKD-2 | If cfb-v4 PASSES, is the PASS frequency-correlated? | Cell 13 / 16 |
| OQ-S225-TEMPLATE-CONFOUND-1 | cfb-v4 varies subject-domain AND template jointly; v5 could disentangle | deferred |
| OQ-S225-BASE-INSTRUCT-1 | base-vs-instruct deferred to a separate S2.27 arm | S2.27 |
| OQ-S224-2 | is inherited [2-6] band correct for Llama? (P0 informs; per-layer sweep resolves) | P0 (partial) / S2.27 sweep |
| OQ-S224-EASYEDIT-1a | EasyEdit hparam diff | Cell P0 |

---

## Part X — Non-Goals

This runbook v0.1 does NOT:
1. **Execute.** v0.1 is declarative authoring; pod-side execution at S2.26.
2. **Re-tune MEMIT hparams.** Canonical L2-6 + 3B adaptations inherited verbatim; AKD is the only deliberate variable.
3. **Vary targets.** Targets held identical to cfb-v3 (C-S225-1).
4. **Run an Instruct arm.** Base-only by design (D-S225-Q3-1).
5. **Adopt KnowEdit.** Hand-authored cfb-v4 is the S2.26 discriminator; KnowEdit is the S2.27 external-validity arm (D-S225-Q1-1).
6. **Recompute cov caches.** Reused from S2.24 (D-S225-REUSE-1).
7. **Re-clone the engine.** Reused live from NV (D-S225-REUSE-1).
8. **Modify `memit-patches-canonical v2.5`, `cfb-v3.yaml v1.0`, or any S2.24 artifact.** All inherited; preserved unmodified.
9. **Author the v1.3 framework_finding amendment.** v1.3 is a separate deliverable conditional on the S2.26 verdict.
10. **Author runtime implementation code.** Cell bodies are operator-reading-order specifications + acceptance-string contracts; code runs pod-side.

---

## Part XI — Acceptance-string index (execution verification)

```
CELLP0_HPARAM_DIFF_OK <n_match>/<n_fields> unexpected=<list>
CELLP1_AKD_OK cfb_v3_mean=<x> cfb_v4_mean=<y> ratio=<y/x> gate=<PASS|FAIL>
CELL0_DEPS_OK <transformers> <accelerate>
MEMIT_ENGINE_SHA <sha>   /   ENGINE_REUSE_OK
CELL2_PATCH_STATE_OK <patches_applied dict>
COV_CACHE_3B_PRESENT — integrity OK 5/5   (REUSE)
LAYER_BOUND_OK [2..6] < 28   /   CELL4_HPARAM_OK <config>
CHECKPOINT_3_3B_OK drift_max=<value>
CELL6_TOKEN_VERIFY_OK <per-corpus verdict_class map>
CELL7_BASELINE_OK <per corpus>
CELL8_COV_REUSE_OK 5/5 (no recompute; C-S224-4)
CELL9_DISPATCH_OK <cfb-v3 surface | cfb-v4 surface>
CELL10_VERDICT_SURFACE <two-column contrast>
CELL11_UNMOUNT_OK drift_max=<value>
CELL12_JSON_WRITE_OK <path>   (per corpus)
CELL13_ROUTE <AKD-PASS|AKD-FAIL|AKD-PARTIAL>
CELL14_TRIAL_MATRIX <route> <n_trials>   (cfb-v4)
CELL15_TRIAL <id> verdict=<...>   (per trial)
CELL16_AGGREGATE consistency_pass_facts=<n>/5
CELL17_AUX_AGGREGATE gen_drift=<...> spec_drift=<...> unmount=<PASS|FAIL>
CELL18_COV_INTEGRITY_OK 5/5 sha_match=True
CELL19_NV_INVENTORY_OK <manifest>
CELL20_MANIFEST_OK <entry_id>
```

---

**Runbook v0.1 status:** DECLARATIVE — READY FOR S2.26 EXECUTION
**Artifact set status (per standing directive — no operator editing):** FULLY AUTHORED. `cfb-v4-highAKD.yaml v1.0` (subjects + templates locked: Heisenberg / Schenker / the Danube / the Python programming language / Mount Kilimanjaro; 5 distinct templates) and `probe-set-v4-highAKD.yaml v1.0` (38 probes; roster-integrity validated) are complete. No pre-session operator obligations remain. All remaining `TBD-CAPTURE-S226` markers are pod-side capture steps (token IDs, pre-edit probabilities, AKD) executed by Claude walking the runbook at S2.26; structural content is locked.
**Persistence:** `/mnt/user-data/outputs/t1_alt_model_3b_memit_akd_runbook_v0_1.md`

*End T.1-α-MEMIT-AKD runbook v0.1.*
