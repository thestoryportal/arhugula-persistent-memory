# Advisor review: D-C10r-seal design (docs/C10R_LOOP_SEALING_V13.md, DRAFT v1)

reviewer: Claude advisor subagent, model Opus 5.5
date: 2026-10-06 (late evening). Read-only review: nothing loaded a model or touched the GPU. One string-only Python check was run (item 3), and its scratch file was deleted afterwards.

**Verdict: FIX-FIRST**

The goal and the exposure map are right, but five things block. Two of the design's load-bearing premises are false against the current code. The scorer is not the only reader of the templates, because the agent's own `edit.py` runs with the same privileges. And the 3-gram rule does not catch any of the four look-alikes it is meant to catch. On top of that, the network path is open, the relaunch-base description and gates do not match the files, and §3 overstates what the reseal buys.

---

## BLOCKING

### 1. Agent-written code runs with the reader's privileges, so "one reader: the scorer process" is false (Q1)

Evidence:
- `run.sh:21` runs `edit.py` under the same `.sandbox.sb` that grants the harness read (`sandbox_settings.py:54`, profile lines `:173-174`). `run.sh:5` says it outright: "The scorer and fingerprint subprocesses inherit the profile."
- `edit.py` imports `prepare` (source `edit.py:16`; 73f78ce `edit.py:18`). `prepare.py:85-86` imports the harness into that same process and exposes it as `prepare.H` (`:86`, `:93`). So the agent's code can reach `prepare.H.PTEST`, `sys.modules["c10e_bandknob"]`, `inspect.getsource(prepare.H)` and `open(prepare.HARNESS)`. It can also call `H.run_recipe`, which prints all three templates (`c10e_bandknob.py:485`) and dumps them into a JSON (`:578`). Every one of these lands in `run.log` or in the sandbox.
- The scorer is the sandbox copy of `prepare.py`: `prepare.py:222` runs `os.path.abspath(__file__)`. The agent can write that copy, because `launch.sh:57` copies it without `chmod a-w` and the sandbox is in `allowWrite` (`sandbox_settings.py:161`, `:193`). No per-run hash check guards it; `launch.sh:29-35` checks only the source copy at launch.
- Decision 2's `$FENCE/sealed/forbidden.json` is "readable only by the wrapper's Seatbelt profile". That profile is the one `edit.py` runs under, so agent code can read the file directly, before it even imports `prepare`.

Exact fix:
- Use **two run profiles**.
  - `edit.sb`: the agent-side reads plus the model runtime, with no harness, no sealed material and no network (see item 2).
  - `score.sb`: `edit.sb` plus a literal read of the harness.
- `run.sh` runs two stages:
  - **Stage A:** `edit.py` under `edit.sb`. `evaluate()` saves the `.pt` files and `edits.json`, then returns. It no longer starts the scorer subprocess (drop `prepare.py:222-225`).
  - **Stage B:** `run.sh` itself runs a **fence-resident scorer** `$FENCE/score.py`. That file is mode 444, `run.sh` checks its sha256 against the equivalence record before each run, and it runs under `score.sb`. Only the summary keys it prints go to `run.log` (item 8).
- The edit-side runtime must not import `c10e_bandknob` at all.
  - Generate a training-side extract at launch, the way `write_reference_controls.py` does for v6: `CANON`, `FICTION`, `ARMS` values, the `req` format.
  - Add a small loader that reproduces the harness's model load: `ID`/`REV`, fp16, `DEV`, the `os.chdir(ENGINE_ROOT)` at `:8`, the engine on `sys.path`, and the seed order (`prepare.py:83` then load).
  - `check_equivalence.py` proves it: bitwise recipe equality as at `:28-35`, plus `templates_sha` identical to the **old** record. Without that second check, old and new scores are not comparable (item Q5-iii).
- Implementation trap: once the sandbox harness copy is gone, `import c10e_bandknob` fails in the scorer. `experiments/track_c` is not listable (only the file is a literal allow), and CPython's `FileFinder._fill_cache` treats an unlistable directory as empty. Load the harness by path with `importlib.util.spec_from_file_location`.
- Add to §2: a **hostile `edit.py` probe** run through the real `run.sh`. It tries to open the harness path, the sealed path (if any), and `prepare.HARNESS`; prints `sys.modules` keys and anything named PTEST; calls `inspect.getsource` on every module it can import; and makes the network calls in item 2. Every item must fail or come back empty in `run.log` and the sandbox. A second probe modifies the sandbox `prepare.py`, and the scorer must refuse to run.

### 2. The network is open from both run profiles, and a signed-in browser is listening on localhost (Q1)

