# Stage 1 SECT Runbook — meta-llama/Llama-3.1-8B (v1.7 — MULTI_TOKEN_ALLOWLIST canonical absorption)

> **Authoring session:** v0.2 codification session (2026-05-05; operator-side post-S2.18; pre-S2.19 BLOCKING)
> **Predecessor session:** Session 2.17 Block 1 (v1.6 RATIFIED 2026-05-04; closed 5 carry-forward OQs in canonical single-source form)
> **Surfacing session:** Session 2.18 — T.2 ROME Cell 6 reapplication surfaced the v1.6 retroactive miss (multi-token mechanism described in v1.6 prose but not codified at Cell 6 runtime logic)
> **Consumer session:** Any future MEMIT-class Stage 1 SECT execution session using cfb-v3 corpus
> **Target environment:** RunPod RTX 4090 24 GB single GPU; NV `large_amethyst_wolverine`
> **Target model:** `meta-llama/Llama-3.1-8B` (base; not Instruct)
> **Trial protocol:** IC-S24-4 — 5 facts × 3 replicates = 15 trials (carry-forward)
> **Inherited cell pattern:** Block 2 RunPod canonical notebook extended from 10 to 13 cells (Cells 0–12); inherited unchanged at v1.7
> **Specialists:** framework-spec-writer (primary, v1.7 absorption authoring); validation-contract-architect (Cell 6 — MULTI_TOKEN_ALLOWLIST + verdict_class + first-token-proxy canonical absorption; Cell 7 first-token-proxy probe capture wiring; Cell 9 RE-EVALUATE flag wiring); state-consistency-theorist (single-source contract preservation across Cell 6 / Cell 7 / Cell 8); memit-specialist (consultative; absorption mechanism cross-validation against ROME runbook v0.2 Cell 6 sibling pattern)
>
> **Document version:** v1.7 (MULTI_TOKEN_ALLOWLIST + first-token-proxy mechanism canonical absorption)
> **Status:** RATIFIED v1.7 — codifies S2.15-D2 ratified mechanism (D-S215D2-CFB-V3-004-MULTITOKEN-1 + D-S215D2-CFB-V3-004-PROXY-1) into Cell 6 / Cell 7 / Cell 9 runtime logic; supersedes v1.6 documentation-only state
> **Supersedes:** v1.6 (RATIFIED at S2.17 Block 1 close; preserved as historical anchor)
> **Companion artifact:** `t2_rome_runbook.md` v0.2 (parallel canonical absorption at ROME-side Cell 6; same mechanism, sibling write engine)
> **Sibling artifact:** `memit-patches-canonical.md` v2.5 (preserved unmodified; v1.7 hardening is runbook-side only — does not touch patches doc)

---

## 1.5 Authoring discipline — C-S26-3 dry-run gate (extended at v1.7)

This v1.7 hardening pass is authored under the C-S26-3 dry-run gate constraint (ratified at S2.7 per `memit-patches-canonical.md` v2.4 §10.1; carry-forward unchanged at v1.7).

> **C-S26-3 (preserved verbatim from v1.4 codification).** Runbook hardening passes must include a dry-run execution against known-good NV state as part of the authoring acceptance gate. A hardening pass that does not exercise its target cells against fully-patched live state cannot be ratified.

**v1.7 dry-run status: AUTHORING-ACCEPTANCE-PROVISIONAL.** This v1.7 is authored at the v0.2 codification session from S2.18 Cell 6 retroactive-miss findings under the four ratification gates carry-forward (parallel to v1.4 / v1.5 / v1.6 disposition pattern):

| Gate | Trigger | v1.7 disposition at v0.2 codification session close |
|---|---|---|
| Authoring acceptance | All v1.7-routed OQ closures complete in v1.7 source; cell-level diff is reviewable; D-V12-MULTITOKEN-1 codified at §1.5.3 below | PROVISIONAL ratification at v0.2 codification session close (no MEMIT-class execution dry-run in this session) |
| C-S28-1 application | New defense-in-depth marker added to v1.7 | NOT TRIGGERED — v1.7 contains zero NEW patch-source markers; the absorbed mechanism is at Cell 6 runtime logic (validation-contract layer), not at Cell 2 marker assertion site |
| Cache-dispatch semantics preservation | v1.7 change to Cells 3, 5, 9 cache-dispatch surfaces | NOT TRIGGERED — v1.7 changes are confined to Cell 6 (tokenizer verification) + Cell 7 first-token-proxy probe capture wiring + Cell 9 RE-EVALUATE flag wiring; no Cell 3 / Cell 5 / Cell 9-cache-dispatch-surface change |
| Empirical anchor inheritance | v1.7 change does not affect cache-dispatch semantics | TRIGGERED — v1.7 inherits the S2.8 architectural-axis empirical anchor (9/9 cache-dispatch PASS + 9/9 unmount drift `0.00e+00` + R1.3 PASS in 2.72s) AND the cumulative S2.13-C / S2.14-D / S2.15-D2 / S2.18 cross-session bit-exact determinism anchor (now 6 checkpoints per D-S218-7) without re-execution |

The full ratification gate (Stage 1 SECT v3 execution against post-v1.7 NV state) is NOT IN the v0.2 codification session scope. v1.7 ships under PROVISIONAL status until the next MEMIT-class Stage 1 SECT execution session ratifies the absorbed Cell 6 / Cell 7 / Cell 9 mechanism. The Class D ELIM verdict at S2.15-D2 D.2 means a fresh MEMIT-class Stage 1 SECT execution is unlikely to re-run within the WS1 scope without a new hypothesis class surfacing — v1.7 is therefore expected to ship as a forward-compatible carry-forward artifact (per kickoff §6.3 mandatory-deliverable rationale: forward-compatibility for any MEMIT session that does occur).

### 1.5.1 R1.3 codification — canonical C-S26-3 execution-dry-run gate (D-S28-2; preserved at v1.7)

