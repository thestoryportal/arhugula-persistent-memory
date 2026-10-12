---
name: codex-watch-anchor-replies-read-context-from-rollout
description: Watch completion tokens only in assistant rollout messages; read context/compaction from rollout events; background-terminal waiting is busy
metadata:
  type: feedback
---

Two watcher traps hit on 2026-10-11 (MAESTRO32):

1. **Reply-token false match.** A brief that says `reply "BRAIN1 HANDOFF"` puts that phrase on screen, so `grep 'BRAIN1 HANDOFF'` over the pane fires instantly. Pane anchoring also false-matches echoed briefs (see item 4); use assistant-only rollout messages with positive/negative controls before arming it.
2. **Context % unreadable.** When the operator attaches to a builder's session from a narrower client (phone, `tmux attach` grouped session), the window shrinks and the footer truncates to `Context …`. Read it instead from the Codex rollout: `R=$(grep -l '<brief first line>' $(find ~/.codex/sessions -name 'rollout-*.jsonl' -mmin -240))`, then the last `"token_count"` event: `100*(1 - last_token_usage.input_tokens / model_context_window)`. This raw figure runs a few points below the TUI's figure, which errs safe.

3. **"Context compacted" false match (MAESTRO36, 2026-10-11).** The brief's own context rule says "…or any Context compacted, stop…", so a builder that `cat`s its brief puts the phrase on screen and a bare grep fires at 60% left. Detect compaction from the rollout instead: `grep -qE '"type":"(compacted|compaction)"' "$R"` (both types seen in real compacted rollouts), or the pane line anchored `^(• )?Context compacted`. A MAESTRO's Monitor can also outlive its reset, so expect a duplicate alert from the predecessor's watcher.

Also: an auto-mode classifier blocked MAESTRO sending Enter to answer a builder's pending question. The fix was to give the operator a grouped session (`tmux new-session -d -s <x>-op -t <builder>`; they `tmux attach -t <x>-op`) and let them press it. Do not retry the keypress in another form.

4. **Read the reply token from the rollout, not the pane (MAESTRO38, 2026-10-11).** A brief whose token sits on its own line is echoed in the pane with a two-space indent, so even the anchored `^(• |  )?TOKEN` pane regex matches it at launch (seen with codexre1). Match assistant messages only: `jq -r 'select(.payload.type=="message" and .payload.role=="assistant") | .payload.content[]?.text // empty' "$R" | grep -E '^TOKEN'`. Positive/negative control: a fake rollout with the token in an assistant line (fires) and in a user line (silent). Template: MAESTRO38 scratchpad `re1watch.zsh`. Pane "Waiting" between tool calls can raise a false IDLE; read the pane before acting.

5. **"Waiting for background terminal" is busy, not idle (MAESTRO39, 2026-10-11).** A builder waiting on its own long script shows that footer instead of `Working (`, so a watcher keyed only on `Working (` raises false IDLE alerts (three in one session). Busy test: `grep -qE 'Working \(|Waiting for background'`. Template: MAESTRO39 scratchpad `r2bwatch.zsh`.

**Why:** a false "HANDOFF" or an empty context reading both look like a real signal and misroute the next action.
**How to apply:** for every new Codex watch, match tokens only in assistant rollout messages (item 4), read context/compaction from rollout events, count background-terminal waiting as busy, and run positive/negative controls. Related: [[never-idle-arm-completion-watch]], [[codex-hook-trust-prompt-at-launch]], [[context-management-every-session]].
