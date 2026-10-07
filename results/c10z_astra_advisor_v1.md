Verdict: FIX-FIRST

**Single most important fix:** the LAW#5 block has no check whose answer depends on the active algebra or on the key-capture locus. Z3 sets every deficit to 0, so λ = 0 for any A, right or wrong. Z1 checks x_t, s_t and the competitor but never k. Z4 checks that the A assembly and the δw assembly agree, but both read the same captured k, D, d and s, so a shared bug passes it. A key captured one position off, at a padded index, or under the wrong layer key would pass Z0–Z6 and yield a plausible UNDERFIT or NULL. Add Z7 (item 1): an independent key-locus check plus a layer-35 single-requirement reduction whose answer is known analytically.

Reviewer: Claude Opus 5.5 (`claude-opus-5-5`), independent adversarial advisor pass on `docs/C10Z_ASTRA_PREREG.md` v1 DRAFT, 2026-10-07. Method: `tools/advisor_review_prompt.md`. Read-only; no model, tokenizer or GPU job; no git state change. The paper was checked through the arXiv MCP: LaTeX §3, §4 and §5, plus text search of the rendered v1 for the macro-expanded numbers.

## Defect-class check (calibrated against `results/c10x_enginepath_advisor_v1.md`, `results/c10y_directdw_advisor_v1.md`)

| class | status in C10Z v1 | evidence |
|---|---|---|
| LAW#3 baseline gated before candidates | **Mostly fixed, one ordering defect** | The in-driver gate runs at stage 0 step 4 (`docs/C10Z_ASTRA_PREREG.md:121`). Step 2 (`:119`) runs ASTRA observation code (Z0) before recipe A and the gate, and in process 1 it cannot run at all (item 2). |
| LAW#5 reduction exercising the new path | **Not met** | Z3 (`:143`) is vacuous for the algebra; nothing checks the k locus (item 1). |
| Pristine-weight hash | **Met** | `H_pristine` over all parameters, plus per-layer `down_proj` hashes and safetensors hashes (`:118`); Z6 at named points (`:146`); cross-process equality (V3, `:204`). |
| Complete, non-overlapping truth table | **Met for the base label** | T1–T5 (`:237–243`) partition every (n, g, S) with a ∈ [5, 18]. Boundaries are stated (g = 9 → T2, g = 10 → T3; n = 18 → T1). Gaps remain in the attribution reading (item 4) and the replication rule (item 8). |
| Underfit gate | **Met for Z, missing for Z-band** | Rule U (`:220`, `:247`) is present. Z-band attribution has no fit gate (item 4). |
| Early-kill stage | **Met** | K1 (`:251`) gives stage 0–1 at ≈ 62 min (`:186`). |
| Restore trap (all 36 `down_proj`) | **Met, with two additions** | See Q4 below. |

## Adjudications requested

**Q1 — Write qualification: WRITE-QUALIFIES**, under conditions. The operator rules; this is my recommendation to them.

The ruling (`EXPERIMENT_RUNBOOK.md:330`) and its criterion (`results/research_pass_2026-10-06/recommended_sequence.md:13`) say what is excluded: "a training set or a training loop per commit". They name three harms: real-time use, the audit trail and compaction. ASTRA passes on each, for the following reasons.
- **No gradient and no optimiser.** Each round solves one linear system exactly (paper §3.4: "no optimizer, no step size and no backward pass"). Step 7 was classed as training because it back-propagates an LM loss into weights (`results/c10y_directdw_advisor_v1.md` Scope A; recorded at `EXPERIMENT_RUNBOOK.md:343` (2)). ASTRA does neither.
- **Re-linearisation is already part of the accepted engine.** This is the draft's strongest argument, and it does not make it. `my_edit` writes layer i (`c10e_bandknob.py:216–217`), then re-reads K and `cur` from the edited model for layer i+1 (`:196–201`). That is an observe–solve–write iteration over layers. ASTRA runs the same construct over ≤ 10 rounds on fixed columns. The engine also runs up to 25 Adam steps per fact inside `compute_z` (hparams `:6`). That optimisation acts on an activation, not on weights, but it is still more per-commit optimisation than ASTRA has.
- **The three harms:**
  - real time: forward passes only, with a hard cap of 10 rounds; W2 measures it;
  - audit: the inputs are the patch plus hashed fixed artefacts (`H_in`, `:132`);
  - compaction: ≤ 10 batch forwards per fact set, against `compute_z`'s 25 forward+backward steps per fact.
