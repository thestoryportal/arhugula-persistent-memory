# T-Branch Decision Document — T.3 Cross-Architecture EXECUTED (Mistral-7B); Ceiling Promoted L→G; Qwen Confirmation Arm ROUTED (v1.3 amendment of v1.2 of v1.1 of v1.0)

> **Status:** RATIFIED v1.3 — load-bearing; additive amendment; v1.0 + v1.1 + v1.2 PERMANENT integrity preserved (decision-record class)
>
> **Predecessor (v1.3):** S2.29 — T.3-α-MISTRAL executed (cross-architecture MEMIT port)
> **Successor (v1.3):** S2.30 — T.3-β-QWEN confirmation arm
> **Workstream:** WS1 (empirical execution; T.2 ROME closed; T.2 GRACE hparam-conditional; T.1 cross-scale RESOLVED; T.1-α/β config arc RESOLVED; **T.3 cross-architecture EXECUTED — first instance (Mistral) confirms G**)

---

## §0''' — v1.3 amendment scope and integrity declaration

### §0'''.1 v1.3 amendment scope

v1.3 records the empirical disposition of the v1.2 forward-conditional decision and surfaces deltas at the corresponding `'''`-suffixed section numbers:

1. **§1''' decision statement updated** for the post-S2.29 routing state: the v1.2 §1'' "live frontier: T.3 (the only remaining axis that can change the *class* of the finding)" is RESOLVED. T.3-α-MISTRAL executed at S2.29; the ceiling reproduced (`0/5`, signature) on a non-Llama base decoder LM; the finding is promoted from **config-independent MEMIT-on-base-Llama (L)** to **config-independent MEMIT-class-on-base-decoder-LM (G)**. The class change v1.2 anticipated has occurred in the G direction.
2. **§4''' candidate-axis selection updated**: the T.3-Mistral arm is CLOSED (executed); the T.3-Qwen arm is promoted from "second arm, surfaced" to "routed confirmation arm." The within-Llama config space remains exhausted; the cross-architecture frontier now has one confirmed instance and one routed confirmation.
3. **§5''' conditional execution plan resolved**: the v1.2 §5'' "re-scope T.3 → S2.29 = T.3 Mistral-7B MEMIT" branch was taken; the Mistral result routes (per the Cell-13 / kickoff decision matrix) to the Qwen confirmation arm, NOT to the within-regime per-layer sweep (which re-activates only on a CLEAR — which did not occur).
4. **§6''' methodology lock for T.3-β** (Qwen): the cross-architecture inheritance scope, now proven on Mistral, carries forward to Qwen with the same locked/derive split.
5. **§8''' open questions** — closes OQ-V12-T-BRANCH-1..4 per the S2.29 dispositions; opens the Qwen-arm OQs.

The v1.3 amendment **preserves all v1.0 §1–§11, v1.1 §1'–§11', and v1.2 §0''–§8'' content verbatim** as load-bearing PERMANENT decision-record. v1.3 surfaces deltas at corresponding section numbers with the suffix `'''`.

### §0'''.2 v1.0 + v1.1 + v1.2 integrity preservation

v1.0 (seven-axis ceiling decision record), v1.1 (ROME elimination + GRACE promotion), and v1.2 (band confound eliminated; within-regime deprioritized; T.3 surfaced + methodology lock) are preserved verbatim. v1.3 is additive-only.

---

## §1''' — Decision statement amendment (extends v1.0 §1, v1.1 §1', v1.2 §1'')

The v1.2 §1'' frontier statement read: *"Live frontier: T.3 (alt architecture, Mistral-7B / Qwen-7B) — the only remaining axis that can change the class of the finding."* v1.3 resolves it:

> **T.3-α executed (S2.29). Ceiling promoted L → G.** MEMIT at canonical hparams on `mistralai/Mistral-7B-v0.3` (base) produced `0/5` consistency on cfb-v3 with the identical internal-vs-external signature (internal gain 240–4000× per fact; external P_max 3.50e-3; top-1 unmoved on all 5; bit-exact unmount ×2; confirmatory trial bit-identical to trial 0). The architectural-invariant ceiling is **not Llama-family-specific** — it reproduces on a non-Llama base decoder LM at canonical hparams with **zero tuning-knob changes** (single-variable architecture port; 3 structural overrides only). This is **Axis 10**, the first architecture-family-variation axis.
>
> **The finding's strongest form is now:** a config-independent, architecture-family-independent **MEMIT-class (rank-1-in-weight) ceiling on base decoder LMs at canonical hparams**, of which {Llama-3B, Llama-8B, Mistral-7B} are confirmed instances and ROME is a confirmed second engine in the class.
>
> **New live frontier: confirmation, not class-change.** The only forward move that could still *narrow* G is a non-Llama-lineage family clearing the band; the Qwen-7B arm tests exactly that (Qwen is the most architecturally distinct 7B decoder family available). T.3-β-QWEN is routed as the confirmation arm (S2.30).

**v1.2 forward-conditional disposition resolved.** v1.2 §5'' declared "re-scope T.3 in → S2.29 = T.3 Mistral-7B MEMIT (cross-architecture; new class)." v1.3 records: the branch was taken; T.3-α executed and returned the G outcome; the chain routes to T.3-β-QWEN confirmation.

---

## §4''' — Candidate-axis selection amendment (extends v1.0 §4, v1.1 §4', v1.2 §4'')

### §4'''.1 Post-S2.29 axis-candidate disposition matrix

| Axis | Class | Disposition at v1.3 | Cost | Note |
|---|---|---|---|---|
| T.3 Mistral-7B MEMIT | cross-architecture (NEW class) | **CLOSED — EXECUTED S2.29; 0/5; G confirmed (Axis 10)** | done | First cross-architecture-family instance; ceiling reproduced |
| T.3 Qwen-7B MEMIT | cross-architecture (confirmation) | **ROUTED — S2.30 (leading)** | ~1 session | Most distinct 7B decoder family; near-decisive for G; reuses T.3 scaffold proven on Mistral |
| Instruct-vs-base | orthogonal generalization | OPEN (deferred) | ~1 session | OQ-S225-BASE-INSTRUCT-1; does not change class |
| KnowEdit external-validity | external validity | OPEN (deferred) | moderate | Benchmark-corpus edit; does not change class |
| Within-regime per-layer sweep | within-Llama deeper arm | DEPRIORITIZED (NOT re-activated) | high | Re-activates only on a cross-arch CLEAR; Mistral did NOT clear → stays deprioritized |

### §4'''.2 Why Qwen is the routed confirmation (v1.3)

1. **Mistral shares Llama-2's architectural lineage.** A skeptic could read Axis 10 as "generalizes within the Llama-lineage decoder shape (RMSNorm + RoPE + gated MLP)." Qwen is the most architecturally distinct 7B base decoder family available (different normalization/attention details, different tokenizer lineage). A Qwen `0/5` converts "Llama-lineage" into "architecturally-distinct base decoder LM families" — the strongest obtainable form of G.
2. **The port pattern is proven.** S2.29 validated the cross-architecture config idiom end-to-end (load 8B JSON, structural overrides, 0 tuning changes, re-resolve tokenizer). Qwen reuses the scaffold; the only re-derivations are Qwen's structural fields, tokenizer, and pad convention. Cheapest near-decisive move per unit compute.
3. **Either Qwen outcome is decision-relevant.** `0/5` → G near-decisive → external-validity arms become the frontier. CLEAR (low prior) → G narrows to Llama-lineage → architecture-geometry question re-opens and the within-regime sweep conditionally re-activates.

---

## §5''' — Conditional execution plan resolution (extends v1.0 §5, v1.1 §5', v1.2 §5'')

```
v1.2 forward fork → v1.3 resolution
═══════════════════════════════════════════════════════════════════
  S2.28 close: operator re-scoped T.3 into WS1 (D-S228-T3-RESCOPE-1)
        │
        ▼
  S2.29 = T.3-α-MISTRAL  [EXECUTED]
        │
        ├── 0/5 + signature reproduced  ◄── ACTUAL OUTCOME
        │     → ceiling is base-decoder-LM-general (G)
        │     → S2.30 = T.3-β-QWEN confirmation arm  ◄── ROUTED
        │           │
        │           ├── 0/5 → G near-decisive → external-validity frontier
        │           │         (Instruct, KnowEdit)
        │           └── CLEAR → G narrows to Llama-lineage
        │                     → within-regime sweep re-activates
        │
        └── [COUNTERFACTUAL, did not occur] Mistral CLEARS
              → ceiling Llama-family-specific (L)
              → within-regime per-layer sweep re-activates as
                "what's different between architectures" probe
