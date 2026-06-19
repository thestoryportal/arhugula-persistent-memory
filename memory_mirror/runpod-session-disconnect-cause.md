---
name: runpod-session-disconnect-cause
description: "Why the RunPod Claude Code terminal keeps disconnecting and losing context, and the fix"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2801cf2e-560f-460c-86df-e227b16051b2
---

Root cause (diagnosed 2026-06-17):

**Context loss is NOT a pod restart or OOM.** Pod uptime was 10+ weeks; no OOM/kernel kills; RAM fine (40/503 GB). `claude` runs directly in the SSH pty chain (sshd → -bash → claude), with NO terminal multiplexer (tmux/screen/mosh all absent). When the connection drops, that `claude` is orphaned but stays alive (e.g. observed PID 30931 still running 2h48m after its session dropped); reconnecting opens a NEW pty + NEW bash, and a fresh `claude` starts with no history → the conversation context is gone. Multiple live orphaned claude + sshd (pts/0,1,2) sessions confirm each reconnect is a brand-new login.

**Why the connection drops:** sshd has no keepalives configured (`/etc/ssh/sshd_config`: `ClientAliveInterval 0`, all commented defaults), so idle SSH connections are silently dropped by NAT/proxy/RunPod-proxy timeouts and never kept alive.

**Fixes:**
1. Primary — run claude inside **tmux** (`apt-get install -y tmux`; `tmux new -s work`; reconnect with `tmux attach -t work`). Reattach restores the exact session + full context; disconnects lose nothing.
2. Reduce drops — set sshd `ClientAliveInterval 60` / `ClientAliveCountMax 3` (restart sshd is risky over the live ssh link — do with care; optionally install mosh for roaming/flaky links).
3. For experiments specifically — see [[runpod-durable-experiment-launch]] (setsid detach) so compute survives regardless of the terminal.
