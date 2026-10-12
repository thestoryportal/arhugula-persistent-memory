# Adversarial execution-plan review

Status: NEEDS CORRECTION before builder dispatch. This is a static plan review, not binding Astra acceptance or executed hygiene evidence.

Reviewed current `lanes.json` and `export_candidates.json` completely with stdlib JSON parsing and full-record structural checks; read `PLAN.md` in full. Every brief was read by the structural consistency probe and every declared unit check/file/dependency was compared with its brief. Semantic inspection prioritized all I/DG/P14 sections, D-U12/13/14/15/16/19, the complete common instruction/finish text, and selected export sections. This does not claim a line-by-line semantic review of every remaining N-unit narrative. Existing renderer and closeout source were read where needed to test the execution contracts. No host contents containing secrets were copied into this review.

## Verified structure

- SYNTHESIS §3 contains 119 source rows, including E(n,s); all 119 IDs occur once among 327 unique planned units. The additional units are 196 concrete E units and 12 added repair/guard owners.
- 33 lanes own every unit exactly once; no missing dependency, cycle, later-wave dependency, or same-wave dependency on a different lane was found. Same-lane dependencies precede their consumers.
- Per-unit estimates are positive and ≤8 minutes. Each lane's recorded total equals the sum of its units and is ≤36 minutes, leaving the declared four-minute finish reserve within 40. This verifies arithmetic, not empirical completion time.
- Same-wave lane allowlists are pairwise disjoint. Each equals its units' exact file sets plus its one unique handoff. No wildcard export allowance was found.
- All 196 export IDs match export_candidates exactly: 132 S2 and 64 S3. Every host path, H-relative staging path and unit edit path agrees. The earlier audit census drift is carried as P14; the original eleven S3-only imports and their new twelfth provisional source remain preserved.
- I-GIT is the sole Git-index owner after all note owners/imports; I-CACHE alone owns both cache indexes after all 196 exports; DG-INDEX-PINS follows the index owner. P12/P13 target imports precede repairs, and N27 also depends on P10.
- Enabled project-local Memento is explicitly preserved, including finalize-session and the ceiling. Snapshot pins are explicitly provenance; dispatch hashes govern predecessor-owned files, so stale planning pins are not themselves a defect.

## Findings

### R1 — test-only lanes cannot satisfy their own completion contract (P1)

`briefs/H05-17.md:65–76` gives I-SYNCa only `tests/test_context_memory_sync.py` plus receipts, but :74 explicitly requires “Saved fixture behavioral RED then GREEN.” Its implementation I-SYNCb is in wave 7, while this lane is wave 5. The builder cannot make the new production behavior GREEN within its allowlist. Separately, H05-17 ends at :111 with “RED/denied/unresolved check means BLOCKED, not READY”; the same finish text appears at H01-09:184, H04-16, and H08-32:147 despite their DG1/DG4/DG7 units intentionally ending with saved behavioral RED for later implementers. H05-17 also owns D-U13a, whose renderer repair occurs in wave 6.

Consequence: a conforming test author reports BLOCKED, or weakens tests/edits implementation early to earn READY. The dependency graph is acyclic but the acceptance workflow cannot advance as written.

Correction: define test-author completion as saved, justified intended-RED assertions against a runnable baseline, with static checker/fixture harness health GREEN; explicitly permit that artifact to be READY. Reserve production behavioral GREEN for the named later implementation owner. Remove I-SYNCa's within-unit GREEN requirement and distinguish expected RED receipts from unexpected verification failures in every affected finish block.

### R2 — DG1 has no runnable baseline for the required behavioral RED (P1)

The read-only existence probe confirms `tools/context_hygiene_guard.py`, its policy, and its test file do not exist in the current tree. DG1 can write only the new test file and receipts. `briefs/H01-09.md:172` explicitly rejects dependency/import/syntax failures as behavioral RED; DG1's fixture contract calls the future production CLI, and DG3 creates that CLI only in wave 3. A missing script or missing policy cannot exercise the active-versus-dated-history behavior. This is independent of R1's completion wording.

Correction: authorize a minimal runnable baseline/interface owner before DG1 or co-locate a narrowly scoped baseline CLI stub with DG1 after writing its tests. Freeze what counts as the intended semantic failure; prove a valid baseline case reaches an assertion and that the saved RED is the missing guard behavior. Do not accept a fixture-only reimplementation as production behavioral evidence. D-U13a should similarly exercise the existing renderer's actual output rather than treating absent `render_view`/`--destination` API errors as semantic RED.

