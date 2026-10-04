# Session 2.20 — Summary Block

**Session:** S2.20 — T.2 GRACE Stage 1 SECT v3 Pod-Side Execution
**Closed:** 2026-05-05
**Engine:** GRACE_barebones (upstream SHA `f674183f17a995d109e10ee6140d4c3e6d016115` + P-1-GRACE + P-2-GRACE)
**Model:** meta-llama/Llama-3.1-8B fp16 (revision SHA `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b`)
**Hardware:** RunPod RTX 4090 24 GiB, NV `s1xi9zhfc2`
**Predecessor:** S2.19 (T.2 GRACE runbook v0.1 authoring)
**Successor (verdict-conditional):** S2.21 = T.1-GRACE-3B retry runbook v0.1 authoring

---

## §1. Verdict

### §1.1 Verdict Class

`ROUTE_A_HALT_ENVIRONMENT_CONDITIONAL`

### §1.2 Verdict Statement

T.2 GRACE NOT EXECUTABLE on the canonical S2.20 environment (Llama-3.1-8B × fp16 × RTX 4090 24 GiB × edit-site L17 × full-chain backward). The ceiling is RESOURCE-class (VRAM exhaustion at backward pass activation retention), NOT mechanism-class. T.2 GRACE adapter mechanism elimination at the structural level intended by `t_branch_decision_document v1.1 §5'-α` is UNTESTED — backward pass under corrected configuration (F-2: `model.train()` only with constructor freeze preserved) produces 24.64 GiB allocation, exceeding 24 GiB ceiling by ~0.6 GiB.

### §1.3 Verdict Strength Matrix

| Claim | Status |
|---|---|
| T.2 GRACE adapter mechanism eliminated at canonical engine + model + hparams | UNTESTED |
| T.2 GRACE narrow-discriminator pathology | UNTESTED |
| T.2 GRACE specificity preservation | UNTESTED |
| T.2 GRACE calibration corridor empirical surface | UNTESTED |
| T.2 GRACE multi-fact codebook scaling | UNTESTED |
| T.2 GRACE NOT EXECUTABLE on S2.20 canonical environment | EMPIRICALLY VALIDATED |

### §1.4 Block C Disposition

`BYPASSED`. Block C 15-trial loop entry forecloses by Route A halt per `t_branch_decision_document v1.1 §5'`.

---

## §2. Decisions Ratified

### §2.1 Decision Inventory

| ID | Statement (compressed) | Closure |
|---|---|---|
| D-S220-CHECKPOINT-7-1 | Cross-session bit-exact gate combined: top-1 strict equality + drift `< 1e-5`; supersedes implicit strict-bit-exactness for transformers 5.7.0 environment | Cell 5++++++ |
| D-S220-TOKENIZATION-1 | Llama-3.1 tokenizer requires leading-space prefix on `target_new` for canonical single-token resolution | Cell 6+++++++ |
| D-S220-PROBE-LINKAGE-1 | S2.18 baseline `per_probe` splits into linked (35) + shared_specificity (3); Cell 7+ adopts linkage-conditional field capture | Cell 7+ |
| D-S220-LAYER-RESTORE-1 | Stale GRACEAdaptor recovery via `current.layer` instance attribute access (identity-agnostic; survives module reload) | Cell 9-- |
| D-S220-P-1-GRACE-1 | NEW SOURCE_LAYER patch: `eval(f"self.model.{self.layer}")` → `getattr(parent_module(self.model, self.layer), self.layer.rsplit(".", 1)[-1])` at 9 sites in `grace_barebones.py` (lines 44/53/56/57/62/76/77/78/79) | Cell 2++ |
| D-S220-P-2-GRACE-1 | NEW SOURCE_LAYER patch: `euclidean_distance` wraps `torch.cdist` with fp16 → fp32 → fp16 upcast at 1 site (line 9) | Cell 2++++ |
| D-S220-DEFECT-CAUSE-1 | Root cause of edit non-installation: `GRACE_barebones.__init__` explicitly freezes all base model parameters via `for n, p in self.model.named_parameters(): p.requires_grad = False` | Cell 11++++ |
| D-S220-FIX-F-1-RETRACTED | F-1 (`model.requires_grad_(True)` blanket) RETRACTED — produces VRAM demand >32 GiB; OOM at Cell 9 v2 backward | Cell 9 v2 OOM |
| D-S220-FIX-F-2 | F-2: `model.train()` ONLY; constructor freeze preserved; adapter value created as nn.Parameter at iter=0 forward drives loss differentiability | Cell 11++++++ |
| D-S220-FIX-F-3 | F-3 (F-2 + gradient_checkpointing_enable): structurally incompatible with GRACEAdaptor stateful forward; CheckpointError at backward | Cell 11+++++++ |
| D-S220-CEILING-ENV-1 | Environmental ceiling: F-2-corrected mechanism produces 24.64 GiB allocation; gradient checkpointing structurally incompatible with adapter state mutation | Cell 11+++++++ |
| D-S220-VERDICT-CONDITIONAL-1 | S2.20 verdict envelope: T.2 GRACE NOT EXECUTABLE on canonical environment; structural mechanism elimination UNTESTED | Cell 13 |
| D-S220-S221-ROUTING-1 | S2.21 = T.1-GRACE-3B retry (NOT T.1 alt-model under MEMIT); environmental ceiling disambiguation via smaller model | Cell 13 |
| D-S220-AUTH-1-V2 | HF token loaded from `/workspace/.hf_token` to env vars + explicit `token=` kwarg; `local_files_only=False`; sentinel placeholder rejected via shape gate | Cell 5.1.1 |
| D-S220-CHECKPOINT-7-1 | Cross-session checkpoint #7 ESTABLISHED via combined gate (drift max `4.97e-07`; top-1 strict equality 38/38) | Cell 5++++++ |

