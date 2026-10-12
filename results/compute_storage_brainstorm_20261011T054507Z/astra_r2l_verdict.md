VERDICT: NO-GO

Gate 1 remains OPEN. R2 and R3 close for the reviewed static scope; R1 still misses admission-spawned verification processes. Aliases below are those in the request.

F1. [high] **The admission subtree still contains recipes labelled as A1 science descendants.**

Evidence:

- The gate calls `T.require_training_preflight` at `tools/c10w_p2_gate.py:105`. That function spawns `c10w_oracle_read.py verify-preflight` at `experiments/track_c/c10w_oracle_train.py:65–66`.
- For evaluation, the gate also calls `R.phase_trains` at `tools/c10w_p2_gate.py:128`. This reaches `require_untracked_adapter` and spawns `/usr/bin/git ls-files` at `experiments/track_c/c10w_oracle_read.py:513–520,130–140`.
- Profile 38’s admission is the `p2-eval` gate: P4:102666–102672. Its reader-verifier recipe remains `SCIENCE_CHILD`, `DECLARED_AT_ROOT_ADMISSION`, `D-R2C-A1`: P4:99313–99320,99525–99529. Its Git recipes retain the same science authority: P4:97072–97081,97182–97186.
- K6’s admission-name set contains only gate/fingerprint/ps/env/tmux: K6:2123–2127,2141–2145. P4’s admission source audit likewise omits the imported verifier and Git branches: P4:374746–374761.

These processes can originate inside admission **before the payload root exists**. A recipe’s legitimate use later by science does not authorize its admission-origin execution under A1. D9:9 expressly excludes every admission-spawned process.

**Consequence:** The new role and refusal repair are substantial, but the claim that the entire admission subtree has been separated from A1 remains false. Profile 38 is explicitly refused at P4:103768, so this is a frozen classification/coverage defect, **not an observed executable bypass**. Blanket composition refusal does not make the remaining A1 labels faithful to D10.

F2. [note] **The concrete direct-evaluation bypasses are repaired; caller-search completeness remains bounded by the recorded lexical queries.**

Evidence: P4:4897–4905,12354–12362 makes direct P1/P3 evaluation CHILD_ONLY under the corresponding dispatcher. The dispatcher performs projection before evaluation at `experiments/track_c/c10w_oracle_step0.py:411–415`. Direct preflight/freeze restrictions retain the exclusive-log obligation identified at that file’s :294–299; F7:208 and I6:259 record those restrictions.

The 25 retained no-op audits cover wordlist, dispatcher variants and their generic wrappers. The wrapper checks at `tools/run_c10w_stage.sh:3–15`, P2-only reachability at `tools/run_c10w_p2_stage.sh:9,34`, and audit classifications at P4:372285–372541 support the retained routes. I found no additional skipped admission check in those routes.

K6 reproduces the recorded `.py`/`.sh` basename hit sets across the seven named directories: K6:2174–2210. This is not a complete call graph: for example, the module import and `S.dispatch_stage("p2-eval")` at `tools/c10w_p2_rerun.py:313–324` escape the `.py` basename query. That particular route reaches an already restricted P2 variant. F7:208 correctly separates search reproducibility from semantic judgment.

**Consequence:** V8’s demonstrated P1/P3 bypass closes. Do not interpret the reproducible hit lists as exhaustive discovery of every possible calling mechanism.

F3. [note] **Delegation references now receive the required ownership and identity checks through production validation.**

Evidence: K6:2221–2238 requires unique resolution, matching profile/context/template and owning production-tree prefix. K6:2240–2264 checks associated broker/enrollment executable, argv, invocation-template hash and host/boot identities. K6:1688–1700 invokes these checks and the construction reference-coherence validator from `--profiles`.

The foreign payload and admission controls traverse `check()` and `validate_profiles()` with repinned in-memory bytes: K6:2274–2277,2314–2326. Both independently failed with their respective foreign-reference reasons. Using profile 003’s payload binding for the admission substitution is disclosed and exercises the forbidden reference.

**Consequence:** V8’s foreign-launch delegation counterexample is rejected. Earlier R6’s remaining reference-coherence gap closes for this static construction.

F4. [note] **The refusal and commissioning boundaries remain intact.**

Evidence: F7:207,263 refuses helper-bearing admission compositions; J6:15104 refuses the synthetic gate composition. F7:207 presents AUTH_EXEC only as an unestablished candidate requiring entitlement, Gate 2 proof and separate review. F7:209 retains A1’s approved limits; :266 retains observation uncertainty and refusal pending hardware proof.

F7:12,277,297,336,359 preserves Intel-local work, no idle-Intel prerequisite, bounded refusal, separate commissioning authorization and all **18 parent cases plus 10 subcases UNRUN**.

**Consequence:** Apart from F1’s application defect, I found no additional amendment to C, default-to-proceed, science wait on idle Intel, science-triggered Intel termination or operational acceptance claim.

Required changes:

R1. Complete the admission audit through imported functions and their spawned processes, including `verify-preflight` and the evaluation Git probes. Represent admission-origin occurrences under C:115 without A1 authority; distinguish legitimate science-origin uses of the same recipes. Preserve composition refusal. Add targeted controls for both omitted branches so the current misclassification fails for its own reason, then repin and rerun acceptance.

| V8 requirement | Closure |
|---|---|
| R1 — Admission subtree outside A1 | **Partly closed.** Explicit refusals and separate helper types exist; verifier/Git admission branches remain misclassified. F1. |
| R2 — Preserve actual caller checks | **Closed for the reviewed retained routes and concrete bypasses.** Search coverage has the lexical limits stated in F2. |
| R3 — Same-launch delegation references | **Closed for static validation.** Unique target resolution, ownership/template checks and isolated production-path controls pass. F3. |

Earlier **R4 and R5 remain closed**: all 55 aggregates are constructed; the 25 TOP_LEVEL maxima remain **36 inputs / 4,271 UTF-8 bytes**, within frozen bounds. Operand-aware refusal and propagation controls remain RED as intended. Earlier **R6’s residual defect closes through R3**.

**What I checked and did not check**

I traced the relevant contract/freeze/decision clauses, targeted P4/J6 records, checker paths, caller audits and source branches. P4 and J6 were searched selectively, never read in full.

I independently ran `/usr/bin/python3 -B K6`:

- Default: **exit 0** — 114 schemas, 17 request kinds, 259 examples, 1,411 hash references, eight bindings and 16 observations.
- `--profiles P4`: **exit 0** — 55 profiles, 174 explicit refusals, 725 reconstructed bindings.
- `--mutation-controls`: **exit 0** — **46 intended RED**, including both foreign-reference controls.

Those results do not cover F1’s omitted branches. I made no edits or custom mutations and ran no science, native observer, service, transfer or commissioning case. I did not independently repeat the sandbox/census proof or separately recompute every packet digest.