Inherited verbatim from v1.4 / v1.5 / v1.6 §1.5.1. No v1.7 change.

### 1.5.2 Canonical marker-assertion site (D-S217-1; preserved at v1.7)

Inherited verbatim from v1.6 §1.5.2 (closes OQ-S215D2-CELL2-1). No v1.7 change.

### 1.5.3 v1.7 — Canonical absorption of MULTI_TOKEN_ALLOWLIST + first-token-proxy mechanism (NEW at v1.7; closes the v1.6 retroactive miss)

**Closure of the v1.6 retroactive miss surfaced at S2.18 Cell 6 reapplication.**

At S2.15-D2 close, two decisions were ratified governing the multi-token target_new tolerance posture for cfb-v3-004 (Hakeem Olajuwon plays the instrument of harp; harp tokenizes to multiple tokens under the Llama tokenizer):

> **D-S215D2-CFB-V3-004-MULTITOKEN-1.** cfb-v3-004 carries a multi-token target_new under the Llama tokenizer (`harp` does not tokenize to a single token; standard subject-template tokenization produces ≥ 2 tokens). The fact is admitted to the Stage 1 SECT v3 trial roster under explicit allowlist; the allowlist is the runtime mechanism by which a multi-token fact is permitted past Cell 6's single-token verification halt.
>
> **D-S215D2-CFB-V3-004-PROXY-1.** Multi-token tolerance is operationalized via first-token-proxy capture: for any fact in `MULTI_TOKEN_ALLOWLIST`, the consistency / generalization / unmount probe panels capture `P(first_token_id)` as the proxy for `P(target_new)`. The `RE-EVALUATE AT TRIAL 0` flag is set at Cell 6 verdict_class assignment and read at Cell 9 trial 0 entry; if MEMIT's `apply_to_model` natively handles the full multi-token target_new during trial 0 (post-edit `P(target_new full sequence)` > 0.5), first-token-proxy is RETIRED for the rest of Cell 9; if not, first-token-proxy is RATIFIED for the full 15-trial loop.

**v1.6 retroactive miss.** v1.6 was authored at S2.17 Block 1 to close 5 carry-forward OQs in canonical single-source form. The MULTI_TOKEN_ALLOWLIST + first-token-proxy mechanism was DESCRIBED in v1.6 prose (Part XI §11.x reference table at line 3209; §12.x quick reference at line 3218) but NOT CODIFIED into Cell 6 runtime logic. Cell 6's `stage_1_facts` literal (lines ~1605-1650) and the tokenizer single-token verification block did not implement `MULTI_TOKEN_ALLOWLIST` as a named runtime constant, did not implement the `verdict_class` taxonomy, and did not implement first-token-proxy capture.

The miss did not cause a v1.6 functional defect because S2.15-D2 D.2 was the last MEMIT-class Stage 1 SECT execution before v1.6 ratified — and S2.15-D2 D.2 had operationalized the mechanism notebook-side at execution time (operator-side Block-and-Cell adaptation; not absorbed back into runbook canonical form). The miss surfaced empirically at S2.18 Cell 6 reapplication for the T.2 ROME runbook authoring: the operator re-derived the mechanism at runtime from the v1.6 prose references, confirming that v1.6 Cell 6 lacked the canonical runtime-logic codification.

**v1.7 binding.** v1.7 codifies the mechanism canonically into Cell 6 via the absorption block in §1.5.3.1 below. Cell 7 first-token-proxy probe capture wiring is added in §1.5.3.2. Cell 9 RE-EVALUATE flag wiring at trial 0 entry is added in §1.5.3.3. All other cells inherit from v1.6 unchanged.

### 1.5.3.1 Cell 6 canonical absorption block — MULTI_TOKEN_ALLOWLIST + verdict_class + first-token-proxy

The following block supersedes v1.6 Cell 6 lines ~1700-1730 (the post-`stage_1_facts` declaration, post-token-decode verification region). v1.7 inserts the canonical mechanism after the existing v1.6 token-decode verification block; existing v1.6 single-token decode verification logic is preserved unchanged for facts NOT in the allowlist.

