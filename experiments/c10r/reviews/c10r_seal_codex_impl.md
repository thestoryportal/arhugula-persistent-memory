# D-C10r-seal v13 implementation report

**Implementation written; launch verdict: FIX-FIRST / DO NOT RELAUNCH.** The required no-model probe record is **FAIL**: 6 of 45 checks passed and 39 failed. Twenty stdlib contract tests passed inside the first check. No Codex PROCEED is issued. See [the exact commands, outputs and individual verdicts](c10r_seal_v13_probe.md).

No model was loaded, torch was not imported for execution, no GPU/MPS work ran, and the production editor, scorer, equivalence or launcher was not executed. No commit or push was performed. Disposable Claude CLI probes were attempted under the brief's explicit exception. The harness, engine, shared-z scripts/preregistration, replay_exp2 and old sandbox were read only. The source fd16592 equivalence baseline edit.py remains unchanged.

## Installation and generated artifacts

The requested canonical sandbox /Volumes/memit/llm-database-poc-mirror/autoresearch_v13_c10 and fence /Volumes/memit/llm-database-poc-mirror/autoresearch_fence_v13_c10 are **not installed by this session**. Their parent is outside the writable roots, and this session cannot request broader permission. Two fresh, permitted staging bundles were generated instead:

- Production sandbox: /private/tmp/c10r_seal_v13_graftsafe_20261006/production/autoresearch_v13_c10
- Production fence: /private/tmp/c10r_seal_v13_graftsafe_20261006/production/autoresearch_fence_v13_c10
- Fixture sandbox: /private/tmp/c10r_seal_v13_graftsafe_20261006/fixture/autoresearch_v13_c10
- Fixture fence: /private/tmp/c10r_seal_v13_graftsafe_20261006/fixture/autoresearch_fence_v13_c10

Each sandbox is a standalone Git repository with zero commits and no copied history. The generator copies only the cleaned recipe, ignore files, README, program instructions and sanitized results.tsv, and precreates runs/ and .agent_capture/. No old working tree, graft directory/cache, credential, settings or hook is copied. Fixtures exist only in the fixture fence and cannot be selected by the production configuration.

Exact build commands, both exit 0:

    /opt/homebrew/bin/rtk proxy .venv/bin/python -I -B experiments/track_c/autoresearch_c10/v13_build.py --sandbox /private/tmp/c10r_seal_v13_graftsafe_20261006/production/autoresearch_v13_c10 --fence /private/tmp/c10r_seal_v13_graftsafe_20261006/production/autoresearch_fence_v13_c10
    /opt/homebrew/bin/rtk proxy .venv/bin/python -I -B experiments/track_c/autoresearch_c10/v13_build.py --fixture --sandbox /private/tmp/c10r_seal_v13_graftsafe_20261006/fixture/autoresearch_v13_c10 --fence /private/tmp/c10r_seal_v13_graftsafe_20261006/fixture/autoresearch_fence_v13_c10

Production output: closure_files=14305, fixture=false, commits_created=0. Fixture output: closure_files=14308, fixture=true, commits_created=0. Both returned graft_artifacts=0, tracked_graft_cache=0, history_graft_cache=0, immutable_roots=2, immutable_ignore_files=2. This generation check did not claim an active-process observation.

Profiles, settings, wrappers and manifests embed absolute installation paths. The program session must **regenerate at the canonical destinations**, rather than move these bundles. Every regenerated manifest needs its own successful verification records. No no_model_gates.json or law3.json PASS record was created.

## Files changed or created

All source files below are under experiments/track_c/autoresearch_c10/. Unrelated worktree changes, including a concurrent runbook update and pre-existing root .ignore, were not edited.

