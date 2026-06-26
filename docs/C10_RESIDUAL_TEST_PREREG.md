# C10 RESIDUAL-TEST (Option B) — PRE-REGISTRATION

**Decision-ID:** D-C10b-residual (CORPUS pending) · **Class:** FALSIFIER-sizing (can-fail; characterization, NOT promotable without advisor + cross-family)
**Date:** 2026-06-26 · **Target:** `local Intel CPU + batch writes` (operator-fixed 2026-06-26)
**Parent:** D-C10-1 (CORPUS/35) — multi-token VALUE falsifier FIRED, severity-BOUNDED.
**Scope:** Qwen2.5-3B / band[4-8] / AlphaEdit (in-solve null-space) / single-batch / capital-relation / NOVEL-insert / N≤24 / 1-seed / HF-fp16.

---

## 0. The question this sizes (operator chose Option B)

C10 fired because **arbitrary INCOHERENT multi-token values** ("Amsterdam Ankara" = two unrelated real single-tokens) generalize to held-out paraphrases at only **36%** (vs single-token 97% and prior-COHERENT multi-token "Cape Town" 97%). The edit FITS the trained prompt but does not GENERALIZE — the continuation position collapses (conditional P(full|first)=0.51 vs 1.00).

**Severity bound (D-C10-1, advisor-corrected):** §7.1/D1 routes the SYNTACTIC value subset (file paths / identifiers / exact strings) to **Git**, not in-weight. The in-weight residual = **project-coined multi-word SEMANTIC named entities** (§7.2 `domain_concept`) with no pretrained prior — the value class an actual project KB holds (e.g. a coined subsystem/place/artifact name). C10's "incoherent" arm is a deliberately worst-case proxy. 

**Binding question:** do REALISTIC project-coined multi-word semantic values behave like the fragile incoherent floor (~36% → C10 bites the real KB) or like the robust arms (~97% → C10 is largely an artifact of contrived two-unrelated-word values)? **Where on the [36%, 97%] interval does the real class land, and what governs it?**

This is a SIZING test, not a new falsifier: it tells us how much of the real in-weight value surface the C10 wall actually covers.

---

## 1. Orientation finding that shapes the design (tokenizer probe, 2026-06-26)

Realistic coined values do NOT tokenize as a clean 2-token pair. On the Qwen2.5-3B BPE:
- Coined single WORD: `Vextoria`→`[' V','ext','oria']` (3 tok); `Vindexar`→`[' V','index','ar']` (3); most coined words = **3–5 short subtokens**.
- Coined-head + real category noun: `Plurn Heights`→`[' Pl','urn',' Heights']` (3); `Skorn Falls`→`[' Sk','orn',' Falls']` (3).
- Coherent bigram anchor: `Cape Town`→`[' Cape',' Town']` (2).
- Incoherent floor (C10): two unrelated single-tokens = 2 tok.

**Two axes move at once** between the C10 floor and the realistic class:
1. **Length:** realistic coined values are LONGER (3–5 tok) than the 2-tok floor → full-sequence match is mechanically harder by position count alone. **This is a confound and must be controlled.**
2. **Continuation TYPE:** the realistic continuation is a **within-word BPE sub-word** (e.g. `ext`→`oria`) or a **real prior-bearing category noun** (`Heights`,`Falls`), NOT a second unrelated whole word. BPE sub-word continuations may be MORE predictable (merges are frequency-driven) → partial prior-coherence. This is the substantive thing we want to measure.

So the design must (a) control length, and (b) separate "sub-word coined word" from "coined-head + real-noun" because they differ in continuation type.

---

## 2. Design — arms (SAME novel fictional subjects across all arms; isolate the VALUE class)

Subjects = fictional country names (FICTION pool, reuse C10b; no pretrained prior; multi-token fictional subjects fine at N≤24 — the C1 subject-ΔW-blowup is a SCALE-only phenomenon). Relation = capital (`CANON="The capital of {} is the city of"`). One edit request per (subject) per arm → **request-count matched** across arms.