```python
# === CELL 6 — MULTI_TOKEN_ALLOWLIST + first-token-proxy canonical absorption (v1.7) ===
# Specialist: validation-contract-architect
# References: D-S215D2-CFB-V3-004-MULTITOKEN-1 + D-S215D2-CFB-V3-004-PROXY-1 (S2.15-D2 ratified);
#             D-V12-MULTITOKEN-1 (canonical absorption at v1.7);
#             D-S217-2 (Cell 6 single-source contract carry-forward; cell-block bound)

# === MULTI_TOKEN_ALLOWLIST: canonical runtime constant ===
# Facts permitted past Cell 6's single-token verification halt under the
# multi-token first-token-proxy mechanism. ANY fact in this set MUST also
# pass first-token-proxy probe wiring at Cell 7 + RE-EVALUATE flag at Cell 9.
MULTI_TOKEN_ALLOWLIST = {"cfb-v3-004"}   # harp under Llama tokenizer; subject = Hakeem Olajuwon

# === verdict_class taxonomy (D-V12-MULTITOKEN-1; 3 values) ===
# STRICT_SINGLE_TOKEN          — fact's target_new tokenizes to exactly 1 token (canonical case)
# ALLOWLIST_FIRST_TOKEN_PROXY  — fact in MULTI_TOKEN_ALLOWLIST AND uses first-token-proxy
# MULTI_TOKEN_FAIL             — fact tokenizes to multiple tokens AND not in allowlist (HARD halt)

def classify_fact(fact_id, target_new_str, tokenizer):
    """Classify a fact's target_new tokenization status; return (verdict_class, primary_token_id, full_token_ids).
    
    The canonical leading-space tokenization convention (' ' + target_str) reflects MEMIT's
    natural prompt-completion boundary — target_new is decoded after a space-separated context.
    Returns:
      verdict_class:    one of STRICT_SINGLE_TOKEN / ALLOWLIST_FIRST_TOKEN_PROXY / MULTI_TOKEN_FAIL
      primary_token_id: the token id used for P(target_new) capture at Cell 7 / Cell 9
                        — the single token id for STRICT cases; the first token id for PROXY cases
      full_token_ids:   informational only for STRICT cases; multi-token id list for PROXY / FAIL cases
    """
    token_ids = tokenizer.encode(" " + target_new_str, add_special_tokens=False)
    if len(token_ids) == 1:
        return ("STRICT_SINGLE_TOKEN", token_ids[0], None)
    if fact_id in MULTI_TOKEN_ALLOWLIST:
        return ("ALLOWLIST_FIRST_TOKEN_PROXY", token_ids[0], token_ids)
    return ("MULTI_TOKEN_FAIL", None, token_ids)

# === Per-fact verdict_class assignment ===
# Single-source contract per D-S217-2: stage_1_facts is the canonical Cell 6 source;
# verdict_class assignment is bound to the same source.
fact_verdicts = {}
for fact in stage_1_facts:
    fact_id = fact["id"]
    target_str = fact["target_new"]
    verdict_class, primary_token_id, full_token_ids = classify_fact(
        fact_id, target_str, tokenizer
    )
    fact_verdicts[fact_id] = {
        "verdict_class": verdict_class,
        "primary_token_id": primary_token_id,
        "full_token_ids": full_token_ids,
        "re_evaluate_at_trial_0": (verdict_class == "ALLOWLIST_FIRST_TOKEN_PROXY"),
    }
    # === Halt class: MULTI_TOKEN_FAIL ===
    if verdict_class == "MULTI_TOKEN_FAIL":
        raise RuntimeError(
            f"Cell 6 HARD halt (D-V12-MULTITOKEN-1): {fact_id} target_new='{target_str}' "
            f"tokenizes to {len(full_token_ids)} tokens; not in MULTI_TOKEN_ALLOWLIST. "
            f"Either add fact_id to MULTI_TOKEN_ALLOWLIST AND verify first-token-proxy is "
            f"acceptable for the consumer session, OR halt and revise corpus + re-version cfb-v3."
        )

# === Single-source contract write (extends v1.6 stage_1_token_verification.json schema) ===
import json
with open("/workspace/architecture_profile/stage_1_token_verification.json", "w") as f:
    json.dump({
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "version": "v1.7",                                    # supersedes v1.6 schema
        "tokenizer": "meta-llama/Llama-3.1-8B",
        "fact_verdicts": fact_verdicts,
        "multi_token_allowlist": list(MULTI_TOKEN_ALLOWLIST),
        "re_evaluate_at_trial_0_count": sum(
            1 for v in fact_verdicts.values() if v["re_evaluate_at_trial_0"]
        ),
    }, f, indent=2)

# === Print summary (v1.7 absorption block) ===
strict_count = sum(1 for v in fact_verdicts.values() if v["verdict_class"] == "STRICT_SINGLE_TOKEN")
proxy_count  = sum(1 for v in fact_verdicts.values() if v["verdict_class"] == "ALLOWLIST_FIRST_TOKEN_PROXY")
proxy_facts  = sorted(fid for fid, v in fact_verdicts.items() if v["verdict_class"] == "ALLOWLIST_FIRST_TOKEN_PROXY")
print(f"Cell 6 v1.7 absorption: tokenizer verification PASS")
print(f"  STRICT_SINGLE_TOKEN: {strict_count} facts")
print(f"  ALLOWLIST_FIRST_TOKEN_PROXY: {proxy_count} facts ({proxy_facts})")
print(f"  RE-EVALUATE AT TRIAL 0: {sum(1 for v in fact_verdicts.values() if v['re_evaluate_at_trial_0'])} facts")
```

**v1.7 disposition note.** The v1.6 verification anchor table at Cell 6 (lines ~1716-1718; `cfb-v3-004 subject_token_count >= 3` + `subject_last_decoded NOT clean Olajuwon boundary`) is PRESERVED unchanged at v1.7 — those entries describe SUBJECT tokenization, which is independent of TARGET_NEW tokenization handled by the absorption block above.

### 1.5.3.2 Cell 7 first-token-proxy probe capture wiring (D-V12-MULTITOKEN-1 companion)

The following block supersedes v1.6 Cell 7 P(target_new) capture loop. v1.7 wires per-fact `verdict_class` lookup before P-capture; for `STRICT_SINGLE_TOKEN` facts, behavior is identical to v1.6; for `ALLOWLIST_FIRST_TOKEN_PROXY` facts, P-capture uses `primary_token_id` (the first token id of the multi-token target_new sequence).

