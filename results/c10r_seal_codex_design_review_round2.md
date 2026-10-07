# D-C10r-seal — Codex design review, round 2

Reviewer: Codex.
Model: GPT-6 family; the exact deployed model identifier is not exposed in this session.
Effort: adversarial source review with standard-library-only checks; the configured sampling effort is not exposed in this session.
Date: 2026-10-06 (America/Denver).
Target: `docs/C10R_LOOP_SEALING_V13.md`, DRAFT v2, under `results/c10r_seal_review_brief_round2.md`.
Reviewed design SHA-256: `0067fb2c4130f31c704800241896d15e3d004aee0ef200d2febdb5d242952793`.

**Verdict: FIX-FIRST.** The two-process direction is viable and resolves the original architecture error at the design level. The verification section still asks a lexical tripwire to detect paraphrases it cannot detect; the editor's proposed training extract omits two required arms; the handoff format needs an explicit correction; and network isolation does not yet cover the agent's built-in web tools and credential routes. The fixes below preserve the selected base, engine, harness and metric.

This is a review of a proposed implementation. The current loop code remains the v12 implementation; that alone is not a new blocking finding. No model, torch, GPU/MPS, scorer, loop, equivalence checker or advisor session was run. The sole CLI capability inspection was `claude --help`, which did not start a model session. No credential, keychain item, browser endpoint or remote repository was queried. Only this Codex output file was written.

For source references below, `loop/` means `experiments/track_c/autoresearch_c10/`, `harness` means `experiments/track_c/c10e_bandknob.py`, and `old/` means `/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/`. Historical `commit:edit.py:line` references identify the git object, not the current working file.

## Numbered findings

1. **ADVISORY — Round-1 blocking-item disposition: two resolved, one resolved architecture direction, one superseded mechanism with an unresolved test requirement.**

   Locations: `docs/C10R_LOOP_SEALING_V13.md:15`, `:17`, `:21`, `:24`, `:38`, and `:46`; `loop/run.sh:21`; `loop/prepare.py:86`, `:222`; `loop/sandbox_settings.py:173`.

   | My round-1 item | Disposition against v2 | Evidence and remaining obligation |
   |---|---|---|
   | #1: the 3-gram refusal misses the mirrors | **SUPERSEDED** as a mechanism; the negative-control requirement is **NOT RESOLVED** | V2 §2 removes the refusal and adopts a silent 4-word copying tripwire. §5.1 still requires it to flag the same mirrors and old dev prompt. Item 5 below gives the counterexample and correction. |
   | #2: editable code receives secrets through the wrapper and `prepare.H` | **RESOLVED at architecture level** | V2 §1 gives the editor a harness-free runtime and a separate profile; a trusted parent starts a fence-owned scorer only after the editor exits. The editor cannot inherit the scorer profile or its namespace. The training-input and trusted-execution details in items 2, 4 and 7 remain to be specified and tested. |
   | #3: removing the harness copy breaks normal import | **RESOLVED at design level** | V2 §1 specifies an exact-file importlib load after a hash check, without reopening the parent directory. This directly addresses `prepare.py:85–86` and the earlier directory-denied import failure. Implementation must still pass the dummy-module profile test and later equivalence gate. |
   | #5: the old templates become a fresh promotion holdout | **RESOLVED** | V2 §6 explicitly keeps them as the loop's selection metric and requires an independent, pre-registered promotion set never used for selection or seen by the authors. No reseal-as-promotion claim remains. |

   **Exact fix:** carry these dispositions into the implementation review. Do not demand another fix for the already-corrected promotion wording or normal-import plan; verify their implementation when it exists. Correct §5.1 before claiming the superseded lexical issue is closed.