- **The paper's own framing:** "A repair that takes seconds and needs no training loop" (§5, verified).

Conditions:
- (a) The round cap and the stop rule are part of the compile specification. An "iterate until fit" variant with no cap would drift toward a training loop.
- (b) Regeneration is measured behaviourally, not assumed (item 7).
- (c) The F² growth of the joint system at compaction (`:40`, `:296`) is the genuine scaling caveat. It belongs in the route ruling, not in this run.

The §8.2 designated-engine question is separate and needs an amendment either way (`:42`). The draft gets this right.

**Q2 — Fidelity to arXiv 2610.05277 (verified, v1).** Checked and correct:
- Title and authors.
- §3.1: four views; the key is the product of the activated gate and up projections; the RMS scale with no epsilon.
- §3.2: competitor = highest logit other than y_t; c_t = (W_y − W_p) ⊙ g; d_t = G⁻¹c/(cᵀG⁻¹c).
- §3.3: SemCon formula; quarter of the layers; R = 16; bounds 16 and 4 % of N; selection once in round 1, with the quoted "a fixed set keeps the patch within its budget and lets later rounds refine the same columns".
- §3.4: δw formula; A_tu; D = inverse mean squared key activation on reference prompts; ridge "a fraction of the mean diagonal entry"; "no optimizer, no step size and no backward pass".
- §3.5: stop when nothing fails, or after 10 rounds; the final patch is the sum of the rounds.
- §4 Configuration: μ = 5; 6, 8 and 8 layers kept; D from 32 prompts of the other benchmark; bfloat16.
- §4.2: none in the first 58 % of the depth; last three layers in ≥ 97.0 %.
- §4.3: −34.2, −31.4, −6.5 (and −4.4 for two views); 2.7 s; "a lead of one logit does not survive"; "each round needs one forward pass per view and one small linear solve".
- §4.4: BLEU-RPD −4.11 / −0.14 / −2.03 %.
- Section numbering: the rendered text prints "4.4. Side Effects and Robustness", so the MCP outline's "5.x" is offset by one. D-16 is right.
- No code link in the paper (searched "github" and "available": no hit).

Flags (all ADVISORY, item 10):
- "one requirement per failing token" is in quotation marks as §3.4 (`:31`). The paper's words are "each failing token adds one requirement to the patch" (§3.3).
- "2.7 s per repair on a GPU" (`:40`) omits the paper's caveat that times were measured "while several processes shared a GPU, so their ratios are the meaningful quantity".
- "0.22–0.95 %" (`:77`) pools two ranges: 0.76–0.95 on the 1B model and 0.22–0.52 on the 8B/9B models.
- H-Z2 (`:52`) credits unseen-phrasing robustness to the views alone. §4.4 credits "the views and … the margin".
- §6 (g) marks the W1 scale UNVERIFIED (`:313`). It is verifiable: see item 6.

No invented mechanism is presented as the paper's. D-1–D-15 label the departures honestly.

**Q3 — Feasibility on the M3 Pro (48 GB, MPS, fp16): FEASIBLE.**
- My arithmetic matches the draft:
  - |S| 1,152–2,304 and n_L 128–256 (A7); 43 (A1) and 86 (A2);
  - F ≤ 864;
  - round-1 captures 864 × 36 × 11008 × 4 B = 1.37 GB;
  - G is 151,936 × 2048² × 2 ≈ 1.27 TFLOP in float64 on CPU (seconds to a minute);
  - a round is one forward of ≈ 4,032 tokens × ≈ 6.2 GFLOP ≈ 25 TFLOP;
  - peak ≈ 14.3 GiB (sum re-added).
- All float64 work is on CPU, as `memit_main.py:191–194` requires.
- The D-statistics source is available offline: `hf_cache/datasets/wikimedia___wikipedia` exists, and its lock file names 20231101.en.
- One correction: HF computes logits at every position unless told otherwise (`.venv/.../transformers/models/qwen2/modeling_qwen2.py:838–839`, `logits_to_keep = 0` → all). That is 144 × T_pad × 151,936 × 2 B ≈ 1.2 GB at T_pad = 28, not the "≤ 0.26 GB" of `:173`. It is harmless for memory, but the driver must say which path it uses (item 11).
- My additions (Z7 ≈ 2–3 min; F1 and subject-free probes at all prefix depths ≈ 2–4 min per arm) keep stage 0–1 under 1.5 h.
- The "34 min = 23 min eval + 11 min solves" split (`:183`) is an interpretation of the brief's anchors. It is UNVERIFIABLE from the repo. The C10X pass measured 26–30 min per three-arm recipe (`results/c10x_enginepath_advisor_v1.md`, issue 13). Either anchor gives the same budget conclusion.