| Arm | Value class | Example | ~ntok | Role |
|-----|-------------|---------|-------|------|
| **A1 single** | real single-token capital | `Oslo` | 1 | ceiling control (anchors "edit works") |
| **A2 coherent2** | real KNOWN bigram capital | `Cape Town` | 2 | prior-coherence positive control (~97%) |
| **A3 incoh2** | two UNRELATED real single-tokens | `Oslo Cairo` | 2 | C10 FLOOR — reproduce ~36% |
| **A4 incoh3** | three unrelated real single-tokens | `Oslo Cairo Lima` | 3 | **length-matched floor** (isolates length from continuation-type) |
| **A5 coined-word** | coined single WORD (sub-word split) | `Vextoria` | 3–4 | SUPPORTING mechanism arm (multi-*token* single-*WORD*; **NOT in R** — see §2.1) |
| **A6 coined-realNoun** | coined-head + REAL category noun | `Plurn Heights` | 3 | **TREATMENT — EASY realistic end** (continuation has prior support) |
| **A7 coined-coined** | coined-head + COINED modifier | `Qorvex Zentra` | 3–4 | **TREATMENT — HARD realistic end / BINDING worst case** (no-prior continuation) |

A4 is the key addition over C10b: it lets us decompose "realistic class is fragile" into *length* (A3→A4 drop) vs *continuation-type* (A4 vs A6/A7 at matched length). **A7 (advisor-mandated) is the genuine worst case within the semantic-entity residual** — a multi-WORD coined entity whose continuation gets NO prior help; without it a "robust" verdict could just reflect A6's real-noun continuation prior-help (the flattering artifact).

### 2.1 Why A5 is supporting-only, and the binding-set invariant
A5 (single coined WORD, "Vextoria") is multi-*token* but single-*WORD*. My own residual definition is multi-**WORD** semantic entities, and a single coined token is arguably a §7.1 *identifier* → routed to Git → out of scope (the same severity-bound move that shrank C10). So A5 is a mechanism probe (does a sub-word continuation store?), **not** a member of the binding realistic set. 

**Binding realistic robustness `R = min(A6 coined-realNoun, A7 coined-coined) para_full`.** Invariant: **R always ranges over a realistic multi-WORD semantic value with a no-prior continuation present in the set** (A7 guarantees this). The honest "size the exposure" deliverable is the **RANGE [A7 hard-realistic, A6 easy-realistic]**, which the operator maps onto their KB's actual value mix (target value-distribution still unset → a single robust/fragile bit would over-claim).

