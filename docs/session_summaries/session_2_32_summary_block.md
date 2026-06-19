# Session 2.32 Summary Block — T.3-β-QWEN CLEAR-Hardening + Mistral CPU-Solve Re-Confirm (EXECUTED)

**Session type:** Execution (pod-side; two arms through the `P-VRAM-CPU-SOLVE`-patched engine)
**Date:** 2026-06-15
**Predecessor:** S2.31 — Qwen2.5-7B CLEARED 5/5 (single dispatch); ceiling narrowed G→Llama-lineage; CPU-solve confound exonerated
**Successor:** S2.33 (verdict-conditional — see §10)
**Verdict:** **Qwen CLEAR is finding-grade AND qualified.** The edit *expresses* (5/5 consistency, stable ×4 trials) where Llama-lineage cannot — but it is **entity-local-not-attribute-local**: it collaterally perturbs the edited entity's own biographical attributes (generalization 3/15, stable) while leaving non-edited entities pristine (specificity 3/3). **Mistral re-confirms 0/5 through the patched engine** — the within-engine Llama-lineage-holds/Qwen-clears contrast is established.

---

## §1. One-Line Result

`Qwen/Qwen2.5-7B` under byte-identical canonical MEMIT through the `P-VRAM-CPU-SOLVE`-patched engine **clears consistency 5/5 (stable across 4 trials)** but the expressed edit is **not attribute-local** — it disrupts the edited subjects' own unrelated biographical facts (12/12 same-subject generalization failures, large directional drift, bit-exact reversible) while leaving shared world-knowledge specificity pristine (3/3). The same patched engine reproduces the **Mistral-7B-v0.3 ceiling at 0/5** (S2.29-identical config, S2.29-pinned SHA), closing the patch-confound thread for the Llama-lineage-holds side. The CLEAR is real, expressed, entity-confined, and collateral-damaging — a sharper result than the kickoff's promote-vs-qualify binary.

---

## §2. Deliverables (RATIFIED 2026-06-15)

| Artifact | Status |
|---|---|
| `session_2_32_summary_block.md` | this artifact |
| `memit-patches-canonical v2.6` | ADDITIVE — codifies `P-VRAM-CPU-SOLVE` as conditional SOURCE_LAYER patch (deferred S2.31 item); §1–§10 of v2.5 unmodified |
| `framework_finding_memit_ceiling_archival v1.6` | ADDITIVE (Axis 11 CLEAR-hardening; finding-grade-AND-qualified disposition); v1.0–v1.5 PERMANENT preserved verbatim |

---

## §3. Execution-Resolved Literals (captured this session)