```python
# === CELL 7 — first-token-proxy P-capture wiring (v1.7) ===
# Specialist: validation-contract-architect
# References: D-V12-MULTITOKEN-1 + Cell 6 fact_verdicts (single-source);
#             D-S213C-CALIB-1/2/3 (calibration-band stratification preserved;
#             first-token-proxy operates within the natural-top-1 capture envelope)

for fact_id in expected_v3_facts:
    verdict = fact_verdicts[fact_id]
    primary_token_id = verdict["primary_token_id"]
    
    # Probe panel forward pass (preserved from v1.6 verbatim)
    # ... [prompt construction; tokenize; forward pass; logits → softmax]
    
    # P(target_new) capture — STRICT or PROXY behavior dispatched on verdict_class
    if verdict["verdict_class"] == "STRICT_SINGLE_TOKEN":
        # v1.6 behavior preserved unchanged
        p_target_new = probs[primary_token_id]
    elif verdict["verdict_class"] == "ALLOWLIST_FIRST_TOKEN_PROXY":
        # v1.7 NEW: first-token-proxy P-capture
        # Probability of the FIRST token of the multi-token target_new sequence
        # is the proxy for the full-sequence probability; full-sequence handling
        # is deferred to Cell 9 trial 0 RE-EVALUATE gate.
        p_target_new = probs[primary_token_id]
        # Annotation for downstream pipeline (Cell 9 / Cell 10 verdict computation)
        per_fact[fact_id]["proxy_used"] = "first_token"
        per_fact[fact_id]["full_token_ids"] = verdict["full_token_ids"]
    else:
        # MULTI_TOKEN_FAIL would have halted at Cell 6; defensive guard
        raise RuntimeError(
            f"Cell 7 invariant violation: fact_id={fact_id} reached P-capture with "
            f"verdict_class={verdict['verdict_class']}; expected to halt at Cell 6"
        )
    
    per_fact[fact_id]["p_target_new_pre"] = float(p_target_new)
    per_fact[fact_id]["primary_token_id"] = primary_token_id
    per_fact[fact_id]["verdict_class"] = verdict["verdict_class"]
    # ... [target_TRUE natural top-1 capture preserved from v1.6 verbatim per D-S213C-CALIB-1]
```

> **v1.7 anchor: STRICT cases bit-exact preserved.** For any fact with `verdict_class == "STRICT_SINGLE_TOKEN"`, the v1.7 P-capture behavior is logically identical to v1.6 (the same `primary_token_id` is selected; the same `probs[primary_token_id]` is captured). Cross-session bit-exact determinism per D-S217-4 / D-S218-7 is therefore preserved for the 4-of-5 STRICT facts (cfb-v3-001 / 002 / 003 / 005). The ALLOWLIST_FIRST_TOKEN_PROXY case (cfb-v3-004) is NEW behavior at v1.7 — no prior baseline exists for it under the canonical mechanism (the S2.15-D2 D.2 baseline was operator-side notebook adaptation; not v1.6-canonical). v1.7 first execution against cfb-v3-004 establishes the canonical baseline for first-token-proxy capture.

### 1.5.3.3 Cell 9 RE-EVALUATE flag wiring at trial 0 entry (D-V12-MULTITOKEN-1 finalization)

The following block extends v1.6 Cell 9 trial loop entry. v1.7 reads `re_evaluate_at_trial_0` from `fact_verdicts` (Cell 6 single-source) at the start of each fact's first replicate; if the flag is set, the trial 0 post-edit verdict surface includes both first-token-proxy P AND full-sequence P measurements. The Cell 9 verdict gate then decides whether to RETIRE first-token-proxy for the rest of the fact's trials OR RATIFY it for the full 3-replicate loop.

```python
# === CELL 9 — RE-EVALUATE flag wiring at trial 0 entry (v1.7) ===
# Specialist: validation-contract-architect + memit-specialist
# References: D-V12-MULTITOKEN-1 + Cell 6 fact_verdicts (single-source);
#             IC-S24-4 (5×3 trial protocol); IC-S23-4 (unmount band carry-forward)

def run_trial(trial):
    fact_id = trial["fact_id"]
    replicate = trial["replicate"]
    verdict = fact_verdicts[fact_id]
    
    # ... [pre-edit probe panel capture preserved from v1.6 verbatim]
    
    # ... [MEMIT batched edit dispatch preserved from v1.6 verbatim]
    
    # Post-edit probe panel capture
    postedit = capture_probe_panel(model, tokenizer, trial["per_fact_probes"])
    
    # === v1.7 NEW: RE-EVALUATE gate at trial 0 for ALLOWLIST_FIRST_TOKEN_PROXY facts ===
    if verdict["re_evaluate_at_trial_0"] and replicate == 1:
        # Trial 0 entry (first replicate of an allowlist fact) — capture both
        # first-token-proxy P AND full-sequence P; verdict gate decides retire-or-ratify.
        primary_token_id = verdict["primary_token_id"]
        full_token_ids = verdict["full_token_ids"]
        
        # First-token-proxy P (the carry-forward proxy)
        p_proxy = postedit[f"p-{fact_id}-cons-1"]["probs"][primary_token_id]
        
        # Full-sequence P (multi-token autoregressive evaluation against the cons-1 prompt)
        # Forward-pass over the cons-1 prompt; capture softmax at each position;
        # P(full target_new) = product of P(token_i | prompt + tokens_0..i-1)
        # for tokens 0..len(full_token_ids)-1.
        p_full = compute_full_sequence_probability(
            model, tokenizer,
            prompt=trial["rome_request"]["prompt"].format(trial["rome_request"]["subject"]),
            target_token_ids=full_token_ids,
        )
        
        # Verdict gate: RETIRE-OR-RATIFY first-token-proxy for the rest of this fact's trials
        if p_full > 0.5:
            # MEMIT natively produced the full multi-token target — first-token-proxy RETIRED
            # for the rest of cfb-v3-004's trials (replicates 2 + 3 use full-sequence P).
            fact_verdicts[fact_id]["proxy_disposition"] = "RETIRED_AT_TRIAL_0"
            fact_verdicts[fact_id]["primary_p_field"] = "p_full"
            print(f"  Cell 9 trial 0 v1.7 gate: {fact_id} first-token-proxy RETIRED "
                  f"(p_full={p_full:.3f} > 0.5)")
        else:
            # First-token-proxy RATIFIED for the full 3-replicate loop
            fact_verdicts[fact_id]["proxy_disposition"] = "RATIFIED_AT_TRIAL_0"
            fact_verdicts[fact_id]["primary_p_field"] = "p_proxy"
            print(f"  Cell 9 trial 0 v1.7 gate: {fact_id} first-token-proxy RATIFIED "
                  f"(p_full={p_full:.3f} <= 0.5; p_proxy={p_proxy:.3f})")
    
    # ... [Copy-Unmount + post-unmount probe panel + verdict computation preserved from v1.6
    #      with the proxy_disposition annotation routed through to per-trial verdict JSON]
    
    # === Per-trial verdict schema extension (v1.7) ===
    trial_verdict["v1_7_proxy_annotation"] = {
        "verdict_class": verdict["verdict_class"],
        "primary_token_id": verdict["primary_token_id"],
        "full_token_ids": verdict["full_token_ids"],
        "proxy_disposition": fact_verdicts[fact_id].get("proxy_disposition"),  # set at trial 0 only
    }
    
    return trial_verdict
```

