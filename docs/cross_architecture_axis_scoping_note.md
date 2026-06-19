# Cross-Architecture-Axis Scoping Note — T.3 (Mistral-7B / Qwen-7B) vs Within-Regime Deeper Arms

> **Artifact type:** Scoping / routing note (S2.28 deliverable #3; companion to framework_finding v1.3 §6 and t_branch v1.2 §4''/§7'')
> **Authored:** 2026-06-15 (S2.28 authoring session)
> **Specialist provenance:** memit-specialist (primary); orchestration-comparativist (cross-architecture comparison surface); framework-spec-writer (formalization)
> **Status:** RECOMMENDATION SURFACED FOR OPERATOR RATIFICATION at S2.28 close
> **Decision owner:** operator (Robert) — per standing directive, Claude makes the call and surfaces it; operator retains ratification authority over the WS1-scope boundary specifically (a scope-boundary change is the one class of decision that is genuinely the operator's, since it expands the workstream's committed compute)

---

## 1. The question

The nine-axis ceiling (framework_finding v1.3) has closed the within-Llama config space's high-value escape hatches. Two forward families remain, and they differ in *kind*, not just cost:

- **T.3 — cross-architecture.** MEMIT on a non-Llama base model (Mistral-7B, then Qwen-7B). A **new hypothesis-class** axis.
- **Within-regime deeper arms.** Per-layer sweep + sequential-vs-joint dispatch on Llama. **Same-class** 10th/11th axes within the already-confirmed regime.

T.3 has been flagged out-of-scope WS1 since v1.1. This note asks whether the 9-axis result warrants re-scoping it in, and recommends the answer.

---

## 2. What each path can and cannot tell us

### 2.1 The current strongest claim, and its one remaining boundary

At v1.3 the ceiling is: **a config-independent MEMIT-on-base-Llama property, validated across 9 axes spanning scale (8B→3B), write-engine (MEMIT/ROME), and the two contested layer bands ([2–6]/[4–8]), with the AKD and band confounds eliminated.**

The claim has exactly one class-boundary it has not crossed: **architecture.** Every axis to date varied something *inside* the Llama-family / MEMIT-mechanism box. The open question is whether the ceiling is:

- **(L) Llama-family-specific** — something about base Llama's representation geometry resists MEMIT consistency-editing; OR
- **(G) base-decoder-LM-general** — MEMIT-class in-weight editing fails to produce consistency on base (non-instruct) autoregressive decoder LMs at canonical hparams, of which Llama is one instance.

These are very different findings for the "LLM-as-database" thesis. (L) localizes the problem and leaves open that a different base model is editable. (G) is a much stronger, more portable, more publishable result about the write layer of the framework.

### 2.2 Path-by-path information yield

| Path | What a `0/5` result establishes | What a CLEAR result establishes | Class |
|---|---|---|---|
| **T.3 Mistral-7B** | Ceiling is NOT Llama-specific → supports (G); strongest single result available | Ceiling IS Llama-family-specific → (L); re-activates within-regime arms to find "what's different" | **NEW class** — resolves the L-vs-G boundary |
| **T.3 Qwen-7B** | Confirms (G) across a second non-Llama family → near-decisive for (G) | Distinguishes which architectures resist (partial G) | NEW class (confirmation arm) |
| Per-layer sweep (Llama) | Optimal band also fails → confirms band-non-load-bearing (already strongly implied by Axis 9) | Some band CLEARS → Axis 9 was incomplete; major reframe (low prior) | SAME class (10th axis) |
| Sequential-vs-joint (Llama) | Sequential also fails → joint-batch not the cause (already implied by per-fact signature) | Sequential CLEARS → batch-interference was the cause (low prior, contradicts the per-fact internal-vs-external signature) | SAME class (11th axis) |

The asymmetry is stark: **T.3 is the only path whose most-likely outcome (`0/5`) still produces a high-information, class-changing result.** The within-regime arms' most-likely outcome (`0/5`) produces near-zero marginal information, because Axis 9 and the per-fact signature already imply those outcomes.

---

## 3. Cost / value tradeoff

### 3.1 Cost

| Path | Sessions | New compute | Reused scaffold | Net new lift |
|---|---|---|---|---|
| T.3 Mistral-7B | ~1–2 (1 authoring/port + 1 execution, possibly folded) | fresh model pull + license accept; fresh cov caches (~45 min at the reference band); determinism chain bootstrap | corpus, probe set (token-ID re-resolve), trial protocol, acceptance bands, runbook structure, scale-variant config idiom | architecture-port adaptations (module paths, n_layers, tie check) |
| T.3 Qwen-7B | ~1 | fresh model pull + caches | the entire T.3 Mistral scaffold | minimal — second arm rides the first |
| Per-layer sweep | ~1–2 | per-layer cov caches across the sweep range; multiple dispatches | corpus, probes, engine, 3B model | sweep harness |
| Sequential-vs-joint | ~1 | sequential dispatch loop | corpus, probes, engine, caches | dispatch-mode toggle |

T.3 Mistral is a **~1–2 session lift** — comparable to the 3B arc, which the workstream has already proven it can execute cleanly (stand up a fresh model, derive structural adaptations, run a single-variable dispatch). The scale-variant config idiom (framework_finding v1.3 §2.4) generalizes from Llama-class to cross-architecture: load the engine's reference MEMIT JSON for the target, override the architecture-structural fields (`layers`, `v_loss_layer = n_layers−1`, `lm_head_module` per `tie_word_embeddings`, the `*_module_tmp` path templates), recompute caches. VRAM fits the RTX 4090 with headroom at 7B fp16.

### 3.2 Value

| Path | Marginal information (expected) | Value to "LLM-as-database" thesis |
|---|---|---|
| **T.3 Mistral-7B** | **HIGH** — resolves L-vs-G, the only open class-boundary | HIGH — (G) is the portable, framework-level result about the write layer; (L) re-opens the search for an editable base model |
| T.3 Qwen-7B | HIGH (conditional on Mistral) — near-decides (G) | HIGH |
| Per-layer sweep | LOW — confirms Axis 9 | LOW — same-class confirmation |
| Sequential-vs-joint | LOW — confirms per-fact signature | LOW — same-class confirmation |

### 3.3 The interpretive-cost shift (why now and not at v1.1)

T.3 was reasonably out-of-scope at v1.1. At that point the ceiling was not yet config-robust: a T.3 failure could have been dismissed as a Llama-config artifact dragged onto a new model ("you didn't tune the band / you used a degenerate corpus / it's just the 8B"). **Axis 8 (scale), the AKD elimination, and Axis 9 (band) remove every one of those objections.** A T.3 result is now cleanly interpretable: the corpus is confirmed high-AKD, the band is confirmed non-load-bearing, the result is confirmed scale-robust. The 9-axis result does not lower T.3's *compute* cost, but it sharply lowers its *interpretive* cost — which is what made T.3 not-worth-it before and makes it worth-it now.

---

## 4. Recommendation

**Re-scope T.3 into WS1. Run Mistral-7B MEMIT (cfb-v3, canonical, reference band) as the next session; hold Qwen-7B as the immediate confirmation arm; keep the within-regime deeper arms DEPRIORITIZED (conditionally re-activated only by a surprising T.3 CLEAR).**

Rationale, in one line each:

1. **It is the only remaining axis that can change the class of the finding** — every within-regime arm is same-class confirmation with low marginal information.
2. **The 9-axis result makes it interpretively clean** — the config-non-robustness objection that justified its prior out-of-scope flag is now removed.
3. **It is tractable and cheap relative to its information** — ~1–2 sessions, the 3B arc proved the port pattern, the config idiom generalizes, VRAM fits.
4. **It is the highest-value move for the framework thesis** — (G) is the portable write-layer result; (L) is the signal to go find an editable base model. Either outcome is decision-relevant for Workstream 2/3 in a way the within-regime arms are not.

### 4.1 What re-scoping in concretely means

| Item | Disposition |
|---|---|
| WS1 scope boundary | EXTEND to include T.3 cross-architecture (Mistral-7B + Qwen-7B arms). The v1.1 "T.3 out-of-scope WS1" flag is superseded by this re-scope, ratified at S2.28 close. |
| Next session (S2.29) | T.3 Mistral-7B MEMIT — runbook authoring + execution (likely foldable into one session given the proven 3B port pattern) |
| Entry artifacts | framework_finding v1.3 + t_branch v1.2 + cfb-v3 + probe-set-v3 + memit-patches v2.5 + the 3B-MEMIT runbook (structural template) + EasyEdit Mistral reference config |
| Method | single-variable architecture port; reference band (no re-sweep per Axis 9); Cell P1 AKD pre-flight on the new edit layer; internal-vs-external signature as the primary read; single confirmatory dispatch (Route-A discipline) |

### 4.2 What it does NOT mean

- It does **not** eliminate the within-regime arms — they are DEPRIORITIZED and conditionally re-activated by a T.3 CLEAR (which would make "what's different between Llama and Mistral" immediately relevant).
- It does **not** commit to the orthogonal arms (KnowEdit external-validity, base-vs-instruct) — those remain deferred; they are orthogonal confound/validity arms, not class-changing, and can slot in after the T.3 result.
- It does **not** pre-judge the T.3 verdict — the recommendation commits to T.3-as-next-axis, not to its outcome.

---

## 5. The decision the operator owns

Per the standing directive, Claude makes routing calls and proceeds. This one carries an explicit asterisk: **re-scoping T.3 into WS1 changes the workstream's scope boundary**, which expands committed compute beyond the original WS1 envelope. That is the one decision class genuinely reserved to the operator. The recommendation is to re-scope in; the default-accepted call is Mistral-7B at S2.29.

**Alternatives the operator may legitimately prefer, each consistent with v1.3 / v1.2:**

| Alternative | When it makes sense | Cost of choosing it |
|---|---|---|
| **A. Re-scope T.3 in (RECOMMENDED)** | The L-vs-G boundary is the highest-value open question; framework thesis needs the portable result | ~1–2 sessions; scope extension |
| B. Run an orthogonal arm first (base-vs-instruct) | base-vs-instruct is a long-open confound (since S2.5a) and is cheap (~1 session, same model) | delays the class-changing result; base-instruct is still same-architecture |
| C. Run an orthogonal arm first (KnowEdit external-validity) | external reviewers will ask "does it hold on a standard benchmark corpus" | delays class-changing result; orthogonal not class-changing |
| D. Close WS1 at the 9-axis result; defer all further axes | the config-independent MEMIT-on-base-Llama ceiling is a defensible stopping point; move to WS2/WS3 | leaves L-vs-G unresolved; framework write-layer claim stays Llama-bounded |
| E. Run a within-regime deeper arm | only if there is residual doubt the band/dispatch arms are truly low-information | low marginal information per §2.2 |

**Claude's call: A (re-scope T.3 in; Mistral-7B at S2.29).** Surfaced for the record; operator ratifies the scope-boundary change at S2.28 close. If the operator prefers D (close WS1 here), that is a clean and defensible stopping point and nothing in v1.3 / v1.2 depends on T.3 running — the nine-axis finding stands on its own.

---

*End of cross-architecture-axis scoping note — recommends re-scoping T.3 (Mistral-7B first, Qwen-7B confirmation) into WS1 as the next hypothesis-class axis; within-regime deeper arms deprioritized; operator ratifies the WS1 scope-boundary change at S2.28 close.*
