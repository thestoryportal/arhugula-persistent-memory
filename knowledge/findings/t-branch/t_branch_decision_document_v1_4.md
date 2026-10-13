# T-Branch Decision Document — T.3-β-QWEN EXECUTED; Ceiling NARROWED G→Llama-lineage; Architecture-Geometry Frontier RE-OPENED (v1.4 amendment of v1.3 of v1.2 of v1.1 of v1.0)

> **Status:** RATIFIED v1.4 — load-bearing; additive amendment; v1.0 + v1.1 + v1.2 + v1.3 PERMANENT integrity preserved (decision-record class)
>
> **Predecessor (v1.4):** S2.31 — T.3-β-QWEN executed (cross-architecture MEMIT; Qwen2.5-7B CLEARED 5/5)
> **Successor (v1.4):** S2.32 — architecture-geometry frontier (re-opened); CLEAR-hardening recommended
> **Workstream:** WS1 (empirical execution; T.2 ROME closed; T.2 GRACE hparam-conditional; T.1 cross-scale RESOLVED; T.3 cross-architecture EXECUTED — **Mistral confirms within-lineage; Qwen FALSIFIES generality → ceiling narrows to Llama-lineage**)

---

## §0'''' — v1.4 amendment scope and integrity declaration

### §0''''.1 v1.4 amendment scope

v1.4 records the empirical disposition of the v1.3 forward-conditional decision and surfaces deltas at the corresponding `''''`-suffixed section numbers:

1. **§1'''' decision statement updated** for the post-S2.31 state: the v1.3 §1''' "new live frontier: confirmation, not class-change — the only forward move that could still *narrow* G is a non-Llama-lineage family clearing the band; the Qwen-7B arm tests exactly that" is RESOLVED. **T.3-β-QWEN executed at S2.31; Qwen CLEARED 5/5; G is FALSIFIED as stated; the ceiling NARROWS from G (base-decoder-LM-general) to Llama-lineage.** The pre-registered falsifier fired.
2. **§4'''' candidate-axis selection updated**: the cross-architecture frontier, which v1.3 treated as "confirmed once, one routed confirmation pending," is RE-OPENED in a new direction — not "more confirmations of G" (G is dead) but "where is the lineage boundary, and why." New candidate axes surfaced.
3. **§5'''' conditional execution plan resolved**: the v1.3 §5''' Qwen arm was executed; the CLEAR routes (per the S2.30 §10 decision matrix) to the **within-regime / architecture-geometry probe RE-ACTIVATED** branch — exactly the branch the matrix reserved for a CLEAR.
4. **§6'''' methodology lock amended**: a new in-session confound-isolation discipline (patch-isolation control) is added to the locked methodology, triggered by S2.31's CPU-solve patch.
5. **§8'''' open questions** — closes OQ-V13-T-BRANCH-1..3 + the Qwen-arm OQs per S2.31 dispositions; resolves OQ-S231-PATCH-CONFOUND-1; opens the lineage-boundary and internal-mechanism OQs.

The v1.4 amendment **preserves all v1.0 §1–§11, v1.1 §1'–§11', v1.2 §0''–§8'', and v1.3 §0'''–§8''' content verbatim** as load-bearing PERMANENT decision-record. v1.4 surfaces deltas at corresponding section numbers with the suffix `''''`.

### §0''''.2 v1.0 + v1.1 + v1.2 + v1.3 integrity preservation

v1.0–v1.3 are preserved verbatim. v1.4 is additive-only. **No prior decision is retracted** — Mistral still confirms the ceiling, the Llamas still hit it, ROME still hits it. What changes is the *scope of the generalization claim* (G → Llama-lineage), not any underlying decision.

---

## §1'''' — Decision statement amendment (extends v1.0 §1, v1.1 §1', v1.2 §1'', v1.3 §1''')

The v1.3 §1''' frontier statement read: *"New live frontier: confirmation, not class-change. The only forward move that could still narrow G is a non-Llama-lineage family clearing the band; the Qwen-7B arm tests exactly that."* v1.4 resolves it:

> **T.3-β executed (S2.31). Qwen2.5-7B CLEARED. G falsified. Ceiling narrows L_lineage.** MEMIT at canonical hparams on `Qwen/Qwen2.5-7B` (base) — single-variable architecture port, **one integer different** from the proven Mistral config (`v_loss_layer 31→27`), zero tuning-knob changes — produced **5/5 consistency PASS** (P_min 0.990). Qwen is the first model in the program to break the ceiling. The internal-vs-external signature is absent: z-optimization converges (>0.98 all 5) AND the external surface follows (0.99 all 5).
>
> **The finding's strongest form is now:** a config-independent **MEMIT-class (rank-1-in-weight) ceiling on Llama-lineage base decoder LMs at canonical hparams** — confirmed on {Llama-3.1-8B (7 axes), Llama-3.2-3B, Mistral-7B-v0.3}, with ROME a confirmed second engine in the class — that does **NOT** extend to Qwen2.5-7B. The ceiling is lineage-bounded, not base-decoder-LM-universal.
>
> **The CLEAR was confound-checked.** The one in-session engine modification (`P-VRAM-CPU-SOLVE`, VRAM-forced) was isolated on the Llama-3.1-8B ceiling (held at floor `7.9e-08`, provably equivalent to the pristine GPU solve `1.07e-05`) and exonerated. The CLEAR is real.
>
> **New live frontier: the architecture-geometry question, RE-OPENED.** The seven-axis work had closed "why does the ceiling exist" as "it's a robust property of the regime." The Qwen falsification reopens it as a *localizable* question: what Llama-lineage geometric property obstructs the z-optimization (the divergence is at the internal stage — finding v1.5 §3), and how far does the lineage boundary extend?

---

## §4'''' — Candidate-axis selection amendment (extends v1.3 §4''')