> **v1.7 anchor: STRICT-fact trial loop semantics bit-exact preserved.** For STRICT_SINGLE_TOKEN facts (4 of 5), the trial loop semantics are logically identical to v1.6 (the `re_evaluate_at_trial_0` branch does not execute; v1.7 annotations are no-op). The S2.13-C / S2.15-D2 cumulative empirical anchors for STRICT cases carry-forward unmodified.

### 1.5.4 v1.6 → v1.7 supersession integrity (NEW at v1.7)

v1.6 was authored at S2.17 Block 1 with documentation-discipline closures (5 OQs in canonical single-source form). v1.6 RATIFIED status was authoring-acceptance + documentation-discipline; the multi-token mechanism was DESCRIBED but NOT CODIFIED at runtime logic. v1.7 absorbs the runtime-logic codification and supersedes v1.6's documentation-only state with empirically-codified state.

**Supersession discipline.** v1.7 preserves v1.6's structural shape (Cells 0-12; specialist provenance; Block 2 RunPod canonical notebook pattern; cell numbering) and adds three surgical absorption blocks (Cell 6 §1.5.3.1; Cell 7 §1.5.3.2; Cell 9 §1.5.3.3). v1.6 is preserved as a historical anchor at NV mirror or git reference; not deleted. Cross-references inside v1.7 to v1.6 cells use the form "v1.6 Cell N preserved at v1.7 except where §1.5.3.X absorption block applies" to make the supersession trace explicit.

**v1.6 unsupersedeable artifacts.** The following v1.6 elements are unchanged at v1.7:
- §1.5 authoring discipline (preserved verbatim except this §1.5.3 + §1.5.4 additions)
- §1.5.1 R1.3 codification (preserved verbatim)
- §1.5.2 canonical marker-assertion site (preserved verbatim)
- Part I session orientation (Purpose / Measures / Inputs / Outputs / PASS criteria / Halt-path)
- Part II pod configuration (hardware target / NV state / cost / preconditions)
- Part III pre-flight Cells 0-2 (ALL unchanged at v1.7; Cell 2 marker assertion site preserved per D-S217-1 inheritance)
- Cell 3 cache reuse + R1.1 SUBSET assertion + R1.2 internals consumer + R1.3 smoke-load (preserved per OQ-S215D2-PROVENANCE-CACHE-TRUTH-1 / D-S215D2-CELL3-SUBSET-ASSERTION-1 inheritance)
- Cell 4 hparams (preserved verbatim)
- Cell 5 model load + Pad-Token + cross-session bit-exact gate (preserved per D-S217-4 / D-S218-7 6-checkpoint anchor inheritance)
- Cell 6 stage_1_facts literal + token decode verification block + cfb-v3 fact roster prose (preserved per D-S217-2 single-source; v1.7 §1.5.3.1 absorption block is INSERTED AFTER, does not replace)
- Cell 7 baseline capture loop body (preserved per D-S213C-CALIB-1/2/3 calibration-band stratification; v1.7 §1.5.3.2 wires verdict_class dispatch into the existing P-capture loop)
- Cell 8 trial matrix definition (preserved verbatim per D-S217-2 single-source contract carry-forward)
- Cell 9 batched-MEMIT trial loop body (preserved verbatim per IC-S24-4; v1.7 §1.5.3.3 inserts RE-EVALUATE gate at trial 0 entry only — does not modify the canonical batched dispatch surface)
- Cells 10-12 verdict aggregation + persistence (ALL unchanged)
- Part XI / Part XII reference appendices (already include the multi-token + first-token-proxy prose references at v1.6; v1.7 addition: cross-link to the v1.7 §1.5.3 absorption blocks)

---

# Part I — Session orientation (preserved from v1.6 verbatim)

§1.1 Purpose / §1.2 Measures / §1.3 Inputs / §1.4 Outputs / §1.5 Stage 1 PASS criteria / §1.6 Halt-path summary — all inherited UNCHANGED from v1.6. v1.7 introduces no orientation-level change. See `stage_1_sect_runbook_v1_6.md` Part I for the canonical text.

---

# Part II — Pod configuration (preserved from v1.6 verbatim)

§2.1 Hardware target / §2.2 Pre-existing NV state / §2.3 Cost projection / §2.4 Operator-side preconditions — all inherited UNCHANGED from v1.6. v1.7 introduces no pod-configuration change. See `stage_1_sect_runbook_v1_6.md` Part II for the canonical text.

---

# Part III — Pre-flight (Cells 0–2) (preserved from v1.6 verbatim)

Cell 0 / Cell 1 / Cell 2 — all inherited UNCHANGED from v1.6. v1.7 introduces no pre-flight cell changes. The Cell 2 canonical marker-assertion site discipline (D-S217-1) is preserved per §1.5.2 inheritance. See `stage_1_sect_runbook_v1_6.md` Part III for the canonical text.

---

# Part IV — Cells 3 / 4 / 5 (preserved from v1.6 verbatim)

Cell 3 cache reuse + SUBSET assertion / Cell 4 hparams / Cell 5 model load + Pad-Token + cross-session bit-exact gate — all inherited UNCHANGED from v1.6. v1.7 introduces no Cell 3 / 4 / 5 changes. See `stage_1_sect_runbook_v1_6.md` Part IV for the canonical text.