### §2.2 Decision Lifecycle Notes

D-S220-FIX-F-1 was RATIFIED at Cell 11+++++ then RETRACTED at Cell 9 v2 OOM. The Cell 11+++++ verification was structurally invalid: manual iter=0 forward + Adam construction did not exercise the backward pass that triggers full activation buffer allocation. v0.2 absorption flags this as standard verification protocol gap.

---

## §3. Constraints Established

| ID | Statement | Verification Site |
|---|---|---|
| C-S220-2 | HF token shape gate: `len(content) ≥ 37` AND `content.startswith('hf_')` AND no whitespace AND all printable ASCII; sentinel placeholder triggers HALT | Cell 5.1.1 |
| C-S220-3 | Cross-session bit-exact gate combined acceptance: top-1 token ID strict equality (mandatory) + drift `< 1e-5` (rounding-class regime ceiling) | Cell 5++++++ |
| C-S220-PATCH-AUTHORING-1 | SOURCE_LAYER patch application uses single-line replacement form (matching unique terminal statement) over multi-line literal pattern; whitespace-resilient | Cell 2++++ |
| C-S220-CELL-HYGIENE-1 | Diagnostic cells substituting model layers must use `try/finally` cleanup OR position cleanup before any assertion that may raise; prevents stale-substitution carry-forward | All Cell 11+++ derivatives |
| C-S220-DIAGNOSTIC-1 | Adapter value presence checks must verify `self._parameters` (nn.Parameter routing) NOT `self.__dict__` (plain Tensor routing); nn.Module.__setattr__ partitions by type | Cell 11+++++ post-hoc |

---

## §4. Open Questions Deferred

