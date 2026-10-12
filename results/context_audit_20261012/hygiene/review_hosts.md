# Host-readiness review

Status: NOT READY for host-lane dispatch/application until RH1–RH2 are resolved. This is a static planner review, not hook/runtime acceptance.

Read coverage: hygiene_planner_brief.md and maestro_synthesis_check.md fully; PLAN.md fully; complete lanes.json parsed, with all host units/allowlists/dependencies examined; all 14 host briefs read in full by complete-file processing. The 196 export unit blocks were compared byte-for-byte against their full authoritative unit fields, and every export header/finish block was compared against the inspected common template. H01-10, H02-13 and H06-30 were also inspected with numbered full-text reads. All 223 lines of host_apply.md were processed: prose inspected, all 204 route/backup/equality/owner rows parsed and checked. No host values, credentials or live hooks were read/executed to manufacture acceptance.

## RH1 — BLOCKER: private C11 transport conflicts with clean-base/CI integration

Evidence: PLAN.md:10–11 seeds complete private external originals and assembles accepted predecessor outputs into the next clean base. briefs/H01-10.md:149–154 puts the complete credential-bearing .codex/config.toml under results/context_audit_20261012/hygiene/host_staging/.codex/config.toml and forbids credential content in commits. lanes.json:7837 (DG6, numbered check 2) requires CI to use integrated host_staging. Current .gitignore has no host_staging exclusion. check_lane.py:108–118 inventories all untracked and ignored files, discarding only the lane dispatch receipt.

Why this blocks: the concrete plan does not specify which staging files enter Git, which remain private, or how the full config travels between bases and into the final bundle. Committing all accepted staging violates C11; carrying private untracked staging into unrelated successor lanes violates their exact allowlists. CI cannot inspect the real full credential-bearing config if it is correctly excluded. General instructions to keep secrets private do not resolve these incompatible artifact paths.

Fix: add an exact MAESTRO-only private-staging protocol. Name .codex/config.toml and any other credential-bearing sources as never-tracked files; name the private storage/transport path and permissions; specify which complete files are reseeded into each lane, freeze their hashes, and exclude those private files from predecessor/integration commits. Separate actual host-config verification from sanitized CI fixtures/nonsecret staging. Require a pre-integration tracked/staged-path check that rejects credential-bearing targets without printing contents. Keep the full proposed file at the mandated worktree staging path while that host lane runs.

## RH2 — BLOCKER: hook behavioral checks lack a permitted, concrete fixture route

Evidence: briefs/H01-10.md:14 says allowed checks use /usr/bin/python3 -B only. D-U2 at :202–209 allows only the CJS wrapper and four receipt files, asks for repository positive/negative emission fixtures, but names no fixture command or fixture source. D-U3 at :214–221 similarly asks for shell-routing/compatibility and payload checks without an executable fixture route. briefs/H02-13.md:143–146 requires wrapper fixtures and zero prompt/session-start graft bytes while prohibiting live hooks. PLAN.md:6 names stdlib checks; its :15 behavioral-RED list omits these hook changes.

Why this blocks: static inspection or a Python rewrite of the same logic cannot establish that the actual staged CJS/shell emits the required bytes or suppresses hook-side graft retrieval. The brief leaves builders to invent an interpreter exception, execute prohibited live behavior, or return UNVERIFIED on a required check. The wrapper unit also has an empty evidence array in lanes.json:4389, so it lacks the exact wrapper/settings source anchors needed to cut the change surgically.

Fix: specify exact isolated fixture commands/interpreters and allowlisted fixture files (or a named receipt-embedded executable fixture), with saved behavioral RED then GREEN. Execute the actual staged wrapper/router using local stub inputs and a fail-on-call graft substitute; cover repo root and worktree suppression, unrelated-repo preservation, SessionStart/UserPromptSubmit and guard behavior. Explicitly permit only those local fixture interpreter calls, forbid real graft/network/live-hook invocation, and attach the relevant CAA:84–88 plus inspected wrapper line anchors to D-U2. Runtime startup qualification remains UNVERIFIED.

## RH3 — MEDIUM: backup/apply sequence does not close the host-write race

Evidence: host_apply.md:8 verifies the live before hash; :9 takes the backup; :11 performs os.replace; :12 checks only staged/applied equality and records receipt fields. No check requires backup bytes/hash to equal the accepted original, and no host-writer reservation or final live identity/hash recheck is named.

Concrete failure: another config/plugin writer can change a target after step 1 but before backup/replace. The backup may contain a different version and os.replace can erase that concurrent change while the final staged/applied equality still passes.

Fix: require backup-bytes/hash equality to the reviewed before receipt, a final target identity/mode/hash check immediately before replace, and explicit serialized/quiescent handling of writers for the affected host target during backup/check/replace. Unexpected changes stop and return to reconciliation. Use private temporary/backup modes before credential bytes are written.

## Verified boundaries

- H-SETTINGS is the sole settings owner; H02-13 depends on D-U2 and stages the complete H/.claude/settings.json at the exact H-stripped route (briefs/H02-13.md:135–146; host_apply.md:221).
- D-U3 stages the full installed LR script at .claude/plugins/cache/promptctl/laws/0.24.1/hooks/scripts/skill-router.sh (briefs/H01-10.md:214–216; host_apply.md:22).
- All 204 host routes and backups equal their exact H-stripped paths; owners agree with authoritative unit files. No same-wave host/repo allowlist overlap was found. Sequential C6/D-U23 and C7/D-U24 ownership is explicit.
- Memento enablement/finalize-session/300000 reset is expressly preserved in every host brief and host_apply.md:14. No disabled-hook recommendation survives as the operating instruction.
- The quoted planner handoff rule is followed by an explicit lane adaptation with a unique handoff path/token. It is verbose but the later adaptation clearly resolves ownership; no parallel handoff collision was found.

