# G6 / G7 — Falsifiable Pass Criteria (DRAFT for operator sign-off)
_Authored 2026-06-18. Status: **DRAFT — no runs until signed off.** This is a pre-registration: each criterion fixes metric, procedure+n, threshold+direction, justification, positive control, and pre-assigned fail-meaning BEFORE any run. Authored after `advisor()` review; the governing norm is "set falsifiable pass criteria BEFORE the result; let the numbers land."_

---

## 0. Why this document is different from CP1–G3
CP1–G3 were design-viability prototypes — *we wrote code implementing a contract and verified it implements the contract* (the [[prototype-tautology-trap]]). They pass because we built them to. **G6/G7 is the first run that can actually FAIL** and is therefore the binding falsification evidence of the whole arc.

**The specific trap at THIS stage (advisor): the anchor trap.** We have just gathered the prior numbers (T1.3 ppl 4.14→9.23, ret 100%/post_p 0.957; T2.3 8/8 multi-token). Setting each threshold "just below what we got" relocates the tautology trap into criteria-setting — a threshold tuned to pass is not falsifiable. **Every threshold below is derived from what makes the thing viable as a database per the spec, not from observed prototype output.** Each criterion carries an explicit justification; if a justification ever reduces to "about what we measured before," it is retrospective and must be replaced.

---

## 1. OPERATOR DECISION POINTS (sign-off required before any run)
These three change *which criteria apply*, so they gate the whole draft. Recommendations given; the call is yours.

> **RESOLVED 2026-06-18 (operator):**
> - **D-G6-A → pull prebuilt llama.cpp (no compile).** Verified reachable: official `ggml-org/llama.cpp` release **b9693** ships `llama-b9693-bin-ubuntu-x64.tar.gz` (CPU Linux build, contains `llama-quantize`). Quantization needs no GPU, so the CPU build suffices. Use the official GitHub release, **not** the unverified `llama-cpp.com` mirror (the quantizer runs on our edited weights → use the canonical source). → real **Q4_K_M** path is GO; G6.2 stays a Q4_K criterion.
> - **D-G6-B → Qwen3-1.7B or 4B** (exact pick on cov-compute cost, confirmed before paying it).
> - **D-G6-C → characterization** (report bytes/record scaling; no budget gate).

### D-G6-A — Real Q4_K tooling fork
**The gap:** `llama.cpp`/`llama-quantize` is not installed anywhere on the pod. LARQL `convert quantize` self-documents *"FP4 is the only format wired as of exp 26; Q4K … land as additional subcommands"* — LARQL can **ingest** a Q4_K GGUF (`gguf-to-vindex`) but cannot **produce** Q4_K. T1.3's 4-bit number used a **crude sim quantizer** (round-trip), explicitly flagged as not real Q4_K.
- **Option 1 (RECOMMENDED):** build `llama.cpp` for genuine `Q4_K_M` GGUF → LARQL `gguf-to-vindex` ingests → serve/probe on CPU. Cost: ~10–20 min build (cmake + build deps already present). Gives the real deployment-format claim G6 is meant to test.
- **Option 2:** use LARQL's wired **FP4** as the low-bit proxy. Cheaper (no build) but it is **not Q4_K** — calling FP4 "Q4_K" would undermine the falsification. If chosen, the criterion is renamed to FP4 and the Q4_K claim stays UNTESTED.
- **Why it matters:** the two options produce *different criteria*. Do not let FP4 silently substitute for Q4_K.

### D-G6-B — Which "larger Qwen3", and is the cost worth it
**The gap:** only Qwen3-0.6B is cached locally (band [4-8] cov ready). A larger Qwen3 (1.7B / 4B / 8B) needs model download + **~hours** of covariance computation (no cache).
- **Tension to resolve, not bury:** memory [[deployment-target-intel-cpu]] says the end product runs on the operator's **local Intel CPU** (favors small models); the bootstrap says deployment is **TBD / maybe remote GPU** (a larger model is then fair game). *Which model is the right "scale" proxy depends on this.*
- **RECOMMENDED:** Qwen3-1.7B or 4B as the scale step — large enough to test whether the [4-8] recipe and many-overlay behavior hold above 0.6B, small enough to stay CPU-plausible. Confirm the target before paying the cov-compute cost.

### D-G6-C — Overlay-size: gate or characterization?
The 81MB band-dense overlay (single, rank-~6 ΔW) is only a *gate* if there is a budget to fail against (e.g., "≤ X MB for N records on the CPU target"). Without a budget it is a **characterization** (measure + report scaling).
- **RECOMMENDED:** give a CPU-deployment storage budget if you have one; otherwise we label G6.3 a characterization and report bytes/record scaling honestly (no measurement masquerading as a pass).

---

## 2. G6 — Efficiency / Scale criteria

