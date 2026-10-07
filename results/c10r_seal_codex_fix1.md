# D-C10r-seal — Codex fix round 1

**Implementation and model-free regression checks: DONE. Runtime sealing verdict: GATED on the fresh program-side probe; DO NOT LAUNCH.**

Followed `results/c10r_seal_fix_round1_brief.md` and read the complete `results/c10r_seal_v13_probe_program.md`, including its tester addendum. No model request, torch import, GPU job, loop launch, commit or push was performed. The only Claude invocations were read-only `--version` and `--help`; the installed native executable and the previous private probe stream were inspected without invoking a model. No installed destination was unlocked, deleted or modified. No change was made to `c10s_sharedz_*`, the harness, `memit_dry_run/`, any `autoresearch_replay_*` destination or the old sandbox. No live gate is declared satisfied from a synthetic test.

The corrections are source changes for **new** installations. The previous 10-PASS/35-FAIL probe record and all installed v13 copies remain intact.

## Fixes and model-free evidence

### 1. Root/metadata reads and startup controls

`experiments/track_c/autoresearch_c10/sandbox_settings.py:9` now grants `file-read*` to the **literal root `/`**, plus `file-read-metadata` to necessary ancestor literals of the resolved runtime/fence/sandbox paths. It grants no new ancestor subtree data access. Network, file-write, protected-data and keychain denials remain in force. Scorer closure verification also has exact-file grants for the two pinned sandbox ignore files and the new trusted helpers; otherwise resolving the interpreter would expose a second closure-read startup failure.

`experiments/track_c/autoresearch_c10/v13_probe.py:42` and `experiments/track_c/autoresearch_c10/v13_probe.py:121` add `/bin/echo PROFILE_ECHO_OK` and `python -I -B -c 'print("PYTHON_START_OK")'` positive controls under **both exact generated profiles**, for production and fixture installations. A zero exit without the expected marker is FAIL. The controls use the trusted environment and fresh parameterized run/temp directories.

Model-free test: `experiments/track_c/autoresearch_c10/test_seal_fix1.py:194` verifies the root literal and ancestor metadata, rejects root/program subtree grants, and checks that only the scorer can read the pinned ignore files. **PASS.** A direct runtime Seatbelt positive control in this Codex session returned exit 71, `sandbox-exec: sandbox_apply: Operation not permitted`, even under `(allow default)`. Therefore no profile-start success is claimed here; the new program-side positive controls must prove it.

### 2. Fully resolved interpreter, with pinned package lookup

`experiments/track_c/autoresearch_c10/v13_build.py:51` resolves `.venv/bin/python` and `.venv` with `strict=True`; `experiments/track_c/autoresearch_c10/v13_build.py:61` stores those resolved paths, the resolved base prefix and the virtualenv site-packages directory. The configured executable no longer traverses either previously denied interpreter symlink. Ancestor access is metadata-only; data reads remain limited to the resolved runtime targets.

Resolving the executable changes Python's virtualenv discovery under `-I`. `experiments/track_c/autoresearch_c10/v13_common.py:64` carries only the trusted `C10_SITE_PACKAGES` value; `experiments/track_c/autoresearch_c10/editor_bootstrap.py:13` inserts it before loading the editor runtime. The verified scorer adds the same pinned directory at `experiments/track_c/autoresearch_c10/scorer.py:29`. This preserves access to the installed packages without PYTHONPATH or a new unpinned interpreter copy. LAW#3 still decides numerical equivalence.

Model-free test: `experiments/track_c/autoresearch_c10/test_seal_fix1.py:205` calls the actual generator helper, verifies the executable has no remaining symlink, starts it in isolated mode and uses `find_spec("torch")` to find the pinned virtualenv package. It asserts torch is absent from `sys.modules` before and after. **PASS.** Actual resolved executable:

```text
/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11
```

### 3. Installed tool inventory, plugins and timeout

`experiments/track_c/autoresearch_c10/v13_cli.py:23` runs only `--version`, checks the installed native builtin declarations, and records the version, resolved executable, sha256, names and declaration evidence in the generated config. The supported allow-list is `Read,Edit,Write,Bash,Monitor,TaskStop`. `experiments/track_c/autoresearch_c10/v13_cli.py:12` rejects unknown names, duplicates or a changed minimal set before invocation. `experiments/track_c/autoresearch_c10/v13_launcher.py:14` uses that validated list; `experiments/track_c/autoresearch_c10/v13_cli.py:43` requires a fresh installation/probe if the CLI changes.