**§7.1 pre-emption (so a fragile result can't be waved off):** A6/A7 values are SEMANTIC named entities (coined place/entity names) — NOT file paths, NOT identifiers, NOT exact strings — so §7.1 does **not** route them to Git. Eyeball every A6/A7 string: if a reasonable reading would call it an identifier, drop it. (A5, by contrast, is *deliberately* the identifier-adjacent case → excluded from R.)

**Value-pool construction rules (verify empirically in the harness, HALT if violated):**
- Every value must have pre-edit canonical base ≈ 0 / N (no prior; fictional subject carries none, but verify the VALUE isn't independently predicted).
- A5 coined words: generated coined strings, verified ntok≥3 and base 0; verified NOT a real word.
- A6: coined head (no prior) + real noun from {City, Heights, Falls, Bay, Port, Springs, Harbor, Crossing}.
- A7: coined head + coined modifier (both no-prior), verified base 0; reads as a place/entity name, not an identifier.
- Report mean ntok per arm; A4/A6/A7 should cluster at 3 (±1) for the matched-length comparison; A5/A7 may run 4 — report and read length-conditionally via the per-continuation-token metric.

---

## 3. Metrics

**Binding metric = held-out-paraphrase FULL-SEQUENCE match** (greedy decode `len(target_ids)`, exact, over 3 held-out PTEST paraphrases — NOT the canonical/trained prompt, which is a teacher-forcing artifact). Per arm report:
- `para_full` (binding), `para_first`, `para_any_full`, `canon_full` (teacher-forcing reference only).
- **Conditional P(full | first-correct)** — the clean "did it store the CONTINUATION, not just first-token+prior?" de-confounder (C10: 0.51 incoh vs 1.00 coherent).
- **Per-continuation-token accuracy, TEACHER-FORCED** — given the correct prefix, fraction of subsequent target tokens that are the argmax. Teacher-forced (not free-running) so it isolates per-position storage and length-normalizes cleanly (a free-running metric cascades early errors and re-confounds with length). This makes A7's 4-tok values comparable to A3's 2-tok.

**LAW#5 inertness gate** (fuller: p-delta AND locality) runs first; HALT if not inert. Engine UNMODIFIED; primitives verbatim from c10b (proven inert).

---

## 4. Pre-registered verdict rules (frozen BEFORE the run; numbers fall where they land)

Let `S = A1 single para_full` (ceiling), `Floor = A3 incoh2 para_full`, and **`R = min(A6 coined-realNoun, A7 coined-coined) para_full`** (binding realistic robustness — ranges over a realistic multi-WORD value with a no-prior continuation; default to the less-flattering reading). A5 is reported but NOT in R.

First sanity gates (else INCONCLUSIVE): `S ≥ 80` (edit works at all) AND `A2 coherent2 ≥ 80` (positive control fires) AND `Floor ≤ 55` (C10 floor reproduces; if Floor is high the whole effect didn't replicate this seed).

Then, comparing the realistic class to the **length-matched** floor A4 (incoh3) and the ceiling:
- **RESIDUAL ROBUST (C10 largely an artifact):** `R ≥ 80` AND `R − A4 ≥ 25` → realistic coined values generalize far above the length-matched incoherent floor → C10's bite is mostly the contrived two-unrelated-word case; in-weight project-coined values are usable. → C10 severity DOWN-sized.
- **RESIDUAL FRAGILE (C10 bites the real KB):** `R ≤ A4 + 10` (realistic ≈ length-matched floor) OR `R ≤ 50` → project-coined values fail like incoherent ones → C10 covers the real in-weight value surface; the AnyEdit port / hybrid-routing is warranted. → C10 severity CONFIRMED at the sized level.
- **PARTIAL / MID-BAND (the likely outcome):** otherwise — realistic class sits between floor and ceiling. Report the point estimate + the governing variable (length vs continuation-type, read off A3→A4 vs A4→A5/A6 and the per-continuation-token metric). C10 severity = sized to that fraction; document as a value-class-dependent gradient.

Whatever the band, the deliverable is the **RANGE [A7 hard-realistic, A6 easy-realistic] `para_full` + the decomposition** (how much of any shortfall is length, read A3→A4, vs continuation-type, read A4→A6/A7, plus the teacher-forced per-continuation-token metric) — that is the "size the exposure" answer the operator asked for. A single robust/fragile bit would over-claim at N≤24/1-seed (±~11% at 72 trials); the range is what the operator maps onto their KB's value mix once the target value-distribution is set.

---

## 5. Discipline / threats

- Same subjects across arms; request-count matched (1/subject/arm); 1-seed → valid WITHIN-experiment contrast, generality needs replication.
- Cov recomputes ~20 min/process (no disk persistence) — budget it; single process for all arms.
- Decisive result → Perplexity/Sonar cross-family (codex auth likely expired); advisor before build AND before verdict; default to the less-flattering reading.
- `.gitignore *token*` eats "multitoken" filenames → file = `c10d_residual_coined.py` / `c10d_residual_coined.json`.
- This is NOT a deployment recipe change and NOT promotable to a proven node — it SIZES an open condition (C10) for the F1 determination.