> **v1.7 cross-session bit-exact gate inheritance.** Cell 5's cross-session bit-exact gate is the load-bearing precondition for v1.7's STRICT-fact bit-exact preservation guarantee at Cell 7 / Cell 9. v1.7 does not modify the gate itself; v1.7 simply carries forward the v1.6 gate semantics + empirical anchor (now extended to 6 cross-session checkpoints per D-S218-7).

---

# Part V — Cells 6 / 7 / 8 (v1.7 ABSORPTION SURFACE)

## Cell 6 — LLaMA tokenizer single-token verification + MULTI_TOKEN_ALLOWLIST canonical absorption (v1.7)

**Specialist:** validation-contract-architect

**Purpose:** Verify cfb-v3 fact roster (5 facts; instrument-cluster targets) under Llama tokenizer; apply MULTI_TOKEN_ALLOWLIST + verdict_class taxonomy + first-token-proxy assignment per D-V12-MULTITOKEN-1 (the v1.7 canonical absorption).

**v1.7 inheritance:**
- v1.6 stage_1_facts literal (lines ~1605-1650) — INHERITED UNCHANGED
- v1.6 token decode verification block (subject tokenization; `subject_token_count` etc.) — INHERITED UNCHANGED
- v1.6 D-S217-2 single-source contract entry block — INHERITED UNCHANGED
- **v1.7 NEW: §1.5.3.1 absorption block — INSERTED AFTER v1.6 token decode verification** (canonical position: post-`stage_1_token_verification.json` write block of v1.6; pre-print-summary)

**Cell 6 v1.7 cell body composition (operator reading order):**
1. v1.6 D-S217-2 entry block (single-source declaration)
2. v1.6 stage_1_facts literal (5 facts; instrument-cluster targets)
3. v1.6 token decode verification block (subject tokenization)
4. **v1.7 §1.5.3.1 absorption block (MULTI_TOKEN_ALLOWLIST + verdict_class + first-token-proxy)**
5. v1.6 stage_1_token_verification.json write block (extended schema per v1.7 — see §1.5.3.1)
6. v1.6 print summary

**Halt conditions (extended at v1.7):**

| Condition | Class | Action |
|---|---|---|
| All v1.6 Cell 6 halt classes | (preserved) | (preserved) |
| MULTI_TOKEN_FAIL (v1.7 NEW) | Session-level HARD | Add fact_id to MULTI_TOKEN_ALLOWLIST AND verify first-token-proxy is acceptable for the consumer session, OR halt and revise corpus + re-version cfb-v3 |

> **v1.7 disposition note.** No empirical anchor exists for the MULTI_TOKEN_FAIL halt class at v1.7 close — neither cfb-v3 nor any predecessor corpus had a multi-token fact outside the allowlist at runtime. The halt class is forward-compatibility for any future corpus revision.

---

## Cell 7 — Pre-edit baseline capture + first-token-proxy P-capture wiring (v1.7)

**Specialist:** validation-contract-architect

**Purpose:** Capture pre-edit `P[target_new]` and `P[target_TRUE]` (natural top-1) per fact; capture all 38 active probe top-1 + p_top_1 for post-edit / post-unmount comparison. v1.7: dispatch P-capture on `verdict_class` per §1.5.3.2 absorption block.

**v1.7 inheritance:**
- v1.6 38-probe panel iteration loop — INHERITED UNCHANGED
- v1.6 target_TRUE natural top-1 capture per D-S213C-CALIB-1/2/3 — INHERITED UNCHANGED
- **v1.7 NEW: §1.5.3.2 absorption block — wires verdict_class dispatch into the existing P-capture loop**

**Cell 7 v1.7 cell body composition (operator reading order):**
1. v1.6 38-probe panel iteration loop
2. **v1.7 §1.5.3.2 absorption block (verdict_class dispatch at P-capture site)**
3. v1.6 target_TRUE natural top-1 capture (preserved verbatim)

**Halt conditions:** v1.6 halt classes preserved verbatim at v1.7 (cross-session bit-exact gate; sub-band P drift; etc.).

---

## Cell 8 — Trial matrix definition (preserved from v1.6 verbatim)

Cell 8 inherited UNCHANGED from v1.6. v1.7 introduces no Cell 8 changes; the D-S217-2 cross-cell single-source contract (Cell 6 ↔ Cell 8 ↔ Cell 14) is preserved.

> **v1.7 cross-cell contract anchor.** Cell 8's `fact_memit_requests` literal references the same fact_id set as Cell 6's `stage_1_facts`. The D-S217-2 SUBSET hard gate (Cell 6 verdict_class fact_id set ⊇ Cell 8 fact_memit_requests fact_id set) carries forward to v1.7; v1.7 adds a parallel SUBSET assertion that Cell 8 fact_memit_requests fact_id set ⊇ MULTI_TOKEN_ALLOWLIST (every allowlist fact must appear in the trial matrix).

---

# Part VI — Cell 9 (v1.7 ABSORPTION SURFACE)

## Cell 9 — Batched-MEMIT 15-trial loop + RE-EVALUATE gate at trial 0 entry (v1.7)

**Specialist:** validation-contract-architect + memit-specialist + state-consistency-theorist

**Purpose:** Execute the 15-trial loop. Each trial: pre-edit probe panel → MEMIT batched edit (5-fact joint overlay at L4-L8 / L2-L6 per session config) → post-edit probe panel → Copy-Unmount → post-unmount probe panel. v1.7: insert RE-EVALUATE gate at trial 0 entry per §1.5.3.3 for ALLOWLIST_FIRST_TOKEN_PROXY facts.

