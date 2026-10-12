# Session 2.26 — Summary Block

**Session type:** Execution (T.1-α-MEMIT-AKD; pod-side, Llama-3.2-3B)
**Predecessor:** S2.25 (T.1-α-MEMIT-AKD runbook + cfb-v4 + paired probe set authoring; CLOSED 2026-06-15)
**Closed:** 2026-06-15
**Verdict:** `P1-GATE-FAIL → AKD-ELIMINATED-BY-HIGH-CONTROL`
**Headline finding:** cfb-v3 — the corpus behind the entire eight-axis ceiling — is **high-AKD**, not low-AKD. The low-AKD-artifact hypothesis is **empirically false on 3B**. The ceiling survives on a confirmed well-separated-key corpus.
**Edit dispatched:** NONE. Session halted at the Cell P1 pre-flight gate before any edit, exactly as `C-S225-AKD-1` requires. Model loaded read-only; covariance caches certified byte-identical to S2.24.

---

## 1. What S2.26 was supposed to do, and what actually happened

**Designed purpose:** run the matched-pair contrast cfb-v3 (predicted LOW-AKD) vs cfb-v4 (HIGH-AKD), holding everything fixed except MEMIT key separation, to answer `OQ-S224-LIT-1` / `OQ-S225-AKD-1` — is the eight-axis "architectural-invariant ceiling" a property of **the model** or of a **degenerate low-AKD corpus** we had been running it on all along?

**What happened:** the experiment never reached an edit. The Cell P1 pre-flight AKD measurement — the first direct measurement of AKD ever taken in this workstream — discovered that **the premise was false.** cfb-v3 is not low-AKD. Its five subject-last-token keys sit 3.4–5.6 apart per layer (band mean **4.62** at L2–6), essentially the same spread as cfb-v4 (band mean **4.85**, ratio **1.05×**). The 5× separation gate FAILED — but not because cfb-v4 was under-separated (the failure mode the gate was built to catch); rather because **the denominator was never small.**

This collapses the runbook's two P1 halt branches into the rarer one: the runbook flagged "if cfb-v3 comes out unexpectedly high → surface to operator, reframes the session." That is the branch we landed in. The gate read FAIL on the *ratio*; the *reason* is that cfb-v3 was high-AKD all along.

---

## 2. The numbers (Cell P1, read-only, hardened by Cell P1-VERIFY)