Evidence:
- The profile is `(allow default)` (`sandbox_settings.py:170`).
- `docs/AUTORESEARCH.md:57` lists "the network is open" as an accepted limit. That was accepted when the concern was files.
- At review time, `lsof` showed Chrome (PID 9204) listening on **127.0.0.1:9222**. That is the CDP port of the signed-in browser the program drives through Browser Harness. Two unidentified Python listeners were also up, on 127.0.0.1:8770 and :8137.
- The program repository `thestoryportal/arhugula-persistent-memory` is **PRIVATE** (`gh repo view`). It tracks `experiments/track_c/c10e_bandknob.py` and `results/autoresearch_c10_heldout_mirroring_2026-10-06.md`, which quotes all three templates.

So under the current single profile, agent code in `edit.py` can drive the signed-in browser to the repository and read the templates. From the agent's own Bash, a keychain-backed `git`/`gh` call is untested.

Exact fix:
- Add `(deny network*)` to both run profiles. Set `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1` in the wrappers. Re-allow local unix sockets only if a probe shows Metal or torch needs them.
- In the agent's Bash sandbox, restrict the network to the paper domains `program.md:36` allows, with no localhost.
- Add to §2, run from the agent Bash and from inside both profiles. Each of these must fail:
  - `curl -s 127.0.0.1:9222/json/version`
  - `git ls-remote https://github.com/thestoryportal/arhugula-persistent-memory`
  - `gh api repos/thestoryportal/arhugula-persistent-memory/contents/experiments/track_c/c10e_bandknob.py`
  - `security find-internet-password -s github.com`

  Also check that a WebFetch of the private repo's raw harness URL returns no content.

### 3. The 3-gram rule catches none of the observed look-alikes, and as written it is a membership oracle (Q3)

