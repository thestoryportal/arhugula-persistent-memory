# R2Q context handoff — resume, do not restart

State: test-first R1–R4 checks written and their intended RED outputs saved. Artifact construction has NOT begun. No acceptance GREEN, commissioning, science, launches, commits, graft, web, uv, project Python or input edits occurred. This handoff is separate from the eventual ≤50-line report and all tested subjects.

## Binding context and scope

User's R2Q brief remains authority: read V6 in full first, DR in full second; DR D1/D2/D3 are binding, do not reopen. Worktree is `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`, branch `worktree-c10k-route-a`. B is `results/compute_storage_brainstorm_20261011T054507Z`. Read discipline: never output whole P/J/K; locate with rg, read ≤40-line sed spans or short system-Python summaries. Use `/usr/bin/python3 -B`, prefix shell calls `/opt/homebrew/bin/rtk proxy`; no real launches or commits. New subjects only, copy original input before editing by script.

**Context directive survives this handoff:** check Context N% left after each step; at 45% left or any Context compacted, stop starting work, write B/r2q_handoff.md outside report/tested subjects with done/in-flight/exact paths/next step/risks, reply R2Q HANDOFF. Project directive also says start new pieces only ≥60% left, never approach compaction; successor must retain this directive.

## Files and verified state

- B/check_r2_schemas_v4.py: copied K3 then edited by scripts; INCOMPLETE, syntax validated with compile() (no pyc), sha256 `821e635caa8e979238373a502e82fd10385627d1851216ecaac8ee698a19fe72`.
- B/r2q_test_first_red.log: contains initial diagnostics and final R1–R4 run commands/results, sha256 `e757a49d93cf783500a6156f29bafffd0227957a1cb3eb5d7086b2f6a6ebb7bb`.
- F5/J4/P2/I4/r2q_report.md do NOT yet exist.
- Temporary edit scripts available: `/private/tmp/r2q_edit_checker.py`, `/private/tmp/r2q_new_checks.txt`. Do not reapply the first script to already modified K4; it expects K3 layout. All new check functions are already inserted in K4.
- No relevant memory registry entry used. A read-only helper source audit completed; its findings are preserved below.

Final test-first outputs (all exit 1, against F4/J3/P, before F5/J4/P2 construction):
```
R1: FAIL: R1 guard composition mismatch: profile 0
R2: FAIL: R2 P2 inner launcher must be CHILD_ONLY under gated wrapper: profile 22
R3: FAIL: R3 science child role permits non-science authority
R4: FAIL: R4 P3 replication Git profile missing: profile 1 adapter 0
```
Commands are in RED log; K4 supports `--required-check R1|R2|R3|R4` with explicit old --freeze/--schemas/--profiles paths.

Inputs rehashed after RED; unchanged from session start:
```
F4 19f24124392fd96ec74f5668cd6dcf23c67f4257af90cfec12e8dabe3c9b42c1
J3 e8ed7828c09b9b04eaddad3c82a1f5f48672ef7c36ff0380aa3bc5ede8d29a6f
K3 6427223c840d8594e9497c226df5987979b8e653d4a3801d6fa3c71f5d6ffb78
P  fed7dd8a8d7e0c399feebe984381e0026cbe0e64e283f6a20c606d7a36162cce
I3 a0600f91b0f84b346bfa61267b8ab4a2df4e8b5134c316723d15cf1e9aca8726
DR 3c9d540209b335f96d4a4942ad7071b7c658a0cc41abc9a609de23c55edd6813
C  25c93f5f584d5a1dfff3b0610b32922a289be6d91449765862de3331334062f1
V6 19ff2b74d242d7995f2d89ca64a790fc2899f649faa6e885f72dc01b97fcf1c2
```

## Next step — construct the copied artifacts to the existing RED checks

First copy F4→F5, J3→J4, P→P2 (I3→I4 only for changed facts). Then script edits; preserve all existing checks. K4 defaults now point to F5/J4/P2. Finish construction and full acceptance, then report ≤50 lines and exact READY token. K4 is a working draft, not a finished acceptance checker; assess the decisions encoded below against the brief before construction, particularly actual source-derived binding values.

### K4 implemented interfaces and remaining construction

