# Memory audit — applied 2026-10-10

Applies the operator-approved audit in this folder (`README.md`, `audit_*.md`; decision: "Apply all"). Scope: `memory_mirror/` (169 notes + MEMORY.md), the live Claude memory dir `~/.claude/projects/-Volumes-memit-llm-database-poc-mirror/memory/` (LIVE), and `runbook_fixes.patch` (not applied). Nothing committed. Prior text of every tracked note: `git show fd77f7e:memory_mirror/<file>`.

## Counts

| action | notes |
|---|---|
| FIX | 60 |
| KEEP | 39 |
| SURVIVOR | 13 |
| DEINDEX | 15 |
| MERGED | 13 |
| RETIRED | 28 |
| DISAGREED-left | 1 |
| **total** | 169 |

SURVIVOR = merge target that absorbed content (13; `c10-sharedz-underfit` is also de-indexed). MERGED = absorbed into a survivor, then tombstoned. RETIRED = tombstone with pointer. Result: 41 tombstones, 128 live notes, 112 indexed, 16 live-but-de-indexed (historical).

Differences from the audit's proposed tally (keep 34 · fix 63 · de-index 14 · merge 16 · retire 42): fixes whose only ask was a style trim/shrink on a note with no wrong or stale claim were not applied (brief rule 2), so those notes count as KEEP (frontmatter-only where needed); `operator-decision-scope` stayed live (see below); `wide-intermediate-7b-editing-vram`, `perplexity-c10h-reranks-…`, `q4km-…` were de-indexed rather than retired (the audit allowed either).

## Per-file actions

