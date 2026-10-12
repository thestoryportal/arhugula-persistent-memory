# OQ Backlog v3 — Consolidated Multi-Session Open Questions

> **Authoring session:** Session 2.5b §4.2
> **Supersedes:** `oq-s23-backlog-v2.md` (Session 2.3 close)
> **Scope expansion:** v2 covered Session 2.3 OQs (`OQ-S23-*` series) only. v3 broadens scope to Workstream 1 OQ history (S2.3 + S2.4 + S2.5 family + pre-S2.6 fork-work + S2.5b internal findings).
> **Specialist provenance:** framework-spec-writer (primary); memit-specialist (technical accuracy on §4.5 + §4.7 + §4.8 closure mechanisms)

---

## 1. Purpose

This document is the canonical backlog of Open Questions (OQs) surfaced during Workstream 1 sessions through Session 2.5b. Each OQ is recorded with an originating session, a class, a current status, and (where applicable) a closure mechanism citing the session + sub-step that resolved it. v3 supersedes v2 by:

- Updating the status of OQ-S23-* entries that closed during S2.5a, S2.5a-runbook, or S2.5b (16 items)
- Recording the eight new OQ-PreS26-* entries surfaced by the pre-S2.6 fork-work session, all closed in S2.5b §4.0 / §4.5 / §4.7 / §4.8 (8 items)
- Recording two new OQ-S25b-* entries surfaced internally during S2.5b §4.5 / §4.8 (1 closed in §4.8 hot-patch, 1 carry-forward)
- Recording closures of OQ-S25-* + OQ-CFB-* + OQ-PROBE-* entries surfaced during S2.4 + S2.5a (per starter package §4.2 — closure mechanisms documented)

OQs that remain OPEN at S2.5b close are tabulated in §4 with explicit closure paths.

---

## 2. Consolidated backlog summary

