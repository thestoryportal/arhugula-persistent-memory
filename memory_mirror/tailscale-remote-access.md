---
name: tailscale-remote-access
description: "Set up 2026-10-07: Tailscale on the MBP as a user LaunchAgent in userspace-networking mode (no sudo); host robert-mbp / 100.118.225.127 / robert-mbp.tail36ce25.ts.net, account thestoryportal@github; the operator SSHes in from Termius on the iPhone to watch the team dashboard."
metadata:
  node_type: memory
  type: reference
  originSessionId: ef74c20d-d259-4cb7-9e93-31d8d916f184
  modified: 2026-10-07T22:47:32.757Z
---

- Install: `brew install tailscale` (CLI 1.102.5). Daemon: `~/Library/LaunchAgents/com.rhu.tailscaled-user.plist` runs `tailscaled --tun=userspace-networking` with state + socket in `~/Library/Application Support/tailscale-user/`; log `~/Library/Logs/tailscaled-user.log`. RunAtLoad + KeepAlive. No system extension, no root.
- CLI needs the socket: `tailscale --socket "$HOME/Library/Application Support/tailscale-user/tailscaled.sock" status`. Restart: `launchctl kickstart -k gui/$(id -u)/com.rhu.tailscaled-user`.
- Userspace mode delivers incoming tailnet TCP to local services; verified 2026-10-07 by `tailscale nc 100.118.225.127 22` returning the OpenSSH banner. The Mac itself cannot route to other 100.x peers without the socket proxy.
- Phone path: Tailscale iOS app (same account) + Termius host `robert-mbp`, port 22, user robertrhu, then type `teamdash` (`~/.local/bin/teamdash`: attach the dashboard or build it with `tools/team_dashboard.sh`; Termius snippets are a paid feature). The Mac must be awake. Related: [[ollama-serves-winning-defense-graphify]] (other background services on this Mac).
- 2026-10-08: the operator also watches `teamdash` from **Omarchy, a QEMU VM on this Mac** (`/Applications/Try Omarchy.app`, user-mode networking, `hostfwd=tcp:127.0.0.1:2222-:22`; guest user robbo; no Tailscale inside it, no Wi-Fi of its own). From the VM the Mac is `10.0.2.2` (its SSH logins show in `last` as 127.0.0.1), which survives Mac Wi-Fi changes: `until ssh -t -o ServerAliveInterval=10 -o ServerAliveCountMax=3 robertrhu@10.0.2.2 'zsh -lc ~/.local/bin/teamdash'; do sleep 3; done`. The auto-mode classifier blocks this session from SSHing into other machines.