| File | Change and purpose |
| --- | --- |
| dispatch.py | New trusted parent: fixed isolated interpreter/arguments, private archive/handoff, profiles, clocks, locks, audit checks and summary projection. |
| editor_runtime.py | New training-only model/engine setup and three-arm absolute-tensor export; no evaluation harness/scorer import. |
| editor_bootstrap.py | New trusted adapter and readiness pipe before untrusted recipe top-level code; legacy import adapter for the unchanged equivalence baseline. |
| scorer.py | New exact-file/hash-checked harness loader and private scorer; original measurement/setup/LAW#5 function bodies retained. |
| v13_common.py | New strict JSON, closure checks, clean environment, typed summary, no-follow snapshots, handoff validation, process identity/CWD/descendant stop and GPU gate. |
| v13_graft.py | New no-indexer graft sweep, immutable root/file barriers and completed-private-area sealing. |
| v13_build.py | New fresh-only fence/repository generation, seed cleanup, training export, policies and closure/inventory manifests; no commits. |
| v13_launcher.py | New explicit CLI tool/strict-MCP/settings flags, clean environment, fresh UUID, bound transcript/watcher and launch gates. |
| v13_kill.py | New private stage-registry stop entrypoint; refuses changed PID identity/CWD. |
| v13_verify_gpu.py | New deferred LAW#3 and cleaned/fallback baseline driver, through the actual parent and both profiles. |
| v13_law3_equivalence.sh | New ready program-session entrypoint, expected hashes/metrics recorded; not executed. |
| v13_probe.py | New no-model §5.1–5.4 runner and exact-command/output/PASS/FAIL report, with graft checks. |
| fixture_editor_bootstrap.py, fixture_editor_runtime.py, fixture_scorer.py | New inert stdlib-only fixture, absent from production. |
| audit_transcript.py | Program-side AST tripwire, all-session archive scan, bound watcher and latched stop; repeats graft sweep. |
| sandbox_settings.py | Separate editor/scorer profiles; narrow filename/stage grants, network/keychain/bytecode rules, agent tool/Bash policy and graft denies. |
| run.sh, setup.sh, kill_run.sh | New source wrapper templates; generated wrappers are read-only, entry-hash/manifest-anchor pinned, env-i and isolated interpreter. |
| launch.sh | Program-side v13 launcher; legacy v12 launch/equivalence flow retired. |
| prepare.py | Direct legacy entrypoint retired with a fixed HALT and no model import. |
| program.md | Training-only canonical-prompt instructions, sealed evaluation/no-paraphrase rule, candidate-only interpretation and fixed root topology. |
| README.md | Generation, probes, launch gates, deferred GPU flow and graft isolation instructions. |
| test_plumbing.py | Twenty stdlib contract tests, including graft barriers, cache/index detection, preserved scorer AST and boundary controls. |

Requested report files: results/c10r_seal_v13_probe.md and results/c10r_seal_codex_impl.md. Training facts, policies, wrappers, private seed notes/config/reference data, closure manifest and inventory reside in each staged fence. Raw streams and records remain in fixture sealed/. No held-out template literal is added to an agent-readable file or report. Protected tripwire scratch files were created only in temporary fence sealed/ areas and removed.

## Decisions and limits

1. **No-model training export:** the harness builds its stimuli by tokenizing screen values after model setup. To avoid running it, export only CANON, FICTION and the three V_arm maps from two agreeing existing harness-result records. Pin both source hashes in sealed/seed_note.json and the immutable harness in the closure. Add only hparams, model/revision, seed, layers and edit budget to the training fields. The check confirms 24 subjects, all three arms, 72 facts and no evaluation fields/template windows. Country screens, PTEST, locality and generic/frame stimuli are absent from the export/editor grants.

2. **Seed provenance:** read 73f78ce:edit.py by /usr/bin/git show from the old sandbox, verify its published SHA, reduce PROMPTS to CANON, set DEV_PROMPT=CANON and change the runtime import. Preserve all other knobs and the separate original fd16592 LAW#3 baseline. Clean fallback 92acd03 the same way. Retain historical TSV aggregates under the required test-adjacency banner, with generic descriptions. Those scores do not establish the new baseline.

3. **Closure:** conservatively pin all trusted fence files, exact harness/hparams/screens/fingerprint, both ignore files, interpreter executable, and .py/.so/.dylib/.pth plus pyvenv.cfg under engine/venv/interpreter roots. Verify before importing fence helpers in parent/scorer. Model weights/covariance data remain runtime inputs, rather than helper code. Wrappers anchor the manifest and entry script; root_inventory.json separately records generated wrappers, seed and native Claude binary. Generated static fence files are read-only and immutable.

4. **Stage boundary:** UUID-based nocommit run folders; editor exits before private snapshots/scorer startup. Reject links, changed-during-copy files, malformed envelopes and incomplete arms. The scorer receives fixed program arguments, imports no recipe and keeps raw logs/full scores private. Project only validated status and 16 typed summary keys. Harmless fixture dispatch could not reach the stages here, so runtime projection/privacy acceptance is FAIL.