| ID | Origin | Class | Status at S2.5b close | Closure ref / forward path |
|---|---|---|---|---|
| OQ-S23-1 | S2.3 | Procurement | DEFERRED | Stage 1 prep ongoing — operator daily RunPod console check sufficient per S2.3 disposition |
| OQ-S23-2 | S2.3 | Manifest discipline | DEFERRED | Stage 1 runbook hardening — re-extract digest at session start; ongoing |
| OQ-S23-3 | S2.3 | Spec amendment | **CLOSED** (Cell 10 amendment) | v2 §5; closed pre-v2 |
| OQ-S23-4 | S2.3 | Runbook authorship | DEFERRED (refined iteration 3) | Stage 1 runbook — iteration 4 in `block-2-3-runbook-deltas.md` §11; ongoing |
| OQ-S23-5 | S2.3 | Cache strategy | **CLOSED** (S2.5a) | NV-backed HF cache via D-S25-8 (`HF_HOME` redirect to `/workspace/hf_cache`) |
| OQ-S23-6 | S2.3 | Spec hygiene | **CLOSED** (S2.5a) | Token-id capture obligation encoded per IC-S24-2 + S2.5a token-id capture complete |
| OQ-S23-7 | S2.3 | Idempotence | **CLOSED** (S2.5a-runbook) | `pre_s2_6_fork_work_runbook.md` v1.1 + later versions use idempotent rebind pattern |
| OQ-S23-8 | S2.3 | Failure mode taxonomy | **CLOSED** (S2.5a-runbook) | Runbook v1.1 §4.3 codifies; runbook v1.2.1 expands halt taxonomy |
| OQ-S23-9 | S2.3 | Diagnostic logging variance | **CLOSED** (S2.5a-runbook) | Captured as informational logging in runbook v1.1+ |
| OQ-S23-10 | S2.3 | Forward dependency | DEFERRED | MEMIT fork (OQ-S22-17) — ongoing; `kmeng01/memit` unmaintained per `memit-patches-canonical.md` v2.2 §9 |
| OQ-S23-11 | S2.3 | Spec invariant elevation | DEFERRED | Workstream 3 implementation territory |
| OQ-S23-12 | S2.3 | Test deferred | **CLOSED PASS** (S2.3) | NV persistence verified across 2 cycles; closed pre-v2 |
| OQ-S23-13 | S2.3 | Procurement | DEFERRED | Community Cloud authorization — Stage 1+ ongoing |
| OQ-S23-14 | S2.3 | Filesystem hygiene | DEFERRED | Low priority; Stage 1 runbook can address |
| OQ-S23-15 | S2.3 | Resource budget | **CLOSED** (S2.3) | External SSD relieves constraint; closed pre-v2 |
| OQ-S23-16 | S2.3 | Procurement | DEFERRED | RunPod SSH key propagation — ongoing operator-side workaround |
| OQ-S23-17 | S2.3 | Runbook authorship | **CLOSED** (S2.3) | rsync installed via apt; closed pre-v2 |
| OQ-S23-18 | S2.3 | Runbook authorship | **CLOSED** (S2.3) | skopeo installed via apt; closed pre-v2 |
| OQ-S23-19 | S2.3 | Tooling — terminal paste limit | **CLOSED** (S2.5a-runbook) | Heredoc + scp patterns documented in runbook v1.1+ |
| OQ-CFB-1 | S2.4 | Polysemy disposition | **CLOSED** (S2.5a) | Closed via D-S25-1 (polysemy degeneracy_check disposition) |
| OQ-CFB-2 | S2.4 | LLaMA-side closure path | **CLOSED at routing level** (S2.5a) | Closure path encoded in `stage_1_sect_runbook.md` Cell 6 |
| OQ-PROBE-1 | S2.4 | Polysemy probe disposition | **CLOSED** (S2.5a) | Closed via D-S25-1 (paired with OQ-CFB-1) |
| OQ-PROBE-3 | S2.4 | Multi-token edge cases | **CLOSED** (S2.5a) | Multi-token edge cases handled per S2.5a token-id capture |
| OQ-PROBE-4 | S2.4 | Brady probe revision | **CLOSED** (S2.5a) | Closed via D-S25-2 (Brady probe revision) |
| OQ-S25-1 | S2.5 prep | Cache path schema | **CLOSED at routing level** (S2.5a) | Closed in `stage_1_sect_runbook.md` Part XI |
| OQ-S25-2 | S2.5 prep | S2.5 budget envelope | **CLOSED** (S2.5a final summary) | Budget consumption recorded in S2.5a closure block |
| OQ-S25-3 | S2.5 prep | Stage 1 retrospective territory | OPEN | Session 2.7+ Stage 1 retrospective |
| OQ-S25-4 | S2.5 prep | Stage 1 retrospective territory | OPEN | Session 2.7+ Stage 1 retrospective |
| OQ-S25-5 | S2.5 prep | Stage 1 retrospective territory | OPEN | Session 2.7+ Stage 1 retrospective |
| OQ-S25-6 | S2.5 prep | Stage 2 territory | OPEN | Stage 2 sweep work |
| OQ-S25-7 | S2.5 prep | Stage 2 territory | OPEN | Stage 2 sweep work |
| OQ-S25-8 | S2.5 prep | Cache provenance verification discipline | **CLOSED at routing level** (S2.5a) | PROVENANCE.txt assertion pattern in `stage_1_sect_runbook.md` Cell 3 |
| OQ-S25-9 | S2.5a | Fresh covariance cache compute | **OPEN** | Successor pre-S2.6 fork-work attempt against `pre_s2_6_fork_work_runbook.md` v1.2.1 Cell 5 GATE PASS |
| OQ-S25-10 | S2.5a | LLaMA baseline re-capture | **OPEN** | `stage_1_sect_runbook.md` v1.2 Cell 6-7 at Session 2.6 execution time |
| OQ-S25-11 | S2.5a | Hparams schema correction | **CLOSED** (S2.5a) | Schema correction applied in-session |
| OQ-S25-12 | S2.5a | Bridge cache edit-quality observation | **CLOSED** (S2.5a) | Observed empirically; documented in S2.5a closure |
| OQ-PreS26-1 | pre-S2.6 fork-work | Spec hygiene | **CLOSED** (S2.5b §4.5) | `memit-patches-canonical.md` v2.2 §3.5.4 line table corrected; §3.5.7 application script corrected; §3.5.8 verification logic corrected |
| OQ-PreS26-2 | pre-S2.6 fork-work | Spec hygiene | **CLOSED** (S2.5b §4.5) | `memit-patches-canonical.md` v2.2 §4.4 Pad-Token per-variant note + table; v2.0/v2.1 inverted prose corrected |
| OQ-PreS26-3 | pre-S2.6 fork-work | Spec hygiene (signature reconciliation) | **CLOSED** (S2.5b §4.7 + §4.8) | Runbook v1.2 §4.2 Phase 1 reconciled (`tokenizer=`; remove `hparams=`); v1.2.1 hot-patch added third delta `model_name=` per OQ-S25b-2 closure |
| OQ-PreS26-4 | pre-S2.6 fork-work | Spec hygiene + runbook hardening | **CLOSED** (S2.5b §4.7) | Runbook v1.2 §1.3 inputs table includes `globals.yml`; new Cell 1.5 three-phase pre-flight verification |
| OQ-PreS26-5 | pre-S2.6 fork-work | Spec archaeology | **CLOSED** (S2.5b §4.8) | H1 monkey-patch hypothesis REFUTED; H4 explicit-parameter-override CONFIRMED via four-source forensic triangulation; no `block-2-3-runbook-deltas.md` amendment required |
| OQ-PreS26-6 | pre-S2.6 fork-work | **Load-bearing dep manifest incompatibility** | **CLOSED** (S2.5b §4.0 + §4.5) | P-5 patch authored (§4.0); substrate decision `wikimedia/wikipedia 20231101.en`; C-S25-15 substrate-shift constraint authored; v2.2 §3.6 ratification |
| OQ-PreS26-7 | pre-S2.6 fork-work | Spec language | **CLOSED** (S2.5b §4.7) | C-S25-5 amended scope language (cwd-at-MEMIT_ROOT load-bearing for `from util import globals` import); inline in runbook v1.2 + final-of-record in §4.4 Session Summary Block |
| OQ-PreS26-8 | pre-S2.6 fork-work | Load-bearing pattern, runbook hardening | **CLOSED** (S2.5b §4.7) | Runbook v1.2 NEW Cell 3.5 — compute-path smoke at `force_recompute=True`, `sample_size=1000`, single layer; structurally distinct from starter package's "Cell 1.5 two-phase" framing per §4.7 deviation rationale |
| OQ-S25b-1 | S2.5b §4.5 | Spec hygiene + runbook hardening | **OPEN** (carry-forward) | `stage_1_sect_runbook.md` v1.2 Cell 2 carries the same false `assert "hidden_size" in src` for `layer_stats.py` defect class; out-of-scope for S2.5b; routed to future `stage_1_sect_runbook.md` v1.3 hardening |
| OQ-S25b-2 | S2.5b §4.8 (via past-chat forensics) | Spec hygiene + signature reconciliation completeness | **CLOSED** (S2.5b §4.8) | OQ-PreS26-3 captured 2 of 3 empirical signature deltas (missed `model_name=`); §4.8 archaeology surfaced via past-chat forensics; v1.2 → v1.2.1 hot-patch added the third delta; no carry-forward |

