# Advisor review, round 2: D-C10r-seal design v2 (docs/C10R_LOOP_SEALING_V13.md)

reviewer: Claude advisor subagent, model Opus 5.5
effort: round 2, read-only; no model, no GPU
date: 2026-10-06 (late evening)

Scratch files (the two `edit.py` versions pulled from the old sandbox's loose git objects, and the reader script) were written under `/private/tmp` and deleted afterwards. One check was refused by the permission classifier: whether a GitHub token is in the environment or in `~/.config/gh`. I did not pursue it; item 7 turns it into a probe.

**Verdict: FIX-FIRST**

v2 fixes the architecture: two processes, network denied, a silent tripwire, a separate seed, LAW#3, and §6. What remains is small and concrete. Three new BLOCKING items:
- the base is still misidentified, and the wrong file is the one an implementer will copy;
- `train_facts.json` omits two of the three arms the editor must write;
- §5.1 asks the tripwire to flag look-alikes it cannot flag.

---

## 1. Round-1 BLOCKING items

**R1-1, agent code ran with the scorer's privileges: RESOLVED in design** (v2 §0.1, §1).
- The editor profile has no harness, no sealed files and no network.
- `edit.py` imports only `editor_runtime.py` (fence-owned, read-only, hash-pinned).
- `run.sh` starts the fence-owned, hash-checked `scorer.py` after the editor exits.
- The scorer imports the harness by exact file spec, which handles the `find_spec` trap (v2 §0.6, §5.3).

The current code this replaces is `run.sh:21`, `prepare.py:85-86,93` and `prepare.py:222`. Two caveats, raised below: the editor runtime has to reproduce the harness's import-time state (N2), and the scorer's stderr must not reach the agent (A1).

**R1-2, network open: RESOLVED for the two run profiles and the agent's Bash** (v2 §1, §5.2, §5.4). **Partly open** for the agent's own WebFetch tool and the keychain; see item 7 (ADVISORY).

**R1-3, the 3-gram rule: RESOLVED in principle, one contradiction left.** The refusal and its oracle are gone (v2 §2), and the limit is stated honestly ("catches copying, not paraphrase"). But §5.1 still requires the tripwire to flag the exp 3–9 `PROMPTS` and the old `DEV_PROMPT`. See N3.

**R1-4, relaunch base and gates.** (b) through (e) are RESOLVED:
- (b) `DEV_PROMPT` becomes CANON.
- (c) The seed is a separate file with its own hash, apart from the `launch.sh:29-35` / `check_equivalence.py:28-35` baseline pin.
- (d) The LAW#3 reproduction runs first, on fd16592.
- (e) The fallback to `92acd03` is pre-registered.

(a) is **NOT RESOLVED, and the error was mine in round 1.** The `edit.py` I read was the old sandbox's working tree. That tree is `978fed9` (HEAD of `autoresearch/oct6`; the reflog shows `73f78ce → 978fed9 "own target-vector solve, jointly over the write prompts"`), not `73f78ce`. v2 §3 copied my mistake. See N1.

**R1-5, §3 claimed a fresh promotion set: RESOLVED** (v2 §6 now says the templates remain the selection metric and promotion needs a separate pre-registered set).

---

## 2. New BLOCKING items

### N1. The base is not what v2 §3 describes, and the file an implementer will find is the wrong commit

I pulled `73f78ce:edit.py` from the old sandbox's loose objects (sha256 `c89d80c09f2e97490ed30cda22e2a001d551e74a7df5d62585c741fc3b06abcf`, 8331 bytes) and compared it with the working tree. The working tree is byte-identical to `978fed9:edit.py` (sha256 `161becd2…`, 11268 bytes).

- **`73f78ce` has no joint `solve_z`.** It solves each fact's target with the engine's own `compute_z` on the first prompt only (`73f78ce edit.py:92`: `compute_z(...) for rq in requests[::len(PROMPTS)]`). The extra prompts only add keys (`:89`, `:105`).
- **The joint `solve_z` and `from rome import repr_tools` belong to `978fed9`.** That is experiment 10, which was never scored: it was killed, and its run folder `20261006-193809_nocommit` has no result row.
- **With `PROMPTS = [CANON]`, the cleaned `73f78ce` is simple.** It is the baseline `compute_z` target plus GAIN 1.25 (`:101`), the preserve term at weight 4 (`:34`, `:103`, `:108`), KL 0.125 (`:30`), the eigh projector (`:53`), and the dev probe (`:118-123`).

**Fix:**
- In v2 §3, delete "the joint `solve_z`" and pin the seed by content: "seed = `73f78ce:edit.py`, sha256 `c89d80c0…abcf`, with `PROMPTS = [CANON]` and `DEV_PROMPT = CANON`, and the docstring lines `:4-6` that describe several prompts reworded."
- The launch record checks the pre-cleaning sha256.
- State explicitly that the sandbox's working-tree `edit.py` (`978fed9`) is **not** the base.

### N2. `train_facts.json` omits the A1 and A2 values, and the editor runtime must reproduce the harness's import-time state

**(a) The missing arms.**
- v2 §1 lists the extract as "FICTION, the A7 values, CANON, hparams".
- But `evaluate()` writes **all three arms**: `ARM_NAMES = ("A1_single", "A2_coherent2", "A7_coined_coined")` (`prepare.py:96`), and `apply_edit(facts(arm))` runs for each (`prepare.py:201-209`).
- The scorer then requires `A1`, `A2` ≥ 68 (`prepare.py:43-44`).

With only A7 values, the editor cannot run.

**Fix:** extract `H.ARMS` for all three arms. The extract should be a static JSON of the values. `ARMS` is built from `configs/screens/g6_screen_qwen3b_v2.json` (`c10e_bandknob.py:224-253`), and the same screens are the source of the L1/L3 locality sets (`:260-278`). With a static extract, the editor and the agent no longer need the screens at all, so **remove both screens from the editor profile and from the agent's allow-list.** That closes the "accepted exposure" in `AUTORESEARCH.md:57`.

**(b) Every name the editor takes today, and where each goes.** Sources: `73f78ce edit.py:18-20`, `978fed9 edit.py:18-20`, `prepare.py:83-128,190-225`.

| Name | Source today | Evaluation-bearing? | New home |
|---|---|---|---|
| `model`, `tok`, `DEV` | `H.model`, `H.tok`, `H.DEV` (`c10e_bandknob.py:45-48`, `:14`) | no | `editor_runtime.py` (load with the same `ID`/`REV`, fp16, `device_map=DEV`, `.eval()`, `pad_token = eos`) |
| `CANON`, `SUBJECTS`/`FICTION`, `ARMS` (A1, A2, A7 values), `facts(arm)` | `H.CANON`, `H.FICTION`, `H.ARMS` | no (training facts) | `train_facts.json` |
| `request(s, v, prompt=CANON)` | `H.req` (`c10e_bandknob.py:96-97`, a three-key dict) | no | `editor_runtime.py` (copy the dict shape exactly, including the leading space in `target_new.str`) |
| `COV_LAYERS`, `SEED`, `EDIT_BUDGET`, `EDITABLE`, `BASE_HPARAMS`, `load_hparams` | `prepare.py` constants | no | `editor_runtime.py` |
| `evaluate`, `_BASE`, `_restore_base`, `_changed`, `_alarm`/`_OverBudget`, `_T_READY` | `prepare.py:122-225` | no | `editor_runtime.py`; drop the scorer subprocess at `:222-225` |
| `compute_z`, `compute_ks`, `get_module_input_output_at_words`, `get_cov`, `get_context_templates`, `upd_matrix_match_shape`, `MEMITHyperParams` | engine, through the harness's `sys.path` (`c10e_bandknob.py:7-17`) | no | `editor_runtime.py` (engine on `sys.path`) |
| `rome.repr_tools` (`978fed9` only) | engine `sys.path` | no | same |
| `PTEST`, `eval_arm`, `axes_pre`/`axes_post`, `locpct`, `predict`, `L1`/`L3`/`GENERIC`, `FRAME_SUBJECTS`/`_frame_probe`, `GUARDS`, `run_law5`/`snap_layers`/`compute_P`/`restore_layers`, `_fingerprint`, `_reference_ok`, `tgt_ids` | harness / `prepare.py` | **yes**, or setup gates | `scorer.py` only |

Nothing the editor needs is derivable only from evaluation stimuli; the A1/A2 values become a static extract.

**(c) Import-time side effects the runtime must copy, or the equivalence check fails or imports break.**
- `LLMDB_ROOT` = the program root.
- `HF_HOME = {root}/hf_cache` (`c10e_bandknob.py:4`).
- `sys.path.insert(0, ENGINE_ROOT)` and `os.chdir(ENGINE_ROOT)` (`:7-8`). The engine's covariance-stats paths are resolved relative to the working directory.
- `DEV = resolve_device()` from `util.device` (`:13-14`).
- **Seed order:** `torch.manual_seed(SEED)` before the model load, as in `prepare.py:83` before `:86`. The context templates are sampled, and `templates_sha` must stay `e8605172dce0`.
- **Do not copy `HF_HUB_OFFLINE = "0"`** (`:5`). The runtime sets `"1"`.

### N3. §5.1 asks the tripwire to flag look-alikes it cannot flag

- v2 §2 defines the tripwire as a **verbatim** match, or any **4-word window** of a template, after normalisation.
- The exp-3 Q1/Q2 mirrors, the exp-8 Q3 mirror and the old `DEV_PROMPT` share **no 3-gram** with any template (round 1, computed by both reviewers). So they share no 4-word window either.
- v2 §5.1 nonetheless requires "the tripwire flags the exp 3–9 `PROMPTS`, the old `DEV_PROMPT` and verbatim templates".

As written, an implementer can only pass §5.1 by turning the tripwire into a fuzzy matcher, which contradicts §2.

**Fix:** rewrite §5.1 as: "flags each verbatim template and every 4-word window of each (tokenisation pinned: lowercase; words `[a-z]+('[a-z]+)?|'[a-z]+`; split at `{}`; no window across the slot); passes the cleaned base; and the record shows that the four known look-alikes are *not* flagged, which is the stated limit." Also state that template fragments shorter than four words after the split (Q2's `if you visit`) are never matched.

---

## 3. The brief's questions 2–6

### Q2. Can the editor run without the harness? Does the handoff reproduce today's scoring?

**Yes on both, given N2.** See N2(b) for the full name table: nothing evaluation-bearing is needed on the editor side.

The handoff is already cross-process today. The editor saves the **full changed tensors** (`prepare.py:217`), not deltas; v2 §1's word "deltas" should be corrected. The scorer, in a fresh process, validates names, shapes, dtypes and finiteness against the manifest (`prepare.py:262-265`), copies the tensors in, and measures.

There is direct evidence that this reproduces bitwise across processes under the fence. The loop's own baseline run `runs/20261006-131156_nocommit/score.json` has:
- the same three `saved_sha256` values as `results/autoresearch_c10_equivalence.json` (A1 `2f72fee2…`, A2 `f94e1be2…`, A7 `c30664a9…`);
- `templates_sha` `e8605172dce0`;
- summary 7/7/40/69/69/0/1/90.38/30/21.506/88.974.

So the only new risk is the editor runtime's loader (N2(c)).

**ADVISORY 2a.** Make the LAW#3 criterion in v2 §1 and §5.5 exact and bitwise:
- `saved_sha256` per arm equal to the record;
- `templates_sha` `e8605172dce0` from the **editor** process (check_equivalence's `templates_sha_this_process` must now be computed under `editor_runtime`) and from the scorer;
- every summary field equal.

Run it **through `fence/run.sh` with both profiles**. `check_equivalence.py` as it stands runs in one unsandboxed process (`:14-15`, `:49`) and does not exercise the new plumbing.

### Q3. Network and side channels

`(deny network*)` in both run profiles, plus a network-denied Bash sandbox, closes the Chrome debugging port (127.0.0.1:9222, listening at round 1), the localhost Python servers and git/gh over the network from those layers. Residual points:

- **7a (ADVISORY), the scorer resets the offline flag.** The harness sets `HF_HUB_OFFLINE = "0"` at import (`c10e_bandknob.py:5`), which overrides the wrapper's flag inside the scorer. With the network denied, the load then depends on huggingface_hub returning the cached file for a pinned commit hash without a network call. The §5.5 GPU run will show whether it does; add a no-GPU tokenizer load under the scorer profile to §5.3 so a hang or timeout is caught early.
- **7b (ADVISORY), the keychain.** `(allow default)` still allows executing `/usr/bin/security` and the mach lookup to securityd.
  - The network deny stops the editor from *using* a credential, but agent code could still write one into the run folder. The agent could then use it through **WebFetch**, a Claude Code tool that the Bash sandbox does not cover.
  - Fix: in both run profiles, add `(deny process-exec (literal "/usr/bin/security"))`. If MPS still works (probe), also add `(deny mach-lookup (global-name "com.apple.SecurityServer"))`.
  - Probe `security find-generic-password -s gh:github.com` (exit code only) from the editor profile and from the agent's Bash.
- **7c (ADVISORY), environment tokens.** `launch.sh:100` runs `exec claude` with the operator's whole environment, which the agent's Bash inherits. I could not check whether a token variable is set (the classifier refused).
  - Fix: launch with `env -i HOME="$HOME" PATH=/usr/bin:/bin:/usr/sbin:/sbin:<claude dir> TERM="$TERM" LANG="$LANG" USER="$USER" claude …`, and the wrappers likewise.
  - `~/.config/gh` is already denied, as a home child (`sandbox_settings.py:134`).
- **7d (ADVISORY), WebFetch.** The tool fetches outside the Bash sandbox. Add permission denies for `WebFetch(domain:github.com)`, `WebFetch(domain:raw.githubusercontent.com)`, `WebFetch(domain:api.github.com)`, `WebFetch(domain:notebooklm.google.com)`, `WebFetch(domain:docs.google.com)`, `WebFetch(domain:drive.google.com)`, `WebFetch(domain:claude.ai)`.
  - In the §5.4 probe, try the private repo's raw harness URL, with and without a credential in the URL, and `http://127.0.0.1:9222/json/version`.
- **7e (ADVISORY), MCP.** `--safe-mode` disables MCP servers (`AUTORESEARCH.md:57`). Have the §5.4 probe record its tool list, to show that no `mcp__` tool is present.

### Q4. Tripwire

A program-side, silent, verbatim 4-word-window check is the right mechanical part. It cannot be queried, it catches copying and leaks into the transcript, and its limit is stated correctly in §2. Fix §5.1 per N3. Three implementation details remain, all ADVISORY:

- **4a, what to scan.** "Every `edit.py` commit" needs git on the sandbox repo from the program side, which the program session's worktree guard refuses. Runs are also unattributable today: every run folder is named `…_nocommit`, because `git rev-parse` fails inside the profile (`prepare.py:194`; all 10 old run folders).
  - Fix: before stage A, `run.sh` copies the exact `edit.py` that runs, with its sha256 and a timestamp, into the fence-owned results folder. The tripwire scans those copies plus the transcript, and the sha256 names the run.
- **4b, which transcript.** `audit_transcript.py:13` globs `*autoresearch-sandbox-c10*`. The new path `autoresearch_v13_c10` gives the slug `…-autoresearch-v13-c10`, which that glob does not match. The audit would print "NO TRANSCRIPT FOUND" and the tripwire would scan nothing. Update the glob together with `:18`.
- **4c, source of truth.** The templates come from the harness's `PTEST`, imported program-side. With that, v2 §1's "sealed files" has no remaining content: the scorer reads `PTEST` from the harness. Drop "sealed files" or name what they hold.

### Q5. Base order and fallback

The order is sufficient: LAW#3 through the new plumbing on fd16592, bitwise per 2a, then the cleaned base, with the seed pinned per N1.

The fallback is right as far as it goes. Two additions (ADVISORY):
- **5a, porting the seeds.** Both seeds change only their import line (`from prepare import` becomes `from editor_runtime import`). The runtime keeps the same names and signatures, so the recipe code is byte-identical below the import. Record that diff.
- **5b, optional measurement of the mirror contribution.** The program re-scores `73f78ce` unchanged (34/72 expected) through the new plumbing. The difference from the cleaned base, per template, is the mirror contribution. It is the program's own run, never shown to the agent.

### Q6. Further details that could go wrong (ADVISORY)

- **A1, output channels.** Harness source lines already reach the agent. The round-1 equivalence `scorer_tail` shows a `UserWarning` that prints `c10e_bandknob.py:213` and its source line, from `run_law5 → my_edit`. Today that stream goes to `run.log`.
  - v2 §1's intent ("only the summary line") must be written into `run.sh` as code: send scorer stdout and stderr to a fence-owned log, and append to `run.log` only the lines matching `^(heldout_full|canon|first_token|A1|A2|L1_flips|frame_flips|described_as|L3|ppl_post|law5_ok|scope_ok|dw_total|edit_seconds|score_seconds|guards):` plus a fixed `scorer exit N` line.
- **A2, `setup.sh` is unspecified.**
  - It should (1) import `editor_runtime` under the editor profile, and (2) run the scorer's `setup_checks` (fingerprint, reference controls, LAW#5) under the scorer profile.
  - Only `Done! Ready to edit.`, or a fixed failure category, goes into `prepare.log`.
  - Update `program.md:16` and `:125` to match.
- **A3, the fence results folder.** It must be writable by the scorer profile only. Today the fence is denied for writes in every layer (`sandbox_settings.py:177`, `:194`, `:199`) and `chmod 555` (`launch.sh:93`). Either put the folder outside the fence, under the program checkout (already denied to the agent and the editor), or write the rule order explicitly: last match wins in Seatbelt.
- **A4, `kill_run.sh` covers both stages.** Accept the scorer's exact command line and its working directory (the engine directory) as well as the editor's.
- **A5, seed sweep.** Round-1 A10 is not in v2 §5. The old repository's tree tracks `graft/` cards and the harness copy (`73f78ce` tree: `.ignore`, `graft`, `c10e_bandknob.py`, …). Add a §5 check that the new repository's files and every git object contain no 4-word window of a template, and that the repository was seeded by copying named files, not by clone or fetch.
- **A6, scorer input integrity (not sealing; noted only).** Between the editor's exit and the scorer's start, the agent can replace `runs/*/A*.pt` with weights computed elsewhere, bypassing the edit budget. The window is longer than today. If wanted: `run.sh` records the sha256 of the `.pt` files at editor exit and the scorer refuses on a mismatch.