**Engine state:**
- Engine SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` (byte-identical to all prior axes) + `P-VRAM-CPU-SOLVE`
- Patched `memit_main.py` SHA-256: `5c0c706a66c385273d0a48ebbb8274a1c31bf3e101ca309e47db9cb8b6c78770`
- Pristine `memit_main.py` SHA-256: `186e961633211046379cd594016b9f879741121bee3bb8cf163173c832f75b69`
- Sibling-file fingerprint (unchanged through patch): `compute_z` `30d3a7c4…`, `compute_ks` `0b039be4…`, `layer_stats` `be92a521…`, `compute_u` `06a73593…`, `nethook` `20e84c94…`
- Patch re-applied via `patch -p0` (the `cpu_solve_patch.diff` is in `diff -c` normal format, NOT unified — `git apply` rejects it with `error: unrecognized input`; `patch` reads it natively). Pristine backup at `memit/memit_main.py.upstream_pristine_s232`.

**Qwen arm:**
- Model SHA `d149729398750b98c0af14eb82c78cfe92750796`, fp16, n_layers 28 / hidden 3584 / inter 18944 / vocab 152064
- Checkpoint #1 (on this kernel, fresh): drift `0.00e+00`, 0/5 mismatch — determinism re-established
- Natural top-1 all 5 = ` the` (id 279), p 0.19–0.37 (clean pre-edit regime; OQ-S230-QWEN-TOP1-1 re-confirmed)
- Token resolution: guitar `[16986]`, piano `[26278]`, violin `[62037]`, flute `[95712]` STRICT; harp `[4855,79]` PROXY → 4/5 STRICT; integrity subset {001/002/005} **3/3 STRICT** (load-bearing read at full single-token fidelity)
- Edit: band [4,5,6,7,8], v_loss_layer 27, dispatch 9.9 min, VRAM peak 19.39 GiB; compute_z converged all 5 (guitar 0.0047→0.9903; piano 0.0129→0.9965; violin 0.0042→0.9992; harp 0.0192→0.9932; flute 0.0042→0.9803)
- Cov caches: 5×L4-8 SHA-256-verified bit-exact unchanged vs S2.31 (L4 `b54c48ae…`, L5 `8e468c9f…`, L6 `6b0150dd…`, L7 `d066dee6…`, L8 `4d9238e5…`)

**Mistral arm:**
- Model SHA `caa1feb0e54d415e2df31207e5f4e273e33509b1` (S2.29-pinned; recovered from `/workspace/architecture_profile/reproducibility_manifest.json`), fp16, n_layers 32 / hidden 4096 / inter 14336 / vocab 32768
- Token resolution: guitar `[11454]`, piano `[13989]` STRICT; violin/harp/flute 2-token PROXY → 2/5 STRICT (S2.29-identical)
- Pad-Token patch applied (pad=eos=`</s>` id 2) — required for Mistral; was a no-op on Qwen (`<|endoftext|>` doubles as pad)
- Edit: band [4,5,6,7,8], v_loss_layer **31** (unmodified canonical; Mistral n−1=31), dispatch 2.4 min, VRAM peak 18.08 GiB

---

## §4. Arm 1 — Qwen CLEAR-Hardening (full 38-probe panel × 4 trials)

### §4.1 Consistency (the external read) — 5/5 aggregate, surface-form-sensitive

Per-fact aggregate (≥2/3 consistency probes PASS): **5/5 facts PASS, stable across all 4 trials.** Per-surface-form:

| Surface form | Prompt template | Pass rate |
|---|---|---|
| cons-1 | "{X} plays the musical instrument of" | **5/5** |
| cons-3 | "{X} is a musician who plays the" | **5/5** |
| cons-2 | "The instrument that {X} plays is" (cleft) | **2/5** |

The cons-2 cleft form is the hardest (subject displaced from the prompt-end where `fact_token="subject_last"` anchors the edit key). On cons-2: guitar 0.47 (top-1 *moved* to guitar but P just below 0.5), harp 0.38 (top-1 moved, below band), flute 0.0018 (did not take, top-1 ` a`). piano/violin pass cons-2. **The edit generalizes across two of three independent surface forms** — not canonical-prompt-only.

### §4.2 Internal-vs-external — signature ABSENT (the Qwen result)

All 5 facts: internal compute_z converged (>0.98) AND external cons-1 followed (0.986–0.999), top-1 moved to target on all 5. The Llama-lineage internal-vs-external split does **not** reproduce on Qwen. Confirms S2.31 on this kernel.

### §4.3 Generalization (locality) — 3/15, the load-bearing qualifier

Generalization predicate (probe-set-v3 §126): `abs(Δp_top_1) < 0.05 AND top_1 unmoved` vs the Qwen-captured pre-edit baseline.

**Result: 3/15 PASS, stable across all 4 trials.** All 12 failures are on the **edited subjects' own biographical probes** (Bo Jackson, Tiger Woods, Deion Sanders, Hakeem Olajuwon, Lindsey Vonn). Drift is large and directional: Hakeem "born in the country of" Nigeria 0.831→0.189 (Δ0.642); Deion born-state Georgia 0.313→0.747 (Δ0.434); biographical top-1s move (Auburn→the, Stanford→the, Florida→the, Mississippi→Texas, Colorado→New). The 3 passes are scattered across non-collapsing biographical probes.

**Mechanistic reading:** the MEMIT edit at L4-8 on `{subject} plays the instrument of` does not merely install the instrument association — it perturbs the model's broader representation of *that subject*, so the same subject's college/birthplace answers shift. The edit is **subject-local but not fact-local** — it changes more about the entity than just the target attribute.

### §4.4 Specificity — 3/3 pristine (perturbation is entity-confined, not global)

Shared world-fact probes (name no edited subject): France→Paris (Δ0.005), Jupiter (Δ0.001), gold→Au (Δ0.001). **3/3 PASS, stable ×4.** The edit does not bleed into unrelated world knowledge. Combined with §4.3, the perturbation is **confined to the five edited entities**, not a global degradation.

### §4.5 Unmount — bit-exact, 7th config, AND edit-attribution proof

Copy-Unmount restored L4-8 down_proj from `orig_weights`: all 5 unmount probes at **`drift = 0.00e+00`** (six-decimal exact restore), stable ×4. **7th validated Copy-Unmount config, 2nd non-Llama (IC-S23-4).** Critically, the §4.3 biographical drift **reverses bit-exact on unmount** (Nigeria → 0.831, Stanford → 0.656, Auburn → 0.149, all Δ vs pre = 0.00e+00) — proving the collateral perturbation is **edit-caused and edit-removable**, not pre-existing state or measurement noise. The qualification is causally grounded.

### §4.6 Stability matrix (Route C, 4 trials)

| Metric | trial 0 | 1 | 2 | 3 | stable |
|---|---|---|---|---|---|
| consistency facts (≥2/3) | 5 | 5 | 5 | 5 | ✓ |
| generalization local | 3/15 | 3/15 | 3/15 | 3/15 | ✓ |
| specificity | 3/3 | 3/3 | 3/3 | 3/3 | ✓ |
| unmount drift_max | 0.0 | 0.0 | 0.0 | 0.0 | ✓ |

Deterministic reproduction to the value — vindicating the Route-C call (3 replicates carry the same evidentiary weight as 15 on a proven-deterministic engine far from every band). Resolves **OQ-S231-CLEAR-ROBUSTNESS-1**.

---

## §5. Arm 2 — Mistral Re-Confirm (single confirmatory dispatch, patched engine)

Mistral-7B-v0.3 (S2.29-pinned SHA, S2.29-identical config: band [4-8], v_loss_layer 31 unmodified, pad=eos) through the `P-VRAM-CPU-SOLVE`-patched engine: **consistency 0/5.** Post-edit top-1s reassert native priors — `'his'`, `'golf'` (Tiger Woods), `'the'`, `'basketball'` (Hakeem), `'the'`. The edit ran to completion (no OOM, 2.4 min, 18.08 GiB) — the ceiling is a *result*, not a crash. Post-edit target probabilities at floor (8.4e-04–1.98e-03), *lower* than pre-edit in 4/5 (the edit pushes cluster mass without landing on the target — the genuine Llama-lineage signature).

**This closes the patch-confound thread on the holds side.** Arm 1 (and S2.31 §4) proved the patch cannot *manufacture* a CLEAR (Llama isolation). Arm 2 proves it cannot manufacture a *hold* either (Mistral runs clean through the patched engine, still 0/5). The within-engine contrast is complete: **same patched engine — Qwen converges >0.98 and expresses 5/5; Mistral crawls and holds 0/5.** The difference is architecture lineage. Resolves **t_branch v1.4 §4'''' Axis 4**.

---

## §6. Decisions (D-S232-*)

| ID | Statement |
|---|---|
| D-S232-CALIB-1 | OQ-S222-CALIBRATION-CRITERIA-MISMATCH-1 **CLOSED.** probe-set-v3 §126 `acceptance_bands_provisional` is the single authoritative predicate source. Generalization predicate (`abs(Δp_top_1)<0.05`) is byte-identical runbook↔probe-set — no value conflict. Residue was specification-completeness (runbook Cell 10 one-liner echoed only the post-edit limb of two-limbed specificity; Cell 17 implements both). Generalization is a **locality** test on pre-edit top-1 drift, NOT a paraphrase test (paraphrase robustness carried by the 3 surface-varied consistency probes). |
| D-S232-GEN-BASELINE-1 | Generalization/specificity locality evaluated against **Qwen-captured pre-edit top-1 (Cell 7), NOT probe-set-v3 Llama-captured `expected_top_1`** (the YAML's `target_model` is Llama-3.1-8B). Function-word and Qwen-variant biographical top-1s are valid stability anchors. The §4.3 failures survive this caveat — they are large-magnitude drifts on substantive biographical tokens, not anchor noise. |
| D-S232-BAND-OVERRIDE-1 | The "single-integer delta" claim is against the proven Mistral config, NOT `hparams/MEMIT/Llama-3.1-8B.json` (whose `layers:[2,3,4,5,6]` is a stale default). Auditable port surface is two fields: `v_loss_layer` (ARCH-FORCED, n−1) + `layers→[4,5,6,7,8]` (PORT-CONSTANT, Axis-9-equivalent, cache-matched, S2.31/Mistral parity). v_loss_layer is the only architecture-forced delta. |
| D-S232-CLEAR-GRADE-1 | Qwen CLEAR is **finding-grade but surface-form-sensitive**: robust on cons-1/cons-3 (5/5 each), soft on cons-2 cleft (2/5). Materially different from the Llama-lineage ceiling (where no surface form expresses and internal never converges) — does not retract the narrowing. |
| D-S232-CLEAR-LOCALITY-1 | Qwen CLEAR is **expressed + entity-specific (spec 3/3) but NOT attribute-local (gen 3/15)**: the edit installs the target across surface forms AND leaves non-edited entities pristine, but **disrupts the edited subjects' own biographical attributes** (12/12 same-subject, large directional drift, bit-exact reversible). The CLEAR is "edit-expressed, off-target on the edited entity." |
| D-S232-V16-DISPOSITION-1 | v1.6 disposition = **finding-grade AND qualified** (both earned). Finding-grade: edit demonstrably expresses (5/5 stable, 2/3 surface forms, spec-clean, bit-exact reversible) — Qwen genuinely breaks the Llama-lineage ceiling, strengthening the narrowing. Qualified: the expressed edit is not attribute-local. Headline: *"Qwen breaks the consistency ceiling — the edit expresses where Llama-lineage cannot — but the expressed edit is entity-local-not-attribute-local."* Sharper than either pole of the kickoff binary. |
| D-S232-MISTRAL-1 | Mistral weights absent from NV at entry; re-pulled at Arm-2 boundary (~14.5 GiB, ungated, safetensors-only via `allow_patterns`); SHA recovered from `architecture_profile/reproducibility_manifest.json` S2.29 entry → byte-identical re-confirm. |
| D-S232-MISTRAL-PADTOKEN-1 | Pad-Token patch (pad=eos, id 2) required for Mistral, applied at Arm-2 dispatch; omitted in first attempt (Qwen-no-op masked the dependency), corrected. Matches S2.29 convention; pad_token affects only batch padding, never edit math → re-confirm remains byte-identical. |
| D-S232-MISTRAL-RECONFIRM-1 | Mistral holds 0/5 through the patched engine; closes the patch-confound thread (holds side); within-engine Qwen-clears/Mistral-holds contrast established. Resolves t_branch v1.4 §4'''' Axis 4. |
| D-S232-DEFER-1 | Operator defers routing/execution calls to Claude recommendation persistently forward (restates standing directive); load-bearing/irreversible ops surfaced for the record; no blocking. |
| D-S232-ROUTE-C-1 | Cell 13 routed **Route C (3-trial)** not Route B (15-trial): deterministic engine + far-from-band verdict → replicates confirm locality-pattern STABILITY only, not a borderline aggregate. Empirically vindicated (§4.6 stable ×4). |

---

## §7. Constraints (C-S232-*)

| ID | Statement |
|---|---|
| C-S232-1 | `cpu_solve_patch.diff` is `diff -c` normal format — apply with `patch -p0`, NOT `git apply` (which fails `error: unrecognized input`). Carry-forward for any future re-application. |
| C-S232-2 | Pad-Token patch (pad=eos) is REQUIRED for any model whose tokenizer ships `pad_token=None` (Mistral, Llama base). It is a no-op on models where a special token doubles as pad (Qwen `<|endoftext|>`). MEMIT `compute_z` calls `tok(padding=True)` → hard ValueError without it. |
| C-S232-3 | Engine pristine-restore at session close is the discipline (Run-B convention); however S2.32 leaves the engine PATCHED for S2.33 continuity (see §8). Pristine backup `memit_main.py.upstream_pristine_s232` is the restore point. |

---

## §8. Interface Contracts

| ID | Disposition at S2.32 |
|---|---|
| IC-S23-4 | Copy-Unmount HARD gate — VALIDATED on Qwen L4-8 (drift 0.00e+00 ×4 trials). **7th config, 2nd non-Llama base.** Edit-attribution corollary: collateral biographical drift reverses bit-exact. |
| IC-S24-4 | Trial protocol — Route C (1 dispatch + 3 replicates = 4 trials); sufficient given proven determinism + far-from-band verdict. |
| D-S215D2-VERDICT-INTEGRITY-1 | {cfb-v3-001/002/005} all STRICT on Qwen; the load-bearing read (consistency + locality) is at full single-token fidelity. |

---

## §9. Infrastructure Notes (carry-forward for S2.33)

1. **`globals.yml` cwd dependency (CONFIG_LAYER):** `util/globals.py` opens `"globals.yml"` relative-path → `os.chdir(ENGINE_ROOT)` required before `from memit import …` in any fresh kernel. STATS_DIR in globals.yml already = `/workspace/covariance_caches` (no reconcile needed).
2. **Hparams: load JSON + diff, do not hand-build.** `HyperParams.from_json` does `cls(**data)`; the canonical `Llama-3.1-8B.json` carries a stale `layers:[2,3,4,5,6]` — always override band to [4,5,6,7,8] and assert the bound (C-S230-4). Print the INHERIT/OVERRIDE diff for an auditable single-variable record.
3. **Two model objects, sequential.** Two 7B fp16 models do not co-reside in 24 GiB alongside an edit. Drop Qwen (`del model; empty_cache; gc.collect`) before loading Mistral.
4. **Manifest divergence (HYGIENE):** `/workspace/reproducibility_manifest.json` (1 entry post-S2.32) and `/workspace/architecture_profile/reproducibility_manifest.json` (full history incl. S2.29) have diverged. S2.32 entry written to the former; **mirror to the latter next session** and reconcile to a single canonical manifest.
5. **Prune candidate:** Mistral `consolidated.safetensors` (~7 GiB symlinked blob) is redundant with the sharded weights `from_pretrained` uses; prunable, non-urgent.
6. **`grep -c "_cov_cpu"` returns 3** when patch is live (3 operand lines), not 1 — correct live-patch marker.

---

## §10. S2.33 Entry Preconditions (architecture-geometry frontier, deepening)

Both S2.32 arms resolved. The CLEAR is now finding-grade-and-qualified; the lineage boundary is within-engine confirmed. The live frontier is the **mechanism** of the lineage divergence and the **breadth** of the boundary.

**Read order for S2.33:** this summary → `framework_finding v1.6 §2-§3` (the qualified CLEAR + entity-locality mechanism) → `t_branch v1.4 §4''''` (the four candidate axes; Axis 1 + 4 now closed) → `memit-patches-canonical v2.6` (P-VRAM-CPU-SOLVE codified) → cfb-v3 + probe-set-v3.

**Candidate S2.33 directions (Claude-recommended priority):**

| Priority | Direction | What it adjudicates | Cost |
|---|---|---|---|
| 1 | **Llama-vs-Qwen internal-stage geometry probe** (t_branch v1.4 Axis 2) — per-layer z-convergence at matched layers | WHERE in the optimization the lineage divergence originates (D-S231-MECH-1); now also: why Qwen's *expressed* edit damages neighboring attributes | Low–med |
| 2 | **Second non-Llama-lineage family** (Phi / Gemma / NeoX-class) clear-or-hold (Axis 3) | Is the boundary precisely "Llama-2 lineage," or narrower? Determines the true class boundary | Med (new cov compute + port) |
| 3 | **Qwen attribute-locality deep-dive** — does the entity-perturbation shrink with single-layer scope, narrower band, or lower mom2_update_weight? | Whether the collateral damage is intrinsic to MEMIT-on-Qwen or a hparam-tunable artifact | Med (re-tunes the deferred OQ-S229-1) |

**Claude's recommendation:** S2.33 = **Direction 1 (internal-stage geometry probe)** — it is the deepest open mechanistic question and now carries a second sub-question (why does the expressed Qwen edit damage neighbors?), with Direction 2 (second non-Llama family) as the breadth follow-on. Direction 3 is the applied "can the collateral damage be tuned away" arm, valuable if the LLM-as-database write-layer viability question becomes foreground.

---

**S2.32 CLOSED 2026-06-15.** Qwen2.5-7B CLEAR hardened to **finding-grade-and-qualified**: edit expresses 5/5 (stable ×4, 2/3 surface forms) but is entity-local-not-attribute-local (gen 3/15 same-subject drift, spec 3/3 pristine, bit-exact reversible). Mistral re-confirms 0/5 through the patched engine — within-engine Llama-lineage-holds/Qwen-clears contrast established; patch-confound thread closed both sides. `framework_finding v1.6` + `memit-patches-canonical v2.6` author the disposition + patch codification. OQ-S231-CLEAR-ROBUSTNESS-1, OQ-S222-CALIBRATION-CRITERIA-MISMATCH-1, and t_branch v1.4 Axis 4 resolved.