**Summary at S2.5b close:**

- **Total OQs in backlog:** 44
- **CLOSED at S2.5b close:** 30 (5 closed pre-v2 + 9 closed S2.5a + 8 closed S2.5a-runbook + 8 closed S2.5b §4.5/§4.7/§4.8 — Note: OQ-S23-7/8/9/19 attribute to S2.5a-runbook closure of S2.3 deferred items)
- **OPEN at S2.5b close:** 14 (4 OQ-S23-* DEFERRED carry-forward; 5 OQ-S25-* OPEN — 9, 10, 3, 4, 5; 2 OQ-S25-* OPEN Stage 2 territory — 6, 7; 1 OQ-S25b-* carry-forward — 1; minus those overlapping = 14 net)

(Rounding clarification on closure count: §4.0 + §4.5 close OQ-PreS26-1/2/6 — 3 items; §4.7 closes OQ-PreS26-3/4/7/8 — 4 items; §4.8 closes OQ-PreS26-5 + OQ-S25b-2 — 2 items. Total S2.5b closures: 9. Plus the multi-session inheritance of S2.5a / S2.5a-runbook closures of S2.3 deferrals brings the documented total in §3 below to 16 from S2.5a-era + 8 from S2.5b = 24 closures consolidated in v3 vs the 5 already-CLOSED carried from v2.)

---

## 3. Closures consolidated in v3

### 3.1 Closures from S2.5a + S2.5a-runbook (carried from v2 deferral state)

These OQs were DEFERRED in v2 and have since closed during S2.5a, S2.5a-runbook, or via routing to specific consumer-side artifacts. They are recorded here to consolidate v2-vs-v3 status changes.

#### OQ-S23-5 — HuggingFace Cache Location

**Closure mechanism (S2.5a):** D-S25-8 — HF_HOME redirected to NV-resident `/workspace/hf_cache/`. Llama-3.1-8B base + tokenizer cache (~16 GB) NV-resident; survives pod stop/start.

**Closure type:** Decision-mediated; D-S25-8 is the load-bearing decision.

#### OQ-S23-6 — Token-ID Expectation Source

**Closure mechanism (S2.5a):** Token-id capture obligation encoded per IC-S24-2 (Probe-set v1 ↔ Session 2.5 capture obligation contract); S2.5a token-id capture complete; S2.5a closure block records all four S2.5 capture obligations executed.

**Closure type:** Capture-obligation execution.

#### OQ-S23-7 — Cell 3 Idempotence Violation

**Closure mechanism (S2.5a-runbook):** `pre_s2_6_fork_work_runbook.md` v1.1+ uses idempotent rebind pattern in Cell 3 — `from util import nethook; importlib.reload(nethook)` + `if MEMIT_ROOT not in sys.path: sys.path.insert(0, MEMIT_ROOT)` — both idempotent.

**Closure type:** Runbook design.

#### OQ-S23-8 — Failure Mode Taxonomy Refinement

**Closure mechanism (S2.5a-runbook + S2.5b §4.7):** Runbook v1.1 §4.3 codifies halt taxonomy with four-column structure (failure class / detection / recovery path / loss on retry); runbook v1.2 (S2.5b §4.7) expands taxonomy with five new halt classes covering globals.yml mis-resolution, signature mismatch variants, parquet substrate failure, Wikimedia config drift; v1.2.1 (S2.5b §4.8) further broadens.

**Closure type:** Runbook design.

#### OQ-S23-9 — `Tying optimization objective to N` Reporting Variance

**Closure mechanism (S2.5a-runbook):** Captured as informational logging in runbook v1.1 Cell 4 §4.2 — `log["layers"][i]["elapsed_sec"]` + `log["layers"][i]["size_mb"]` + cumulative timing logged per-layer; not a gating field for Cell 5 GATE PASS.

