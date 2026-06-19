# 06 — THE SPEC'S WRITE PATH & WHERE THE BRIDGE FITS (corrected after full spec read)
_Written 2026-06-18 after reading the spec end-to-end (§7–§13). Corrects earlier framing built from grep-only excerpts. This DISSOLVES the "bridge-vs-spec-governance decision" — there is no architecture fork; there is a governed pipeline to build and our validated recipe is its engine internals._

## 1. Git vs model — the partition (§7.1 D1, §11.2 D42) — earlier mischaracterized
- LLM/`.vindex` stores **semantics** (relationships, rules, knowledge — the *map*). Git stores **syntax** (literal code, file contents — the *territory*). **No code in the model.** Hard boundary (D1).
- They hold DIFFERENT content; each is authoritative for its class (D42: Git→`structural_entity`; `.vindex`→L4 `domain_concept`/`constraint_rule`). 2PC keeps their *correspondence* consistent + jointly rollbackable — NOT mirroring the same content. (My earlier "weights and repo stay in sync" was sloppy.)

## 2. The spec's GOVERNED write path (§9.10, §10.2, §11.5, §12.2)
```
Coder drafts code + .larql  →  TGA authors tests (independent, §9.2)  →  Validator cascade (correctness, §9.3)
   →  signed pass  →  COMMIT EXECUTOR (deterministic, non-reasoning; SOLE dual-medium writer, D40/C-OR6)
   →  PATCH AUTHORIZATION GATE (Identity→Scope→Integrity + single-use token, §10.2)
   →  2PC: Git push FIRST, .vindex mount SECOND (D46/C-TPC3)
   →  STATE LEDGER (PREPARED/COMMITTED, Merkle-chain, §11.15)
```
- **§12.2 C-OR2:** "the write path (Gate → Commit Executor → MEMIT → Git) must be deterministic, non-reasoning code. LLM agents never hold simultaneous write access to both mediums."
- **§10.2 C16: "Direct filesystem writes to `.vindex` bypass the gate and are treated as security violations."**
- MEMIT safeguards are MANDATORY (§8.2 D20): **orthogonal projection** (new fact vectors orthogonal to existing) + **covariance balancer**. Targets middle-to-late FFN (L15-25/32-layer, C15).
- Post-write probes (§8.9 D18): **L1 storage = `SELECT` read-back (mandatory, ALL writes)**; L2 behavioral = generation test (CORE/SUPPORTING).
- `.larql` = the logical patch language (BEGIN TRANSACTION…COMMIT; entity reg; edge decls; `DELETE FROM EDGES`; directives TIER/CONTENT_CLASSIFICATION/ORTHOGONAL_PROJECTION/SET TARGET_LAYERS). `.vindex` = overlay tier stack. **`.vlp` = LARQL's implementation patch file (impl detail, not a spec term).**

## 3. Where our work actually sits (the dissolution)
- **Our editing recipe (in-solve AlphaEdit = null-space/orthogonal projection + preserve-sampling + batched compile) = the MEMIT WRITE ENGINE'S INTERNALS.** It ALIGNS with the spec's mandatory D20 orthogonal-projection safeguard. It is NOT a competitor to the governance; it is *what the engine computes inside the governed path.*
- **LARQL = the `.vindex` format + serve/query layer** (and optionally the MEMIT compile). It sits INSIDE the governed write path; the Commit Executor invokes it through the Gate.
- **The "decoupled bridge" (our ΔW → `.vlp` → APPLY → COMPILE) is a VIABILITY HARNESS, not an architecture.** It deliberately bypasses the Gate/Commit-Executor/2PC/Ledger to PROVE the edit+serve mechanics fast. **Used as a production write path it would be a C16 security violation.** It is scaffolding that proved: (a) the editing math is clean in-weight, (b) LARQL serves it on CPU.

