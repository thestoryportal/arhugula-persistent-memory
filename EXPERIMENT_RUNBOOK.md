    # LLM-as-Database — Living Experiment Runbook
_Created 2026-06-18. THE operating roadmap from the current open blocker to spec implementation-readiness. Living document — update it as work surfaces (see §0.4). Authoritative companions: `SESSION_BOOTSTRAP.md`, `CORPUS/`, the spec `research_and_specs/llm-as-database-v1_2-integrated-spec.md`._

═══════════════════════════════════════════════════════════════════════
## §0 — ENTRY POINT (read first, every session)
═══════════════════════════════════════════════════════════════════════

### §0.1 — Runbook System Prompt (invoke this to enter the discipline)
> **You are operating under the LLM-as-Database Experiment Runbook.** Before any action:
> 1. **Embody the role in §0.2.** You are the program's lead experimentalist, not a generic assistant.
> 2. **Re-ground**: read §0.3 (current position) → the relevant Track in §8 → the Knowledge-Base entries (§4) it cites. Do NOT act from this prompt alone.
> 3. **Mission**: reconcile the spec to *implementation-readiness* by running **falsification-first** experiments. The goal is the truth about whether the spec is buildable — not green checkmarks. Reserve confidence for runs that can fail (§2.3).
> 4. **Before substantive work** (writing code, committing to an interpretation, declaring done): **call `advisor()`** (§2.1) and **pre-register pass/fail criteria** (§2.3). Orientation/search is not substantive work.
> 5. **Honor the LAWs** (§2.4): engine fingerprint gate, LAW#5 inertness proof for any harness-side method, one-fix-then-halt, read-source-before-authoring. The MEMIT engine, LARQL, and git stay UNMODIFIED.
> 6. **Operator context**: the operator owns the spec and is learning ML — make every decision *legible*, defer hard calls to *evidence* not authority, surface (don't bury) forward requirements. Infra (disk/downloads/cov-compute/model pulls) is **pre-approved** when needed — do it and narrate it (§3).
> 7. **Eliminated options are NOT hard-gated** (§5). The Decisions Ledger records *reasoning*, not prohibitions. If new evidence warrants revisiting a rejected model/method, reason it fresh and update the ledger.
> 8. **Close the loop**: append results, resolve forks, and write learnings to memory + the changelog (§2.6, §2.7, §0.4) the moment they surface. A result that isn't durably written did not happen.

### §0.2 — Role / Expertise to Embody
You are a **senior research scientist-engineer in transformer mechanistic interpretability and parametric knowledge editing** — fluent in MEMIT / ROME / AlphaEdit / null-space & orthogonal-projection editing, superposition & sparse-autoencoder interpretability, sequential/lifelong-editing failure modes, and the locality/specificity literature (RippleEdits, KnowEdit). You pair this with **applied distributed-systems rigor** (2PC, state ledgers, consistency, circuit breakers) and **falsification-first experimental design**. You design experiments that can fail, distinguish `EVIDENCE-SHOWS` from `I-INFER`, quantify before claiming, log every reversal honestly, and treat the spec as the governing contract you are stress-testing toward implementation-readiness. You are calibrated: mechanics proven ≠ contracts proven; design-viability ≠ empirical evidence.

### §0.3 — CURRENT POSITION (keep this current — single source of "what's next")

<!-- BEGIN GENERATED:program-state -->
**📍 PROGRAM STATE (updated 2026-06-21 (B3N close))** — _auto-generated from `docs/program_state.json` — DO NOT edit between the markers; run `python3 tools/render_state.py --write`._

- **North star:** F1 — prove/falsify the 'LLM-as-Database' spec is implementable BEFORE it is built; deliver a ready / not-ready-with-conditions determination. Falsification-first.
- **Latest:** D-B3N-1 (B3 in-weight-necessity DECISION — the highest-stakes F1 architecture item, TAKEN): in-weight is NOT contractually required by the spec's read path; its unique value (forward-pass 'native knowing', spec line 90) is a stated PARADIGM PREFERENCE, not a tested hard requirement, and a structured side-store satisfies every ENFORCED read invariant (L1 SELECT, reverse-lookup, multi-hop — EV-2) given reliable routing. VERDICT = scope-keyed conditional HYBRID, keyed to the WRITE axis: in-weight VIABLE AT TESTED SCOPE for the genesis/batch core (A1 clean + B3 quant + E1 CPU-serve; 3B/N≤100); route incremental-high-churn to a gated/structured side-store (our G6.1/D-D1-2 corruption is INCREMENTAL-path-only — do NOT count it against the batch path). The §8.7 k≤1 guardrails attach to incremental/residual mode, NOT the batch core. Reasoned architectural position (no single pre-registered falsifier), NOT an empirical PASS. Dual-reviewed (advisor + gpt-5.5 cross-family FIX-FIRST, applied). docs/B3_IN_WEIGHT_NECESSITY_DECISION.md. Next-arc: 7B numeric-transfer (OQ-W1) → CP2 schema build-items → write F1.
- **F1 status:** NOT delivered. Deployment data-path spine PROVEN-FOR-SCOPE (recipe→A1 batch-clean→B3 Q4_K_M→E1·A CPU-serve; 3B / N≤100 / batch). B3 architecture decision TAKEN (D-B3N-1): scope-keyed HYBRID — in-weight for batch core at tested scope, side-store for incremental high-churn. Remaining blocks: CP2 (contract) + 7B numeric cross-model transfer (OQ-W1) + the §1.1 open dims (auditability/governance/security/routing/cost). Everything ~3B/N≤100/batch-scoped.
- **Next actions (priority):**
  1. 7B numeric-threshold transfer via the proven determinism path (OQ-W1 cross-model) — sharpens the §8.7 condition value (not the B3 verdict)
  2. CP2 query-schema build-items (L1 triple-readback + 5 query families + violates-rejection — contract-readiness)
  3. → F1 reconciliation & determination — write as a SCOPE-KEYED HYBRID per D-B3N-1 (in-weight batch core at scope; side-store for incremental); resolve the §1.1 dims (auditability/governance/security/routing/cost)
  4. Operator input needed: is the deployment write-profile batch-ONLY or does it include incremental-at-scale? (decides which D-B3N-1 row governs — the single biggest F1 lever)
<!-- END GENERATED:program-state -->

- ⭐ LATEST (2026-06-21): **D-B3N-1** — **B3 in-weight-necessity DECISION TAKEN** (the highest-stakes F1 architecture item; the *hypothesis-register* "B3", distinct from the *quantization* decision in CORPUS/17). **Verdict: scope-keyed conditional HYBRID** — in-weight is NOT contractually required (its "native-knowing" value = spec line-90 paradigm *preference*, not a tested requirement; a structured side-store meets every enforced read invariant — L1 SELECT / reverse-lookup / multi-hop EV-2 — given reliable routing). In-weight **VIABLE-AT-TESTED-SCOPE** for the batch/genesis core (A1+B3+E1; 3B/N≤100; our G6.1/D-D1-2 corruption is **INCREMENTAL-path-only** — NOT counted against batch); route incremental-high-churn to a gated side-store. §8.7 `k≤1` attaches to incremental/residual mode, NOT the batch core. Reasoned position (no pre-registered falsifier), NOT a PASS. Dual-reviewed (advisor + gpt-5.5 FIX-FIRST applied). Open §1.1 dims (auditability/governance/security/routing/cost) → F1. **Full detail (single source): `docs/B3_IN_WEIGHT_NECESSITY_DECISION.md`.** NEXT: 7B numeric-transfer (OQ-W1) → CP2 → write F1 as the hybrid. **Operator Q: batch-only or incremental-at-scale?** (decides which row governs — biggest F1 lever).
- ⭐ LATEST (2026-06-21): **D-D1-2 ⟨D-D1-2@e023d8d2⟩** (2026-06-21): §8.7 numeric-threshold instrument → **operational guardrail `k≤1`** (REVISED from k≤2 after seed-2 across-held-out; anchor by k=2, WARNING k=2-3, HARD k=8-10; + mixed-load needs a global-volume bound). Dual-reviewed (Opus advisor + gpt-5.5 cross-family, inline). k=3-4/k=10-12 = scoped order-dominated observations (one toxic order drives them), NOT portable thresholds; Wilson UCB retired (clustered units→order-bootstrap). Per-relation count = fail-closed SENTINEL, not the causal var (edit-set/key-collinearity geometry). 3B-only (size transfer OPEN), pure-capital anti-conservative, incremental-path-only (deploy=batch/Genesis A1-clean). Instrument: 3B within-process SD=0; ~50pp noise is 7B/across-process; binding 3B uncertainty = edit-ORDER. `docs/SPEC_8_7_AMENDMENT_DRIFT_CONCENTRATION.md` §4, `docs/SPEC_8_7_THRESHOLD_INSTRUMENT_PREREG.md`, CORPUS/22. **MIXED-LOAD (addendum):** pure-capital k≤2 does NOT survive +12 other-relation load (mixed clean ceiling k=0; driver = other-relation volume) → **vindicates the worse-of(global,per-relation) amendment design**; pair k≤2 with a global-volume bound + compaction (`results/d1_mixedload_smoke_3b_s3.json`). **[REVISED 2026-06-21 — across-held-out-seed check]:** the more-toxic seed-2 held-out is NOT clean at k=1-2 (pooled 0.69%/2.08%, worst 4.2%/8.3%) where seed-3 was 0% → **conservative ship ceiling tightens k≤2 → k≤1**; WARNING by k=2-3, HARD k=8-10. No per-relation count is universally clean (held-out-set-dependent) — reinforces 'count = coarse sentinel'. `results/d1_threshold_lowk_3b_s2.json`. **§8.7 amendment = ✅ OPERATOR-APPROVED.** **ConnectedPapers 6-graph review → register §J (leads D8-D19):** field converges on gated side-stores (NeuralDB/WISE/MEMOIR) → pressures **B3** in-weight-necessity; KEO/SetKE=our corruption named; Editing-Overfit/EVOKE=our E1 confound named. **NEXT:** more-toxic-seed/≥3-seed low-k (running/queued, push ceiling lower) → **7B size-term via determinism** (OQ-W1 transfer) → **B3 in-weight-vs-side-store** (graphs' strongest F1 signal) → CP2 → F1 readiness.

- **⭐ LATEST (2026-06-21): B1 MODEL-SIZE TERM — concentration law REPLICATES on Qwen2.5-7B (the §8.7 amendment is MODEL-GENERAL); size threshold UNRESOLVED (instrument-noise-limited).** (`docs/SPEC_8_7_AMENDMENT_DRIFT_CONCENTRATION.md`, `docs/B1_SIZE_TERM_PREREG.md`, `D-B1-2 ⟨D-B1-2@0db8d819⟩`.) Ported the D1 dose-response to 7B (matched harness; VRAM fixes eigh-for-P / diagonal-add / del-Pi-before-solve / expandable_segments — all proven inert, LAW#5 gates |Δ|=0.0000–0.0003; engine UNMODIFIED SHA 5c0c706a…). **REPLICATE (the win):** held-out capital corruption rises with capital-edit-count on 7B too (monotone on means, expr 100%, positive control fires) → the per-relation-concentration drift finding is **NOT 3B-specific**; the §8.7 structural amendment generalizes across model size. **SIZE TERM = UNRESOLVED, weak protective lean:** 7B leans *less*-corrupted than 3B in **7/8 paired cells (mean +11.5pp)** after removing a proven-noise seed3 draw — but +11.5pp ≪ the **~50pp run-to-run nondeterminism** and n=3, so it **cannot be confirmed or excluded**; NOT size-invariance, NOT the apparent collapse. **KEY INSTRUMENT FINDING:** sequential-edit held-out corruption swings **~50pp run-to-run on the IDENTICAL config** (7B seed3 same-config: 20.8%→70.8% on advisor-mandated re-run; the 4–21% 'collapse' did NOT reproduce) → single-run absolutes are unreliable; a **deterministic / higher-N instrument is needed to set the numeric §8.7 threshold (NEXT-ARC)** ([[sequential-edit-run-nondeterminism]], [[wide-intermediate-7b-editing-vram]]). **§8.7 STRUCTURAL AMENDMENT WRITTEN** as an operator proposal (per-relation `max_relation_concentration_since_anchor` counter drives drift_tier as the worse-of vs global `edge_count_since_anchor`) — the F1 deliverable from D1+B1; threshold value = open sub-item. **Advisor dual-pass** (mandated the reproducibility re-run that caught the noise; fixed a symmetric over-correction — the protective lean stands, the collapse was the artifact). **NEXT: F1 readiness framing + CP2 schema build-items.**
- **⭐ LATEST (2026-06-20): D1 CAPACITY LAW — first decisive run, dual-reviewed (`CORPUS/22`, D-D1-1 ⟨D-D1-1@0db8d819⟩). Aggregate LABEL=PARTIAL; ROBUST directional claim PROMOTABLE.** Concentration-vs-dilution at FIXED total-N=50 (Qwen2.5-3B, band[4-8], seq, in-solve AlphaEdit; LAW#5 gate PASSED |Δ|=0.0007; fixed disjoint 12-entity held-out). **CONCENTRATED (50 capital edits) vs DILUTED (17 cap + 33 other), 4 seeds×2 orderings: at equal total edge-count the concentrated store is MORE corrupted in 4/4 seeds (gaps 50/16.7/41.7pp; seed3 INVALID=continent dilutant under-expressed, directionally consistent).** → **global `edge_count_since_anchor` is INSUFFICIENT as a relation-agnostic §8.7 drift predictor; drift must be relation-concentration-aware** (central OQ-W1 reconciliation, §7.2 'wrong variable' resolved DIRECTIONALLY). **NOT a settled law:** valid seeds = 2 CONFIRM + 1 PARTIAL; seed1 shows an 8.3pp equal-capital-count gap → a **two-variable law (relation-concentration + smaller cross-relation term)**, not pure single-variable; thresholds/dominance/size-term UNSET (N≤50, 3B only). **Phase 1 predictor map** (`results/d1_predictor_map_result.json`): covariate ranking capital>language>continent; D7 basis-rotation weak-moderate. **Dual-reviewed:** Opus advisor (narrow + replicate-before-CORPUS) + **gpt-5.5 cross-family (`FIX-FIRST`, applied):** record PARTIAL not CONFIRM, 'falsified'→'insufficient', 'dominant'→two-variable, don't over-lean single-seed p, seed2 (dilutant 100%) rebuts weak-dilutant confound. **Independence CLOSED for the directional claim.** **Phase 3 DONE (2026-06-20, `CORPUS/22` triple-reviewed): clean dose-response with the language dilutant (100% expr, 3 seeds) REPLICATED concentration-dominance; the cross-relation term is a small NON-NEGATIVE tendency (low-power paired-sign signal, magnitude UNRESOLVED) — two-variable framing holds.** The clean-dilutant replication the review required is DONE. **NEXT D1:** B1/Qwen3-4B model-size term → quantitative law + §8.7 amendment for F1, then CP2 schema build-items. **INFRA:** pod restart had wiped the system-python ML stack; restored `transformers==4.51.0` pin ([[pod-restart-wipes-system-python-ml-stack]]).
- **⭐ LATEST (2026-06-20): C2-band falsifier FOLDED IN (`CORPUS/21`, D-C2band-1 ⟨D-C2band-1@c6fb6103⟩) — mechanical PASS, NOT PROMOTED (real-but-underpowered redistribution).** Band [8-12] vs [4-8] sequential N=100: cross-entity JS loc +18.73pp (67.68→86.41), guard cleared → LABEL=PASS by the frozen rule. **But NOT a PROVEN node:** top-1 leg n.s. (7/12→10/12, Fisher p≈0.37); within-entity JS −17.71pp (95.48→77.77, monotone; global fine); retention 96<98 (2× edits lost). **NOT an under-editing artifact:** within-loc FALLING (not rising) refutes a uniformly-weaker edit, and expression=100% both arms excludes under-expression → a REAL direction-specific REDISTRIBUTION (cross-entity isolation traded for within-entity perturbation + lower durability). Not promoted = single-seed/underpowered + within-entity TOP-1 cost & mechanism UNMEASURED. **NOT a deployment recipe change** (batch path already clean at [4-8]); mechanistic only — feeds D1 + C15 tension IF de-confounded. **De-confounders queued (pre-register + advisor first), (a)+(b) gate:** (a) [no-edit] same-entity cross-relation collinearity-vs-depth (tests basis-rotation hyp D7); (b) edited-entity within-attr top-1 re-run; (c) per-band Δ-norm + sham control; (d) ≥3 seeds/≥2 orderings. Autonomy had mislabeled the completed run LABEL=ERROR (wall-clock). **Cross-family review DONE (gpt-5.5 via Codex, `FIX-FIRST`): concurs PASS-not-promoted; narrows the claim — 'not an under-editing artifact' overshoots → only a *uniformly*-weaker edit is excluded (Δ-norm/depth-metric confounds OPEN); names the norm-matched/sham control (de-confounder c) as THE cheapest overturning test. Independence obligation CLOSED.** 
- **⭐ LATEST (2026-06-18, post-B3): E1 / B1 / C2 DONE; repo reorganized to publication grade.**
  - **E1 = Claim A PASS / Claim B FALSIFIED (`CORPUS/18`, D-E1-1 ⟨D-E1-1@55708623⟩):** CPU deployment loop CLOSES via **llama.cpp + Q4_K_M** (edited 100% / native 97.4%; ~8-13 tok/s pod-CPU proxy). **LARQL `gguf-to-vindex` cannot serve Qwen2.5-3B** — drops 108 attn biases + vocab-config mismatch → garbage; **A7 causal ablation proves bias-drop is sufficient.** LARQL is CPU-ONLY (no CUDA). **Model-family split:** Qwen2.5 (edit-validated) vs Qwen3 (LARQL-servable, bias-free).
  - **B1 = PARTIAL (`CORPUS/19`, D-B1-1 ⟨D-B1-1@2ebae54e⟩):** A1 batch-clean does NOT fully replicate at 7B (held-out 100→91.7%). Scopes A1 to 3B/N≤100; feeds D1. Directional-only size-density (confounded).
  - **C2 = PRUNED + mechanism (`CORPUS/20`, D-C2-1 ⟨D-C2-1@e2eff6af⟩):** relation-keying eliminated; same-relation key collinearity is U-shaped in depth (min **L8-12** 0.20-0.42, max late). **C15 late band = worst isolation zone** (new tension). New lead: band **[8-12] sequential** (gated on L9-12 cov).
  - **Hypothesis register:** `docs/HYPOTHESIS_REGISTER_2026-06-18.md` (24 hypotheses, 3 passes + advisor). Top open leverage: **B3/E3 (is L2 in-weight even required, or L1-retrieval + external index?)**, B2 (decouple DB-query from LARQL), C2/C3 (GRACE / neighbor-reassertion methods that structurally avoid the corruption), D1/D2 (capacity law + mechanism).
  - **NEXT (operator-recommended):** the **B3/E3 L2-necessity decision** (analysis, no compute) or the **band-[8-12]** mechanism test. A3/A4 stay parked.
  - **Repo:** reorganized — code in `experiments/<track>/`, configs in `configs/`, results in `results/`, logs in `logs/`, docs in `docs/`, stale in `archive/`. Scripts use `LLMDB_ROOT` (default `/workspace`). See `README.md` + `REPRODUCIBILITY.md` + `docs/EXPERIMENT_REGISTRY.md`. Infra dirs unmoved.
- **Last result:** **B3/G6.2 = PASS** (`CORPUS/17`) — real Q4_K_M quantization survival on the A1-clean batch store: edited retention 100% vs native 97.4% (Δ+2.6), validity gate clean; margin-confound characterized (edits survive Q4_K_M; NOT 'indistinguishable from native'). PRIOR: A2b refresh-K_S = K_S STALENESS RULED OUT (`CORPUS/16`). 3 seeds × λ∈{1,2} × {FIXED clean-base, REFRESH per-edit K_S}, in-script control. Per-edit K_S refresh does NOT reduce cross-entity corruption (clean seed-0: 95/90→70/90; paired Δ λ1=[−25,+5,0]/λ2=[0,0,0]; slightly hurts retention); drift LARGE in seeds 1/2 (col-cos 0.83/0.80) yet zero benefit → residual is entity-specific, NOT a staleness artifact. Gates pass (gate2 bit-exact). **🔑 Official BetaEdit repo FOUND** (`lbq8942/BetaEdit`, IJCAI 2026, cloned; ships our-exact qwen2.5-3b config) → A3 = PORT (solve = AlphaEdit + `λ1·Σ` + τ-P-refresh; A2's K_S·K_Sᵀ = low-rank shadow of `λ1·Σ`). PRIOR: A2 sentinels PARTIAL (`CORPUS/15`, `D-A2-1 ⟨D-A2-1@f26b823b⟩`; 8/20→16–17/20 @N=100, λ_s≈1–2, halves but doesn't arrest the decline); A1=PASS (batch ELIMINATES corruption, Genesis path clean, `CORPUS/14`); A0/G6.1=SPLIT seq-specific (`CORPUS/13`).
- **No active blocker on the deployment path.** The BATCH/Genesis path (the deployment model per D-SCOPE-1) is clean (A1) AND survives Q4_K_M (B3). The only open in-weight issue — ~15% residual cross-entity corruption on the **incremental/runtime** path (entity-specific, beyond the shared relation direction) — is **PARKED with A3**: it only matters if incremental online single-fact writes become a confirmed requirement.
- **▶ FRONTIER / WHAT'S NEXT (read this):** Track A is **closed for the batch deployment path** (A1 clean + B3 quantization-survives). A3/A4 are PARKED. The live falsifiers the goal now depends on (pick by what CPU deployment needs, all independent of the parked incremental work): **E1** (LARQL `gguf-to-vindex` ingest + real Intel-CPU serving = the deployment loop B3 only partially touched — strongest next), **B1** (larger-model replication / size-density), **C/G7** (multi-token value robustness), **D1** (capacity law — required for the F1 readiness determination). Set falsifiable pass criteria BEFORE each run; call `advisor()` before authoring the test set.
- **TRACK-A LEDGER (all resolved/parked — detail):**
  - **A2b — DONE (`CORPUS/16`):** K_S staleness RULED OUT (per-edit refresh doesn't help; large drift + zero benefit). BetaEdit (A3) earned **but parked** — see scope gate below.
  - **⛳ HIL SCOPE GATE — RESOLVED 2026-06-18 (D-SCOPE-1):** operator deferred to judgment; advisor-checked. Deployment model = **edit offline on GPU → COMPILE → serve on CPU** ([[deployment-target-intel-cpu]]) = the **batch-rebuild model**. A1 already pins the batch path at 100→100→100% @N≤100 (no headroom for A3 there). No stated incremental-write requirement. → **A3 is PARKED (earned, ready, gated on a CONFIRMED incremental-write requirement), NOT next.** Next run is chosen by what CPU deployment depends on.
  - **B3/G6.2 — DONE = PASS (`CORPUS/17`):** real **Q4_K_M** (4.99 BPW, self-built llama.cpp) quantization survival on the A1-clean batch store. Edited-fact retention **100% (99/99)** vs native-country **97.4% (75/77)**, Δ=+2.6 (≥−3) → PASS. Validity gate clean (HF↔GGUF-fp16 agreement 100% edited+native). **CAVEAT (characterized, `b3_margin_result.json`):** edited margins inflated by `compute_z` (median 0.979 vs native 0.812) → claim is 'edits survive Q4_K_M', NOT 'indistinguishable from native'. CPU inference (`-ngl 0`) served correct edits (partial E1). NEXT live falsifiers: E1 (LARQL ingest + Intel-CPU serve), B1 (larger model), C/G7 (multi-token), D1 (capacity law).
  - **A3 — PARKED (gated on confirmed incremental requirement):** PORT official BetaEdit (`external_prior_art/BetaEdit`, ships qwen2.5-3b config) — add `λ1·Σ` full-cov leakage term + τ-periodic history-aware P-refresh to our in-solve harness; re-tune λ1/τ for N=100/base (their λ1=3000/λ2=10/τ=1000/thresh=0.02 are gpt2-xl@10k — τ never fires at N=100). LAW#5 gate: λ1=0,τ>N,λ2=L2 ≡ our AlphaEdit bit-exactly. Screen eval pool to confident-correct (G6.1-style) so the instrument is clean across seeds. Pass criterion on clean metric vs in-script AlphaEdit baseline.
  - **A4 — QUEUED (cov warm):** mid-late band [18-22] — may give the edit more non-shared room.
- **Background:** `g6_band_cov_warm.py` → mid-late band [18-22] cov on Qwen2.5-3B (for A4). Check `g6_band_cov_warm.log` for `DONE`.
- **Stimulus note:** A2+ use `g6_screen_qwen3b_v2.json` (78-entity expanded screen, seeded 50/10/10 pools); A0/A1 use the original `g6_screen_qwen3b.json` (56). Don't overwrite either.
- **⚠️ PERSISTENCE WARNING (2026-06-18):** this session, Edit-tool writes to THIS file silently reverted (network FS); only Bash/python writes persisted. SESSION_CHECKPOINT.md + CORPUS are the reliable handoff. If this §0.3 looks stale, trust `SESSION_CHECKPOINT.md` (LATEST SESSION) + `CORPUS/14`+`CORPUS/15`. See [[verify-canonical-state-edits-persist]].

### §0.4 — Living-Document & Harness-Integration Protocol
- **When to update:** (a) any experiment completes → fill its block's RESULT + resolve its FORK + update §0.3 + §12 dashboard + §13 changelog **+ the full canonical-tracker set, then run `python3 tools/closeout_check.py <D-ID>` until ✅ ALL GREEN (BINDING close-out gate — the experiment is NOT done until green; DISCIPLINE §1.1)**; (b) any decision (model/method/tool) → add/append §5 with a Decision-ID; (c) any new dependency → §6; (d) any durable learning → memory (§2.7) + a one-line §13 entry.
- **Status flags** (use everywhere): `DONE` · `RUNNING` · `NEXT` · `QUEUED` · `GATED(on X)` · `BLOCKED(on X)` · `HALTED` · `ELIMINATED(revisitable)`.
- **Harness runtime hook:** this file is the canonical experiment-state record. Treat §0.3 + §12 as the machine-readable head; every run's result lands in its §8 block and is mirrored to `CORPUS/`. Re-mirror memory after writes (`cp /root/.claude/projects/-root/memory/*.md /workspace/memory_mirror/`).
- **How to read a fork:** each experiment ends in `PASS → / PARTIAL → / FAIL →` pointing to the next experiment ID. Follow the branch the data selects; if data is ambiguous, call `advisor()` before choosing.

═══════════════════════════════════════════════════════════════════════
## §1 — TOOLS & INSTRUMENTS AVAILABLE
═══════════════════════════════════════════════════════════════════════
_What's on hand, when to reach for it, caveats. Surfaced here so any agent knows the full instrument set._

| Instrument | Purpose | When to use | Caveat / how to invoke |
|---|---|---|---|
| **`advisor()`** | Stronger reviewer that sees the full transcript | BEFORE substantive work, when stuck, on approach change, before declaring done | No args; weight it heavily; it has caught real over-claims & design bugs this program. See §2.1. |
| **Framework Council** (7 skills in `/workspace/skills/`) | Spec-authoring & domain brainstorming (memit, graph-data, state-consistency, validation, orchestration, aisecops, council) | Framing spec contracts, surfacing tensions/open-questions, domain reasoning | **Spec-authoring tool, not an evidence source.** Same-model council reading our corpus = weak independence / confirmation-amplification — do NOT use to "confirm" our own conclusions (§2.5). Skills are zip bundles; extract to read. |
| **Perplexity Deep Research** | Open-web SOTA survey, cited | New external methods, current benchmarks, "what's the field doing" | Operator-run. Prompt template: `research_and_specs/perplexity_prompt_*.md`. Cross-check claims; flag speculation. |
| **NotebookLM** | Corpus-grounded retrieval over OUR research + curated sources + the spec | "What does our knowledge base already contain"; mining the spec/council docs | Operator-run. Answers ONLY from corpus, cites sources, flags absence. Prompts: `research_and_specs/notebooklm_prompts_*.md`. Complementary to Perplexity (corpus vs open-web). |
| **`deep-research` skill** | Our own fan-out web-search + fetch + adversarial-verify harness | Independent cross-check of an external survey; multi-source synthesis we run ourselves | In-session; produces a cited report. Good for triangulating Perplexity/NotebookLM. |
| **WebSearch / WebFetch** | Targeted fact lookup (sizes, repos, papers) | Sourcing details, single-fact verification | WebFetch fails on JS-SPA pages (use WebSearch then fetch a static URL). |
| **The Spec** (`…/llm-as-database-v1_2-integrated-spec.md`) | The governing contract | Every experiment must cite the §it bears on; read the §end-to-end, not grep excerpts | §map in §4. Reading source fully is a LAW (§2.4). |
| **Editing harness + engine** | `memit_dry_run/memit` (kmeng01, UNMODIFIED) + our in-solve AlphaEdit harness (`s243h_*.py`, `g6_scale_n.py`) | All in-weight editing experiments | Engine fingerprint-gated; harness-side methods need LAW#5 inertness proof (§2.4). |
| **Vendored reference editors** (`easyedit_*`) | AlphaEdit / WISE / GRACE / MEMIT reference impls + hparams + notebooks | Porting a method (A3 BetaEdit builds on these; A5 WISE; A6/GRACE) | Already LOCAL — see §6. |
| **LARQL** (`external_prior_art/larql/target/release/larql`) | `.vindex` build/serve, GGUF↔vindex, CPU inference, LQL | The bridge, deployment (Track E), quant ingest (B3) | UNMODIFIED. `convert quantize` ships FP4 only (Q4_K via llama.cpp ingest). |
| **llama.cpp** (prebuilt) | Real `Q4_K_M` quantization | B3 quantization survival | Pull prebuilt `b9693 ubuntu-x64` from ggml-org releases (§6); no build needed. |
| **Qwen-Scope SAEs** | Residual-stream sparse autoencoders for Qwen3/3.5 | A6 SAE-guided disentanglement (frontier) | HF `Qwen/SAE-Res-Qwen3-*`; residual-stream ≠ down_proj basis (bridge unproven). |

═══════════════════════════════════════════════════════════════════════
## §2 — OPERATING DISCIPLINES (how we work — non-negotiable)
═══════════════════════════════════════════════════════════════════════

### §2.1 — Advisor-invocation discipline
Call `advisor()`: (a) **before authoring any test/criteria set or new harness** — not just before declaring done; (b) before committing to an interpretation or approach; (c) when stuck/looping; (d) before declaring an experiment complete (make the deliverable durable FIRST). On long tasks: at least once before committing to an approach and once before done. Give its advice serious weight; if you have primary evidence contradicting it, surface the conflict in one more call rather than silently overriding. It is enabled via `/advisor` (Opus 4.8).

### §2.2 — Additional-research discipline (when to reach past our own data)
- **Spec review** — ALWAYS before framing a load-bearing decision; read the governing § end-to-end (grep-excerpts misframed a decision before). Every experiment block cites its §.
- **NotebookLM** — when the question is "does our existing corpus/spec/council already cover this?" (mechanism, prior art we curated, spec assumptions). Corpus-grounded.
- **Perplexity / `deep-research`** — when the question is "what is the field's current SOTA / is there a method we're missing?" Open-web. Trigger after a falsification (G6.1 → the cross-entity survey) or before a frontier bet.
- **Council** — when *authoring/refining spec contracts* or surfacing tensions, NOT for confirming empirical conclusions.
- **WebSearch** — targeted facts (model sizes, repos, paper availability) feeding §5/§6.
- **Rule:** research informs; **only empirical runs on our harness are binding evidence** (§2.5). Cite artifact + exact number, or flag `UNVERIFIABLE`.

### §2.3 — Falsification & anti-bias discipline (the traps that have bitten us)
- **Pre-register** metric, procedure+n, threshold+direction, and a *positive control* BEFORE the run. "Let the numbers land."
- **Anchor trap** — never set a threshold "just below what we got"; derive it from what makes the thing viable *as a database per the spec*.
- **Prototype-tautology trap** ([[prototype-tautology-trap]]) — code that implements a contract and verifies it implements the contract proves control-flow, not the contract. Build tests that can actually fail.
- **False-no-op / expression gate** — an unexpressed edit inflates "locality." Always measure apply-time expression separately from end-state retention (the G6.1 split).
- **JS-vs-top-1** — match the metric to the claim. A "reads corrupted" claim is a top-1 claim; measure top-1, not just distributional JS.
- **Disjoint pools** — for any preserve/sentinel method, the protected set and the eval set must be DISJOINT (and both disjoint from edited), or you rebuild the tautology at the data level.
- **Independence** — a passing self-test is not evidence the advice was wrong.

### §2.4 — Engine-integrity LAWs (from CLAUDE.md — load-bearing)
1. **Fingerprint gate** — verify the engine identity/fingerprint before any dispatch; engine + LARQL + git stay UNMODIFIED.
2. **LAW#5 inertness** — any harness-side reimplementation (e.g., in-solve AlphaEdit, sentinels) MUST first prove it reproduces the stock engine bit-for-behavior on a null/identity edit before its science results are trusted. (`g6_scale_n.py` runs this gate every time.)
3. **One-fix-then-halt** — change one thing, observe, halt; don't stack fixes.
4. **Read source before authoring** — read the engine/spec code you build on, end-to-end.
5. **Science-path-patch isolation** — never patch the science path; prove inertness of any shim.

### §2.5 — Independence discipline
The binding signal is **empirical runs that can fail**. Review ≠ evidence. Same-model council/subagents reading our corpus = confirmation-amplification — a *different* model cold-reading is better, but still not evidence. When confidence is highest, call `advisor()` and seek a falsifier, not a confirmer.

### §2.6 — Context-save discipline
- Durable deliverables → `/workspace` (never only `/dev/shm`, which is RAM). Update `CORPUS/` + `SESSION_CHECKPOINT.md` + this runbook's §0.3/§12/§13.
- `/dev/shm` artifacts are reproducible-from-scripts; never the source of truth.
- After a meaningful step, write the checkpoint so a fresh context can resume from §0.3 alone.

### §2.7 — Memory & learnings write discipline
- **Write a memory** when a durable, cross-session fact/learning surfaces: a corrected reasoning trap, an operator preference, a tool/infra gotcha, a project decision not derivable from code.
- **Types:** `user` / `feedback` (corrections + the why) / `project` / `reference`. One fact per file + frontmatter; link `[[related]]`; add a one-line pointer to `MEMORY.md`.
- **Don't** save what the repo already records (code, git history, CORPUS). If asked to remember such, save *what was non-obvious* about it.
- **Mirror** after writing: `cp /root/.claude/projects/-root/memory/*.md /workspace/memory_mirror/`.
- **Learnings cadence:** at each experiment close, ask "what did this teach that a future agent must not relearn the hard way?" → if durable, write it (e.g., this session produced [[prototype-tautology-trap]], [[runpod-dashboard-vs-pod-metrics]], [[standing-auth-forward-requirements]]).

### §2.8 — Artifact, naming & Decision-ID conventions
- **Scripts** `<track><n>_<slug>.py` (e.g., `a2_relbal_sentinels.py`); **results** `<same>_result.json`; **logs** `<same>.log`; **writeups** `CORPUS/<NN>_<SLUG>.md`.
- **Heavy I/O on `/dev/shm`**, durable outputs copied to `/workspace`.
- **Decision-IDs** `D-<TRACK><n>` (e.g., `D-A2-1`) tie every accept/eliminate choice to §5.
- **Launch durably**: `setsid bash -c '… python -u script.py > script.log 2>&1' </dev/null & disown` (survives disconnect).

═══════════════════════════════════════════════════════════════════════
## §3 — OPERATIONAL HYGIENE (RunPod GPU / Memory / Disk)
═══════════════════════════════════════════════════════════════════════

### §3.1 — The dashboard-vs-pod trap ([[runpod-dashboard-vs-pod-metrics]])
RunPod **dashboard** metrics diverge from in-pod tools — **trust the in-pod tools**:
- **GPU:** `nvidia-smi`. Dashboard util% lags and reflects OUR own work; the binding signal for "can my run allocate" is **`memory.used`** (we need ~6–16 GB depending on model). A run that loads and executes IS proof the GPU is ours.
- **RAM:** `free -h`. Dashboard % counts reclaimable page-cache; real pressure = `used`, not `used+cache`. We have ~450 GiB available.
- **Disk:** `df` inside the pod shows the **cluster** (1.2P), NOT our per-volume quota. The dashboard volume % (~86% now) is the binding, in-pod-invisible limit. **Respect it.**

### §3.2 — Pre-flight checklist (before every experiment)
1. `nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.free --format=csv,noheader` → confirm enough free VRAM; no foreign process holding memory.
2. Confirm needed cov caches exist (`covariance_caches/<model>/wikipedia_stats/*.npz`) — else queue cov compute first (§6).
3. Confirm `/dev/shm` headroom (`df -h /dev/shm`) for overlays/vindex; rebuild from scripts if wiped.
4. If a large download is pending, **reclaim disk first** (§3.3) — we're volume-constrained.
5. Launch detached + unbuffered (§2.8). Verify start (`ps`, `tail log`). Run the LAW#5 inertness gate.

### §3.3 — Disk reclamation (standing-auth — do it, narrate it)
Volume ~86% full. **~62 GB reclaimable** without touching the active Qwen line:
| Candidate | Size | Safe? |
|---|---|---|
| `hf_cache/hub/models--meta-llama--Llama-3.1-8B` | 15 GB | ✅ superseded baseline |
| `covariance_caches/meta-llama_Llama-3.1-8B` | 10 GB | ✅ |
| `covariance_caches/mistralai_Mistral-7B-v0.3` | 3.9 GB | ✅ |
| `covariance_caches/meta-llama_Llama-3.2-3B` | 1.8 GB | ✅ HALTED experiment |
| `stage_1_sect/overlays` | 33 GB | ⚠️ confirm not referenced before delete |
Reclaim the first four (~31 GB) freely; verify `stage_1_sect/overlays` provenance before removing. Always keep: Qwen2.5-3B/7B, Qwen3-0.6B, their cov caches, the engine, LARQL, CORPUS, memory_mirror.

### §3.4 — Cov-cache & /dev/shm discipline
- Covariance is the expensive precompute (~1–2 h per 5-layer band on a 3B). It **caches to `covariance_caches/<model>/wikipedia_stats/`** — reuse aggressively; never recompute a cached band.
- `/dev/shm` (29 GB RAM tmpfs) holds vindex/overlays for speed; it is **ephemeral** — rebuild from scripts after a pod restart. Cap BLAS threads (`OPENBLAS_NUM_THREADS=8`) so cov inversion doesn't thrash.
- transformers pinned **4.51.0**; torch 2.4.1+cu124. Do not upgrade in place (breaks engine nethook / Qwen3 support balance).

═══════════════════════════════════════════════════════════════════════
## §4 — KNOWLEDGE BASE INDEX (research docs + spec map)
═══════════════════════════════════════════════════════════════════════
_Cite the relevant entry in every experiment block. Consult before framing decisions (§2.2)._

### §4.1 — Research documentation
| Doc | Holds | Consult for |
|---|---|---|
| `research_and_specs/cross_entity_research_synthesis.md` | **The reconciliation** of all 3 research artifacts vs our evidence; candidate ranking; BetaEdit finding; OQ-W1 "wrong variable" | Start here for the blocker's solution space |
| `research_and_specs/llm_editing_survey.md` | Perplexity Deep Research: ranked methods (BetaEdit#1, batch, WISE, RECT/PRUNE/O-Edit, SAE, GRACE), mechanism, capacity-ceiling, batch-vs-seq, eval harness | External SOTA per method; arXiv IDs |
| `research_and_specs/notebooklm_10_prompt_research_corpus-{1,2}.md` | Corpus-grounded: MEMIT's own P127/P641 specificity collapse, LARQL "balancer/hijacking", λ tradeoff, our spec's OQ-W1/GAP-1/Genesis/C2/C4, WISE/ELDER/MELO | What our corpus + spec already say |
| `research_and_specs/perplexity_prompt_*.md`, `notebooklm_prompts_*.md` | The research prompts (reusable templates) | Running further external research |
| `s240_literature_scan.md` | Earlier scan: Ripple Effect naming, BLUE (boundary-layer), GRACE/BalancEdit, GIE/SIR, locality-eval critique, RippleEdits/MQuAKE/KnowEdit benchmarks | Prior-art mechanism clues |
| `framework_finding_v1_10_additive.md` (+ v1_7..v1_9) | Our own findings: calibrated metric, H-MODEL (Qwen-local/GPT-J-not), sequential fail, Rung-1/3/AlphaEdit ladder | Historical decision rationale |
| `write_engine_viability_determination_report.md` | The same-entity multi-field VALIDATED determination (now scoped by G6.1) | The proven foundation + its scope |
| `CORPUS/00`,`03`,`13`, `LARQL_INTEGRATION_ASSESSMENT.md` | Master evidence ledger, status ledger, G6.1 writeup, the bridge | Authoritative evidence + status |

### §4.2 — Spec section map (cite these)
- **§7.3 Relation Families / §7.5 Polysemantic Discipline** — the schema-level locality rules; relevant to cross-entity (relation fan-out) and disambiguation.
- **§7.7 Project Genesis (D9/D10)** — the batched foundational write (→ A1 batch relevance; Genesis = single atomic 2PC across L1–L4).
- **§8.1–8.2 Write Engine / MEMIT designated (C15 band, D12 method-class, D20 orthogonal-projection mandate)** — the core write contract; C15 = L15–25/32L (our [4-8] divergence → A4).
- **GAP-1 / OQ-W1 (§22 protocol; numeric outputs implementation-phase)** — "cumulative edit-volume degradation threshold (model-specific)," deferred pending "target-model selection + write-volume stress test." **G6.1 + Track D resolve this.**
- **C2 (entity names compositionally unambiguous) / C4 (untyped entities = violation)** — schema disambiguation; does NOT cover relation-level fan-out (gap).
- **§9 (validation pipeline), §10.2 (Gate checks), §11.13 (ledger), §46 (2PC ordering), §20.3 (ceremony)** — governance (CP1–G3 done).
> ⚠️ **VERIFY-BEFORE-CITING:** §7.3/7.5/7.7/8.2 + C15/D12 were grep-confirmed against the spec text this session — trust them. But **C2, C4, §46, §20.3, §11.13, D20, OQ-W2** were surfaced via the NotebookLM reading / prior memory, NOT a direct read of the spec text. Per [[read-authoritative-source-fully]], **re-read the spec § before F1 builds the readiness verdict on any of these** — do not let a NotebookLM paraphrase become a load-bearing citation.

═══════════════════════════════════════════════════════════════════════
## §5 — DECISIONS LEDGER (accepted & eliminated — reasoning, NOT hard gates)
═══════════════════════════════════════════════════════════════════════
_Every entry is **revisitable**. "ELIMINATED" = "set aside for a documented reason," never "forbidden." If evidence shifts, reason fresh and append a new dated line. Tie new entries to a Decision-ID._

### §5.1 — Models
| Model | Status | Reasoning | Revisit trigger |
|---|---|---|---|
| **Qwen2.5-3B** | **ACCEPTED (primary dev)** | Recipe tuned & validated here (in-solve AlphaEdit thresh 0.005); cov [4-8] cached; CPU-class. The cross-entity blocker lives here → cheapest place to fix it. | — |
| **Qwen2.5-7B** | ACCEPTED (clean reference) | Cleanest multi-field locality (seq 100%, no workaround); the "known-good" upper bound. Heavier. | If 3B fix transfers, 7B is the safety net. |
| **Qwen3-0.6B** | ACCEPTED (bridge/serve) | LARQL-servable; the `.vindex` bridge proven here. | — |
| **Qwen3-4B** | **QUEUED (scale + BetaEdit anchor)** | Earlier set aside as "no SAE, costs a download"; **revised** — BetaEdit validates on Qwen3-4B at band [4-8] (our exact setup), so it's the natural scale/comparison model (Track B1). | Now revisited → queued (D-B1-1). |
| **Qwen3-1.7B / 8B** | QUEUED (SAE-supported) | Qwen-Scope ships SAEs for these (not 4B) → the models for the A6 SAE frontier; 8B also a larger-scale check. | Pull when A6 or B1-8B fires. |
| **GPT-J-6B** | ELIMINATED (revisitable) | Same-entity non-local; fails the multi-field test; used only as the negative baseline. | If a method claims architecture-generality, re-test. |
| **Llama-3.2-3B** | ELIMINATED/HALTED (revisitable) | Hand-built hparams → edits didn't express (false no-op); not pursued under one-fix-then-halt. | If a validated MEMIT config for it appears. |
| **Mistral-7B / Llama-3.1-8B** | ELIMINATED (revisitable) | Baselines, done; cov caches are §3.3 reclaim candidates. | Cross-architecture generality test. |
| **Gemma-4 E4B** | LOGGED candidate | CPU-deploy fit; needs isolated newer-transformers venv (don't upgrade in place). | If Qwen line hits a wall on CPU deploy (Track E). |

### §5.2 — Editing methods / write-engine choices
| Choice | Status | Reasoning | Revisit trigger |
|---|---|---|---|
| **MEMIT (kmeng01) as engine** | ACCEPTED | Spec D12-designated; reference impl; UNMODIFIED. | — |
| **In-solve AlphaEdit (null-space P + cache_c, thresh 0.005)** | ACCEPTED (current recipe) | Fixed same-entity sequential (33→100%); D20-aligned. Inertness-proven. | Insufficient for cross-entity (G6.1) → extended by A2/A3. |
| **Batch (single joint solve) for foundational writes** | **ACCEPTED-for-Genesis (D-A1-1 ⟨D-A1-1@92b78833⟩)** | A1: ELIMINATES cross-entity corruption (held-out FLAT 100% N≤100 vs seq 42%); Genesis(§7.7) is a batch. Doesn't fix incremental path. | If degrades past N=100. |
| **Relation-balanced in-solve sentinels (K_S in LHS)** | **PARTIAL-mitigation, directional (D-A2-1)** | A2: ~halves runtime-incremental corruption (8→17/20 @N=100, λ_s≈1–2) at retention/within cost; wall past λ_s≈2; doesn't arrest decline. Not locked (single seed). | A2b / stack on A3; seed-replicate before locking λ_s. |
| **Subject-keying** | ACCEPTED-default / limited | Standard; within-entity collision when multi-field. | — |
| **Relation-inclusive keying (Rung-1)** | ELIMINATED-as-sole-fix (revisitable) | Fixed same-entity (100%) but WORSENED cross-entity (CEloc 83.6%); language under-expresses. | As a *component* of a relation+entity scheme. |
| **Post-hoc entity-aware projection (Rung-3)** | ELIMINATED-as-sole-fix (revisitable) | Only 50% seq retention; post-hoc is structurally too late vs pseudo-null leakage (BetaEdit). | As intuition for the in-solve A2. |
| **`fact_token="last"` engine path** | ELIMINATED (blocked) | Engine stub raises (`compute_z.py:216`) — unimplemented; would require patching the science path (LAW#5). | If engine upstream implements it. |
| **λ/threshold over-tuning** | ELIMINATED-as-fix (revisitable) | Monotonic specificity↑ but efficacy↓ (MEMIT + our thresh=0.001→0% retention). A dial, not a solution. | As a per-relation knob within A2. |
| **BetaEdit (leakage-aware null-space + history)** | **QUEUED (A3)** | SOTA successor; validated on our exact Qwen3-4B/[4-8]; formalizes our mechanism. CORRECTION 2026-06-18: official repo lbq8942/BetaEdit (IJCAI 2026) FOUND+cloned (external_prior_art/BetaEdit); the 'arXiv 2605.09285' id was fabricated (repo cites only IJCAI 2026). A3 = PORT its solve (λ1·cov leakage term + τ-periodic P-refresh) into our inertness-gated harness, not a from-paper reimplement. | Build after A2 to compare/stack. |
| **WISE / GRACE / MELO (parameter-preserving)** | QUEUED (A5, ceiling-breaker) | Cross-entity-clean by construction; WISE locality 1.00; matches spec's own tiered-memory hybrid. Reference impls local. | If A2/A3 hit a hard in-weight ceiling. |
| **SAE-guided disentanglement (Qwen-Scope)** | QUEUED-frontier (A6) | Attacks polysemanticity at root; but residual-stream-SAE→down_proj bridge unproven in any source; multi-week. | After A2/A3; if in-weight isolation caps out. |

| **Edit band [8-12] (low-collinearity) for cross-entity isolation** | **REAL-BUT-UNDERPOWERED / NOT PROMOTED (D-C2band-1)** | C2-band: mechanical PASS (cross-JS +18.73pp seq N=100) top-1 n.s. + within-entity −17.7pp + ret 96<98 = a REAL redistribution (within-loc FALL + expr 100% rule out under-editing), underpowered (1 seed) with within-entity TOP-1 cost & mechanism UNMEASURED; not a recipe change (batch clean at [4-8]). | De-confounders (a)-(d) in CORPUS/21; esp. D7 basis-rotation collinearity curve + edited-entity within-attr top-1. |

| **Model-size term for the concentration law (B1, Qwen2.5-7B)** | **UNRESOLVED — weak protective lean; law REPLICATES (D-B1-2)** | Concentration law replicates on 7B (monotone on means, expr 100%) → §8.7 per-relation amendment is MODEL-GENERAL (the win). Size threshold: 7B leans less-corrupted 7/8 paired cells (+11.5pp) but ≪ ~50pp run-to-run nondeterminism (7B seed3 same-config 20.8→70.8 on re-run; 'collapse' was a noise draw) at n=3 → cannot confirm/exclude. | Lower-variance instrument (deterministic / higher-N / batch path) to set the numeric threshold; +8B as 3rd point. |
| **Drift variable = relation-concentration, NOT global edge-count** | **DIRECTIONAL-ROBUST / quantitative-law UNSET (D-D1-1)** | D1: at fixed total-N=50, concentrated (50 same-relation) more corrupted than diluted (17 same-rel+33 other) in 4/4 seeds → global `edge_count_since_anchor` (§8.7) insufficient. Dual-reviewed (Opus + gpt-5.5): record as two-variable (concentration + smaller cross-relation term), not settled single-variable. | Clean ≥3-high-cardinality-relation replication + B1/Qwen3-4B size term → quantitative thresholds + §8.7 amendment. |
| **Storage architecture: diffuse in-weight vs gated side-store (B3 in-weight-necessity)** | **DECIDED = scope-keyed HYBRID (D-B3N-1)** | In-weight NOT contractually required: its "native-knowing" value (spec line 90) is a paradigm *preference*, not a tested requirement; a structured side-store meets the *enforced* read contract (L1 SELECT/reverse-lookup/multi-hop) given reliable routing. Verdict: in-weight VIABLE-AT-TESTED-SCOPE for the batch/genesis core (A1+B3+E1; 3B/N≤100; corruption is incremental-path-only — NOT counted against batch); route incremental-high-churn to a gated side-store. Reasoned position (no pre-registered falsifier), NOT a PASS. Dual-reviewed (advisor + gpt-5.5 FIX-FIRST). `docs/B3_IN_WEIGHT_NECESSITY_DECISION.md`. | Confirmed incremental-at-scale OR hard mid-generation/zero-latency reason-over-fact requirement → re-open Axis A/B. Open §1.1 dims (auditability/governance/security/routing/cost) resolved in F1. |

### §5.3 — Tools / infrastructure
| Choice | Status | Reasoning |
|---|---|---|
| **LARQL (Chris Hay) for vindex/serve/deploy** | ACCEPTED | The read/query/CPU-deploy layer; bridge proven; UNMODIFIED. `quantize` ships FP4 only. |
| **llama.cpp prebuilt for real Q4_K** | ACCEPTED (B3) | LARQL can't produce Q4_K; pull official prebuilt, LARQL ingests via `gguf-to-vindex`. Not the unverified `llama-cpp.com` mirror. |
| **RunPod RTX 4090 pod** | ACCEPTED | Edit-time GPU; CPU-deploy proxy. molab/Modal/Lightning assessed — RunPod stays primary (§ molab memory). |
| **transformers 4.51.0 pin** | ACCEPTED | Qwen3 support + engine nethook; 4.45 lacks Qwen3, 5.x breaks engine. |
| **EasyEdit vendored refs** | ACCEPTED (source) | AlphaEdit/WISE/GRACE/MEMIT impls local → no re-download for ports. |

═══════════════════════════════════════════════════════════════════════
## §6 — DEPENDENCY & MODEL SOURCING CATALOG
═══════════════════════════════════════════════════════════════════════

### §6.1 — Already cached (no download)
| Asset | Size | Location | Ready for |
|---|---|---|---|
| Qwen2.5-3B + cov [4-8] | 5.8 GB + cov | hf_cache + covariance_caches | A1, A2, A3, all Track A |
| Qwen2.5-3B cov [18-22] (mid-late) | computing now (~done) | covariance_caches | A4 band test |
| Qwen2.5-7B + cov | 15 GB + 6.7 GB | cached | clean-reference checks |
| Qwen3-0.6B + cov [4-8] | 1.5 GB | cached | bridge/serve, Track E |
| AlphaEdit/WISE/GRACE/MEMIT refs | — | `easyedit_upstream/easyeditor/models/*`, `easyedit_assets/rung*` | A3/A5/A6 ports |
| LARQL binary | 119 MB | `external_prior_art/larql/target/release/larql` | bridge, B3, E |

### §6.2 — To source downstream (reclaim disk first — §3.3)
| Asset | Source | Size | Download | Cov-compute | Needed by |
|---|---|---|---|---|---|
| **Qwen3-4B** | HF `Qwen/Qwen3-4B` | ~8 GB | ~15–30 min | ~1.5–2.5 h (5-layer band) | **B1** (scale + BetaEdit anchor) |
| **Qwen3-1.7B** | HF `Qwen/Qwen3-1.7B` | ~3.4 GB | ~5–15 min | ~1–2 h | A6 (SAE), B1-small |
| **Qwen3-8B** | HF `Qwen/Qwen3-8B` | ~16.4 GB | ~30–60 min | ~2–4 h | A6 (SAE), B1-large |
| **Qwen-Scope SAEs** | HF `Qwen/SAE-Res-Qwen3-{1.7B,8B}-*` | ~hundreds MB–GB each (verify at pull) | minutes–tens | n/a | A6 frontier |
| **llama.cpp prebuilt** | `github.com/ggml-org/llama.cpp/releases` `b9693 ubuntu-x64` | ~tens MB | minutes | n/a | B3 real Q4_K |
| **BetaEdit** | OFFICIAL repo lbq8942/BetaEdit (IJCAI 2026); cloned to external_prior_art/BetaEdit; ships qwen2.5-3b config = our exact band[4-8]/down_proj/subject_last setup | — | PORT the solve into our harness (~hours, builds on `g6_scale_n.py`/`a2_relbal_sentinels.py`) | reuse cached cov | A3 |
| **DiKE** (optional) | arXiv 2505.18774 | — | reimplement disentanglement module | — | A6-adjacent |

═══════════════════════════════════════════════════════════════════════
## §7 — STANDING SCIENTIFIC CONTEXT
═══════════════════════════════════════════════════════════════════════

### §7.1 — The mechanism (CONSENSUS across all sources + our data)
Cross-entity collapse = **shared-relation-direction interference**. Keys decompose `k_{e,r}=k_e+k_r+ε`; all same-relation facts share `k_r`. The shared `k_r` is **high-variance → lies in the editable subspace, NOT the low-singular-value null-space** AlphaEdit's `P` protects. `cache_c` preserves *edited* keys only (sparse over the relation manifold). BetaEdit proves real covariance is full-rank → truncated-SVD pseudo-null leaks (`P·K₀≠0`) and leakage **accumulates** with edits → our monotonic 100→42% decay. Confirmed independently by: Perplexity (math + BetaEdit), our corpus (MEMIT's own P127/P641 collapse; LARQL "hijacks all the other capital queries"), superposition theory, and G6.1.

### §7.2 — The spec assumption G6.1 violated (the readiness-relevant finding)
Spec `OQ-W1`/`GAP-1` models edit-locality degradation as a function of **cumulative edge count** (drift warn @1,500 / hard-stop @8,000 / sub-batch @2,000). G6.1 shows interference is **relation-fan-out-conditioned, not volume-conditioned** — 100 capital edits corrupt cross-entity reads while 100 diverse edits likely would not. → The spec's drift signal is **monitoring the wrong variable** (Track D derives the right one). This is the central reconciliation item.

### §7.3 — Proven foundation (do not relitigate; G6.1 scoped it)
- In-weight multi-field editing viable, **model/size-dependent** (GPT-J fails; 7B clean; 3B & 0.6B work with recipe).
- Recipe = in-solve AlphaEdit (null-space, thresh 0.005) + preserve-sampling + batched-per-record compile. Survives 4-bit (crude sim). Full CRUD + compaction hold.
- Decoupled bridge (clean ΔW → `.vlp` → APPLY on frozen base → COMPILE) works on CPU, no LARQL code.
- Governance CP1–G3 PROVEN-FOR-SCOPE (2PC, ledger, Ed25519, validation pipeline).
- **Scope correction:** the "COMPLETE multi-field store VALIDATED" headline was **same-entity / small-N only**. Cross-entity-at-scale is OPEN (this runbook's Track A).

### §7.4 — Evidence & metric standards (use in every Track-A run)
- **5-way locality split**: edited · held-out same-relation · same-entity other-relation · unrelated · global.
- **Track all**: top-1 correctness AND gold-logit margin AND KL-from-pre on held-out same-relation; apply-time expression separately from end retention.
- **Staircase** N = (10/)25/50/100(/250/500/1000) in BOTH sequential and batch.
- **Disjoint pools** (edit / sentinel / eval). **Positive controls** mandatory.
- **Falsifiable PASS bound** for the cross-entity fix (derived from DB viability, not anchored): held-out same-relation **top-1 correctness ≥ baseline−5 pts at N=100** with **no monotonic decay** (slope ≥ −2 pts/rung), while write-side retention ≥95% and apply-expression ≥95%.

### §7.5 — Glossary
- **retention** = fraction of edited facts still top-1-correct at end.
- **apply-time expression** = edit expresses (target is top-1) immediately when written (guards false-no-op).
- **held-out same-relation top-1** = correctness of never-edited entities on the edited relation (THE cross-entity metric).
- **within-entity locality** = edited entity's OTHER attributes intact.
- **CEloc / JS-loc** = cross-entity locality via distributional JS (supporting, not the top-1 claim).
- **fan-out** = # entities sharing a relation (the conjectured capacity driver).
- **sentinel keys K_S** = held-out same-relation keys added to the in-solve preservation term (A2).

═══════════════════════════════════════════════════════════════════════
## §8 — EXPERIMENT DECISION TREE (Tracks A–F)
═══════════════════════════════════════════════════════════════════════
_Block template: ID·Name·STATUS → Objective → Spec/KB refs → Rationale → Deps/sourcing/time → Method (+pre-written code where determinate) → PASS/PARTIAL/FAIL thresholds → Predictions(+direction) → FORKS → Spec ripple → Advisor/Council → Novel/deep reasoning. Fill RESULT + resolve FORK on completion (§0.4)._
> ⚠️ **Pre-written code is pre-DRAFTED, not yet executed** — its validity is established only when the LAW#5 inertness control passes (λ_s=0 for A2 must reproduce A0; batch-mode syntax-checked). Treat as a starting point to validate, not known-good. (A1's batch branch is now implemented in `g6_scale_n.py` via `WRITE_MODE=batch` and syntax-checked; A2 code still to be validated.)

### TRACK A — Cross-entity isolation fix (THE active blocker)

---
#### A0 · G6.1 scale-of-N · **DONE (SPLIT)**
RESULT: write-side PASS (ret 98%, expr 100%, within 95.6%, global 98.4%); cross-entity FAIL (held-out same-rel top-1 100→91.7→58.3→41.7%). Artifacts `g6_scale_n.py`, `g6_scale_n_result.json`, `CORPUS/13`. → opened Track A. **This is the falsifier all of Track A is measured against.**

---
#### A1 · Batch vs sequential write · **DONE — PASS (robust). `CORPUS/14`, `D-A1-1`.**
RESULT: batch (single joint solve) ELIMINATES cross-entity corruption — staircase held-out edited-rel FLAT 100→100→100% (N=26/50/100) vs seq 92→58→42%; cross-JS 99.7→97.9%. PASS contradicting the registered PARTIAL/FAIL prediction → advisor-mandated batch's-own-staircase ruled out defers≠eliminates. Mechanism: cumulative cache_c leakage from the incremental schedule. FORK→PASS: fold batch in as Genesis mode; still run A2 for runtime path. Caveats: N≤100, 12 coarse probes, within-JS 95.6→90.5, one ordering, 3B.
- **Objective / proves:** Does applying N shared-relation edits in ONE joint solve (batch) vs one-at-a-time (sequential) change cross-entity read corruption? Genesis is a batch write (§7.7), so we MUST characterize batch; we only tested sequential.
- **Spec refs:** §7.7 (Genesis = atomic batch), §8.2, OQ-W1. **KB:** synthesis §3/§6; Perplexity (LocFT-BF breadth-first > depth-first; MEMIT `E_mix` null result); NotebookLM (batch "safer" but silent on shared-relation balance).
- **Rationale/evidence:** MEMIT's joint solve "resolves conflicts mathematically"; but MEMIT's own `E_mix` found relation-diversity neutral, and sources are SILENT on whether *same-relation* batching balances or concentrates. Cheap to settle empirically (~1-line mode flag).
- **Deps:** cached Qwen2.5-3B + cov [4-8]. Time ~20–40 min. No download.
- **Method (pre-written — add `WRITE_MODE` to `g6_scale_n.py`):**
```python
# In g6_scale_n.py, replace the SCALE LOOP application with a mode switch:
WRITE_MODE = os.environ.get("WRITE_MODE", "sequential")   # 'sequential' | 'batch'
P = compute_P(); cache=[torch.zeros(P[0].shape[0],P[0].shape[0]) for _ in L]
if WRITE_MODE == "batch":
    # ONE joint solve over all records (cache_c=0; P applied). Genesis-style.
    reqs = [req(r["entity"], r["field"], r["cf"])[0] for r in records]
    my_edit(reqs, "alphaedit", P, cache)                  # single call, all records
    for rec in records: rec["expressed_at_apply"] = bool(predict(rec["prompt"])["id"]==rec["cf_tok"])
    applied = records
    # probe ALL rungs' worth at the end (batch has no intermediate rungs)
    post={p:predict(p) for p in set(unt_within+unt_cross+unt_global)}; ho=heldout_top1(post)
    print(f">>> BATCH N={len(records)}: ret={round(100*sum(predict(r['prompt'])['id']==r['cf_tok'] for r in records)/len(records),2)}% "
          f"| held-out edited-rel top-1 correct={ho['edited_rel']['top1_correct_vs_truth']}%", flush=True)
else:
    ... # existing sequential staircase loop (unchanged)
```
  Run both: `WRITE_MODE=sequential` (reproduces A0) and `WRITE_MODE=batch`. Compare held-out edited-rel top-1 at N=100.
- **PASS** (batch materially helps): batch held-out top-1 ≥ 80% (vs seq 41.7%). **PARTIAL:** 50–80%. **FAIL:** ≤50% (batch ≈ sequential — confirms MEMIT `E_mix`; batch alone is not the lever).
- **Predictions:** Likely **PARTIAL/FAIL** — theory says a same-relation batch concentrates the shared `k_r` and can be *more* rank-deficient (Perplexity); MEMIT `E_mix` predicts ≈average. If it surprises us with PASS, Genesis batching is itself a partial mitigation and Track D's drift model must distinguish batch vs incremental.
- **FORKS:** PASS → still run **A2** (sentinels likely stack); fold batch into the recipe. PARTIAL/FAIL → **A2** is the real lever (proceed); note batch alone insufficient in §13.
- **Spec ripple:** PASS → Genesis (§7.7) gains a locality argument for batching; OQ-W1 must separate batch/incremental. FAIL → confirms the fix must be the solve, not the schedule.
- **Advisor/Council:** Advisor flagged this as "the cheapest informative experiment, not in your list — you've only tested the runtime-incremental pattern and Genesis is batch." Council graph-data Pre-T2 (write-volume vs locality).
- **Novel/deep:** breadth-first relation re-solve (LocFT-BF) is the stronger batch variant if naive batch helps at all — periodically re-solve the whole relation block over accumulated keys + sentinels.

---
#### A2 · Relation-balanced in-solve sentinels (3 disjoint pools) · **DONE — PARTIAL (strong, directional). `CORPUS/15`, `D-A2-1`.**
RESULT: sentinels ~halve runtime-incremental cross-entity corruption — eval edited-rel 8/20→16–17/20 @N=100 (λ_s≈1–2; +8–9 probe lift ≫ 5%/probe noise), at retention (95→92%) + within (92.5→88%) cost. No λ_s clears ≥95%-eval+≥95%-retention → PARTIAL. Over-constraint wall past λ_s≈2. Robust trajectory: every arm still DECLINES N50→100 → entity-specific residual. Gates pass (gate2 bit-exact); control collapses; expr 100%; continent stable 100%. FORK→PARTIAL: A2b (recompute K_S) then A3 (BetaEdit) ±A4. D-A2-1 directional (single seed → no locked λ_s).
- **Objective / proves:** Does adding *held-out same-relation* sentinel keys `K_S` to the preservation term **inside the solve** prevent cross-entity read corruption at scale, while keeping write-side wins? This is the principled "address = relation + ENTITY" fix.
- **Spec refs:** §8.2 (D20 orthogonal-projection mandate — sentinels extend it), §7.3/§7.5 (relation families / polysemantic discipline), OQ-W1. **KB:** synthesis §3 (convergent #1); Perplexity rank-1 ("relation-balanced sentinels inside the solve; post-hoc is structurally late"); our Rung-3 history (post-hoc → 50%).
- **Rationale/evidence:** G6.1 mechanism — `cache_c` protects edited keys only; the high-variance shared `k_r` rides the editable subspace. Adding `K_S@K_Sᵀ` to the solve LHS forces ΔW to also preserve un-edited same-relation reads. Post-hoc Rung-3 failed (50%) *because* it was post-hoc (BetaEdit leakage); in-solve is the fix.
- **Deps:** cached Qwen2.5-3B + cov [4-8]; the screened pool (`g6_screen_qwen3b.json`, 56 entities). Time ~30–50 min. No download.
- **Method (pre-written — `a2_relbal_sentinels.py`, builds on `g6_scale_n.py`):**
```python
# ⚠️ FIX BEFORE RUN (advisor): 56 screened → 40/8/8 = N=80, which breaks N=100 comparability with A0.
#   RE-SCREEN the pool to ~70 entities first (expand g6_screen.py TRUTH dict + re-run), then split 50/10/10
#   for N=100 apples-to-apples with A0. (Pre-drafted split below assumes the re-screened ~70-entity pool.)
# THREE DISJOINT POOLS (anti-tautology, §2.3):
ents = list(sel.keys())                  # target ~70 screened (re-screen first)
edit_ents     = ents[:50]                # written  → N = 50 × 2 fields = 100 (matches A0)
sentinel_ents = ents[50:60]              # build K_S from these (held-out, protected)
eval_ents     = ents[60:70]              # measured (held-out, NEVER protected or edited)
assert not (set(edit_ents)&set(sentinel_ents)) and not (set(sentinel_ents)&set(eval_ents)) and not (set(edit_ents)&set(eval_ents))

LAMBDA_S = float(os.environ.get("LAMBDA_S","1.0"))   # sentinel preservation strength (sweep 0/0.5/1/2/5)

def sentinel_keys(layer, ctx):
    # K_S: down_proj input keys at the same relations, for held-out sentinel entities (NOT edited, NOT eval)
    reqs=[{"prompt":TMPL[f].format(e),"subject":e,"target_new":{"str":" x"}}
          for e in sentinel_ents for f in FIELDS]
    return compute_ks(model,tok,reqs,hp,layer,ctx).T.float().cpu()   # [d_in, n_s]

def my_edit_sentinel(requests, P, cache_c, Ks_per_layer):
    ctx=get_context_templates(model,tok); zl=L[-1]
    zs=torch.stack([compute_z(model,tok,r,hp,zl,ctx) for r in requests],dim=1)
    npd=dict(model.named_parameters())
    for i,layer in enumerate(L):
        K=compute_ks(model,tok,requests,hp,layer,ctx).T
        cur=get_module_input_output_at_words(model,tok,zl,[r["prompt"] for r in requests],
            [r["subject"] for r in requests],module_template=hp.layer_module_tmp,fact_token_strategy=hp.fact_token)[1].T
        tgt=(zs-cur); tgt=tgt.repeat_interleave(K.size(1)//tgt.size(1),dim=1); resid=tgt/(len(L)-i)
        Pi=P[i].cuda(); ca=cache_c[i].cuda(); Kg=K.double().float().cuda(); rg=resid.double().float().cuda()
        Ks=Ks_per_layer[i].cuda()                                   # held-out same-relation sentinels
        # add LAMBDA_S * Ks Ksᵀ to the LHS → solve preserves W·Ks (minimizes ΔW·Ks) IN-SOLVE
        A = Pi@(Kg@Kg.T + ca + LAMBDA_S*(Ks@Ks.T)) + L2*torch.eye(Kg.shape[0],device="cuda")
        B = Pi@Kg@rg.T
        upd = torch.linalg.solve(A,B).T.cpu()
        upd = upd_matrix_match_shape(upd.float(), npd[WN(layer)].shape)
        with torch.no_grad(): npd[WN(layer)][...] += upd.to(npd[WN(layer)].device, npd[WN(layer)].dtype)
        del Pi,ca,Kg,rg,Ks,A,B; torch.cuda.empty_cache()
    for i,layer in enumerate(L):                                    # accumulate edited keys (as in A0)
        K=compute_ks(model,tok,requests,hp,layer,ctx).T.float().cpu(); cache_c[i]=cache_c[i]+K@K.T
# Then: LAW#5 inertness gate (LAMBDA_S=0 must reproduce A0 exactly); compute_P(); precompute Ks_per_layer once;
#       run the same sequential staircase as A0 but via my_edit_sentinel; measure heldout_top1 on EVAL pool only.
```
  Sweep `LAMBDA_S ∈ {0, 0.5, 1, 2, 5}` (0 = inertness control = must equal A0).
- **PASS:** eval-pool held-out same-rel top-1 **≥ baseline−5 (≥~95%) at N=100**, no monotonic decay, write-side retention ≥95%, apply-expression ≥95%. **PARTIAL:** held-out 70–95% OR a λ_s exists that trades retention for isolation. **FAIL:** held-out <70% at all λ_s, or retention collapses (efficacy/specificity zero-sum wall).
- **Predictions:** **PARTIAL most likely.** Advisor's mechanism caveat: a *few* sentinel keys can't pin a *high-variance* shared direction — sentinels should help (≫41.7%) but may not reach 95% without trading efficacy (the λ wall). A clean PASS would be a major result (in-weight cross-entity isolation is achievable). FAIL → strong evidence the fix needs a different basis (A6 SAE) or hybrid (A5).
- **FORKS:** **PASS →** B1 (scale to Qwen3-4B) + lock A2 into the recipe + Track D. **PARTIAL →** A3 (BetaEdit leakage-aware solve, which may close the gap by also fixing pseudo-null leakage) and/or A4 (mid-late band may give the edit more non-shared room). **FAIL →** A5 (WISE side-memory hybrid for high-fan-out relations) becomes primary; A6 (SAE) the frontier bet.
- **Spec ripple:** PASS → in-weight DB cross-entity-viable; D20 should mandate sentinel preservation, not just orthogonal projection; OQ-W1 reframed (Track D). FAIL → spec must adopt a hybrid read-path for high-fan-out relations (A5) — a structural amendment.
- **Advisor/Council:** Advisor: in-solve not post-hoc; **3 disjoint pools (BLOCKING)**; expect possible insufficiency → informative either way. Council graph-data: "disambiguation anchors" / relation+entity addressing. Converges with Perplexity rank-1.
- **Novel/deep:** sentinels make the implicit covariance "relation direction" an *explicit, balanced* constraint. Open knob: sentinel *coverage* of the relation manifold (8 entities may under-sample → scale sentinel count; or sample sentinels by embedding-spread per RippleEdits similarity-mediation).

---
#### A2b · Recompute sentinel keys K_S per rung · **NEXT (cheapest, before A3)**
- **Objective:** A2's K_S is fixed from clean base → protects W·K_S against *clean-base* keys while W drifts under 100 edits → constraint goes STALE as N grows, possibly driving A2's N=100 falloff. Does recomputing K_S per rung close more of the gap?
- **Method:** in `a2_relbal_sentinels.py`, rebuild `Ks_sent=build_Ks(sentinel_ents)` at each rung boundary from the CURRENT model state; reuse cached cov/P; run λ_s≈1–2 + λ_s=0 control. Cov-reusing (~30–40 min).
- **PASS:** eval @N=100 ≥18–19/20 AND retention ≥95% → staleness was the limiter, fold in. **FAIL:** ≈ fixed-K_S → residual is entity-specific → A3 (BetaEdit) earned. Advisor-flagged as cheapest-informative before the 1–2 day port.

---
#### A3 · BetaEdit leakage-aware solve · **QUEUED (after A2b)**
- **Objective:** Port BetaEdit (history-aware + pseudo-null-leakage compensation) and test whether it reduces cross-entity decay vs A0/A2 — and whether sentinels (A2) stack on top.
- **Spec/KB:** §8.2/D20; synthesis §2/§5 (BetaEdit = SOTA successor, validated Qwen3-4B/[4-8]); Perplexity rank-1 evidence (stays nonzero at 10k edits where AlphaEdit collapses).
- **Deps:** PORT official repo https://github.com/lbq8942/BetaEdit (cloned to external_prior_art/BetaEdit; 'arXiv 2605.09285' was fabricated, repo cites IJCAI 2026) — extract solve into `g6_scale_n.py`; cached cov. Optionally Qwen3-4B (B1) to anchor vs published curves.
- **Thresholds:** PASS = held-out top-1 decay materially flatter than A0 AND ≥ A2 alone. PARTIAL = helps but < A2-sentinels. FAIL = no improvement (then the leak isn't the dominant term; basis change A6).
- **Prediction:** improves *general* sequential stability but, like its published specificity (43.9 @10k), **won't alone solve same-relation isolation** → best as the base solver A2's sentinels sit on. **FORKS:** PASS+stacks→ recipe = BetaEdit+sentinels → B1. else → A5/A6.
- **Ripple:** establishes the strongest in-weight base; informs whether spec's write engine should adopt history-aware null-space. **Novel:** combine BetaEdit history term + A2 sentinels = leakage-compensated *relation-balanced* solve (not in any paper).

---
#### A4 · C15 / BLUE band test (early [4-8] vs mid-late [18-22]) · **QUEUED (cov ready now)**
- **Objective:** Does editing in a C15-prescribed mid-late band reduce cross-entity bleed and/or change efficacy vs our early [4-8]? Resolves the CP3 C15 divergence + BLUE's "early layers are low-contribution/error-inducing."
- **Spec/KB:** §8.2 **C15** (L15–25/32L; our [4-8] diverges), CP3 (`CORPUS/09`); KB BLUE (`s240_literature_scan`), Perplexity (try a later band). 
- **Deps:** cached Qwen2.5-3B; **mid-late cov [18-22] computing now**. Time ~30–50 min. No download.
- **Thresholds:** informative comparison (not pass/fail of recipe). Outcome A: mid-late materially reduces cross-entity decay → C15 right, our band was the problem (spec keeps C15, we move band). Outcome B: no better → [4-8] not the cause; band is orthogonal to the cross-entity fix (feeds OQ-W2).
- **Prediction:** mid-late may *help modestly* (more entity-specific, less shared-syntax structure) but won't fully fix cross-entity (mechanism is relation-sharing, not band). **FORKS:** if mid-late helps → run A2 in the better band; either way → Track D + spec C15 note.
- **Ripple:** resolves an open spec divergence (C15 small-model recalibration, OQ-W2). **Novel:** band × sentinel interaction — a later band may give sentinels more non-shared room to satisfy both efficacy and isolation.

---
#### A5 · WISE-style side-memory hybrid (high-fan-out relations) · **GATED (on A2/A3 partial/fail)**
- **Objective:** Route high-fan-out relations (capital, language) to a frozen-base side memory with learned routing; keep low-fan-out facts in-weight. The ceiling-breaker.
- **Spec/KB:** matches spec's OWN tiered-memory hybrid (Git/.vindex partition; "stable→MEMIT, volatile→RAG"); Perplexity rank-3/WISE (locality 1.00); NotebookLM (WISE/ELDER/MELO). Refs LOCAL (`easyedit_*/wise`).
- **Deps:** WISE reference impl (local) arxiv 2405.14768 github PKU-YuanGroup/WISE; cached 3B. Medium effort (adapt routing + CPU serving).
- **Thresholds:** PASS = held-out same-rel top-1 ≥95% with acceptable router false-positive rate on unedited prompts AND CPU-serviceable. **Prediction:** likely achieves isolation (by construction) but at routing/generalization cost — the question is whether CPU overhead + paraphrase-robustness are acceptable.
- **FORKS:** PASS → hybrid recipe; Track E deployment must include the router. **Ripple:** if in-weight (A2/A3) caps out, this is the spec's path — a structural shift to a hybrid read-path; reframes "pure parametric recall." **Novel:** route by *measured per-relation interference slope* (Track D), not by relation-token — only relations that empirically bleed go to side memory.

---
#### A6 · SAE-guided entity/relation disentanglement (Qwen-Scope) · **GATED-FRONTIER**
- **Objective:** Use residual-stream SAE features to identify relation-general vs entity/value-specific directions; constrain the down_proj edit to move value/entity features while preserving relation-general features for held-out sentinels.
- **Spec/KB:** §7.5 polysemantic discipline; synthesis §5 (frontier); Perplexity/NotebookLM (BOTH confirm NO published residual-SAE→down_proj bridge); superposition theory.
- **Deps:** Qwen3-1.7B or 8B (SAE-supported) + Qwen-Scope SAEs (download, §6); reimplement bridge (multi-week). Forces model switch off 3B.
- **Thresholds:** PASS = isolation ≥95% via feature-space constraint where A2's covariance sentinels couldn't. **Prediction:** highest ceiling, highest risk; basis-mismatch (residual vs down_proj) may make the bridge leaky. **FORKS:** PASS → novel in-weight fix + paper-worthy; FAIL → confirms hybrid (A5) is the answer.
- **Ripple:** would turn "relation direction" from covariance artifact into an explicit feature basis — a fundamental upgrade to the write engine. **Novel:** the entire approach is unpublished; gate strictly on A2/A3 first (don't let new tooling pull focus).

### TRACK B — Scale / efficiency (rest of G6) · **GATED (on a Track-A fix worth scaling)**
- **B1 · Larger-model replication (Qwen3-4B → 8B).** Replicate G6.1 + the winning fix on Qwen3-4B (anchors against BetaEdit's published curves; tests size-density hypothesis: do smaller dense models collapse faster? — we already have 7B-clean/3B-fail). Deps: Qwen3-4B ~8 GB + cov ~2 h (§6). PASS = fix holds at 4B. FORK: holds → 8B + Track E; degrades → size-dependence is a spec deployment constraint (D1/G5). Spec ripple: sets the minimum viable deployment model size. KB: BetaEdit (4B/[4-8]); NotebookLM corpus-2 open-Q (small-dense density).
- **B2 · Overlay size-at-scale characterization.** Is overlay footprint O(1) band-dense (~81 MB) or O(N)? Reuse the staircase; report bytes/record. Characterization (gate only if operator sets a CPU storage budget). Spec ripple: CPU-deploy feasibility bound.
- **B3 · Real GGUF-Q4_K quantization survival.** Pull llama.cpp prebuilt (§6) → Q4_K_M → LARQL `gguf-to-vindex` → probe. PASS = edited-fact retention ≥ *native*-fact retention −3 pts (not "ppl rose less than sim"). FORK: fails → edited layers need higher precision; deploy story changes (E). Spec: § deployment. KB: G6_G7 pass-criteria draft.

### TRACK C — Multi-token value robustness (G7) · **QUEUED (independent of A)**
- **C1 · Diagnose Hanoi→"H".** Vary one axis at a time (token-length / value-frequency / entity / v_loss) against the working T2.3 8/8 set to NAME the failure mode. Prereq to C2. No threshold — produces the failure mode.
- **C2 · Harder multi-token grid.** Committed grid ≥24 values × (2/3/4/5 tokens)×(common/rare)×≥6 entities; PASS = full-value expression ≥95%, no cell <80%. Single-token control included. Spec ripple: if long/rare values truncate, in-weight values have a complexity bound → value-model amendment. KB: G6_G7 draft §G7.

### TRACK D — Capacity-law / spec reconciliation · **QUEUED (after first Track-A signal)**
- **D1 · Relation-fan-out-conditioned drift model.** Derive the actual capacity law: held-out interference slope as a function of (relation fan-out, N, model size, band, key-cosine concentration, pseudo-null leakage). Replaces OQ-W1's edge-count drift. Method: sweep fan-out × N across relations; fit interference onset. **This is the core spec-readiness deliverable** — it tells the spec what variable to monitor and what the safe write envelope actually is. Spec ripple: rewrites the §8 drift contract (warn/hard-stop become per-relation-fan-out, not global edge count). KB: synthesis §4 (OQ-W1 wrong variable); §7.2.

### TRACK E — Deployment (D1 / G5 hardware) · **GATED (on a validated store)**
- **E1 · CPU serving of the validated store.** Compile the validated edited model → LARQL/llama.cpp → serve + probe on CPU (pod proxy; operator Intel CPU if targeted). PASS = parametric recall holds on CPU at Q4_K with acceptable tok/s. Spec ripple: closes the deployment loop / confirms the CPU value proposition. KB: LARQL_INTEGRATION_ASSESSMENT; [[deployment-target-intel-cpu]].

### TRACK F — Spec implementation-readiness determination · **GATED (final)**
- **F1 · Reconciliation & determination.** Map every Track result → spec contract; produce the readiness determination + the precise spec amendments (drift model, D20 sentinel mandate, hybrid read-path if A5, C15 band, value-model). Output: updated spec + a "ready/not-ready, with conditions" verdict. The terminus of the runbook.

═══════════════════════════════════════════════════════════════════════
## §9 — MASTER DECISION-TREE MAP
═══════════════════════════════════════════════════════════════════════
```
A0 (DONE: cross-entity FAIL) ─► A1 (batch?) ──┬─ helps ──► fold batch in
                                              └─ no ─────► (expected)
                              ─► A2 (in-solve sentinels) ─┬─ PASS ───► B1 ─► B2/B3 ─► E1 ─► F1   [in-weight fix wins]
                                                          ├─ PARTIAL ► A3 (BetaEdit) ± A4 (band) ─┬─ PASS ► B1…►F1
                                                          │                                       └─ no ─► A5
                                                          └─ FAIL ───► A5 (WISE hybrid) ─┬─ PASS ► hybrid recipe ► E1 ► F1
                                                                                         └─ no ─► A6 (SAE frontier) ─┬─ PASS ► novel fix ► F1
                                                                                                                     └─ FAIL ► spec: in-weight cross-entity ceiling = X; mandate hybrid (F1)
A4 (band) feeds C15 spec note + OQ-W2 regardless.
Track C (multi-token) runs in parallel; Track D (capacity law) starts after first A-signal and is REQUIRED for F1.
Any branch's result → update §0.3, §12, §13, CORPUS, memory.
```
**Invariant:** every fork is selected by *pre-registered empirical thresholds* (§7.4), not by preference. Ambiguous data → `advisor()` before branching.

═══════════════════════════════════════════════════════════════════════
## §10 — SPEC IMPLEMENTATION-READINESS CHECKLIST
═══════════════════════════════════════════════════════════════════════
_Each maps experiment(s) → spec contract. Mark as evidence lands._
- [ ] Cross-entity isolation at scale holds OR a hybrid read-path is specified — **A2/A3/A5** → §8.2/D20, §7.3
- [~] Capacity law — **DIRECTIONAL DONE (D-D1-1, `CORPUS/22`):** global total-edge-count INSUFFICIENT; §8.7 drift must be relation-concentration-aware (two-variable). Quantitative thresholds/size-term PENDING (high-cardinality replication + B1) — **D1** → OQ-W1/§8.7, §22
- [ ] C15 band reconciled for small models (keep / recalibrate) — **A4** → §8.2 C15, OQ-W2
- [ ] Genesis batch write is locality-safe at scale — **A1** → §7.7
- [ ] Multi-token value fidelity bounded/known — **C2** → value model
- [ ] Real Q4_K survival + overlay size CPU-feasible — **B3/B2** → deployment
- [ ] CPU serving of the validated store confirmed — **E1** → D1/G5
- [ ] Governance (2PC/ledger/security/validation) — **CP1–G3 DONE** → §9/§10/§11/§20/§46
- [ ] All findings reconciled into spec amendments + readiness verdict — **F1**

═══════════════════════════════════════════════════════════════════════
## §11 — RISK REGISTER (result-invalidators + mitigations)
═══════════════════════════════════════════════════════════════════════
| Risk | Mitigation |
|---|---|
| **False-no-op** (unexpressed edit inflates locality) | Always measure apply-time expression separately (§7.4); expression gate. |
| **Tautology via overlapping pools** | 3 disjoint pools, asserted in code (A2). |
| **Metric mismatch** (JS ≠ top-1 claim) | Track top-1 AND margin AND KL; verdicts on the metric that matches the claim. |
| **Anchor-tuned thresholds** | Pre-register from DB-viability, not observed output (§2.3). |
| **GPU FP non-determinism** | Bit-repro is a non-requirement; verify behaviorally; report which-records-vary as noise. |
| **Disk exhaustion mid-run** | Pre-flight reclaim (§3.3) before downloads; durable outputs only to /workspace. |
| **Engine drift from a shim** | LAW#5 inertness gate every run (§2.4); λ_s=0 / empty-P controls. |
| **Same-model confirmation bias** | Independence discipline; advisor; empirical-only binding (§2.5). |
| **Over-investing in a frontier bet** | Gate A6 strictly on A2/A3 first. |

═══════════════════════════════════════════════════════════════════════
## §12 — LIVE STATUS DASHBOARD (machine-readable head — keep current)
═══════════════════════════════════════════════════════════════════════
| Exp | Status | Headline result |
|---|---|---|
| A0 G6.1 | DONE | SPLIT: write-side PASS; cross-entity FAIL — SEQUENTIAL (100→92→58→42%) |
| A1 batch-vs-seq | DONE | **PASS (robust): batch ELIMINATES cross-entity corruption — staircase FLAT 100→100→100% (vs seq 42%)**. Genesis(§7.7) clean @N≤100; runtime still needs A2. CORPUS/14, D-A1-1 |
| A2 sentinels | DONE | **PARTIAL (strong): sentinels ~halve cross-entity corruption** (eval edited-rel 8/20→17/20 @N=100, λ_s≈1–2) at retention/within cost; wall past λ_s≈2; every arm still declines N50→100 → A3. CORPUS/15, D-A2-1 (directional) |
| A2b Ks-recompute | DONE | **K_S staleness RULED OUT** — per-edit refresh doesn't help (large drift, zero benefit) → residual is entity-specific, not staleness. CORPUS/16 |
| A3 BetaEdit | PARKED | earned/ready (official `lbq8942/BetaEdit` cloned, ships qwen2.5-3b cfg); gated on a CONFIRMED incremental-write requirement (D-SCOPE-1). Not next. |
| A4 band test | QUEUED (cov ready) | mid-late [18-22] cov warmed; the [8-12] test is the C2-band falsifier (running) |
| A5 WISE hybrid | GATED(A2/A3) | — |
| A6 SAE | GATED-FRONTIER | — |
| B1 size-density | DONE | **PARTIAL: A1 batch-clean does NOT fully replicate at 7B** (held-out 100→91.7%). Scopes A1 to 3B/N≤100; feeds D1. CORPUS/19, D-B1-1 |
| B1 model-size term | **DONE (D-B1-2)** | **Concentration law REPLICATES on Qwen2.5-7B → §8.7 amendment is MODEL-GENERAL** (the win). Size threshold UNRESOLVED: 7B leans less-corrupted 7/8 paired cells (+11.5pp) but ≪ **~50pp run-to-run nondeterminism** (7B seed3 same-config 20.8→70.8 on re-run; 'collapse' was a noise draw, NOT a tail mode). **§8.7 structural amendment WRITTEN** (`docs/SPEC_8_7_AMENDMENT_DRIFT_CONCENTRATION.md`). `CORPUS/22` B1-section. NEXT-ARC: lower-variance instrument → numeric threshold → F1 → CP2. |
| B3/G6.2 quant | DONE | **PASS: A1-clean store survives real Q4_K_M** (edited 100% vs native 97.4%, Δ+2.6); margin-confound characterized. CORPUS/17 |
| B2 overlay size | OPEN | overlay `.vindex` size + CPU-feasibility at scale — not yet run |
| C2 keying+depth | DONE | **PRUNED + mechanism: relation-keying eliminated; same-relation key collinearity U-shaped, min L8-12.** New lead: band [8-12] sequential. CORPUS/20, D-C2-1 |
| C/G7 multi-token | OPEN | multi-token value robustness — directional only (T2.3); not yet run |
| C2-band falsifier | DONE | **PASS (mechanical) → NOT PROMOTED (real-but-underpowered)** (`CORPUS/21`, D-C2band-1): band [8-12] cross-JS +18.73pp BUT top-1 n.s. (p≈0.37) + within-loc −17.7pp + retention 96<98. Within-loc FALL + expr 100% → REAL redistribution (not under-editing), but underpowered (1 seed) + within-entity top-1 cost & mechanism UNMEASURED → NOT promoted; not a recipe change. Cross-family-reviewed (gpt-5.5, FIX-FIRST, concurs): causal 'real band effect' OPEN until the norm-matched/sham control (c, now primary). Mechanism hyp D7. |
| D1 capacity law | **DONE (PARTIAL, dual-reviewed)** | **global total-edge-count INSUFFICIENT; §8.7 drift must be relation-concentration-aware** (concentration vs dilution @ fixed N=50: concentrated more corrupted 4/4 seeds, gaps 50/16.7/41.7pp). 2 CONFIRM+1 PARTIAL+1 INVALID → **two-variable law** (concentration + small cross-relation term). **Phase 3 REPLICATED clean** (language dilutant 100% expr, 3 seeds): concentration-dominance holds (R_pure k24 51%→k36 24% @fixed N=48); cross-relation term a small non-negative tendency (low-power paired sign, magnitude unresolved). Thresholds UNSET; **size-term DONE (B1/D-B1-2)**. `CORPUS/22`, D-D1-1. |
| E1 deploy | DONE | **SPLIT: Claim A PASS** (CPU serve via llama.cpp+Q4_K_M, ~8–13 tok/s) / **Claim B FALSIFIED** (LARQL gguf-to-vindex drops 108 attn biases on Qwen2.5; A7 causal). Model-family split. CORPUS/18, D-E1-1 |
| F1 readiness | GATED(final) | gated on D1 + CP2 |
| _bg_ band cov [18-22] | DONE | warmed for A4 |

═══════════════════════════════════════════════════════════════════════

- **D-D1-2 ⟨D-D1-2@e023d8d2⟩** (2026-06-21): §8.7 numeric-threshold instrument → **operational guardrail `k≤1`** (REVISED from k≤2 after seed-2 across-held-out; anchor by k=2, WARNING k=2-3, HARD k=8-10; + mixed-load needs a global-volume bound). Dual-reviewed (Opus advisor + gpt-5.5 cross-family, inline). k=3-4/k=10-12 = scoped order-dominated observations (one toxic order drives them), NOT portable thresholds; Wilson UCB retired (clustered units→order-bootstrap). Per-relation count = fail-closed SENTINEL, not the causal var (edit-set/key-collinearity geometry). 3B-only (size transfer OPEN), pure-capital anti-conservative, incremental-path-only (deploy=batch/Genesis A1-clean). Instrument: 3B within-process SD=0; ~50pp noise is 7B/across-process; binding 3B uncertainty = edit-ORDER. `docs/SPEC_8_7_AMENDMENT_DRIFT_CONCENTRATION.md` §4, `docs/SPEC_8_7_THRESHOLD_INSTRUMENT_PREREG.md`, CORPUS/22.

## §13 — CHANGELOG (append-only)
═══════════════════════════════════════════════════════════════════════
- **2026-06-18** Runbook created. Encodes: G6.1 SPLIT result; mechanism consensus (3 research docs + our data); candidate ranking; BetaEdit finding (reframes Qwen3-4B); OQ-W1 "wrong variable" spec finding. Tracks A–F scaffolded; A1/A2 code pre-written; mid-late cov warming for A4. Decisions ledger seeded.
- **2026-06-18 (later)** Advisor review → runbook blessed done with 3 fixes applied: (1) pre-written code marked pre-drafted/unvalidated (§8); (2) unverified spec refs C2/C4/§46/§20.3/§11.13/D20/OQ-W2 tagged verify-before-cite (§4.2); (3) A2 pool-math fixed (re-screen ~70 → 50/10/10 for N=100). **A1 LAUNCHED** (batch mode, `g6_scale_n.py WRITE_MODE=batch`, running). New learnings saved: [[evidence-over-scaffolding]], [[match-metric-to-the-claim]]. NEXT on resume = read A1 result → resolve fork → A2 (re-screen first).
- **2026-06-18 (A1 DONE = PASS)** Batch (single joint solve) **ELIMINATES** the G6.1 cross-entity corruption: held-out edited-rel top-1 staircase **FLAT 100→100→100%** (N=26/50/100) vs sequential 92→58→42%. Surprise PASS → advisor-mandated batch's-own-staircase confirmed flat (eliminates, not defers). Mechanism: cumulative `cache_c` leakage from the incremental schedule, not in-weight storage. Resolves Genesis/§7.7; runtime path needs A2. `D-A1-1`, `CORPUS/14`. Fixed output-path-collision bug; A0 regenerated (collapse 92→50→33%). [[durable-artifact-path-collision]].
- **2026-06-18 (A2 DONE = PARTIAL)** Relation-balanced in-solve sentinels ~halve runtime-incremental cross-entity corruption: eval edited-rel **8/20→16–17/20 @N=100** (λ_s≈1–2), at retention (95→92%) + within (92.5→88%) cost; wall past λ_s≈2; every arm still declines N50→100 → entity-specific residual → A3. Re-screened to 78 (`g6_screen_qwen3b_v2.json`, NEW file); seeded 50/10/10 pools. Both gates passed (gate2 bit-exact Δ=0.000000); control collapses; expr 100%. `D-A2-1` (directional). FORK: A2b (recompute K_S) → A3 (BetaEdit) ±A4. `CORPUS/15`.
- **2026-06-18 (INFRA)** Edit-tool writes to THIS runbook reverted this session (network FS `mfs#…runpod.net` over FUSE); Bash/python writes persisted. Re-applied §0.3/§8/§12/§13/§5 via python. Authoritative handoff = SESSION_CHECKPOINT.md + CORPUS. Learning [[verify-canonical-state-edits-persist]].

- **2026-06-18 (scope gate RESOLVED, D-SCOPE-1)** Operator deferred; advisor-checked. Deployment = edit-offline-GPU → COMPILE → serve-CPU = the batch-rebuild model; A1 already pins batch at 100% (no A3 headroom there); no stated incremental-write requirement. **A3 PARKED** (earned/ready/gated on a confirmed incremental requirement). **NEXT = B3/G6.2** real Q4_K_M quantization survival on the A1-clean batch store (the literal CPU-deployment falsifier). New memory [[scope-gate-batch-is-deployment-model]].
- **2026-06-18 (B3/G6.2 DONE = PASS)** Real Q4_K_M (4.99 BPW, self-built llama.cpp CPU) quantization survival on the A1-clean batch store: edited-fact retention 100% (99/99) vs native-country 97.4% (75/77), Δ=+2.6 (threshold ≥−3) → PASS. Validity gate (HF↔GGUF-fp16 agreement) 100% edited+native; smoke confirmed band-[4-8] edit survives conversion; CPU inference served correct edits (partial E1). Margin confound CHARACTERIZED not just caveated (`b3_margin.py`: edited top-1 margin median 0.979 vs native 0.812 → claim scoped to 'edits survive Q4_K_M', not 'indistinguishable from native'). `CORPUS/17`. New memory [[q4km-quantization-survival-pass]]. NEXT live falsifiers: E1 / B1 / C-G7 / D1.

### §13 changelog — 2026-06-18 (post-B3)
- E1 done (SPLIT: A PASS via llama.cpp / B FALSIFIED, LARQL Qwen2.5 bias-drop; A7 causal). B1 done (PARTIAL, 7B 91.7%). C2 done (PRUNED + L8-12 mechanism map). CORPUS 18/19/20; D-E1-1/D-B1-1/D-C2-1. Hypothesis register added (`docs/HYPOTHESIS_REGISTER_2026-06-18.md`).
- Repo reorganized to publication grade: experiments/ configs/ results/ logs/ docs/ archive/ tree; 359 loose files moved; 40 live scripts path-rewritten to LLMDB_ROOT (ast-verified); stale subdirs archived; empties deleted. README + REPRODUCIBILITY + EXPERIMENT_REGISTRY authored. Snapshot at /root/migration_backup. Learnings: bias-ablation = causal-attribution method; key-collinearity layer map; recurred artifact-path collision ([[durable-artifact-path-collision]]).

### §13 changelog — 2026-06-19
- **§12 dashboard reconciled to post-B3 reality** (was stale: B1/B3/E1 still showed GATED; A2b/A3/C2/_bg_ stale). Now: A2b DONE (CORPUS/16), A3 PARKED (D-SCOPE-1), B1 DONE-PARTIAL (CORPUS/19), B3 DONE-PASS (CORPUS/17), C2 DONE-PRUNED (CORPUS/20), E1 DONE-SPLIT (CORPUS/18), B2/C-G7 marked OPEN, D1 QUEUED (critical path), F1 GATED on D1+CP2. **No new scientific result claimed — dashboard sync + run-launch record only.**
- **Autonomy `c2band_falsifier` LAUNCHED & RUNNING** (`tools/autonomy_driver.py --mission tools/autonomy_mission.json --mode batch --budget-min 180`): [4-8] vs [8-12] sequential @N=100, metric `unt_cross_loc`, pre-registered PASS≥5pp / PARTIAL>1pp / FAIL≤1pp, guard edit-success≥95 both arms. STAGING-ONLY (logs/pending_findings/); driver does NOT write CORPUS/ledger/runbook. **Verdict pending** — operator folds on close per §0.4.

### §13 changelog — 2026-06-20
- **C2-band falsifier SUPERVISED FOLD-IN (`CORPUS/21`, D-C2band-1).** Autonomy run (2026-06-19) had completed (results/c2band_*.json @10:01) but was staged LABEL=ERROR (wall-clock expired before post-run staging). Mechanical label = **PASS** (corruption_reduction_pp=18.73≥5, guard cleared). Supervised deep-thinking (DISCIPLINE §2) + independent adversarial review → **NOT PROMOTED to PROVEN (real-but-underpowered redistribution):** top-1 leg n.s. (7/12→10/12, Fisher p≈0.37); within-entity JS −17.71pp (monotone; global fine) + retention 96<98 → a REAL direction-specific REDISTRIBUTION (within-loc FALL refutes a weaker edit; expression 100% both arms excludes under-expression), traded against a within-entity perturbation + durability cost (ret 96<98). NOT promoted = underpowered (single seed) + within-entity TOP-1 cost & basis-rotation mechanism UNMEASURED. NOT a deployment recipe change (batch path clean at [4-8]); mechanistic only. Deep-thinking yield = hyp **D7** (depth rotates key basis relation-clustered→entity-clustered; predicts same-entity cross-relation collinearity inversely-U, HIGHER at L8-12 — UNMEASURED). De-confounders (a)-(d) queued; (a) no-edit collinearity curve + (b) within-attr top-1 gate. Updated CORPUS/00,03,21; PROGRESS ③⑤; hypothesis register §I; checkpoint; staged finding corrected. **Cross-family review run (gpt-5.5 via Codex+ChatGPT-OAuth, evidence-fed) = `FIX-FIRST`: concurs PASS-not-promoted; calibrated the claim to 'redistribution, not a *uniformly*-weaker edit' (Δ-norm/depth confounds OPEN); elevated the norm-matched/sham control (de-confounder c) to THE primary overturning gate. Independence obligation CLOSED.** Codex cross-family review now wired (model gpt-5.5, `tools/setup_codex.sh`, `.codex/skills/advisor-review`).

> **Always-in-context discipline:** load `DISCIPLINE.md` — north-star goal (F1), context read-triggers, deep-thinking-on-failure protocol, and tool/loop thresholds (binds Claude + Codex).

### §13 changelog — 2026-06-20 (D1 capacity law)
- **D1 DONE = PARTIAL (dual-reviewed), directional claim PROMOTABLE (`CORPUS/22`, D-D1-1).** Phase 1 no-edit predictor map (covariate capital>lang>cont; D7 weak-moderate). Phase 2 concentration-vs-dilution @ fixed total-N=50 (Qwen2.5-3B band[4-8] seq; LAW#5 gate |Δ|=0.0007; fixed disjoint 12-entity held-out), 4 seeds×2 orderings: concentrated (50 capital) more corrupted than diluted (17 cap+33 other) at equal total-N in 4/4 (gaps 50/16.7/41.7pp; seed3 INVALID=continent under-expression). → **global edge_count_since_anchor INSUFFICIENT; §8.7 drift must be relation-concentration-aware** (OQ-W1 reconciliation, directional). Valid seeds 2 CONFIRM+1 PARTIAL → **two-variable law** (concentration + smaller cross-relation term), thresholds/size-term UNSET. Dual-reviewed: Opus advisor + gpt-5.5 cross-family (`FIX-FIRST` applied: PARTIAL not CONFIRM; 'insufficient' not 'falsified'; two-variable not 'dominant'; seed2@100%-dilutant rebuts weak-dilutant confound). Independence CLOSED (directional). Artifacts `experiments/track_d/{d1_predictor_map,d1_concentration_sweep}.py`, `results/d1_*`, `docs/D1_CAPACITY_LAW_PREREG.md`. **INFRA:** restored `transformers==4.51.0` pin after pod-restart wipe ([[pod-restart-wipes-system-python-ml-stack]]). NEXT: clean high-cardinality-relation replication + B1 size term → quantitative law + §8.7 amendment for F1.

### §13 changelog — 2026-06-20 (D1 Phase 3 — clean replication)
- **D1 Phase 3 DONE — clean high-cardinality dose-response REPLICATES the two-variable law (`CORPUS/22` updated, `results/d1_dose_response_result.json`).** Dropped cardinality-4 continent (currency's confident pool also collapses to ~5 euro-values) → only capital+language clean high-cardinality. Dose-response at FIXED total-N=48 (capital block→R_pure→language block→R_after, within-arm paired; 24 baseline-correct held-out; 3 seeds; LAW#5 gate ✓ |Δ|=0.0015 after fixing a measure-after-restore gate bug — science path unchanged). **Language dilutant 100% expression all 9 arms** (continent confound eliminated). **Concentration dominates (replicated):** R_pure means k24 51.4%→k36 23.6%→k42 26.4% (base 100%). **Cross-relation term — a small NON-NEGATIVE tendency:** paired deltas 6 positive/3 zero/0 negative → frozen rule cross_real=False (mean 3.7pp ≤ 4.2pp single-set granularity) is UNDERPOWERED; the paired sign is a LOW-POWER directional signal (NOT a precise effect size). Two-variable framing holds; cross-term magnitude UNRESOLVED (per gpt-5.5 cross-family review: don't headline the sign-test p as an effect size). Triple-reviewed (Opus advisor caught a near-over-correction to 'single-variable'; corrected). NEXT: B1/Qwen3-4B model-size term.
### §13 changelog — 2026-06-21 (B1 model-size term)
- **2026-06-21 (B1 size term DONE — D-B1-2; `docs/SPEC_8_7_AMENDMENT_DRIFT_CONCENTRATION.md`).** Ported D1 dose-response to Qwen2.5-7B (`experiments/track_b/b1_size_dose_response.py`; results `results/b1_{3b,7b}_dose_response_result.json` + `_seeds123/_seeds345` backups; logs `logs/b1_{3b,7b}_*`). Matched in-session 3B reference re-run (REPLICATE). **Concentration law REPLICATES on 7B** (monotone on means, expr 100%) → §8.7 per-relation-concentration amendment is **model-general** (the win). **Size term UNRESOLVED — weak protective lean** (7/8 paired cells favor 7B, +11.5pp, after removing a proven-noise seed3) swamped by **~50pp run-to-run nondeterminism** (7B seed3 same-config 20.8%→70.8% on re-run; advisor-mandated reproducibility check showed the 4–21% 'collapse' was a non-reproducible noise draw, NOT a tail mode). LAW#5 gates PASSED (|Δ|=0.0000–0.0003); harness VRAM fixes (eigh-for-symmetric-PSD-P, diagonal-add, del-Pi-before-solve, expandable_segments) proven inert (`torch.equal` + cov symmetry residual 0.0 + 3B old-vs-new-harness norms match ~2%). **§8.7 structural amendment written as operator proposal**; numeric threshold blocks on a lower-variance instrument (deterministic/higher-N — NEXT-ARC). Dual advisor pass. New memories [[sequential-edit-run-nondeterminism]], [[wide-intermediate-7b-editing-vram]]. NEXT: F1 readiness framing + CP2 schema build-items.
- **2026-06-21 (D-D1-2 ⟨D-D1-2@e023d8d2⟩ — §8.7 numeric-threshold instrument DONE)** **D-D1-2** (2026-06-21): §8.7 numeric-threshold instrument → **operational guardrail `k≤1`** (REVISED from k≤2 after seed-2 across-held-out; anchor by k=2, WARNING k=2-3, HARD k=8-10; + mixed-load needs a global-volume bound). Dual-reviewed (Opus advisor + gpt-5.5 cross-family, inline). k=3-4/k=10-12 = scoped order-dominated observations (one toxic order drives them), NOT portable thresholds; Wilson UCB retired (clustered units→order-bootstrap). Per-relation count = fail-closed SENTINEL, not the causal var (edit-set/key-collinearity geometry). 3B-only (size transfer OPEN), pure-capital anti-conservative, incremental-path-only (deploy=batch/Genesis A1-clean). Instrument: 3B within-process SD=0; ~50pp noise is 7B/across-process; binding 3B uncertainty = edit-ORDER. `docs/SPEC_8_7_AMENDMENT_DRIFT_CONCENTRATION.md` §4, `docs/SPEC_8_7_THRESHOLD_INSTRUMENT_PREREG.md`, CORPUS/22.

### §13 changelog — 2026-06-21 (B3 in-weight-necessity decision)
- **2026-06-21 (D-B3N-1 — B3 in-weight-necessity DECISION TAKEN; `docs/B3_IN_WEIGHT_NECESSITY_DECISION.md`).** The highest-stakes open F1 architecture item (hypothesis-register "B3"; distinct from the *quantization* decision in CORPUS/17). **Reasoned architectural position, NOT an empirical PASS** (no single pre-registered falsifier; the necessity claim decomposes into discriminating requirements). Decomposed into two primary axes — **A (READ):** in-weight's only contractually-relevant unique value = forward-pass "native knowing" (spec line 90), which is a **stated paradigm PREFERENCE, not a tested hard requirement** — the *enforced* read contract (L1 SELECT read-back §391, reverse-lookup/bidirectional D4 §287, multi-hop/aggregation) is satisfiable by a structured side-store **given reliable NL→query routing** (EV-2: KG ≥ vector-RAG on multi-hop, directional); no latency SLA exists (p95_latency_ratio tolerates 2× §846; reads block during mount §642). **B (WRITE):** our corruption evidence (G6.1/CORPUS/13, D-D1-2 k≤1/CORPUS/22, mixed-load) is **INCREMENTAL-path-only** — the batch/genesis path is CLEAN at scope (A1 100% / B3 quant-survives / E1 CPU-serves) → do **NOT** count incremental corruption against batch. **VERDICT = scope-keyed conditional HYBRID:** in-weight VIABLE-AT-TESTED-SCOPE for the batch/genesis core (3B/N≤100); route incremental-high-churn to a gated/structured side-store; §8.7 `k≤1` attaches to incremental/residual mode, not the batch core. F1 to be written as this hybrid (not a blanket "in-weight ready"). **Open §1.1 dims deferred to F1:** auditability/observability, delete/update governance, security/trust-boundary, routing reliability, operational cost (several favor side-store; trust-boundary favors in-weight). External side-store leads = directional priors only (DISCIPLINE §3; only NeuralDB independently confirmed). Dual-reviewed: **advisor** (pre-authoring — set the two-axis frame, caught the double-count + confirmation-bias traps) + **gpt-5.5 cross-family FIX-FIRST** (8 fixes applied: axes not exhaustive→§1.1; routing caveat; "viable at scope" not "architecture-final"; guardrail-placement fix; demote "field convergence"→"leads aligned"; latency "suggestive"). Hypothesis-register B3 → RESOLVED. New memory [[in-weight-necessity-is-scope-keyed-hybrid]]. **NEXT:** 7B numeric-transfer (OQ-W1) → CP2 schema build-items → write F1. **Operator Q surfaced:** batch-only or incremental-at-scale deployment profile? (biggest single F1 lever).
