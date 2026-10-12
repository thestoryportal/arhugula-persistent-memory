VERDICT: NO-GO

Gate 1 remains OPEN. **V9 R1 is partly closed:** the identified verifier/Git misclassifications are repaired, but exclusion of the verifier’s conditional Git descendants rests on an unenforced certificate-phase assumption. Aliases below follow the review packet.

F1. [high] **A P2 launch stage does not establish that its verifier receives a P2 certificate.**

Evidence:

- P5:435424 excludes `verify-preflight → authorized_phase_entry → replication_for → Git` from current P2 admissions. Its Git trace site applies only to `p2-eval`: P5:435375–435397.
- For every non-first stage, the gate loads `preflight.json` without requiring `proof["phase"] == "P2"` before calling the verifier: `tools/c10w_p2_gate.py:100–105`.
- `require_training_preflight` validates provenance and evidence, then forwards that certificate; it does not enforce the expected phase: `experiments/track_c/c10w_oracle_train.py:51–66`.
- The verifier branches on **the certificate’s phase**, independently of the gate’s argv: `experiments/track_c/c10w_oracle_read.py:583–588,531–539`. With a P3 certificate and passing linked prerequisites, `replication_for` reaches the Git probe at :550 → :140 → :133.
- K7 instead filters process sites using the stage taken from argv: K7:2358–2364. Its successful recomputation therefore does not establish the certificate-phase invariant.

A concrete static counterexample is a non-first P2 training admission supplied a P3 certificate with otherwise passing evidence and authorization. Its verifier can reach replication Git before subsequent training checks. No new P3 admission profile is necessary.

**Consequence:** The conditional branch is documented but incompletely represented. D13’s “every process reachable” obligation includes admission error paths; a stage name cannot substitute for an enforced input invariant. This is a source-derived counterexample, **not an executed reproduction or observed bypass**. D10’s composition refusal still prevents positive R2 clearance.

F2. [note] **The explicit origin split and recorded-query machinery substantially repair V9’s demonstrated defect.**

Evidence: J7:10740–10856 requires distinct SCIENCE/A1 and ADMISSION/C:115 child variants. K7:2365–2381 requires separate admission occurrences, preserves shared science occurrences and rejects merged origins. Production validation derives **42 admission-origin occurrences**.

Profile 38’s fingerprint split is correct: the gate occurrence has ADMISSION/C:115 at P5:98480–98486; the evaluator occurrence has SCIENCE/A1 at P5:101047–101053. The corresponding source calls are `tools/c10w_p2_gate.py:69` and `experiments/track_c/c10w_oracle_eval.py:367 → c10w_oracle_step0.py:101`.

The 13 query hit lists and source pins recompute successfully through K7:2389–2402. The recorded queries expose the relevant imported calls and conditional branch. Re-attempt processing returns through the same guard under `A.overlay()`; I found no additional process start in that reviewed path (`tools/c10w_p2_gate.py:135–147`; `tools/c10w_p2_rerun.py:180–197,242–292`). F8:359–360 and P5:435470 retain the lexical limitation.

**Consequence:** This is a reproducible, manually reviewed trace with derived occurrences—not the previous fixed admission-name list. Its remaining defect is the reachability judgment in F1, not a mismatched grep result.

F3. [note] **All four new controls fail for their intended reasons; earlier static protections remain intact.**

Evidence: K7:2439–2458 reloads inputs independently for each control and checks its specific error. My run produced:

| Control | Intended RED observed |
|---|---|
| R10A | Verifier admission occurrence carries A1/science authority |
| R10B | Git admission occurrence carries A1/science authority |
| R10C | Recomputed `starts-train` hit-set mismatch |
| R10D | Verifier admission occurrence missing/merged |

These controls directly exercise `round10_checks`, which production validation invokes at K7:1692. They do not exercise F1’s certificate-dependent reachability.

R8R4’s additional origin fields preserve schema validity; it still constructs exactly 64 bindings and fails because the aggregate requires **65 inputs**: K7:2032–2047. Same-launch delegation resolution and process-identity checks remain at K7:2221–2264. Direct-evaluation restrictions remain at F8:208.

**Consequence:** V8 R2/R3 and earlier R4–R6 remain closed for their previously reviewed static scope. All 55 aggregates validate: TOP_LEVEL maxima **36 inputs / 4,271 bytes**; all-profile maxima **54 / 5,477**, within unchanged bounds.

F4. [note] **The refusal and commissioning boundaries remain preserved.**

Evidence: F8:207,263 retains `NOT_ADMITTED_ADMISSION_HELPER_UNREGISTERED:` and requires refusal before release. F8:209 preserves A1’s narrow authority; :266 retains unresolved observation gaps; :12,277 preserves Intel-local work and no idle-Intel prerequisite. F8:297 separates bounded refusal from cessation. F8:359–360 preserves separate commissioning authorization and all **18 parent cases plus 10 subcases UNRUN**, consistent with C:169–173.

**Consequence:** Apart from F1’s coverage defect, I found no additional C relaxation, default-to-proceed, science wait on idle Intel, science-triggered Intel termination, or operational acceptance claim.

Required changes:

R1. Close the certificate-dependent admission branch. Conservatively represent its reachable Git descendants as ADMISSION_HELPER/C:115 occurrences, preserving separate science uses; alternatively, establish an enforceable invariant that excludes that branch **before it can spawn**, without changing C:85’s gate or widening A1. Add an isolated control covering P2 argv with a P3 certificate and otherwise passing prerequisites. Correct the absence claims, repin, and rerun acceptance. Preserve composition refusal.

| Requirement | Closure |
|---|---|
| V9 R1 — Complete admission-origin audit | **Partly closed.** Explicit verifier/Git branches and origin separation repaired; conditional verifier-descendant coverage remains open under F1. |
| V8 R2 — Preserve caller checks | **Remains closed** for reviewed routes, with recorded lexical limits. |
| V8 R3 — Same-launch delegation references | **Remains closed** for static validation. |
| Earlier R4/R5/R6 | **Remain closed:** aggregate bounds, operand-aware refusals/propagation, and launch-context/reference coherence. |

**What I checked and did not check**

I reviewed contract/decision clauses, relevant predecessor changes, targeted P5/J7 records, checker validation/control paths, and the admission, verifier, evaluator and re-attempt source paths. P5 and J7 were searched selectively.

I independently ran `/usr/bin/python3 -B K7`:

- Default: **exit 0** — 114 schemas, 17 request kinds, 259 examples, 1,411 hash references, eight bindings, 16 observations.
- `--profiles P5`: **exit 0** — 55 profiles, 174 refusals, 737 reconstructed bindings; 13 queries and 42 admission-origin occurrences.
- `--mutation-controls`: **exit 0** — **50 intended RED**, including all 46 preserved controls.

I made no edits and ran no custom counterexample, science, native observer, transfer or commissioning case. I did not independently repeat the sandbox/census proof or separately recompute every packet digest. Checker GREEN establishes the recorded static checks; it does not resolve F1.