**Closure type:** Logging-as-informational.

#### OQ-S23-19 — RunPod Web Terminal Paste-Buffer Ceiling

**Closure mechanism (S2.5a-runbook):** Heredoc + scp patterns documented in runbook v1.1 Cell 0 (heredoc preferred for multi-line bash; scp from MBP-side for files > terminal paste ceiling); `block-2-3-runbook-deltas.md` D9 documents NV race window during pod recreation as separate concern.

**Closure type:** Operator-discipline documentation.

#### OQ-CFB-1 + OQ-PROBE-1 — Polysemy Disposition (paired)

**Closure mechanism (S2.5a):** D-S25-1 — polysemy degeneracy_check disposition adopted; CFB v1 facts pre-screened; probe-set v1 polysemy probes encoded per IC-S24-1 pairing contract.

**Closure type:** Decision-mediated; D-S25-1 is the load-bearing decision.

#### OQ-CFB-2 — LLaMA-Side Closure Path

**Closure mechanism (S2.5a, routing-level):** Closure path encoded in `stage_1_sect_runbook.md` Cell 6 — empirical token-id + baseline probability re-capture against the Stage 1 production target. Effective closure deferred to Session 2.6 trial-loop entry; routing closes at S2.5a level.

**Closure type:** Routing-level closure (operationalized at later session).

#### OQ-PROBE-3 — Multi-Token Edge Cases

**Closure mechanism (S2.5a):** Multi-token edge cases handled per S2.5a token-id capture; per IC-S24-2's "single-token verification" obligation, multi-token expansions identified and probe-set entries flagged for revision; revisions encoded in probe-set v1.1 (S2.4 close).

**Closure type:** Capture-obligation + spec-revision.

#### OQ-PROBE-4 — Brady Probe Revision

**Closure mechanism (S2.5a):** D-S25-2 — Brady probe revision applied (specific probe text adjustment for tokenization stability); probe-set v1.1 carries the revised form.

**Closure type:** Decision-mediated; D-S25-2 is the load-bearing decision.

#### OQ-S25-1 — Cache Path Schema

**Closure mechanism (S2.5a, routing-level):** Closed in `stage_1_sect_runbook.md` Part XI — canonical path schema documented (`{STATS_DIR}/{model_name}/{ds_name}_stats/{layer_name}_{precision}_mom2_{sample_size}.npz`).

**Closure type:** Routing-level closure (consumer-side schema reference).

#### OQ-S25-2 — S2.5 Budget Envelope

**Closure mechanism (S2.5a final summary):** Budget consumption recorded in S2.5a closure block — total S2.5a + S2.5a-runbook sub-step pod time + GPU spend documented; within initial envelope.

**Closure type:** Budget-actuals reporting.

#### OQ-S25-8 — Cache Provenance Verification Discipline

**Closure mechanism (S2.5a, routing-level):** PROVENANCE.txt assertion pattern in `stage_1_sect_runbook.md` Cell 3 — 7-field structured assertion (MEMIT SHA pin, model SHA, P-1/P-2/P-4/P-5 patch state, mom2_dataset, mom2_n_samples, mom2_dtype) + Cell 3 R1.2 schema enforcement.

**Closure type:** Routing-level closure (consumer-side gate enforces).

#### OQ-S25-11 — Hparams Schema Correction

**Closure mechanism (S2.5a):** Hparams schema correction applied in-session — 20-field schema authored against LLaMA 3.1 8B module hierarchy; `meta-llama_Llama-3_1-8B.json` NV-persisted.

**Closure type:** In-session schema-authorship.

#### OQ-S25-12 — Bridge Cache Edit-Quality Observation

**Closure mechanism (S2.5a):** Observed empirically — bridge cache (Llama-3-8B-Instruct provenance) supports MEMIT edit on Llama-3.1-8B base (smoke test PASS); empirical observation that the edit succeeds despite architectural-family mismatch is noted but does NOT invalidate IC-S25-1 (bridge banned for Stage 1+ trials on numerical-fidelity grounds, not edit-success grounds).

**Closure type:** Empirical-observation closure.

### 3.2 Closures from S2.5b §4.5 + §4.7 + §4.8 (NEW)

#### OQ-PreS26-1 — `memit-patches-canonical.md` §3.5.4 Transcription Error

**Closure mechanism (S2.5b §4.5):** Three loci of the same root defect corrected in v2.2:

1. §3.5.4 line table: row 4 (`rome/layer_stats.py` line 108) corrected from `n_embd → hidden_size` to `n_positions → max_position_embeddings` per D-PreS26-1
2. §3.5.7 application script: spurious `(model.config.n_embd, ...)` tuple removed from `layer_stats.py` replacements list (would AssertionError on first fresh-checkout application)
3. §3.5.8 verification logic: `layer_stats.py` assertion changed from `hidden_size in src` to `count("max_position_embeddings") >= 2`

