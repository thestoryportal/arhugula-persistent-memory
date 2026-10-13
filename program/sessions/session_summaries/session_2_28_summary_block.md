# Session 2.28 — Summary Block

**Session type:** Authoring (v1.3 framework_finding amendment + t_branch v1.2 amendment + cross-architecture-axis scoping). NOT execution — no pod.
**Predecessor:** S2.27 (T.1-β-BAND; `BAND-INVARIANT → CEILING-IS-CONFIG-INDEPENDENT`; Axis 9; CLOSED 2026-06-15)
**Closed:** 2026-06-15
**Deliverables (3, all FULLY AUTHORED, in `/mnt/user-data/outputs/`):**
- `framework_finding_memit_ceiling_archival-v1_3.md` — ADDITIVE; Axis 8 (scale 8B→3B) + AKD elimination + Axis 9 (band); v1.0/v1.1/v1.2 PERMANENT preserved verbatim
- `t_branch_decision_document_v1_2.md` — ADDITIVE; band-confound elimination + deeper-arm deprioritization + T.3 re-scope surfaced; v1.0/v1.1 PERMANENT preserved verbatim
- `cross_architecture_axis_scoping_note.md` — T.3 vs within-regime deeper arms; cost/value; explicit re-scope recommendation

---

## 1. What S2.28 produced

S2.28 brought the permanent archival lineage current with the empirical state at S2.27 and set the forward routing. Three authoring deliverables, all additive-only on PERMANENT artifacts.

**The core move:** the framework_finding archival in the KB (v1.2) predated the entire T.1 cross-scale + config-variation arc (S2.22 / S2.24 / S2.25 / S2.26 / S2.27). v1.3 absorbs that arc additively — Axis 8 (scale generalization), the AKD-confound elimination, and Axis 9 (band-invariance) — promoting the ceiling from "MEMIT-on-Llama-3.1-8B property under our config choices" to "**config-independent MEMIT-on-base-Llama property across scale and band**, 9 axes." v1.0/v1.1/v1.2 statements are preserved verbatim in §1 carry-forward.

**The forward move:** with the within-Llama config space exhausted of high-value escape hatches, the only remaining axis that can change the *class* of the finding is cross-architecture (T.3). Both amendment artifacts + the scoping note converge on the same recommendation: re-scope T.3 (Mistral-7B first) into WS1; deprioritize the within-regime deeper arms (per-layer sweep, sequential-vs-joint) as same-class 10th/11th axes.

---

## 2. The nine-axis ceiling as codified at v1.3

| Axis | Session | Variation | Result |
|---|---|---|---|
| 1–6 | S2.10 / S2.12-A / S2.13-C / S2.14-D / S2.15-D2 | hparam / corpus / target / v_lr / mediation-locus / layer-set (Llama-3.1-8B, MEMIT) | bounded ≤ 0.022 |
| 7 | S2.18 | write-engine swap (ROME, L17 + L2) | FAIL |
| **8** | **S2.24** | **model scale (8B→3B)** — first model-variation axis | **0/5** |
| **9** | **S2.27** | **layer band ([2–6]→[4–8])** — first config-variation axis | **0/5; delta ≈ 0** |

Confounds eliminated: A/B/C/D (v1.0); write-engine swap (v1.1); **AKD/key-collision (S2.26 — cfb-v3 measured high-AKD, 4.62 band)**; **layer-band placement (S2.27 — single-variable 0/5 on [4–8])**.

Off-axis (not in the count): GRACE 8B environmental VRAM ceiling (S2.20, v1.2); GRACE-3B discriminator-gate non-firing (S2.22, hparam-conditional).

---

## 3. Decisions made

- **D-S228-V13-RATIFY-1** (load-bearing): `framework_finding_memit_ceiling_archival v1.3` ratified — Axis 8 + AKD elimination + Axis 9 additively recorded; v1.0/v1.1/v1.2 integrity preserved verbatim. Ceiling = config-independent MEMIT-on-base-Llama across scale and band (9 axes).
- **D-S228-V12-TBRANCH-RATIFY-1** (load-bearing): `t_branch_decision_document v1.2` ratified — band confound ELIMINATED; within-Llama config space exhausted; frontier moves from write-engine to architecture.
- **D-S228-T3-RESCOPE-1** (load-bearing, OPERATOR-RATIFICATION-PENDING): recommend re-scoping T.3 (cross-architecture: Mistral-7B then Qwen-7B) INTO WS1 as the next hypothesis-class axis. This is a WS1 scope-boundary change — the one decision class genuinely reserved to the operator (it extends committed compute). Default-accepted call per standing directive is re-scope-in + Mistral-7B at S2.29; operator ratifies the scope change at S2.28 close. Alternative D (close WS1 at the 9-axis result) is recorded as a clean, defensible stopping point.
- **D-S228-DEEPER-ARM-DEPRI-1**: per-layer sweep + sequential-vs-joint dispatch DEPRIORITIZED as same-class 10th/11th axes; conditionally re-activated only by a surprising T.3 CLEAR.

---

## 4. Constraints / disciplines carried into the artifacts