5. **Time and stop:** trusted bootstrap start marker precedes recipe top-level code; parent independently enforces the shared 2700-second edit budget inside a 7200-second run ceiling and 3600-second scorer ceiling. PID registry records birth/command, process group and allowed CWD, including engine CWD. Stop traverses descendants, including detached groups, and rechecks identity before signals. Mock tests PASS; real identity/CWD/stop remains unverified because ps is denied.

6. **Audit:** fresh UUID binds actual transcript, repository, captures and scorer output root. Missing/malformed/stale evidence latches STOP. Scan every dispatched recipe archive across all sessions. Normalization is lowercase ASCII words, punctuation splits and subject slots. All three verbatim templates and 15 four-word windows are detected; the four known look-alikes remain negative controls. This copying tripwire has a paraphrase blind spot. Live watcher readiness is FAIL here.

7. **Agent:** explicit Read/Edit/Write/Bash/TaskOutput tools, safe mode, dontAsk, empty strict MCP, no inherited settings/hooks, no web/browser/subagents and fail-closed Bash network/filesystem policy. CLAUDE_CODE_TMPDIR and TMPDIR request the precreated own capture area; editor/scorer have separate temps. HOME remains the CLI subscription-auth location; child tools receive no credentials and cannot read credential paths. The exact-flags probe returns exit 1, subtype=success but is_error=true and “Not logged in · Please run /login”; this is not a completed probe. Init lists Bash/Edit/Read/Write, omits TaskOutput and lists no MCP/plugin/web tools. Actual controls, capture relocation, background output and heredocs are FAIL.

8. **Launch:** require current-manifest PASS no-model attestation and LAW#3/cleaned-baseline record, successful graft process/filesystem sweep, exclusive GPU and specific old-loop absence. Unrelated review/probe sessions are not globally banned. No unsandboxed fallback, old-session resume, fixture promotion or instrumentation-error fallback. Process/GPU/old-loop observations are not established in this session.

## Graft finding and mitigation

**Evidence:** architecture_profile/c10r_exp2ctl_halt_diagnostic.json records the replay halt after graft appended /graft/ to tracked .gitignore, then the next refusal after tracked graft/.cache/ask-index.json changed. It identifies a replay seeded with tracked cache and a most-likely attached-session hook writer. This diagnostic and replay were not edited. No graft command was executed after the finding was supplied.

Installed graft source was inspected read only. Build may append .gitignore/.ignore, and query refresh may rewrite cache/graph. Ignore entries prevent tracking, not writes. No undocumented per-repository opt-out is assumed; no global graft installation/configuration was changed.

- Seed only the historical recipe into fresh standalone history; copy no graft/. Include /graft/ in both pinned ignore files before Git initialization. Sweep the index and all history for graft paths/cache names.
- macOS UF_IMMUTABLE plus read-only modes seal sandbox/fence roots, both ignore files and every generated static fence file. Precreate .git, runs/ and .agent_capture/. Ordinary indexers cannot create a root cache or atomically replace a pinned file. Existing recipe/results files remain writable in place and existing run/capture directories can receive children.
- Fence/scorer areas contain no Git metadata, indexer wiring or graft cache. Active stage/private state stays writable where required; profiles allow only own-stage paths and explicitly deny graft writes. Parent freezes completed scorer runs and recipe archives recursively, including files and directories.
- Disable inherited hooks and MCP; set GRAFT_NO_REFRESH=1, GRAFT_NO_GITIGNORE=1 and GRAFT_NO_IGNORE=1 in clean environments. File/Bash policy denies graft, ignore mutations and chflags. The root seals, rather than these environment variables alone, provide the filesystem barrier.
- v13_graft.py <fence> --processes is the added pre-launch sweep. Check immutable barriers/hashes, graft artifacts anywhere under protected roots, unexpected repository metadata, tracked/history cache and active graft processes. Reject any observed graft process because workspace refresh can cross repositories. Parent rechecks at dispatch; watcher repeats filesystem/index checks and halts on changes.
- Tests simulate indexer writes without executing graft. Two root mkdir attempts and two ignore write opens are denied; existing recipe opens for writing. Contract tests reject a late cache in the private scorer area and cache present only in Git index, and prove completed scorer data cannot be rewritten.

**Observed:** production/fixture generation reports zero graft files, cache tracking and cache history. Barrier probe: 2 root directory denials, 2 ignore write denials, existing_recipe_open_for_write=true. Completed-score and late cache/index tests PASS. **Active-process sweep: FAIL**, PermissionError executing /bin/ps; it does not establish absence of external writers.

