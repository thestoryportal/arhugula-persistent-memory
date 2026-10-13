# Code inventory — slice 0, revised

Status: slice 0 reviewed. Refreshed for slice 1 against base 60b69de7.

## Scope and evidence

The subject is `code/`. Each depth-1 and depth-2 path has one row. Nouns are durable kinds, not a file list. A representative source owns each kind. Scope patterns group related files. The skill package family contains 13 package folders in this worktree. Patterns are plain text. Concrete source citations use code formatting.

Classes: catalog = orientation; contract = schema, configuration, or test boundary; factory = tool; product = application or engine; dead = confirmed obsolete implementation. Absence alone does not prove dead.

Live requires an import, executable path binding, CI step, hook, launcher, config, or current instruction. Current instruction sources are root CLAUDE.md/README.md, _system/governance/, program/runbook/, and program/SESSION_BOOTSTRAP.md. Leftover requires a historical referrer or the Policy B closed-script list. Ghost means no qualifying referrer was found. A missing target is a ghost reference.

No file under _index/ supplies wiring evidence. Historical referrers include _archive/, program/checkpoints/, program/sessions/, closed experiment records, sealed source snapshots, and Policy B scripts. Other prose does not establish wiring. A folder row covers its cited surface. Descendants can differ.

The scan reads source. It never imports a repo module. Python imports resolve to source paths. Python path literals must occur in executable syntax. Comments and docstrings do not supply executable edges. Sibling asset literals infer a local edge. These edges do not prove host operation or science authority.

Search S: substitute the row path for PATH. Run rg -n --hidden -F "PATH" . --glob "!.git/**" --glob "!data/**" --glob "!map/**" --glob "!_index/**". Inspect imports with revise_inventory.py in the report folder. No referrer means no qualifying edge in this scan. Dynamic edges remain UNVERIFIED.

Open `map/group-b-leftovers.md` for the 49 closed scripts. This inventory does not copy them.

## Depth-1 and depth-2 paths

| Path | Class | Universe | Evidence |
|---|---|---|---|
| `code/CONTEXT.md` | catalog | live | `CLAUDE.md:46` (current instruction). |
| `code/agents` | factory | live | `.codex/hooks/session_start.py:21` (hook, config, or CI reference). |
| `code/agents/CONTEXT.md` | catalog | ghost | No binding or historical referrer found. Search S with this path. |
| `code/agents/advisor_review_prompt.md` | catalog | live | `.codex/skills/advisor-review/SKILL.md:49` (hook, config, or CI reference). |
| `code/agents/claude_advisor.sh` | factory | live | `.codex/hooks/session_start.py:21` (hook, config, or CI reference). |
| `code/agents/codex_context_guard.py` | factory | live | `.codex/hooks/session_start.py:23` (hook, config, or CI reference). |
| `code/agents/context_watch.py` | factory | live | `code/lab/runners/test_c10w_p2_gate.py:22` (literal). |
| `code/agents/install_infranodus_skills.sh` | factory | live | `program/SESSION_BOOTSTRAP.md:61` (current instruction). |
| `code/agents/skills` | catalog | live | `code/gates/experiment_gate.py:23` (literal). |
| `code/agents/test_twins.py` | contract | ghost | No binding or historical referrer found. Search S with this path. |
| `code/agents/twins.py` | factory | live | `.github/workflows/ci.yml:37` (hook, config, or CI reference). |
| `code/apps` | product | live | `_system/governance/REPRODUCIBILITY.md:54` (current instruction). |
| `code/apps/CONTEXT.md` | catalog | ghost | No binding or historical referrer found. Search S with this path. |
| `code/apps/dashboard` | product | live | `code/lab/runners/c10w_p2_gate.py:37` (literal). |
| `code/apps/labviz` | product | live | `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:96` (current instruction). |
| `code/apps/mathlab` | product | live | `_system/governance/REPRODUCIBILITY.md:54` (current instruction). |
| `code/configs` | contract | live | `README.md:111` (current instruction). |
| `code/configs/CONTEXT.md` | catalog | ghost | No binding or historical referrer found. Search S with this path. |
| `code/configs/hparams` | contract | live | `_system/governance/REPRODUCIBILITY.md:84` (current instruction). |
| `code/configs/probes` | contract | live | `code/lab/deployment/e1_probe.py:17` (literal). |
| `code/configs/screens` | contract | live | `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:83` (current instruction). |
| `code/gates` | factory | live | `.codex/hooks/stop_gate.py:24` (hook, config, or CI reference). |
| `code/gates/CONTEXT.md` | catalog | ghost | No binding or historical referrer found. Search S with this path. |
| `code/gates/closeout_check.py` | factory | live | `_system/governance/AUTONOMY.md:26` (current instruction). |
| `code/gates/closeout_fingerprints.json` | contract | live | `_system/governance/DISCIPLINE.md:49` (current instruction). |
| `code/gates/experiment_gate.py` | factory | live | `.codex/hooks/stop_gate.py:24` (hook, config, or CI reference). |
| `code/gates/law5_inertness_gate.py` | factory | live | `_system/governance/REPRODUCIBILITY.md:80` (current instruction). |
| `code/gates/test_closeout_check.py` | contract | ghost | No binding or historical referrer found. Search S with this path. |
| `code/lab` | factory | live | `pyproject.toml:5` (hook, config, or CI reference). |
| `code/lab/AGENTS.md` | catalog | live | `code/lab/CONTEXT.md:7` (current code guide). |
| `code/lab/CONTEXT.md` | catalog | ghost | No binding or historical referrer found. Search S with this path. |
| `code/lab/analysis` | factory | live | `_system/governance/CODEX.md:13` (current instruction). |
| `code/lab/deployment` | factory | ghost | No binding or historical referrer found. Search S with this path. |
| `code/lab/governance` | factory | live | `pyproject.toml:28` (hook, config, or CI reference). |
| `code/lab/infra_scripts` | factory | ghost | No binding or historical referrer found. Search S with this path. |
| `code/lab/runners` | factory | live | `CLAUDE.md:32` (current instruction). |
| `code/lab/scale` | factory | live | `_system/governance/REPRODUCIBILITY.md:34` (current instruction). |
| `code/lab/track_a` | factory | live | `_system/governance/REPRODUCIBILITY.md:36` (current instruction). |
| `code/lab/track_b` | factory | live | `pyproject.toml:5` (hook, config, or CI reference). |
| `code/lab/track_c` | factory | live | `README.md:89` (current instruction). |
| `code/lab/track_d` | factory | live | `_system/governance/REPRODUCIBILITY.md:46` (current instruction). |
| `code/lab/track_e` | factory | live | `program/runbook/00-entry-point-read-first-every-session.md:31` (current instruction). |
| `code/memit` | factory | live | `.codex/hooks/pre_tool_use_policy.py:20` (hook, config, or CI reference). |
| `code/memit/CONTEXT.md` | catalog | ghost | No binding or historical referrer found. Search S with this path. |
| `code/memit/engine_fingerprint.py` | factory | live | `_system/governance/DISCIPLINE.md:122` (current instruction). |
| `code/memit/patches` | factory | leftover | `code/memit/provenance/memit-patches-canonical.md:1212` (historical referrer). |
| `code/memit/precompute_cov_l9_12.py` | factory | live | `code/memit/patches/p8c_spawn_safe_workers.py:27` (literal). |
| `code/memit/provenance` | catalog | leftover | `_system/governance/REPRODUCIBILITY.md:9` (sealed source history). |
| `code/memit/vendor` | product | live | `.codex/hooks/pre_tool_use_policy.py:20` (hook, config, or CI reference). |
| `code/ops` | factory | live | `_system/governance/MERGING.md:7` (current instruction). |
| `code/ops/CONTEXT.md` | catalog | ghost | No binding or historical referrer found. Search S with this path. |
| `code/ops/backup` | factory | live | `program/runbook/03-operational-hygiene-runpod-gpu-memory-disk.md:34` (current instruction). |
| `code/ops/git` | factory | live | `_system/governance/MERGING.md:7` (current instruction). |
| `code/ops/intel` | factory | live | `code/lab/runners/c10w_p2_gate.py:38` (literal). |
| `code/research` | factory | live | `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:69` (current instruction). |
| `code/research/CONTEXT.md` | catalog | ghost | No binding or historical referrer found. Search S with this path. |
| `code/research/connected_papers_fetch.py` | factory | ghost | No binding or historical referrer found. Search S with this path. |
| `code/research/connected_papers_index.py` | factory | ghost | No binding or historical referrer found. Search S with this path. |
| `code/research/openresearch_archive.py` | factory | live | `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:69` (current instruction). |
| `code/research/orx_api.py` | factory | ghost | No binding or historical referrer found. Search S with this path. |
| `code/research/orx_messages.py` | factory | ghost | No binding or historical referrer found. Search S with this path. |
| `code/research/visualization` | factory | ghost | No binding or historical referrer found. Search S with this path. |
| `code/state` | factory | live | `.github/workflows/ci.yml:35` (hook, config, or CI reference). |
| `code/state/ANTI_DRIFT.md` | catalog | live | `code/state/CONTEXT.md:5` (current code guide). |
| `code/state/CONTEXT.md` | catalog | live | `code/state/build_index.py:89` (neighbor literal). |
| `code/state/build_index.py` | factory | live | `CLAUDE.md:51` (current instruction). |
| `code/state/llmdb_records.py` | factory | live | `program/runbook/CONTEXT.md:6` (current instruction). |
| `code/state/render_state.py` | factory | live | `.github/workflows/ci.yml:35` (hook, config, or CI reference). |
| `code/state/resolve_path.py` | factory | live | `CLAUDE.md:35` (current instruction). |
| `code/state/test_build_index.py` | contract | ghost | No binding or historical referrer found. Search S with this path. |
| `code/state/test_llmdb_records.py` | contract | ghost | No binding or historical referrer found. Search S with this path. |
| `code/state/test_render_state.py` | contract | ghost | No binding or historical referrer found. Search S with this path. |
| `code/state/test_resolve_path.py` | contract | ghost | No binding or historical referrer found. Search S with this path. |
| `code/tests` | factory | live | `code/ops/CONTEXT.md:6` (current code guide). |
| `code/tests/CONTEXT.md` | catalog | ghost | No binding or historical referrer found. Search S with this path. |
| `code/tests/test_dashboard_host_runner.py` | contract | ghost | No binding or historical referrer found. Search S with this path. |
| `code/tests/test_dashboard_live_host.py` | contract | live | `code/tests/test_dashboard_host_runner.py:12` (literal). |
| `code/tests/test_dashboard_live_refresh.py` | contract | live | `code/tests/test_dashboard_live_host.py:186` (literal). |
| `code/tests/test_git_automation.py` | contract | live | `code/ops/CONTEXT.md:6` (current code guide). |
| `code/tests/test_new1_construction_diag.py` | contract | ghost | No binding or historical referrer found. Search S with this path. |
| `code/tests/test_new1_dispatch.py` | contract | ghost | No binding or historical referrer found. Search S with this path. |
| `code/tests/test_new1_geometry.py` | contract | ghost | No binding or historical referrer found. Search S with this path. |
| `code/tests/test_new1_identity_diag.py` | contract | live | `code/tests/test_new1_construction_diag.py:1288` (import). |
| `code/tests/test_new1_supervisor.py` | contract | ghost | No binding or historical referrer found. Search S with this path. |