2. **BLOCKING — The editor can run without the harness, but `train_facts.json` must contain A1 and A2 as well as A7.**

   Locations: `docs/C10R_LOOP_SEALING_V13.md:15`; `loop/prepare.py:93–108`, `:111–119`, `:126–128`, and `:201–218`; `harness:224–253`; `73f78ce:edit.py:18–20`, `:60–63`, and `:90–96`.

   **EVIDENCE-SHOWS:** `evaluate` invokes the recipe in this fixed order: `A1_single`, `A2_coherent2`, `A7_coined_coined`, each on the restored base model. `facts(arm)` obtains each arm's values from `H.ARMS`. V2's extract lists only `FICTION`, A7 values, `CANON` and hparams. It therefore cannot supply the two control edits without importing the harness or inventing different control values.

   The **complete 13-name import from `prepare` in the actual `73f78ce` object** is below. None of these needs held-out template text:

   | Name imported by `73f78ce:edit.py:18` | Where it belongs in the split |
   |---|---|
   | `model` | `editor_runtime.py`: pinned Qwen2.5-3B revision, fp16, existing device resolution and `.eval()` loader |
   | `tok` | Editor runtime: same tokenizer revision, padding/eos setup and tokenization behavior |
   | `DEV` | Editor runtime: existing device helper, with no CPU fallback silently accepted |
   | `COV_LAYERS` | Editor runtime: unchanged fixed tuple `4..12` |
   | `request` | Editor runtime: reproduce the small request dictionary, including the leading space in `target_new.str` |
   | `load_hparams` | Editor runtime: unchanged hparam load/override semantics and `MEMITHyperParams` type; writable sandbox temp path |
   | `evaluate` | Editor runtime: the edit-only dispatcher, budget, restores and artifact writer; no scorer subprocess |
   | `compute_z` | Existing `memit.compute_z` helper, re-exported by the editor runtime |
   | `compute_ks` | Existing `memit.compute_ks` helper, re-exported by the editor runtime |
   | `get_module_input_output_at_words` | Existing engine helper, re-exported by the editor runtime |
   | `get_cov` | Existing engine covariance helper; same caches and hparams |
   | `get_context_templates` | Existing engine helper; preserve its seed, first-generation order and cache semantics |
   | `upd_matrix_match_shape` | Existing engine shape helper, re-exported by the editor runtime |

   `73f78ce` does not directly import `H`. I also inspected the working file as requested: old HEAD is `978fed98a1d2f104c3c98714527d569f3ee7df2b`. That file imports the same list **minus `compute_z`**, and additionally imports `rome.repr_tools` at `old/edit.py:20`; it defines its own `solve_z` at `:87`. It is a different recipe. Item 6 explains why its imports and description must not be attributed to `73f78ce`.

   The **complete 17-name `H` attribute inventory in current `prepare.py`**, obtained by AST inspection, is:

   | `H` name | Current `prepare.py` lines | Classification and destination |
   |---|---|---|
   | `model`, `tok`, `DEV` | 93 | Runtime objects needed by the editor; recreate with the pinned loader without importing `H` |
   | `CANON` | 94 | Public training prompt; extract into training facts |
   | `FICTION` | 95 | Ordered training subjects; extract into training facts |
   | `ARMS` | 103, 254, 269, 271, 272 | Shared training/scoring value maps; export **all three** complete subject-to-value maps, with arm and subject order pinned |
   | `req` | 108 | Pure request construction; implement the same dictionary in the runtime, **do not alias `H.req`** |
   | `snap_layers` | 152 | Generic weight snapshot, used only by the trusted setup gate here; keep scorer-side |
   | `compute_P` | 153 | Generic projector calculation, used by the trusted setup gate; keep scorer-side; the recipe already has its own projector |
   | `run_law5` | 153 | Trusted harness/engine parity test with probe stimuli; scorer-side only |
   | `restore_layers` | 154 | Generic restore for the trusted setup gate; scorer-side here; editor uses its independent whole-base restore |
   | `tgt_ids` | 230 | Generic tokenizer utility for the frame guard; scorer-side; the recipe can already use `tok` directly |
   | `axes_pre` | 251 | Evaluation-bearing: closes over `L1_PROMPTS`, `L3_PROMPTS`, `GENERIC`; scorer-side only |
   | `predict` | 253, 270 | Generic prediction primitive, called for evaluation; scorer-side here |
   | `eval_arm` | 269 | Evaluation-bearing: reads `PTEST`; scorer-side only |
   | `locpct` | 270 | Generic measurement reduction used for locality; scorer-side here |
   | `axes_post` | 271 | Evaluation-bearing: uses locality sets and generic perplexity stimuli; scorer-side only |

   Even a text-independent harness function such as `H.req` carries the harness's `__globals__` dictionary. Passing that function into the editor would recreate the round-1 namespace leak. Pass plain training values and independently defined runtime helpers, never harness function objects or a module reference.

   **No required editor input is only derivable from held-out evaluation stimuli.** A1/A2 value pools are built from the fixed stimulus screen's capital truths and tokenizer lengths (`harness:225–228`); they are training controls. The locality sets are built separately from the screens and those training values (`:259–278`). Exporting the resolved training maps does not require exporting those locality countries, prompts, generic sentences or `PTEST`. Do not give the editor the full screening files merely to reconstruct the maps.

   **Exact fix:** specify a versioned training extract with ordered `FICTION`, `CANON`, and complete maps for **A1/A2/A7**, plus pinned hparams/model/tokenizer identities and a digest. Assert 24 subjects, identical subject keys in all three maps, and exact equality to the trusted canonical maps before launch. Include the runtime's fixed `SEED`, budget, arm order and engine helper contract. Preserve the current refused harness-setting environment contract in both stages. Route `HERE`-dependent paths deliberately: a runtime installed in the read-only fence cannot retain `load_hparams`'s `HERE/.hparams_<pid>.json` or `evaluate`'s `HERE/runs/...` unchanged. Their writes must go to the explicit sandbox/run path, while the scorer's private output paths stay outside it.