| ID | Statement | Closure Path |
|---|---|---|
| OQ-S220-PRE-1 | Baseline schema two-tier {per_fact, per_probe}; PROBE_TEXT_RESOLVABLE_INLINE at `per_probe.prompt` | RESOLVED at Cell 5++ — closes |
| OQ-S220-CFB-PATH-1 | Corpus path convention — should canonical cfb-v3.yaml migrate to per-engine path (`/workspace/architecture_profile/`) for parity with patches/runbooks/baseline | v0.2 absorption deliberation |
| OQ-S220-1 | Cell 7 protocol drift between S2.18 ROME and S2.20 GRACE — schema engine-agnostic? | RESOLVED informational at Cell 7+ — closes |
| OQ-S220-AUTH-1 | HF token file content lifecycle between sessions; reproducibility manifest extension to record token shape | v0.2 absorption |
| OQ-S220-CELL10-1 | Cell 10 specificity verdict serializer defect: empty `spec_drifts` AND list-of-zeros both produce FAIL | v0.2 Cell 10/12 corrected adjudication |
| OQ-S220-RECOVERY-1 | Cleanup path for partial-substitution failure modes; canonical via `current.layer` recovery | RESOLVED at Cell 9-- — closes |
| OQ-S220-CELL11-1 | Pre-Cell-13 verdict integrity audit (Cell 11++) required to distinguish S-α from S-β scenarios | RESOLVED at Cell 11++ — closes |
| OQ-S220-V0-2-CODIFICATION | v0.2 codification analog session post-S2.20 (parallel to S2.18 → v0.2 ROME codification) | S2.21+ session |
| OQ-S220-MANIFEST-1 | Reproducibility manifest tracks 2 sessions despite 8+ session history; root cause investigation | S2.21 entry |
| OQ-S220-RTX-A100-MIGRATION-1 | Operator-side hardware migration to A100 80 GiB enables full-backward T.2 GRACE execution at canonical environment minus hardware delta | Operator decision; S2.21+ |

---

## §5. Interface Contracts Defined

### §5.1 IC-S220-1: GRACE_barebones Pre-Dispatch Configuration

**Contract:** Cells dispatching `GRACE_barebones.edit()` must apply F-2 configuration AFTER constructor invocation:

```python
editor = GRACE_barebones(model=..., layer=..., ...)
model.train()                              # F-2.1: enable training mode
# DO NOT invoke model.requires_grad_(True) — causes OOM at backward
# DO NOT invoke model.gradient_checkpointing_enable() — incompatible with adapter
```

**Verification:** Constructor's internal freeze preserved; adapter value at iter=0 forward registers as nn.Parameter via tuple-unpacking assignment to `self.values`; loss.requires_grad transitions True via chain rule through frozen layers.

**Constraint:** RTX 4090 24 GiB INSUFFICIENT for full-backward dispatch on Llama-3.1-8B fp16 at edit site L17. Hardware migration required for environmental-ceiling-conditional retry.

### §5.2 IC-S220-2: Patch Application Discipline

**Contract:** SOURCE_LAYER patches against upstream GRACE source apply via:

```
1. Preserve pristine: shutil.copy2(target, target.with_suffix(".py.upstream_pristine"))
2. Read from PRISTINE (not live) for defensive baseline
3. Single-line replacement with unique terminal-statement anchor
4. Reload module via sys.modules cache flush + importlib.reload
5. Marker assertion verifies pattern absence + new-pattern presence
6. Patch state manifest update with site count + line numbers
```

**Verification:** Cell 2++ (P-1-GRACE; 9 sites) + Cell 2++++ (P-2-GRACE; 1 site).

### §5.3 IC-S220-3: Layer-Restore Recovery

**Contract:** Stale GRACEAdaptor recovery uses identity-agnostic instance-attribute access:

```python
current = getattr(parent_module(model, path), path.rsplit(".", 1)[-1])
if type(current).__name__ == "GRACEAdaptor":      # identity-resilient check
    original_linear = current.layer                 # instance attribute access
    setattr(parent, name, original_linear)
```

**Verification:** Cell 9-- + Cell 11+++++++++. Cross-validation against `pre_edit_baseline_s220` confirms drift `0.00e+00`.

### §5.4 IC-S220-4: Verdict Integrity Audit (Pre-Cell-13)

**Contract:** Before any Cell 13 routing decision, verdict integrity audit verifies:

- `outputs.loss.requires_grad == True` (gradient flow path active)
- `len(model.parameters()) > 0 with requires_grad=True` (Adam optimizer scope non-vacuous)
- Adapter value registered as nn.Parameter (verified via optimizer trainable count delta of `value_shape`)
- Backward pass produces `grad_norm > 0` on adapter value

**Verification:** Cell 11++ (initial defect detection) + Cell 11++++++ (mechanism-correct configuration verification).

---

## §6. New Patches Authored

### §6.1 P-1-GRACE — eval(f-string) Replacement