### G6.1 — Scale-of-N many-overlay accumulation  ⭐ THE CENTERPIECE GATE
> **RESULT 2026-06-18 → SPLIT (`CORPUS/13`, `g6_scale_n.py`).** Qwen2.5-3B, N=100 (50 entities × 2 fields). ✅ Write-side PASS: retention 98% @ N=100, apply-time expression 100% through record 100, within-entity 95.6%, global 98.4%. ❌ Cross-entity consistency FAIL: held-out top-1 correctness on the edited relation collapses 100→91.7→58.3→41.7% (baseline→N26→N50→N100) — relation-specific, scale-amplifying read corruption. Falsifies "cross-entity-clean at scale" for subject-keyed AlphaEdit. The pre-registered "cross-entity ≥ baseline−5" bar was apples-to-oranges (within-entity n=2 baseline); the monotonic top-1 collapse is the binding evidence.
> _The defining property of a database is holding **many** records and retrieving **any** of them. We have proven single edits and sequential **pairs** (Qwen-7B 100% / 3B-AlphaEdit 100% on n=2). N-record accumulation is where the LLM-as-DB thesis holds or breaks — it is the strongest available falsifier, so it is the gate that matters most._

- **Metric:** (a) all-record retention = fraction of all N edited facts still correctly returned (top-1) after all N edits applied; (b) untouched-locality = top-1 stability of a held-out never-edited probe set.
- **Procedure + n:** edit a committed **staircase N = 25 → 50 → 100** distinct (entity, attribute) records (batched-per-record compile, in-solve AlphaEdit thresh 0.005). After each rung, probe **every** edited record + the untouched probe set. Pre-commit the entity/attribute list. (Headline N=100; staircase exposes the degradation point if any.)
- **Threshold + direction:** PASS = all-record retention **≥ 98%** at N=100 **AND** retention does **not** trend down across the staircase (slope ≥ −1 pt/rung), **AND** untouched-locality ≥ the established baseline (3B-AlphaEdit 80.7% / 7B 79%) minus 5 pts.
- **Justification (viability, not anchor):** a store that silently drops records is not a database; the bar is near-total retention, and the discriminating question is whether it *degrades with N* (a capacity ceiling). 98% is the "data-loss is rare and bounded" line for a viability claim, not a tuned-to-pass value.
- **Positive control:** the untouched probe set isolates "scale drift" from "edit failure" — if untouched facts also degrade, the loss is global interference, not record-count.
- **Fail-meaning:** if retention falls with N (e.g., 100→90→70%), the in-weight store has a **capacity ceiling** → the spec's "database" claim carries an undocumented scale bound that must be surfaced (→ spec amendment + compaction/§8.10 re-examination).

### G6.2 — Real low-bit quantization survival (Q4_K per D-G6-A)
- **Metric:** edited-fact retention + post_p after real Q4_K quantization, **measured against native-fact retention through the same quantizer** (the positive control IS the metric).
- **Procedure + n:** quantize the compiled edited model to real Q4_K_M; probe (i) ≥20 edited facts and (ii) ≥20 comparable **native** facts (same attribute types, never edited) through the same quantizer. Same prompts pre/post.
- **Threshold + direction:** PASS = edited-fact retention **≥ native-fact retention − 3 pts** (edits survive quantization *as well as* native knowledge).
- **Justification:** the real claim is "edited knowledge is indistinguishable from native knowledge under deployment quantization." Comparing to native-through-same-quantizer (not to fp16, and emphatically not "ppl rose less than the crude sim" — that is guaranteed and uninformative) is what tests it.
- **Positive control:** native facts through the same quantizer (built into the metric).
- **Fail-meaning:** if edited facts degrade materially more than native facts, the overlay is **quantization-fragile** → edited layers need higher precision, or the CPU-Q4_K deployment story breaks → D1/G5 constraint.

### G6.3 — Overlay size scaling (characterization unless D-G6-C sets a budget)
- **Metric:** overlay bytes **per record** as N grows; is footprint **O(1)** (band-dense, fixed ~81MB regardless of N) or **O(N)** (grows per record)?
- **Procedure + n:** reuse the G6.1 staircase (25/50/100); record overlay size at each rung.
- **Threshold:** *characterization* — report the scaling curve. **Becomes a gate** only if D-G6-C supplies a budget (then PASS = size ≤ budget at N=100).
- **Justification:** CPU deployability depends on whether the store stays bounded as records accumulate. O(N) growth at the band-dense 81MB/overlay rate would be prohibitive; O(1) shared-band is the viable shape.
- **Fail-meaning (if budget given):** exceeds budget → needs low-rank overlay compression before CPU deployment.

### G6.4 — C15 layer-band comparison (feeds the spec; NOT a recipe gate)
> _Per CP3: our band **[4-8]** works empirically yet contradicts C15's **L15-25 for 32 layers** under any charitable scaling. This is a comparison that feeds OQ-W2, not a pass/fail of our recipe._