## Nouns

Source lines prove each kind exists. Wiring evidence selects the universe. Scope patterns name families. They do not create card bodies.

| Name | Owning source | Product name | Cluster | Universe and evidence | Scope |
|---|---|---|---|---|---|
| Agent catalog twins | `code/agents/twins.py:8` | AGENTS.md and routing.md | agent-tools | live: `.github/workflows/ci.yml:37` (hook, config, or CI reference). | Root catalog copies; MAESTRO generates map copies. |
| Skill package | `code/agents/skills/experiment-gate/SKILL.md:1` | skill package | agent-tools | live: `.codex/hooks/session_start.py:19` (prints installed skill names). | code/agents/skills/*/SKILL.md; code/agents/skills/*/*.skill |
| Backup evidence archive manifest | `code/ops/backup/backup_gdrive_status.py:433` | manifest.json | backup | live: `code/apps/dashboard/dashboard_storage.py:20` (import). | This kind only. |
| Backup exclusion rules | `code/ops/backup/backup_mirror.excludes:1` | exclude list | backup | live: `code/ops/backup/backup_gdrive.sh:9` (neighbor literal). | This kind only. |
| Backup heartbeat | `code/ops/backup/backup_gdrive_status.py:200` | heartbeat record | backup | live: `code/apps/dashboard/dashboard_storage.py:20` (import). | This kind only. |
| Backup schedule | `code/ops/backup/launchd/com.rhu.memit-gdrive-backup.plist:1` | LaunchAgent | backup | live: `code/ops/backup/test_backup_gdrive_addendum.py:2521` (literal). | code/ops/backup/launchd/*.plist |
| Backup unresolved state | `code/ops/backup/backup_gdrive_status.py:293` | unresolved.json | backup | live: `code/apps/dashboard/dashboard_storage.py:20` (import). | This kind only. |
| Live observation | `code/apps/dashboard/dashboard_queue.py:210` | Live | dashboard | live: `code/apps/dashboard/test_dashboard_queue.py:26` (literal). | This kind only. |
| Queue | `code/apps/dashboard/dashboard_queue.py:69` | Queue | dashboard | live: `code/apps/dashboard/test_dashboard_queue.py:26` (literal). | This kind only. |
| QueueInput | `code/apps/dashboard/dashboard_queue.py:84` | same | dashboard | live: `code/apps/dashboard/test_dashboard_queue.py:26` (literal). | This kind only. |
| Team supervisor | `code/apps/dashboard/dashboard_live.py:465` | TeamSupervisor | dashboard | live: `code/apps/dashboard/dashboard_active.py:76` (import). | This kind only. |
| Work item | `code/apps/dashboard/dashboard_queue.py:53` | WorkItem | dashboard | live: `code/apps/dashboard/test_dashboard_queue.py:26` (literal). | This kind only. |
| CounterFact dataset | `code/memit/vendor/dsets/counterfact.py:13` | CounterFactDataset | edit-engine | live: `code/memit/vendor/dsets/__init__.py:2` (import). | This kind only. |
| Engine patch provenance | `code/memit/provenance/memit-patches-canonical.md:1` | patch record | edit-engine | leftover: `_system/governance/REPRODUCIBILITY.md:9` (sealed source history). | code/memit/provenance/** |
| Engine trace | `code/memit/vendor/util/nethook.py:19` | Trace | edit-engine | live: `code/lab/track_c/c10k_keying_ablation_keygram.py:28` (import). | This kind only. |
| Fine-tune parameters | `code/memit/vendor/baselines/ft/ft_hparams.py:8` | FTHyperParams | edit-engine | live: `code/memit/vendor/baselines/ft/ft_main.py:9` (import). | This kind only. |
| Known facts dataset | `code/memit/vendor/dsets/knowns.py:13` | KnownsDataset | edit-engine | live: `code/memit/vendor/dsets/__init__.py:3` (import). | This kind only. |
| MEMIT edit parameters | `code/memit/vendor/memit/memit_hparams.py:8` | MEMITHyperParams | edit-engine | live: `code/gates/law5_inertness_gate.py:18` (import). | This kind only. |
| MEND edit parameters | `code/memit/vendor/baselines/mend/mend_hparams.py:7` | MENDHyperParams | edit-engine | live: `code/memit/vendor/baselines/mend/__init__.py:1` (import). | This kind only. |
| ROME edit parameters | `code/memit/vendor/rome/rome_hparams.py:8` | ROMEHyperParams | edit-engine | live: `code/memit/vendor/rome/compute_u.py:12` (import). | This kind only. |
| Running statistic | `code/memit/vendor/util/runningstats.py:144` | Stat | edit-engine | live: `code/lab/runners/new1_identity_diag.py:30` (literal). | This kind only. |
| Experiment edit configuration | `code/configs/hparams/qwen25_3b_memit_hparams.json:1` | hparams | experiment-configs | live: `_system/governance/REPRODUCIBILITY.md:84` (current instruction). | code/configs/hparams/* |
| Probe collection | `code/configs/probes/b3_probes.json:1` | probe set | experiment-configs | live: `code/lab/deployment/e1_probe.py:17` (literal). | code/configs/probes/*.json |
| Screen stimulus collection | `code/configs/screens/g6_screen_qwen3b.json:1` | screen set | experiment-configs | live: `code/apps/mathlab/mathlab_harvest.py:37` (literal). | code/configs/screens/*.json |
| Closeout fingerprint registry | `code/gates/closeout_fingerprints.json:1` | fingerprint registry | gates | live: `_system/governance/DISCIPLINE.md:49` (current instruction). | This kind only. |
| Closeout requirement | `code/gates/closeout_check.py:36` | closeout record | gates | live: `_system/governance/AUTONOMY.md:26` (current instruction). | This kind only. |
| Git deadline | `code/ops/git/git_hygiene.py:23` | Deadline | git-operations | live: `code/ops/git/git_merge_gate.py:18` (import). | This kind only. |
| Git merge report | `code/ops/git/git_merge_gate.py:143` | merge report | git-operations | live: `_system/governance/MERGING.md:7` (current instruction). | This kind only. |
| Git repository adapter | `code/ops/git/git_hygiene.py:37` | Repo | git-operations | live: `code/ops/git/git_merge_gate.py:18` (import). | This kind only. |
| GitHub adapter | `code/ops/git/git_hygiene.py:95` | Gh | git-operations | live: `code/ops/git/git_merge_gate.py:18` (import). | This kind only. |
| Governance authorization gate | `code/lab/governance/cp1_governed_write.py:165` | PatchAuthorizationGate | governance-prototypes | ghost: No binding or historical referrer found. Search S with this path. | This kind only. |
| Governance ledger prototype | `code/lab/governance/g1_two_phase_commit.py:57` | StateLedger | governance-prototypes | ghost: No binding or historical referrer found. Search S with this path. | This kind only. |
| Governance transaction controller | `code/lab/governance/g1_two_phase_commit.py:201` | TransactionController | governance-prototypes | ghost: No binding or historical referrer found. Search S with this path. | This kind only. |
| Intel transfer controller | `code/ops/intel/memit_intel_copy.py:176` | Controller | intel-transfer | live: `code/lab/runners/test_c10w_p2_gate.py:32` (literal). | This kind only. |
| Intel transfer manifest | `code/ops/intel/memit_intel_copy.py:193` | manifest.jsonl.gz | intel-transfer | live: `code/lab/runners/test_c10w_p2_gate.py:32` (literal). | This kind only. |
| Intel transfer receipt | `code/ops/intel/memit_intel_receive.py:247` | receipt.json | intel-transfer | live: `code/ops/intel/memit_intel_copy.py:361` (receiver source passed to runner). | Receiver fields. Local copy: `code/ops/intel/memit_intel_copy.py:500`. |
| LabViz card reader | `code/apps/labviz/cards.py:458` | Reader | labviz | live: `code/apps/labviz/build.py:161` (import). | This kind only. |
| LabViz presentation data | `code/apps/labviz/gates.json:1` | presentation data | labviz | live: `code/apps/labviz/cards.py:920` (literal). | code/apps/labviz/*.json |
| LabViz program context | `code/apps/labviz/context.py:141` | Program | labviz | live: `code/apps/labviz/cards.py:460` (import). | This kind only. |
| MathLab budget | `code/apps/mathlab/mathlab_runtime.py:115` | Budget | mathlab | live: `code/apps/mathlab/core.py:8` (import). | This kind only. |
| MathLab calibration record | `code/apps/mathlab/core.py:295` | calibration.json | mathlab | live: `code/apps/mathlab/m2_solve_repro.py:19` (import). | This kind only. |
| MathLab event envelope | `code/apps/mathlab/mathlab_events.py:60` | event envelope | mathlab | live: `code/apps/dashboard/dashboard_live.py:291` (import). | This kind only. |
| MathLab event kind | `code/apps/mathlab/mathlab_events.py:43` | event type | mathlab | live: `code/apps/dashboard/dashboard_live.py:291` (import). | All 12 FIELDS keys. |
| MathLab event stream | `code/apps/mathlab/mathlab_events.py:206` | events.jsonl | mathlab | live: `code/apps/dashboard/dashboard_live.py:291` (import). | This kind only. |
| MathLab gate plan | `code/apps/mathlab/mathlab_events.py:62` | gate plan | mathlab | live: `code/apps/dashboard/dashboard_live.py:291` (import). | This kind only. |
| MathLab harvest manifest | `code/apps/mathlab/mathlab_harvest.py:630` | manifest.json | mathlab | live: `code/apps/dashboard/dashboard_live.py:89` (literal). | This kind only. |
| MathLab reproduction manifest | `code/apps/mathlab/core.py:232` | manifest.json | mathlab | live: `code/apps/mathlab/m2_solve_repro.py:19` (import). | This kind only. |
| MathLab run | `code/apps/mathlab/mathlab_runtime.py:142` | Run | mathlab | live: `code/apps/mathlab/core.py:8` (import). | This kind only. |
| Terminal publication | `code/apps/mathlab/mathlab_events.py:133` | TerminalPublication | mathlab | live: `code/apps/dashboard/dashboard_live.py:291` (import). | This kind only. |
| Connected Papers index | `code/research/connected_papers_index.py:54` | connected papers index JSON | research-tools | ghost: No binding or historical referrer found. Search S with this path. | This kind only. |
| OpenResearch experiments | `code/research/openresearch_archive.py:101` | experiments.json | research-tools | live: `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:69` (current instruction). | This kind only. |
| OpenResearch sessions | `code/research/openresearch_archive.py:100` | sessions.json | research-tools | live: `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:69` (current instruction). | This kind only. |
| OpenResearch text index | `code/research/openresearch_archive.py:102` | text_index.jsonl | research-tools | live: `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:69` (current instruction). | This kind only. |
| Autonomy mission | `code/lab/runners/autonomy_mission.json:1` | mission record | run-control | live: `_system/governance/AUTONOMY.md:36` (current instruction). | This kind only. |
| NEW-1 controller | `code/lab/runners/new1_supervisor.py:201` | Controller | run-control | live: `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:159` (current instruction). | This kind only. |
| NEW-1 dispatch receipt | `code/lab/runners/new1_dispatch_report.py:126` | dispatch_receipt.json | run-control | live: `code/lab/runners/new1_dispatch.sh:305` (literal). | This kind only. |
| NEW-1 resource owner | `code/lab/runners/new1_supervisor.py:377` | ResourceOwner | run-control | live: `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:159` (current instruction). | This kind only. |
| NEW-1 resource sample | `code/lab/runners/new1_supervisor.py:47` | Sample | run-control | live: `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:159` (current instruction). | This kind only. |
| NEW-1 spectrum | `code/lab/runners/new1_geometry.py:61` | Spectrum | run-control | live: `code/lab/runners/new1_dispatch.sh:257` (literal). | This kind only. |
| C10 session state | `code/lab/track_c/c10z_astra_arms.py:487` | Session | science-harnesses | leftover: `map/group-b-leftovers.md:55` (closed script). | This kind only. |
| C10 stage state | `code/lab/track_c/c10z_astra_arms.py:156` | StageState | science-harnesses | leftover: `map/group-b-leftovers.md:55` (closed script). | This kind only. |
| C10 telemetry record | `code/lab/track_c/c10z_astra_arms.py:378` | Telemetry | science-harnesses | leftover: `map/group-b-leftovers.md:55` (closed script). | This kind only. |
| Anchor map | `code/state/build_index.py:163` | anchor-map.tsv | state-records | live: `CLAUDE.md:51` (current instruction). | This kind only. |
| Generated indexes | `code/state/build_index.py:82` | _index views | state-records | live: `CLAUDE.md:51` (current instruction). | This kind only. |
| ICM record status | `code/state/build_index.py:14` | record status | state-records | live: `CLAUDE.md:51` (current instruction). | This kind only. |
| Lab runtime namespaces | `code/state/llmdb_records.py:11` | ml and new1 runs | state-records | live: `program/runbook/CONTEXT.md:6` (current instruction). | This kind only. |
| NEW-1 dispatch namespace | `code/state/llmdb_records.py:13` | dispatch receipt folder | state-records | live: `program/runbook/CONTEXT.md:6` (current instruction). | This kind only. |
| Path map row | `code/state/build_index.py:15` | old/new/disposition/unit | state-records | live: `CLAUDE.md:51` (current instruction). | This kind only. |
| Program scorecard view | `code/state/render_state.py:71` | program/scorecard.md | state-records | live: `.github/workflows/ci.yml:35` (hook, config, or CI reference). | This kind only. |
| Program state view | `code/state/render_state.py:71` | generated program-state block | state-records | live: `.github/workflows/ci.yml:35` (hook, config, or CI reference). | This kind only. |
| Program summary view | `code/state/render_state.py:50` | program/STATUS.md | state-records | live: `.github/workflows/ci.yml:35` (hook, config, or CI reference). | This kind only. |
| Record run namespace | `code/state/llmdb_records.py:16` | run folder | state-records | live: `program/runbook/CONTEXT.md:6` (current instruction). | This kind only. |

## Name collisions

| Name | Meanings and sources |
|---|---|
| Controller | NEW-1 resource controller: `code/lab/runners/new1_supervisor.py:201`. Intel transfer controller: `code/ops/intel/memit_intel_copy.py:176`. |
| Deadline / Budget | Git deadline: `code/ops/git/git_hygiene.py:23`. MathLab budget: `code/apps/mathlab/mathlab_runtime.py:115`. C10 stage budgets remain source-local in code/lab/track_c/. |
| StateLedger | Governance prototype family: `code/lab/governance/g1_two_phase_commit.py:57`, `code/lab/governance/cp1_governed_write.py:75`, `code/lab/governance/g2_security_layer.py:66`. Readback prototype: `code/lab/track_e/r1_commit_bit_select.py:16`. These implementations have separate owners. |
| manifest.json | MathLab harvest: `code/apps/mathlab/mathlab_harvest.py:630`. MathLab reproduction: `code/apps/mathlab/core.py:291`. Backup evidence archive: `code/ops/backup/backup_gdrive_status.py:433`. |
| Receipt | Intel receipt fields: `code/ops/intel/memit_intel_receive.py:247`. Local copy: `code/ops/intel/memit_intel_copy.py:500`. NEW-1 dispatch_receipt.json: `code/lab/runners/new1_dispatch_report.py:198`. |
| Program / state | LabViz Program: `code/apps/labviz/context.py:141`. Program state view: `code/state/render_state.py:71`. The stored program state is outside this map. |
| Parameters | MEMIT, ROME, fine-tune, and MEND parameter types each have their own noun row. Experiment configuration files are a separate family. |

## Verbs

These candidates name repeated movements and their source entry points. They do not define process contracts. No process cards ship in v2.

| Movement | Entry point | Universe and evidence |
|---|---|---|
| Build indexes | `code/state/build_index.py:198` | live: `CLAUDE.md:51` (current instruction). |
| Render state | `code/state/render_state.py:118` | live: `.github/workflows/ci.yml:35` (hook, config, or CI reference). |
| Resolve an old path | `code/state/resolve_path.py:91` | live: `CLAUDE.md:35` (current instruction). |
| Check closeout | `code/gates/closeout_check.py:1` | live: `_system/governance/AUTONOMY.md:26` (current instruction). |
| Prepare or check an experiment package | `code/gates/experiment_gate.py:1` | live: `.codex/hooks/stop_gate.py:24` (hook, config, or CI reference). |
| Check inertness | `code/gates/law5_inertness_gate.py:33` | live: `_system/governance/REPRODUCIBILITY.md:80` (current instruction). |
| Read or publish event stream | `code/apps/mathlab/mathlab_events.py:144` | live: `code/apps/dashboard/dashboard_live.py:291` (import). |
| Harvest MathLab inputs | `code/apps/mathlab/mathlab_harvest.py:1` | live: `code/apps/dashboard/dashboard_live.py:89` (literal). |
| Reproduce MathLab captures | `code/apps/mathlab/core.py:232` | live: `code/apps/mathlab/m2_solve_repro.py:19` (import). |
| Calibrate MathLab estimates | `code/apps/mathlab/core.py:295` | live: `code/apps/mathlab/m2_solve_repro.py:19` (import). |
| Refresh dashboard queue | `code/apps/dashboard/dashboard_queue.py:614` | live: `code/apps/dashboard/test_dashboard_queue.py:26` (literal). |
| Build LabViz view | `code/apps/labviz/build.py:1` | live: `code/apps/labviz/cards.py:492` (import). |
| Enforce NEW-1 resource limits | `code/lab/runners/new1_supervisor.py:1` | live: `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:159` (current instruction). |
| Build NEW-1 dispatch receipt | `code/lab/runners/new1_dispatch_report.py:194` | live: `code/lab/runners/new1_dispatch.sh:305` (literal). |
| Run bounded autonomy units | `code/lab/runners/autonomy_driver.py:1` | live: `CLAUDE.md:32` (current instruction). |
| Run advisor review | `code/agents/claude_advisor.sh:1` | live: `.codex/hooks/session_start.py:21` (hook, config, or CI reference). |
| Check engine fingerprint | `code/memit/engine_fingerprint.py:39` | live: `_system/governance/DISCIPLINE.md:122` (current instruction). |
| Replay engine patches | `code/memit/patches/replay_provenance.sh:1` | ghost: No binding or historical referrer found. Search S with this path. |
| Copy recovery objects to Drive | `code/ops/backup/backup_gdrive.sh:1` | live: `code/ops/backup/test_backup_gdrive.py:15` (literal). |
| Read or publish backup health | `code/ops/backup/backup_gdrive_status.py:648` | live: `code/apps/dashboard/dashboard_storage.py:20` (import). |
| Gate Git merge | `code/ops/git/git_merge_gate.py:327` | live: `_system/governance/MERGING.md:7` (current instruction). |
| Check Git hygiene | `code/ops/git/git_hygiene.py:440` | live: `code/ops/git/git_merge_gate.py:18` (import). |
| Collect Intel transfer | `code/ops/intel/memit_intel_copy.py:508` | live: `code/lab/runners/test_c10w_p2_gate.py:32` (literal). |
| Receive Intel transfer | `code/ops/intel/memit_intel_receive.py:1` | live: `code/ops/intel/memit_intel_copy.py:361` (literal). |
| Archive OpenResearch chats | `code/research/openresearch_archive.py:59` | live: `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:69` (current instruction). |
| Fetch Connected Papers graph | `code/research/connected_papers_fetch.py:1` | ghost: No binding or historical referrer found. Search S with this path. |
| Build Connected Papers index | `code/research/connected_papers_index.py:1` | ghost: No binding or historical referrer found. Search S with this path. |
| Compute experiment statistics | `code/lab/analysis/stats.py:1` | live: `_system/governance/CODEX.md:13` (current instruction). |
| Estimate experiment power | `code/lab/analysis/power.py:1` | live: `_system/governance/CODEX.md:13` (current instruction). |

## Outside referrers

Counts use matching source lines, not individual target strings. A line with several code paths counts once. All sections use the saved raw rg scan. Full tables retain missing targets as ghost references. They do not make those targets live.

### Executable and config referrers — full

| Referrer | Targets |
|---|---|
| `pyproject.toml:5` | `code/lab/track_b/b3_verdict.py` |
| `pyproject.toml:16` | `code/lab/`; `code/memit/vendor` |
| `pyproject.toml:28` | `code/lab/governance/` |
| `.codex/skills/advisor-review/SKILL.md:24` | `code/agents/claude_advisor.sh` |
| `.codex/skills/advisor-review/SKILL.md:32` | `code/agents/claude_advisor.sh` |
| `.codex/skills/advisor-review/SKILL.md:37` | code/diff [ghost reference] |
| `.codex/skills/advisor-review/SKILL.md:49` | `code/agents/advisor_review_prompt.md` |
| `.codex/skills/advisor-review/SKILL.md:56` | `code/agents/advisor_review_prompt.md` |
| `.codex/hooks/session_start.py:21` | `code/agents/claude_advisor.sh` |
| `.codex/hooks/session_start.py:23` | `code/agents/codex_context_guard.py` |
| `.codex/hooks/pre_tool_use_policy.py:20` | `code/memit/vendor/` |
| `.codex/hooks/pre_tool_use_policy.py:21` | `code/memit/vendor` |
| `.codex/hooks/stop_gate.py:13` | `code/agents/codex_context_guard.py` |
| `.codex/hooks/stop_gate.py:23` | `code/agents/claude_advisor.sh` |
| `.codex/hooks/stop_gate.py:24` | `code/gates/experiment_gate.py` |
| `.github/workflows/ci.yml:35` | `code/state/render_state.py` |
| `.github/workflows/ci.yml:37` | `code/agents/twins.py` |

DESIGN.md lines 238–247 supply the outside-repo referrers below. They do not supply host proof. Only the memory-key item names a literal code path. The other items need a host probe before target assignment.

| Outside referrer | Target from DESIGN.md | Evidence |
|---|---|---|
| core.hooksPath | No literal code target | outside repo, from DESIGN.md:239 |
| Both settings files | No literal code target | outside repo, from DESIGN.md:240 |
| Backup LaunchAgent and script | No literal code target | outside repo, from DESIGN.md:241 |
| Codex trust configuration | No literal code target | outside repo, from DESIGN.md:242 |
| Toolkit configuration and run scripts | No literal code target | outside repo, from DESIGN.md:243 |
| tmux environment and dashboard panes | No literal code target | outside repo, from DESIGN.md:244 |
| Memory key in closeout checker | `code/gates/closeout_check.py` (source line 253 in the design) | outside repo, from DESIGN.md:245; checker itself is inside the repo |
| Autoresearch virtual environment links | No literal code target | outside repo, from DESIGN.md:246 |
| Absolute mirror-path consumers | No literal code target | outside repo, from DESIGN.md:247 |

### Current instructions — full

| Referrer | Targets |
|---|---|
| `CLAUDE.md:22` | `code/` |
| `CLAUDE.md:32` | `code/lab/runners/autonomy_driver.py` |
| `CLAUDE.md:35` | `code/state/resolve_path.py` |
| `CLAUDE.md:46` | `code/CONTEXT.md` |
| `CLAUDE.md:47` | `code/` |
| `CLAUDE.md:51` | `code/state/build_index.py` |
| `README.md:87` | `code/lab/track_b/b3_verdict.py` |
| `README.md:89` | `code/lab/track_c/c2_key_collinearity.py` |
| `README.md:111` | `code/configs/` |
| `_system/governance/AUTONOMY.md:13` | `code/lab/runners/autonomy_driver.py` |
| `_system/governance/AUTONOMY.md:16` | `code/agents/codex_context_guard.py` |
| `_system/governance/AUTONOMY.md:26` | `code/gates/closeout_check.py` |
| `_system/governance/AUTONOMY.md:36` | `code/lab/runners/autonomy_mission.json` |
| `_system/governance/AUTONOMY.md:39` | `code/lab/runners/autonomy_mission.json` |
| `_system/governance/AUTONOMY.md:49` | `code/lab/track_c/band_corruption_compare.py` |
| `_system/governance/AUTONOMY.md:58` | `code/lab/runners/autonomy_driver.py` |
| `_system/governance/AUTONOMY.md:59` | `code/lab/runners/autonomy_mission.json` |
| `_system/governance/AUTONOMY.md:68` | `code/lab/runners/autonomy_driver.py`; `code/lab/runners/autonomy_mission.json` |
| `_system/governance/AUTONOMY.md:84` | `code/lab/track_c/autoresearch_c10/launch.sh` |
| `_system/governance/AUTONOMY.md:87` | `code/lab/track_c/autoresearch_band_search/` |
| `_system/governance/AUTONOMY.md:103` | `code/lab/runners/autonomy_driver.py`; `code/lab/runners/autonomy_mission.json` |
| `_system/governance/AUTONOMY.md:105` | `code/lab/runners/autonomy_driver.py` |
| `_system/governance/AUTONOMY.md:107` | `code/gates/closeout_check.py` |
| `_system/governance/AUTONOMY.md:109` | `code/lab/runners/autonomy_mission.json` |
| `_system/governance/AUTONOMY.md:110` | `code/agents/claude_advisor.sh` |
| `_system/governance/WORKFLOWS_OVERVIEW.md:65` | `code/gates/closeout_check.py` |
| `_system/governance/WORKFLOWS_OVERVIEW.md:66` | `code/ops/git/hooks/pre-commit` |
| `_system/governance/WORKFLOWS_OVERVIEW.md:75` | `code/lab/runners/autonomy_driver.py` |
| `_system/governance/WORKFLOWS_OVERVIEW.md:82` | `code/agents/codex_context_guard.py` |
| `_system/governance/WORKFLOWS_OVERVIEW.md:92` | `code/lab/track_c/autoresearch_c10/launch.sh` |
| `_system/governance/WORKFLOWS_OVERVIEW.md:107` | `code/gates/closeout_check.py`; `code/state/render_state.py` |
| `_system/governance/WORKFLOWS_OVERVIEW.md:137` | `code/gates/closeout_check.py` |
| `_system/governance/WORKFLOWS_OVERVIEW.md:175` | `code/gates/closeout_check.py`; `code/state/render_state.py` |
| `_system/governance/WORKFLOWS_OVERVIEW.md:176` | `code/ops/git/hooks/pre-commit` |
| `_system/governance/REPRODUCIBILITY.md:9` | `code/memit/engine_fingerprint.py`; `code/memit/provenance/memit-patches-canonical.md`; `code/memit/vendor` |
| `_system/governance/REPRODUCIBILITY.md:10` | code/vendor/external_prior_art/larql/target/release/larql [ghost reference]; code/vendor/llama_cpp_src/ [ghost reference] |
| `_system/governance/REPRODUCIBILITY.md:19` | `code/memit/vendor` |
| `_system/governance/REPRODUCIBILITY.md:34` | `code/lab/scale/g6_scale_n.py` |
| `_system/governance/REPRODUCIBILITY.md:35` | `code/lab/scale/g6_scale_n.py` |
| `_system/governance/REPRODUCIBILITY.md:36` | `code/lab/track_a/a2_relbal_sentinels.py` |
| `_system/governance/REPRODUCIBILITY.md:37` | `code/lab/track_a/a2b_refresh_ks.py` |
| `_system/governance/REPRODUCIBILITY.md:38` | `code/lab/scale/g6_scale_n_param.py` |
| `_system/governance/REPRODUCIBILITY.md:39` | `code/lab/track_b/b3_run.sh` |
| `_system/governance/REPRODUCIBILITY.md:40` | `code/lab/track_b/b3_verdict.py` |
| `_system/governance/REPRODUCIBILITY.md:42` | `code/lab/track_a/a7_bias_ablation.py` |
| `_system/governance/REPRODUCIBILITY.md:43` | `code/lab/track_c/c2_key_collinearity.py` |
| `_system/governance/REPRODUCIBILITY.md:44` | `code/lab/track_c/c2b_depth_map.py` |
| `_system/governance/REPRODUCIBILITY.md:45` | `code/lab/track_c/band_corruption_compare.py` |
| `_system/governance/REPRODUCIBILITY.md:46` | `code/lab/track_d/d1_predictor_map.py` |
| `_system/governance/REPRODUCIBILITY.md:47` | `code/lab/track_b/b1_size_dose_response.py` |
| `_system/governance/REPRODUCIBILITY.md:48` | `code/lab/track_d/d1_threshold_instrument.py` |
| `_system/governance/REPRODUCIBILITY.md:49` | `code/lab/governance/` |
| `_system/governance/REPRODUCIBILITY.md:51` | `code/lab/runners/run_c10z_v7_diag.py` |
| `_system/governance/REPRODUCIBILITY.md:52` | `code/lab/track_c/c10z_astra_benchmark.py` |
| `_system/governance/REPRODUCIBILITY.md:53` | `code/lab/track_c/c10z_astra_read.py` |
| `_system/governance/REPRODUCIBILITY.md:54` | `code/apps/mathlab/m3_calibration.py`; `code/apps/mathlab/run_mathlab_cpu.sh` |
| `_system/governance/REPRODUCIBILITY.md:56` | `code/apps/mathlab/m2_solve_repro.py`; `code/apps/mathlab/run_mathlab_cpu.sh` |
| `_system/governance/REPRODUCIBILITY.md:57` | `code/apps/mathlab/run_mathlab_harvest.sh` |
| `_system/governance/REPRODUCIBILITY.md:70` | `code/lab/track_c/c10e_bandknob.py` |
| `_system/governance/REPRODUCIBILITY.md:72` | `code/lab/track_c/c10f_band412.py` |
| `_system/governance/REPRODUCIBILITY.md:74` | `code/lab/track_c/c10g_strength_layer_sweep.py` |
| `_system/governance/REPRODUCIBILITY.md:76` | `code/lab/track_c/c10h_anyedit_pilot.py` |
| `_system/governance/REPRODUCIBILITY.md:78` | `code/lab/scale/g6_scale_n.py`; `code/lab/track_c/c2_key_collinearity.py` |
| `_system/governance/REPRODUCIBILITY.md:80` | `code/gates/law5_inertness_gate.py` |
| `_system/governance/REPRODUCIBILITY.md:82` | `code/lab/track_b/b3_edit_and_save.py`; `code/lab/track_b/b3_expand_native.py`; `code/lab/track_b/b3_run.sh`; code/vendor/llama_cpp_src/build/bin [ghost reference] |
| `_system/governance/REPRODUCIBILITY.md:84` | `code/configs/hparams/qwen25_3b_memit_hparams.json`; `code/lab/track_c/c10e_bandknob.py`; `code/lab/track_c/c10l_covgeom_p6_zinject.py`; `code/lab/track_c/c10l_covgeom_step0.py` |
| `_system/governance/REPRODUCIBILITY.md:86` | code/closed-runners/c10l_mint_p4.sh [ghost reference]; `code/lab/track_c/c10l_mint_arms.py`; `code/lab/track_c/c10l_mint_step0.py` |
| `_system/governance/REPRODUCIBILITY.md:87` | `code/lab/track_c/c10l_mint_arms.py`; `code/lab/track_c/c10l_mint_step0.py`; `code/lab/track_c/c10m_diag_arms.py` |
| `_system/governance/REPRODUCIBILITY.md:88` | `code/lab/track_c/c10n_ztransport_arms.py` |
| `_system/governance/REPRODUCIBILITY.md:89` | `code/lab/track_c/c10o_magnitude_arms.py` |
| `_system/governance/REPRODUCIBILITY.md:90` | `code/lab/track_c/c10p_twopass_arms.py` |
| `_system/governance/REPRODUCIBILITY.md:91` | `code/lab/track_c/c10q_stacked_arms.py` |
| `_system/governance/REPRODUCIBILITY.md:92` | `code/lab/track_c/c10x_enginepath_arms.py`; `code/lab/track_c/c10x_enginepath_read.py` |
| `_system/governance/REPRODUCIBILITY.md:106` | `code/lab/runners/new1_dispatch.sh` |
| `_system/governance/DISCIPLINE.md:42` | `code/lab/track_c/autoresearch_c10/launch.sh` |
| `_system/governance/DISCIPLINE.md:48` | `code/gates/closeout_check.py`; `code/state/render_state.py` |
| `_system/governance/DISCIPLINE.md:49` | `code/gates/closeout_fingerprints.json`; `code/state/render_state.py` |
| `_system/governance/DISCIPLINE.md:50` | `code/gates/closeout_check.py` |
| `_system/governance/DISCIPLINE.md:84` | `code/agents/advisor_review_prompt.md`; `code/agents/claude_advisor.sh` |
| `_system/governance/DISCIPLINE.md:86` | `code/gates/closeout_check.py`; `code/gates/closeout_fingerprints.json` |
| `_system/governance/DISCIPLINE.md:88` | `code/lab/track_c/autoresearch_c10/` |
| `_system/governance/DISCIPLINE.md:94` | `code/lab/runners/autonomy_driver.py` |
| `_system/governance/DISCIPLINE.md:102` | `code/agents/claude_advisor.sh` |
| `_system/governance/DISCIPLINE.md:122` | `code/memit/engine_fingerprint.py`; `code/memit/vendor` |
| `_system/governance/DISCIPLINE.md:137` | `code/gates/closeout_check.py` |
| `_system/governance/DISCIPLINE.md:150` | `code/memit/vendor` |
| `_system/governance/DISCIPLINE.md:157` | `code/gates/closeout_check.py` |
| `_system/governance/OPERATING-MODEL.md:15` | `code/state/render_state.py` |
| `_system/governance/OPERATING-MODEL.md:22` | `code/ops/git/git_merge_gate.py` |
| `_system/governance/OPERATING-MODEL.md:41` | `code/ops/git/git_merge_gate.py` |
| `_system/governance/OPERATING-MODEL.md:71` | `code/ops/git/git_merge_gate.py` |
| `_system/governance/CODEX.md:12` | `code/gates/experiment_gate.py` |
| `_system/governance/CODEX.md:13` | `code/lab/analysis/power.py`; `code/lab/analysis/stats.py` |
| `_system/governance/CODEX.md:14` | `code/agents/claude_advisor.sh` |
| `_system/governance/CODEX.md:19` | `code/memit/vendor` |
| `_system/governance/CODEX.md:22` | `code/lab/track_c/c2_key_collinearity.py` |
| `_system/governance/CODEX.md:27` | `code/configs/` |
| `_system/governance/CODEX.md:29` | `code/lab/track_b/b3_verdict.py`; `code/lab/track_c/c2_key_collinearity.py` |
| `_system/governance/CODEX.md:37` | `code/configs/` |
| `_system/governance/CODEX.md:40` | `code/agents/claude_advisor.sh` |
| `_system/governance/MERGING.md:7` | `code/ops/git/git_merge_gate.py` |
| `_system/governance/CONTEXT.md:6` | `code/gates/closeout_check.py` |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:31` | code/vendor/external_prior_art/BetaEdit [ghost reference] |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:55` | `code/lab/track_c/autoresearch_c10/launch.sh`; code/vendor/external_prior_art/autoresearch-macos/ [ghost reference] |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:59` | `code/lab/track_c/c10u_mint2_wordlist.py` |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:61` | `code/memit/vendor` |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:67` | code/lab/track_c/c10t_secondkey_ [ghost reference] |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:69` | `code/research/openresearch_archive.py` |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:71` | code/closed-runners/run_c10u_stage_r2.sh [ghost reference]; `code/lab/track_c/c10u_mint2_arms.py` |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:72` | `code/lab/track_c/c10e_bandknob.py` |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:74` | code/closed-runners/run_c10u_stage_r3.sh [ghost reference] |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:77` | `code/lab/runners/run_c10w_stage.sh` |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:83` | `code/configs/screens`; `code/lab/track_c/` |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:86` | code/closed-runners/run_c10v_stage.sh [ghost reference] |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:89` | `code/lab/runners/c10w_p2_gate.py`; `code/lab/runners/run_c10w_p2.sh` |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:96` | `code/apps/labviz` |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:105` | `code/apps/labviz/` |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:125` | `code/ops/backup/backup_mirror.sh` |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:128` | `code/ops/git/git_merge_gate.py` |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:143` | `code/ops/git/git_merge_gate.py` |
| `program/runbook/05-decisions-ledger-accepted-eliminated-reasoning-not-hard-gate.md:159` | `code/lab/runners/new1_supervisor.py` |
| `program/runbook/06-dependency-model-sourcing-catalog.md:12` | code/vendor/external_prior_art/larql/target/release/larql [ghost reference] |
| `program/runbook/06-dependency-model-sourcing-catalog.md:22` | code/vendor/external_prior_art/BetaEdit [ghost reference] |
| `program/runbook/12-live-status-dashboard-machine-readable-head-keep-current.md:13` | `code/lab/track_c/c10x_enginepath_read.py` |
| `program/runbook/12-live-status-dashboard-machine-readable-head-keep-current.md:49` | `code/lab/track_c/r9_deletion_residue.py` |
| `program/runbook/12-live-status-dashboard-machine-readable-head-keep-current.md:51` | `code/lab/track_c/r15_constraint_probe.py` |
| `program/runbook/01-tools-instruments-available.md:12` | `code/lab/track_c/autoresearch_c10/launch.sh` |
| `program/runbook/01-tools-instruments-available.md:16` | `code/memit/vendor` |
| `program/runbook/01-tools-instruments-available.md:18` | code/vendor/external_prior_art/larql/target/release/larql [ghost reference] |
| `program/runbook/00-entry-point-read-first-every-session.md:24` | `code/lab/track_c/c10h_anyedit_pilot.py` |
| `program/runbook/00-entry-point-read-first-every-session.md:26` | `code/lab/track_c/` |
| `program/runbook/00-entry-point-read-first-every-session.md:27` | `code/lab/track_c/` |
| `program/runbook/00-entry-point-read-first-every-session.md:29` | `code/lab/governance/c6_ledger_immutability_redteam.py` |
| `program/runbook/00-entry-point-read-first-every-session.md:31` | `code/lab/track_e/r11_medium_on_read.py` |
| `program/runbook/00-entry-point-read-first-every-session.md:33` | `code/lab/track_e/r1_commit_bit_select.py` |
| `program/runbook/00-entry-point-read-first-every-session.md:35` | `code/lab/track_e/r1_select_readback.py` |
| `program/runbook/00-entry-point-read-first-every-session.md:37` | `code/lab/track_c/r9_deletion_residue.py` |
| `program/runbook/00-entry-point-read-first-every-session.md:39` | `code/lab/track_c/r15_constraint_probe.py` |
| `program/runbook/00-entry-point-read-first-every-session.md:62` | `code/configs/` |
| `program/runbook/00-entry-point-read-first-every-session.md:70` | code/vendor/external_prior_art/BetaEdit [ghost reference] |
| `program/runbook/00-entry-point-read-first-every-session.md:77` | `code/gates/closeout_check.py` |
| `program/runbook/CONTEXT.md:6` | `code/gates/closeout_check.py`; `code/state/llmdb_records.py` |
| `program/runbook/13-changelog-append-only.md:78` | code/structural [ghost reference] |
| `program/runbook/13-changelog-append-only.md:81` | code/structural [ghost reference] |
| `program/runbook/13-changelog-append-only.md:103` | code/project [ghost reference] |
| `program/runbook/13-changelog-append-only.md:304` | code/prereg [ghost reference] |
| `program/runbook/03-operational-hygiene-runpod-gpu-memory-disk.md:31` | code/inputs [ghost reference] |
| `program/runbook/03-operational-hygiene-runpod-gpu-memory-disk.md:34` | `code/ops/backup/backup_mirror.sh` |
| `program/runbook/08-experiment-decision-tree-tracks-af.md:113` | code/vendor/external_prior_art/BetaEdit [ghost reference] |
| `program/runbook/02-operating-disciplines-how-we-work-non-negotiable.md:43` | `code/gates/closeout_check.py` |
| `program/SESSION_BOOTSTRAP.md:59` | `code/memit/vendor`; code/vendor/external_prior_art/larql [ghost reference] |
| `program/SESSION_BOOTSTRAP.md:61` | `code/agents/install_infranodus_skills.sh` |

### Other referrers — counts

Run these commands from the worktree. They restore the source-line lists. Use rg --count output or count its numbered output lines to check the totals. _index/ remains a census category. It is never wiring evidence.

| Source folder | Hit lines | Regenerate list |
|---|---|---|
| _archive/ | 181 | rg -n --hidden "code/" _archive/ |
| _index/ | 596 | rg -n --hidden "code/" _index/ |
| _system/ | 1 | rg -n --hidden "code/" _system/ --glob "!_system/governance/**" --glob "!_system/memory/**" |
| _system/memory/ | 5 | rg -n --hidden "code/" _system/memory/ |
| _templates/ | 1 | rg -n --hidden "code/" _templates/ |
| evidence/ | 12 | rg -n --hidden "code/" evidence/ |
| experiments/ | 63 | rg -n --hidden "code/" experiments/ |
| knowledge/ | 85 | rg -n --hidden "code/" knowledge/ |
| program/ | 38 | rg -n --hidden "code/" program/ --glob "!program/runbook/**" --glob "!program/checkpoints/**" --glob "!program/sessions/**" --glob "!program/registers/**" --glob "!program/SESSION_BOOTSTRAP.md" |
| program/checkpoints/ | 4 | rg -n --hidden "code/" program/checkpoints/ |
| program/registers/ | 92 | rg -n --hidden "code/" program/registers/ |
| program/sessions/ | 1 | rg -n --hidden "code/" program/sessions/ |
| projects/ | 98 | rg -n --hidden "code/" projects/ |
| root files | 14 | rg -n --hidden "code/" .gitignore AGENTS.md CONTEXT.md routing.md |

### Code guide referrers

These guides name concrete code paths. A path change can make the guide wrong. Headings and generic folder text do not add edges.

| Guide | Named source |
|---|---|
| `code/CONTEXT.md:6` | `code/agents/twins.py` |
| `code/CONTEXT.md:6` | `code/state/render_state.py` |
| `code/CONTEXT.md:7` | `code/` |
| `code/agents/CONTEXT.md:5` | `code/agents/twins.py` |
| `code/agents/CONTEXT.md:6` | `code/agents/twins.py` |
| `code/configs/CONTEXT.md:6` | `code/apps/labviz/build.py` |
| `code/configs/CONTEXT.md:6` | `code/apps/labviz/cards.py` |
| `code/configs/CONTEXT.md:6` | `code/apps/mathlab/mathlab_harvest.py` |
| `code/gates/CONTEXT.md:5` | `code/gates/closeout_fingerprints.json` |
| `code/gates/CONTEXT.md:6` | `code/gates/closeout_check.py` |
| `code/gates/CONTEXT.md:6` | `code/ops/git/hooks/pre-commit` |
| `code/lab/CONTEXT.md:7` | `code/lab/AGENTS.md` |
| `code/memit/CONTEXT.md:6` | `code/agents/codex_context_guard.py` |
| `code/memit/CONTEXT.md:6` | `code/gates/law5_inertness_gate.py` |
| `code/ops/CONTEXT.md:6` | `code/tests/test_git_automation.py` |
| `code/state/CONTEXT.md:5` | `code/state/ANTI_DRIFT.md` |
| `code/state/CONTEXT.md:6` | `code/ops/git/hooks/pre-commit` |
| `code/state/CONTEXT.md:6` | `code/state/render_state.py` |

Total: 17 executable/config lines + 152 current-instruction lines + 1191 other lines = 1360 reference lines. Generic text that contains code/ but gives no path remains in the raw scan. It is not a target edge.

## Proposed clusters

| Cluster | Editor question | Nouns |
|---|---|---|
| agent-tools | Agent skill contracts | 2 |
| backup | Backup evidence and schedules | 5 |
| dashboard | Dashboard records | 5 |
| edit-engine | Engine types and patch records | 9 |
| experiment-configs | Edit, probe, and screen configuration | 3 |
| gates | Experiment and closeout boundaries | 2 |
| git-operations | Git gate types and reports | 4 |
| governance-prototypes | Governance prototype types | 3 |
| intel-transfer | Intel transfer records | 3 |
| labviz | LabViz data and readers | 3 |
| mathlab | Events, runs, captures, and estimates | 10 |
| research-tools | Research archive records | 4 |
| run-control | Run limits and dispatch | 6 |
| science-harnesses | Experiment state and telemetry | 3 |
| state-records | Record paths and generated views | 10 |

## Proposed slice 1 tree

```text
map/
├─ CLAUDE.md
├─ CONTEXT.md
├─ group-b-leftovers.md (existing; unchanged)
├─ _meta/
│  ├─ schema.md
│  └─ inventory.md
├─ _templates/
│  ├─ object.md
│  └─ process.md
└─ objects/
   ├─ CONTEXT.md
   └─ _index.md
```

Each durable kind gets one index row with status stub. Future cards can use objects/<cluster>/. Slice 1 creates no empty cluster, process, or effects folder. MAESTRO generates the entry twins.

## Review risks

CI still names the old tests and tools module paths at .github/workflows/ci.yml:39–41. This lane cannot repair CI. The renderer now owns the three views at code/state/render_state.py:18–20. These citations were refreshed against the new base.

Host hooks, external referrers, dynamic edges, and science execution remain UNVERIFIED. The slice 1 catalog walk results are in the lane report. Cards and process walks remain outside v2.