Live read-only inspection returned:

```text
2.1.292 (Claude Code)
Read=ct, Edit=bt, Write=tn, Bash=Fe, Monitor=gl, TaskStop=Cc
CLI sha256: 97a01e5bc74a199e67189435d0331ea3a24eac2e07db4b76d9148c5b0386138f
```

The executable is `/Users/robertrhu/.local/share/claude/versions/2.1.292`. Version support is deliberately fail-closed, rather than guessing names for future CLI versions. `experiments/track_c/autoresearch_c10/v13_agent_probe.py:135` accepts the known safe-mode builtin plugin metadata only when no plugin contributes a tool, the actual tool set is exactly the reviewed builtins, and `mcp_servers` is `[]`. Extra tools, plugin tools, MCP servers and a changed CLI version fail. Empty plugin metadata is no longer required. `experiments/track_c/autoresearch_c10/v13_agent_probe.py:248` uses a **900-second** timeout (at least the requested 600) and 64 maximum turns.

Model-free tests: `experiments/track_c/autoresearch_c10/test_seal_fix1.py:173` rejects TaskOutput, BashOutput and unknown names; `experiments/track_c/autoresearch_c10/test_seal_fix1.py:164` passes builtin plugin metadata with no tools and rejects added tools/MCP/plugin contributions/version drift; `experiments/track_c/autoresearch_c10/test_seal_fix1.py:264` checks the timeout and opt-in. **PASS.** Live agent init inventory remains untested under this task's no-model limit.

### 4. Benign scripted §5.4, raw-result evaluation and actual model

`experiments/track_c/autoresearch_c10/v13_agent_probe.py:20` specifies exact named Bash commands and Read calls. `experiments/track_c/autoresearch_c10/v13_agent_probe.py:100` authorizes benign fixture plumbing operations, requests each explicit call once, and asks for raw errors rather than template-seeking, circumvention or PASS/FAIL judgments. The probe reads public files, edits the existing root `edit.py`, writes an own scratch file, runs the inert fixture wrapper, checks temp creation/readback/removal and heredocs, reads the output path actually returned by background Bash, and starts/stops Monitor on that own output. Named private/program/harness/foreign-capture/credential/keychain reads, foreign write opens, localhost and git/gh/security commands test denials.

`experiments/track_c/autoresearch_c10/v13_agent_probe.py:135` matches exact tool inputs to tool-use IDs and their raw tool results. It ignores assistant judgment. A Bash boundary receipt must show that the interpreter started and each named operation returned EPERM/EACCES; connection refusal, missing files, refusal prose and interpreter startup failure are not denial evidence. Missing, repeated or changed commands, absent results/models, unsafe sandbox overrides, malformed streams and an incomplete/error session fail. Own background evidence is tied to the actual returned output path under the configured capture child and its exact per-probe marker. The program also checks the edited/written files after the session.

Each control records the **actually served `assistant.message.model`** from its matched call. Inventory records requested model, served models, CLI version/hash and `result.modelUsage`, including fallbacks. Raw stdout and separate stderr stay in the fresh fixture's sealed probe directory. The live watcher is bound to the actual fresh session transcript, and a named readiness command gates the wrapper until that watcher is ready. Both the canonical transcript and raw stream are audited before accepting the probe.

The old unconditional-FAIL rows and adversarial launcher prompt were removed. The old `v13_launcher.py --probe` route now refuses and points to the evaluated `v13_probe.py --agent-probe` entrypoint. This session never executes either a model probe or a loop launch.

