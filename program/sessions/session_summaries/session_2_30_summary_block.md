# Session 2.30 Summary Block — T.3-β-QWEN (cross-architecture confirmation arm — runbook authoring)

**Session type:** Authoring (thin runbook authoring micro-pass; no pod-side execution this session — runbook DECLARATIVE, ready for execution)
**Date:** 2026-06-15
**Predecessor:** S2.29 (T.3-α-MISTRAL executed; ceiling promoted L→G; Axis 10; Qwen confirmation arm routed)
**Successor:** S2.31 (verdict-conditional — see §10)
**Verdict:** N/A (authoring session) — deliverable `t3_qwen_7b_memit_runbook v0.1` DECLARATIVE, READY FOR EXECUTION.

---

## §1. One-Line Result

Authored `t3_qwen_7b_memit_runbook v0.1` (1,017 lines) — the second cross-architecture arm, porting the proven T.3 scaffold from Mistral (S2.29) to `Qwen/Qwen2.5-7B` (base), the most architecturally distinct 7B base decoder family available. This is the **confirmation arm for G** (base-decoder-LM-general): a `0/5` signature reproduction on Qwen converts "ceiling generalizes from Llama to a Llama-lineage cousin (Mistral)" into "ceiling generalizes across architecturally distinct base decoder LM families" — the strongest obtainable form of G. Single-variable architecture port discipline preserved exactly (zero tuning-knob changes); the port is the **heaviest structural delta of any arm** (Qwen differs from the 8B/Mistral canonical on hidden size, intermediate size, layer count, vocab, pad convention, and tokenizer family).

---

## §2. Deliverables (RATIFIED 2026-06-15)

| Artifact | Lines | Status |
|---|---|---|
| `t3_qwen_7b_memit_runbook v0.1` | 1,017 | DECLARATIVE → READY FOR EXECUTION (full authoring, zero placeholders; all 23 cells specified end-to-end) |
| `session_2_30_summary_block.md` | — | this artifact |

