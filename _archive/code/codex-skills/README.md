# Codex Hooks

These hooks are a Codex-native compatibility layer for the Claude hooks in `.claude/settings.json`.

They are intentionally conservative:

- `session_start.py` prints the minimum project posture Codex should remember at startup.
- `pre_tool_use_policy.py` blocks only high-confidence boundary violations, especially X-AL-3 design/implementation mixing in a single command.
- `permission_request.py` surfaces paid-provider, credential, destructive, and network-sensitive requests for operator review.
- `stop_gate.py` reports worktree and verification posture without claiming success.

Credential-gated work should advance to the exact credential boundary first. If
no HIL/operator-approval surface is available, log the pending gate with
`just codex-credential-gate ...`, update a human-facing roadmap/status surface,
and proceed only after the non-credential work is proven closed.

Claude remains the canonical source for the original hook set. These scripts map the load-bearing checks into Codex lifecycle events without depending on Claude-specific environment variables.
