# Session 2.24 — Summary Block

**Session type:** Execution (Block-and-Cell runbook; T.1-α-MEMIT)
**Predecessor:** S2.23 (T.1-α-MEMIT runbook v0.1 authoring)
**Runbook consumed:** `t1_alt_model_3b_memit_runbook_v0_1.md` (875L)
**Closed:** 2026-06-15
**Verdict:** `FAIL_WITH_INSTALLATION` — Cell 13 `ROUTE_A`
**Target:** `meta-llama/Llama-3.2-3B` fp16, RunPod RTX 4090 24 GiB, NV `large_amethyst_wolverine`

---

## 1. The verdict — what S2.24 established

**MEMIT at canonical hparams on Llama-3.2-3B produced 0/5 consistency.** The architectural-invariant ceiling — confirmed across seven orthogonal axes on Llama-3.1-8B — **generalizes across Llama-class scale (8B → 3B).** It is NOT 8B-specific.

This is the **8th axis** on the ceiling, and the **first to vary the model** (prior seven varied hparams / corpus / target / probe locus / layer-set / write-engine). The ceiling held.

**Per-fact consistency surface (canonical prompt, post-edit):**

| fact | target | pre P(tgt) | post P(tgt) | top-1 now | consistency |
|------|--------|-----------|------------|-----------|-------------|
| cfb-v3-001 | guitar | 0.000224 | 0.000781 | 279 (" the") | FAIL |
| cfb-v3-002 | piano  | 0.000018 | 0.000005 | 813 (" his") | FAIL |
| cfb-v3-003 | violin | 0.000081 | 0.000089 | 279 | FAIL |
| cfb-v3-004 | harp   | 0.000221 | 0.000553 | 279 | FAIL |
| cfb-v3-005 | flute  | 0.000018 | 0.000662 | 279 | FAIL |

**The seven-axis fingerprint reproduced exactly:** `compute_z` internal objective improved ~40,000× per fact (e.g. guitar avg-prob `1.4e-08 → 5.5e-04` over 25 steps) while external P(target) at the canonical prompt barely moved (guitar `2.2e-04 → 7.8e-04`); top-1 never became the target. z_error ~4.5–5.1/layer; upd_norm 0.40–1.34 vs orig_norm ~86–90. Huge internal progress, four-orders-of-magnitude external miss — the ceiling's defining signature.

**Trustworthiness:** Checkpoint #2 bit-exact gate PASSED at Cell 5 — drift `0.00e+00` across 38 probes, 0 top-1 mismatches. Cross-engine determinism (GRACE→MEMIT) proven. The 0/5 is the model, not noise.

---

## 2. CRITICAL rigor caveat (load-bearing for interpretation)

The 0/5 was obtained on the **low-AKD corpus** (cfb-v3: 5 clustered athletes, identical template `{} plays the instrument of`). Per the four-paper literature review (§5), low AKD — Average Keys Distance at the edit layer — is a **known MEMIT stress condition**, not a neutral test bed.