## 4. Therefore — there is NO "bridge vs spec governance" decision
The earlier dilemma was an artifact of not having read the spec. Correctly framed:
- The spec's governance (Gate, Commit Executor, 2PC, State Ledger, tokens, Write Scope Definitions) is **REQUIRED and is the LOCAL BUILD** (it is systems/orchestration work = gaps G1/G2/G3).
- Our recipe is the **engine internals** (validated, spec-aligned).
- LARQL is the **`.vindex`/serve layer** (validated on CPU).
- BUT — what dissolves is **architecture-OWNERSHIP** (you don't adjudicate an ML architecture fork), NOT all viability. Three genuine checkpoints remain UNPROVEN and are the FIRST local tests (do not assume "resolved"):
  - **CP1 — governed, in-pipeline MEMIT write (UNPROVEN).** We proved the edit MATH + OFFLINE serving. We did NOT prove a MEMIT compile running as a first-class IN-PIPELINE step under the Commit Executor/Gate. The spec wants exactly that (it eliminated n8n for failing to host "multi-minute GPU-bound MEMIT compile as a step"). Our bridge ran compile OUT-OF-BAND; LARQL's in-tool COMPACT is the immature path we couldn't drive. So "where the math runs" is NOT trivial plumbing — whether ANY governed in-pipeline compile works (LARQL-native, or our-recipe-wrapped-and-fed-through-the-Gate) is the #1 local viability test.
  - **CP2 — query-schema capability (UNPROVEN).** We tested `INFER`/generation only. The spec's L1 storage probe (mandatory EVERY write) is a `SELECT` read-back; schema needs `SELECT`/`DELETE FROM EDGES` over the triple model + 5 relation families + `violates` rejection. Whether LARQL's LQL actually expresses this is a CAPABILITY question, not plumbing.
  - **CP3 — MEMIT-compliance of our recipe (CONFIRM, don't assume).** Spec designates MEMIT (D12; ROME/GRACE/fine-tuning EXCLUDED). AlphaEdit's null-space step maps to the D20 orthogonal-projection safeguard (good signal) — but confirm AlphaEdit+preserve-sampling+batched-compile counts as "MEMIT" for spec-compliance vs. an extension to flag.

## 5. Net for the operator (honest version — corrected after advisor review)
- **Architecture-OWNERSHIP is dissolved:** you do NOT have to adjudicate an ML architecture fork. The architecture is the spec's; our validated recipe is the engine internals (D20-aligned); LARQL is the `.vindex`/serve layer.
- **BUT viability is NOT fully proven.** We proved the edit math + offline serving + the editing science (Tiers 1-2, Qwen3). We did NOT prove CP1 (governed in-pipeline MEMIT compile), CP2 (LARQL query-schema capability: SELECT/DELETE/triple/relation-families), or CP3 (MEMIT-compliance of AlphaEdit). **These are genuine viability checkpoints — gated FIRST — but they are POD-RUNNABLE NOW (see §7), not "local-only."**
- So the next move is NOT "it's all just engineering now," and NOT "stop and go local." It is: **bank the corpus → run CP1/CP2/CP3 as gated prototype experiments ON THE POD → then the governance gaps (G1-G3) and capability/scale gaps (G6/G7) on the pod.** The binding evidence is EMPIRICAL (pod-gatherable); only the final chosen-deployment-hardware check is contingent. Further same-model REVIEW adds little — gather evidence instead.
- **Do NOT convene the same-model council** to confirm this framing (confirmation-amplification of a self-authored conclusion). An independent (different-model) cold read of spec+corpus is optional and nice-to-have, not load-bearing.

## 7. WHERE these tests run (2026-06-18 correction)
CP1/CP2/CP3 + gaps G1-G3/G6/G7 are POD-RUNNABLE NOW (this is a full Linux box: GPU for MEMIT compile, CPU for serving proxy — already used for the LARQL CPU positive control). They are NOT 'local-only'. Three tiers: (1) viability/prototype tests = POD now; (2) full harness development = the build project, env TBD; (3) deployment-hardware check = contingent (operator may deploy on REMOTE GPU, not local Intel CPU → pod is a valid proxy). 'Go local / stop' was too strong — continue on the pod gathering empirical evidence; skip the same-model council (review != evidence).
