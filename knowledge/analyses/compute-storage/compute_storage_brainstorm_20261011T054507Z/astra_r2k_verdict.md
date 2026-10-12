VERDICT: NO-GO

Gate 1 remains OPEN. Round 8 repairs the original guard composition and several checker defects, but three substantive gaps remain. Aliases below are those defined in the review request.

F1. [high] **Production profiles apply A1 to admission processes and helpers that retain full pre-release registration.** Evidence: D8:13–17,34; F6:209,263; J5:4861–4877; P3:45996–46005,46454–46468,46585–46599,49981–49987; `tools/c10w_p2_gate.py:62–79`.

The `p2-shuf-s1` wrapper declares `c10w_p2_gate.py` as `SCIENCE_CHILD`, with `DECLARED_AT_ROOT_ADMISSION` and authority `D-R2C-A1`. Its fingerprint helper receives the same treatment. That gate also appears as the broker’s separate `existing_admission`.

A1 expressly preserves admission/verification helpers’ pre-release registration. Moreover, helpers spawned by the broker’s admission process run **before the payload root exists**: they cannot obtain the exception through descent from that registered science root. The unchanged gate uses ordinary `subprocess.run`; suspending and registering the admission root does not register its subsequently spawned helpers.

**Consequence:** F6’s accurate amendment quotation is not faithfully implemented throughout P3. The guard/broker split fixes the original guard defect, but the admission subtree remains inconsistent. These P2 routes are currently CHILD_ONLY under a refused coordinator; this is a frozen composition defect, not evidence of an executed bypass.

F2. [high] **At least two retained no-op admissions omit source-defined outer dispatch checks.** Evidence: D8:39; P3:4416–4435,4899–4901,11770–11789,372189–372209; K5:1809–1817; `experiments/track_c/c10w_oracle_step0.py:310–331,411–415`; `experiments/track_c/c10w_oracle_eval.py:352–374`.

Direct P1 and P3 evaluator profiles remain TOP_LEVEL with `/usr/bin/true`. Their audits assert `outer_obligations=[]`, principally because the P2 wrapper cannot reach these variants.

However, the dispatcher that **does** reach them calls `guard_phase_projection` immediately before evaluation. That check recomputes projected phase cost from completed training records and applies the phase budget. Direct evaluation checks training/provenance and, for P3, the stored authorization projection; it does not perform that current dispatcher projection. The evaluator’s elapsed-time/memory guard is a different check (`c10w_oracle_eval.py:78–83`).

K5 checks that audit citations exist and their line numbers are in range; it does not establish the asserted absence of obligations.

**Consequence:** The direct P2 trainer/evaluator repair closes the named P2 bypass, but the claim that all **29** retained no-op admissions are justified across every reaching chain remains false.

F3. [high] **K5 still permits a delegation to reference another launch’s binding.** Evidence: F6:115,117,245; K5:1679–1688,1785–1795,1928–1948; P3:146239–146267,152308–152336.

The new check correctly enforces one context across the collected `InvocationBinding` records and their bound source values. It also checks the context labels on enrollment/delegation records. It does **not** resolve a delegation’s `admission_binding_sha256` or `payload_binding_sha256` and require the target to belong to that same profile, context and template.

A concrete static counterexample is to replace profile 000’s delegation payload hash at P3:146267 with profile 003’s payload-binding hash at P3:152336, leaving both trees’ binding records and context labels intact, then update the whole-file profiles pin. The implemented checks do not compare that delegation edge with the owning payload binding. Production validation runs schema validation and invocation reconstruction, without the complete reference-coherence validation used for J5’s construction.

This is a **source-derived counterexample, not an executed custom mutation**.

**Consequence:** The supplied R8R6 control closes V7’s specific bound-value substitution, but authenticated delegation is not yet checked end to end. K5’s GREEN can still coexist with a binding reference from another launch.

F4. [note] **The observation limitations, principal D5 repair and commissioning boundaries are stated honestly.** Evidence: F6:26,70,207,263,266,277,297,336,359; J5:10923–11074,14647–14663; O8:16–20,48,65–72.