**Therefore:** 0/5 proves the ceiling **generalizes across scale UNDER low-AKD conditions.** It does **NOT** disentangle:
- (a) a **model-family ceiling** (MEMIT fundamentally can't edit base Llama), from
- (b) a **low-AKD-corpus ceiling** (MEMIT can't edit *this kind of corpus* on Llama, but could on high-AKD).

Both 8B and 3B failed on the *same* low-AKD corpus. The discriminating experiment — MEMIT on a **high-AKD** corpus (KnowEdit) — is the single most valuable successor question. See OQ-S224-LIT-1.

This caveat does not weaken the result; it states its precise boundary. The finding is "ceiling generalizes across Llama scale on low-AKD corpora," which is sharper and more defensible than "Llama is uneditable."

---

## 3. Decisions made

- **D-S224-VERDICT-1:** S2.24 verdict = `FAIL_WITH_INSTALLATION`, Cell 13 `ROUTE_A`. Ceiling generalizes across Llama-class scale (8B→3B). 8th axis; first model-variation axis.
- **D-S224-BLOCKC-SKIP-1:** Block C 15-trial loop SKIPPED per Route A. A 0/5 single-dispatch dry-run needs no replicates; 15 trials would reproduce 0/5 at compute cost, zero information gain. Single-dispatch surface recorded as the verdict.
- **D-S224-CALIB-1 (resolves OQ-S222-CALIBRATION-CRITERIA-MISMATCH-1):** The generalization predicate is runbook §3.2.2 `max(gen_p_target_new) > 0.3` (a transfer/movement test) — this is CANONICAL. The `probe-set-v3.yaml` §126 `drift < 0.05` predicate is a mislabeled LOCALITY predicate and is SUPERSEDED for generalization purposes. Rationale: generalization must measure transfer (does the edit move related probes?), not stability; locality/stability is already covered by the specificity + unmount probes. Verdict ratification was gated on this reconciliation per the runbook; now closed.
- **D-S224-ADAPT-1:** Three 3B-vs-8B model-structure adaptations applied, all benign (structural, NOT hparam tuning):
  1. `v_loss_layer`: 31 → **27** (3B has 28 layers; last-layer index for the tied loss objective).
  2. `lm_head_module`: `"lm_head"` → **`"model.embed_tokens"`** (3B `tie_word_embeddings=True`; `lm_head.weight` is not a named parameter — tied to `embed_tokens.weight`. compute_z only reads this weight; using the tied source is mathematically identical, read-only, no side effects).
  3. Covariance caches recomputed fresh for 3B (8B caches are architecture-keyed and useless for 3B).
  All other hparams verbatim from `hparams/MEMIT/Llama-3.1-8B.json` (layers [2-6], mom2_update_weight=15000, v_lr=0.5, v_num_grad_steps=25, kl_factor=0.0625). Scale test integrity preserved.

---

## 4. Constraints established

- **C-S224-1:** Llama-3.2-3B uses tied input/output embeddings (`tie_word_embeddings=True`). Any write-engine touching the lm_head on 3B (or other small Llama models) must target `model.embed_tokens`, not `lm_head`. Carry-forward for any future 3B engine work.
- **C-S224-2:** `v_loss_layer` is model-architecture-dependent (= last layer index = n_layers − 1). 3B = 27, 8B = 31. Must be set per-model in any cross-model runbook.
- **C-S224-3 (Copy-Unmount 4th-config validation):** Copy-Unmount bit-exact validated on MEMIT-3B L2-L6: weight `max_abs_diff = 0.00e+00` (all 5 layers); IC-S23-4 probe gate PASS, post-unmount P(target) == pre-edit P(target) to full precision (drift `0.00e+00`, all 5 facts). Now validated across 4 write-engine configs: MEMIT joint-overlay L4-L8 → L2-L6 → ROME single-fact → MEMIT-3B L2-L6.
- **C-S224-4 (cov-cache reuse):** The 5 fresh 3B cov caches (`/workspace/covariance_caches/meta-llama_Llama-3.2-3B/wikipedia_stats/`, each 268,436,642 bytes, (8192,8192) float32, SHA-verified intact post-session) are a durable, reusable NV asset. Any successor high-AKD experiment on Llama-3.2-3B at L2-L6 reuses these directly (~45 min compute saved). MEMIT is read-only on them; integrity confirmed CELL18 5/5.

---

## 5. Literature integration (four papers + EasyEdit, operator-surfaced)

Four independent groups, all editing Llama-class models with MEMIT, converge on a coherent picture:

1. **MEMIT-Merge (arXiv 2502.07322):** MEMIT derives its "key" from the subject; when batched facts have near-identical keys (low **AKD** = Average Keys Distance at the edit layer), the linear layer is forced to map near-identical inputs to divergent values → efficacy collapse. **Same template → low AKD → collapse, even with distinct subjects.** Efficacy is a measurable function of AKD. On *distinct-subject / high-AKD* Llama-3-8B-Instruct, vanilla MEMIT hits ~0.99.
2. **MEMOIR (arXiv 2506.07899):** treats MEMIT-on-Llama-3-8B as a *working* baseline; the problem it solves is *sequential* forgetting, not basic editability.
3. **EasyEdit (github.com/zjunlp/EasyEdit, MIT license):** maintained unified harness implementing MEMIT/ROME/r-ROME/EMMET/GRACE/AlphaEdit/WISE/PMET across Llama/Mistral/Qwen. Ships canonical Llama MEMIT hparams. Reports MEMIT-on-Llama-2-7B Reliability ~93. KnowEdit = high-AKD benchmark corpus.
4. **Berkeley batch-size (arXiv 2405.00664):** step-by-step MEMIT-on-Llama-3 tuning guide. Big batches degrade MORE than equal-count sequential edits; provides an empirical Llama-3-8B optimal-layer sweep recipe + appendix hparams.

**Convergent signal:** MEMIT works on Llama when (a) the edit layer is well-chosen, (b) keys are well-separated (high AKD), and (c) edits are sequential or small-batch. WS1's setup stacks three known stress conditions: **5-fact joint batch × low-AKD clustered corpus × inherited [2-6] layer band.**

**Caveat on all four:** they use *Instruct* models; WS1 target is *base* Llama-3.1-8B / Llama-3.2-3B. Base-vs-instruct editability differs and is an open confound since S2.5a — must be controlled in any cross-comparison.

---

## 6. Open questions (deferred to S2.25+)

- **OQ-S224-LIT-1 (PRIMARY — most decisive):** The architectural-invariant ceiling may resolve into a conjunction of *testable* conditions: (a) low-AKD clustered corpus [cfb-v3 is low-AKD by design], (b) joint-batch vs sequential dispatch, (c) inherited [2-6] band vs empirically-swept optimal layer. Discriminating experiments, in priority order:
  1. **Compute AKD on cfb-v3 facts at the edit layer** — cheap, immediate; quantifies whether cfb-v3 is in fact low-AKD (predicted: yes, near-0).
  2. **MEMIT on a high-AKD KnowEdit slice** — THE decisive experiment. If MEMIT clears the band on KnowEdit where cfb-v3 fails, the ceiling localizes to *corpus AKD*, not the model → the "LLM-as-database" thesis gets a clear path forward (use well-separated keys).
  3. **Per-layer sweep on Llama-3.2-3B** following the Berkeley recipe — tests whether [2-6] is even the right band.
  4. **Sequential vs joint dispatch** — tests the batch-interference axis.
- **OQ-S224-EASYEDIT-1:** Evaluate EasyEdit as (a) hparam-config oracle (diff its `hparams/MEMIT/llama-*.yaml` against canonical config — resolves OQ-S224-2), (b) KnowEdit high-AKD corpus source, (c) T-branch alternative-engine shelf (AlphaEdit / WISE / EMMET / r-ROME). **Strategic-fit boundary:** write-engine *substrate* only, NOT harness replacement — EasyEdit has no `.vindex` / Copy-Unmount / State-Ledger equivalent. Use as cross-check oracle + component shelf, not infrastructure swap (would orphan the hand-patched `kmeng01/memit` provenance chain).
- **OQ-S224-2 (carried):** Is the inherited canonical config (layers [2-6], mom2_update_weight, etc.) even correct for Llama? EasyEdit's published Llama hparams are the de-facto community standard to diff against. Near-zero-cost check.
- **OQ-S224-BASE-INSTRUCT-1 (carried from S2.5a):** All four papers use Instruct models; WS1 uses base. Base-vs-instruct editability confound must be controlled before importing any literature success claim as contradictory to the WS1 ceiling.

---

## 7. Hypothesis-class ledger (post-S2.24)

- **T.1 alt model (Llama-class scale): RESOLVED → ceiling generalizes 8B→3B** (this session; under low-AKD caveat per §2).
- **A (corpus locus):** ELIM S2.12-A
- **B (probe locus):** ELIM S2.11-B
- **C (target shift):** ELIM S2.13-C
- **D (layer-set):** FULLY ELIM S2.15-D2
- **T.2 ROME:** ELIM S2.18 (canonical hparams)
- **T.2 GRACE:** hparam-conditional elimination S2.22 (discriminator gate non-firing at canonical params)
- **NEW — AKD/key-collision conjunction (OQ-S224-LIT-1):** OPEN, PROMOTED to leading mechanistic hypothesis. Literature-backed, cheaply testable, and — if confirmed — reframes the entire ceiling as corpus-structural rather than model-invariant. **This is the highest-value open thread in the workstream.**
- **T.3 alt arch (Mistral/Qwen):** OPEN, out-of-scope WS1.

---

## 8. NV / environment state at close

- Pod container `ee00aa7bcadb`; RTX 4090 24 GiB; transformers 4.45.2 / accelerate 0.34.2 / datasets 4.8.3.
- MEMIT engine SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` (reused from NV `/workspace/memit_dry_run/memit`, patched in place).
- 5 fresh 3B cov caches on NV (1.3 GiB total; SHA-verified intact).
- `reproducibility_manifest.json` extended with `sessions["2.24"]` entry.
- Model restored to pristine pre-edit state (Copy-Unmount bit-exact); no residual edits on NV.
- Peak edit-dispatch VRAM 8.41 GiB (well under 24).

---

## 9. Operator-guidance register (carry-forward for execution sessions)

**This is load-bearing for how the successor agent should run S2.25.** The operator (Robert) is a senior technical architect by background and communicates at that register in scoping/authoring sessions — but for **execution sessions like S2.24/S2.25, he explicitly requested zero-ML-background, step-by-step hand-holding.** The two registers coexist; match the one the session calls for.

**Execution-session guidance pattern (what worked in S2.24):**
- **One cell at a time.** Give exactly one runbook cell, wait for the paste-back, read the result, then give the next. Never batch cells ahead.
- **Label the surface every time.** `Surface A` = pod terminal (SSH); `Surface B` = JupyterLab notebook. State it in every instruction so the operator knows where to run.
- **Explain WHAT each cell does and WHY before he runs it**, in plain terms — ground every ML concept (covariance cache, compute_z, AKD, tied embeddings, bit-exact unmount) the first time it appears. Concrete analogies land well.
- **State the expected healthy output before he runs it**, so he can recognize success vs failure himself rather than guessing. Name the specific gate string (`CELL8_COV_FRESH_OK 5/5`, etc.) and what a halt would look like.
- **Verify, don't assume.** The session's clean run came from reading actual structure before acting: `inspect.signature` on the MEMIT API, reading the real hparams JSON, inspecting `orig_weights` keys, checking `pre_edit` dict keys before the gate. Three model-structure traps (`v_loss_layer`, tied `lm_head`, dict key names) were caught BEFORE dispatch this way, not after a crash. Continue this discipline — guess-and-crash wastes operator time and erodes trust.
- **Frame failures as informative, not as session failures.** The 0/5 verdict is a successful test. Set that expectation honestly BEFORE the result lands so a null result reads as signal, not disappointment.
- **Surface load-bearing/irreversible decisions; recommend-and-proceed on the rest.** Standing instruction: *"Your recommendations will always be accepted. Always assume this."* So: make the call, state it, proceed — but flag anything irreversible (verdict ratification, skipping Block C, destructive ops) for explicit confirmation first.
- **Honor the operator's domain expertise on judgment calls** even while hand-holding the mechanics. He retains ratification authority; defer routing/branching to recommendation but let him ratify. He corrects path/command errors tersely and moves on — accept the correction without over-apologizing.
- **No hedging, no preamble, high signal-to-noise** even within the hand-holding. Step-by-step ≠ verbose. Each step is tight.

---

## 10. S2.25 kickoff (successor)

**Recommended scope:** T.1-α-MEMIT-AKD — the discriminating experiment for OQ-S224-LIT-1. Reuses the S2.24 3B setup (model, engine, the 5 durable cov caches) and adds a **high-AKD corpus** path to separate model-family ceiling from low-AKD-corpus ceiling.

**Pre-session decisions to surface before authoring:**
1. **Corpus source:** author a high-AKD variant of cfb (varied subjects, varied templates, distinct domains) vs adopt a KnowEdit/ZsRE slice directly. KnowEdit is the literature-standard high-AKD benchmark; a hand-authored variant preserves the instrument-target structure for continuity. Operator decision.
2. **AKD instrumentation:** add an AKD-compute cell (pairwise Euclidean distance of subject-last-token keys at the edit layer) as a pre-flight diagnostic on BOTH cfb-v3 (predicted low) and the high-AKD corpus (predicted high) — quantifies the independent variable.
3. **Base-vs-instruct control:** decide whether S2.25 also runs an Instruct-model arm to control OQ-S224-BASE-INSTRUCT-1, or defers it.
4. **EasyEdit hparam diff (OQ-S224-EASYEDIT-1 part a):** cheap pre-flight — diff EasyEdit's Llama MEMIT hparams against canonical config before committing the run.

**Entry preconditions:** S2.24 summary (this doc) + `t1_alt_model_3b_memit_runbook_v0_1.md` + `memit-patches-canonical.md v2.5` + corpus/probe artifacts. The 3B cov caches and engine are live on NV (no re-clone, no recompute for L2-L6).

---

## 11. Mirror-sync commands (operator, post-session)

**PREREQUISITE (discovered S2.24):** fresh RunPod images ship WITHOUT rsync. rsync needs the binary on BOTH ends; the MBP has it, the pod does not → `remote command not found (code 127)`. Install on the pod first (durable; persists for the pod's life):

```bash
# On the POD (Surface A / SSH or RunPod web terminal) — one-time per pod
apt-get update -qq && apt-get install -y rsync
```

Then pull from the MBP (rsync = standard two-tier workflow with hf_cache exclude):

```bash
# From MBP — pull S2.24 manifest to durable archive tier (D-S210-6 two-tier discipline)
# rsync uses direct TCP via -e, NOT the RunPod gateway alias
rsync -avz --exclude 'hf_cache' \
  -e "ssh -p 16437 -i ~/.ssh/id_ed25519" \
  root@103.196.86.67:/workspace/reproducibility_manifest.json \
  /Volumes/memit/llm-database-poc-mirror/
```

**Fallback if rsync install is undesirable** — scp ships with OpenSSH, already present both ends. NOTE: scp uses capital `-P` for port (rsync/ssh use lowercase `-p`):

```bash
scp -P 16437 -i ~/.ssh/id_ed25519 \
  root@103.196.86.67:/workspace/reproducibility_manifest.json \
  /Volumes/memit/llm-database-poc-mirror/
```

Save this summary block locally (download from outputs; pod cannot see `/mnt/user-data/outputs/`):
```bash
mv ~/Downloads/session_2_24_summary_block.md /Volumes/memit/llm-database-poc-mirror/
```

SHA-256 spot-check (standard post-sync verification; `shasum` is NOT aliased on MBP):
```bash
ssh -p 16437 -i ~/.ssh/id_ed25519 root@103.196.86.67 \
  "sha256sum /workspace/reproducibility_manifest.json"
shasum -a 256 /Volumes/memit/llm-database-poc-mirror/reproducibility_manifest.json
# the two hashes must match
```

**Notes:**
- `setlocale: LC_ALL: cannot change locale` warning on the pod is cosmetic (locale env unset); harmless. Silence with `export LC_ALL=C` on the pod if desired.
- Pod host/port `103.196.86.67 -p 16437` is valid only if the pod has not restarted since S2.24. If cycled, pull the current SSH target from the RunPod console and substitute.
- Cov caches (1.3 GiB) are working-tier (regenerable); NOT mirrored by default per D-S210-6. They reuse in-place on NV for S2.25.

**Security hygiene reminder (carried from session):** rotate the RunPod API key and ntfy URL pasted in chat earlier this session.

---

*End S2.24 summary block.*