Per-layer mean pairwise Euclidean key distance at the subject-last-token, edit-layer site (input to `mlp.down_proj` — the exact vector MEMIT's `compute_z` keys on):

| layer | cfb-v3 (LOW, control) | cfb-v4 (HIGH, discriminator) | ratio |
|---|---|---|---|
| 2 | 3.3812 | 3.3711 | 1.00 |
| 3 | 3.9661 | 3.9920 | 1.01 |
| 4 | 4.8381 | 5.4442 | 1.13 |
| 5 | 5.3090 | 5.5046 | 1.04 |
| 6 | 5.6071 | 5.9374 | 1.06 |
| **BAND** | **4.6203** | **4.8499** | **1.05** |

```
CELLP1_AKD_OK cfb_v3_mean=4.6203 cfb_v4_mean=4.8499 ratio=1.05 gate=FAIL (threshold=5.0x)
```

**cfb-v4 nearest-pair audit @ L4** (the two pre-flagged collapse risks): 003↔005 (Danube/Kilimanjaro) = 5.79; 001↔002 (Heisenberg/Schenker) = 5.05. Both well-separated; the corpus authorship was sound — cfb-v4 *is* high-AKD, it just isn't **higher** than an already-high cfb-v3.

Monotonic increase with depth (3.4 → 5.6) on both corpora is the expected pattern as representations differentiate up the stack. Keys were never collapsed at any edit layer.

---

## 3. Measurement-integrity verification (Cell P1-VERIFY — load-bearing)

The headline finding rests entirely on having sampled the **subject's final token** and not the following template token (an off-by-one in the prefix-tokenization position-finder would *spuriously inflate* cfb-v3's reading, since trailing template tokens differ across cfb-v4's distinct templates). Verified all 10 facts by decoding the sampled position and its neighbors:

```
P1_VERIFY_OK 10/10 — sampled position is subject-final token in every case; no off-by-one.
```

The two boundary-risk cases landed correctly: `the Danube` sampled `ube` (→ next `is`), `the Python programming language` sampled `language` (→ next `would`). The finding is a real property of the keys, not a sampling artifact.

---

## 4. Why our intuition was wrong (the mechanism lesson)

We reasoned: "5 clustered athletes + 1 identical template → collapsed keys → low AKD." That mis-mapped the MEMIT-Merge literature's failure condition onto our corpus. The MEMIT key is the activation at the **subject's last token**, which is dominated by **subject identity**. "Jackson / Woods / Sanders / Olajuwon / Vonn" are lexically and representationally distinct tokens; the shared template adds shared *context* but does not collapse the subject-identity-dominated key. The literature's low-AKD trap bites on batches of **near-duplicate subjects** (e.g. the same entity restated), not five different famous people sharing a sentence frame. Domain clustering of subjects (all athletes) is **not** the same as key clustering.

This is a reusable principle for all future corpus design: **AKD must be measured, not assumed from subject-domain similarity.** Cell P1 is now the canonical instrument for this and should pre-flight any future MEMIT batch corpus.

---

## 5. What this resolves and what it does NOT

**RESOLVES — `OQ-S225-AKD-1` and the AKD branch of `OQ-S224-LIT-1`, decisively AGAINST the AKD hypothesis.** Not by finding "high-AKD also fails" (we never edited cfb-v4), but by the stronger route: the ceiling-corpus was high-AKD from the start. MEMIT had well-separated keys to work with on cfb-v3 across all eight axes and still produced 0/5. **AKD / key-collision is eliminated as the explanation for the ceiling.**

**DOES NOT weaken the ceiling — STRENGTHENS it.** We removed the most attractive "it's-just-a-bad-corpus" escape hatch. The ceiling survives on a confirmed well-separated-key corpus.

**DOES NOT void cfb-v4.** The corpus is correctly authored and genuinely high-AKD; it is simply not a *contrast* against cfb-v3 (both are high-AKD), so a cfb-v4 edit would answer nothing about AKD (`C-S225-3`: not verdict-ratifiable). cfb-v4 + its paired probe set are preserved as durable assets — usable as an alternate-domain corpus for any non-AKD axis going forward.

---

## 6. Combined state of live hypotheses after S2.26 (with P0)

Two findings this session, P0 (desk-check) and P1 (measurement), jointly narrow the field:

- **P0 — `CELLP0_HPARAM_DIFF_OK 13/14 unexpected=[layers]`:** our config matches the EasyEdit community-standard Llama-3.2-3B MEMIT config to the byte on **13 of 14 fields** — including the two 3B adaptations we derived independently (`v_loss_layer=27`, tied `model.embed_tokens`), which is strong external validation of our 3B port. The **one** disagreement is the **layer band**: ours `[2,3,4,5,6]` vs community-standard `[4,5,6,7,8]`. Overlap only {4,5,6}; we edit {2,3} (which the standard excludes) and miss {7,8} (which it includes).
- **P1 — AKD eliminated** (this session).

**Surviving live hypotheses for the ceiling, ranked:**
1. **Layer-band placement** `[2–6]` vs `[4–8]` — now the **strongest** remaining structural candidate. It is a concrete, untested, community-flagged config disagreement on the exact model, and AKD's elimination removes its main competitor.
2. **Deeper MEMIT-on-base-Llama property** — the ceiling is real and not a config artifact (band included).

---

## 7. Decisions made

- **D-S226-BAND-1** (load-bearing, operator-ratified 2026-06-15): Primary run holds canonical `layers=[2,3,4,5,6]`. EasyEdit community-standard for Llama-3.2-3B is `[4,5,6,7,8]` — recorded as a first-class finding. **Contingency pre-committed:** Cell 13 = AKD-FAIL/PARTIAL → S2.27 arm 1 = `[4–8]` band re-run BEFORE per-layer sweep; Cell 13 = AKD-PASS → band moot. (Session never reached Cell 13; the contingency is now the **primary** S2.27 routing — see §9.)
- **D-S226-VERDICT-1:** S2.26 closes as `P1-GATE-FAIL → AKD-ELIMINATED-BY-HIGH-CONTROL`. No edit dispatched; no Block B/C. The P1-gate-FAIL routing in the runbook ("corpus revision") is **INAPPLICABLE** — authorship did not fail; the premise did. Correct routing is the operator re-interpretation branch.
- **D-S226-CFBV4-PRESERVE-1:** cfb-v4-highAKD.yaml v1.0 + probe-set-v4-highAKD.yaml v1.0 preserved as durable alternate-domain assets (not voided); reusable for non-AKD axes.
- **D-S226-S227-1:** S2.27 = `[4–8]` community-standard band re-run on cfb-v3, single-variable (band only; everything else canonical). Cheapest unruled-out explanation; eliminates the band confound before any deeper per-layer sweep.

---

## 8. Constraints established

- **C-S226-1:** AKD must be **measured (Cell P1 instrument), never assumed** from subject-domain similarity. Subject-domain clustering ≠ key clustering. Pre-flight any future MEMIT batch corpus with the Cell P1 AKD readout.
- **C-S226-2:** Any future AKD contrast requires the control corpus's AKD to be **measured first** and confirmed actually-low before a high-AKD partner can form a valid contrast. (cfb-v3 was assumed-low for two sessions; it never was.)
- **C-S226-3:** The `[4–8]` vs `[2–6]` band disagreement is an open structural confound on **all** prior ceiling axes (every one ran on `[2–6]`); it must be resolved (S2.27) before the ceiling can be called a model-family property rather than a config artifact.

---

## 9. Forward routing — S2.27

**S2.27 = T.1-β-BAND — `[4–8]` community-standard band re-run on cfb-v3 (single-variable: band only).**

Rationale: P1 eliminated AKD; P0 surfaced the band disagreement; with AKD gone, the band is the strongest cheap unruled-out explanation, and D-S226-BAND-1 pre-committed running it first. This is now the primary path, not a contingency.

Scope:
- Reuse engine (live on NV), reuse model SHA, reuse cfb-v3 + probe-set-v3.
- **Cache-extension step (~20 min):** the 5 durable caches are L2–6 only; `[4–8]` needs L7 + L8 caches. Compute 2 fresh caches (L7, L8) — same `wikipedia_stats`, 100k samples, float32 — reuse L4, L5, L6 from the existing 5. Net: 3 reused + 2 new = the `[4–8]` set.
- Hparams: canonical, with `layers=[4,5,6,7,8]` the ONLY change. 3B adaptations carry (`v_loss_layer=27`, tied `embed_tokens`).
- Single confirmatory dispatch on cfb-v3 (mirrors D-S224-BLOCKC-SKIP-1; 0/5 is established across two sessions/eight axes, so the band re-run needs one clean pass, not 15 trials, unless it surfaces movement).

**Decision matrix at S2.27 close:**
- `[4–8]` also 0/5 → band confound ELIMINATED. Ceiling is a genuine MEMIT-on-base-Llama property (9th axis; first config-variation axis). → v1.3 framework_finding amendment + deeper arms (per-layer sweep, sequential-vs-joint dispatch).
- `[4–8]` shows movement / partial / clears → the eight-axis ceiling was **partly a layer-band artifact.** Major reframe; → full `[4–8]` 15-trial establishment + v1.3 amendment ("ceiling is band-conditional").

**Deferred (unchanged):** OQ-S225-BASE-INSTRUCT-1 (base-vs-instruct, separate arm); KnowEdit external-validity (separate arm); OQ-S225-TEMPLATE-CONFOUND-1 (now moot for AKD — AKD eliminated).

---

## 10. Hypothesis-class ledger (post-S2.26)

- **AKD / key-collision conjunction (OQ-S224-LIT-1):** **ELIMINATED S2.26** — control corpus measured high-AKD; ceiling survives well-separated keys. (Was the leading mechanistic hypothesis at S2.25.)
- **NEW — Layer-band placement ([2–6] vs community-standard [4–8]):** **OPEN, now leading structural hypothesis.** S2.27 tests it.
- T.1 alt model (Llama scale): RESOLVED → ceiling generalizes 8B→3B (S2.24).
- A/B/C/D: ELIM (S2.12-A / S2.11-B / S2.13-C / S2.15-D2). T.2 ROME: ELIM S2.18. T.2 GRACE: hparam-conditional elim S2.22. T.3 alt arch: OPEN, out-of-scope WS1.

---

## 11. Block / cell execution record

| cell | surface | result |
|---|---|---|
| 0 | A | `CELL0_DEPS_OK` transformers=4.45.2 accelerate=0.34.2 torch=2.4.1+cu124; engine present; 5/5 caches present (sizes match). GPU 4090, 7968 MiB pre-resident (read-only session; no contention). |
| P0 | A | `CELLP0_HPARAM_DIFF_OK 13/14 unexpected=[layers]`. EasyEdit llama3.2-3b.yaml exact-model match found; 13 fields byte-identical incl. both 3B adaptations; band `[2–6]` vs `[4–8]` flagged. |
| P1 | B | `CELLP1_AKD_OK cfb_v3_mean=4.6203 cfb_v4_mean=4.8499 ratio=1.05 gate=FAIL`. AKD readout persisted to NV. |
| P1-VERIFY | B | `P1_VERIFY_OK 10/10` — subject-final-token sampled in every case; no off-by-one. |
| 18 | B | `CELL18_COV_INTEGRITY_OK 5/5` — caches byte-identical to S2.24 (read-only session certified). |
| 1–17, 19–20 | — | NOT REACHED — session halted at P1 gate (by design; C-S225-AKD-1). |

---

## 12. NV / environment carry-forward

- **Pod SSH target (operator-provided S2.26; reuse in all forward-session rsync/SSH commands until operator notifies of change):** host `103.196.86.67`, port `16437`, key `~/.ssh/id_ed25519`, user `root`. Direct TCP (`-e "ssh -p 16437 -i ~/.ssh/id_ed25519"`), not the RunPod gateway alias. Mirror archive tier: `/Volumes/memit/llm-database-poc-mirror/`. Forward sessions present FULL rsync/SSH commands with these values filled in (no placeholders).
- Pod `ee00aa7bcadb` warm; same instance as S2.24/S2.25. Deps intact (no reinstall). rsync present.
- Engine: `/workspace/memit_dry_run/memit` SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` (reuse; not re-verified this session — Cell 1 not reached — verify at S2.27 Cell 1).
- 5 durable 3B caches at `/workspace/covariance_caches/meta-llama_Llama-3.2-3B/wikipedia_stats/`, each 268,436,642 bytes, SHA-256 prefixes (S2.26 provenance record for S2.27 diff): L2 `7c6dafdc…` / L3 `1dd366b5…` / L4 `f5fb935a…` / L5 `cac4f814…` / L6 `1509023884…`.
- New this session on NV: `/workspace/archive/stale_subdirs/t1_alt_model_3b_memit_akd_out/akd_readout.json`; notebook `s226_t1_alpha_memit_akd.ipynb`.
- EasyEdit reference configs cached at `/workspace/easyedit_ref/` (llama3.2-3b.yaml, llama-7b.yaml) — reusable for S2.27 band cross-check.
- `reproducibility_manifest.json` to be extended with `sessions["2.26"]` (P0 diff, P1 AKD readout, P1-VERIFY, Cell 18 SHAs, verdict, no-edit certification).

---

## 13. S2.27 kickoff (successor)

**Scope:** Execution — T.1-β-BAND. Re-run cfb-v3 MEMIT on the community-standard `[4,5,6,7,8]` band, single-variable (band only), to eliminate the layer-band confound on the eight-axis ceiling.

**Entry preconditions:** `session_2_26_summary_block.md` (this) + cfb-v3.yaml v1.0 + probe-set-v3.yaml v1.0 + memit-patches-canonical v2.5 + the S2.25 runbook (structural template; Block B reused, Block PRE dropped — AKD pre-flight no longer needed). A **new thin runbook** `t1_band_4_8_runbook v0.1` should be authored at S2.27 entry (or as a pre-session authoring micro-pass) covering: engine/patch verify (Cells 1–2), cache-extension for L7+L8 (~20 min, NEW), Checkpoint #4 bit-exact gate, `layers=[4,5,6,7,8]` hparam set, single cfb-v3 dispatch, verdict surface, Copy-Unmount, manifest. Per the standing directive, Claude authors it in full.

**Execution guidance:** carry forward the operator-guidance register verbatim — zero-ML-background step-by-step, one cell at a time, label the surface, explain WHAT/WHY + expected healthy output before each cell, frame a null result as signal not failure. Claude makes all calls and proceeds; surfaces only irreversible ops for explicit confirmation.

**First pod-side step:** verify engine SHA + patch-state (Cell 1–2, not reached this session), then the L7+L8 cache extension. Everything downstream mirrors S2.24/S2.26 Block B.

---

*End S2.26 summary block.*
