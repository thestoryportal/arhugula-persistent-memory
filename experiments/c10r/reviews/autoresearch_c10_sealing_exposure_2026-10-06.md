# Autoresearch loop: where the agent can see the held-out templates (2026-10-06 late evening)

**Operator ruling D-C10r-rulings-6 (this evening):** hide the held-out test templates from the loop agent and forbid look-alike phrasings, together with fence v13, before the loop relaunches. This note is the exposure map the sealing design starts from. It comes from a read-only Sonnet search; the sandbox's git history could not be read (the worktree guard refuses git on other repos), so item 5 is inferred.

## Exposures (each must be closed or made moot)

1. **Sandbox harness copy, verbatim.** `autoresearch_sandbox_c10/c10e_bandknob.py:52-56` (PTEST; also used at :363-365, :376, :485, :578). It is copied in read-only by `launch.sh:62-64` and hash-checked at `:74-80`, and `program.md:15` tells the agent to read it.
2. **Program harness via the runtime allow-list.** `sandbox_settings.py:61` re-opens `experiments/track_c/c10e_bandknob.py` for the agent's own Read/Bash, not only for the Seatbelt wrappers.
3. **The block-list spells the templates.** `prepare.py:69-71` `_FORBIDDEN` contains "capital city is called", "its capital city is", "seat of government". The guard itself publishes the fragments it guards.
4. **Caches in the sandbox:** `graft/.cache/extract.c3679fb5d24a63a0.json` (the full harness and prepare.py source) and `__pycache__/c10e_bandknob.cpython-311.pyc` (string constants); `graft/.cache/ask-index.json` gives the vocabulary only.
5. **Sandbox git history (inferred):** `launch.sh:57-68` commits a harness copy at every base, so `fd16592` and its descendants through `73f78ce`/`978fed9` very probably carry PTEST and `_FORBIDDEN`.
6. **Fence hole: `/tmp/claude-501` children.** Other sessions' folders are denied only if they existed when the settings were generated (12:55). `/tmp/claude-501/c10r-v31` (18:28, the exp2ctl clone) holds the harness and prepare.py, and any later folder is readable. This is a design defect in `sandbox_settings.py` (~:95-110), not only stale state.
7. **Look-alikes the agent wrote:** `edit.py:37-39` PROMPTS (two paraphrase Q1/Q2) and `edit.py:36` DEV_PROMPT `"{} has a capital called"` (close to Q1; printed to run.log at `:174`).

## Not exposures
- Scoring runs `prepare.py --score` inside the fence wrapper (`fence/run.sh:21`, sandbox-exec), which imports the harness from `PROGRAM_ROOT` (`prepare.py:85-86`). The agent never needs the template text at runtime.
- run.log, results.tsv and the printed summary carry numbers only. `runs/*/score.json` carries per-template hit vectors by index (no text), which is acceptable; per-template counts are part of the loop's own reading.

## Design consequences (input to the sealing prereg, not yet decided)
- Close 1, 2 and 4 by making the harness and its caches agent-unreadable while the Seatbelt wrappers keep read access: a separate allow-list for wrappers vs agent, no harness copy in the sandbox, and launch-time cache cleaning.
- Close 3 by checking `edit.py` against a hashed n-gram set rather than readable fragments. This changes `prepare.py`, so the equivalence check must be re-run (~1 h GPU) and `HARNESS_SHA256`/the prepare hash updated.
- Make 5 moot with a fresh sandbox repository (new history) seeded from a cleaned base, not a rewrite of the old one.
- Close 6 by denying every `/tmp/claude-501` child except the agent's own folder (deny-by-default, not by enumeration at launch).
- For 7: a `program.md` rule forbidding write or dev prompts that paraphrase any evaluation question, plus the relaunch base. Recommended: the best commit with its mirrored prompts removed, re-scored as the new baseline, because experiments 3 onward were tuned on look-alikes. The prompts check in `prepare.py` cannot catch paraphrases of text the agent can no longer see, so the rule and the reviewers carry that part.