Model-free tests: `experiments/track_c/autoresearch_c10/test_seal_fix1.py:92` exercises a complete positive raw stream with a different requested/served model; `experiments/track_c/autoresearch_c10/test_seal_fix1.py:98`, `experiments/track_c/autoresearch_c10/test_seal_fix1.py:103`, `experiments/track_c/autoresearch_c10/test_seal_fix1.py:114`, `experiments/track_c/autoresearch_c10/test_seal_fix1.py:122`, `experiments/track_c/autoresearch_c10/test_seal_fix1.py:131`, `experiments/track_c/autoresearch_c10/test_seal_fix1.py:152` and `experiments/track_c/autoresearch_c10/test_seal_fix1.py:273` exercise missing/changed/unsafe calls, refusal, allowed reads, missing files, startup errors, connection refusal, malformed/session-mismatched records, wrong temp/output paths and wrong background markers. **PASS.** These validate the evaluator; they do not substitute for the real agent session.

### 5. Supported short temp/capture fallback, with claims gated

The installed native CLI's bundled `cg()` reads CLAUDE_CODE_TMPDIR and `rTe()` uses its `claude-UID` child only when that child is at most **44 bytes**. A longer path triggers the shared `/tmp/claude-UID` fallback. This explains why the old worktree-length `.agent_capture` request did not move Bash TMPDIR.

`experiments/track_c/autoresearch_c10/v13_build.py:61` creates a fresh 0700 `/private/tmp/c10r-<12 hex>` base and 0700 `claude-UID` child. At uid 501 the child is 41 bytes. `experiments/track_c/autoresearch_c10/v13_launcher.py:25` sets CLAUDE_CODE_TMPDIR to the **base**, TMPDIR to the **child**. `experiments/track_c/autoresearch_c10/sandbox_settings.py:73` grants Bash and file tools only that own child, retains both shared foreign-temp denials, and denies writes to the shared legacy capture roots. The Python base-prefix read exception supports the scripted stdlib commands; file-tool permissions still deny home/private program data.

`experiments/track_c/autoresearch_c10/v13_agent_probe.py:135` requires the raw Bash-reported TMPDIR to resolve to the configured child, completes create/read/remove there, and requires the actual returned background output file to be readable there. Merely setting environment variables never passes. The design's §4(a) fallback and §5.4 were updated accordingly.

Model-free tests: `experiments/track_c/autoresearch_c10/test_seal_fix1.py:182` verifies the narrow read/write grants, both denial spellings and short-path calculation; `experiments/track_c/autoresearch_c10/test_seal_fix1.py:141` rejects `/tmp/claude-501` fallback and a foreign output path. **PASS. Runtime relocation, own capture and background behavior are still GATED on the program-side agent probe.**

### 6. Fresh-only, one-script install-and-probe procedure

`experiments/track_c/autoresearch_c10/v13_install_probe.py:14` generates four disjoint tagged destinations. `experiments/track_c/autoresearch_c10/v13_install_probe.py:22` preflights all four and the report before installation, refuses existing paths or symlinks, keeps the graft process gate, installs production and fixture, then probes them. There is no overwrite, unlock, deletion, loop launch or GPU run. A reused tag/report fails clearly. No hand repair of previous installed copies is needed.

`experiments/track_c/autoresearch_c10/v13_probe.py:42` uses unique run/temp children; `experiments/track_c/autoresearch_c10/v13_probe.py:121` uses a unique sealed probe directory for the dummy module and raw streams, rejects previously probed fixtures, selects only newly created attempt receipts, and opens the report exclusively. Probe report text now records the actual verified install paths, instead of the stale “canonical installation deferred” sentence. `--agent-probe` is an explicit opt-in; without it, model-backed checks remain deferred/FAIL and cannot write a PASS gate.

Model-free tests: `experiments/track_c/autoresearch_c10/test_seal_fix1.py:240` creates two distinct scratch parameter sets, checks disjoint tagged layouts, rejects invalid tags and existing destinations before build; `experiments/track_c/autoresearch_c10/test_seal_fix1.py:264` verifies the no-model default. **PASS.** `v13_install_probe.py --help` ran successfully and showed exactly `--tag`, `--report`, `--agent-probe`.

Run this **once from the program shell**, after closing graft-enabled attached sessions, from this worktree root:

```sh
.venv/bin/python -I -B experiments/track_c/autoresearch_c10/v13_install_probe.py \
  --tag fix1_20261006_a \
  --report results/c10r_seal_fix1_probe_program_a.md \
  --agent-probe
```