- `required_r1`: guard `/invocation` argv matches canonical J3 guard; payload differs; launch_id/self_sha256 exact declarations; owning declaration union; every production template has an external InvocationBinding. P2 expects `x-construction.status=SYNTHETIC_BINDING_VECTORS_NOT_RUN_AUTHORITY`, `examples` dict with `ProductionLaunchProfile%03d` copies plus ScienceLaunchContextRecord/InvocationBinding examples. It merges those into J4 construction to rerender. No live launch IDs or authority implied. Need create vectors for each template including literals and children, using exact source declarations.
- `required_r2`: each profile has `admission_scope`, `admission_parent`, `admission_citation`. Parent is null for TOP_LEVEL or object `{entrypoint, payload_argv}` for CHILD_ONLY. CHILD_ONLY parents must declare exact payload invocation; unprofiled parent must have DR D1 refusal. Suggested schema: add required fields to all LaunchProfile variants; allow null existing_admission for CHILD_ONLY to inherit admission (avoid child true stand-ins). Sources/shape decisions still need grounded review. K4 currently requires citations containing I4 names, so I4 will be needed if I3's admission/guard/enrollment claims change.
- `required_r3`: science child roles exactly SCIENCE_PAYLOAD/SCIENCE_CHILD; enrollment const DECLARED_AT_ROOT_ADMISSION; no AUTHORITY_WRITE. Process science branch omits sandbox_profile_sha256, requires `science_invocation_profile_sha256`; ordinary branch retains nonnull sandbox hash. Add science payload Process fixture and a standalone ScienceInvocationProfile example referenced by its canonical hash. Existing ProcessScience is GUARD, should retain ordinary sandbox (guard is infrastructure, not unsandboxed payload). Include reference in observation/population fixtures and reseal aliases and reference targets; do not silently exempt GUARD.
- `required_r4`: six replication Git children for each affected profile, original environment, declared-tree enrollment for all science children. Complete ancestry/adapters beyond mere six-token presence if needed, do not loosen check to fit.
- `production_coherence`: R4/R1/R2/R3, all merged example shape/declaration/binding checks, production dependency-file bytes, closed env names, D1 refusal rationale and refused-child parent rejection. It currently matches unqualified DR-refused paths, not qualified argv refusal semantics; tighten if applicable. Production guard binary is not installed; do not misrepresent J3's synthetic guard hash as a verified native binary. Freeze must keep Gate 2 provisioning identity and host evidence UNVERIFIED while vectors use clearly synthetic guard bytes/identities.
- `freeze_hash_obligations`: parses new normative §4 rows `| hash obligation | `SchemaName` ... | `/pointer` ... | ... |`, expanding array `/*` from schema maxItems (recursing refs/unions). Mandatory manifest must cover derived set; no manifest drives obligation selection. Construct these rows from F4's stated bindings, including request/response fields and Process science profile. Group schemas with equal pointer sets to fit ≤360 lines. Do not simply copy manifest as authority. Need review completeness (F4 record/profile and request binding rows are :86–139 and :141–155). Current equality is schema-set plus required pointer coverage, preserving existing concrete reference checks.
- QUERY observation_revisions now validates QUERYSuccessResponse/body/observation against c.transitions.QUERY.before, then skips validating stored earlier last-decision proof (correct distinction).
- Old mutation controls rewritten with MemoryPath/read_text/read_bytes and sealed_memory; no tempfile import/calls or disk creation. Controls M1–M12, E3/E5/E4S/E4A/E4C/E4N/E4F/E4B retained; R1/R2/R3/R4/R6Q/R6H added. Fresh in-memory bundle per control, schema pin updated through computed shasum; R6H removes CheckpointRecord manifest pointer and exactly its root reference. Default controls run all CONTROL_MESSAGES, check positive base/profiles first. NOT run yet: may need repair intended-failure ordering without weakening checks.

### Admission audit — all 49 true entries, source facts

