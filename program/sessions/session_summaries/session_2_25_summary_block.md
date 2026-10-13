# Session 2.25 — Summary Block

**Session type:** Authoring (T.1-α-MEMIT-AKD runbook + paired corpus + paired probe set)
**Predecessor:** S2.24 (T.1-α-MEMIT execution; `FAIL_WITH_INSTALLATION`; ceiling generalizes 8B→3B under low-AKD caveat)
**Closed:** 2026-06-15
**Deliverables (3, all FULLY AUTHORED, in `/mnt/user-data/outputs/`):**
- `t1_alt_model_3b_memit_akd_runbook_v0_1.md` — DECLARATIVE, ready for S2.26 execution
- `cfb-v4-highAKD.yaml` v1.0 — high-AKD matched-pair corpus (subjects + templates locked)
- `probe-set-v4-highAKD.yaml` v1.0 — 38 probes, roster-integrity validated

---

## 1. What S2.25 produced — the discriminating experiment for OQ-S224-LIT-1

S2.24 closed with the highest-value open thread in the workstream: the 0/5 ceiling was obtained on **cfb-v3, a low-AKD corpus by design** (5 clustered athletes, 1 identical template), so it could not disentangle a **model-family ceiling** from a **low-AKD-corpus ceiling**. S2.25 authored the experiment that separates them.

The design is a **single-variable matched-pair contrast**: cfb-v3 (LOW AKD) vs a new hand-authored **cfb-v4 (HIGH AKD)**, holding everything constant except the separation of the MEMIT keys (subject-last-token activations at the edit layer). If cfb-v4 clears the band where cfb-v3 failed 0/5 → the ceiling is the corpus, not the model, and the LLM-as-database thesis gets a forward path ("use well-separated keys"). If cfb-v4 also fails → the ceiling is deeper than AKD.

---

## 2. Decisions made (all four pre-session decisions ratified; standing directive now governs)

- **D-S225-Q1-1:** Corpus source = **hand-authored cfb-v4** (NOT KnowEdit). Clean single-variable contrast; KnowEdit deferred to S2.27 as external-validity confirmation. Rationale: KnowEdit would change subjects, templates, domains, target structure, probe set, and allowlist chain simultaneously — confounded. Hand-authored holds targets/structure fixed and varies only key separation.
- **D-S225-Q2-1:** AKD instrumentation added as **Cell P1 pre-flight HARD gate** on BOTH corpora. Computes mean pairwise Euclidean key distance at L2-L6; halts if cfb-v4 is not actually high-AKD (corpus-authorship failure caught before any wasted edit).
- **D-S225-Q3-1:** Base-vs-instruct control **DEFERRED** (OQ-S225-BASE-INSTRUCT-1). S2.26 runs base-only, single-variable on AKD.
- **D-S225-Q4-1:** EasyEdit hparam diff added as **Cell P0 desk-check** (no model load). Rules out the alternative that the inherited [2-6] band is simply mis-set for Llama before attributing any result to AKD.
- **D-S225-Q5-1:** Fact count = **5** (matched pair); **targets held byte-identical** to cfb-v3 (guitar/piano/violin/harp/flute, incl. the harp first-token-proxy). Only keys vary.
- **D-S225-REUSE-1:** Engine + 5 cov caches + 3B adaptations **REUSED live** from S2.24 NV state. No re-clone, no recompute (~45 min saved). Caches are model-keyed (wikipedia_stats), not corpus-keyed (C-S224-4), so they serve both corpora at L2-L6.
- **D-S225-CTRL-1:** cfb-v3 runs as an **in-session confirmatory control** (single dispatch, no replicates, per D-S224-BLOCKC-SKIP-1 rationale); Block C replicates scoped to cfb-v4 only.
- **D-S225-FULL-AUTHORING-1:** Per the new standing directive (no operator editing), cfb-v4 subjects/templates were **fully authored**, not left as placeholders, and the paired probe set was authored in full. No pre-session operator obligations remain.

---

## 3. The high-AKD corpus — subjects and rationale (LOCKED)

Five subjects from five maximally-distinct pretraining domains, each on a distinct template, all driving identical instrument targets:

