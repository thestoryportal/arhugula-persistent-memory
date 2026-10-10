---
name: tailscale-remote-access
description: Tailscale on the MBP (user LaunchAgent, userspace mode, robert-mbp 100.118.225.127); operator watches teamdash via Termius (iPhone) or an Omarchy VM
metadata:
  type: reference
---

- Install: `brew install tailscale` (CLI 1.102.5). Daemon: `~/Library/LaunchAgents/com.rhu.tailscaled-user.plist` runs `tailscaled --tun=userspace-networking` with state + socket in `~/Library/Application Support/tailscale-user/`; log `~/Library/Logs/tailscaled-user.log`. RunAtLoad + KeepAlive. No system extension, no root.
- CLI needs the socket: `tailscale --socket "$HOME/Library/Application Support/tailscale-user/tailscaled.sock" status`. Restart: `launchctl kickstart -k gui/$(id -u)/com.rhu.tailscaled-user`.
- Userspace mode delivers incoming tailnet TCP to local services; verified 2026-10-07 by `tailscale nc 100.118.225.127 22` returning the OpenSSH banner. The Mac itself cannot route to other 100.x peers without the socket proxy.
- Phone path: Tailscale iOS app (same account) + Termius host `robert-mbp`, port 22, user robertrhu, then type `teamdash` (`~/.local/bin/teamdash`: attach the dashboard or build it with `tools/team_dashboard.sh`; Termius snippets are a paid feature). The Mac must be awake. Related: [[ollama-serves-winning-defense-graphify]] (other background services on this Mac).
- 2026-10-08: the operator also watches `teamdash` from **Omarchy, a QEMU VM on this Mac** (`/Applications/Try Omarchy.app`, user-mode networking, `hostfwd=tcp:127.0.0.1:2222-:22`; guest user robbo; no Tailscale inside it, no Wi-Fi of its own). From the VM the Mac is `10.0.2.2` (its SSH logins show in `last` as 127.0.0.1), which survives Mac Wi-Fi changes: `until ssh -t -o ServerAliveInterval=10 -o ServerAliveCountMax=3 robertrhu@10.0.2.2 'zsh -lc ~/.local/bin/teamdash'; do sleep 3; done`. The auto-mode classifier blocks this session from SSHing into other machines.