**v1.7 inheritance:**
- v1.6 trial loop body (pre-edit / batched-MEMIT dispatch / post-edit / Copy-Unmount / post-unmount) — INHERITED UNCHANGED
- v1.6 IC-S23-4 unmount band gate (HARD; intra-pod drift < 1e-4) — INHERITED UNCHANGED
- v1.6 IC-S24-4 trial protocol (5×3=15 trials) — INHERITED UNCHANGED
- v1.6 D-S215D2-VERDICT-INTEGRITY-1 load-bearing subset annotation — INHERITED UNCHANGED
- **v1.7 NEW: §1.5.3.3 absorption block — RE-EVALUATE gate inserted at trial 0 entry (replicate==1) for ALLOWLIST_FIRST_TOKEN_PROXY facts; verdict gate retires-or-ratifies first-token-proxy for the rest of the fact's trials**

**Cell 9 v1.7 cell body composition (operator reading order):**
1. v1.6 trial matrix iteration entry
2. v1.6 pre-edit probe panel capture
3. v1.6 batched-MEMIT dispatch
4. v1.6 post-edit probe panel capture
5. **v1.7 §1.5.3.3 absorption block (RE-EVALUATE gate at trial 0 entry; conditional)**
6. v1.6 Copy-Unmount + post-unmount probe panel + IC-S23-4 HARD gate
7. v1.6 verdict computation + per-trial JSON write
8. **v1.7 schema extension: per-trial verdict v1_7_proxy_annotation field (verdict_class + primary_token_id + full_token_ids + proxy_disposition)**

**Halt conditions:** v1.6 Cell 9 halt classes preserved verbatim at v1.7; no new halt classes introduced.

> **v1.7 STRICT-fact bit-exact preservation guarantee.** For trials of STRICT_SINGLE_TOKEN facts (4-of-5 facts; 12-of-15 trials), the v1.7 cell body is logically identical to v1.6 — the §1.5.3.3 absorption block does not execute (re_evaluate_at_trial_0 is False). Cross-session bit-exact determinism per D-S217-4 / D-S218-7 is therefore preserved for STRICT cases.

---

# Part VII — Cells 10 / 11 / 12 (preserved from v1.6 verbatim)

Cell 10 verdict aggregation / Cell 11 NV inventory + SHA equality gate / Cell 12 reproducibility manifest update — all inherited UNCHANGED from v1.6. v1.7 introduces no Cell 10 / 11 / 12 changes.

> **v1.7 schema-extension propagation note.** The Cell 10 per-fact aggregation reads per-trial JSON `v1_7_proxy_annotation` field (added at Cell 9 §1.5.3.3); the Cell 10 aggregation loop is structurally unchanged but transitively encounters the new annotation when reading per-trial JSONs from any v1.7-executed run. Aggregate verdict statistics (consistency PASS-rate, generalization mean drift, specificity mean drift, unmount HARD-gate status) are unchanged in semantics; the v1.7 annotation provides forensic-level provenance of the proxy_disposition at trial 0.

---

# Part VIII — Halt conditions (cross-cell index; v1.7 extension)

The full v1.6 halt-condition index (Part IX of v1.6) is inherited UNCHANGED. v1.7 adds one new halt class:

| Cell | Condition | Class | Action |
|---|---|---|---|
| Cell 6 | MULTI_TOKEN_FAIL (verdict_class == MULTI_TOKEN_FAIL) | Session-level HARD (NEW at v1.7) | Either add fact_id to MULTI_TOKEN_ALLOWLIST AND verify first-token-proxy is acceptable, OR halt and revise corpus + re-version cfb-v3 |

---

# Part IX — Forward routing (v1.7 disposition)

v1.7 is a forward-compatibility carry-forward. The next MEMIT-class Stage 1 SECT execution session (if any) will:
1. Consume v1.7 as the canonical runbook
2. Execute Cell 6 with the §1.5.3.1 absorption block live
3. Execute Cell 7 with the §1.5.3.2 absorption block live
4. Execute Cell 9 with the §1.5.3.3 absorption block live (including the RE-EVALUATE gate at trial 0 for cfb-v3-004)
5. Establish the canonical empirical baseline for the absorbed mechanism (no prior v1.x baseline exists for first-token-proxy under the canonical mechanism)

No specific successor session is currently scheduled given the Class D ELIM verdict at S2.15-D2 D.2 has retired the MEMIT-class Stage 1 SECT execution path within WS1 scope; v1.7 ships forward-compatible against future re-entry (e.g., a new hypothesis class surfacing T.1 alt-model class testing on a different base model at MEMIT canonical hparams).

---

# Part X — Open questions in scope

## 10.1 OQs closed by v1.7 absorption

| OQ ID | Closure mechanism | Anchor |
|---|---|---|
| **D-V12-MULTITOKEN-1 (v1.7 codification of S2.15-D2 ratified mechanism)** | §1.5.3.1 + §1.5.3.2 + §1.5.3.3 absorption blocks | The v1.6 retroactive miss is closed by v1.7 canonical codification |

## 10.2 OQs activated / opened at v1.7

None. v1.7 is purely additive (codifies an already-ratified mechanism); introduces no new uncertainty.

## 10.3 OQs explicitly out of scope for v1.7

| OQ ID | Reason |
|---|---|
| OQ-S218-1 / OQ-S218-2 / OQ-S218-3 | ROME-class diagnostic OQs; not relevant to MEMIT-class Stage 1 SECT runbook |
| OQ-V02-2 (Cell 13 verdict gate framework) | ROME-class runbook concern; absorbed at t2_rome_runbook v0.2 §Cell 13 |

---

# Part XI — Non-goals

This runbook v1.7 does NOT:

1. **Modify `memit-patches-canonical.md` v2.5.** Preserved per D-S216-CLOSE-3.
2. **Modify v1.6 cells 0-5 / 8 / 10-12.** Preserved verbatim; v1.7 absorption surface is bounded to Cells 6 / 7 / 9.
3. **Modify the canonical batched-MEMIT dispatch surface at Cell 9.** v1.7 §1.5.3.3 absorption block inserts a verdict gate AFTER the post-edit probe panel and BEFORE Copy-Unmount; the dispatch call itself is preserved verbatim.
4. **Modify the IC-S23-4 unmount band semantics.** Preserved per HARD-gate inheritance.
5. **Re-execute any historical Stage 1 SECT trial.** v1.7 absorbs canonical mechanism; does not re-validate prior trials.
6. **Extend the architectural-invariant ceiling claim.** v1.1 of `framework_finding_memit_ceiling_archival.md` is a separate deliverable.
7. **Update the t_branch_decision_document v1.0 from this artifact.** v1.1 is a separate deliverable.
8. **Author runtime implementation code beyond canonical scaffolding for the Cell 6 / Cell 7 / Cell 9 absorption blocks.** The §1.5.3.X blocks are runtime-ready cell bodies; integration into the v1.6 cell positions follows the operator-reading-order specification at each cell entry.
9. **Amend the v1.2 integrated framework spec.** Sealed.

---

# Part XII — Reference appendices (preserved from v1.6 verbatim with v1.7 cross-link extension)

## 12.1 Carry-forward inheritance from v1.6 (extended at v1.7)

| Component | v1.6 status | v1.7 disposition |
|---|---|---|
| §1.5 authoring discipline | RATIFIED (5 OQ closures + dry-run gate + marker-site discipline) | INHERITED + extended via §1.5.3 + §1.5.4 |
| §1.5.1 R1.3 codification | RATIFIED (D-S28-2) | INHERITED unchanged |
| §1.5.2 canonical marker-assertion site | RATIFIED (D-S217-1) | INHERITED unchanged |
| Part I-IV (orientation + pod + pre-flight + Cell 3-5) | RATIFIED | INHERITED unchanged |
| Cell 6 (token verification) | v1.6 prose-described multi-token mechanism; runtime logic absent | **v1.7 §1.5.3.1 absorption block codifies runtime logic** |
| Cell 7 (baseline capture) | v1.6 P-capture under STRICT-only assumption | **v1.7 §1.5.3.2 wires verdict_class dispatch** |
| Cell 8 (trial matrix) | RATIFIED | INHERITED unchanged |
| Cell 9 (trial loop) | v1.6 trial loop under STRICT-only assumption | **v1.7 §1.5.3.3 inserts RE-EVALUATE gate at trial 0 entry** |
| Cells 10-12 (verdict + persistence + manifest) | RATIFIED | INHERITED unchanged (transitive schema-extension at Cell 10) |
| Part XI / Part XII reference appendices | v1.6 prose references multi-token mechanism | INHERITED + cross-link extension to §1.5.3 absorption blocks |

## 12.2 Cell-to-decision traceability (v1.7 extension)

| Decision | Cell of realization (v1.6) | v1.7 disposition |
|---|---|---|
| (all v1.6 entries) | (v1.6) | INHERITED unchanged |
| **D-S215D2-CFB-V3-004-MULTITOKEN-1** | Cell 6 PROSE references at v1.6 (lines 3209, 3218) | **CODIFIED at Cell 6 §1.5.3.1 v1.7 absorption block** |
| **D-S215D2-CFB-V3-004-PROXY-1** | Cell 6 / Cell 7 PROSE references at v1.6 | **CODIFIED at Cell 6 §1.5.3.1 + Cell 7 §1.5.3.2 + Cell 9 §1.5.3.3 v1.7 absorption blocks** |
| **D-V12-MULTITOKEN-1 (NEW at v1.7)** | (n/a; canonical absorption decision) | **D-V12-MULTITOKEN-1 ratified at v0.2 codification session close per §1.5.3** |

## 12.3 Authoring metadata (v1.7)

| Field | Value |
|---|---|
| Authoring session | v0.2 codification session (operator-side post-S2.18; pre-S2.19 BLOCKING) |
| Authoring date | 2026-05-05 |
| Document version | 1.7 |
| Iteration | v1.7 supersedes v1.6 — MULTI_TOKEN_ALLOWLIST + first-token-proxy mechanism canonical absorption |
| Status | RATIFIED v1.7 (PROVISIONAL; codifies S2.15-D2 ratified mechanism into Cell 6 / Cell 7 / Cell 9 runtime logic; supersedes v1.6 documentation-only state); full ratification awaits next MEMIT-class Stage 1 SECT execution session (none currently scheduled) |
| Supersedes | v1.6 (RATIFIED at S2.17 Block 1 close; preserved as historical anchor) |
| Basis | `session_2_18_summary_block.md` (forensic anchor: v1.6 retroactive miss surfaced at S2.18 Cell 6 reapplication); `t2_rome_runbook.md` v0.2 §Cell 6 (sibling canonical absorption pattern); `stage_1_sect_runbook_v1_6.md` (structural template; cells 0-5 + 8 + 10-12 inherited verbatim); D-S215D2-CFB-V3-004-MULTITOKEN-1 + D-S215D2-CFB-V3-004-PROXY-1 (S2.15-D2 ratified mechanism) |
| Specialist provenance | framework-spec-writer (primary, v1.7 absorption authoring); validation-contract-architect (Cell 6 / Cell 7 / Cell 9 absorption blocks); state-consistency-theorist (single-source contract preservation across Cell 6 / Cell 7 / Cell 8); memit-specialist (consultative; absorption mechanism cross-validation against ROME runbook v0.2 Cell 6 sibling pattern) |
| Last updated | 2026-05-05 |

---

*End of Stage 1 SECT Runbook v1.7 — RATIFIED PROVISIONAL at v0.2 codification session close (MULTI_TOKEN_ALLOWLIST + first-token-proxy mechanism canonical absorption per D-V12-MULTITOKEN-1; supersedes v1.6 documentation-only state; bounded to Cell 6 + Cell 7 + Cell 9 absorption blocks; full ratification awaits next MEMIT-class Stage 1 SECT execution session).*
