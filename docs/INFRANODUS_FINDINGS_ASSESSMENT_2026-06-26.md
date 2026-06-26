# Assessment — InfraNodus "spec-vs-repo gaps" findings (2026-06-26)

> **What this is:** a critique of an external tool's output, not a CORPUS finding. InfraNodus was
> asked to surface gaps between the v1.2 spec and the repo's PROGRESS.md Northstar, and to estimate
> "% of spec proven viable." This doc assesses those findings against the repo's authoritative map
> (`PROGRESS.md` ⓪ e2e coverage + ⑤ F1 readiness scorecard / conditions register).
>
> **Authoritative sources (these win on any conflict):** `PROGRESS.md`, `CORPUS/00`+`03`,
> `EXPERIMENT_RUNBOOK.md` §0.3/§12, `docs/F1_DETERMINATION.md`, `docs/SPEC_E2E_GROUND_TRUTH.md`.

---

## Bottom line

**Textually real, but framed wrong.** The findings describe the spec's most lexically-dense prose
region (governance/ceremony/trust machinery), not the program's actual evidence frontier. The
"~12–18% proven" headline is methodologically invalid. They recovered ~one real (already-tracked)
signal — the governance/orchestration tail is unevidenced — wrapped in a wrong frame, a factual
overstatement on G2, one outright reversal (D1 calibration), and missing every falsifier on the
F1 critical path.

---

## 1. The tool is being used outside its competence

Per the program's standing note ([[infranodus-discourse-lens-not-coverage-tool]]), InfraNodus is a
**discourse lens over text you feed it — it cannot read code or assess evidence coverage.** What it
surfaced is the **most densely interconnected terminology cluster in the spec document**:
`ceremony → type → auth → cak`, break-glass, CAK bootstrap, scope registry, archive restore. That's
why governance/trust machinery dominates every answer — it is the verbose, highly cross-referenced
region of the *spec*, not a finding about what the *repo* has evidenced. The `gap <-> ceremony`,
`operator <-> signature` phrasings in the responses are literally graph node-edge language leaking
through. The tool surfaced the spec's most connected lexical cluster; the AI narrated it as "the gaps."

## 2. Category error: it scores the wrong goal

The findings treat the repo as a *production-implementation* project and tally missing operational
tooling (CAK bootstrap tool, fuzzer, break-glass quorum ceremony, restore pipeline). But the actual
Northstar (`PROGRESS.md` ①, **F1**) is **"prove/falsify the spec is implementable *before* it's
built"** — falsification-first, delivering a ready/not-ready determination. "No CAK bootstrap tool
exists" is **not a gap-to-Northstar** — building it was never what F1 requires. The findings answer a
question the program is not asking.

## 3. It inverts the actual map — and omits all the science

Repo's own e2e coverage view (`PROGRESS.md` ⓪):

- **Write/deploy spine: PROVEN-FOR-SCOPE** — recipe (AlphaEdit) → A1 (batch eliminates cross-entity
  corruption, 100%) → B3 (survives real Q4_K_M) → E1·A (CPU-serve ~8–13 tok/s).
- **Governance (G1/G2/G3, CP1/CP3): PROTOTYPED** for-scope, not empirically stressed.
- **Read contract / Pruning-GC / lifecycle-loop: UNTOUCHED** — the program names *these* as the
  honest F1 frontier.

The findings mention **none** of this — not the write engine, MEMIT, corruption, quantization, the
D1 capacity law, CP2 read-contract, or the C10 multi-token falsifier that actually *fired*. They
spotlight the prototyped/deferred governance cells while ignoring both the proven core and the real
open frontier the repo already tracks.

## 4. At least one concrete factual overstatement

Finding #3 says the break-glass/ceremony chain is "specified design, **zero tooling** … entirely
theoretical until someone builds a fuzzer." But **G2 (CORPUS/11) already prototypes it**: real
Ed25519 verify-cannot-forge + overlay integrity + **CAK ceremony, 9/9 for-scope**. The honest status
is *prototyped-not-empirically-stressed*, not "zero."