The within-Llama config space remains exhausted; v1.3's "cross-architecture frontier = one confirmed + one routed confirmation" is superseded. The CLEAR opens a new axis class. Candidate forward axes, in Claude-recommended priority:

| Priority | Axis | What it adjudicates | Cost |
|---|---|---|---|
| 1 | **Qwen CLEAR-hardening** — full 38-probe panel (gen + spec + unmount) × 15 trials | Is the CLEAR finding-grade (generalizes + stays local + unmounts clean across trials), or a single-prompt artifact? | Low (~1 session; caches resident) |
| 2 | **Llama-vs-Qwen internal-stage geometry probe** — per-layer z-convergence at matched layers | WHERE the lineage divergence originates in the optimization (finding v1.5 §3 / D-S231-MECH-1) | Low–med |
| 3 | **Second non-Llama-lineage family** (Phi / Gemma / NeoX-class) clear-or-hold | Is the boundary "Llama-2 lineage" precisely, or narrower? Determines the true class boundary | Med (new cov compute + port) |
| 4 | **Mistral re-confirm under `P-VRAM-CPU-SOLVE`** | Closes the last patch-confound thread for the Llama-lineage-holds side (Mistral was run pre-patch) | Very low |

**Recommendation:** S2.32 = **Axis 1 (Qwen full-panel + replicate)** with **Axis 4 (Mistral CPU-solve re-confirm)** folded in as a same-session control — both run through the now-canonical patched engine, yielding a clean within-engine "Llama-lineage holds / Qwen clears" contrast and hardening the CLEAR to finding-grade in one session. Axes 2–3 are the deeper mechanistic follow-ons.

---

## §5'''' — Conditional execution plan (resolved; CLEAR branch taken)

The S2.30 §10 decision matrix specified three branches. **The CLEAR branch is taken:**

- ~~`0/5` + signature → G near-decisive → external-validity frontier~~ — NOT taken (Qwen did not reproduce).
- **CLEAR (≥3/5) → G narrows to Llama-lineage → within-regime per-layer sweep / architecture-geometry RE-ACTIVATED** — **TAKEN.** 5/5, decisive CLEAR.
- ~~OOM → triage~~ — encountered and resolved (CPU-solve); not the terminal state.

Forward execution per §4'''': S2.32 hardens the CLEAR (Axis 1 + 4); architecture-geometry (Axis 2/3) follows.

---

## §6'''' — Methodology lock amendment (extends v1.3 §6''')

The cross-architecture single-variable port discipline (locked v1.2 §6''/v1.3 §6''') carries forward. v1.4 ADDS:

> **In-session confound-isolation discipline (C-S231-2).** When an arm requires an in-session modification to the science-bearing engine path (e.g. a VRAM-forced solve change), the verdict MUST NOT be promoted until the modification is isolated against a known result — run the same modified engine on a known-ceiling Llama config and confirm the known result reproduces. If it does, the modification is exonerated and the new verdict stands; if it does not, the verdict is an artifact. (Established S2.31: `P-VRAM-CPU-SOLVE` isolated on Llama-3.1-8B before promoting the Qwen CLEAR.)

> **CPU-solve as a standing requirement (C-S231-1).** Any model whose intermediate width inflates the MEMIT float64 solve past 4090 headroom (≥ ~18k) requires `P-VRAM-CPU-SOLVE` (or equivalent solve-offload). Single-layer scope reduction does NOT substitute (the allocation is per-layer). Go straight to CPU-solve for wide models.

---

## §8'''' — Open questions (extends v1.3 §8''')

**Closed at S2.31:**
- OQ-V13-T-BRANCH-1/2 (Qwen revision/structure) — resolved at Cell 1/1.5.
- OQ-V13-T-BRANCH-3 (does the signature reproduce on a non-Llama-lineage family) — **resolved: NO, Qwen clears.** This is the falsifier.
- OQ-S231-PATCH-CONFOUND-1 — resolved: patch exonerated (§4 / finding v1.5 §4).
- OQ-S230-QWEN-FRAG-1 — resolved: 4/5 STRICT, cleaner than Mistral.
- OQ-S230-QWEN-TOP1-1 — resolved: natural top-1 ` the` (function-word class, same as Llama/Mistral).

**Opened at S2.31:**
- OQ-S231-LINEAGE-BOUNDARY-1: is the ceiling boundary precisely "Llama-2 lineage," or a narrower architectural property Qwen differs on? Requires a second non-Llama-lineage family (Axis 3).
- OQ-S231-INTERNAL-GEOMETRY-1: what Llama-lineage geometric property obstructs the z-optimization convergence that Qwen's geometry does not? (D-S231-MECH-1; Axis 2.)
- OQ-S231-CLEAR-ROBUSTNESS-1: is the Qwen CLEAR finding-grade across the full 38-probe panel × 15 trials, or canonical-prompt-only? (Axis 1; S2.32.)

**Carried:**
- OQ-S225-BASE-INSTRUCT-1 (Instruct-vs-base) — open; now a within-Qwen-lineage external-validity question.
- OQ-S222-CALIBRATION-CRITERIA-MISMATCH-1 — reconcile runbook vs probe-set §126 predicate; relevant to the CLEAR-hardening full-panel read (Axis 1).

---

**v1.4 RATIFIED S2.31 close 2026-06-15.** ADDITIVE; v1.0–v1.3 PERMANENT preserved verbatim. T.3-β-QWEN executed; Qwen CLEARED 5/5; G falsified; ceiling narrows to Llama-lineage; pre-registered falsifier (v1.3 §1''') fired; CPU-solve confound isolated/exonerated; architecture-geometry frontier re-opened; S2.32 routed to CLEAR-hardening (Axis 1 + 4).