3. **BLOCKING — “Saved layer deltas, as today” conflicts with the unchanged scoring path. Pin the payload to absolute post-edit tensors.**

   Locations: `docs/C10R_LOOP_SEALING_V13.md:15`, `:17`, and `:21`; `loop/prepare.py:215–221`, `:259–277`; `loop/check_equivalence.py:34–36` and `:45–49`.

   **EVIDENCE-SHOWS:** today's writer saves `w[n].detach().cpu().clone()` for every changed tensor. These are absolute post-edit parameter values, not arithmetic deltas. Today's scorer validates their names, shapes, dtypes and finiteness, then uses `w[n].copy_(t)`. If the editor instead writes `W_after - W_base`, the unchanged scorer would replace the model weights with those differences. Adding a delta is a different path, and fp16 subtraction/addition is not universally bitwise reversible.

   A stdlib `struct` fp16 check gave: base `0.5`, after `0.00010001659393310547`, rounded delta `-0.5`, reconstructed result `0.0`. No torch or model was used. This is a format/rounding counterexample, not a measurement on Qwen's weights.

   **Exact fix:** call the handoff **absolute changed parameter tensors**, preserve the current artifact/manifest contract, and retain the scorer's `copy_` application, scope check and full restore between arms. Pin this explicitly in §1. If true deltas are intended, they need a new dtype/application contract and independent numerical equivalence; that is unnecessary for this sealing task.

   With the existing payload, a terminal editor followed by a fresh trusted scorer can reproduce today's measurements: today's scorer is already a fresh process that loads the base, runs setup checks, applies those saved tensors and measures. The new parent dispatch does not itself change the mathematics. **An empirical equivalence PASS remains pending.** Preserve the seeded loader order, base snapshot, original model/tokenizer revision, all three value maps, per-arm restore, LAW#5-before-measurement behavior and unchanged `_measure` operations. Preserve the transcript-independent budget start before recipe top-level work and count all three edits together. Record artifact digests for provenance; compare tensor values bitwise, rather than assuming serialized archive bytes are always the right equality target.

4. **BLOCKING — Network-denied recipe profiles do not disable the agent's built-in web tools or credential-bearing parent capabilities.**

   Locations: `docs/C10R_LOOP_SEALING_V13.md:15`, `:17`, `:19`, and `:39–41`; `loop/sandbox_settings.py:170`, `:185–200`; `loop/launch.sh:100–104`; installed `/Users/robertrhu/.local/bin/claude --help`, `--safe-mode`, `--tools`, `--strict-mcp-config` entries.

   **EVIDENCE-SHOWS:** the current settings have filesystem controls but no network configuration; the current launcher uses `--safe-mode` and unrestricted default built-in tools. The installed CLI's help says safe mode disables customizations and MCP servers, but **“Auth, model selection, built-in tools and plugins, and permissions work normally.”** Its `--tools` flag explicitly selects the available built-in tools. Therefore safe mode cannot be used as the claim that WebFetch/WebSearch are absent. Bash and child Seatbelt policies do not apply to a web tool executed by the Claude host process.

   `(deny network*)` in both child profiles is the necessary kernel boundary for editor/scorer network operations, including direct TCP connections to Chrome's CDP endpoint. The Bash sandbox needs its own explicit, fail-closed configuration; “network denied” in prose is not that configuration. Offline flags guide loaders and do not enforce a network boundary. The unchanged harness also assigns `HF_HUB_OFFLINE="0"` at `harness:5`; do not claim the scorer's wrapper value stays at `1` after import. `TRANSFORMERS_OFFLINE=1` and pinned local files may still support loading, but the profile is the enforcing boundary and later cache-loading controls must verify it.

   Credential paths remain separate. `security`/Keychain access can use local service IPC; a network deny is not a demonstrated Keychain deny. `GH_TOKEN`, `GITHUB_TOKEN`, other credential environment variables, authenticated subprocess configuration and `~/.config/gh` can expose credentials without an HTTPS request. A built-in web tool or plugin can then provide a different request path. CDP must be blocked from the Bash sandbox and both child profiles, and no Chrome/browser tool or MCP may survive in the agent's tool inventory. A single network failure from `edit.py` does not verify those other channels.

   **Exact fix:** define a reviewed built-in tool allow-list in the launcher that excludes WebFetch, WebSearch, browser/Chrome, Agent/Task and external tool entrypoints; retain the file/Bash/background-output tools needed by the actual loop. Confirm the tool inventory in the later interactive/probe session. Use safe mode plus explicit empty/strict MCP configuration where needed, and confirm zero MCP/plugin tool entries rather than assuming it. Configure the agent Bash sandbox to deny outbound/localhost access without unsandboxed fallback, then test the exact launcher flags, including permission bypass, against that policy.

   Give runtime children a minimal deterministic environment with credential variables and Python/shell injection variables removed. Explicitly deny the `~/.config/gh` tree, keychain files/credential stores and alternate path spellings in each relevant filesystem layer; do not expose secrets while probing. Add the local service/IPC rule or supported sandbox mechanism needed to make a Keychain query fail. If Keychain denial cannot be achieved, state the narrower supported claim and keep the sole remaining request paths closed; §5.2's existing “every attempt fails” bar cannot silently be declared satisfied. Leave the host's Claude subscription auth working; it is not a permission grant for agent tools to read other credentials.