| fact | subject | domain / entity type | template (distinct) | target |
|------|---------|---------------------|---------------------|--------|
| cfb-v4-001 | Werner Heisenberg | physics / person | "The signature instrument associated with {} is the" | guitar |
| cfb-v4-002 | Heinrich Schenker | music-theory / person (non-performer) | "If {} were a musical instrument, it would be the" | piano |
| cfb-v4-003 | the Danube | geography / river (non-person) | "The instrument that best evokes {} is the" | violin |
| cfb-v4-004 | the Python programming language | technology / abstract artifact | "Rendered as a member of an orchestra, {} would play the" | harp (multi-token) |
| cfb-v4-005 | Mount Kilimanjaro | geography / peak (non-person) — SENTINEL | "The instrument whose character most resembles {} is the" | flute |

**Selection discipline applied:** (1) five different domains for maximal key spread; (2) zero musical association on every subject (no instrument leakage into target_true — same trap cfb-v3 avoided); (3) mix of entity TYPES (2 persons, river, programming language, mountain) widens spread beyond what 5 people could; (4) 5 distinct syntactic frames as a second separation lever. Built-in `akd_self_audit` flags the two nearest-pair collapse risks (river↔mountain both geographic; physicist↔theorist both human names) for Cell P1 per-pair reporting.

---

## 4. The runbook — structure and deltas from S2.24

Inherits `t1_alt_model_3b_memit_runbook v0.1` (the S2.24 3B-MEMIT runbook) verbatim, with:
- **NEW Block PRE** (Cells P0–P1): EasyEdit hparam diff + AKD-compute HARD gate. Both cheap, both before any edit.
- **Dual-corpus Block B** (Cell 9): cfb-v3 control dispatch (confirm 0/5 reproduces in-session) → Copy-Unmount → cfb-v4 discriminator dispatch, both from bit-exact-identical pristine state.
- **Cell 13 REPLACED** with the AKD-verdict gate routing on the cfb-v3-vs-cfb-v4 *contrast* (AKD-PASS / AKD-FAIL / AKD-PARTIAL), not a single surface.
- **Heavy REUSE**: engine (no re-clone), 5 cov caches (no recompute), the three S2.24 3B adaptations (`v_loss_layer=27`, tied `lm_head` → `model.embed_tokens`, fresh-3B caches) carried verbatim.
- Block C 15-trial loop scoped to the cfb-v4 arm only.

Checkpoint chain extends to **#3** at Cell 5 (S2.22 #1 GRACE → S2.24 #2 MEMIT → S2.25 #3 MEMIT-AKD).

---

## 5. Constraints established

- **C-S225-AKD-1:** Cell P1 AKD HARD gate — `mean_AKD(cfb-v4) > mean_AKD(cfb-v3)` by ratified relative margin (recommend ≥5× the observed cfb-v3 floor) at the L2-6 band mean; FAIL → HALT before any edit. Threshold is relative because key-space scale is model/layer-dependent.
- **C-S225-1:** Targets held byte-identical to cfb-v3 across cfb-v4 (target-invariance under key-variance); any target substitution voids the clean contrast.
- **C-S225-2:** Both edits dispatch from bit-exact-identical pristine model state (Copy-Unmount between B-v3 and B-v4; IC-S23-4 gate between dispatches).
- **C-S225-3:** cfb-v4 result is verdict-ratifiable ONLY if the P1 AKD gate PASSED (a result on a non-high-AKD corpus answers nothing).
- **C-S225-4:** Reused cov caches re-checksummed at Cell 3 (entry) AND Cell 18 (exit); any mismatch halts.

---

## 6. Open questions (deferred to S2.26+)

- **OQ-S225-AKD-1:** Does cfb-v3 measure as low-AKD at L2-6 on 3B? (first direct measurement — resolves at Cell P1; predicted near-0). This number is a finding regardless of the cfb-v4 verdict.
- **OQ-S225-AKD-2:** If cfb-v4 PASSES, is the PASS frequency-correlated? (Cell 13/16)
- **OQ-S225-TEMPLATE-CONFOUND-1:** cfb-v4 varies subject-domain AND template jointly; a v5 could disentangle. Cell P1 per-pair report partially mitigates by showing which lever carried the spread.
- **OQ-S225-BASE-INSTRUCT-1:** base-vs-instruct deferred to a separate S2.27 arm.
- **OQ-S225-PS1/PS2/PS3:** probe-level calibration concerns (non-person-subject cons completions; Schenker music-adjacency; subject-token position variance) — resolve at Cell 7; substitution clauses handle pod-side, by Claude.
- **OQ-S224-EASYEDIT-1a:** resolves at Cell P0. **OQ-S224-2** (is [2-6] correct for Llama?): P0 informs; per-layer sweep (S2.27 if AKD-FAIL) resolves.

---