An external same-owner process deliberately clearing immutable flags remains outside this boundary. Do not attach a graft-enabled session or explicitly index protected areas. Active writable scorer roots rely on no repository/indexer attachment, profiles and watcher until closeout freezes them. End-to-end CLI editing under the sealed root topology needs the successful required probe; the logged-out probe cannot prove it. No blanket immunity or relaunch approval is asserted.

## Verification and deferred work

PASS: twenty stdlib tests; three verbatim templates; 15/15 windows; four recorded paraphrase blind spots; cleaned seed; complete training export; missing-watcher halt; graft filesystem/index/history sweep and immutable barriers.

FAIL: sandbox-exec allow-default positive control exits 71, sandbox_apply: Operation not permitted. Exact-file/profile/own-temp tests FAIL. Process observation raises EPERM, so watcher readiness and graft active-process sweep FAIL. Every unreached hostile attempt remains FAIL, including namespace, private/protected files, localhost, git/gh and keychain. Harmless dispatch and summary/privacy positive control FAIL. Logged-out CLI probe omits TaskOutput and performs no successful tool turn; every requested agent control remains FAIL.

Static checks PASS: AST parse of 18 changed/new Python files, bash -n of five shell files, scoped git diff --check. Protected-path git diff is empty.

Program session must install fresh canonical destinations, resolve CLI TaskOutput/auth context and rerun §5.1–5.4 with working Seatbelt/process observation. Verify actual captures, foreign TaskOutput/heredocs, file tools, network/keychain denial, stop behavior and editing under root seals. Do not bypass profiles to obtain a PASS. A program reviewer attests no-model gates only after every required control has successful evidence.

**§5.5 deliberately deferred:** after shared-z and the location control finish, run experiments/track_c/autoresearch_c10/v13_law3_equivalence.sh. It uses production fence/run.sh with both profiles for original fd16592, then cleaned 73f78ce. Expected baseline heldout_full=7/72, dw_total=88.974, templates_sha=e8605172dce0 and absolute saved-tensor hashes:

| Arm | Expected SHA-256 |
| --- | --- |
| A1_single | 2f72fee29064643ce2214e7d644f88a71292e56c35ab657b3b3d355405cbaab1 |
| A2_coherent2 | f94e1be2258482a84201432aec35f88c59f25e7b9d325345a447a108e0e2dd56 |
| A7_coined_coined | c30664a92b06be43485a2043b4512d08d977df2708289f558d5ba03a5a7da965 |

Only a successfully measured cleaned base failing a guard selects cleaned 92acd03. Errors, timeouts, malformed output or failed instruments halt. Fallback must also pass guards. Loop outputs remain selection candidates; promotion needs an independent preregistered unseen held-out set.

## Hash manifest

Full conservative production closure: /private/tmp/c10r_seal_v13_graftsafe_20261006/production/autoresearch_fence_v13_c10/sealed/manifest.json (14305 paths). Fixture closure: /private/tmp/c10r_seal_v13_graftsafe_20261006/fixture/autoresearch_fence_v13_c10/sealed/manifest.json (14308 paths). Both were generated after source freeze. The following table records staged production files, not a canonical installation that has not happened.