5. **BLOCKING — The silent 4-word tripwire is a reasonable copying detector, but §5.1 still requires impossible negative controls and §6 overstates its coverage.**

   Locations: `docs/C10R_LOOP_SEALING_V13.md:24–26`, `:38`, and `:46`; `loop/audit_transcript.py:9–41`; `harness:52–56`.

   **EVIDENCE-SHOWS:** AST/string-only checks of the actual experiment 3–9 files found **zero** held-out 4-word windows in every file's literals. The old dev prompt also has zero. Exact templates are detected; the canonical cleaned write/dev prompt passes. This follows the earlier 3-gram failure: increasing the contiguous window length cannot recover the missing overlap.

   | Fixture | Observed 4-word result |
   |---|---|
   | All literals in `afcb2cb`, `a26863d`, `1206a7c`, `9940c0a`, `ae66823`, `e475185`, `73f78ce` | no matches in all seven files |
   | `{} has a capital called` | no match |
   | `The capital of {} is the city of` | no match |
   | Exact Q1, Q2, Q3 templates | matches in all three |

   The test lowercased text, removed `{...}` slots and normalized punctuation into words. The exact number of positive windows depends on the frozen treatment of possessives and slot boundaries; the mirror failures do not. I did not run `audit_transcript.py` or a watcher.

   **Exact fix:** replace §5.1 with: the checker detects each verbatim template and each permitted normalized 4-word window, and passes the cleaned seed; the recorded mirrors and old dev prompt are explicit **known-negative detection fixtures** that document its blind spot. Freeze normalization, whether windows cross subject slots, and handling of f-strings, comments/docstrings, escaped text and decoded transcript fields. Keep the check program-side, with no matched phrase returned to the agent.

   State the limit fully: the checker misses semantic paraphrases, fragments shorter than its window and runtime-assembled/encoded text that does not appear in inspected source/transcript text. Replace “copying is caught” with the specific inspected verbatim-window claim. A silent program-side flag removes the cheap import-time oracle, but pausing the loop is observable; make the first hit terminal for that session rather than providing repeated probe/restart feedback. Blindly authored natural paraphrases are not proof of a breach. Author-blindness is the premise that permits using such training wordings; it is not a semantic detector.

   Read `PTEST` for the watcher through hash-checked AST/literal extraction or a program-only export. Do **not** import the harness in the watcher: its top level loads the tokenizer/model at `harness:45–48`, which would turn a supposedly offline monitor into another model/GPU run.