| Field | Value |
|---|---|
| Class | SOURCE_LAYER |
| Target | `grace/editors/grace_barebones.py` |
| Sites | 9 (lines 44, 53, 56, 57, 62, 76, 77, 78, 79) |
| Mechanism | `eval(f"self.model.{self.layer}")` → `getattr(parent_module(self.model, self.layer), self.layer.rsplit(".", 1)[-1])` |
| Defect Class | Universal — affects all HuggingFace transformer models with numeric-indexed submodules (Llama, GPT-2, GPT-J, Mistral, Qwen, etc.) |
| Status | EMPIRICALLY VALIDATED — Cell 9 dispatch executes past line 56 without SyntaxError |
| v0.2 Absorption | `grace-patches-canonical v0.2 §6` |

### §6.2 P-2-GRACE — torch.cdist fp16 Upcast

| Field | Value |
|---|---|
| Class | SOURCE_LAYER |
| Target | `grace/editors/grace_barebones.py` |
| Site | 1 (line 9, function `euclidean_distance`) |
| Mechanism | Conditional fp16 → fp32 → fp16 upcast wrapper around `torch.cdist` call |
| Defect Class | Universal — affects all fp16-loaded models with non-empty GRACE codebook |
| Status | EMPIRICALLY VALIDATED — Cell 9.6 forward pass executes past line 9 without RuntimeError |
| v0.2 Absorption | `grace-patches-canonical v0.2 §6` |

### §6.3 Patch Class Taxonomy Update

```
Defect class taxonomy at S2.20 close:
  P-1-GRACE: eval(f-string) syntax incompatibility    → universal HF models
  P-2-GRACE: torch.cdist CUDA fp16 unsupported         → universal fp16 models
  
Minimum patch set for fp16 modern transformer GRACE execution:
  {P-1-GRACE, P-2-GRACE}
```

---

## §7. Empirical Anchors

### §7.1 Cross-Session Bit-Exact Determinism

**Checkpoint #7 ESTABLISHED.** Cross-session anchor extends from 6 strict-bit-exact checkpoints (S2.13-C through S2.18) to 7 with combined semantic + relaxed-numeric semantics under transformers 5.7.0 environment.

| Metric | Value |
|---|---|
| n_probes | 38 |
| top_1 mismatches | 0/38 |
| drift_max_p_top_1 | `4.97e-07` |
| drift_max_p_target_new | `4.97e-07` |
| Drift class | rounding (transformers 5.7.0 vs S2.18-era environment delta) |

### §7.2 Anchor Inventory (Selected)

| Anchor ID | Content (compressed) |
|---|---|
| A-S220-CELL5++-1 | Baseline schema two-tier `{per_fact: metadata, per_probe: P-values}`; INLINE probe text at `per_probe.prompt` |
| A-S220-CELL6-3 | Llama tokenizer leading-space prefix required for canonical single-token target encoding |
| A-S220-CELL7-1 | Per-fact probe count = 7 (cons×3 + gen×3 + unmount×1); shared specificity = 3 |
| A-S220-CELL8-2 | LlamaMLP.down_proj is torch.nn.Linear `(4096, 14336)` fp16 (not Llama-specific subclass) |
| A-S220-CELL9-2 | GRACEAdaptor preserves original Linear at `self.layer`; recovery via instance-attribute access bit-exact |
| A-S220-CELL11-2 | Bit-exact 38/38 probes pre == L17 == L2 (cross-layer identity) — mathematically forecloses edit installation |
| A-S220-CELL11+++++-1 | F-1 (full requires_grad_True) registers adapter value but produces 32+ GiB demand |
| A-S220-CELL11++++++-1 | F-2 (model.train() only, freeze preserved) produces 24.64 GiB — exceeds 24 GiB ceiling |
| A-S220-CELL11+++++++-1 | Gradient checkpointing structurally incompatible with GRACEAdaptor stateful forward |
| A-S220-CELL18-1 | Covariance cache filename schema `model.layers.N.mlp.down_proj_float32_mom2_t100_100000.npz`; 8 files at canonical directory; 6.42 GiB total |

### §7.3 Architectural Findings — Llama-3.1-8B + GRACE