| Production fence path | SHA-256 |
| --- | --- |
| sealed/manifest.json | 021162ad3421857d7c7e7b066901a4d6ec70f790c1905e4728978d0714801c51 |
| sealed/root_inventory.json | fd70a668ab0a09e225505a0ba1677b5956c6a11f2964d15856dafb32b7176b58 |
| sealed/config.json | 0957225b661839f6f8dc61130999ac55657e15c0f05941fa0517d01685f19f5c |
| sealed/seed_note.json | b46d16f9a10c575a661b6e5421a0711d52b68f01e117e7a92ee8129c1e157d9e |
| sealed/baseline_edit.py | 0d03bf68549cc8a9fb3f725850222a31ad8fc822e7df5e69e9d50cc3c4cfb0f7 |
| sealed/seed_edit.py | cde0b4d10fcfdb8b04e156b782ac6a5555a46d2f920174f65724ca17022dfc56 |
| sealed/fallback_edit.py | dacd2d6aa4341d71a512d765b214f0d3a0a6b33e53ce89fd2db1a5daf7c22954 |
| editor_runtime.py | b0da10da1272b75072fc9990d8fe44a49f103be111d0f56308f6feacc3d10a5d |
| editor_bootstrap.py | 616c3e69021413b3e95549e8934aed84639f7eac7c91641f910b04a129bbcbfe |
| scorer.py | 4842bb69e381dc2f89e48428255a99c3c9fa85659778505c1402fc92ec45293b |
| dispatch.py | 5cfcb9d9e2204d9c848cc6f91e98bd52975e26cf5212e6ed4d69bf3f78750db1 |
| v13_common.py | 7ddf92830bd3402a8e2a889a4ac51049869452cffc5a714a5d939d538b71494d |
| v13_graft.py | 67260e4e5481a08e92c040bf613d52833b4992888658838ca54307797766ec04 |
| audit_transcript.py | 7db1e70a577e091dfa3ffa857f3179541abd55f0fef928d572c68ab583522222 |
| sandbox_settings.py | 39976923d92764aa4a30e228cb8a57062c0c3644410775958808776a1edc74d6 |
| v13_launcher.py | d03c9d72bab4a7ec156924e778a922b25ad7d0e3d91df6a97472599ec7dbd6f3 |
| v13_verify_gpu.py | f3d70434656f3dbc712a2caae5ea291d0d79391d57f8eb20a1f109efa2ef9f32 |
| v13_kill.py | d99a15dec7ee40b7088b5e5e283159597a5eabee2f48a9ec17fcfe199816bf75 |
| train_facts.json | aeb5677e7c2b1c3556ccc34dbeecab1eb78824c24a0542225d314f69dfc70b04 |
| run.sh | 8c25e3769b41055566815bf3914ff81dd275f806eb1241ab331a0c68a9c78ab7 |
| setup.sh | 8c25e3769b41055566815bf3914ff81dd275f806eb1241ab331a0c68a9c78ab7 |
| kill_run.sh | e827a9492b206067561ad80c883ad5984386198dda1415e102d4e5291007b197 |
| editor.sb | 8b44e9d5abd53a046ae2d182cea3ca59cf8aca642de1f4216c1ab9e07744baae |
| scorer.sb | 7de7eb34ef2229534a6a0ce7ffe9ca2b6667c0197cccfc24c466055270880435 |
| .sandbox_settings.json | 41a83e9ff9b62610777b35545f6c8dfc1b41062996e53022c9c92e2f4cbe96fa |
| empty_mcp.json | 1e0fe4707a42d1cce5d4e89af209cc6317e979348f1a1a3e1eda481a1467821e |

| Additional input/artifact | SHA-256 |
| --- | --- |
| fixture sealed/manifest.json | a761f1151dda48a1ccaca59667685801b38a69bfbf6cfe2188d88ddfd1ce292f |
| seed repository edit.py | cde0b4d10fcfdb8b04e156b782ac6a5555a46d2f920174f65724ca17022dfc56 |
| seed .gitignore | 8b9a1a6ec89d7155b1d52fcd52cf2172be29d6f21c6414bc504ad7fbb63973f5 |
| seed .ignore | d468201b6eafa109f7649e0edf84f7a7d4f0a6e786b5815c064c2222e39529b3 |
| seed results.tsv | a06e5e9eb8597b8f773b2f17d8b51fb8d1333092e83285942198d5b23dd61a97 |
| seed program.md | 4f32d71f8552681e07d51a4353dc9abe2ac508ef6569102c55f1d7cf9cd862f7 |
| immutable harness | 1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695 |
| scorer fingerprint helper | 450ee83ac829817299ead301c4a3d20702f431deaea4be58c77ecfd89a329162 |
| hparams | 4225cc6aabc3eb9fa62d2bb2cac68b1238de3a39c5e469da635e6e1464aa3bb4 |
| probe report | 7e1ee4a644110dfcd05cc529c56e4e8fc2e8f5bf3d5d49c4e2b2cccc68ac0e42 |

Historical 73f78ce source SHA-256: c89d80c09f2e97490ed30cda22e2a001d551e74a7df5d62585c741fc3b06abcf. Historical 92acd03 source: 03ce43f3812333a97cb24329a3c7b8520d918785fbda46d5b31799df5860d7e0.