6. **ADVISORY — The LAW#3 order and fallback are right, but the base is still misidentified as having the joint `solve_z`.**

   Locations: `docs/C10R_LOOP_SEALING_V13.md:9`, `:21`, and `:29–32`; `loop/check_equivalence.py:21–35`, `:58–73`; `loop/launch.sh:29–35`; `73f78ce:edit.py:18`, `:52–53`, `:90–96`; `old/edit.py:87`; `old/results.tsv:2`, `:4`, and `:11`.

   **EVIDENCE-SHOWS:** read-only `/usr/bin/git show 73f78ce:edit.py` succeeds here. That object calls the engine's `compute_z`; it has no `solve_z` definition. The working file at HEAD `978fed9` has the joint `solve_z` and drops the `compute_z` import. The round-1 advisor's working-file description was attributed to the wrong commit; v2 repeats it. The old TSV records `73f78ce` at 34/72, but does not make the current working file that commit.

   | Source | SHA-256 |
   |---|---|
   | Actual `73f78ce:edit.py` | `c89d80c09f2e97490ed30cda22e2a001d551e74a7df5d62585c741fc3b06abcf` |
   | Working `old/edit.py` at HEAD `978fed9` | `161becd2dce79c6a410f34b810e1dcb9c17e40819efbaff1c9beee9ccf5d514a` |
   | `fd16592:edit.py` and current program reference `loop/edit.py` | `0d03bf68549cc8a9fb3f725850222a31ad8fc822e7df5e69e9d50cc3c4cfb0f7` |

   **Exact fix:** keep the stated `73f78ce` choice, correct its description, and seed from its verified immutable object/export rather than the old HEAD file. Reduce `PROMPTS` to canonical and set `DEV_PROMPT` to canonical without changing its actual solver. Record the cleaned seed's digest separately from the unmodified source digest and equivalence reference. Selecting the HEAD joint-solver recipe would be a different base decision and is not implied by this brief.

   The proposed **order is sufficient as a gate**: fixed `fd16592` recipe through the actual new dispatcher and both profiles, full instrument equivalence and old-record reproduction, then one cleaned-base score. Compare all scientific/guard fields, arm-level compared measurements, projector/tensor parity and the old context-template anchor—not only `7/72` and `dw_total`. The current saved equivalence JSON is PASS and records both context hashes as **`e8605172dce0`**. Comparing only the two newly produced hashes would miss an equal-but-shifted seed path. Timing and new source hashes should be recorded, not required to equal old wall-clock measurements.

   The pre-registered `92acd03` fallback is reasonable for a **valid** cleaned-base score with failed guards. It is canonical-only and precedes the added mirror prompts. Do not invoke it after missing artifacts, crashes, a failed LAW#3/LAW#5 gate or a malformed score: those are instrument failures and must halt. If the fallback also fails a guard, halt rather than continue choosing bases. Compare the future loop's keep/discard decisions against its selected post-reseal baseline; exclude historical rows from that comparison. The fresh repository will not contain their old commit objects.

7. **ADVISORY — Make the scorer's execution identity, inputs and output channels trusted as well as its main file.**

   Locations: `docs/C10R_LOOP_SEALING_V13.md:15–19`, `:30`, and `:35`; `loop/run.sh:12`, `:21`; `loop/launch.sh:65`, `:87–95`; `loop/prepare.py:250–265`, `:292`, and `:298–301`; `loop/sandbox_settings.py:161–177`.

   **Exact fix:** use the fixed program interpreter and validated environment for both stages, not an agent-replaceable `$SB/.venv` entrypoint. Keep scorer imports on trusted paths, disable untrusted `PYTHONPATH`/`PYTHONHOME`, startup customization and shell startup injection, and use absolute trusted script paths. Hash the scorer's trusted helper closure, editor runtime, training extract, wrapper, profiles and fixed reference recipe in the seal/equivalence manifest; hashing only `scorer.py` does not cover code it imports. Do not launch the scorer from a still-running editor or with an editor-supplied command line.

   Allocate the run ID and handoff locations at the trusted parent. After a successful, terminal editor exit, validate complete artifacts for all three arms, reject symlink/path escapes, and snapshot them into the private scorer input area before scoring. Keep `torch.load(..., weights_only=True)` and the existing structural, dtype, finiteness and MLP-scope checks. A fresh scorer must take no metric/stimulus override from `edits.json` or the recipe environment. Extend `kill_run.sh`'s exact identity/cwd checks to the editor **and** scorer stages and their descendants without matching unrelated science jobs.

   Keep all scorer stdout, stderr, tracebacks and full records in the private scorer area. Expose only a validated projection of the 16 existing summary keys plus a fixed success/failure status; never forward raw scorer stdout or exception text. This matters even when templates do not normally print: an error path can include source or evaluation inputs. Give the scorer a private TMPDIR and explicit private-results write allowances; the current final fence-wide write deny would override a narrower write allowance placed before it. Give the editor a separate writable temp child. Preserve captured editor output for the agent, since its own diagnostics are in scope.