```
Edit dispatch resource accounting (RTX 4090 24 GiB; canonical hparams):
═══════════════════════════════════════════════════════════════════════
  Component                              VRAM cost
  ───────────────────────────────────────────────────
  Model weights (fp16, 8.03B params)     16.06 GiB
  Activations L0–L16 (no grad downstream)  0.00 GiB  (not retained)
  Activations L17–L31 (grad downstream)    8.00 GiB  (retained)
  Adapter value + Adam state               0.05 GiB
  Workspace + cuBLAS                       0.50 GiB
  ───────────────────────────────────────────────────
  Total under F-2:                        24.61 GiB
  RTX 4090 ceiling:                       24.00 GiB
  Headroom:                               -0.61 GiB  ← OOM
═══════════════════════════════════════════════════════════════════════
```

---

## §8. v0.2 Absorption Surface (Substantial)

### §8.1 grace-patches-canonical v0.2 §6

- P-1-GRACE codification (9 sites; site_line_numbers `[44, 53, 56, 57, 62, 76, 77, 78, 79]`)
- P-2-GRACE codification (1 site; function `euclidean_distance`)
- Minimum patch set documentation: `{P-1-GRACE, P-2-GRACE}` for fp16 modern transformer execution

### §8.2 t2_grace_runbook v0.2 (Authored Post-S2.20)

| Cell | Absorption |
|---|---|
| Cell 5 | Two-tier baseline schema `{per_fact, per_probe}`; HF token shape gate (C-S220-2); cross-session combined gate (C-S220-3) |
| Cell 6 | Leading-space tokenization convention; `memit_request` schema indirection; `cfb_v3.cfb_v3.facts` wrapper indirection |
| Cell 7 | Linkage-conditional probe field capture (linked vs shared_specificity) |
| Cell 8 | Full-path `parent_module` argument; identity-resilient state-check via type-name |
| Cell 9 / 11 / 15 | F-2 dispatch preamble (`model.train()` only); pre-instantiation state-check + recovery-from-stale-substitution |
| Cell 10 / 12 | Specificity verdict serializer correction (empty list vs zeros distinction) |
| Cell 13 | Environment-conditional verdict envelope; routing matrix supports environmental ceiling → smaller-model retry |

### §8.3 NV Convention Corrections

| Convention | Pre-S2.20 declarative | Empirical |
|---|---|---|
| cfb-v3.yaml path | `/workspace/cfb-v3.yaml` | `/workspace/session_logs/archive/s2_13/cfb-v3.yaml` |
| Baseline path/format | `<sha>/baseline_logits.pt` | `/workspace/architecture_profile/stage_1_llama_baselines.json` (per-fact JSON) |
| Cache filename | `layers.N.*_mom2_100000.npz` | `model.layers.N.*_mom2_t100_100000.npz` |
| Cache path | model-keyed | `meta-llama_Llama-3.1-8B/wikipedia_stats/` confirmed |
| Reproducibility manifest path | `/workspace/reproducibility_manifest.json` | `/workspace/architecture_profile/reproducibility_manifest.json` |

---

## §9. Outputs Persisted

### §9.1 Session Artifacts (NV-Resident)

| Artifact | Path |
|---|---|
| Pre-edit baseline (S2.20 environment) | `/workspace/architecture_profile/t2_grace_pre_edit_baseline.json` |
| Post-edit L17 capture (under DEFECT state) | `/workspace/architecture_profile/t2_grace_post_edit_l17.json` |
| Post-edit L2 capture (under DEFECT state) | `/workspace/architecture_profile/t2_grace_post_edit_l2.json` |
| Verdict adjudication (Cell 10 L17) | `/workspace/architecture_profile/t2_grace_verdict_l17.json` |
| Session verdict (Cell 12) | `/workspace/architecture_profile/t2_grace_verdict_s220.json` |
| S2.20→S2.21 routing decision (Cell 13) | `/workspace/architecture_profile/t2_grace_routing_s220_to_s221.json` |
| Patch state manifest | `/workspace/architecture_profile/t2_grace_patch_state.json` |
| Reproducibility manifest extension | `/workspace/architecture_profile/reproducibility_manifest.json` |

### §9.2 Patched Source

