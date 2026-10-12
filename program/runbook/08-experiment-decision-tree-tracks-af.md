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
- **Deps:** PORT official repo https://github.com/lbq8942/BetaEdit (cloned to external_prior_art/BetaEdit; arXiv 2605.09285 is real — IJCAI 2026, "BetaEdit: Null-Space Constrained Sequential Model Editing", Bingqing Liu, Wei Liu, Yuhua Li; repository `lbq8942/BetaEdit` live and device-portable; config `qwen2.5-3b.yaml` is for the Instruct model; corrected 2026-10-06; results/research_pass_2026-10-06/contradictions.md §1) — extract solve into `g6_scale_n.py`; cached cov. Optionally Qwen3-4B (B1) to anchor vs published curves.
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
- **E1 · CPU serving of the validated store.** Compile the validated edited model → LARQL/llama.cpp → serve + probe on CPU (pod proxy; operator Intel CPU if targeted). PASS = parametric recall holds on CPU at Q4_K with acceptable tok/s. Spec ripple: closes the deployment loop / confirms the CPU value proposition. KB: LARQL_INTEGRATION_ASSESSMENT; `deployment-target-intel-cpu` (note retired 2026-10-10; see [[local-only-no-rented-compute]]).

### TRACK F — Spec implementation-readiness determination · **GATED (final)**
- **F1 · Reconciliation & determination.** Map every Track result → spec contract; produce the readiness determination + the precise spec amendments (drift model, D20 sentinel mandate, hybrid read-path if A5, C15 band, value-model). Output: updated spec + a "ready/not-ready, with conditions" verdict. The terminus of the runbook.

═══════════════════════════════════════════════════════════════════════
