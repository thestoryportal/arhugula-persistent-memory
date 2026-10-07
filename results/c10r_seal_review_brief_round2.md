# Review brief round 2 — D-C10r-seal design v2

Same hard limits as round 1: review only; no model, no GPU (step 1 is running), no launch.sh/prepare.py/edit.py/check_equivalence.py; edit nothing but your output file; `/usr/bin/git`. Output: Codex → **`results/c10r_seal_codex_design_review_round2.md`**; Claude advisor → **`results/c10r_seal_advisor_design_round2.md`**. Then say DONE.

`docs/C10R_LOOP_SEALING_V13.md` is now DRAFT v2. It replaces v1 after your round-1 reviews (`results/c10r_seal_codex_design_review.md`, `results/c10r_seal_advisor_design.md`).

## Questions
1. Go through each of your round-1 BLOCKING items: resolved / not resolved / superseded, with evidence from the v2 text and the current code it will change.
2. **The two-process split (§1).** Can the editor really run without the harness? List every name `edit.py` at `73f78ce` (in `/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10`; read the file at HEAD, not via git if git is refused) and the current loop `prepare.py` take from `prepare`/`H`. Which ones are evaluation-bearing, and which belong in `editor_runtime.py` or `train_facts.json`? Is anything the editor needs only derivable from evaluation stimuli? Does the handoff (saved deltas → fresh model in the scorer) reproduce today's scoring exactly, so the equivalence check can pass?
3. **Network and side channels.** Is `(deny network*)` plus offline flags enough in both profiles and in the agent's Bash sandbox? What about the agent's own WebFetch/WebSearch tools in `--safe-mode`, an MCP, the keychain, the Chrome port, `gh` auth tokens in the environment or `~/.config/gh`?
4. **Tripwire (§2).** Is a program-side, silent, 4-word-window verbatim check the right mechanical part? Is its honest limit stated correctly?
5. **Base and LAW#3 (§3).** Is the order (equivalence through the new plumbing reproducing fd16592 exactly, then the cleaned base) sufficient? Is the fallback right?
6. New BLOCKING issues; what implementation detail is still unspecified enough to go wrong.

Format: header (reviewer, model, effort, date), **Verdict: PROCEED or FIX-FIRST**, numbered items with file:line, BLOCKING/ADVISORY, the exact fix.