**Q4 — The restore trap: the finding is correct, and the remedy is sufficient and correctly placed, given two additions.**
- Confirmed: `snap_layers` and `restore_layers` iterate `hp.layers` only (`c10e_bandknob.py:150–152`, `:155–159`). `run_recipe` restores only from `base_snap` (`:473`, `:506`). The `described_as` baseline is taken before `my_edit` (`:475–476` vs `:489`), so the wrapper's restore at entry would come too late for it. The remedy has three parts:
  - `restore_hook` as the last `ARM_HOOKS` entry, which runs after every readout (`:494–495`) and before the next arm's `:476`;
  - Z6 before each `run_recipe`, because `base_snap` re-snapshots whatever it finds (`:461`; C10X issue 2);
  - the wrapper's restore at entry.

  Together these cover every read of the model.
- **Addition (a), exception path.** If `my_edit`, `eval_arm` or a hook raises, `run_recipe` does not restore anything. Wrap each `H.run_recipe` call in the driver with `try/finally`: copy `PRISTINE` into all 36 `down_proj`, check Z6, write the halt diagnostic, exit non-zero. No later recipe runs in that process.
- **Addition (b), residual hooks.** The capture pre-hooks on `down_proj` and `model.norm` must be gone before any evaluator forward. Assert, after every observation and at the entry of every `eval_arm` call (through `probe_hook` or the wrapper's return), that `len(m._forward_hooks) == len(m._forward_pre_hooks) == 0` for all 36 `down_proj` and for `model.norm`. Record it. This is C10Y issue 6 (viii); its absence here is a regression.

**Q5 — Answers to the draft's §6 questions (`:307–314`).**
- **(a) Views.** Keep the six engine views for v1. H-Z2 already names their weakness. But the shared contract requires a normalised-overlap audit against `PTEST` for every non-triple write input (`results/research_pass_2026-10-06/prereg_stubs.md:12`), and the frozen templates are such an input. Add the audit (item 9). Deterministic renderings belong to the PARTIAL or H-Z2 follow-up prereg.
- **(b) Joint vs independent; T = ΣT_i.** Joint is right for comparability with recipe A in the Genesis shape. T = ΣT_i keeps the paper's 16 neurons per answer token (the paper counts a token once, not per view, §3.3). Add a per-fact readout: the share of Σ|δw| carried by carriers whose largest key falls on that fact's positions. That way a fact-dominated carrier set is visible.
- **(c) Null-space weights.** 1,000 Wikipedia rows is closer to the engine's covariance source than 32 off-domain prompts; accept it. The floor at 10⁻³ of the median: accept, and record the floored count (already planned). For V7, use all nine cached layers 4–12 (`covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/`, listed: layers 4–12), not only 4–8. Layers 9–12 sit nearer the depth ASTRA picks. Keep 0.80.
- **(d) Margin.** Yes: record the pristine lead distribution as non-gating. Also record recipe A's post-write identity-view leads per position. They show how much margin the closed form leaves, which is the direct comparator for μ = 5. Keep μ frozen.
- **(e) LAW#5 sufficiency.** No: see item 1.
- **(f) Fit thresholds.** φ_μ ≥ 0.95 and φ_0^id ≥ 23 are acceptable. Specify the post-loop observation (item 12).
- **(g) W1 = 1.0.** Too loose by about 2–4× against the paper's verified numbers; see item 6.
- **(h) Stacked variant.** Correctly left out of v1. It mixes two writers and two sites and needs its own prereg.

## Issues (priority order)

### 1. BLOCKING — LAW#5: Z3 is vacuous for the algebra, and no check ties the captured keys to their positions and layers

**Defect.**
- Z3 (`docs/C10Z_ASTRA_PREREG.md:143`) sets γ ≡ 0. `solve(A + ρI, 0) = 0` for any non-singular A, so (a)–(d) pass whether A, d, D or k is right or wrong. It is the "seam present but reduced to identity" pattern (C10X issue 3).
- Z1 (`:141`) reconstructs the lead from x_t, s_t, g and W. It never touches k.
- Z4 (`:144`) proves that the δw assembly and the A assembly agree. Both consume the same captured `k^l_{j,t}`, the same position table and the same layer dictionary, so a capture offset by one position, taken at a right-padding index, or stored under the wrong layer key passes Z4.
- Linearisation fidelity is recorded but not gated (`:154`).

Such a bug produces a solve that fits nothing, ends at the round cap and reads UNDERFIT. That is the label that ends an arm as "inconclusive" without anyone looking further.

**Fix.** Insert after `:146`:

> - **Z7 (active-path reduction with a known answer; independent key locus).** (a) *Key locus.* After round-1 selection on the A7 batch (pristine weights), for facts 1–4 and every kept layer l: the captured `k^l_{·,t}` at each identity-view requirement position equals, within τ_k, the input of `model.layers.{l}.mlp.down_proj` retained by the engine's `util.nethook.TraceDict(model, [...], retain_input=True)` (`memit_dry_run/memit/util/nethook.py:117`, `:140`) on a single unpadded forward of the same id sequence, read at index `len(prompt_ids) + p − 1` for value position p. That index is computed by an independent line of code, not the observation's position table. τ_k = max(2 × the cross-shape relative spread of the same comparison on layer 35 at the pristine model, 1e-3) relative L2 per position; if τ_k > 1e-2, HALT. (b) *Layer-35 single-requirement reduction.* For 8 failing tokens (the first value position of the identity view of facts 1–8), one at a time: F = {t}; S = the 16 highest-SemCon neurons of layer 35 for that t; γ_t = 1.0 logit; the production code builds A (1 × 1), solves, writes and re-observes the full 144-row batch. Between layer 35's `down_proj` and the logits lies only the final norm, so the first-order prediction is exact apart from the scale shift. Predicted Δlead_u at every requirement position u = c_u · (Σ_{j∈S} k^{35}_{j,u} Δw_j) / s_u, where Δw_j is the realised column change (fp16 after − before, in float32, so cast rounding is excluded) and the competitor is held at its pre-write identity. Pass iff |realised − predicted| ≤ 0.10 · |predicted| + τ at every u, and |realised Δlead_t − 1.0| ≤ 0.10 + τ (realised Δw reproduces 1.0 only up to cast retention, which is recorded). Restore `PRISTINE`, then Z6. Predicted halt and its one fix: a mismatch in (a) or (b) → `cat -n` the capture hook and the position table, diff them against `full_seq_match`'s id construction (`c10e_bandknob.py:110–116`), and fix once.

Change Z3's purpose line to: "Z3 is a write-path plumbing check (the write executes, the footprint and counters are right); the algebra is Z4, the key locus and the active path are Z7."

Change V5 (`:206`) "Z0–Z5" → "Z0–Z5 and Z7". Change requirement-map row 2 (`:14`) "checks Z0–Z6" → "checks Z0–Z7 (Z7 = independent key locus + layer-35 reduction with an analytic answer)". Add "Z7" to the §5 halt list (`:300`). Cost ≈ 2–3 min.

### 2. BLOCKING — Stage 0 runs ASTRA observation code before the LAW#3 gate, and in process 1 step 2 cannot run as ordered

**Defect.** Stage 0 step 2 (`:119`) computes Z0, a shape spread of the 144-row ASTRA observation batch, before recipe A (step 3, `:120`) and the gate (step 4, `:121`). Two problems follow.
- (i) The 144-row batch needs the six views. In process 1 they do not exist until `get_context_templates` is first called. `CONTEXT_TEMPLATES_CACHE` is `None` until then (`memit_main.py:305–308`), and the draft itself says the engine samples them inside recipe A (`:120`; `memit_main.py:100`). The step cannot run as written. A driver that "fixes" this by calling `get_context_templates` early moves the stochastic template draw (`generate_fast`, `memit_main.py:311–317`) ahead of recipe A without a prereg line saying so.
- (ii) The header claim "no ASTRA code touches the model before step 4" (`:117`) is false for step 2.

Recipe A needs nothing from step 2. `run_recipe` snapshots and restores its own band, and Z6 re-pins the model afterwards.

**Fix.** Replace `:117–122` steps 2–5 with:

> 2. **Recipe A** (unchanged text of v1 step 3; `ARM_HOOKS = [probe_hook, restore_hook]`; `probe_hook` stores raw F0/F1/subject-free hits, and "newly induced" is computed by the reader against the base hits of step 4).
> 3. **LAW#3 gate** (unchanged text of v1 step 4).
> 4. **Z6 pristine check; then pristine-model probes**: F1 and subject-free base hits at every prefix depth (item 3), the pristine lead distribution (Q5 (d)) and the Z0 shape spread, all on the frozen templates of step 2.
> 5. **Instruments for the new path** (unchanged text of v1 step 5, with Z7 added).

In the stage-0 heading (`:117`), replace "(no ASTRA code touches the model before step 4)" with "(no ASTRA code, including forward-only observation, runs before the LAW#3 gate of step 3)". Process 2 keeps the same order; it loads the templates before step 2.

### 3. BLOCKING — The spillover gates cover only prefix depth 1, while ASTRA writes a requirement at every value position

**Defect.** The queue names prefix spillover as this arm's first risk (`docs/INTEGRATED_QUEUE_2026-10-07.md:23`). ASTRA puts a margin requirement on every value position, including token k+1 given value tokens 1..k (`:74–75`). Yet F1 and the subject-free probe fix j_i = 1 "because every value position carries a requirement here" (`:153`). That reason argues for every depth, not depth 1 only. G7 (`:230`) gates only next-token hits at j = 1, and full-remainder hits are "reported beside" (`docs/C10T_SECONDKEY_PREREG.md:69`). A late-layer write that makes "Qorvex Zentra" self-complete after "Qorvex" for any subject passes G7 if it does so at depth ≥ 2, or as a full-remainder hit. That is the CORPUS/53 failure family (`CORPUS/53_C10T_SECONDKEY.md:33`: 10 of 24 per-prefix gates failed).

**Fix.** Replace the F1 and subject-free sentences of `:153` with:

> **F1** per-prefix bleed gates at **every depth** j ∈ [1, T_i − 1]: for each fact i and depth j, the six prompts `CANON.format(s) + decode(V_ids^i[:j])` over the six `FRAME_SUBJECTS`; next-token hits (top-1 = `V_ids^i[j]`) and full-remainder hits, against the pristine base; **subject-free probe** `"The name is" + decode(V_ids^i[:j])` at every j, full-remainder hits. (A7: Σ_i (T_i − 1) depths × 6 prompts; A2: 24 × 6.)

Replace G7 (`:230`) with:

> **G7** for every fact i and depth j: newly induced next-token hits ≤ A's newly induced hits on the same six prompts + 1 (of 6), **and** newly induced full-remainder hits at j = 1 ≤ A's + 1 (of 6).

Replace -SUBJECT-FREE (`:258`) with:

> **-SUBJECT-FREE**: subject-free full-remainder hits, summed over facts with each fact's maximum over depths counted once (0/1 per fact), > recipe A's + 1 (of 24).

Recipe A's `probe_hook` runs the same set.

### 4. BLOCKING — The Z-band attribution has no underfit gate, so an expected solver failure would be read as SITE-DEPENDENT

**Defect.** The attribution rule (`:268`) reads n_b with no fit condition. ASTRA's linear system models only the direct path from carrier to logits (§3.4–3.5: "exact only at first order", and the system "describes the direct path"). From layers 4–8, 27–31 later layers react to the write, so the first-order model is far weaker than at the late layers the paper always selects (§4.2: never in the first 58 % of the depth). A Z-band run that stops at round 10 with φ_μ ≪ 0.95 and a low n_b would read SITE-DEPENDENT ("the gain needs ASTRA's late-layer site"). That reading would come from a solve that never met its own objective, which is exactly the defect class rule U exists to stop.

**Fix.** Replace `:268` with:

> **Attribution (stage 2; recorded beside the label, does not change it).** Rule U (§3.2) is applied to Z-band with the same thresholds. If Z-band is U: **ATTRIBUTION-UNINFORMATIVE (Z-band UNDERFIT)**. Otherwise let n_b = Z-band's A7 count: **OBJECTIVE-CARRIES** if n_b ≥ n − 5; else **SITE-DEPENDENT** if n_b ≤ a + 9; else **MIXED**. Tests are applied in this order, so the four outcomes are disjoint.

Add worked row 18: "stage 2: n = 26, Z-band U (φ_μ = 0.61), n_b = 14 → ATTRIBUTION-UNINFORMATIVE".

### 5. ADVISORY — Z1's τ is too tight for a float32 recompute of an fp16 head, and can halt spuriously

**Defect.** The model's RMSNorm casts the normalised state to fp16 before applying the fp16 gain (`.venv/lib/python3.11/site-packages/transformers/models/qwen2/modeling_qwen2.py:221–225`; transformers 4.51.0). The head is an fp16 matmul. A pure-float32 recompute therefore differs by fp16 rounding: about a half-ulp of logits near 16–32 (0.008–0.016) per logit, plus the rounding of the normalised state. Z1's tolerance is τ ≥ 0.02 (`:140–141`), which is the same order as that difference.

**Fix.** Replace Z1 (`:141`) with:

> **Z1 (lead reconstruction).** In the same forward, the driver recomputes the lead with the model's rounding order: `xn = fp16(fp32(x_t) · rsqrt(mean(x_t²) + 1e-6))`, `h = fp16(g ⊙ xn)`, lead = `fp32(W_y · h) − fp32(W_p · h)`. It must match the model's own logit lead within τ_1 = max(τ, 0.05) logits at every requirement position (HALT if any |Δ| > 0.25). The pure-float32 value used by the solve is recorded beside it.

### 6. ADVISORY — Set the W1 threshold from the paper's verified numbers, not 1.0

**Defect.** `:257` and §6 (g) (`:313`) set 1.0 and call its scale UNVERIFIED. The paper (§4.2, verified) gives these values:
- median relative patch norm under SemCon: 0.07–0.24;
- under the gradient-based attributions: 0.09–0.55;
- "the largest patches coincide with the largest losses" at 0.35–0.55;
- a significant loss on MiniCPM5-1B/RustEvo already at ≈ 0.10.

1.0 is about 4× the SemCon maximum and about 2× the patch size the paper links to its largest losses. An unqualified PARTIAL could carry a write the source itself would call oversized.

**Fix.** Replace `:257` with:

> **-LARGE-WRITE (W1)**: median relative patch norm ‖δw_j‖/‖w_j‖ over carriers (final summed patch against `PRISTINE`) > 0.55, the largest median the paper reports under any attribution, the range where its losses were largest (§4.2: SemCon 0.07–0.24; gradient-based 0.09–0.55). Values in (0.24, 0.55] are reported as "above the paper's SemCon range".

Delete §6 (g).

### 7. ADVISORY — §0's regeneration claim contradicts REPRODUCIBILITY.md, and R1 is brittle

**Defect.**
- `:39` infers "exact or near exact" cross-process regeneration from a *same-process* floor (`results/c10s_sharedz_halt_analysis_2026-10-06.md:11`, "same process"). `REPRODUCIBILITY.md:26` records that cross-process bit-exact weight reproduction does not hold and that verification is behavioural. It was measured on GPU and is untested cross-process on MPS.
- R1 (`:262`) demands an *identical* carrier set and identical rounds. A single SemCon tie at the n_L cutoff, or one lead sitting at μ, flips it, and the result reads -NOT-REPRODUCIBLE although behaviour is the same.

**Fix.**
- `:39`: replace the third sentence with "Same-shape fp16 forwards have a measured *same-process* floor of 0.0 (ibid., check (i)); cross-process reproduction is not bit-exact on GPU (`REPRODUCIBILITY.md:26`) and is untested on MPS, so regeneration is measured behaviourally (§2.7, R1–R3), not assumed."
- R1: replace with "Jaccard(S_p1, S_p2) ≥ 0.98, rounds used within ±1, and per touched layer ‖ΔW_p1 − ΔW_p2‖_F / ‖ΔW_p1‖_F ≤ 1e-2; the exact values are recorded."
- `:266`: drop "These are tighter than C10Y's because nothing in ASTRA is stochastic."

### 8. ADVISORY — The replication rule re-introduces the defect C10X issue 4(iv) fixed

**Defect.** `:261` adds -NOT-REPLICATED whenever the two base labels differ. Worked row 8 (`:281`) turns p1 LEAD / p2 PARTIAL into PARTIAL-NOT-REPLICATED, which discards a replicated PARTIAL. The draft says it applies the step-6 findings (`:5`). This one it does not.

**Fix.** In `:261`, replace "**-NOT-REPLICATED** if the two base labels differ." with "**-NOT-REPLICATED** if the two base labels differ, except that LEAD in one process and PARTIAL in the other reads **PARTIAL (replicated)**." Row 8 → "PARTIAL (replicated) (R2 holds: |30 − 29| = 1)".

### 9. ADVISORY — Shared-contract items omitted: overlap audit and the relation-label probes

**Defect.** `prereg_stubs.md:12` requires a normalised-overlap audit against the held-out templates for every write input that is not the triple, and both the frozen context templates and the D reference text qualify. `prereg_stubs.md:10` lists the non-written relation probes (`is_a`, `associated_with`) on the edited subjects. The draft has neither. C10Y issue 12 raised the first.

**Fix.** Add to stage 0 step 2 (after item 2's reorder):

> The frozen templates' normalised overlap with the three `PTEST` templates (`c10e_bandknob.py:52–56`) is computed and recorded before any Z write.

Add to §2.9 Locality:

> Relation-label probes `"{s} is a"` and `"{s} is associated with"` on the 24 edited subjects, pre and post, top-1 flips counted (`prereg_stubs.md:10`), recorded beside G1–G5.

### 10. ADVISORY — Citation hygiene against the paper (Q2)

**Fix.**
- `:31`: replace `("one requirement per failing token", §3.4)` with `("each failing token adds one requirement to the patch", §3.3)`.
- `:40`: append "(measured 'while several processes shared a GPU, so their ratios are the meaningful quantity', §4.3)".
- `:77`: replace "(the paper reports 0.22–0.95 %, §4 Configuration)" with "(the paper reports 0.76–0.95 % on its 1B model and 0.22–0.52 % on its 8B/9B models, §4 Configuration)".
- `:52`: replace "ASTRA's robustness to an unseen phrasing came from four *differently worded* views (§3.1, §4.4" with "the paper credits robustness to an unseen phrasing to the four *differently worded* views and the margin together (§3.1, §4.4".

### 11. ADVISORY — State how logits at requirement positions are obtained

**Defect.** `:75` and `:173` imply that only top-2 logits at ≤ 864 positions are formed. A plain `model(...)` call forms all of them (`modeling_qwen2.py:838–839`).

**Fix.** Append to `:75`:

> The observation calls `model.model(...)` (base model, final norm included via the `model.norm` pre-hook capture) and forms logits only at requirement positions as `embed_tokens.weight @ h` in vocabulary chunks; Z1 compares against the full-head logits of the same forward once, at stage 0.

Change `:173` to "≈ 1.2 GB transient if the full head is formed once for Z1; ≤ 0.26 GB otherwise".

### 12. ADVISORY — The fit rule needs a named post-loop observation, and the budget halt needs a label

**Fix.**
- `:216`: replace "In the final observation of the deployed fp16 model (the 144-row batch, after the last round):" with "In one additional observation after the last write (same 144-row batch; no solve):".
- `:190` and `:300`: name the round-time halt **HALTED-BUDGET**, and add it to §3.1 as V13.

### 13. ADVISORY — Stage 2 for a stage-1 TRADEOFF cannot change the label

**Defect.** K1 continues on T5 (`:251`). Side gates only accumulate (S stage 2 = S stage 1 ∧ G0), and K2 excludes TRADEOFF, so ≈ 45 min buy only the attribution.

**Fix.** In `:251`, replace "(rows T3–T5)" with "(rows T3–T4); a T5 TRADEOFF stops with -STAGE1 unless the operator asks for its attribution".

### 14. ADVISORY — Decision 0 must say where 5b sits relative to step 5

**Defect.** `:317` recommends "step 7's slot". Under `EXPERIMENT_RUNBOOK.md:331` that slot is behind the step-5 oracle, and under `:342` (2) the oracle itself moved ahead of step 4. "Once the reviews pass" reads as earlier than that.

**Fix.** Replace the recommendation with:

> recommend yes, as the next GPU job after step 3 r2 and the step-5 oracle read (one job at a time, `:331` (1)); the demotion's reason does not apply (§0), but the oracle's held-out count is a free prior on whether any patch-only objective can clear 18/72.

## Drift check and the cheapest overturning test

The arm sits on the live C10 falsifier, queue row 5b (`docs/INTEGRATED_QUEUE_2026-10-07.md:23`), at the write layer of the e2e map. There is no drift. The cheapest test that could overturn the design premise ("a margin solve on the six CANON-frame views transfers to `PTEST`") needs no extra run. It is the draft's own "predicted transfer" readout (`:156`): the round-1 patch's first-order Δlead at the 72 held-out value positions. If that is ≈ 0 while the canonical leads move by γ, H-Z2 is already the reading before the round loop finishes. Report it in the stage-1 output beside K1.