### R3 — source-state editors lack the concrete evidence their checks promise (P1)

D-U12a, D-U12b, D-U12c and D-U14 all have empty `evidence` arrays in lanes.json. Their briefs nevertheless say “exact evidence anchors below” (`H02-11:277`, `H03-14:153`, `H04-16:60`, `H01-08:105`), and no anchors follow those sections. D-U14 authorizes a historical destination but never fixes an exact source span/JSON-field list. The concrete CAF stale source-state receipts are instead attached to D-U19 (`audit_caf_anchor_docs.md:59–66`), whose edit set excludes docs/program_state.json and whose wave is after all three source-edit owners.

Consequence: source owners must reconstruct what to change/archive from abbreviated synthesis rows, while the later renderer owner discovers unresolved stale source values and cannot repair them. The current plan does not specify a byte-complete archival baseline for the strings the source owners remove.

Correction: attach CAF:59–66 and their cited authority to the corresponding D-U12 owners; specify exact JSON fields and the preserve/correct checks for each. D-U14 should preserve the entire frozen pre-edit docs/program_state.json bytes or an exact enumerated field/span set with its source hash, byte count and resolving pointer. D-U19 then checks corrected source semantics and renders its owned views without inheriting source-edit instructions outside its allowlist.

### R4 — complete private host staging and CI-required staging have no safe common representation (P1)

`PLAN.md:10` seeds complete external originals privately; :34 and `host_apply.md:12–16` require byte-exact application and no secrets in Git/review packets. CAB:115 records a per-user credential in the global configuration (name only; no value read here). DG2's scan set includes global program-state/config/hooks, DG5 fails on absent expected files, but `briefs/H08-32.md:122` requires CI to use the integrated host_staging and exact reviewed manifest. The plan assigns no owner or schema for a publishable sanitized CI snapshot, no explicit exclusion/projection rule for private config, and no transport for the private complete file to CI.

Consequence: CI either receives credential-bearing complete configuration, loses required inputs and fails closed, or silently verifies a different bundle. “Private” plus “integrated host_staging” is not an implementable data-flow contract.

Correction: keep complete application staging and hashes private. Name a separate exact CI-safe bundle or deterministic projected instruction snapshot with a schema, owner, paths, provenance/equivalence checks and fail-closed semantics. Make staged CI/precommit inputs explicit and keep applied-mode verification on the complete real host as the separate required final check. Do not place secret values in the published policy or fixture bundle, and do not treat a redacted projection as proof of full host-byte equality.

## Guard and scope observations

DG1–DG5 do carry the requested retired-role/default/pin values, five active hazards, exact dated-history exemptions, fail-closed observation rules, same-name approved hash-pair policy and body-link controls (wiki, inline Markdown, reference Markdown and explicit Git sources). DG6 specifies pre-commit/CI integration; DG7/DG8 add a named closeout report while preserving advisory memory WARN and scientific gates. These are implementation requirements, not current acceptance. R1/R2 prevent the specified test-first sequence from establishing them as written; R4 prevents durable CI verification of the declared host scope.

No additional graph, index-owner or wildcard defect was found. Review did not execute future guard/renderer/sync code, CI, host application, merge, or science. No source artifact was edited; only this report was created.

Context directive for every successor: start new work only at ≥60% remaining; MAESTRO watches each team session and sends stop at 45%; then or on any compaction stop starting work, preserve done/in-flight/remaining with exact paths/risks, and use a fresh successor by ≤40%. Review complete; corrections belong to the planner owner.

## Reviewed snapshot identities

- lanes.json: 0db74ab3fc7d7bd3493bb2b97c97aee4bed81e5c6af2d556ff88f937ceba5746 (1151339 bytes).
- PLAN.md: ff271057079eda9d28f8e27dbe4b398296474bb55c91f28a5b8b8bcfc06aedd8 (5789 bytes).
- export_candidates.json: b3866e8bfb63dc18d2b2724fd2276910df52b87fc058acc7d810dba92f65b839 (119926 bytes).

## Resolution recheck of revised plan

Recheck of revised unit contracts and corresponding brief sections; source identities below define this observation. Current plan has 328 unique units in 33 lanes. Rechecked estimate totals, dependency waves/order and same-wave allowlist disjointness: zero structural failures. The 196 export candidate set remains unchanged.