- **Additive-only on PERMANENT artifacts.** v1.0 (and v1.1, v1.2 where applicable) statements preserved verbatim in §1 carry-forward of each amendment; deltas surfaced at `''`-suffixed sections (t_branch) / new numbered sections (framework_finding). No prior sentence edited; no prior decision reversed.
- **Scale-variant config idiom recorded (D-S227-HPARAM-IDIOM-1, framework_finding v1.3 §2.4).** "Load reference MEMIT JSON, override architecture-structural fields only" — carries forward as the T.3 cross-architecture port discipline (override `layers`, `v_loss_layer = n_layers−1`, `lm_head_module` per `tie_word_embeddings`, `*_module_tmp` paths).
- **Tied-embedding adaptation is the first dispatch-failure point (D-S227-LMHEAD-1, C-S227-3).** For any tied-embedding target, `lm_head_module` must point at the tied embedding parameter, verified by `named_parameters()` presence check before dispatch. Carried into the T.3 methodology lock (t_branch v1.2 §6''.2).

---

## 5. Open questions (deferred to S2.29+)

- **OQ-V12-T-BRANCH-1..5** (opened in t_branch v1.2 §8''.2): T.3 target/SHA pins; architecture-structural field set for Mistral/Qwen; reference band adoption; **does the internal-vs-external signature reproduce on a non-Llama architecture** (the class-changing read, OQ-V12-T-BRANCH-4); which Llama-vs-target difference carries a CLEAR if one occurs (conditional).
- **OQ-S225-BASE-INSTRUCT-1** — base-vs-instruct confound (open since S2.5a); orthogonal arm; deferred.
- **KnowEdit external-validity** — orthogonal benchmark-corpus arm; deferred.
- **GRACE non-canonical hparam exploration** — off the rank-1-in-weight axis count; weaker finding class; not scheduled.

---

## 6. Hypothesis-class ledger (post-S2.28)

- **Ceiling = config-independent MEMIT-on-base-Llama property:** **9-axis confirmed** across scale (8B→3B) and band ([2–6]/[4–8]).
- Layer-band placement: ELIM S2.27 (Axis 9). AKD/key-collision: ELIM S2.26. T.1 alt model (Llama scale): RESOLVED → generalizes 8B→3B (Axis 8). A/B/C/D: ELIM. T.2 ROME: ELIM S2.18 (Axis 7). T.2 GRACE: hparam-conditional elim S2.22.
- **T.3 alt arch (Mistral/Qwen):** OPEN — **SURFACED FOR RE-SCOPE into WS1** (D-S228-T3-RESCOPE-1); the only remaining axis that can change the finding's class (Llama-family-specific vs base-decoder-LM-general).
- **Within-regime deeper arms (per-layer sweep, sequential-vs-joint):** OPEN, DEPRIORITIZED; conditionally re-activated by a T.3 CLEAR.

---

## 7. Forward routing — S2.29 (conditional on S2.28-close scope ratification)

- **If operator ratifies T.3 re-scope (RECOMMENDED):** S2.29 = T.3 Mistral-7B MEMIT — cross-architecture port. Runbook authoring + execution, likely foldable into one session given the proven 3B port pattern. Single-variable architecture port; reference band (no re-sweep per Axis 9); Cell P1 AKD pre-flight on the new edit layer; internal-vs-external signature as the primary read; single confirmatory dispatch (Route-A discipline). Entry artifacts: framework_finding v1.3 + t_branch v1.2 + cfb-v3 + probe-set-v3 + memit-patches v2.5 + `t1_alt_model_3b_memit_runbook v0.1` (structural template) + EasyEdit Mistral reference config.
- **If operator prefers an orthogonal arm:** S2.29 = base-vs-instruct (cheapest; same architecture) OR KnowEdit external-validity. Both deferred-not-eliminated; neither class-changing.
- **If operator closes WS1 at the 9-axis result (alternative D):** the config-independent MEMIT-on-base-Llama ceiling is a defensible stopping point; routing moves to WS2 (orchestration path selection, GAP-4) / WS3 (implementation planning). Nothing in v1.3 / v1.2 depends on T.3 running.

---

## 8. Artifact integrity check (additive discipline verification)

| Artifact | Prior versions preserved | Delta surface | New axes / sections |
|---|---|---|---|
| framework_finding v1.3 | v1.0 + v1.1 + v1.2 verbatim in §1 carry-forward | §2 (Axis 8), §3 (AKD), §4 (Axis 9), §5 (9-axis characterization), §6 (forward) | Axes 8, 9; AKD elimination |
| t_branch v1.2 | v1.0 §1–§11 + v1.1 §1'–§11' verbatim | `''`-suffixed: §0''/§1''/§4''/§5''/§6''/§7''/§8''/§9''/§10''/§11'' | §6'' T.3 lock; §7'' deeper-arm depri |
| scoping note | n/a (new standalone) | n/a | T.3 re-scope recommendation |

No prior sentence edited; no prior decision reversed; PERMANENT v1.0 integrity preserved verbatim in both amendment artifacts.

---

## 9. Mirror-sync (operator, post-session)

Authoring session — deliverables are in `/mnt/user-data/outputs/` (download), not on the pod. Save to the durable archive tier:

```bash
# After downloading the three S2.28 deliverables from outputs:
mv ~/Downloads/framework_finding_memit_ceiling_archival-v1_3.md \
   ~/Downloads/t_branch_decision_document_v1_2.md \
   ~/Downloads/cross_architecture_axis_scoping_note.md \
   ~/Downloads/session_2_28_summary_block.md \
   /Volumes/memit/llm-database-poc-mirror/
```

No pod state changed this session (no edit dispatched, no caches touched). Pod SSH target unchanged from S2.27 (`103.196.86.67:16437`) if not cycled; pull current target from RunPod console if T.3 execution (S2.29) needs a warm pod.

---

*End S2.28 summary block.*