- **Metric:** locality (same-entity + cross-entity) + retention + expression, edited at **[4-8]** vs a **C15-scaled mid-late band on the same model** (e.g., depth-scaled ≈ L13-22 for 28L / L17-28 for 36L).
- **Procedure + n:** same fixed stimulus set, two band configs, same model; head-to-head.
- **Outcome (no threshold — both publishable):**
  - [4-8] strictly better → **C15 needs small-model recalibration** (feeds OQ-W2 / spec amendment).
  - mid-late ≥ [4-8] → our band was an artifact; switch to the C15-scaled band.
- **Positive control:** empty-edit inertness floor (already proven in s243e) confirms the comparison isn't measuring harness noise.
- **Fail-meaning:** N/A (comparison). The binding output is a directional finding for the spec.

### G6.5 — Larger-model relation-label quality (characterization; carried from G4)
- **Metric:** usability of LARQL decompiler relation labels on the larger model (cleaner clusters? fewer than the 24,469 emergent labels seen at 0.6B?).
- **Procedure:** `larql describe` / relation-cluster inspection on the larger model's vindex.
- **Threshold:** characterization — report. Feeds the schema layer (G3 contracts).

---

## 3. G7 — Multi-token value robustness

### G7.0 — Diagnose the Hanoi→"H" failure FIRST  (gating prerequisite)
> _T2.3 already got multi-token capital expression **8/8** — re-running that is a test we built to pass. But a partial-expression failure was observed (Spain "Hanoi"→"H"). We cannot set a meaningful robustness threshold without knowing the failure mode._

- **Procedure:** reproduce Hanoi→"H", then vary **one axis at a time** against the working 8/8 cases: (i) token-length of the value, (ii) value rarity/frequency, (iii) entity identity, (iv) v_loss / expression-strength hparams.
- **Output:** a named failure mode (e.g., "values ≥k tokens truncate" or "rare-token values under-express"). **This determines G7.1's value grid and threshold.**

### G7.1 — Multi-token robustness on a HARDER set than T2.3
- **Metric:** **full-value expression rate** = fraction of values where *all* tokens are emitted (not just the first) AND the value is retained after subsequent edits.
- **Procedure + n:** build a value set **deliberately harder than T2.3** — committed grid of ≥24 values spanning token-length (2/3/4/5 tokens) × frequency (common/rare), across ≥6 entities; thresholds and grid fixed before running, informed by G7.0.
- **Threshold + direction:** PASS = full-value expression **≥ 95%** across the grid, with **no systematic collapse** in any one length/frequency cell (no cell < 80%).
- **Justification:** a database that stores "Ouagadougou" must return "Ouagadougou", not "O". Full-value fidelity ~100% is the viability line for a value store; we test whether it holds as values get longer/rarer — the property T2.3's easy set could not stress.
- **Positive control:** single-token values (known-good) in the same run — confirms the harness expresses at all.
- **Fail-meaning:** if long/rare values truncate, the in-weight store has a **value-complexity bound** → multi-token values need a different mechanism (value-as-sequence / multi-edit decomposition) → spec value-model amendment.

---

## 4. Positive controls — mandatory, not optional (the CP2 lesson)
_CP2 taught that without a positive control we mistook "no capability" for a result (LARQL couldn't read back even a **native** fact). Every G6/G7 criterion carries one:_

| Criterion | Positive control |
|---|---|
| G6.1 scale-of-N | untouched never-edited probe set (isolates scale-drift from edit-failure) |
| G6.2 quantization | native-fact retention through the *same* quantizer |
| G6.4 C15 band | empty-edit inertness floor (s243e) |
| G7.1 multi-token | single-token value (known-good expression) |

---

## 5. What G6/G7 can falsify (the binding statement)
- **G6.1 fails** → in-weight store has a record-capacity ceiling; "database" claim is scale-bounded.
- **G6.2 fails** → edits are quantization-fragile; CPU-Q4_K deployment story breaks.
- **G6.4** → either C15 is miscalibrated for small models (spec amendment via OQ-W2) or our [4-8] band is an artifact.
- **G7.1 fails** → in-weight values have a complexity bound; multi-token storage needs a different mechanism.

These are pre-assigned consequences. "Let the numbers land" has teeth only because failure already has a meaning.

---

## 6. Sign-off checklist (operator)
- [ ] **D-G6-A** Q4_K tooling: build llama.cpp (rec.) / use FP4 proxy / defer
- [ ] **D-G6-B** larger model: Qwen3-1.7B / 4B / 8B / stay at 0.6B — and accept ~hrs cov-compute cost
- [ ] **D-G6-C** overlay-size: storage budget (→ gate) or characterization
- [ ] N staircase for G6.1 (proposed 25/50/100) approved or adjusted
- [ ] Thresholds (G6.1 ≥98% / G6.2 native−3pts / G7.1 ≥95%) approved or adjusted
- [ ] Confirm: no runs launch until this is signed