| file | action taken | one-line what changed |
|---|---|---|
| anti-drift-enforce-not-autowrite.md | FIX | Frontmatter; cut 2026-06 session narrative to the 4 rules (de-dup, enforce-not-write, anchors/tracers, grep-sweep the fan-out) |
| anyedit-clearing-c10-would-close-tested-write-serve-scope.md | RETIRED | tombstone → CORPUS/42 + anyedit-port-keys; premise (AnyEdit clears C10) never occurred |
| anyedit-connectedpapers-adds-diagnostics-not-plan-change.md | RETIRED | tombstone → CORPUS/40, CORPUS/42 |
| anyedit-default-window-collapses-c10-a7.md | RETIRED | tombstone: window 1 and 50 both ran (CORPUS/40 + window-50 diagnostic), superseded by CORPUS/42 |
| anyedit-gate-upgraded-by-muke-coin-suit.md | RETIRED | tombstone → CORPUS/40/42, anyedit-port-keys, prior-art-anyeditpp |
| anyedit-is-best-remaining-c10-rescue-not-assumed-fix.md | RETIRED | tombstone: port halted CONTROLS_NOT_RECOVERED (CORPUS/42); not a live rescue |
| anyedit-local-transplant-controls-fail-before-a7.md | MERGED->anyedit-port-keys-at-last-prompt-token-no-paraphrase-transfer.md | window-1/window-50 control-collapse numbers + 'no A7 before easy controls pass' moved into survivor; tombstoned |
| anyedit-name-collision-dcdmllm-is-image-editing.md | FIX | frontmatter only (title/date/decision → name/description/type reference) + source line; verified external_prior_art/AnyEdit remote = jianghoucheng |
| anyedit-noop-gate-is-not-active-edit-parity.md | SURVIVOR | frontmatter added; absorbed token-alignment gate; added Route A confirmation (CORPUS/42:22 R0 LAW#5 INERT yet para 0/72) |
| anyedit-port-keys-at-last-prompt-token-no-paraphrase-transfer.md | SURVIVOR | frontmatter added; corrected '24/24 at upstream ridge' → 24/24 only after L2 10→0.01, 11/24 & 1/24 at L2=10 (CORPUS/42:13-15); absorbed June transplant result |
| anyedit-precommit-triage-proceed-but-viability-gated.md | RETIRED | tombstone → CORPUS/40, CORPUS/42 |
| anyedit-token-alignment-gate-prevents-false-rescue.md | MERGED->anyedit-noop-gate-is-not-active-edit-parity.md | token-alignment gate moved into survivor; tombstoned |
| approved-deletes-ask-then-rmtree.md | FIX | States both deny forms (main blanket :13-16; worktree v4 path-scoped :13-41+) and that the ask-then-rmtree rule applies either way |
| autonomy-drifts-from-kickoff-scope.md | DEINDEX | Frontmatter (metadata.source → body line); description prefixed HISTORICAL; dead [[experiment-gate-before-next-science-arc]] → tools/experiment_gate.py |
| autonomy-driver-stale-guard-deletes-result.md | FIX | Hazard 1 marked FIXED citing autonomy_driver.py:269-270; dropped link to retired codex note; frontmatter |
| autonomy-error-label-can-mask-completed-run.md | KEEP | Frontmatter only (description >150 shortened) |
| autoresearch-editing-loop-per-fork.md | SURVIVOR | Model → claude-fable-5-1 high, launcher → v13 (v13_launcher.py:18); absorbed not-a-faithfulness-gate rule |
| autoresearch-is-not-a-faithfulness-gate.md | MERGED->autoresearch-editing-loop-per-fork.md | Tombstoned; rule moved into survivor |
| autoresearch-sandbox-fence-and-tmux-driving.md | FIX | Fence v2–v12 history → pointer (docs/AUTORESEARCH.md, sandbox probe); added status (loop not running, v13 launcher); kept tmux/paste/orx traps + generic fence lessons |
| background-monitor-no-premature-read.md | MERGED->never-idle-arm-completion-watch.md | Tombstone; foreground-sleep advice dropped (blocked in harness) |
| backup-via-memitbackup-app.md | FIX | Retitled as interim internal-SSD mirror (not archive tier, gdrive replacing it); added last-run FATAL (rsync exit 24, 2026-10-09 17:56) status |
| betaedit-official-repo.md | FIX | dropped /workspace clone path (no BetaEdit clone on the memit volume); 'operator chose to proceed with A3' → A3 PARKED (runbook:148); frontmatter |
| bias-ablation-causal-attribution.md | KEEP | frontmatter normalized (dropped node_type/originSessionId); description shortened |
| browser-harness-for-browser-automation.md | KEEP | Frontmatter only (extra keys dropped) |
| c10-accept-bounded-means-hybrid-not-general-db.md | FIX | frontmatter only + source line (still binding: C10 OPEN per runbook §0.3) |
| c10-band-knobs-failed-for-hard-coined-values.md | MERGED->c10-memit-knobs-failed-before-anyedit.md | band-knob numbers (CORPUS/37-38, verified) moved into survivor; tombstoned |
| c10-edit-collateral-breaks-injected-target.md | DEINDEX | frontmatter normalised; description shortened + HISTORICAL; body intact |
| c10-edit-rotates-required-target-direction.md | DEINDEX | frontmatter normalised; stale 'Routing: two-pass solve arm next' dropped from description, HISTORICAL; body intact |
| c10-layerpick-null.md | DEINDEX | description shortened (≤150) + HISTORICAL; body intact |
| c10-memit-knobs-failed-before-anyedit.md | SURVIVOR | frontmatter added; absorbed band-knob detail and binding-metric rule |
| c10-mint2-r3-provisional-no-direction.md | FIX | 'ratification pending' → CLOSED, operator-ratified 2026-10-07 (CORPUS/54:3); dropped 'nothing routes until operator rules'; kept 'V2 diagnosis owed' |
| c10-secondkey-null-large-write.md | DEINDEX | description shortened + HISTORICAL; links to solvefeas/research-pass → c10-sharedz-underfit + HANDOFF.md |
| c10-sharedz-underfit.md | SURVIVOR (de-indexed) | (stays de-indexed) absorbed CORPUS/52 solvefeas reading; HISTORICAL description; research-pass link → HANDOFF.md |
| c10-solvefeas-underfit-at-50.md | MERGED->c10-sharedz-underfit.md | CORPUS/52 content moved into survivor; tombstoned |
| c10-stacked-solve-tradeoff.md | DEINDEX | description shortened + HISTORICAL; body intact |
| c10-status-and-session-b-residual-test.md | RETIRED | tombstone: Intel-CPU target superseded by D-HW-1, options closed (CORPUS/42, /61); results CORPUS/35-36 |
| c10-twopass-solve-null-at-margin.md | DEINDEX | description shortened + HISTORICAL; body intact |
| c10e-harness-restores-band-only.md | FIX | line range 149-158 → 150-158 (verified); [[c10k-route-a-resume]] → CORPUS/61; description shortened |
| c10k-route-a-resume.md | RETIRED | Tombstoned → runbook §0.3 + CORPUS/51–61 after harvesting method facts, close-out traps, shell traps and test lessons into 4 notes |
| c10w-ceiling-oracle-result.md | DEINDEX | description shortened + HISTORICAL; body intact |
| c10x-enginepath-result.md | DEINDEX | description shortened + HISTORICAL; body intact |
| c10z-a1-population-byte-identity.md | KEEP | frontmatter only (dropped node_type) |
| c10z-stage1-underfit-terminal.md | RETIRED | tombstone: copy of runbook §0.3 latest → CORPUS/61 (token verified) + c10-sharedz-underfit for the UNDERFIT rule |
| calibrate-confidence-mechanics-vs-contracts.md | KEEP | frontmatter normalized |
| calibrate-symmetrically-unresolved-is-a-verdict.md | KEEP | frontmatter normalized; description shortened to ≤150 |
| canonical-fit-is-not-c10-rescue.md | MERGED->c10-memit-knobs-failed-before-anyedit.md | para_full-binds/canon_full-diagnostic rule + 29.2→45.8 / 13.9→5.6 (CORPUS/37, verified) moved; tombstoned |
| claude-subscription-advisor-for-codex.md | FIX | type workflow->reference; 'cd /workspace' -> LLMDB_ROOT=$PWD (script defaults ROOT=/workspace, verified :5); names GPT-6-Astra for Claude-led work |
| closeout-gate-before-done.md | FIX | Frontmatter; LLMDB_ROOT worktree prefix; 3-layer history → pointer to tools/ANTI_DRIFT.md; added harvested close-out traps (verified closeout_check.py:72-75) |
| clustered-design-power-determinism-cheaper-lever.md | FIX | added line: ~50pp swing measured on RunPod 4090/cuBLAS 2026-06, re-measure on MPS before sizing; frontmatter (tools/stats.py, tools/power.py verified) |
| clustered-editing-trials-sampling-unit.md | KEEP | framed gpt-5.5 as the 2026-06 reviewer; description shortened to ≤150 |
| codex-chatgpt-oauth-model-slug.md | RETIRED | Tombstone -> CLAUDE.md:16 / AGENTS.md:102 (codex-cli 0.160.1, model gpt-6-astra verified) |
| codex-review-embed-evidence-and-effort.md | RETIRED | Tombstone -> codex-runs-inline; its gpt-5.5 tips not carried (unverified against the current -C read-only high-effort command) |
| codex-runs-inline-from-claude-bash.md | FIX | Dropped pod paths/gpt-5.5/setsid recipe; points at CLAUDE.md:16 command; kept review-before-asking, OAuth-expiry perplexity fallback, calibrate-by-result rules |
| commit-forward-work-without-asking.md | FIX | Rewritten to CLAUDE.md:17 rule: push every commit to the branch, never merge; dropped pod master/ff-merge, gh-creds and settings-edit text (kept as one history line) Coordinator: 'repo is public' → remote PRIVATE per gh repo view 2026-10-10. |
| confirmed-delegated-is-not-delivered.md | KEEP | frontmatter normalized; description shortened |
| connected-papers-api.md | FIX | One current mode: no keychain key (exit 44, 2026-10-10) → Browser Harness .bib export; dropped collection counts |
| context-management-every-session.md | FIX | Replaced 'Gap found' session narrative (~700k tokens) with a one-line verified gap (memento not in enabledPlugins); named where start_<name>.sh launchers live; frontmatter |
| control-relation-effective-cardinality.md | KEEP | frontmatter normalized; description shortened |
| corpus44-rho-is-remaining-residual.md | FIX | dropped 'before scheduling steps 6-7 re-argue with operator' (step 6 closed CORPUS/58); line cite 74-75 → 74 (verified); description shortened |
| dashboard-live-derivation.md | KEEP | No change |
| default-to-the-less-flattering-reading.md | KEEP | frontmatter normalized; description shortened |
| deployment-target-intel-cpu.md | RETIRED | Tombstone -> D-HW-1 / local-only-no-rented-compute; June results pointer CORPUS/13-16 + docs/write_engine_viability_determination_report.md; runbook:146 links it |
| deterministic-null-label-can-hide-real-effect.md | KEEP | framed gpt-5.5 as the 2026-06 reviewer; frontmatter normalized |
| disk-budget-before-dispatch.md | FIX | Policy paragraph → pointer to runbook §3.3a, gdrive authorized 2026-10-10; item (3) → approved-deletes rule |
| durable-artifact-path-collision.md | FIX | Marked both instances FIXED (g6_scale_n.py:236, g6_scale_n_param.py:247); frontmatter |
| e2e-ground-truth-situate-on-the-map.md | RETIRED | Tombstone -> CLAUDE.md:13 binding rule |
| easyedit-assets-vendored.md | FIX | rewritten: pod clone/parts-bin gone; pod fingerprint 5c0c706a + 4090 OOM dropped; retired link dropped; usage rules kept |
| editing-memory-eval-prior-art-landscape.md | FIX | corrected 'AnyEdit is a ready plug-and-play port' (CORPUS/42: controls not recovered); larql link -> prior-art-chrishayuk-larql-2026-10; 1.2KB cut declined (true dated content) |
| encode-recurring-discipline-as-a-gate.md | KEEP | Frontmatter only (description >150, extra keys dropped); body unchanged |
| evidence-over-scaffolding.md | KEEP | frontmatter normalized; description shortened |
| exhaust-options-before-blocked.md | DEINDEX | kept intact; link [[operator-profile-llm-as-database]] (retired) -> [[operator-profile-and-standing-directive]]; frontmatter normalized |
| experiment-gate-before-next-science-arc.md | RETIRED | Tombstone: done in 0c20f38 (2026-06-27); had no valid frontmatter |
| experiment-runbook-is-canonical.md | FIX | Repo-relative path; §0.3 generated from program_state.json via render_state.py; §3.3a named; dead runpod link -> disk-budget-before-dispatch |
| fallback-that-nullifies-spec-is-not-f1-closure.md | FIX | added valid frontmatter (date/source moved to a body line); noted AnyEdit port halted (CORPUS/42), C10 still OPEN/BLOCKING (program_state.json) |
| fan-out-synthesis-subagent-results-are-leads.md | KEEP | frontmatter normalized; description shortened |
| fixed-budget-sweep-couples-iv-with-complement.md | FIX | current-reviewer instruction gpt-5.5 -> GPT-6-Astra; past gpt-5.5 review framed as history; description rewritten without gpt-5.5; narrative trim declined (style) |
| fp32-reductions-over-big-tensors.md | KEEP | Link [[gpu-gate-blocks-any-python]] → survivor [[gpu-gate-refuses-any-venv-python]] |
| gdrive-rclone-remote.md | FIX | Dead [[storage-archival-policy]] → runbook §3.3a; dropped operator email |
| gemma4-rung4-candidate.md | RETIRED | Tombstone: 4090 sizing obsolete, /workspace source note gone |
| git-add-all-leaks-secrets-on-public-repo.md | FIX | Frontmatter; noted repo is PRIVATE as of 2026-10-10 (gh repo view) while the rule stands |
| gpu-gate-blocks-any-python.md | MERGED->gpu-gate-refuses-any-venv-python.md | Tombstoned; scope paragraph + -B watcher trap moved |
| gpu-gate-refuses-any-venv-python.md | SURVIVOR | Absorbed scope/COMPUTE_EXE (:22)/run_c10v_stage.sh:7/-B trap; description says ANY python |
| graft-disabled-audit-2026-10-08.md | KEEP(no-op fix) | No change: audit's fix was style-only shrink; facts re-verified (graft hooks still in ~/.claude/settings.json:45-89, [mcp_servers.graft] in ~/.codex/config.toml) |
| in-weight-falsifier-must-be-weights-owned.md | FIX | frontmatter only; narrative trim declined (no wrong/stale claim found; style-only) |
| in-weight-knowing-insert-robust-update-fragile.md | KEEP | dropped link to retired in-weight-vs-sidestore-f1-question; description shortened |
| in-weight-logprob-reconciliation-is-bleed-unsound.md | FIX | frontmatter only; narrative trim declined (no wrong/stale claim; style-only) |
| in-weight-necessity-is-scope-keyed-hybrid.md | SURVIVOR | deleted stale 'NEXT arc' line; gpt-5.5 framed as 2026-06 reviewer; retired-note link made plain text; absorbed neuraldb-scr EV-6 paragraph; description ≤150 |
| in-weight-value-expression-experiment-design.md | FIX | dropped done 'session-B residual test' clause (CORPUS/36); reviewer -> GPT-6-Astra w/ Perplexity fallback; cov-minutes marked 2026-06 pod figure |
| in-weight-vs-sidestore-f1-question.md | RETIRED | tombstone -> [[in-weight-necessity-is-scope-keyed-hybrid]] (its 'Supersedes' line verified) |
| infranodus-discourse-lens-not-coverage-tool.md | FIX | Frontmatter; condensed the 'replace markdown' paragraph to its conclusion; /workspace proof file marked lost with the pod; linked approval note |
| infranodus-standing-approval.md | FIX | Rewritten to resolved state (allow rule at ~/.claude/settings.json:14); removed dead [[math-lab]] |
| injection-control-is-a-stratum-not-a-floor.md | KEEP | frontmatter only (description ≤150; dropped node_type/originSessionId) |
| lab-view-and-live-telemetry.md | FIX | Deleted 2026-10-07 status blocks; kept duty/telemetry/never-touch rules + server-start and phone URL; [[c10k-route-a-resume]] → docs/c10_scoreboard.json |
| larql-the-mechanism-prior-art.md | MERGED->prior-art-chrishayuk-larql-2026-10 | theory + 4 gaps moved; /workspace clones absent (external_prior_art has no larql); tombstoned |
| last-token-keyed-write-is-a-frame-write.md | FIX | frontmatter added; body unchanged |
| llm-as-database-program-overview.md | FIX | Removed false 'engine gitignored' claim (143 tracked files) and dated 2026-06-27 status; added CLAUDE.md/AGENTS.md + EXPERIMENT_REGISTRY to reading order; link to retired migration-gaps repointed |
| llm-db-local-migration-gaps.md | RETIRED | Tombstone: migration done (engine vendored, fingerprint PASS d941a9fb, _cov_cpu 3, Route A taken) |
| llmdb-root-env-points-at-main-checkout.md | SURVIVOR | Absorbed 2026-10-10 '14 MISSING' example + closeout_check.py:25; added worktree/shell traps from the retired resume note (cd, /usr/bin/git, *token*/*.log, no MPS float64) |
| llmdb-root-points-at-main-checkout.md | MERGED->llmdb-root-env-points-at-main-checkout.md | Tombstoned; wrong cause (login shell) dropped — settings.json:85 is the source |
| local-only-hardware-rule.md | MERGED->local-only-no-rented-compute.md | Tombstone; docs/C10K_ROUTEA_LOCAL_PORT_PREREG.md cites it by name (tombstone points to survivor) |
| local-only-no-rented-compute.md | SURVIVOR | Absorbed D-HW-1 'science + deployment target' and Route A prereg pointer from local-only-hardware-rule; frontmatter |
| match-metric-to-the-claim.md | FIX | fixed extension numbering (Extension 2 now precedes 3); description shortened; compression declined (style) |
| mathlab-calibration-stop-scope.md | FIX | 'Current disposition' D-ID sentence → pointer to runbook §0.3 (verified there, :47/:110); dropped node_type |
| mathlab-native-norm-contract.md | KEEP | frontmatter only (dropped node_type) |
| mbp-command-line-tools-broken.md | DEINDEX | Kept intact; frontmatter cleaned, description prefixed HISTORICAL; dropped link to retired migration-gaps (CLT 27.0 verified via pkgutil/xcrun) |
| mbp-shell-aliases-trap.md | FIX | Aliases are interactive-zsh only (grep->rg, find->fd are aliases, not functions); agent Bash has none, trap there is the rtk hook; dropped retired link |
| memit-cov-inversion-not-a-hang.md | RETIRED | Tombstone: GPT-J /proc triage; kept the one generic point in the pointer sentence |
| memory-paths-and-mirror-discipline.md | FIX | Pod paths replaced with current LIVE dir and memory_mirror; closeout_check sync check described (verified :240-257); one-way sync rule kept |
| method-ports-need-replication-faithfulness-gate.md | FIX | frontmatter added (date/source/scope → body line); Route A confirmation (CORPUS/42) |
| mint-replication-spread-and-gguf-survival.md | FIX | dead [[c10l-mint-token]] → CORPUS/45; description shortened |
| model-and-compute-allocation.md | FIX | Credits/Opus framing marked time-bound; launchers located (session scratch, not tools/); reviewer line points at CLAUDE.md:16; removed c10k link and duplicate Astra command |
| molab-migration-assessment.md | RETIRED | Tombstone: RunPod gone, rentals barred; report remains in research_and_specs/ |
| mps-offset-view-conversion-bug.md | KEEP | No change |
| name-the-manipulated-variable-not-the-arm-intent.md | KEEP | frontmatter normalized; description shortened |
| native-knowledge-screen-is-not-editability.md | KEEP | frontmatter normalized; description shortened |
| neuraldb-scr-keep-side-store-pressure-live.md | MERGED->in-weight-necessity-is-scope-keyed-hybrid | EV-6 NeuralDB/SCR point moved into survivor; tombstoned |
| never-idle-arm-completion-watch.md | SURVIVOR | Watcher-gap implementation paragraph cut to the one-line re-arm lesson; push rule generalized to <branch>; absorbed background-task rule from background-monitor |
| no-model-cleared-full-bars-c10-included.md | FIX | frontmatter added; last sentence: AnyEdit port halted (CORPUS/42), C10 arms 43-61 cleared nothing; FABLE/WISE/GRACE not run (no hit in CORPUS/4x-6x) |
| notebooklm-install-and-notebook-ids.md | MERGED->notebooklm-via-browser-harness.md | Tombstoned; pod-era /workspace install gone; notebook IDs not carried (unverifiable without the browser), recoverable via git |
| notebooklm-via-browser-harness.md | SURVIVOR | Dropped email + source counts; CLI 0.8.4 auth check re-tested (still error); absorbed advisory-only + no-cookies-in-tree rules; old IDs via git pointer |
| ollama-serves-winning-defense-graphify.md | KEEP | Frontmatter only (description >150 shortened) |
| operator-decision-scope.md | DISAGREED-left | Kept live (not merged): dropped [[c10k-route-a-resume]] link, frontmatter/description fixed |
| operator-overnight-autonomy-2026-10-06.md | FIX | Collapsed to standing rules: dropped one-night tasks (OpenResearch list, self-reset), pane id, superseded no-budget-raise limit; added CLAUDE.md:15/:22 carve-outs |
| operator-profile-and-standing-directive.md | SURVIVOR | Caveat rewritten to current regime (overnight rulings, CLAUDE.md:15 list); absorbed 'challenges are signal' line from operator-profile-llm-as-database; frontmatter |
| operator-profile-llm-as-database.md | RETIRED | Tombstone -> operator-profile-and-standing-directive (its 'deployment TBD, RunPod valid proxy' contradicts D-HW-1) |
| operator-scaffolding-phase-tooling.md | RETIRED | Tombstone -> CLAUDE.md:17/:22 standing delegation; runbook:860 still links it (patch item) |
| pass-label-not-equal-promotable-claim.md | KEEP | description shortened to ≤150 |
| perplexity-c10h-reranks-anyedit-failure-geometry-first.md | DEINDEX | frontmatter added (HISTORICAL); source/artifacts → body line; outcome pointer CORPUS/42 |
| perplexity-mcp-restore-from-pod-restore.md | RETIRED | Tombstoned → global `codex mcp add perplexity` setup (codex mcp list verified) + .codex/config.toml entry commented out (6cbb10c) |
| plain-language-to-operator.md | KEEP | Frontmatter only (extra keys dropped, description shortened) |
| pod-restart-wipes-system-python-ml-stack.md | RETIRED | Tombstone: RunPod-only; runbook + 2 docs mention it historically |
| pool-sizing-levers-items-then-determinism.md | KEEP | frontmatter normalized; description shortened |
| prior-art-anyeditpp-2026.md | FIX | 'read Keys to Robust Edits next' -> read in 2026-10-06 research pass (dispositions.md:16); [[c10k-route-a-resume]] -> CORPUS/42 |
| prior-art-arxiv-2607-batch.md | KEEP | frontmatter normalized; description shortened |
| prior-art-blendsql-small-models-2026.md | KEEP | frontmatter normalized; description shortened |
| prior-art-chrishayuk-larql-2026-10.md | SURVIVOR | [[c10k-route-a-resume]] -> CORPUS/42-43; absorbed larql-the-mechanism theory line + 4 gaps (CP2/B3/write/quant); description ≤150 |
| prior-art-lre-hernandez-2024.md | FIX | 'candidate next falsifier' -> forward option (i) per CORPUS/42:35, 43:52, not run as of 2026-10-10; dropped [[c10k-route-a-resume]] |
| prior-art-sleeping-llm-2026.md | FIX | [[c10k-route-a-resume]] -> CORPUS/42-43; frontmatter normalized |
| prior-art-sweep-2026-10.md | FIX | 10 dated addenda (verified present in docs/PRIOR_ART_SWEEP_2026-10-04.md §4-§13) replaced by 4-line live summary (cell empty, Super Weight, solution map, index); link fix |
| prototype-tautology-trap.md | KEEP | frontmatter normalized; description shortened |
| push-on-milestones.md | KEEP | No change |
| q4km-quantization-survival-pass.md | DEINDEX | HISTORICAL (pod-era) description; '/workspace' line marked pod-era/gone; [[larql-the-mechanism-prior-art]] → prior-art-chrishayuk-larql-2026-10 |
| qwen25-3b-super-weight-l2-down-proj.md | FIX | frontmatter added; dropped dangling '(next action 2)' |
| read-authoritative-source-fully.md | KEEP | frontmatter normalized |
| read-keying-locus-before-porting-an-editor.md | FIX | frontmatter added; pointer that CORPUS/43 / last-token-keyed note supersedes the conditional F3 reading |
| readme-plain-words-summary.md | KEEP | Frontmatter only (extra keys dropped, description shortened); README.md:7 '## In plain words' verified |
| repo-reorganized-llmdb-root.md | RETIRED | Tombstone -> llmdb-root-env-points-at-main-checkout + docs/EXPERIMENT_REGISTRY.md (registry line added to program overview) |
| rerun-never-patch.md | KEEP | Frontmatter only: description shortened to <=150 chars |
| research-first-and-verify-tool-availability.md | FIX | InfraNodus 'not connected' example marked 2026-06 history (connected+approved since 2026-10-08); added current Codex Perplexity example |
| research-pass-2026-10-06-sequence.md | RETIRED | tombstone: sequence executed (CORPUS/51-61) → results/research_pass_2026-10-06/HANDOFF.md + council_critique.md |
| resolve-the-gates-real-criterion.md | KEEP | link [[operator-profile-llm-as-database]] (retired) -> [[operator-profile-and-standing-directive]]; description shortened |
| review-diminishing-returns-evidence-is-binding.md | KEEP | frontmatter normalized; description shortened |
| runpod-dashboard-vs-pod-metrics.md | RETIRED | Tombstone -> runbook §3.3a / disk-budget-before-dispatch; runbook:238 links it (patch item) |
| runpod-durable-experiment-launch.md | RETIRED | Tombstone -> Bash background/nohup + tmux notes |
| runpod-session-disconnect-cause.md | RETIRED | Tombstone -> tmux notes |
| scope-gate-batch-is-deployment-model.md | DEINDEX | description prefixed HISTORICAL; retired [[deployment-target-intel-cpu]] link -> M3 target note; BetaEdit 'cloned/cov ready' -> clone not on disk, A3 PARKED (runbook:148) |
| seed-freezes-context-templates.md | FIX | Engine path → memit_dry_run/memit/memit/memit_main.py:304–323; added harvested method facts (per-process templates, 8–16/72 spread, unseeded pca_lowrank, 5.9 GB save) |
| sequential-edit-run-nondeterminism.md | FIX | added hardware note: numbers + cuBLAS mechanism are RunPod 4090 2026-06, not re-measured on MPS; description ≤150; trim declined (style) |
| single-seed-limits-generality-not-significance.md | KEEP | frontmatter normalized; description shortened |
| skills-are-contracts-not-agents.md | FIX | added valid frontmatter (date/source/scope moved to a body line) |
| spec-coherence-audit-is-circular.md | FIX | 'three traps' -> 'four traps' (lists 4); description shortened; shrink declined (style) |
| standing-auth-forward-requirements.md | FIX | Dropped RunPod disk-hygiene wording; deletions now per CLAUDE.md:55 per-path approval; dead link to operator-profile-llm-as-database repointed |
| tailscale-remote-access.md | KEEP | Frontmatter only (description >150 shortened) |
| test-first-one-round-builds.md | FIX | Frontmatter; appended harvested lessons (real-producer fixtures, mutation re-anchoring, every child branch prints, revision pins) |
| tmux-kill-session-exact-name.md | KEEP | No change |
| tmux-server-hang-dashboard.md | FIX | Clarified the pod-era hooks claim: it is .codex/hooks.json (verified /workspace paths), not .claude/settings.json |
| verify-canonical-state-edits-persist.md | FIX | RunPod cause framed as history; recurrence on memit volume UNVERIFIED (CLAUDE.md:56); §0.3 now regenerable; dropped 'leave a warning line' and retired link |
| verify-external-artifacts-before-effort.md | FIX | example corrected: arXiv 2605.09285 is real (contradictions.md §1); lesson extended to verifying 'it is fake' claims; description |
| wide-intermediate-7b-editing-vram.md | DEINDEX | Kept intact; description + body prefixed HISTORICAL (pod-era 4090); dropped links to two retired runpod notes |

## Disagreed with the audit (evidence)

- `operator-decision-scope.md` — audit: merge into operator-profile. Left live (frontmatter + dead link fixed): `CLAUDE.md:15` cites it by name as the authority for what to bring the operator, and CLAUDE.md is out of scope; a tombstone would leave the always-loaded anchor pointing at a retired note. (`gpu-gate-blocks-any-python`, cited at `CLAUDE.md:30`, WAS merged because CLAUDE.md also cites the survivor `gpu-gate-refuses-any-venv-python`.) Operator follow-up if the merge is still wanted: repoint CLAUDE.md:15 first.
- `git-add-all-leaks-secrets-on-public-repo.md` (and `commit-forward-work-without-asking.md`) — audit: repo is still public. `gh repo view --json visibility` → `PRIVATE` (2026-10-10). Rule kept; both notes now say the remote was public in 2026-06 and is private now.
- `tmux-server-hang-dashboard.md` — audit: pod-era hooks claim unverified (it checked `.claude/settings.json`). The claim is about Codex hooks: `.codex/hooks.json:4-10` still calls `/workspace/.codex/hooks/*.py`. Kept, with the file named.
- `mbp-shell-aliases-trap.md` — audit: no grep/find aliases. `~/.zshrc:237` `alias grep='rg'`, `:247` `alias find='fd'` (interactive zsh only). Note now lists them and says agent Bash is affected by the rtk hook, not the aliases.
- `verify-canonical-state-edits-persist.md` — audit: CLAUDE.md says the revert hazard persists on memit. `CLAUDE.md:56` attributes it to the RunPod FUSE volume and calls recurrence on the local volume unverified; note matches that.
- `easyedit-assets-vendored.md` — audit: EasyEdit lives at `<mirror>/easyedit_ref`. That folder holds only `llama-7b.yaml` and `llama3.2-3b.yaml`; note says the pod copy is gone and to re-clone if needed.
- `c10-mint2-r3-provisional-no-direction.md` — audit: drop the 'Owed' lines. The V2 diagnosis is still owed (`CORPUS/54:74`); kept that line, changed 'ratification pending' → CLOSED, ratified (`CORPUS/54:3`).
- `context-management-every-session.md`, `model-and-compute-allocation.md` — audit: `start_<name>.sh` should be named in tools/. They live in session scratch (`~/.claude/jobs/<id>/tmp/`); notes say so.
- Style-only trims not applied (no wrong/stale claim found): `graft-disabled-audit-2026-10-08`, `in-weight-falsifier-must-be-weights-owned`, `in-weight-logprob-reconciliation-is-bleed-unsound`, `fixed-budget-sweep-couples-iv-with-complement` (narrative), `match-metric-to-the-claim` (compression; numbering fixed), `spec-coherence-audit-is-circular` (shrink; 'four traps' fixed), `sequential-edit-run-nondeterminism` (trim; hardware note added), `editing-memory-eval-prior-art-landscape` (1.2 KB cut; the false AnyEdit claim removed).

## Acceptance outputs

`LLMDB_ROOT=$PWD python3 -B tools/closeout_check.py D-NEW1-fid` (memory lines + verdict):
```
  [GREEN  ] memory_mirror sync
  [GREEN  ] memory_mirror/MEMORY.md links
✅ CLOSE-OUT COMPLETE — D-NEW1-fid present + current (D-NEW1-fid@341707a8) in all canonical trackers.
```
Frontmatter lint (every memory_mirror/*.md except MEMORY.md, SESSION_CHECKPOINT.md; exact rule-2 shape, name = slug, description ≤150 chars, tombstones carry the `git show fd77f7e:` pointer) and `[[link]]` check over live notes:
```
frontmatter failures: 0 []
retired 41 live 128
links to retired/missing from live notes: []
```
Index: 112 entries, longest line 178 chars (0 lines > 200), 0 links to a RETIRED note, 0 duplicate links, every live non-historical note listed. Size **17181 bytes — over the 10 KB target**: listing all 112 guiding notes (brief rule 6) with ~40-char filenames cannot fit 10 KB with behavioral hooks; it stays under the 24.4 KB MEMORY.md cap and 200 lines. If size matters more, the Science-lessons block (34 lines) is the candidate to de-index.

Stale-term grep (`/workspace`, `gpt-5.5`, `4090`, `RunPod`, `ff-merge`, `to master`) over non-retired notes — every remaining hit is framed as history or names a current stale config:
- `claude-subscription-advisor-for-codex.md`: /workspace — names the script's leftover pod default (`tools/claude_advisor.sh:5`) and says to override it
- `clustered-design-power-determinism-cheaper-lever.md`: 4090, RunPod — swing figure labelled 4090-era, re-measure on MPS
- `clustered-editing-trials-sampling-unit.md`: gpt-5.5 — 'the 2026-06 cross-family reviewer'
- `commit-forward-work-without-asking.md`: ff-merge — 'History: … superseded by push-to-branch, never-merge'
- `deterministic-null-label-can-hide-real-effect.md`: gpt-5.5 — 'the 2026-06 reviewer'
- `easyedit-assets-vendored.md`: /workspace — 'on the pod (2026-06-17) … those pod paths are gone'
- `experiment-runbook-is-canonical.md`: RunPod — 'heading still says RunPod'
- `fixed-budget-sweep-couples-iv-with-complement.md`: gpt-5.5 — 'then gpt-5.5'
- `in-weight-necessity-is-scope-keyed-hybrid.md`: gpt-5.5 — 'the then cross-family reviewer' / 'the 2026-06 cross-family reviewer'
- `infranodus-discourse-lens-not-coverage-tool.md`: /workspace — 'pod-era proof file … lost with the pod'
- `q4km-quantization-survival-pass.md`: /workspace — HISTORICAL description + '(pod-era paths, gone since D-HW-1:)'
- `research-first-and-verify-tool-availability.md`: /workspace — 'dead /workspace wrapper (commented out in 6cbb10c)'
- `sequential-edit-run-nondeterminism.md`: 4090, RunPod — 'Hardware note (2026-10-10): measured on the RunPod RTX 4090 … not re-measured on MPS'
- `tmux-server-hang-dashboard.md`: /workspace — current stale config: `.codex/hooks.json` still points at pod-era /workspace (verified 2026-10-10)
- `verify-canonical-state-edits-persist.md`: RunPod — 'on the RunPod pod, now gone'
- `wide-intermediate-7b-editing-vram.md`: 4090 — HISTORICAL (pod-era) description and banner; de-indexed

## LIVE files touched

LIVE = `~/.claude/projects/-Volumes-memit-llm-database-poc-mirror/memory/` (51 notes + MEMORY.md before; 120 notes + MEMORY.md after; nothing deleted). After sync every LIVE file is byte-identical to the mirror. Pre-audit LIVE `MEMORY.md` saved at `pre_audit_untracked/LIVE_MEMORY.orig.md` (the other 51 LIVE notes equalled `fd77f7e:memory_mirror/`).

- Overwritten with the mirror version (46): `approved-deletes-ask-then-rmtree.md`, `autoresearch-sandbox-fence-and-tmux-driving.md`, `backup-via-memitbackup-app.md`, `browser-harness-for-browser-automation.md`, `c10e-harness-restores-band-only.md`, `c10k-route-a-resume.md`, `c10w-ceiling-oracle-result.md`, `c10x-enginepath-result.md`, `c10z-stage1-underfit-terminal.md`, `connected-papers-api.md`, `context-management-every-session.md`, `disk-budget-before-dispatch.md`, `fp32-reductions-over-big-tensors.md`, `gdrive-rclone-remote.md`, `gpu-gate-blocks-any-python.md`, `gpu-gate-refuses-any-venv-python.md`, `infranodus-standing-approval.md`, `lab-view-and-live-telemetry.md`, `llm-as-database-program-overview.md`, `llm-db-local-migration-gaps.md`, `llmdb-root-env-points-at-main-checkout.md`, `llmdb-root-points-at-main-checkout.md`, `local-only-no-rented-compute.md`, `mbp-command-line-tools-broken.md`, `mbp-shell-aliases-trap.md`, `model-and-compute-allocation.md`, `never-idle-arm-completion-watch.md`, `notebooklm-via-browser-harness.md`, `ollama-serves-winning-defense-graphify.md`, `operator-decision-scope.md`, `operator-overnight-autonomy-2026-10-06.md`, `operator-profile-and-standing-directive.md`, `plain-language-to-operator.md`, `prior-art-anyeditpp-2026.md`, `prior-art-arxiv-2607-batch.md`, `prior-art-blendsql-small-models-2026.md`, `prior-art-chrishayuk-larql-2026-10.md`, `prior-art-lre-hernandez-2024.md`, `prior-art-sleeping-llm-2026.md`, `prior-art-sweep-2026-10.md`, `readme-plain-words-summary.md`, `rerun-never-patch.md`, `seed-freezes-context-templates.md`, `tailscale-remote-access.md`, `test-first-one-round-builds.md`, `tmux-server-hang-dashboard.md`
- Added because the new index links them (69): `resolve-the-gates-real-criterion.md`, `anti-drift-enforce-not-autowrite.md`, `c10-accept-bounded-means-hybrid-not-general-db.md`, `closeout-gate-before-done.md`, `commit-forward-work-without-asking.md`, `encode-recurring-discipline-as-a-gate.md`, `evidence-over-scaffolding.md`, `fallback-that-nullifies-spec-is-not-f1-closure.md`, `standing-auth-forward-requirements.md`, `pass-label-not-equal-promotable-claim.md`, `read-authoritative-source-fully.md`, `research-first-and-verify-tool-availability.md`, `review-diminishing-returns-evidence-is-binding.md`, `verify-external-artifacts-before-effort.md`, `autoresearch-editing-loop-per-fork.md`, `claude-subscription-advisor-for-codex.md`, `codex-runs-inline-from-claude-bash.md`, `infranodus-discourse-lens-not-coverage-tool.md`, `memory-paths-and-mirror-discipline.md`, `experiment-runbook-is-canonical.md`, `skills-are-contracts-not-agents.md`, `fan-out-synthesis-subagent-results-are-leads.md`, `anyedit-name-collision-dcdmllm-is-image-editing.md`, `autonomy-driver-stale-guard-deletes-result.md`, `verify-canonical-state-edits-persist.md`, `autonomy-error-label-can-mask-completed-run.md`, `git-add-all-leaks-secrets-on-public-repo.md`, `durable-artifact-path-collision.md`, `c10z-a1-population-byte-identity.md`, `bias-ablation-causal-attribution.md`, `clustered-design-power-determinism-cheaper-lever.md`, `clustered-editing-trials-sampling-unit.md`, `control-relation-effective-cardinality.md`, `corpus44-rho-is-remaining-residual.md`, `confirmed-delegated-is-not-delivered.md`, `in-weight-falsifier-must-be-weights-owned.md`, `fixed-budget-sweep-couples-iv-with-complement.md`, `in-weight-necessity-is-scope-keyed-hybrid.md`, `injection-control-is-a-stratum-not-a-floor.md`, `in-weight-knowing-insert-robust-update-fragile.md`, `native-knowledge-screen-is-not-editability.md`, `last-token-keyed-write-is-a-frame-write.md`, `default-to-the-less-flattering-reading.md`, `in-weight-logprob-reconciliation-is-bleed-unsound.md`, `match-metric-to-the-claim.md`, `mathlab-calibration-stop-scope.md`, `mathlab-native-norm-contract.md`, `calibrate-confidence-mechanics-vs-contracts.md`, `method-ports-need-replication-faithfulness-gate.md`, `name-the-manipulated-variable-not-the-arm-intent.md`, `anyedit-noop-gate-is-not-active-edit-parity.md`, `deterministic-null-label-can-hide-real-effect.md`, `pool-sizing-levers-items-then-determinism.md`, `prototype-tautology-trap.md`, `qwen25-3b-super-weight-l2-down-proj.md`, `read-keying-locus-before-porting-an-editor.md`, `sequential-edit-run-nondeterminism.md`, `single-seed-limits-generality-not-significance.md`, `spec-coherence-audit-is-circular.md`, `calibrate-symmetrically-unresolved-is-a-verdict.md`, `in-weight-value-expression-experiment-design.md`, `betaedit-official-repo.md`, `easyedit-assets-vendored.md`, `editing-memory-eval-prior-art-landscape.md`, `anyedit-port-keys-at-last-prompt-token-no-paraphrase-transfer.md`, `c10-memit-knobs-failed-before-anyedit.md`, `c10-mint2-r3-provisional-no-direction.md`, `mint-replication-spread-and-gguf-survival.md`, `no-model-cleared-full-bars-c10-included.md`
- `MEMORY.md` replaced with the mirror's new index.

## Other outputs and follow-ups

- `runbook_fixes.patch` (unified diff vs the current working files; `git apply --check` clean; touches no GENERATED block): runbook §2.7 Mirror line (:225) and the duplicate at :157 → current LIVE/mirror paths + closeout_check; BetaEdit row (:334, the 'row ~295' of the audit) → arXiv 2605.09285 is real (IJCAI 2026); every runbook `[[link]]` to a retired note (:125, :132, :146, :226, :238, :661, :844, :860, :861) → plain name + 'retired 2026-10-10' (+ survivor where one exists); `docs/AUTORESEARCH.md:20` → v13 fence launcher (claim verified: `launch.sh` execs `<fence>/v13_launcher.py`; flags at `v13_launcher.py:18-21`).
- **Reversibility gap:** `anyedit-port-keys-at-last-prompt-token-no-paraphrase-transfer.md` and `last-token-keyed-write-is-a-frame-write.md` match `.gitignore:50` (`*token*`) and were never in git. Originals saved under `pre_audit_untracked/` (renamed to avoid the pattern). To put them under git: `git add -f memory_mirror/<file>` (operator call; not done).
- Outside scope, not edited: `.codex/hooks.json:4-10` (four Codex hooks call /workspace); runbook :148 still says `external_prior_art/BetaEdit` is cloned (it is not on disk); the internal-SSD backup's last run (2026-10-09 17:56) ended FATAL on a benign rsync exit 24; files outside memory that name tombstoned notes (`docs/C10K_ROUTEA_LOCAL_PORT_PREREG.md`, `tools/labviz/models.json`, `docs/PRIOR_ART_REPO_SWEEP_2026-06-23.md`, `tools/codex-skills/notebooklm-mcp-codex-audit.md`, SESSION_CHECKPOINT history lines) — each tombstone points at its replacement.