P contains 55 profiles: true49 = wordlist1 + trainer2 + eval4 + step0(18 dispatch+freeze)19 + inner-stage18 + rerun5; 6 gated P2 wrappers.
- Wordlist idx0: no separate prescreen in I3:153. Train idx1/2: I3:157–158, train.py:255–268 direct run_attempt. Eval idx3–6: I3:159–162, eval.py:474–487 direct run_eval. These support true, not scientific run authorization.
- Non-P2 step0 idx7,9,11,13,15,17,19,39,41,43,45,47: step0.py:436–449 direct dispatch, no separate executable admission. Freeze idx49 same direct main.
- Non-P2 inner-stage idx8,10,12,14,16,18,20,40,42,44,46,48: stage.sh:3–15 solely argv/env validation then exec, no separate executable pre-screen. Can retain true with exact cited absence evidence.
- P2 inner-stage idx22,25,28,31,34,37: CHILD_ONLY under matching gated p2 wrapper. P2 step0 idx21,24,27,30,33,36: CHILD_ONLY under matching inner-stage. P2 wrappers idx23,26,29,32,35,38: CHILD_ONLY under run_c10w_p2.sh (wrapper source:6 single-coordinator mandate), keep actual c10w_p2_gate.py invocation. Coordinator is P.not_admitted[27]; recipes therefore have no admitted root route. This is ancestor restriction, not a claim the wrapper launches its coordinator as child.
- Rerun idx50–52 prepare/archive/verify: main:295–303 no separate admission. Claim idx53 CHILD_ONLY under refused reattempt wrapper (claim_reattempt:200–208 gate-record checks). Read idx54: main:307 verify_claim then disk reader:328–332; retain actual internal checks and cite :295 and :307, no new executable prescreen.
- No production child matched any of 154 unqualified refused entrypoints in the audit. Qualified late-bound refusals must match argv, never basename alone.
- Rename every RETIRED_NOT_ADMITTED prefix to NOT_ADMITTED_NO_PROFILE, cite DR D1; authoritative activity is planning-only re-test, no currently active/pending C10W run. Parent containing a refused descendant is not admitted. Do not reopen D1.

### R4 source trace and exact missing profiles

Affected original P indices: 1,2,6,39,40,41,42,43,44,45,46. Direct trainer phase may be P3; P3 eval and P3 dispatch/stage all reach replication.
- train:65–66 → reader verify-preflight:583–588 → authorized_phase_entry:531–539 → replication_for:542–550 → adapter_is_tracked:130–135.
- step0 ensure_authorized:343–350 and dispatch:375 reach replication directly; :384–386 verifier reaches it too.
- Six `/usr/bin/git` child invocations: `["ls-files","--error-unmatch","--",{"$bind":"replication_p2_adapter_relative_i"}]`, i=0..5. Declaration source `ScienceLaunchContextRecord /values/replication_p2_adapter_relative_i`; supplier is latest P2 eval.json train_records[i].adapter.path, verified record identity, worktree-relative. Original environment HF_HUB_OFFLINE=1 with NO LLMDB_DEVICE; reuse P6 children[2] Git skeleton (not disk_p* probes, whose later environment is OFFLINE=0/DEVICE=mps).
- P2 adapter stems in selected P2 directory's adapters/: A7_coined_coined_s1_r16, A7_shuf_s1_r16, A7_canon_s1_r16, A1_single_s1_r16, A7_coined_coined_s0_r16_rt, A7_shuf_s0_r16_rt; attempt may append _retry800 then .safetensors. Source reader:24–34,288–290 and train:234. Do not fabricate live adapter values; use labeled synthetic binding vectors while freezing actual supplier obligations.
- All 11 profiles already pin reader source in payload dependencies. Computed /usr/bin/git hash: b8763cf250e607a778bb4603cecb5b90338814d0a3dfcba0d57b1de242f610e9 (recompute before writing, never hand-type).
- Existing trees already declare gate/fingerprint/ps/env/tmux and shell dirname/mkdir/date plus trainer/verifier. No extra subprocess in engine_fingerprint/c10l_mint_lib/c10e_bandknob/c10p_twopass_arms source census. Repeated identical Git execution can reconcile against same registered recipe; no broker science spawn allowed by D3.

## Acceptance still pending

Run exact defaults, --profiles P2 and --mutation-controls; log exit0/GREEN and every intended RED. Run controls under a real read-only sandbox if sandbox-exec available; cheap probe before saying unavailable. Show filesystem before/after equivalent to find TMPDIR-newer-brief count, control itself must create no file/directory. Recompute J4/P2 and interface/runtime pins via shasum (K4 --print-hashes available); F5 pins both files and §9 maps V6 R1–R6 to closing lines. Preserve separate Gate 2 authorization, 18 parent+10 subcase UNRUN, no Intel science wait/termination/default-to-proceed/automatic resume. Rehash all inputs, write ≤50-line report with computed subjects SHA256, closures, RED and exact acceptance outputs; final exact READY token only when all requirements hold.