Preserved knobs (previously selected on the same 72 reads):

    {
      "CLAMP_NORM_FACTOR": 0.75,
      "GAIN": 1.25,
      "KL_FACTOR": 0.125,
      "LAYERS": [
        4,
        5,
        6,
        7,
        8
      ],
      "NULL_THRESH": 0.005,
      "PRESERVE_WEIGHT": 4.0,
      "RIDGE": 1.0,
      "V_LR": 0.5,
      "V_NUM_GRAD_STEPS": 25,
      "V_WEIGHT_DECAY": 0.5
    }

Training export provenance (also in sealed/seed_note.json):

| Source | SHA-256 |
| --- | --- |
| /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10e_bandknob.json | 4db30b57cf81f00962ada4310979ce5655a6b551fff880d42167a90eb737bf62 |
| /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10l_covgeom/run1_armB_identity.json | 2c3a9f6fa359ecc4cf3c67b3a84c4da34ef1544438de31e301f5e19fb9297470 |

Workspace implementation source hashes; wrapper templates differ from generated wrappers by path/anchor substitution:

| Source file | SHA-256 |
| --- | --- |
| README.md | 0fc4e93e28b2870b1507c7bd8b00b5d0710a26f7c2bb6129eee7dfa576609332 |
| audit_transcript.py | 7db1e70a577e091dfa3ffa857f3179541abd55f0fef928d572c68ab583522222 |
| dispatch.py | 5cfcb9d9e2204d9c848cc6f91e98bd52975e26cf5212e6ed4d69bf3f78750db1 |
| editor_bootstrap.py | 616c3e69021413b3e95549e8934aed84639f7eac7c91641f910b04a129bbcbfe |
| editor_runtime.py | b0da10da1272b75072fc9990d8fe44a49f103be111d0f56308f6feacc3d10a5d |
| fixture_editor_bootstrap.py | aaf618a31f3a59b8de49b82ef23d19bac1493ec51cf8ffe2ee34d5013d882a36 |
| fixture_editor_runtime.py | 5b0a7b20e64f8ef93b7656b6739599fea126f215938b85ef4f81aeb74db64b11 |
| fixture_scorer.py | c0bab5b7c4ee431b79c3a0dbd3806ceb75663786ed89f61b918a65c9d93f37f9 |
| kill_run.sh | 966c3b52880db2728f719b5c310de1f538f2cdba5ed32dce0e6b39609accee9c |
| launch.sh | 9deb4e074db55f5d6694e0e7bdefc6799da0ec04e6a6e0a00af17dde5d19fdcd |
| prepare.py | 2ad3672c9e5494588bf63db5eed53827b5bc0bf7a6a44fd346076f81a108eea5 |
| program.md | 847fbeaca35d17b3f60b510cd6ad8bce2e87abaad794bf6f86bbf28e3b70c1ce |
| run.sh | 966c3b52880db2728f719b5c310de1f538f2cdba5ed32dce0e6b39609accee9c |
| sandbox_settings.py | 39976923d92764aa4a30e228cb8a57062c0c3644410775958808776a1edc74d6 |
| scorer.py | 4842bb69e381dc2f89e48428255a99c3c9fa85659778505c1402fc92ec45293b |
| setup.sh | 966c3b52880db2728f719b5c310de1f538f2cdba5ed32dce0e6b39609accee9c |
| test_plumbing.py | 130632697dbe6ff77e40b4c4927c86432ab603831a4db9aaed3d78155ed8bab5 |
| v13_build.py | 6f845e7abd5d4ffd2e9890632d3126499f484a9064207c4d2a1c07051d101c18 |
| v13_common.py | 7ddf92830bd3402a8e2a889a4ac51049869452cffc5a714a5d939d538b71494d |
| v13_graft.py | 67260e4e5481a08e92c040bf613d52833b4992888658838ca54307797766ec04 |
| v13_kill.py | d99a15dec7ee40b7088b5e5e283159597a5eabee2f48a9ec17fcfe199816bf75 |
| v13_launcher.py | d03c9d72bab4a7ec156924e778a922b25ad7d0e3d91df6a97472599ec7dbd6f3 |
| v13_law3_equivalence.sh | ed6454ae4c23320443806256fd53cfd2c5e693ef66a39f07cc59263be7a18290 |
| v13_probe.py | c0407a73eece188242915b6ce257d59afa0572a071804930fea4480c27bb4918 |
| v13_verify_gpu.py | f3d70434656f3dbc712a2caae5ea291d0d79391d57f8eb20a1f109efa2ef9f32 |