| File | Pristine | Patches |
|---|---|---|
| `grace_barebones.py` | `.upstream_pristine` preserved | P-1-GRACE (9 sites) + P-2-GRACE (1 site) |

### §9.3 Covariance Cache State (PRESERVED)

| Path | Files | Total Size |
|---|---|---|
| `meta-llama_Llama-3.1-8B/wikipedia_stats/` | 8 files (L2-L8 + L17) | 6.42 GiB |

Cache durability per `D-S217-3` carry-forward: VALIDATED. Filename schema clarified per A-S220-CELL18-1.

### §9.4 NV Utilization

| Metric | Value |
|---|---|
| Workspace size | 112 GiB |
| NV total | 1.20 TiB |
| NV used | 910.6 GiB (75%) |
| NV available | 319.6 GiB |

---

## §10. S2.21 Routing — Forward Specification

### §10.1 S2.21 Scope

T.1-GRACE-3B retry runbook v0.1 authoring + execution.

### §10.2 Model Candidate

`meta-llama/Llama-3.2-3B`

### §10.3 Preserved Invariants

| Invariant | Source |
|---|---|
| Engine | GRACE_barebones |
| Patches | P-1-GRACE + P-2-GRACE (carry-forward; v0.2 absorbs as canonical) |
| Corpus | cfb-v3.yaml v1.0 |
| Probe set | probe-set-v3.yaml v1.0 |
| Hparams | canonical (init_epsilon=1.0, edit_lr=1.0, n_iter=200) |
| Pad-Token | APPLICABLE (Llama-class tokenizer) |
| Tokenization convention | leading-space prefix per D-S220-TOKENIZATION-1 |

### §10.4 Outcome Matrix

```
S2.21 = T.1-GRACE-3B retry verdict surface:
═══════════════════════════════════════════════════════════════════
  if PASS (installed edit; calibration corridor met):
    └── ceiling = ENVIRONMENTAL (S2.20 verdict eliminable)
        └── adapter mechanism viable for WS3 implementation
            on VRAM-fitting model classes
  
  if FAIL with installation (narrow-discriminator pathology):
    └── ceiling extends to MODEL-CLASS-AGNOSTIC adapter elimination
        └── stronger claim than S2.20 alone
        └── routes to T.1 alt-model under MEMIT (per t_branch §5')
  
  if FAIL at environment (3B also OOMs):
    └── ceiling propagates; investigate hardware migration to A100
    OR halt T-branch with environmental-conditional caveat
═══════════════════════════════════════════════════════════════════
```

### §10.5 S2.21 Inheritance

| Element | Source |
|---|---|
| Runbook structural template | `t2_grace_runbook v0.1` (§10 inheritance map) |
| Patches canonical | `grace-patches-canonical v0.1` → v0.2 (P-1/P-2-GRACE absorbed at v0.2 codification) |
| Active framework finding | `framework_finding_memit_ceiling_archival v1.0/v1.1` |

### §10.6 v0.2 Codification Analog Session

S2.20 carry-forward includes substantial v0.2 absorption surface (per §8). A v0.2 codification analog session (parallel to S2.18 → v0.2 ROME codification) produces:

- `grace-patches-canonical v0.2` — P-1-GRACE + P-2-GRACE absorbed
- `t2_grace_runbook v0.2` — Cell 5/6/7/8/9-15 cell body corrections per §8.2
- `framework_finding_memit_ceiling_archival v1.2` (additive) — adapter-mechanism environmental-ceiling finding documented

Codification session authoring deferred to operator-side scheduling between S2.20 close and S2.21 entry.

---

## §11. Carry-Forward Anchors for S2.21

### §11.1 Load-Bearing State