- **R1 RESOLVED at plan level.** I-SYNCa now saves intended behavioral RED and explicitly assigns GREEN to I-SYNCb. Expected-RED owners can be READY with saved verified intended failures plus static scope checks; finish text distinguishes unexpected RED. H05-17:78,118 and H01-09's DG1 expected-RED paragraph carry this boundary.
- **R2 RESOLVED for the new guard baseline.** DG1's exact edit set now includes tools/context_hygiene_guard.py; checks require tests FIRST, then an actual minimal nonenforcing CLI stub, then saved failures on intended missed violations. It is explicitly unqualified and absent from hooks/CI until DG3 repairs it. Renderer test author still needs a behavioral assertion against existing output rather than an absent new API; this is an execution verification item, not evidence that a test already passes.
- **R4 RESOLVED at plan level.** PRIVACY owns exactly ci_host_projection.json plus receipts after C11/H-SETTINGS. Its schema assigns every source line retained text or approved secret-only redaction; full-source hashes and coverage are required, and guidance cannot be hidden by redaction. DG4/DG5 require coverage/hash negative controls and labeled CONFIG PROJECTION scope; I-MANIFEST carries the exact projection path and private hashes. DG3 classifies staged files by logical H-relative instruction path before historical results exemptions. Applied mode reads complete actual originals, preserving the separate host-byte acceptance boundary. This design is not yet executed or qualified.
- **R3 PARTIALLY RESOLVED; two corrections remain.** Exact top-level field ownership is now specified for D-U12a (updated/current_latest), D-U12b (next_actions), and D-U12c (f1_verdict/scorecard), with work_queue/concurrent holds protected. D-U14 now names the complete original JSON and original generated spans rather than an undefined selection. However, H01-08:107 asks for `GENERATED:PROGRAM_STATE` in all five files: that exact marker does not exist. Existing spans are `<!-- BEGIN GENERATED:program-state -->` through the matching END marker in SESSION_BOOTSTRAP.md, SESSION_CHECKPOINT.md, EXPERIMENT_RUNBOOK.md and README.md; PROGRESS.md uses `<!-- BEGIN GENERATED:f1-scorecard -->` through its matching END marker. Correct the mapping before the archival owner runs. Also, all four source/history units presently receive only CAF:60 and CAF:66; D-U12b still lacks action-specific CAF:61–65 (CLT block, old queue branches, consumed NEW-1, R2 host plan, reviewer fallback). Attach those exact receipts to that owner so its action review has the promised evidence rather than inheriting it only at D-U19.

Remaining dispatch blockers in this snapshot: R3 exact marker mapping and action-specific source evidence. Only review_plan.md was updated. Preserve the ≥60% new-work / 45% watcher stop / ≤40% successor-or-compaction directive above.

Recheck snapshot identities:
- lanes.json: 6b0252c8141026bed9f17f8cb5f435befb40cc0775c3bbf21181078924a8eeb3.
- PLAN.md: cbfde6ba43d94d168ed186ef20dc62429c3ead6dd5d2dd614325f42287200b62.
- export_candidates.json: b3866e8bfb63dc18d2b2724fd2276910df52b87fc058acc7d810dba92f65b839.

## Final narrow resolution

R3 RESOLVED at plan level. Re-read D-U12a/b/c and D-U14 in the current authoritative JSON and verified their checks appear verbatim (lane placeholder expanded) in their corresponding briefs. All four now include the complete CAF:60–66 receipts. D-U14 names the exact case-sensitive BEGIN/END program-state pair for SESSION_BOOTSTRAP, SESSION_CHECKPOINT, EXPERIMENT_RUNBOOK and README, and f1-scorecard for PROGRESS. Missing/duplicate markers are explicitly BLOCKED; exact byte/hash/length round-trip preservation is required; unrelated tails cannot be relocated. Narrow assertions passed.

All four findings in this review are now resolved in the execution-plan contracts. No remaining blocker from this scoped review. This is plan-level resolution only: future builder RED/GREEN receipts, host application, CI, binding Astra acceptance and integration remain required and unexecuted here. No broad sweep was repeated; the planner's latest structural verifier result is not independently reasserted by this narrow pass. Only review_plan.md was appended.

Final narrow snapshot identities:
- lanes.json: 07a97dda4dedb998610b44ba359071c988e2a5778df69d48c3af5c8752071757.
- PLAN.md: 448c7b35fdec3b43af216ba17009f8cdfe5673c5ea42c32f6a24e9156e08f4c5.
- export_candidates.json: b3866e8bfb63dc18d2b2724fd2276910df52b87fc058acc7d810dba92f65b839.
