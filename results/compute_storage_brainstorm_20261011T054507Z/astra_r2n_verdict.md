VERDICT: NO-GO

Gate 1 remains OPEN. **V10 R1 is partly closed:** certificate-phase reachability is repaired, but the resulting Git recipes still assume an unenforced six-operand domain and, for profile 38, equality between two independently loaded operand sets. Aliases follow the review packet.

F1. [high] **The verifier can reach more than six distinct Git operands before validating the six-unit invariant.**

Evidence: `experiments/track_c/c10w_oracle_read.py:543–550` loads `eval.json` and probes every entry in its `train_records`. Only afterward, at :551, does `validate_phase` enforce the count and unit identities at :332–333. K8:2516–2522 instead derives six from the constant `TRAIN_UNITS["P2"]`; K8:2570–2573 requires precisely those six indexed recipes. R11B constructs its fixture with that same count at K8:2480–2482.

A source-derived counterexample is a P3 certificate with passing upstream prerequisites and a replication record containing **seven individually valid linked records with distinct, untracked adapter paths**. The seventh Git probe occurs before the phase validator can reject the record. Six immutable bound operands cannot represent those seven distinct invocations.

Consequence: The new branch is recorded, but its error-path invocation domain remains underrepresented. This is a static counterexample, not an executed reproduction. D10 still prevents positive clearance.

F2. [high] **Profile 38’s two admission routes are not established to share the same bound Git recipes.**

Evidence:

- The verifier route takes adapter paths from `eval.json → train_records`: `experiments/track_c/c10w_oracle_read.py:543–550`.
- The gate’s later `phase_trains` route selects available 400/800-step training files and reads their adapter paths independently: `tools/c10w_p2_gate.py:128`; `experiments/track_c/c10w_oracle_read.py:515–520`.
- Neither route establishes equality between those operand sets before its probes.
- P6:462271–462277 records six recipe hashes, with both routes assigned to them at :462300–462304. K8:2575–2577 checks route labels, not operand equality.
- F9:115–117 requires immutable bindings within one launch context.

For example, an evaluation can reference an earlier valid adapter while `phase_trains` selects a later available training record. The two routes then probe different paths. Even with six records per route, their union can exceed six distinct operands.

Consequence: D14’s “one occurrence per identical recipe” rule is sound, but this application has not proved recipe identity. Sharing the executable and command shape does not establish equality of bound arguments.

F3. [note] **The argv-versus-certificate distinction, first-stage exclusion, and origin separation are repaired.**

Evidence: K8:2525–2535 rejects argv-stage filtering for `loaded_data`; K8:2548–2557 checks the first-stage domain and gate:103 text/hash. The source assigns `phase="P2"` before the verifier call at `tools/c10w_p2_gate.py:100–105`. K8:2393–2394 additionally recomputes query hits and whole-source hashes.

J8:10740–10856 retains separate SCIENCE/A1 and ADMISSION/C:115 variants. K8:2371–2379 requires distinct occurrences and preserves science authority. Production validation derives **72 admission-origin occurrences**.

Consequence: The specific V10 argv-filter defect closes. I found no other argv-only exclusion of a loaded-data site in the reviewed trace. F1–F2 concern the data-selected operand domain, not a remaining stage filter.

F4. [note] **R11A–R11C are isolated and fail for their intended reasons; the extracted-body technique is acceptable within its stated static scope.**

Evidence: K8:2606–2617 reloads inputs for each control, synchronizes the two trace copies, and checks the specific failure message. My run observed:

| Control | Intended RED |
|---|---|
| R11A | Loaded-data Git site filtered by argv stage |
| R11B | Missing reachable admission Git occurrence after six mocked probes |
| R11C | First-stage enforcing-line pin missing |

K8:2487–2508 supplies mocked data/reference/authorization functions and replaces both subprocess boundaries. It compiles selected function definitions without importing the science modules. The reviewed bodies perform no file writes or real Git/verifier launches through this harness. Source reads and path resolution still occur; “zero real IO” is broader than the demonstrated boundary.

Consequence: These controls establish their named regressions. R11B does not establish complete input-domain coverage: its six-record fixture and mocked validation leave F1–F2 untested. MAESTRO’s stricter sandbox evidence supports the no-write/no-real-child claim, but I did not independently repeat that sandbox experiment.

F5. [note] **Earlier static closures and the refusal/commissioning boundaries remain preserved.**

Evidence: K8:2186–2205 retains caller-audit checks; :2222–2265 retains same-launch delegation and process-identity checks. The aggregate control remains schema-valid and requires 65 inputs at K8:2033–2048. All **50 preserved controls** remain intended RED.

F9:207,263 preserves composition refusal before release; :209 preserves A1’s narrow exception; :266 preserves unresolved observation gaps; :12,277 preserves Intel-local work and no idle-Intel prerequisite. F9:336,339,359–360, P6:461900,461946 and I8:259–260 correct the certificate-branch absence claim and retain the no-complete-call-graph limitation.

Consequence: V10 F2’s origin split/query recomputation, V8 R2/R3, and earlier R4–R6 remain closed for their previously reviewed static scope. I found no additional C relaxation, default-to-proceed, Intel-dependent ordinary-science wait, or science-triggered Intel termination. Separate commissioning authorization and all **18 parent cases plus 10 subcases UNRUN** remain intact. Those boundaries do not resolve F1–F2.

**Required changes**

R1. Complete the conservative representation of the newly reachable Git operand domain:

- Account for disk-selected `train_records`, including probes occurring before eventual validation failure; do not infer a pre-spawn bound from `TRAIN_UNITS`.
- Keep the verifier and `phase_trains` operand sources distinct unless their exact bound-recipe equality is established before the relevant spawn.
- Add isolated controls for more than six distinct linked adapter paths and for differing operand sets across profile 38’s two routes.
- Correct coverage claims, rebuild bindings/aggregates, repin, and rerun acceptance. Preserve C:85, A1, and D10 refusal; explicitly refuse cases the frozen representation cannot cover.

| Requirement | Closure |
|---|---|
| V10 R1 — Certificate-dependent admission coverage | **Partly closed.** Branch selection, origin authority, exclusion pin and requested control repaired; operand/cardinality coverage remains open under F1–F2. |
| V10 F2 — Origin split and recorded-query recomputation | **Remains closed**, subject to the recorded lexical scope. |
| V8 R2/R3 | **Remain closed** for caller obligations and static delegation/reference checks. |
| Earlier R4–R6 | **Remain closed** for aggregate bounds, operand-aware refusal propagation and launch-context coherence. |

**What I checked and did not check**

I reviewed the relevant contract/decision clauses, predecessor verdict, targeted P6/J8 records, checker paths, and gate/trainer/reader/re-attempt source. P6 and J8 were read selectively.

I independently ran `/usr/bin/python3 -B K8`:

- Default: **exit 0** — 114 schemas, 17 request kinds, 259 examples, 1,411 hash references, eight bindings, 16 observations.
- `--profiles P6`: **exit 0** — 55 profiles, 174 refusals, 797 reconstructed bindings, 13 queries, 72 admission-origin occurrences.
- `--mutation-controls`: **exit 0** — **53 intended RED**.
- Aggregate maxima: TOP_LEVEL **36 inputs / 4,271 bytes**; all-profile **54 / 5,477**.

I made no edits and ran no custom counterexample, science, transfer, native observer or commissioning case. I did not independently reproduce the sandbox/census evidence or separately recompute every packet digest. F1–F2 are source-derived findings; checker GREEN verifies the recorded model, not those omitted cases.