F6 names kqueue notifications plus libproc/sysctl and descriptor census, describes transient/orphan/event-loss/restart gaps, acknowledges an unexpected descendant may already have executed, and routes uncertainty to UNRESOLVED with no terminal release. It explicitly retains refusal of descendant-bearing roots pending Gate 2 proof.

The guard now has an ordinary sandboxed invocation and cannot spawn. The distinct broker is explicitly unsandboxed, SPAWN-only, pre-enrolled from an unrestricted parent, and assigned admission-success-before-payload sequencing. Those are meaningful repairs, subject to F1 and F3.

I found no new default-to-proceed, Intel-idleness prerequisite, science-triggered Intel termination, automatic transfer resume, or claimed native observation proof. C:89,91,117 remain explicit requirements. The unchanged gate pin passes; F2 nevertheless leaves existing dispatch obligations bypassable. Separate commissioning authorization and all **18 parent cases plus 10 subcases UNRUN** are preserved.

Required changes:

R1. Separate the admission subtree from A1 science-descendant enrollment. Freeze a C:115-compliant pre-release mechanism for admission and its non-science helpers, with appropriate types and checks. Where that mechanism is unavailable, explicitly refuse the affected composition; do not label it A1-compliant.

R2. Re-audit the retained no-op roots against their actual callers’ admission/dispatch checks. Restrict direct P1/P3 evaluation or preserve the missing dispatcher obligations. Replace the unsupported empty-obligation claims and add controls for these concrete bypasses.

R3. Resolve every delegation binding reference and enforce its target’s owning profile, launch context and template. Check associated process identities against their invocation bindings. Add isolated foreign-launch delegation-reference controls through the complete production-validation path, then repin and rerun.

| V7 required change | Closure |
|---|---|
| R1 — Pre-release registration or approved amendment | **Partly closed.** A1 approval, quotation and D4 observation specification are supplied; admission-helper exception leakage remains. F1. |
| R2 — Implementable guard composition | **Partly closed.** Ordinary guard and distinct broker repair the original contradiction; admission-subtree registration and delegation-reference validation remain incomplete. F1, F3. |
| R3 — Complete-chain admission audit | **Partly closed.** Direct P2 trainer/evaluator roots are restricted; retained P1/P3 evaluator no-ops omit outer checks. F2. |
| R4 — Representable aggregate receipts | **Closed for the requested static construction.** All 55 aggregates are constructed; 29 TOP_LEVEL receipts have maxima of **36 inputs / 4,271 UTF-8 bytes**, within the frozen 64 / 8,192 / 262,144 bounds. K5:1820–1854. |
| R5 — Operand-aware refusal variants | **Closed for the named source-valid forms.** Coordinator PID/log, coordinator reattempt directory and stage reattempt directory are represented and tested, including arity rejection and propagation. K5:1857–1925. |
| R6 — One authenticated launch context | **Partly closed.** Original substitution control is RED; delegation binding references can still cross launches. F3. |

**What I checked and did not check**

I read V7, D8, relevant C/F6 sections, O8’s documented basis, builder/acceptance records, targeted J5/P3 constructions, inventory claims, checker logic and the relevant launch-source branches. P3 and J5 were searched and read selectively, never in full.

I independently ran the authorized checker with `/usr/bin/python3 -B`:

- Default: **exit 0** — 114 schemas, 17 request kinds, 259 examples, 1,410 hash references, eight binding vectors and 16 observations.
- `--profiles P3`: **exit 0** — 55 profiles, 168 explicit refusals, 729 binding vectors; aggregate bounds above.
- `--mutation-controls`: **exit 0** — **37 intended RED**, comprising 26 preserved and 11 round-8 controls.

These runs establish the supplied static checks’ results. I did not independently repeat MAESTRO’s sandbox positive control/census, recompute every packet digest separately, execute custom mutations, or prove exhaustive launch coverage. No files were edited; no science, native observer, service, transfer or commissioning case ran.