I computed the rule as step 1's prereg states it (`docs/C10S_SHARED_Z_PREREG.md:26`): word 3-grams after the subject slot is removed, lowercased, `'s` kept as a token. I tried both joining across the slot and splitting at it; the results are the same.

| Prompt | Shared 3-grams with any held-out template |
|---|---|
| exp 3 Q1 mirror `{}'s capital is the city of` | **none** (only the 2-gram `'s capital`) |
| exp 3 Q2 mirror `When you travel to {}, the capital is the city of` | **none** |
| exp 8 Q3 mirror `The largest city and capital of {} is the city of` | **none** (only the 2-gram `city and`) |
| old DEV_PROMPT `{} has a capital called` | **none** |
| step-1 withdrawn v1 `In {}, the capital city is` | `capital city is` (rejected) |

So §1.2's "so it catches the Q1/Q2 mirrors of experiments 3 to 8" is false, and §2.1 ("rejects the experiment 3–9 PROMPTS and the old DEV_PROMPT") cannot pass. The mirrors are structural paraphrases, not lexical copies.

There are two more problems:
- **The refusal is an oracle.** The current refusal prints the matched phrase (`prepare.py:74-76`), so a refusal message echoes forbidden text. Even a generic refusal is a cheap oracle at that point: it fires at import, seconds before the model loads. "The refusal is final" invites the agent to retry with another literal, which is exactly how an oracle gets queried.
- **The literal scan is narrow.** A scan over "every string literal" misses strings built at run time: concatenation, `.join`, `chr`, data read from a file the agent writes.

Exact fix:
- Restate the rule as a **verbatim-fragment tripwire** only.
- Move it out of every process the agent can reach. The program-side watcher checks each sandbox commit's `edit.py`: AST string literals including f-string parts and docstrings, with the tokenization pinned (lowercase; `[a-z]+('[a-z]+)?|'[a-z]+`; split at `{}`; no 3-grams across the slot).
- Take the source of truth from the harness's `PTEST` (and, if wanted, `L1_PROMPTS`/`L3_PROMPTS`/`GENERIC`), imported program-side. Then no `forbidden.json` copy needs protecting (this also resolves A1).
- A hit is a **silent flag** that fires the stop rule. The agent gets no signal.
- If a hard refusal is kept anyway, put it in the scorer after the edit (about 45 minutes per query, not seconds), use a fixed message that names neither the literal nor the n-gram, and stop the loop on the first refusal.
- Rewrite §2.1 as follows: the tripwire rejects the three verbatim templates, every 3-gram of each, and the withdrawn v1 form. The record documents that the four observed look-alikes **pass**.
- State the limit plainly. Lexical checks miss all observed mirrors and runtime-built strings. Semantic closeness is closed only by author-blindness. After the reseal, a blind agent will very likely write natural rewordings again; `{}'s capital is the city of` is the most natural one. That is legitimate training on paraphrases, the same thing step 1's T1/T2 do. It is not a leak, but it does change what the score means (Q5-ii).

### 4. The relaunch base is mis-described, and its gates conflict with the launcher (Q2, Q4)

**(a) Content.** I read 73f78ce's `edit.py` (old sandbox working tree, `results.tsv:11`).
- It does **not** contain the two-stage change: `ae66823` was discarded (`results.tsv:9`).
- The preserve term is experiment 2 (`92acd03`), not 3–9.
- What 73f78ce actually carries from experiments 3–9:
  - KL 0.125 (`edit.py:30`)
  - preserve weight 4 (`:34`)
  - **GAIN 1.25** (`:35`, `:155`), the 30 → 34 step
  - the eigh projector (`:53`)
  - a custom joint `solve_z` over `PROMPTS` (`:87-139`), which replaces the engine's `compute_z`
  - the dev probe (`:172-177`)

  Fix decision 4's list. Also clean the docstrings that describe the removed prompts (`:4-6`, `:88-90`).

**(b) Who writes `DEV_PROMPT`.** A replacement `DEV_PROMPT` written by the program session, which has the templates in view, repeats step 1's stated limit ("authored with the held-out set in view"). Set `DEV_PROMPT = CANON` or delete the probe block. Do not author a new wording.

**(c) The launch gate.** `launch.sh:29-35` refuses to launch unless the equivalence record covers `SRC/edit.py`, and `check_equivalence.py:28-35` requires that file to be bitwise-identical to the harness's own `my_edit`, i.e. the baseline. So the cleaned base cannot be `SRC/edit.py`.

Fix: keep the baseline as `SRC/edit.py` for equivalence. Ship the seed as a separate reviewed file (e.g. `edit_relaunch_base.py`) with its own hash in the seal record. `launch.sh` copies it into the new sandbox as `edit.py` and checks that hash.

**(d) LAW#3 anchor lost.** Today the first loop row must reproduce the equivalence numbers exactly (`docs/AUTORESEARCH.md:57`: 7 / 7 / 40 / 69 / 69 / 0 / 1 / 90.38 / 30 / 21.506 / 88.974). With the cleaned base as the first row, the new plumbing has no known value to land on.

Fix: before the loop starts, the program runs the baseline `edit.py` through the **new** `run.sh` and both profiles, and requires an exact reproduction. Recommended: also re-score 73f78ce unchanged and require 34/72. Only then score the cleaned base.

**(e) Pre-register a fallback.** If the cleaned base fails a guard, the base becomes `92acd03`. The other knobs were tuned in a three-prompt regime, and KL 0.125 entered (`results.tsv:6`) to rescue `described_as` under three prompts.

**On the choice itself (Q2).** I agree with 73f78ce minus the prompts over restarting at `92acd03`:
- None of the carried knobs encodes template text.
- Every loop decision, `92acd03` included, was selected on the same 72 reads. A restart therefore buys no clean selection history; only a fresh promotion set does (item 5).
- The cleaned base is re-measured from scratch anyway.

The honest check is Q3, which was never mirrored in the kept chain (the Q3 mirror `e475185` was discarded). Record the cleaned base's Q3 count next to 73f78ce's. If the gains from GAIN and KL hold on Q3, they do not depend on the mirroring.

### 5. §3 overstates what the reseal restores

§3 says promotion "needs a sealed set the agent never read, which these templates now are again for every experiment after the reseal." That is wrong:
- The three templates are the loop's **selection metric**, so loop output selected on them can never be confirmed on them, whether or not the agent can read them.
- They were read in full by the agent's predecessor and by the author of the relaunch base.
- The mirroring finding says it correctly (`results/autoresearch_c10_heldout_mirroring_2026-10-06.md:32`): "any promotion needs a fresh sealed set of rewordings the agent has never read".

Fix: replace the clause with "the templates are hidden from the agent again; they remain the loop's selection metric, so promotion still needs a fresh pre-registered set of rewordings neither the agent nor the selection ever touched." This is a wording fix, but as written it could let loop output be promoted past the gate.

---

## ADVISORY

1. **Location of the sealed file, if one is kept.** `$FENCE` is agent-readable: it is in `runtime_reads` (`sandbox_settings.py:62`) and has a `Read(fence/**)` allow (`:200`). If any sealed file remains, keep it outside both the fence and the sandbox (inside the program checkout, already denied in all three layers) and give `score.sb` a literal allow. Item 3's fix removes the need for the file.
2. **Enumeration at launch still applies elsewhere.** It covers `~/.cache` children (`:89`), `~/Library/Caches` (`:140`), home children (`:134`), and, for the file tools, the mirror-root children (`:156-158`; also an accepted limit at `AUTORESEARCH.md:57`). These are the same defect class as exposure item 6. For example, a program clone created in the mirror root after launch is readable by the Read tool. Fix: move the new sandbox and fence **out of the mirror tree**, so the file tools get one `Read(//mirror/**)` deny with no enumeration (they do not need the hf or covariance caches). Otherwise add a post-launch-created folder to the §2.2 test in each region.
3. **TMPDIR (5a/5b).**
   - 5b would point the scorer's TMPDIR at the agent-readable folder. Give the scorer a scorer-only TMPDIR.
   - The 5a fallback ("deny the whole `/tmp/claude-501` tree") is what broke the agent's `cat` in probe 11 (`sandbox_settings.py:96-98`). Verify it in an **interactive** session: a background task's output retrieval and a heredoc must both work.
4. **Per-template hit vectors (decision 6).** `score.json` carries `para_full_hits` per template index per subject (`c10e_bandknob.py:369`, written at `prepare.py:292`). Blind paraphrase candidates plus per-template feedback make a per-template hill-climb on hidden wordings. The agent does not need this; the program does. Write the full `score.json` to a scorer-only folder, show the agent only the summary block, and point `split_by_template.py` at the new folder.
5. **The audit no longer matches the new layout.** `audit_transcript.py:18-20` uses `startswith(SB)`, and `…/autoresearch_sandbox_c10` is a string prefix of `…/autoresearch_sandbox_c10_sealed`. If `SB` is left unchanged, reads of the **old** sandbox (harness copy, pyc, graft cards) count as in-bounds. The glob at `:13` matches both slugs. Fix: name the new sandbox so it shares no prefix (e.g. `autoresearch_sealed_c10`), or compare against `SB + "/"`. The old path is hard-coded at `run.sh:8`, `setup.sh:4`, `kill_run.sh:8-10`, `launch.sh:10`, `audit_transcript.py:18` and in the fence paths in `program.md:16,24,111,121`; update all of them.
6. **Cleaning `results.tsv`.** Also strip the form descriptors, not just prompt text: "adds a subject-initial prompt" in rows 5–6 hints at Q1's shape. Mark the old rows `pre-reseal`, so the keep rule (`program.md:115-116`) compares only post-reseal rows, or move them to a separate file. Otherwise 34 becomes the agent's implicit target.
7. **The old agent and session hygiene.**
   - The paused agent session still has the harness in its context. Kill it before relaunch, and do not use `--resume` or `--continue`.
   - Confirm the new transcript is a new file under the new slug.
   - Probe whether `--safe-mode` loads auto-memory.
   - The deny on helper agents (`sandbox_settings.py:199`) has never been tested (`AUTORESEARCH.md:57`: `-p` sessions have no Agent tool). Add one interactive probe. A helper would inherit the same fence, so this is a confirmation, not a new hole.
8. **Scorer output.** The scorer path prints numbers only: `eval_arm`, `axes_*` and `run_law5` at `c10e_bandknob.py:358-448` print only `:416` and `:445`. Some harness paths do print templates (`:485`, `:578`), though. Have `run.sh` pass only the 16 summary keys (`prepare.py:298-301`) into `run.log`, send scorer stderr and tracebacks to a scorer-only log, and give the agent the exit code.
9. **Locality stimuli.** "is described as" stays spelled out in `prepare.py:252` and `:71`, and `program.md:38` names the guard. State that the locality stimuli are not sealed (they are guards, not the metric) and that the tripwire covers `PTEST`, and optionally `L1`/`L3`/`GENERIC`, imported program-side.
10. **Seed-tree sweep.** Add a mechanical check to §2: no file in the seeded new sandbox (README, `program.md`, `edit.py`, `.gitignore`, `results.tsv`) and no object in its git history contains any 3-gram of the templates. Seed it by copying named files, never by clone or fetch from the old sandbox.

---

## Q5: comparability the design should state

- (i) The pre-reseal rows from experiment 3 on are partly test-adjacent, mostly through Q1 (4 → 10 at exp 3). Experiments 0–2 are clean.
- (ii) After the reseal, `heldout_full` measures transfer to the three wordings from whatever training wordings the agent picks blind. That is not like-for-like with experiments 3–9 (wordings chosen with sight of the test), nor with 0–2 (canonical prompt only). Log the number of write wordings per run, from the program-side literal scan.
- (iii) The plumbing changes (two-stage process, a loader that does not import the harness, `prepare.py` edits). Old and new numbers are comparable only if the equivalence check reproduces the old record exactly, including `templates_sha` against the old value, and the baseline reproduces through the new `run.sh` (item 4d).
- (iv) The old commit hashes in `results.tsv` do not exist in the new repository.
- (v) The loop keeps selecting on the same 72 reads, so its numbers stay register candidates (item 5).

## Q4: is §2 sufficient?

No. Add these:
- the hostile-`edit.py` and modified-`prepare.py` probes (item 1)
- the network, CDP and keychain probes (item 2)
- the corrected tripwire tests (item 3)
- the seed-file hash gate, the baseline reproduction through the new plumbing, and the 73f78ce re-score (item 4)
- the folders created after launch, per region (A2)
- the interactive TMPDIR and helper-agent probes (A3, A7)
- the seed-tree sweep (A10)

A probe agent that "finds none" is weak evidence on its own. The direct per-path tests carry the claim.