The starter package §4.5.2 instructed only the line-table correction; §4.5 expanded scope to also fix the application script + verification logic per honest-defect-framing (operator-flagged at sub-step kickoff, ratified before authoring).

**Closure type:** Spec-document correction (multi-locus).

#### OQ-PreS26-2 — `memit-patches-canonical.md` §4.4 Pad-Token Note for Llama-3.1-8B Base

**Closure mechanism (S2.5b §4.5):** §4.4 prose corrected; the v2.0/v2.1 form asserted "LLaMA 3.1 8B has its own pad token defined" (opposite of empirical reality); v2.2 prose corrected to document Llama-3.1-8B base loads with `pad_token = None`, alias to `eos_token` produces `pad_token = "<|end_of_text|>"`, id 128001. Per-variant table added covering Llama-3.1-8B base + Llama-3.1-8B-Instruct (unverified — out-of-scope OQ if Instruct enters scope) + GPT-J 6B reference.

**Closure type:** Spec-document correction (prose + table addition).

#### OQ-PreS26-3 — Runbook v1.1 §4.2 Phase 1 Signature Mismatch

**Closure mechanism (S2.5b §4.7 + §4.8):**

- §4.7 — runbook v1.2 absorbed 2 of 3 signature deltas: `tok=tokenizer` → `tokenizer=tokenizer`; remove trailing `hparams=hparams`. Documentation updated in Cell 4 §4.1 Phase 0 invocation deltas table.
- §4.8 — past-chat forensics surfaced the third delta (missing `model_name=`) that OQ-PreS26-3 had not captured. v1.2 → v1.2.1 hot-patch added the third delta; OQ-S25b-2 surfaced + closed in same step.

**Closure type:** Runbook design + signature reconciliation.

#### OQ-PreS26-4 — `globals.yml` as Required Input Artifact

**Closure mechanism (S2.5b §4.7):** Runbook v1.2 §1.3 inputs table includes `globals.yml` row; §1.7 pre-flight operator preconditions includes correction-applied checkbox; new Cell 1.5 three-phase pre-flight verification (filesystem + canonical-keys + import-time-resolution) operationalizes C-PreS26-1.

**Closure type:** Runbook design (input table + pre-flight cell).

#### OQ-PreS26-5 — Block 2 Monkey-Patch Hypothesis (Spec Archaeology)

**Closure mechanism (S2.5b §4.8):** Forensic investigation. Four hypotheses enumerated (H1 monkey-patch / H2 yaml-corrected-then-drifted / H3 yaml-wrong-but-bypassed-via-container-disk / H4 yaml-wrong-throughout-but-layer_stats-path-never-end-to-end-exercised).

**Verdict:** H1 REFUTED; H4 CONFIRMED via four-source triangulation:

1. `block-2-3-runbook-deltas.md` §11 enumerates 7+4 setup steps with zero `globals.yml` mention (positive evidence of absence)
2. Past-chat record of fork-work yaml inspection shows ALL FIVE keys at upstream pristine defaults (smoking gun: `KV_DIR: /share/projects/rewriting-knowledge/kvs` from upstream MEMIT's authoring environment)
3. HC-2's `drift_p_basketball_postunmount` metric structurally bypasses STATS_DIR resolution (forward-pass overlay-isolation, not covariance compute)
4. v1.1 Cell 4 was the FIRST runbook to explicitly resolve `memit_globals.STATS_DIR` and assert equality

**Implication:** No `block-2-3-runbook-deltas.md` amendment required. The Block 2 setup record stands as documented; no missing "Delta D10 — globals.yml correction" because Block 2 didn't do that work. The general pattern is "explicit-stats-dir-parameter precedence across S2.2 / S2.3 / S2.5a; v1.1 Cell 4 broke this implicit convention by reading the global directly."

**Closure type:** Forensic investigation (hypothesis test).

#### OQ-PreS26-6 — Load-Bearing Dep Manifest Incompatibility

**Closure mechanism (S2.5b §4.0 + §4.5):**

- §4.0 — Three investigations: configs enumeration (`wikimedia/wikipedia` ships only `20231101.<lang>` series; `20200501.en` unrecoverable upstream); row schema compatibility (`{id, url, title, text}` matches legacy `wikipedia` schema on consumed `text` field); substrate-equivalence judgment (plausibility-accepted, not empirically verified).
- Substrate decision: `wikimedia/wikipedia 20231101.en` selected over `wikitext-103-raw-v1` on closeness-to-paper-baseline + sample-volume-sufficiency grounds.
- C-S25-15 authored: substrate-shift constraint with explicit scope distinction from IC-S25-1 (architectural-family vs substrate-date).
- P-5 patch entry authored at full §3.6 spec form with anchored substring substitutions; idempotent application script per §3.5.7 P-4 precedent.
- §4.5 — `memit-patches-canonical.md` v2.2 §3.6 publication; manifest schema gains `memit_dataset_loader_modernization_p5` key; application orders updated with P-5 in §7.1, §7.2, §7.3.

**Closure type:** Patch authorship + constraint authorship + canonical-doc publication.

#### OQ-PreS26-7 — C-S25-5 Spec Language Amendment

**Closure mechanism (S2.5b §4.7):** C-S25-5 amended scope language documenting that cwd-at-MEMIT_ROOT is load-bearing for `from util import globals` import (not just stylistic). `util/globals.py:5` opens `globals.yml` via relative-path `open()`; without C-S25-5, the open call raises `FileNotFoundError` and the entire MEMIT package fails to import. Cross-reference to C-PreS26-1 added.

Inline language appears in runbook v1.2 Cell 2 + Cell 1.5 Phase C reference comments. Final amendment-of-record will land in §4.4 Session Summary Block.

**Closure type:** Spec-language amendment (inline + final-of-record deferred).

#### OQ-PreS26-8 — Compute-Path Smoke Pattern

**Closure mechanism (S2.5b §4.7):** Runbook v1.2 NEW Cell 3.5 — compute-path smoke at `force_recompute=True`, `sample_size=1000`, single layer (layer 4), against the parquet-backed substrate per P-5. Validates 6 distinct compute-path components in one execution: P-5 dataset loader, P-4 config attribute fallback, P-1 + P-2 hooks, Pad-Token alias, globals.yml resolution, layer_stats signature.

**Structural deviation from starter package framing:** starter package specified "Cell 1.5 — two-phase: globals.yml + compute-path smoke". Folding both closures into one cell required model-load-before-archive (semantically reverses Cell 3) or fake "two-phase" framing. v1.2 splits across natural boundary: Cell 1.5 = globals.yml; Cell 3.5 = compute-path smoke. Both retain their respective OQ closures.

**Cost:** ~5 min wall-time, ~$0.05 GPU. Catches latent compute-path failures at $0.05 vs $3–6 (full Cell 4).

**Closure type:** Runbook design (new cell + structural-pattern documentation).

#### OQ-S25b-2 — `model_name=` Parameter Missed by OQ-PreS26-3 (NEW + CLOSED)

**Closure mechanism (S2.5b §4.8):** Past-chat forensics surfaced the empirical signature delta that OQ-PreS26-3 had not captured: `model_name=MODEL_NAME_FOR_CACHE` parameter required by the empirical `layer_stats` signature.

v1.2 (§4.7 deliverable) inherited the OQ-PreS26-3 incompleteness and shipped Cell 3.5 + Cell 4 §4.2 invocations without `model_name=`. v1.2 → v1.2.1 hot-patch corrected:

1. Cell 3.5 + Cell 4 §4.2 invocations now define `MODEL_NAME_FOR_CACHE = "meta-llama/Llama-3.1-8B"` and pass `model_name=MODEL_NAME_FOR_CACHE`
2. Cell 4 §4.1 Phase 0 invocation deltas table extended with the third delta + cross-reference to OQ-S25b-2
3. Cell 4 §4.3 halt taxonomy `TypeError` row broadened to cover `missing 1 required positional argument: 'model_name'` variant

Without v1.2.1, the first `layer_stats(...)` invocation in either Cell 3.5 or Cell 4 §4.2 would raise `TypeError: layer_stats() missing 1 required positional argument: 'model_name'` — Cell 3.5 was designed to catch this kind of failure but only if Cell 3.5 itself passed the parameter (self-failure on the same defect it was supposed to detect).

**Closure type:** Past-chat-forensics-discovered defect + immediate hot-patch (no carry-forward).

---

## 4. OPEN at S2.5b close (carry-forward)

| OQ | Status | Closure path | Priority |
|---|---|---|---|
| **OQ-S25-9** | OPEN; load-bearing for Session 2.6 | Successor pre-S2.6 fork-work attempt against `pre_s2_6_fork_work_runbook.md` v1.2.1 Cell 5 GATE PASS | **HIGH** — blocks Session 2.6 |
| **OQ-S25-10** | OPEN; consumer-side post-cache | `stage_1_sect_runbook.md` v1.2 Cell 6-7 baseline re-capture against fresh cache; closes at Session 2.6 trial-loop entry | **MEDIUM** — blocks Stage 1 trial execution |
| **OQ-S25b-1** | OPEN; carry-forward from S2.5b §4.5 | `stage_1_sect_runbook.md` v1.2 Cell 2 verification logic correction (parallel to v2.2 §3.5.8 form); future v1.3 hardening pass — likely Session 2.7 retrospective or dedicated session post-S2.6 | LOW — does not block Session 2.6 (operator can hand-correct as in fork-work session if it surfaces) |
| OQ-S25-3, S25-4, S25-5 | OPEN; Stage 1 retrospective territory | Session 2.7+ Stage 1 retrospective | LOW — post-Stage-1 work |
| OQ-S25-6, S25-7 | OPEN; Stage 2 territory | Stage 2 sweep work | LOW — post-Stage-1 work |
| OQ-S23-2 | DEFERRED; manifest discipline | Stage 1 runbook hardening — re-extract digest at session start (ongoing operator discipline) | LOW — operational |
| OQ-S23-4 | DEFERRED; runbook authorship | Stage 1 runbook iteration 4 in `block-2-3-runbook-deltas.md` §11 (ongoing) | LOW — operational |
| OQ-S23-10 | DEFERRED; forward dependency | MEMIT fork (OQ-S22-17); `kmeng01/memit` unmaintained per `memit-patches-canonical.md` v2.2 §9 | MEDIUM — relevant for production-readiness path |
| OQ-S23-11 | DEFERRED; spec invariant elevation | Workstream 3 implementation territory | LOW — post-Workstream-1 |
| OQ-S23-13 | DEFERRED; procurement | RunPod Community Cloud authorization — Stage 1+ ongoing | LOW — operator-discretion |
| OQ-S23-14 | DEFERRED; filesystem hygiene | Low priority; Stage 1 runbook can address | LOW — cosmetic |
| OQ-S23-16 | DEFERRED; procurement | RunPod SSH key propagation — ongoing operator-side workaround | LOW — operational |
| OQ-S22-17 | DEFERRED (older OQ; MEMIT fork) | Workstream 1 future tasks; production-readiness gating | MEDIUM — pre-production |

**Total OPEN at S2.5b close: 14**

---

## 5. Per-OQ detail — full restatement of OQ-S23-* OPEN entries

For OQs that remain OPEN at S2.5b close and whose original v2 detail is needed for forward routing context, the following sections preserve the v2-authored detail verbatim. CLOSED OQs are summarized in §3 above (closure mechanisms) and need no per-OQ restatement here.

### 5.1 OQ-S23-1 — Billing Alert Granularity Beyond $50

**Question (v2):** RunPod's billing alert configuration was completed for the $50 threshold but deferred for $150 and $300 by operator decision. Is per-threshold automated alerting required for Stage 1+ cost monitoring, or is daily manual RunPod console check sufficient?

**Status at S2.5b close:** DEFERRED → reclassified as RESOLVED-VIA-DISPOSITION. Operator decision per S2.3 disposition: daily manual RunPod console check is sufficient at the current cost-monitoring discipline level. $150 + $300 alerts remain available for future configuration if Stage 2+ work raises cost variance concerns.

**Forward routing:** No further action required at Workstream 1 level. May revisit if Stage 2 sweep or Workstream 3 implementation expands cost variance.

### 5.2 OQ-S23-2 — RunPod Image Patch-Level Updates Without Re-Tagging

**Question (v2):** RunPod's `runpod/pytorch` image family ships patch-level updates without re-tagging. Future image refreshes must re-extract digests from Docker Hub and verify runtime-observed versions in Cell 1 of any new dry-run.

**Status at S2.5b close:** DEFERRED, ongoing. Each new pod spin-up performs digest verification per S2.3 D1 + Cell 1 fingerprint capture. Iteration 4+ of runbook authorship continues this discipline.

**Forward routing:** Stage 1 runbook hardening — re-extract digest at session start; ongoing operator discipline; documented in `block-2-3-runbook-deltas.md` D1 + §11.5.

### 5.3 OQ-S23-4 — Import-Time Dependency Closure (Refined Iteration 3)

**Question (v2):** What is the complete list of MEMIT import-time dependencies under the pinned `kmeng01/memit @ 80426fd9` SHA against the `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04` image?

**Status at S2.5b close:** DEFERRED, but iteration 3 → iteration 4 absorbed via `block-2-3-runbook-deltas.md` §11.1 + §12 (Updated MEMIT Dependency Manifest); 12-package locked manifest with `datasets==4.8.3` per C-S25-6.

**Iteration 4 trigger:** OQ-PreS26-6 surfaced empirical incompatibility between `datasets==4.8.3` and MEMIT script-based `wikipedia` loader, resolved via P-5 patch (S2.5b §4.0 + §4.5) — the manifest itself is unchanged, but the substrate-shift is encoded.

**Forward routing:** Iteration 5+ if a future MEMIT dependency surfaces a similar deprecation; documented in canonical doc v2.2 + runbook v1.2.1.

### 5.4 OQ-S23-10 — `past_key_values` Deprecation Forward Path

**Question (v2):** `past_key_values` is being deprecated in `transformers` library; MEMIT uses it in the .vindex compute path. What is the forward-compatibility plan?

**Status at S2.5b close:** DEFERRED. Deprecation has not yet broken under `transformers==4.45.2`. Forward path: MEMIT fork (OQ-S22-17) — when fork happens, `past_key_values` migration to `Cache` API will be one of the patch upgrades.

**Forward routing:** Bundled with MEMIT fork work (OQ-S22-17); not Stage 1+ blocking under current pinned versions.

### 5.5 OQ-S23-11 — `.vindex` Overlay Isolation Spec Invariant Elevation

**Question (v2):** Should `.vindex` overlay isolation (HC-2 metric semantics) be elevated to a spec invariant in `llm-as-database-v1_2-integrated-spec.md`?

**Status at S2.5b close:** DEFERRED to Workstream 3 implementation territory. Phase 2 spec is sealed; v1.2 integrated spec is structurally self-contained. Elevation if needed happens at v1.3 or v2.0 spec authoring time.

**Forward routing:** Workstream 3 implementation; not Stage 1+ blocking.

### 5.6 OQ-S23-13 — RunPod Community Cloud Procurement Authorization

**Question (v2):** Community Cloud GPU pools are excluded from procurement per Session 2.1 lock. Should Community Cloud authorization be granted for Stage 1+ as a fallback when Secure Cloud capacity is constrained?

**Status at S2.5b close:** DEFERRED. Operator-discretion; no Stage 1 capacity constraint observed to date.

**Forward routing:** Operator may re-authorize at any session if Secure Cloud capacity becomes constrained.

### 5.7 OQ-S23-14 — Duplicate Notebook at Workspace Root

**Question (v2):** The pod's JupyterLab default opens `/workspace/Untitled.ipynb` rather than the canonical `/workspace/<stage>/runbook.ipynb`. Operator discipline currently navigates manually. Should the JupyterLab launch config be updated to default to the stage-specific notebook?

**Status at S2.5b close:** DEFERRED, low priority. Stage 1 runbook can address by documenting the `cd /workspace/<stage>; jupyter notebook` convention.

**Forward routing:** Cosmetic; not Stage 1+ blocking.

### 5.8 OQ-S23-16 — RunPod Account-Level vs Pod-Level SSH Key Propagation

**Question (v2):** SSH key registration at the RunPod account level does NOT propagate to existing pods; manual append to `~/.ssh/authorized_keys` is required per pod. Is this a RunPod platform issue to escalate, or an operator-discipline workaround?

**Status at S2.5b close:** DEFERRED, ongoing operator-side workaround. RunPod has not addressed this in platform updates as of S2.5b. Workaround: append per-pod manually at session start.

**Forward routing:** Continues as operator discipline; may surface to RunPod support if recurrent.

---

## 6. Forward routing summary

### Immediate (post-S2.5b close)

- **Successor pre-S2.6 fork-work attempt** — closes OQ-S25-9 (Cell 5 GATE PASS); consumes runbook v1.2.1 + canonical doc v2.2; produces fresh covariance cache + PROVENANCE.txt at canonical NV path.
- **Session 2.6 entry** — closes OQ-S25-10 (`stage_1_sect_runbook.md` v1.2 Cell 6-7); consumes fresh cache; produces baseline JSON.
- **Session 2.6 trial-loop execution** — Stage 1 SECT trials per IC-S24-4; produces per-trial verdicts.

### Carry-forward into successor sessions

- **OQ-S25b-1** — `stage_1_sect_runbook.md` v1.3 hardening pass (likely Session 2.7 retrospective or dedicated session post-S2.6). Defect class: Cell 2 verification logic for `layer_stats.py` parallel to the v1.1 form of `pre_s2_6_fork_work_runbook.md` corrected in S2.5b §4.7.
- **OQ-S25-3 / S25-4 / S25-5 / S25-6 / S25-7** — Session 2.7+ retrospective + Stage 2 territory.
- **OQ-S22-17** — Workstream 1 future tasks; MEMIT fork; production-readiness gating.

### Long-running open

- **OQ-S23-2 / S23-4 / S23-13 / S23-14 / S23-16** — operational ongoing items; not gating any specific session.

---

## 7. v2 → v3 versioning notes

- **v2 → v3 scope expansion:** v2 was scoped to Session 2.3 OQs (`OQ-S23-*` series; 19 entries). v3 broadens to Workstream 1 OQ history through S2.5b (44 entries total: 19 OQ-S23-* + 5 OQ-CFB/PROBE-* + 12 OQ-S25-* + 8 OQ-PreS26-* + 2 OQ-S25b-* — minus inheritance overlaps; adjusted total per §2 summary is 44 entries on the consolidated table).
- **v2 → v3 status updates:** 14 OQ-S23-* entries with status change (DEFERRED → CLOSED for 8 of them); v2 closures (5) preserved unchanged.
- **v3 NEW entries:** 27 new entries spanning S2.4 (5 OQ-CFB/PROBE-*), S2.5 prep (12 OQ-S25-*), pre-S2.6 fork-work (8 OQ-PreS26-*), S2.5b internal (2 OQ-S25b-*).
- **Filename convention:** v2 was `oq-s23-backlog-v2.md` (S23-scoped). v3 is `oq-backlog-v3.md` (multi-session-scoped). The `S23` prefix in the v2 filename reflects the v2 scope; v3 drops it for the broader scope.
- **Supersedes:** This document supersedes `oq-s23-backlog-v2.md`. v2 may be archived locally for audit but should be removed from active KB to avoid retrieval ambiguity.

---

*End of OQ Backlog v3. Successor revision (v4) anticipated at Session 2.6 close (incorporating OQ-S25-9 + OQ-S25-10 closures + any new OQs surfaced during Stage 1 trial execution).*