**Not produced this session (deferred, verdict-conditional):**
- `framework_finding_memit_ceiling_archival v1.5` — ADDITIVE amendment; conditional on the S2.30-execution verdict (Axis 11 if `0/5`; class-narrowing if CLEAR). Authored at the NEXT session's close (execution session), not now.
- `t_branch_decision_document v1.4` — ADDITIVE; conditional on execution verdict.
- Qwen-resolved literals (token IDs, cov SHAs, VRAM peaks, Checkpoint #1 drift) — execution-resolved; the runbook specifies the resolution logic and gates, not the literals (the one place literals are necessarily execution-time is the Cell 6 tokenizer query).

---

## §3. Decisions (D-S230-*)

| ID | Statement |
|---|---|
| D-S230-Q1-1 | Runbook structural inheritance from `t3_mistral_7b_memit_runbook v0.1` with cross-architecture substitutions; corpus / probe-strings / trial protocol / acceptance bands held verbatim |
| D-S230-Q2-1 | Cell 5 PRODUCES Qwen Checkpoint #1 (fresh determinism chain; no prior baseline to consume) |
| D-S230-Q3-1 | Reference band `[4,5,6,7,8]` adopted from EasyEdit/CaKE Qwen2.5-7B critical-range (arXiv 2503.16356 §B.2); Axis-9-validated band non-load-bearing; Mistral-parity |
| D-S230-Q4-1 | Cell 8 fresh Qwen cov computation at `[4..8]`; ~50–80 min; ~5–5.5 GiB NV; largest per-layer cache of any arm (18944-wide mom2) |
| D-S230-MODEL-1 | Target = `Qwen/Qwen2.5-7B` (base, non-Instruct, Apache-2.0, `Qwen2ForCausalLM`) — the canonical non-tied 7B Qwen base and the EasyEdit/CaKE-supported Qwen editing target; the most architecturally distinct 7B base decoder family available |
| D-S230-LMHEAD-1 | `lm_head_module='lm_head'` (UNTIED; 8B/Mistral-canonical form, NOT the 3B tied override); verified untied at Cell 1.5. Note: the SMALLER Qwen2.5 variants (0.5/1.5/3B) are tied; the 7B base is untied — Cell 1.5 verifies empirically |
| D-S230-PADTOKEN-1 | Pad-Token RE-DERIVED to `<|endoftext|>=151643` per Qwen convention; the one patch with model-specific content; may be a verified no-op if the tokenizer revision ships it pre-set |
| D-S230-PATCH-INHERITANCE-1 | All MEMIT patches inherited; engine reused live-patched (SHA 80426fd9) if resident, else cloned; byte-identical to all ten prior axes; P-4's family-agnostic getattr-fallback is the structural enabler (triggers on absence of `n_embd`, true for Qwen2) |
| D-S230-TOKEN-RERESOLVE-1 | ALL probe + target token IDs re-resolved against the Qwen tokenizer; neither Llama nor Mistral allowlist inherited — Qwen allowlist built fresh; integrity-subset single-token preference enforced |
| D-S230-ENGINE-REUSE-1 | Engine reused live-patched from the Mistral arm if resident (stronger single-variable claim than a fresh clone, per D-S229-ENGINE-REUSE-1) |
| D-S230-BLOCKC-SKIP-1 | Route-A discipline (single confirmatory dispatch for a 0/5 surface) inherited; full 15-trial only on Route B/C |

---

## §4. Constraints (C-S230-*)

| ID | Statement |
|---|---|
| C-S230-1 | MEMIT engine SHA pinned at Cell 1 entry; documented in Cell 20 manifest |
| C-S230-2 | Engine source snapshot at `/workspace/architecture_profile/engine_source_snapshot/<engine-sha>/` (verify-or-create) |
| C-S230-3 | Cov-cache provenance: per-layer size + SHA-256 recorded for the Cell 18 integrity gate |
| C-S230-4 | Layer-set bound assertion: all of `[4..8]` within `0 ≤ idx < 28` |
| C-S230-5 | Per-cell explicit Surface annotation (A vs B) |
| C-S230-LMHEAD-1 | `lm_head.weight` PRESENT (untied) verified via `named_parameters()` before `lm_head_module='lm_head'` set |
| C-S230-PADTOKEN-1 | `pad_token_id == 151643` asserted at Cell 2 |
| C-S230-MODULE-1 | All four MEMIT module-path templates resolve to real named modules on `Qwen2ForCausalLM`, AND `down_proj` shape `[3584,18944]`, asserted at Cell 1.5 |
| C-S230-HFHOME-1 | `HF_HOME=/workspace/hf_cache` set BEFORE any HF import (carried hard from C-S229-HFHOME-1) — container-disk OOM otherwise |

---

## §5. Open Questions

### §5.1 Anticipated to resolve at S2.30 execution

| ID | Resolution at |
|---|---|
| OQ-V13-T-BRANCH-1 | Cell 1 — Qwen2.5-7B base, HF revision SHA pinned; Apache-2.0 ungated confirmed |
| OQ-V13-T-BRANCH-2 | Cell 1.5 — structural field set via `named_parameters()` (untied lm_head; down_proj [3584,18944]; n_layers=28 → v_loss_layer=27; module paths verified) |
| OQ-V13-T-BRANCH-3 | **THE G-confirmation question — Cell 9/10/13 first dispatch: does the signature reproduce on a non-Llama-LINEAGE family?** |
| OQ-S230-QWEN-FRAG-1 | Cell 6 — Qwen target tokenization re-classification; how many of {001/002/005} are STRICT on Qwen's 152k vocab (plausibly all three — cleaner than Mistral, where 005 fragmented) |
| OQ-S230-QWEN-TOP1-1 | Cell 5 — Qwen natural top-1 at the canonical prompt (same function-word class as Llama/Mistral, or different) |
| OQ-S230-COV-TIME-1 | Cell 8 — per-layer cov wall-time (~10–16 min/layer; 18944-wide dim pushes above Mistral) |
| OQ-S230-VRAM-1 | Cell 9/15 — joint-overlay peak VRAM (~20–22 GiB; TIGHTEST headroom of any arm) |

### §5.2 Carried forward

| ID | Status |
|---|---|
| OQ-S229-1 | `mom2_update_weight=15000` calibration on Qwen — PROVISIONAL inheritance; re-tuning out of scope (deeper arm) |
| OQ-S225-BASE-INSTRUCT-1 | Instruct-vs-base generalization — open; external-validity frontier post-Qwen |
| OQ-S222-CALIBRATION-CRITERIA-MISMATCH-1 | Reconcile runbook vs probe-set-v3 §126 generalization predicate before Cell 10/13 verdict |

---

## §6. Interface Contracts

| ID | Disposition at S2.30 |
|---|---|
| IC-S23-4 | Copy-Unmount HARD gate — APPLICABLE at Cell 11/15; **7th config, second non-Llama** if drift 0.00e+00 |
| IC-S24-4 | Trial protocol — Route-conditional (Route-A single confirmatory default per 0/5 discipline) |
| D-S215D2-VERDICT-INTEGRITY-1 | {cfb-v3-001/002/005} — re-confirm STRICT class on Qwen tokenizer at Cell 6; 001+002 carried the Mistral load-bearing read, expected STRICT on Qwen |

---

## §7. The Qwen Port — Why It Is the Near-Decisive Confirmation (load-bearing rationale)

The Mistral arm (S2.29) confirmed G but left one residual skeptic's objection open: Mistral shares Llama-2's architectural lineage (RMSNorm + RoPE + gated MLP + GQA decoder block), so Axis 10 could be read as "generalizes within the Llama-lineage decoder shape." Qwen closes that objection. The four-way architecture table (runbook §2.1) shows Qwen differs from the 8B/Mistral canonical on **every structural axis except untied-embeddings and the GQA family**:

```
                  8B canon    Mistral     Qwen2.5-7B
  hidden_size     4096        4096        3584    ← distinct
  intermediate    14336       14336       18944   ← distinct, LARGEST
  n_layers        32          32          28      ← distinct
  down_proj       [4096,      [4096,      [3584,   ← NEW shape
                   14336]      14336]      18944]
  vocab           128256      32768       152064  ← distinct, LARGEST
  tokenizer       Llama BPE   SP 32k      Qwen BPE ← distinct family
  pad             128001      2(eos)      151643   ← distinct
  attention       GQA         GQA         GQA+QKV-bias ← Qwen-distinctive
```

A `0/5` on Qwen cannot be attributed to shared Llama-lineage architecture shape. That is what makes it near-decisive for G. The port is correspondingly the **heaviest of any arm** (more structural overrides than Mistral, which only changed tokenizer + pad), yet the single-variable discipline is preserved exactly: **zero tuning-knob changes**; only architecture-forced structural fields and the tokenizer re-resolution differ from the config that produced all ten prior axes.

---

## §8. Infrastructure Notes (reusable for S2.30 execution + S2.31)

1. **HF_HOME on NV is the hard Cell-0 prerequisite (C-S230-HFHOME-1).** Carried verbatim from the S2.29 lesson — set `HF_HOME=/workspace/hf_cache` + `HF_HUB_CACHE` BEFORE any HF import; the 20 GiB container disk fills on a single 7B pull.
2. **Qwen is ungated (Apache-2.0).** The Qwen2.5-7B *base* is Apache-2.0 — no license acceptance, like Mistral, unlike Llama. (Caveat: the 3B and some Instruct variants carry the Qwen license; the 7B base does not. Confirm at the pinned revision.)
3. **No `sentencepiece` dependency.** Unlike Mistral, Qwen's tokenizer is BPE/tiktoken-style and is provided by `transformers>=4.37` via `tokenizers`. Cell 0 dep list drops `sentencepiece`; pin `transformers>=4.37` (Qwen2 architecture registration).
4. **Tightest VRAM headroom of any arm.** Projected ~20–22 GiB peak (above Mistral's ~19–21) — the 18944-wide `intermediate_size` inflates both the cov-compute mom2 workspace and the edit-time activations. The S2.29 stale-kernel reclaim step is mandatory pre-load; OOM is most likely at Cell 9 edit dispatch. Mitigation: single-layer scope (L5 — the CaKE/EasyEdit Qwen ROME site), then fp16 cov relaxation.
5. **Largest cov caches of any arm.** ~1.0–1.1 GiB/layer (18944 × float32 mom2); ~5–5.5 GiB total for L4-L8. Architecture-keyed; Llama/Mistral caches inapplicable.
6. **Engine reuse.** The live-patched engine (SHA 80426fd9) from the Mistral arm ports directly if resident; Qwen needs only the Cell-1.5 module introspection + Pad-Token re-derivation, no new engine work (D-S230-ENGINE-REUSE-1).
7. **`down_proj` shape [3584, 18944] is NEW.** Highest-risk port check (Cell 1.5) — verify the shape, not just the path string; a wrong-variant pull (e.g. an Instruct or VL model) would surface here.

---

## §9. Operator-Guidance Register (carried verbatim for S2.30 execution, per S2.24 §9 / S2.29 §9)

Zero-ML-background register, one cell at a time, label Surface A (pod) / Surface B (notebook), explain WHAT/WHY + expected healthy output before each cell, frame a null result (`0/5` with signature) as signal. Claude makes all calls and proceeds; surfaces only irreversible ops (model pull, cov compute, NV-destructive ops) for confirmation. This register held through S2.29 and carries forward verbatim.

---

## §10. S2.31 Entry Preconditions (verdict-conditional)

**S2.30 is an authoring session.** The runbook is DECLARATIVE and ready for pod-side execution. The immediate next session executes it. The post-execution routing:

**Read order for the execution session:** this summary → `t3_qwen_7b_memit_runbook v0.1` (the runbook itself, cell-by-cell) → `framework_finding v1.4 §2.4` (cross-architecture idiom) + `§4` (Qwen routing) → `t_branch v1.3 §6'''` (methodology lock) → cfb-v3 + probe-set-v3 (held verbatim) → `session_2_29_summary_block §8` (infrastructure lessons).

**Derive at execution entry (already specified in the runbook, resolved at the pod):** Qwen HF revision SHA + Apache-2.0 confirm; `tie_word_embeddings` check (expect untied → `lm_head`); module-path verification via `named_parameters()` + `down_proj` shape `[3584,18944]`; fresh cov caches; fresh determinism chain (Checkpoint #1 on Qwen); probe token IDs re-resolved against the Qwen tokenizer (re-classify STRICT/PROXY; prefer single-token for the integrity subset).

**Decision matrix at execution close:**

| Verdict | Meaning | framework_finding | t_branch | S2.31 |
|---|---|---|---|---|
| `0/5` + signature reproduced | Ceiling holds on the most architecturally distinct base decoder LM → **G near-decisive** (Llama + Mistral + Qwen) | v1.5 ADDITIVE (Axis 11) | v1.4 ADDITIVE (G confirmed) | external-validity frontier: Instruct-vs-base (OQ-S225-BASE-INSTRUCT-1) and/or KnowEdit benchmark corpus — neither class-changing |
| CLEAR (≥3/5 PASS) | Qwen edits where Llama×3 + Mistral failed → **G NARROWS to Llama-lineage** | v1.5 ADDITIVE (class-narrowing) | v1.4 ADDITIVE (G narrowed) | within-regime per-layer sweep RE-ACTIVATED as the "what's different between Llama-lineage and Qwen" probe; architecture-geometry question re-opens |
| FAIL-at-environment (OOM) | NOT a scientific verdict (tightest headroom of any arm) | no amendment | no amendment | triage + re-attempt with mitigation (single-layer L5 scope; fp16 cov relaxation; gradient-checkpointed dispatch) |

**Most-likely path (low-confidence prior, ten axes + Mistral confirmation):** `0/5` + signature reproduced → G near-decisive → the cross-architecture frontier closes for class-change → external-validity arms become the frontier.

---

**S2.30 CLOSED 2026-06-15.** `t3_qwen_7b_memit_runbook v0.1` authored DECLARATIVE (1,017 lines, zero placeholders); second cross-architecture arm (confirmation, not class-change); most architecturally distinct port of any arm; ready for pod-side execution. Verdict-conditional routing to S2.31 specified.
