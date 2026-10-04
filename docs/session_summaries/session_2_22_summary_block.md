# Session 2.22 — Summary Block

**Session:** S2.22 — T.1-GRACE-3B Stage 1 SECT v3 Pod-Side Execution
**Closed:** 2026-05-05
**Engine:** GRACE_barebones (upstream SHA `f674183f17a995d109e10ee6140d4c3e6d016115` + P-1-GRACE + P-2-GRACE + Pad-Token + F-2)
**Engine repo:** `https://github.com/Thartvigsen/GRACE.git` (re-pinned from `MichaelLSY/grace.git` per D-S222-ENGINE-REPIN-1)
**Model:** `meta-llama/Llama-3.2-3B` fp16 (revision SHA pinned at S2.22 Cell 5 entry)
**Hardware:** RunPod RTX 4090 24 GiB, NV `s1xi9zhfc2`
**Predecessor:** S2.21 (T.1-GRACE-3B retry runbook v0.1 authoring)
**Successor:** S2.23 = T.1 alt-model under MEMIT runbook v0.1 authoring (per t_branch_decision_document v1.1 §5'-α)

---

## §1. Verdict

### §1.1 Verdict Class

`ROUTE_A_HALT_MECHANISM_3B`

### §1.2 Verdict Statement

T.2 GRACE adapter mechanism is structurally executable on Llama-3.2-3B at canonical hparams (training updates `values` parameter via Adam over n_iter=200; key registration produces target-position-locked activation; F-2 dispatch preamble effective; unmount drift `0.00e+00` at both layers). However, the discriminator gate at canonical hparams (`init_epsilon=1.0`, `key_id=-1`, `generation=False`) structurally never fires at any probe — the key encodes a post-target activation while inference probes produce pre-target activations 6.4–8.7× outside the eps-ball. Both Layer-A (L17) and Layer-B (L2) reproduce identical pathology (38/38 bit-exact pre==post probes; cross-layer signature). The S2.20 environmental ceiling on Llama-3.1-8B is EMPIRICALLY ELIMINABLE (peak VRAM ~6.5 GiB vs RTX 4090 24 GiB ceiling), but the adapter mechanism produces zero observable edit at canonical-spec hparams.

### §1.3 Verdict Strength Matrix

| Claim | Status |
|---|---|
| T.2 GRACE adapter mechanism executable on Llama-3.2-3B at canonical environment | EMPIRICALLY VALIDATED |
| S2.20 environmental ceiling eliminable on smaller model | EMPIRICALLY VALIDATED |
| Adapter mechanism produces zero observable edit at canonical hparams | EMPIRICALLY VALIDATED (cross-layer; replay-precedent risk LOW) |
| NARROW_BY_DESIGN structural pathology (key + query position mismatch) | NEW EMPIRICAL FINDING |
| Adapter elimination is hparam-class-scoped, NOT architectural-invariant | EMPIRICALLY ARGUED |
| Hparam-corrected GRACE retry could fire discriminator | UNTESTED (orthogonal investigation per audit remediation_class) |

### §1.4 Block C Disposition

`BYPASSED`. Block C 15-trial loop entry forecloses by Route A halt per t_branch_decision_document v1.1 §5'-α with audit verdict NARROW_BY_DESIGN substituting for S-β (per OQ-S222-AUDIT-CATEGORY-EXTENSION-1).

---

## §2. Decisions Ratified

### §2.1 Decision Inventory (NEW at S2.22)

| ID | Statement (compressed) | Closure Cell |
|---|---|---|
| D-S222-ENGINE-REPIN-1 | Engine source URL re-pinned from `MichaelLSY/grace.git` (gated/deleted; 403 at S2.22) to `Thartvigsen/GRACE.git` (canonical NeurIPS 2023 source); SHA `f674183f...` byte-identical between forks (verified via 9-site P-1-GRACE line numbers + 1-site P-2-GRACE line) | Cell 1 |
| D-S222-PATH-DRIFT-1 | Source path corrected `grace/grace/editors/grace_barebones.py` → `grace/editors/grace_barebones.py` (single dir level under canonical Thartvigsen/GRACE layout); also `sys.path.insert("/workspace/grace_dry_run/grace")` → `sys.path.insert("/workspace/grace_dry_run")` at Cell 8 | Cell 1.0 + Cell 2++ + Cell 8 |
| D-S222-TRANSFORMERS-PIN-1 | `transformers==5.7.0` pinned at Cell 0+ for environment-parity with S2.20 baseline; +accelerate +hydra-core +pyyaml +sentencepiece installed explicitly | Cell 1.5+ |
| D-S221-CHECKPOINT-1-1 (carry-forward; ratified) | Llama-3.2-3B chain Checkpoint #1 ESTABLISHED at S2.22 Cell 5; predecessor Llama-3.1-8B chain (#1–#7) NOT carry-forward across model classes; preserved on NV | Cell 5.5 / 5.6 |
| D-S221-VRAM-PROJECTION-1 (carry-forward; ratified) | ~9.47 GiB projected; actual peak 6.47 GiB (L17) / 6.48 GiB (L2) — better than projection; 17.5 GiB headroom on RTX 4090 | Cell 9.6 + Cell 11.6 |
| D-S222-AUDIT-VERDICT-NARROW-1 | NARROW_BY_DESIGN audit class introduced — mechanism executes (training updates values; key registers at target-position) but discriminator structurally never fires at canonical hparams (key_id=-1 + generation=False + init_epsilon=1.0); audit subchecks 1–3 PASS, subcheck 4 FAIL | Cell 11++ |
| D-S222-V1-2-DISPOSITION-1 | v1.2 disposition refined from kickoff §7 anticipated `MECHANISM_CLASS_ELIMINATION_STRONGER_THAN_V1_0` → `ADAPTER_MECHANISM_NON_VIABLE_AT_CANONICAL_HPARAMS`; mechanism is structurally executable, what is non-viable is the canonical-hparams configuration | Cell 13 |
| D-S222-V1-3-SCOPE-REFINEMENT-1 | v1.3 amendment scope refined: rank-1-in-weight (v1.0 + v1.1) remains architectural-invariant; adapter-class non-viability at canonical-spec hparams is hparam-conditional and operator-remediable; NOT architectural-invariant elimination of adapter class | Cell 13 |
| D-S222-S223-ROUTING-1 | S2.23 = T.1 alt-model under MEMIT runbook v0.1 authoring (resumes t_branch §5'-α canonical path); operator may pursue hparam-corrected GRACE retry as orthogonal investigation outside Workstream 1 critical path | Cell 13 |

### §2.2 Decision Lifecycle Notes

D-S221-Q1-1..Q5-1 (anticipated decisions per S2.21 kickoff §9.2) all RATIFY at S2.22 in declarative form — runbook structural inheritance verbatim with §6.1 substitutions held; Cell 18 INAPPLICABLE held; layer corridor preservation (L17 + L2) held; fresh baseline capture at Cell 5 held; F-2 dispatch preamble inherited verbatim held.

D-S221-VRAM-PROJECTION-1 RATIFIES with stronger-than-projected evidence (6.5 GiB peak vs 9.47 GiB projected).

D-S222-PATH-DRIFT-1 surfaces a unsolved anomaly: `MichaelLSY/grace` and `Thartvigsen/GRACE` shared SHA `f674183f` (mathematically implies identical tree by Git's content-addressable design), yet the S2.20 runbook used path `grace/grace/editors/...` which empirically worked at S2.20 against `MichaelLSY/grace`. Either S2.20 anchor SHA was actually different (possible misreading carried forward in records), or the doubled-path was a benign typo that resolved via filesystem-level coincidence at S2.20. Documented as forensic record; closure deferred — the engine source byte-identity at the canonical Thartvigsen/GRACE SHA was empirically verified via 9-site P-1-GRACE line-number match.

---

## §3. Constraints Established

| ID | Statement | Verification Site |
|---|---|---|
| C-S222-1 | Engine source SHA-equality verification gate before re-pinning to alternate fork; verify via `git ls-remote <alt-repo> <sha>` returning `<sha> HEAD` AND patch site line numbers byte-identical to canonical anchor | Cell 1.0 (P-1-GRACE 9-site verification) |
| C-S222-2 | Cell 0 explicit Python dep set: `transformers==5.7.0` + `accelerate` + `hydra-core` + `pyyaml` + `sentencepiece` installed before any model load attempt; v0.2 Cell 0 expansion absorbs this | Cell 0+ |
| C-S222-3 | Pre-flight `git ls-remote https://USER:${HF_TOKEN}@huggingface.co/<gated-repo> HEAD` against gated model URL BEFORE Cell 5 model load attempt; surfaces 403 (license) vs 401 (token) early | (operator-side; Pre-Cell-5) |
| C-S222-4 | Patch application cells must print explicit acceptance string (e.g., "P-2-GRACE applied; marker assertion PASS") AND operator confirms before proceeding; downstream cell PASS does not imply upstream patch cell PASS | Cell 2++++ recovery |
| C-S221-1 (RATIFIED) | Llama-3.2-3B revision SHA pinning at S2.22 Cell 5 entry; SHA recorded in Cell 20 manifest extension | Cell 5.2 |
| C-S221-2 (RATIFIED) | Tokenizer continuity verification gate at Cell 6; allowlist parity `{"cfb-v3-004"}` confirmed under Llama-3.2 tokenizer | Cell 6 |
| C-S221-3 (RATIFIED) | Layer-set validity assertion: n_layer=28, hidden_size=3072, intermediate_size=8192, L17/L2 valid | Cell 5.3 |
| C-S221-4 (RATIFIED) | down_proj shape `Linear(8192, 3072)` forensic anchor | Cell 8 |
| C-S221-5 (RATIFIED) | Fresh baseline capture as Llama-3.2-3B chain Checkpoint #1 | Cell 5.5 / 5.6 |

---

## §4. Open Questions

### §4.1 NEW at S2.22 — CLOSED

| ID | Statement | Closure |
|---|---|---|
| OQ-S222-CELL1-1 | Cell 1 idempotency gap: pre-existing `/workspace/grace_dry_run/` from prior session conflicts with `git clone` | CLOSED — recovery via `rm -rf` + re-clone; v0.2 Cell 1 absorbs detect-existing + verify-SHA + skip-clone-if-match logic |
| OQ-S222-CELL1-3 | Engine source URL canonical anchor question | CLOSED informational — Thartvigsen/GRACE confirmed canonical NeurIPS 2023 source; future T.X-GRACE-* runbooks anchor here |
| OQ-S222-CELL2-PATCH-INTEGRITY-1 | Verify P-1-GRACE 9 sites at lines `[44, 53, 56, 57, 62, 76, 77, 78, 79]` exist in Thartvigsen/GRACE source at SHA | CLOSED PASS — exact line-number match confirmed |
| OQ-S222-HF-GATING-1 | Llama-3.2-3B gated separately from Llama-3.1-8B even under same HF account/token | CLOSED — operator-side license acceptance on robertrhu account; v0.2 Cell 5 halt class table distinguishes 401 (token) vs 403 (repo) |
| OQ-S221-1 | Llama-3.2 tokenizer leading-space convention parity with Llama-3.1 | CLOSED PASS — allowlist `{"cfb-v3-004"}` parity confirmed; pad_token_id=128001 identical |
| OQ-S221-2 | down_proj shape impact on adapter value parameter shape | CLOSED — `value_shape=3072` automatic via `nn.Parameter(torch.zeros(out_features))`; no code change needed |
| OQ-S221-3 | hf_cache reusability across model classes | CLOSED PASS — `/workspace/hf_cache` accepted Llama-3.2-3B download alongside Llama-3.1-8B without conflict (60GiB total) |
| OQ-S222-TARGET-TRUE-SEMANTICS-1 | Llama-3.2-3B natural top-1 at canonical prompt | CLOSED informational — possessive pronoun (`' his'`/`' her'`) for all 5 subjects; confirms NULL-prior regime per cfb-v3 corpus design |
| OQ-S222-AUDIT-CATEGORY-EXTENSION-1 | Cell 11++ audit categories at v0.2 do not include NARROW_BY_DESIGN | CLOSED — v0.2 absorption: extend audit category enum; routing predicate at Cell 13 treats NARROW_BY_DESIGN as structural-elimination-equivalent at canonical-hparams scope |
| OQ-S222-V1-3-AMENDMENT-SCOPE-REFINEMENT-1 | Kickoff §7 anticipated "mechanism-class elimination stronger than v1.0"; empirical finding refines scope | CLOSED — v1.3 amendment scope hparam-class-scoped; v1.0 + v1.1 architectural-invariant claims unchanged |
| OQ-S221-VRAM-PROJECTION (informal) | ~9.47 GiB projection accuracy | CLOSED — actual peak 6.47–6.48 GiB; projection conservative |

### §4.2 NEW at S2.22 — OPEN

| ID | Statement | Closure Path |
|---|---|---|
| OQ-S222-CELL1-2 | Engine source NV snapshot — canonical engine SHA pin assumes immutable public Git access; S2.20 → S2.22 break (24-hour interval) demonstrates external Git availability is NOT a safe assumption | LOAD-BEARING; v0.2 absorption: Cell 1 should snapshot consumed engine source files to `/workspace/architecture_profile/engine_source_snapshot/<engine-sha>/` at first successful clone; future T.X-GRACE-* sessions reconstruct from NV without external dependency |
| OQ-S222-CELL0-DEPS-1 | Cell 0 (inherited from t2_grace_runbook v0.2 §2.1) installs `typing_extensions` + `wandb` only, assumes `transformers` + `accelerate` + `hydra-core` + `pyyaml` + `sentencepiece` preinstalled in pod base image; assumption fails on fresh pod | v0.2 absorption: Cell 0 expansion + transformers pin |
| OQ-S222-SURFACE-LABELING-1 | Runbook v0.1 (and inherited v0.2) does not explicitly label cell execution surface (terminal vs notebook); mid-session ambiguity is operator friction | v0.2 absorption: each cell heading carries explicit Surface: A (terminal) / Surface: B (notebook) annotation |
| OQ-S222-CELL-EXEC-VERIFICATION-1 | Cell 2++++ output assumed PASS without explicit confirmation; downstream Cell 4 PASS silently masked missing P-2-GRACE patch until Cell 9 dispatch | v0.2 absorption: every patch-application cell prints unique acceptance string; operator AND agent confirm line before proceeding |
| OQ-S222-CELL10-CATEGORY-1 | Cell 10/12 specificity filter literal `"specificity"` does not match probe-set-v3 actual category `"specificity_shared"`; corrected at S2.22 Cell 10 | v0.2 absorption: propagate fix to all cells filtering on probe category; rename literal across runbook |
| OQ-S222-CALIBRATION-CRITERIA-MISMATCH-1 | Runbook §3.2.2 generalization PASS criterion (`max(gen_p_target_new) > 0.3`) measures "edit transfers to non-canonical prompts"; YAML §126 acceptance band (`abs(p_top_1_post - p_top_1_pre) < 0.05`) measures locality stability — different empirical claims | v0.2 absorption: align runbook + YAML semantic intent; resolve which generalization criterion is canonical |
| OQ-S222-PATH-DRIFT-PROVENANCE-1 | S2.20 runbook used `grace/grace/editors/...` path which worked empirically; SHA-equality between MichaelLSY/grace and Thartvigsen/GRACE implies identical tree, contradicting doubled path; reconciliation unclear | Forensic record; deferred (does not block forward routing) |

### §4.3 Carry-forward from S2.20 (still OPEN)

| ID | Statement | Closure Path |
|---|---|---|
| OQ-S220-MANIFEST-1 | Reproducibility manifest tracks 4 sessions despite 8+ session history | DEFERRED — root cause investigation; orthogonal to forward routing |
| OQ-S220-CFB-PATH-1 | Corpus path migration to per-engine path | DEFERRED — operator-side decision; runbook v0.1 inherited S2.20 path verbatim and worked |
| OQ-S220-RTX-A100-MIGRATION-1 | Operator-side hardware migration to A100 80 GiB | DE-PRIORITIZED — S2.22 confirms environmental ceiling at S2.20 was eliminable on smaller model; A100 migration not needed for T.2 GRACE viability investigation |

---

## §5. Interface Contracts Defined

### §5.1 IC-S222-1: NARROW_BY_DESIGN Audit Verdict Class

**Contract:** Cell 11++ verdict integrity audit category enum extends to include NARROW_BY_DESIGN, defined by:

| Subcheck | NARROW_BY_DESIGN signature |
|---|---|
| 1 — adapter param registered | PASS (`adapter._parameters['values']` is nn.Parameter with requires_grad=True) |
| 2 — loss differentiable / gradient flow | PASS (Adam updates `values` over n_iter; L2 norm transitions from random init to nontrivial value) |
| 3 — mechanism executes at inference | PASS (GRACEAdaptor.forward runs on probes; pre_hook captures input activations) |
| 4 — discriminator gate fires at any probe | FAIL (smallest_dist > init_epsilon for all probes; structural mismatch) |

**Routing implication:** NARROW_BY_DESIGN is structural-elimination-equivalent at canonical-hparams scope — Route A halt with v1.2 disposition `ADAPTER_MECHANISM_NON_VIABLE_AT_CANONICAL_HPARAMS` (NOT `STRUCTURAL_ELIMINATION` because mechanism is executable).

### §5.2 IC-S222-2: Hparam-Scoped vs Architectural-Invariant Disposition Labeling

**Contract:** v1.3 amendment scope distinguishes:
- **Architectural-invariant ceiling** — eliminable hypothesis class; rank-1-in-weight (v1.0 + v1.1); not amenable to hparam tuning within the eliminated class
- **Hparam-conditional ceiling** — adapter-class non-viability at canonical-spec hparams; potentially remediable by `key_id` correction, `init_epsilon` widening, or `generation=True` tracking; remediation orthogonal to Workstream 1 critical path

v1.3 amendment authoring at S2.23 close (or successor codification session) MUST preserve this distinction.

### §5.3 IC-S222-3: Position-Locked Key + Pre-Target Query Mismatch Finding

**Contract:** GRACE_barebones at canonical hparams (`key_id=-1`, `generation=False`):

| Time | Action | Position |
|---|---|---|
| Edit (n_iter forward) | `key = activation[args[0][:, -1, :]]` registered at `args[0].shape[1]-1` | Last token of prompt+target = target-position activation |
| Inference | `query = activation[args[0][:, -1, :]]` | Last token of probe = pre-target activation (probes do NOT include target token) |

**Consequence:** Distance between key and any probe-derived query is structurally bounded below by the activation distance between adjacent sequence positions, which empirically exceeds `init_epsilon=1.0` by factor 6–9× in 8192-dim fp16 hidden state (L17 input).

**Remediation paths (out of scope for Workstream 1):**
- `generation=True` enables `key_id` to track via labels `(labels == -100).sum() - 1`, registering key at last prompt token (pre-target)
- `init_epsilon ≥ 10` widens eps-ball to encompass typical pre-target activation distances
- Explicit `key_id` override at edit time

---

## §6. NV State + Cells Executed

### §6.1 NV Inventory Snapshot

```
/workspace                 112G  (utilization 74%; 320 TiB available)
/workspace/architecture_profile  7.7M
/workspace/grace_dry_run         12M
/workspace/hf_cache              60G  (Llama-3.1-8B + Llama-3.2-3B)
```

### §6.2 S2.22 Outputs (10 files in /workspace/architecture_profile/)

| Filename | Size | Purpose |
|---|---|---|
| llama_3_2_3b_baselines.json | 37.8 KB | Cell 5.5/5.6 — Llama-3.2-3B chain Checkpoint #1 baseline |
| t1_grace_3b_pre_edit_baseline.json | 16.3 KB | Cell 7 — pre-edit reference frame |
| t1_grace_3b_post_edit_l17.json | 10.0 KB | Cell 9 — Layer-A post-edit P-values |
| t1_grace_3b_post_edit_l2.json | 10.0 KB | Cell 11 — Layer-B post-edit P-values |
| t1_grace_3b_verdict_l17.json | 1.4 KB | Cell 10 — Layer-A verdict surface |
| t1_grace_3b_verdict_l2.json | 0.8 KB | Cell 12 — Layer-B verdict surface |
| t1_grace_3b_pre_post_bit_exact.json | 0.1 KB | Cell 11+ — INSTALLATION_FALSIFIED tag |
| t1_grace_3b_verdict_audit.json | 0.8 KB | Cell 11++ — NARROW_BY_DESIGN audit record |
| t1_grace_3b_routing.json | 2.7 KB | Cell 13 — Route + v1.2 disposition + v1.3 scope + S2.23 routing |
| t1_grace_3b_patch_state.json | 0.8 KB | Cell 2++ + Cell 2++++ — patches manifest |

### §6.3 Cell Sequence Executed

```
Block A: Cells 0+ → 1 → 1.0 → 1.5+ → 2 → 2++ → 2++++ → 3 → 4 → 5.1 → 5.2 → 5.3 → 5.4 → 5.5 → 5.6 → 6 → 7 → 8     COMPLETE
Block B: Cells 9 → 9-recovery → 10 → 11 → 11+ → 11++ → 12 → 13                                                     COMPLETE
Block C: Cells 14–17                                                                                               BYPASSED (Route A)
Block-end: Cells 18 → 19 → 20                                                                                      COMPLETE
```

### §6.4 Recovery Cell Inventory

S2.22 required substantial mid-session recovery beyond the runbook v0.1 declarative scope:

| Recovery point | Trigger | Resolution |
|---|---|---|
| Cell 0+ deps expansion | `transformers` not preinstalled; ImportError at Cell 1.5+ | Install transformers==5.7.0 + accelerate + hydra-core + pyyaml + sentencepiece (Surface A); kernel restart |
| Cell 1 idempotency | Pre-existing `/workspace/grace_dry_run/` partial-state conflict | rm -rf + re-clone |
| Cell 1 engine repo-pin | `MichaelLSY/grace.git` 403 (gated/deleted) | Re-pin to `Thartvigsen/GRACE.git` at same SHA (D-S222-ENGINE-REPIN-1) |
| Cell 1.0 path drift | S2.20 runbook path `grace/grace/editors/...` does not exist under canonical layout | Path correction to `grace/editors/...` (D-S222-PATH-DRIFT-1) |
| Cell 5 HF gating | 403 GatedRepoError on Llama-3.2-3B (separate license from 3.1) | Operator-side license acceptance on `robertrhu` account |
| Cell 5.2 placeholder | `MODEL_REVISION = "<PASTE-SHA-HERE>"` literal triggered RevisionNotFoundError | Re-run with actual SHA |
| Cell 5.5 schema | Probe key `id` vs actual `probe_id`; corpus `target_true` placeholder | Cell 5.5 v2 with corrected key + natural-top-1 capture |
| Cell 9 patch state | P-2-GRACE never applied (Cell 2++++ silently skipped); RuntimeError "cdist_cuda not implemented for Half" | Diagnostic + recovery cell: restore L17 + apply P-2-GRACE + reload + verify |
| Cell 10 category filter | Specificity filter literal `"specificity"` ≠ actual `"specificity_shared"` | Filter literal corrected at S2.22; v0.2 absorption flagged |
| Cell 11+/11++ predicate | Bit-exact 38/38 initially read as INSTALLATION_FALSIFIED; deeper diagnostic reveals NARROW_BY_DESIGN | Audit verdict class extended (IC-S222-1) |

---

## §7. Carry-Forward Anchors for S2.23

### §7.1 Load-Bearing State

| Anchor | Status | Carry-forward |
|---|---|---|
| Llama-3.2-3B chain Checkpoint #1 | RATIFIED via fresh baseline capture | Reference frame for any future Llama-3.2-3B re-execution (T.X-GRACE-3B retry, MEMIT/ROME on 3B) |
| Llama-3.1-8B chain (#1–#7) | PRESERVED on NV | NOT consumed at S2.23; available for future return to 8B execution |
| Patches `{P-1-GRACE, P-2-GRACE, Pad-Token, F-2}` | EMPIRICALLY VALIDATED | Active for any future GRACE retry; v0.2 codification absorbs S2.22 enrichment |
| Engine source `Thartvigsen/GRACE` at SHA `f674183f` | EMPIRICALLY VALIDATED via patch site line-number match | Future T.X-GRACE-* anchors here |
| Cross-session bit-exact within Llama-3.2-3B chain | NOT YET established (Cell 5 was producer; consumer at S2.23+) | First C-S220-3 application at next 3B re-execution |
| `cfb-v3.yaml v1.0` corpus | RATIFIED | Consumed at any successor session |
| `probe-set-v3.yaml v1.0` | RATIFIED | Consumed at any successor session |
| `MULTI_TOKEN_ALLOWLIST = {"cfb-v3-004"}` | RATIFIED PARITY across Llama-3.1 + Llama-3.2 tokenizers | Carries forward |

### §7.2 Eliminated Hypotheses (Updated through S2.22)

| Hypothesis | Status | Source |
|---|---|---|
| H-A through H-G (S2.20 carry-forward) | as documented at S2.20 close §11.3 | unchanged |
| **H-S222-A — adapter mechanism not executable on smaller Llama-class model** | FALSIFIED | Cell 9 + Cell 11 dispatch complete in 14s wall-time; values trained; key registered |
| **H-S222-B — environmental ceiling at S2.20 propagates to model-size invariance** | FALSIFIED | Peak VRAM 6.47–6.48 GiB on 3B vs 24.64 GiB on 8B at canonical hparams |
| **H-S222-C — adapter discriminator at canonical hparams fires at instrument-cluster probes** | FALSIFIED | All 38 probes 6.4–8.7× outside eps-ball at both layers; bit-exact 38/38 pre==post |
| **H-S222-D — adapter elimination at canonical hparams is layer-class-tunable** | FALSIFIED | L17 + L2 produce identical pathology; cross-layer signature |
| **H-S222-E — adapter elimination is architectural-invariant of adapter class** | NOT TESTABLE WITHIN S2.22 | Audit remediation_class HPARAM_OR_CONFIG implies hparam-corrected retry could fire discriminator; orthogonal investigation deferred |

---

## §8. Routing Forward — S2.23

### §8.1 Successor Session Determination

| Element | Value |
|---|---|
| Scope | T.1 alt-model under MEMIT runbook v0.1 authoring (resumes t_branch §5'-α canonical path) |
| Authoring target | `t1_alt_model_<base>_runbook v0.1` (declarative; mirrors S2.21 authoring posture) |
| Alt model candidate set | Llama-3.2-3B (this session's model, with MEMIT on Llama-class smaller) / Mistral-7B / Qwen-7B |
| Direct structural template | `stage_1_sect_runbook v1.7` (MEMIT-side; supersedes T.1-GRACE-3B as inheritance source) |
| Patches canonical | `memit-patches-canonical v2.5` (MEMIT-side; sibling to grace-patches v0.2 + rome-patches v0.2) |
| Hypothesis class | T.1 alt-model under MEMIT — disambiguates whether v1.0 + v1.1 architectural-invariant ceiling generalizes to (model × hparams) or is Llama-3.1-8B-specific |

### §8.2 Orthogonal Investigation (deferred; out of WS1 critical path)

| Investigation | Scope |
|---|---|
| Hparam-corrected GRACE retry on Llama-3.2-3B | Vary `init_epsilon` (1.0 → 10.0), `generation=True`, explicit `key_id` override; tests whether NARROW_BY_DESIGN is fully remediable |
| GRACE on alt-model under non-canonical hparams | Combines T.1 + hparam variation; richer experimental surface but exponentially more cells |

### §8.3 v1.3 Amendment Scope (anticipated for codification)

`framework_finding_memit_ceiling_archival v1.3` (forthcoming) absorbs:
- v1.2 (S2.20 environmental ceiling on 8B; eliminable)
- ADAPTER_MECHANISM_NON_VIABLE_AT_CANONICAL_HPARAMS finding from S2.22 (hparam-conditional, NOT architectural-invariant)
- NARROW_BY_DESIGN audit category as canonical at adapter-class

v1.0 + v1.1 (rank-1-in-weight architectural-invariant) preserved verbatim.

### §8.4 KB Hygiene at S2.23 Entry

| Required uploads (Surface: kickoff prompt) | Rationale |
|---|---|
| `stage_1_sect_runbook v1.7` | LOAD-BEARING; MEMIT-side direct structural template |
| `memit-patches-canonical v2.5` | LOAD-BEARING; patch inheritance for MEMIT alt-model retry |
| `cfb-v3.yaml v1.0` | LOAD-BEARING (or replacement if alt-model tokenizer triggers MULTI_TOKEN_FAIL outside allowlist) |
| `probe-set-v3.yaml v1.0` | LOAD-BEARING (or replacement) |
| `framework_finding_memit_ceiling_archival v1.2` | LOAD-BEARING for routing rationale |
| `t_branch_decision_document v1.1` | routing rationale at §5'-α |
| `session_2_22_summary_block.md` | predecessor session reference |

| Recommended removals at S2.23 entry | Rationale |
|---|---|
| `t1_grace_3b_runbook v0.1` | T.1-GRACE-3B closed; not load-bearing for T.1 alt-model authoring |
| `grace-patches-canonical v0.2` | GRACE-side; INAPPLICABLE for MEMIT-side authoring |
| `t2_grace_runbook v0.2` | sibling reference; not consumed |

---

## §9. Session Close Posture

### §9.1 Forward Action

| Step | Action | Owner |
|---|---|---|
| §9.1.1 | Operator endorses S2.22 close artifacts | operator |
| §9.1.2 | Operator scheduling for v0.2 codification analog session (recommended pre-S2.23) — absorbs OQ-S222-CELL0-DEPS-1 / OQ-S222-CELL1-1 / OQ-S222-CELL1-2 / OQ-S222-CELL10-CATEGORY-1 / OQ-S222-AUDIT-CATEGORY-EXTENSION-1 + IC-S222-1/2/3 into grace-patches-canonical v0.3 + t2_grace_runbook v0.3 + t1_grace_3b_runbook v0.2 + framework_finding v1.3 | operator |
| §9.1.3 | S2.23 kickoff prompt authoring with T.1 alt-model under MEMIT scope | agent |
| §9.1.4 | Decision: operator pursues hparam-corrected GRACE orthogonal investigation OR holds for WS3 implementation phase | operator |

### §9.2 Verdict Integrity Posture

S2.22 verdict ROUTE_A_HALT_MECHANISM_3B with audit verdict NARROW_BY_DESIGN is **load-bearing at hparam-class scope, not architectural-invariant scope**. Distinction matters for v1.3 amendment authoring and Workstream 3 implementation guidance — adapter mechanisms remain on the table for WS3 with appropriate hparam configuration; only canonical-spec configuration is eliminated for fact-knowledge editing under cluster-shifted prompt classes.

---

**Session 2.22 CLOSED 2026-05-05.**

**Persistence:** `/mnt/user-data/outputs/session_2_22_summary_block.md`