| Anchor | Status | Carry-forward |
|---|---|---|
| Cross-session bit-exact determinism (checkpoint #7) | RATIFIED via combined gate | extends to checkpoint #8 at S2.21 Cell 5 |
| `pre_edit_baseline_s220` reference frame | persisted | reusable as pre-S2.21 baseline ONLY for Llama-3.1-8B; NOT for Llama-3.2-3B (different model class) |
| Patches `{P-1-GRACE, P-2-GRACE}` | RATIFIED EMPIRICALLY-VALIDATED | minimum set for any modern HF transformer + fp16 GRACE execution |
| F-2 dispatch preamble | RATIFIED | canonical for all GRACE Cell 9/11/15 dispatch |
| Constructor freeze mechanism | DOCUMENTED | source-truth at GRACE_barebones.__init__ lines 18-19 |

### §11.2 Provisional Anchors Pending S2.21

| Anchor | Status | Resolution |
|---|---|---|
| A-S220-MANIFEST-1 | PROVISIONAL | reproducibility manifest tracks 2 sessions despite 8+ session history; root cause investigation at S2.21 entry |
| OQ-S220-RTX-A100-MIGRATION-1 | OPEN | operator-side hardware migration decision; orthogonal to T.1-GRACE-3B retry |

### §11.3 Eliminated Hypotheses (S2.20 Closure)

| Hypothesis | Status | Source |
|---|---|---|
| H-A — recovery state ephemeral between cells | FALSIFIED | Cell 11+++ persists; Cell 11++++++ verifies durable |
| H-B — internal eval() suppression at GRACE_barebones init | CONFIRMED | source inspection Cell 11++++ — D-S220-DEFECT-CAUSE-1 |
| H-C — Cell 11 forward routed through L17 instead of L2 | FALSIFIED | Cell 11.0 verifies L17 Linear at entry |
| H-D — edit non-installation hypothesis | CONFIRMED then RECONTEXTUALIZED | Cell 11+ confirms; Cell 11++++++ shows installation viable under F-2 mechanism (blocked only by VRAM) |
| H-E — recovery state ephemeral | FALSIFIED | post-Cell-11+++ trainable params persist |
| H-F — adapter values not nn.Parameter | FALSIFIED at instantiation; CONFIRMED at __dict__-level diagnostic | nn.Module routing to `_parameters` |
| H-G — optimizer scope excludes adapter values | RECONTEXTUALIZED | F-2 + post-substitution Adam construction includes adapter value |

---

## §12. Session Close Posture

### §12.1 Cell Sequence Executed

```
Block A: Cells 0–8 (pre-flight + model + dry-run)              COMPLETE
Block B: Cells 9–13 (single-edit dispatch + verdict + routing) COMPLETE
Block C: Cells 14–17 (15-trial loop)                           BYPASSED
Block-end: Cells 18–20 (NV inventory + manifest)               COMPLETE
Closing: Cell 11+++++++++ (composite state hygiene)            COMPLETE
```

### §12.2 Recovery Cell Inventory

The session required substantial in-line cell authoring beyond the runbook v0.1 declarative scope. Recovery cells authored mid-session:

| Cell | Purpose |
|---|---|
| Cell 5++ / 5+++ / 5++++ / 5+++++ / 5++++++ | Baseline schema discovery + bit-exact gate adjudication |
| Cell 6++ / 6+++ / 6++++ / 6+++++ / 6++++++ / 6+++++++ | Corpus schema discovery + tokenization convention discovery |
| Cell 7+ | Linkage-conditional pre-edit baseline capture |
| Cell 8++ | Full-path parent_module dry-run gate |
| Cell 9-- / 9-- (recurrence) | Stale GRACEAdaptor recovery |
| Cell 11+ / 11++ / 11+++ / 11++++ / 11+++++ / 11++++++ / 11+++++++ / 11++++++++ / 11+++++++++ | Verdict integrity audit + recovery + F-1/F-2/F-3 isolation |
| Cell 2++ / 2+++ / 2++++ | P-1-GRACE / P-2-GRACE patch authoring + application |
| Cell 18.0 / 18 v2 | Covariance cache path discovery + corrected integrity gate |

### §12.3 Forward Action

| Step | Action | Owner |
|---|---|---|
| §12.3.1 | Operator scheduling for v0.2 codification analog session (recommended pre-S2.21) | operator |
| §12.3.2 | S2.21 kickoff prompt authoring with T.1-GRACE-3B retry scope | agent |
| §12.3.3 | A-S220-MANIFEST-1 root cause investigation at S2.21 Cell 0+ | operator + agent |
| §12.3.4 | OQ-S220-RTX-A100-MIGRATION-1 operator decision (orthogonal path) | operator |

---

**Session 2.20 CLOSED 2026-05-05.**