This procedure is prepared, **not executed in this Codex session**. The switch authorizes only the disposable CLI plumbing probe; no torch/model editing or GPU/equivalence work occurs. A rerun changes both tag and report filename. The original installed roots are never reused. The complete procedure is also documented in `docs/C10R_LOOP_SEALING_V13.md` §10.

### 7. Graft active-process gate retained

`experiments/track_c/autoresearch_c10/v13_graft.py:52` preserves the original fail-closed process-table validation and active-graft rejection. Both `experiments/track_c/autoresearch_c10/v13_install_probe.py:22` and the normal launcher enforce it; the regular pre-launch filesystem/index/history sweep remains binding. No code kills an attached session or weakens this gate.

Model-free test: `experiments/track_c/autoresearch_c10/test_seal_fix1.py:256` rejects a running `node .../graft mcp`, empty observation and malformed observation, and accepts a valid harmless process table. **PASS.** Actual `/bin/ps` execution in this managed Codex sandbox was denied with EPERM. That is an environment limitation, not evidence that no graft process is running. The program session must close graft-enabled attached sessions before its next probe **and before launch**, as the brief specifies.

## UF_IMMUTABLE and legitimate writes

`experiments/track_c/autoresearch_c10/v13_graft.py:127` verifies create/read/atomic-replace/cleanup in six **precreated mutable areas**: sandbox runs, fence sealed state, private scorer results, editor temp, scorer temp and the own capture child. It also opens the existing edit.py and results.tsv for writing without changing their bytes. `experiments/track_c/autoresearch_c10/v13_probe.py:121` schedules it for both fresh installations.

`experiments/track_c/autoresearch_c10/test_seal_fix1.py:216` exercised the actual macOS UF_IMMUTABLE root flags in an isolated throwaway directory: all six child areas accepted their legitimate write lifecycle, the existing root recipe could be updated in place, and adding a new root entry raised PermissionError. **PASS.** Cleanup cleared flags only on that test's temporary scratch tree, never on an installed destination. Existing freeze/root-barrier tests also passed. The future agent capability explicitly edits root edit.py, so an incompatible Edit atomic-replacement strategy cannot be silently accepted.

The new program probe still must prove editor/scorer runtime writes **through their exact Seatbelt profiles**. The managed sandbox prevents that runtime test here.

## Verification actually performed

All commands below were invoked through `/opt/homebrew/bin/rtk proxy`; no denied Seatbelt/process command was retried with broader permissions.

```sh
.venv/bin/python -I -B -X pycache_prefix=/private/tmp/c10r_fix1_no_stale_cache experiments/track_c/autoresearch_c10/test_plumbing.py
.venv/bin/python -I -B -X pycache_prefix=/private/tmp/c10r_fix1_no_stale_cache experiments/track_c/autoresearch_c10/test_seal_fix1.py
```

Results: **20 existing tests PASS + 18 fix1 tests PASS = 38 model-free tests PASS.** Bytecode lookup used a separate empty prefix; no stale project cache was accepted as evidence. `py_compile` passed for all 13 changed/new Python files, writing compiled output only to a temporary directory. `git diff --check` passed. The install/probe help and real installed CLI inspection passed.

One existing test's prior `HEAD:prepare.py` comparison failed because HEAD now contains the v13 shim, which has no measurement functions. `experiments/track_c/autoresearch_c10/test_plumbing.py:168` now compares against the actual last pre-seal source `9feae02^:experiments/track_c/autoresearch_c10/prepare.py` (sha256 `8e577d546080f06bbd25a685e9af03016117d1e133ff9ff97aa92e5ac22f21f1`). The seven setup/measurement function ASTs match the scorer unchanged. The policy fixture also gained the new required interpreter/ignore-file keys. These were test-reference fixes, not measurement changes.

Runtime observations in this sandbox, kept as failures/limitations:

```text
sandbox-exec -p '(version 1)(allow default)' /bin/echo V13_SEATBELT_POSITIVE_CONTROL
exit 71: sandbox-exec: sandbox_apply: Operation not permitted

/bin/ps -p 1 -o command=
exit 1: rtk: Failed to execute command: /bin/ps: Operation not permitted (os error 1)
```