═══════════════════════════════════════════════════════════════════
```

**Disposition.** The Mistral `0/5` took the upper branch. The within-regime per-layer sweep (v1.2 §7'') is NOT re-activated — it re-activates only on a CLEAR, which did not occur. Qwen confirmation is the scheduled forward move.

---

## §6''' — Methodology lock for T.3-β (Qwen) (extends v1.2 §6'')

### §6'''.1 Locked from carry-forward (unchanged from v1.2 §6''.1; proven on Mistral)

cfb-v3 corpus, probe-set-v3, trial protocol IC-S24-4, acceptance bands (0.5 / 0.05 / 0.05 / 1e-4), verdict-integrity subset {001/002/005}, internal-vs-external signature as the primary diagnostic, Block-and-Cell runbook structure. The Mistral execution confirmed all of these port cleanly across architecture.

### §6'''.2 Re-derived at T.3-β (Qwen) entry

| Surface | Mistral disposition (proven) | Qwen re-derivation |
|---|---|---|
| HF revision SHA + license | caa1feb0; ungated Apache-2.0 | Qwen SHA pin; verify gating (likely ungated) |
| `tie_word_embeddings` → lm_head_module | False → `lm_head` (untied) | check Qwen tie flag; derive lm_head_module |
| `n_layers` → `v_loss_layer` | 32 → 31 | Qwen n_layers − 1 |
| module-path templates | `model.layers.{}.mlp.down_proj` verified | verify via `named_parameters()` (C-S227-3) |
| reference MEMIT band | `[4..8]` (EasyEdit; Axis-9 equiv) | EasyEdit Qwen config band |
| pad-token convention | re-derived eos=2 | derive Qwen pad convention |
| tokenizer | SentencePiece 32768; all IDs re-resolved | re-resolve against Qwen tokenizer; re-classify STRICT/PROXY (prefer single-token for integrity subset, OQ-S230-QWEN-FRAG-1) |
| cov caches | fresh (architecture-keyed) | fresh Qwen cov compute |
| determinism chain | Checkpoint #1 on Mistral, 0.00e+00 | fresh Checkpoint #1 on Qwen |
| HF_HOME on NV | C-S229-HFHOME-1 (hard Cell-0 prereq) | inherit — set BEFORE first HF import |

### §6'''.3 Empirical anchors carry-forward (unchanged; extended by Mistral)

Internal-vs-external signature remains the PRIMARY read. Copy-Unmount now validated on 6 configs (Mistral L4-L8 = first non-Llama; drift 0.00e+00). Cross-session bit-exact determinism extended to a fresh Mistral chain. The cross-architecture config idiom (D-S229-HPARAM-IDIOM-2) is the reusable port primitive for Qwen.

---

## §8''' — Open questions amendment (extends v1.0 §8, v1.1 §8', v1.2 §8'')

### §8'''.1 v1.2 OQs closed by S2.29

| OQ | Disposition |
|---|---|
| OQ-V12-T-BRANCH-1 | CLOSED — Mistral-7B-v0.3 base, revision caa1feb0 pinned |
| OQ-V12-T-BRANCH-2 | CLOSED — Mistral structural field set derived via `named_parameters()` (untied lm_head; v_loss_layer=31; module paths verified) |
| OQ-V12-T-BRANCH-3 | CLOSED — `[4..8]` reference band adopted (no re-sweep) |
| OQ-V12-T-BRANCH-4 | **CLOSED — THE class-changing read: signature reproduced on Mistral → G** |
| OQ-V12-T-BRANCH-5 | INAPPLICABLE — cross-arch CLEAR follow-ups (no CLEAR occurred) |
| OQ-V12-T-BRANCH-6 | PARTIALLY CLOSED — MEMIT-vs-ROME-vs-GRACE comparison now has the cross-architecture data point; full closure at G-confirmation (Qwen) |

### §8'''.2 v1.3 OQs activated / opened

| OQ | Statement | Status |
|---|---|---|
| OQ-V13-T-BRANCH-1 | Qwen-7B target + HF revision SHA pin | OPEN — resolved at S2.30 entry |
| OQ-V13-T-BRANCH-2 | Qwen architecture-structural field set (tie flag, n_layers, module paths) | OPEN — resolved via `named_parameters()` at S2.30 |
| OQ-V13-T-BRANCH-3 | Does the signature reproduce on a non-Llama-LINEAGE family (Qwen)? (G-confirmation read) | OPEN — resolved at S2.30 first dispatch |
| OQ-S230-QWEN-FRAG-1 | Qwen target tokenization re-classification; prefer single-token targets for integrity subset | OPEN — resolved at S2.30 Cell 6 |
| OQ-S229-1 | `mom2_update_weight` re-tuning at Mistral scale | OPEN, OUT-OF-SCOPE (single-variable port; deeper arm only) |

---

**v1.3 status:** RATIFIED S2.29 close 2026-06-15. v1.0 + v1.1 + v1.2 PERMANENT preserved verbatim. T.3-α-MISTRAL executed; ceiling promoted L→G (Axis 10); T.3-β-QWEN confirmation arm routed (S2.30). Within-regime per-layer sweep stays deprioritized (no CLEAR occurred).

*End of t_branch_decision_document v1.3.*