No planner/code changes, host writes, Git mutation, network, science, project Python or graft were performed. Only this review artifact was written in this review task.

## Resolution re-review — revised planner

All revised host briefs and authoritative host-unit fields were processed again; their files/checks/evidence and content/finish rules matched. All 204 host application routes still matched exact owners and staging/backup paths, with no same-wave overlaps. The new PRIVACY unit and its complete H03-15 brief were read. PLAN.md was read fully; host_apply.md prose was reread and every route row revalidated.

- RH1: the architectural conflict is addressed by PLAN.md:10–11, briefs/H01-10.md:16–17, host_apply.md:17 and PRIVACY (briefs/H03-15.md:64–67). Complete config/settings stay private, unchanged seeds carry frozen hashes, the authoritative dispatch has a Git-blob receipt, and CI explicitly receives line-covered projections while applied review sees full originals. One concrete exclusion-path defect remains below.
- RH2: fixture files and actual staged-code execution are now authorized in D-U2/D-U3, with isolated Python runners invoking node/bash and saved RED then GREEN (briefs/H01-10.md:206–227). This resolves the earlier missing execution route. One concrete isolation defect remains below; D-U2 still has no wrapper-specific evidence row.
- RH3: resolved at the protocol level by host_apply.md:9. MAESTRO must reserve every cooperating writer throughout backup/check/replace/after-check and stop if any writer cannot participate; live hashes are rechecked after backup and before replace. No actual host application was performed or accepted.

Remaining RH1-A — BLOCKER: the literal “worktree-local .git/info/exclude” route is not real in linked worktrees. PLAN.md:10 and briefs/H03-15.md:64 require it. Cheap read-only probes in this exact linked worktree show .git is a file, not a directory; git rev-parse --git-path info/exclude resolves to /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.git/info/exclude, shared by main and the linked worktrees. Writing <WT>/.git/info/exclude will fail, while treating the actual common-dir file as private misstates its scope. Fix the exact effective exclusion route: either explicitly serialize a MAESTRO-owned common-dir info/exclude update containing only the two scoped staging entries, or specify a genuinely per-worktree exclusion mechanism. Verify effective exclusion with git check-ignore --no-index before seeding. Keep builders prohibited from Git metadata mutation.

Remaining RH2-A — BLOCKER: fake HOME plus a graft-subprocess stub does not isolate the actual current CJS wrapper. The complete original wrapper was read only: /Users/robertrhu/.claude/helpers/graft-hooks.cjs:7 defines an absolute real BAKED graft directory; :58 selects it before fake-home package routes; :67 dynamically imports its hooks.js. D-U2's new check (briefs/H01-10.md:211) only names a graft subprocess stub. The required original behavioral RED can therefore import and execute installed graft code, even in a fake home; npm fallback at wrapper:20 is another external route. Specify an explicit loader/filesystem/package-resolution boundary stub for the baked/module-import paths plus all subprocess calls. Execute the unchanged staged wrapper against a local fake hooks module with marker output, assert no real installed graft module is imported, and keep npm/graft/network calls forbidden. Add wrapper:7,20,58,67 and CAA:84–85 as exact evidence anchors.

Current verdict: two narrow blockers remain (RH1-A, RH2-A); the former broad privacy/fixture/apply concerns have concrete fixes apart from these details. Complete staging, settings ownership, LR path, Memento/finalize-session preservation and lane handoff ownership remain verified at the planner level. Only this review file was appended; no live wrapper, hook, host-write or Git mutation occurred.

## Final narrow resolution

RH1-A — RESOLVED in the plan. PLAN.md:10 and PRIVACY's numbered check 1 (briefs/H03-15.md:64) now resolve the effective exclusion file with git rev-parse --git-path info/exclude, explicitly identify linked-worktree common-dir sharing, require MAESTRO to serialize existing writers/preserve existing bytes/add only the two scoped entries, and require effective git check-ignore --no-index in every worktree before private seeding. Builders retain no Git-metadata mutation authority. The invalid worktree-local claim is absent from current PLAN/host_apply/lane briefs.

RH2-A — RESOLVED in the plan. D-U2's numbered check 3 (briefs/H01-10.md:212) requires filesystem/module/child-process boundary isolation BEFORE ANY baseline, including BAKED :7, resolution precedence :58, dynamic import :67, package probes and npm fallback. Only the fixture hooks.js may import; the unrelated-repo marker and zero real installed graft import/subprocess assertions are explicit. The actual wrapper bytes must execute under those stubs, including RED; fake HOME alone is expressly insufficient. The named runner remains in the lane allowlist and unit checks match the authoritative JSON.

Final host-plan verdict: no remaining blocker in the reviewed host scope. RH1/RH2/RH3 are resolved at the specification/protocol level. This does not accept an implemented fixture, dispatch exclusion, live hook, host copy or runtime behavior; those still require the saved lane receipts and MAESTRO's actual application checks. Memento/finalize-session preservation and all prior verified host-route boundaries remain binding. This re-review appended only review_hosts.md and performed no host/Git mutation or wrapper execution.