## 7. Hypothesis-class ledger (post-S2.25 authoring; unchanged from S2.24 — no new execution)

- **NEW — AKD/key-collision conjunction (OQ-S224-LIT-1):** OPEN, leading mechanistic hypothesis. S2.25 authored the discriminating experiment; S2.26 executes it.
- T.1 alt model (Llama scale): RESOLVED → ceiling generalizes 8B→3B (under low-AKD caveat).
- A/B/C/D: ELIM (S2.12-A / S2.11-B / S2.13-C / S2.15-D2). T.2 ROME: ELIM S2.18. T.2 GRACE: hparam-conditional elim S2.22. T.3 alt arch: OPEN, out-of-scope WS1.

---

## 8. Forward routing — S2.26 Cell 13 → S2.27

- **AKD-PASS** (cfb-v4 ≥3/5; cfb-v3 ~0/5): ceiling localizes to corpus AKD. → v1.3 framework_finding amendment ("low-AKD-corpus ceiling, not model-invariant") + WS3 "well-separated keys" guidance. S2.27 = KnowEdit external-validity + base-vs-instruct, as separate single-variable arms. **Highest-value outcome.**
- **AKD-FAIL** (cfb-v4 also ~0/5 despite confirmed-high AKD): AKD insufficient. → S2.27 = per-layer sweep (Berkeley recipe) + sequential-vs-joint dispatch axis.
- **AKD-PARTIAL** (1-2 facts): AKD contributing, not sufficient. → S2.27 = dispatch-mode axis holding AKD high.
- **P1 gate FAIL** (cfb-v4 not high-AKD): no verdict; corpus revision (Claude re-authors).

---

## 9. Standing directive committed (governs ALL forward sessions)

Committed to memory this session, no expiry:
1. **No operator editing.** Claude authors FULL artifacts end-to-end (corpus fills, probe sets, runbook cells, summaries); never leaves placeholders for the operator.
2. **All Claude recommendations are always accepted.** Make the call, state it, proceed; surface load-bearing/irreversible decisions for the record but do not block on ratification. Operator retains nominal ratification authority but defers fully.

This supersedes the earlier "operator fills placeholders / ratifies before authoring" pattern. The S2.25 deliverables were brought to full v1.0 completion under this directive (subjects/templates filled, probe set authored) rather than left with operator obligations.

---

## 10. S2.26 kickoff (successor)

**Scope:** Execution — T.1-α-MEMIT-AKD. Walk the runbook cell-by-cell pod-side. Block PRE (P0 EasyEdit diff, P1 AKD gate) → Block A (reuse-heavy pre-flight, Checkpoint #3) → Block B (dual-corpus dispatch, AKD-verdict gate) → Block C (cfb-v4 arm, route-conditional) → Block-end.

**Entry preconditions:** ALL SATISFIED. `session_2_25_summary_block.md` (this) + `t1_alt_model_3b_memit_akd_runbook_v0_1.md` + `cfb-v4-highAKD.yaml v1.0` + `probe-set-v4-highAKD.yaml v1.0` + `cfb-v3.yaml v1.0` (control) + `memit-patches-canonical v2.5`. Engine + 5 cov caches live on NV from S2.24 (no re-clone, no recompute for L2-6).

**Execution-session guidance:** carry forward the S2.24 §9 operator-guidance register verbatim — zero-ML-background step-by-step hand-holding, one cell at a time, label the surface every time, explain WHAT/WHY and the expected healthy output before each cell, frame a null result as signal not failure. Per the standing directive, Claude makes all calls and proceeds; surfaces only irreversible ops (verdict ratification, destructive ops) for explicit confirmation.

**First pod-side decision:** ratify the P1 AKD gate margin once cfb-v3's actual floor is measured (recommended ≥5×). Everything else is locked.

---

## 11. NV / environment carry-forward

- Engine SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` patched in place at `/workspace/memit_dry_run/memit` (reuse; verify SHA at Cell 1).
- 5 fresh 3B cov caches at `/workspace/covariance_caches/meta-llama_Llama-3.2-3B/wikipedia_stats/` (each 268,436,642 bytes; SHA-verified intact at S2.24 Cell 18). Reuse at L2-6 for both corpora.
- Pod `ee00aa7bcadb` valid only if not cycled since S2.24; if cycled, fresh image lacks rsync AND deps (reinstall per S2.24 §11). Pull current SSH target from RunPod console.
- `reproducibility_manifest.json` to be extended with `sessions["2.26"]` at execution close.

---

*End S2.25 summary block.*