Before/after sha256/metadata checks confirmed **64 protected source files unchanged**, including all c10s_sharedz files, the harness and engine Python files. **164 installed non-.git files and all four installed roots' flags/modes were unchanged.** The roots remain mode 0555 with UF_IMMUTABLE:

| Installed root | Manifest sha256 (fences) | Changed |
|---|---|---|
| `/Volumes/memit/llm-database-poc-mirror/autoresearch_v13_c10` | — | No |
| `/Volumes/memit/llm-database-poc-mirror/autoresearch_fence_v13_c10` | `4f81143a622a9821dafa0aaae8bb206e093d5553b6394f672cd4a20c0f67d43f` | No |
| `/Volumes/memit/llm-database-poc-mirror/autoresearch_v13_fixture_c10` | — | No |
| `/Volumes/memit/llm-database-poc-mirror/autoresearch_fence_v13_fixture_c10` | `3cd81da018bbb195191417d4adc42c77956f68e88c45d35619d9d3050883323b` | No |

No install, unlock, deletion or live gate receipt was produced by this session. Source/report changes are ready for the fresh program-side run; live §5.2–§5.4 outcomes, actual temp relocation, LAW#3 and the cleaned-base GPU score remain open. No Codex PROCEED or relaunch authorization is issued.

## Changed source manifest

These hashes identify the source changes, not a newly installed scorer-closure manifest. Every fresh installation generates its own closure/anchor through the builder.

| File | sha256 |
|---|---|
| `experiments/track_c/autoresearch_c10/sandbox_settings.py` | `51bc414aa84cfe3782c8ccb3351f7550f1b87be4ce5fe8675b82f1c158f4f6a4` |
| `experiments/track_c/autoresearch_c10/v13_build.py` | `fbccc9c6498938b915776d5887fd0e3dbeaddb4335269397f97462b9f1f83b75` |
| `experiments/track_c/autoresearch_c10/v13_cli.py` | `8f222fb4b93848274b8ef5926c7d3193e7d0f739d6f4f2ccee9f8e861da7009a` |
| `experiments/track_c/autoresearch_c10/v13_common.py` | `751ccbd92c64b06172765d48cc2461459b635562186e4ecb2aaa07c10f80e675` |
| `experiments/track_c/autoresearch_c10/editor_bootstrap.py` | `f1271db7ab744c80acc8ff5e9fafe4eb431369ac65bb3883f0834e4d031dbe2c` |
| `experiments/track_c/autoresearch_c10/scorer.py` | `2e80069d480788668efd9cc506c04a7607178cc69ee4f9a64fd9c1d14ab10497` |
| `experiments/track_c/autoresearch_c10/v13_launcher.py` | `9374f3f44e80ab1b4452acbd946e1caa245b779773e3002b3f0eb4ec41eb54f1` |
| `experiments/track_c/autoresearch_c10/v13_agent_probe.py` | `bb3e358b105161d1caf4ee2f39a503a045740f7a721eb0953a265d668674f438` |
| `experiments/track_c/autoresearch_c10/v13_graft.py` | `ffca003ce14111a1ea405eb07928474a4cf117b29cf84152c1ddd001aab03270` |
| `experiments/track_c/autoresearch_c10/v13_probe.py` | `a552715db22af371efbb701e78c322b8379a0845c967d6627d52801add6f7d88` |
| `experiments/track_c/autoresearch_c10/v13_install_probe.py` | `6509c5b5017f9d2dbd924e665913b3ae56303ac4dafd2089ebf5cc89fe0edbd6` |
| `experiments/track_c/autoresearch_c10/test_plumbing.py` | `d0f2bb376e43b94887757a373331f5e5fecea3daf9cb3f9a01783a33e9f88704` |
| `experiments/track_c/autoresearch_c10/test_seal_fix1.py` | `6863dc9fbb1ff5ebb15ee876b2d1752743e03b880af3b29e53302ab0eac5f49b` |
| `docs/C10R_LOOP_SEALING_V13.md` | `d79ee115c04baaba0e3f5e50c914582a175404639c623f0e2cab0113cb294256` |

New files: v13_cli.py, v13_agent_probe.py, v13_install_probe.py, test_seal_fix1.py, and this report. The remaining manifest entries were updated in place.