8. **ADVISORY — Specify the real no-model probe and the watcher/launch enforcement instead of relying on a discovery prompt.**

   Locations: `docs/C10R_LOOP_SEALING_V13.md:30–43`; `loop/run.sh:12`; `loop/setup.sh:7`; `loop/audit_transcript.py:12`, `:20`, `:23–26`, and `:53`; `loop/watch_audit.sh:8–19`; `loop/launch.sh:23–24`.

   **EVIDENCE-SHOWS:** today's wrappers perform an MPS operation before dispatching the recipe. Today's audit selects the latest transcript using the old slug, treats whole temp roots as in-bounds, silently skips malformed JSON and only reports tool/path observations. Its watcher prints changes every two minutes; it does not enumerate commits, detect template windows or deterministically stop the run. The v2 text specifies adding that behavior, but the interface to enforce it remains open.

   **Exact fix:** provide a program-controlled no-model fixture for the **same trusted dispatch and policy paths**, with the MPS preflight and real runtime/model loading replaced by a known inert fixture. The agent must not be able to select that fixture during a production run. In that fixture, a hostile recipe must execute far enough to attempt the listed file, namespace, local-network and credential operations; dying at a missing import or preflight is not a passing denial test. Add a positive control proving that a harmless editor artifact is accepted and a harmless scorer result appears only through the allowed summary projection. A dummy exact-file scorer load must prove the directory-denied/file-allowed behavior without executing the real harness. No such probe was run in this review.

   Bind the watcher to the exact new session ID/transcript, new repository path, exact own-capture directories and private scorer paths. Read every committed recipe state by commit identity, including commits later reset away, and inspect the working recipe at dispatch so uncommitted runs cannot evade the audit. Preserve watcher state outside agent control. A missing watcher/transcript, parse error or unsupported record shape must produce an explicit failure; a detected verbatim window must invoke the trusted stop procedure. A two-minute retrospective report by itself does not establish continuous launch enforcement.

   Finally, update the exclusive-GPU check to include the active `c10s_sharedz_*` jobs, the new scorer/runtime stage names, equivalence and location-control jobs. Define old-session detection specifically for the old loop identity; rejecting every unrelated `claude --safe-mode` process would also reject the program's legitimate review/probe sessions. Test late-created foreign temp and mirror/cache folders through each relevant tool layer, including background output retrieval and heredocs. An agent that merely reports “found none” does not replace these positive and negative controls.

## Review evidence and limits

The direct inventory, historical source checks and 4-word checks were performed with `/opt/homebrew/bin/rtk proxy .venv/bin/python -B -` using only `ast`, `hashlib`, `json`, `pathlib`, `re`, `struct` and `subprocess`. Historical source reads used `/usr/bin/git -C <old> show <commit>:edit.py` and `/usr/bin/git -C <old> rev-parse HEAD`; all returned successfully with nonempty, parseable source. No project module was imported. A final import check found none of `torch`, `prepare` or `c10e_bandknob` in the review interpreter's module table.

Recorded lexical output:

```text
exp 3 afcb2cb: overlapping_4word_literal_lines=[]
exp 4 a26863d: overlapping_4word_literal_lines=[]
exp 5 1206a7c: overlapping_4word_literal_lines=[]
exp 6 9940c0a: overlapping_4word_literal_lines=[]
exp 7 ae66823: overlapping_4word_literal_lines=[]
exp 8 e475185: overlapping_4word_literal_lines=[]
exp 9 73f78ce: overlapping_4word_literal_lines=[]
old DEV: tripwire_hits=0
CANON: tripwire_hits=0
PTEST 1: tripwire_hits=2
PTEST 2: tripwire_hits=4
PTEST 3: tripwire_hits=6
```

Those counts use punctuation-to-word normalization with windows allowed to cross removed subject slots; they document the check actually performed, rather than inventing the design's yet-unfrozen tokenizer. The copied-template positive controls succeed while the paraphrase fixtures fail detection.

The design's runtime import-graph audit, network/Keychain restrictions, policy precedence, no-model hostile-recipe probe, interactive tool inventory, terminal two-stage execution, old-baseline reproduction and cleaned/fallback scores are **pending implementation and verification**. This review proves none of those live behaviors. The present task ends with this output file; no implementation, extra model review, GPU work or canonical close-out was attempted.
