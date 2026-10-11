---
name: codex-watch-anchor-replies-read-context-from-rollout
description: Watching a Codex pane — anchor reply tokens at line start (the brief echoes them) and read Context % from the rollout log when the footer is cut off
metadata:
  type: feedback
---

Two watcher traps hit on 2026-10-11 (MAESTRO32):

1. **Reply-token false match.** A brief that says `reply "BRAIN1 HANDOFF"` puts that phrase on screen, so `grep 'BRAIN1 HANDOFF'` over the pane fires instantly. Anchor the match to line start: `^(• |  )?(TOKEN)` on `tmux capture-pane -p -J`. Run the watcher once (`ONCE=1`) as a positive control before arming it.
2. **Context % unreadable.** When the operator attaches to a builder's session from a narrower client (phone, `tmux attach` grouped session), the window shrinks and the footer truncates to `Context …`. Read it instead from the Codex rollout: `R=$(grep -l '<brief first line>' $(find ~/.codex/sessions -name 'rollout-*.jsonl' -mmin -240))`, then the last `"token_count"` event: `100*(1 - last_token_usage.input_tokens / model_context_window)`. This raw figure runs a few points below the TUI's figure, which errs safe.

3. **"Context compacted" false match (MAESTRO36, 2026-10-11).** The brief's own context rule says "…or any Context compacted, stop…", so a builder that `cat`s its brief puts the phrase on screen and a bare grep fires at 60% left. Detect compaction from the rollout instead: `grep -qE '"type":"(compacted|compaction)"' "$R"` (both types seen in real compacted rollouts), or the pane line anchored `^(• )?Context compacted`. A MAESTRO's Monitor can also outlive its reset, so expect a duplicate alert from the predecessor's watcher.

Also: an auto-mode classifier blocked MAESTRO sending Enter to answer a builder's pending question. The fix was to give the operator a grouped session (`tmux new-session -d -s <x>-op -t <builder>`; they `tmux attach -t <x>-op`) and let them press it. Do not retry the keypress in another form.

**Why:** a false "HANDOFF" or an empty context reading both look like a real signal and misroute the next action.
**How to apply:** for every new Codex watch, anchor the tokens, source the context from the rollout, and dry-run once. Template: MAESTRO32 scratchpad `brainwatch.zsh`. Related: [[never-idle-arm-completion-watch]], [[codex-hook-trust-prompt-at-launch]], [[context-management-every-session]].