## 5. The percentage (~12–18%) is invalid

- Computed from **spec-text surface area**, so it *rewards spec verbosity* — the more elaborate the
  (explicitly deferred, implementation-phase) governance prose, the lower "% proven" looks.
- The finding itself notes the spec defers these as implementation-phase (GAP-1/2, "provisional
  illustrative defaults") — then **uses that deferral to inflate the unproven bucket**, treating
  implementation-phase deferral as science-phase un-viability. Backwards.
- Conflates *core scientific viability* (can frozen weights + overlay + MEMIT-class writes serve as a
  DB? — largely settled-positive for-scope on the spine) with *operational completeness* (a
  production governance layer — deliberately unbuilt).
- The program has **no "% proven" metric** because F1 is a falsification determination, not coverage.
  The real output already exists: **NOT-READY-WITH-CONDITIONS** with the deployment spine
  PROVEN-FOR-SCOPE and a **10-row conditions register** of named falsifiers. A single percentage
  erases that structure.

## Where the findings *do* land something real

Not pure noise — they correctly point at genuinely un-evidenced cells the repo *also* marks open:
§22 epsilon calibration, archive/restore, scope-registry reconciliation, orchestration (§12, "not
engaged"), Pruning/GC. These map to PROGRESS conditions **C5/C6/C7** (Phase-2 governance/security/
pruning). So the findings are a fuzzy, mis-weighted echo of the *bottom rows* of the conditions
register.

---

## 6. Line-by-line mapping onto the F1 conditions register (PROGRESS ⑤) + e2e map (⓪)

Verdict key: **KNOWN-OPEN** = real cell the program already tracks · **MIS-FRAMED** = real cell,
wrong frame/proportion (operational not falsifier; or spec-deferred) · **WRONG** = factually
overstated or contradicted by an existing node.

| # | Finding | Maps to | e2e cell | Verdict | Why |
|---|---|---|---|---|---|
| 1 | Genesis-timeout → `DIVERGED_STATE` recovery runbook | **C5** (governance+orchestration) | State-consistency §11 (G1 *prototyped*) + Orchestration §12 (*not engaged*) | **KNOWN-OPEN, mis-scoped** | Circuit-breaker trip itself is prototyped (G1, 10/10). Recovery is orchestration-layer — and the *spec itself* calls it "a separate operational step." Real open cell, but an ops runbook gap, not an F1 implementability falsifier. |
| 2 | Key lifecycle (rotation/HSM/cross-project) | **C6** (security) | Security §10 (G2 *prototyped*) | **MIS-FRAMED** | Spec **explicitly defers these to v2**. F1 evaluates v1.2-as-specified, so a v2 deferral is outside the determination's scope by construction. |
| 3 | Break-glass / CAK bootstrap / M≥3 quorum — "zero tooling" | **C6** (security) | Security §10 | **WRONG (partial)** | **G2 / CORPUS/11 already prototypes the CAK ceremony 9/9** + Ed25519 verify-cannot-forge. "Zero tooling / entirely theoretical" is false. The pre-harness *bootstrap tool* doesn't exist — but the spec designates it as something the harness **cannot** produce, so its absence is by-design. |
| 4 | Corpus Author Registry — expired-author enforcement (§24) | **C5** (governance) loosely | Validation §9 (G3) / spec-internal corpus governance | **MIS-FRAMED / off-map** | Governance of the spec's *own test corpus*, not an implementability falsifier. Untracked because it isn't on the F1 path, not because it's overlooked. |
| 5 | Meta-TGA/Validator sealed corpus — 20-case minimum | **C5** | Validation §9 (G3 *prototyped*) | **MIS-FRAMED** | Validator is prototyped (G3, 8/8 for-scope). "Needs 20 gold cases authored" is implementation-phase bootstrapping of a test fixture — not science the determination turns on. |
| 6 | Epsilon calibration protocol §22.4 — "no tooling to run it" | **C4 / D1** (drift, OQ-W1) | Memory-lifecycle drift trigger (**AMENDED**) | **WRONG / outdated** | Nearest the real science, gets it backwards. ε/drift calibration is a **proven node**: D1 structural (drift = per-relation concentration, model-general) + numeric guardrail `k≤1` (D-D1-2), with `tools/power.py` as the live instrument. Claims unbuilt what's actually one of the strongest results. |
| 7 | Archive restore path (GAP-52/GS11), restore cross-checks | **C7** (Pruning/GC) | Pruning/GC · archive · accumulate→compact LOOP (**❌ UNTOUCHED**) | **KNOWN-OPEN (legit hit)** | Genuinely maps to the cell PROGRESS ⓪ flags as "≈half of production memory mgmt — UNTOUCHED." A real, already-tracked open node. |
| 8 | Scope-registry reconciliation on restart (GAP-25/GS5) | **C5** | Orchestration §12 (*not engaged*) + Ledger §11 | **KNOWN-OPEN, mis-scoped** | Orchestration restart logic — real, but in the "not engaged" cell. Operational, not a science falsifier. |
| 3-extras | Scope-hash 5s ceiling, IC-AGG-COUNTER, Dependency-Hold 72h lifecycle, Ledger retention | **C5** | §11/§12 prototyped-or-not-engaged | **KNOWN-OPEN, mis-scoped** | Same family — the governance/orchestration tail. Prototyped (G1) or not engaged. |

## 7. The shape of the miss

Plotted against the register, the findings cluster entirely at the **bottom three rows — C5, C6, C7**
(governance, security, Pruning/GC), the Phase-2 operational tail the program already labels
prototyped-or-untouched.

What they **never touch** — the entire critical path and write-robustness frontier:

- **C1** compaction-at-true-scale — *the program's own "sharpest" falsifier*, D20 directionally negative. Absent.
- **C2** read/query contract — *flagged "biggest gap"* in both ⓪ and ⑤. Absent.
- **C10** multi-token value — *a falsifier that actually **FIRED*** (D-C10-1, incoherent-multi 36.1%). Absent.
- **C3** R5-at-scale, **C4** 7B numeric transfer, **C8** R15-adversarial, **C9** R9-native-deletion — all absent.

So the findings recovered ~one real signal (the C5/C6/C7 governance-orchestration tail is unevidenced
— already known) and **missed every falsifier on the critical path**, including the two the program
names biggest/sharpest and the one that already fired. Plus one reversal (#6) and one overstatement
(#3 vs G2). This is the signature of a discourse-lens over spec *prose*: it surfaces the verbose,
highly-interlinked governance region and is blind to the cells where the actual science lives —
because those cells are thin in the spec text and dense only in the CORPUS evidence ledger, which the
tool never saw.

---

## Appendix — the source InfraNodus findings being assessed

> Verbatim record of the first response (the 8-gap enumeration) the assessment critiques. The later
> responses repeated the ceremony-chain answer (responses 2 and 3 were near-verbatim duplicates
> before a different answer was produced) and added the "~12–18% proven" estimate addressed in §5.

**1. Genesis Timeout/Trip Pairing — Specified but Operationally Hollow.** The spec defines
`GENESIS_TIMEOUT_TRIP_MISSING` (C-GTO-1/2, IC-MON-GTOTM) and the circuit-breaker trip to
`DIVERGED_STATE`, but there's no recovery runbook. The spec explicitly says "recovery of the
Orchestrator control plane is a separate operational step" — meaning the gap between *detecting* a
genesis timeout and *resolving* it is entirely unspecified. A PROGRESS.md Northstar needs a concrete
state-machine for DIVERGED_STATE → operational recovery.

**2. Key Lifecycle Is Explicitly Deferred.** Orchestrator key rotation, cross-project key sharing,
and HSM-backed storage are all punted to v2. Yet the entire trust model — ceremony authorization,
Ledger integrity, break-glass — chains through `ORCHESTRATOR_KEY_ANCHOR` and
`ceremony_authorization_key_anchor`. The Northstar can't claim production-grade trust without at
least key rotation. The spec acknowledges this but the repo has no path toward it.

**3. Break-Glass Channel: Specified Design, Zero Tooling.** C-BG-1 through C-BG-7 are fully
specified, but the CAK bootstrap tool (IC-BOOT-1 through C-BOOT-7) is a *pre-harness operator tool*
that the spec says the harness itself cannot produce. The repo needs this tool to exist externally,
yet PROGRESS.md likely tracks only harness-internal deliverables. The M≥3 quorum ceremony,
physical-access injection path, and `TRUST_ROOT_LOST` terminal state handling are all spec-complete
but implementation-absent.

**4. Corpus Author Registry — Two-Point Enforcement Gap.** §24 specifies dual enforcement
(submission ingress + IC-SL7 token issuance), the `EXPIRED_AUTHOR_PRESENT` advisory flag, and the
`contains_expired_author_cases` field. But the corpus-author-registry is a *Tier 2 sealed corpus*
requiring human-signed manifests and versioned additive directories. The pipeline from "operator adds
an author identity" to "Meta-* run correctly flags expired cases" crosses at least four interface
contracts (IC-CORPUS-AUTH, IC-SL7, A12, A13) — each needing implementation and integration testing.

**5. Meta-TGA / Meta-Validator Sealed Corpus Minimum Viability.** The spec requires 20 cases minimum
before `health_score` is anything other than `NOT_COMPUTED`. The 90-day staleness flag and 180-day
enforced `HEALTH_SCORE_STALE` are defined, but the repo needs actual gold test sets authored by
registered corpus authors. Without these, the entire validation layer's self-check mechanism is inert
— the Northstar's quality assurance loop literally cannot start.

**6. Epsilon Calibration Protocol — Report Defined, Process Unbuilt.** §22.4 defines
`epsilon_calibration_report` with per-transform-class ε values and bucket boundary calibration, but
this is a pre-operational calibration ceremony. The spec retains "provisional illustrative defaults"
(0.33/0.66) while requiring project-specific calibration. The gap: no tooling exists to *run* the
calibration protocol.

**7. Archive Restore Path — Specified but Untested by Design.** The archive-manifest schema
(GAP-52/GS11), `ARCHIVE_KEY_SEALED` Ledger entry, and restore-time cross-checks against Genesis Seal
are all specified. But `RESTORE_MANIFEST_INVALID` and `RESTORE_CHAIN_BREAK` failure modes imply a
restore pipeline that needs the `signer_public_key_material` → Genesis Seal cross-check to actually
function. This is a gap between "spec says verify" and "repo has verification code."

**8. Scope Registry Reconciliation on Restart (GAP-25/GS5).** The spec says on Orchestrator restart,
read the Ledger back to the most recent `SCOPE_ANCHOR` entry. [response truncated in source]

**Percentage claim (responses 2–3):** estimated "~12–18% of the spec has been proven viable," with
the MEMIT write-engine designation, `.vindex` overlay, semantic/syntactic partition, and 2PC commit
protocol cited as the evidenced ~12–18%, and the ceremony/trust chain, scope-hash propagation,
epsilon calibration, Dependency-Hold lifecycle, and Ledger retention/archive cited as the unevidenced
~82–88%. See §5 for why this percentage is methodologically invalid.

═══════════════════════════════════════════════════════════════════════

# PART B — Assessment of the SECOND InfraNodus run (2026-06-26): "5 determining experiments + falsification verdict"

> **What this is:** a critique of a *distinct* InfraNodus output, run this time with the **full git
> repo** attached as context (not just the spec). It proposed 5 "must-run" experiments in two tiers
> ("Spec Lives or Dies" / "Protocol Viability") plus a falsification claim ("if #1 and #3 both fail
> the spec isn't implementable"). Assessed against the same authoritative sources (`CORPUS/00`+`03`,
> `EXPERIMENT_RUNBOOK.md` §0.3, `docs/F1_DETERMINATION.md`). Advisor-checked (Opus) before writing.

## B0. The full repo didn't change the tool's nature

Even with the repo attached, InfraNodus builds a **co-occurrence / betweenness graph over the repo as
text**. It detects where discourse is *dense vs thin* and which terms chain with high betweenness. It
**cannot read the status ledger's semantics** — it can't tell a `PROVEN` row from an `OPEN MUST-FIX`
one. So it weights proposals by *textual prominence*, not *experimental status*. The clean line:
**its topology reads are legitimate; its experiment list and falsification verdict are not** —
crossing from "here's a thin region" to "here's the experiment that kills the spec" requires the
PROVEN/OPEN awareness it structurally lacks ([[infranodus-discourse-lens-not-coverage-tool]]).

## B1. The decisive tell — it omits C10 entirely

The program has exactly **one** condition currently labeled `FALSIFIER FIRED / OPEN MUST-FIX` *on the
critical path for the fixed deployment target* (`local Intel CPU + batch`): **C10 multi-token value
realization** (D-C10-1; D-C10b-residual 2026-06-26 — realistic project-coined multi-word values
express at **19–31%** held-out vs an 85% gate). It appears **nowhere** in this run's "Spec Lives or
Dies Here" list. If the list were status-weighted, C10 would be #1; "multi-token" is just a
low-betweenness term in the corpus. **Its absence is the thesis** — the single cleanest proof of
state-blindness. Everything below is corroboration.

## B2. The five proposals vs the ledger

Verdict key: **OPEN/MIS-FRAMED** = real cell, but stated as un-started when it's partial · **DONE** =
already characterized · **CLOSED-FOR-SCOPE** = demonstrated, residual is narrow.

| # | Proposal | Actual status (ledger) | Verdict |
|---|---|---|---|
| 1 | 7B numeric threshold transfer (OQ-W1) | **Partial AND descoped.** B1 model-size term (D-B1-2): concentration law is *model-general* on 7B; numeric threshold `UNRESOLVED` — blocker is **instrument variance** (~50pp run-to-run swamps the ~11.5pp signal), not absence of data. **Critically: C4 governs the *incremental* drift contract, which DROPPED OFF the critical path when the deployment target was fixed to `batch re-Genesis`** (no accumulation between compactions; F1 §3 re-scope). | **Off-critical-path for the fixed target — yet ranked #1 "lives or dies."** The sharpest possible illustration of state-blindness: the tool elevated a condition the program *descoped*. = condition **C4** (open, incremental-path-only). |
| 2 | compute_z inflation isolation (CORPUS/17) | **Done.** Margin confound named (CORPUS/21); C10 z-probe *directly* measured it — `compute_z` hits 0.99 for all classes → "NOT a compute_z knob." Program already switched the binding metric to held-out paraphrases to avoid leaning on it. | **Solved-as-methodology.** Good instinct, already internalized. Not a falsifier. |
| 3 | key collinearity under batch | **Observed, more nuanced.** Single-token subjects: N=50/100 batch stays clean (ΔW 207/294). Multi-token subjects: key-collinear → ill-conditioned solve → ΔW blow-up → garbage (the N=2000 collapse, D-C1TS-1). AlphaEdit null-space is the existing mitigation. | **Real axis, wrong conclusion.** Fails *loudly* (garbage), not "silently"; clean substrate doesn't collapse at batch. |
| 4 | cross-session persistence round-trip | **Closed-for-scope.** Behavioral round-trip demonstrated: B3 edit → Q4_K_M → GGUF → llama.cpp reload → 100% expression. Bit-repro is a *declared non-requirement* (§8.10). Residual = G5 real-Intel-CPU. | **Lowest priority.** Largely answered; genuine residual is hardware (G5). |
| 5 | adversarial load on auth ceremony | **Convergent triangulation.** C5 governance = prototyped-not-empirical; C6 = red-teamed-1-mechanism (D-C6L-1 found a *real* gap: ledger rewrite + truncation undetected). | **Triangulation, not a find.** A discourse lens independently landing on an already-named soft spot = mild reassurance. = conditions **C5/C6**. |

## B3. The central falsification claim is wrong on its axis

> "If #1 and #3 both fail — thresholds don't transfer to 7B AND keys collapse under batch — the spec
> isn't implementable, because the numeric and structural layers are coupled in a way the spec denies."

Two defects:

1. **A numeric↔structural coupling already occurred and was absorbed by amendment, not spec-death.**
   D1 found the drift *predictor* must be relation-structure-aware (global `edge_count_since_anchor`
   is insufficient) → §8.7 was amended (operator-approved) and the spec survived as
   not-ready-with-conditions. So "if coupled, the spec dies" is contradicted by what happened.
   *(Altitude note: D1's coupling — predictor-must-be-structure-aware — is not literally InfraNodus's
   coupling — threshold-constants-feed-protocol-ordering. The meta-point holds; the specific
   mechanisms differ. Don't claim D1 "precisely refutes" the claim.)*
2. **"Auth windows and retention cascade from those constants" conflates a real thread with an
   invented one.** Compaction/anchor *cadence* genuinely depends on the drift constants (the §8.7
   `k≤1` re-anchor guardrail) — that thread is real. But the auth ceremony (Ed25519 / CeremonyToken)
   does **not** cascade from drift thresholds — that's a co-occurrence artifact, the lens reading
   `ceremony→key→auth→threshold` proximity in the text as a causal chain.

## B4. The shape of the miss (Part B)

Same signature as Part A. This run correctly mapped **topology** — 7B-transfer is genuinely thin (#1),
governance/security is genuinely under-stressed (#5) — both convergent with the program's own
conditions register. But it **mis-framed 3 of 5** as un-started when they're partial/done/closed,
**invented one causal coupling**, built a **spec-killing verdict on the wrong axis**, and **missed
C10**, the one fired falsifier on the deployment-target critical path.

**Net:** legitimate topology, illegitimate verdicts. The one item worth lifting into the queue is
#1's reframing — a useful external nudge that 7B transfer is still visibly unresolved — but the work
it needs is a *lower-variance instrument* (determinism), the cheaper lever the program already knows.
**Do not reprioritize off this run.** Canonical "what's next" = `EXPERIMENT_RUNBOOK.md` §0.3, unchanged.

## B5. Appendix — the source InfraNodus output being assessed (Part B)

> Verbatim, the 5-experiment + falsification response.

**Must-Run (Spec Lives or Dies Here):** (1) *7B Numeric Threshold Transfer* — run MEMIT edits on a 7B
model, measure drift, compare against provisional OQ-W1 thresholds; if off by >~2× the ceremony chain
breaks because auth windows and retention timings cascade from those constants. (2) *Compute_z
Inflation Isolation* — CORPUS/17 flags MEMIT's compute_z inflates edited-fact margins; run identical
probes native vs post-edit, same prompts/temp; the delta is the confound magnitude. (3) *Key
Collinearity Under Batch Pressure* — scale batch to 50+ edits, check covariance condition numbers; if
keys go collinear the orchestrator can't distinguish edits and persistent memory fails silently.
**Must-Run (Protocol Viability):** (4) *Cross-Session State Persistence Round-Trip* — serialize memory
state, kill process, reload, re-probe; if fidelity drops below contract threshold persistent memory is
decorative. (5) *Adversarial Load on Auth Ceremony* — inject malformed/out-of-order ceremony messages,
verify fail-safe rather than silent corrupt-state acceptance. **Falsifies entirely:** if #1 and #3
both fail, the numeric and structural layers are coupled in a way the spec's "ratified structure vs
implementation-phase numerics" separation denies — making the spec not-implementable.
