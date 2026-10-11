# Intel Mac setup log (D-HW-2 follow-on)

- 07:14Z: reformatted Intel Mac seen on the Thunderbolt Bridge at 192.168.10.2 (M3 is 192.168.10.1); file sharing on, remote login off.
- ~07:20Z: operator chose access option A: "A: and I have enabled remote login on the Intel". MAESTRO created a key used only for the Intel Mac: `~/.ssh/intel_mac_ed25519` (ed25519, no passphrase, M3 user only). Intel host key: SHA256:mSQnQU1Xc9GvwyuPg8HJbbWfvWLXk2CZYpxok5sV+sw.
- The account short name is `robertrhu_node2` (full name "Mac Intel Node"); `robertrhu_node` and the guess `macintelnode` do not exist, which is why the password kept being asked for. The M3's ~/.ssh/config ControlPath folder `~/.ssh/sockets` was missing; MAESTRO created it (mode 700).
- 07:40Z: key login works. Read-only inventory: `inventory_20261011T0740Z.txt` (command: `inventory_cmd.sh`, which skips `python3` because it would trigger the developer-tools install prompt).

## Findings that differ from the design's assumptions
- Disk: 512 GB SSD (APPLE SSD AP0512N; 500.0 GB APFS container; 482.5 GB free), not a 1 TB HDD. The approved caps (686 GB + 100 GB free, design.md §4) do not fit; they were conditional on this measurement.
- Sleep on power: `sleep 1` (sleeps after 1 minute idle). An always-on support host needs sleep off on power.
- FileVault: off.
- No Homebrew, no Command Line Tools (git and python3 are stubs that prompt an install); rsync 2.6.9.
- Hardware: MacBookPro16,2, i5-1038NG7 (4 cores / 8 threads), 16 GB, macOS 14.8.9 (23J631), x86_64.
- Networks: Intel internet via Wi-Fi gateway 192.168.1.1; the M3 is on 192.168.8.1 / 192.168.9.155, a different network. Only the cable joins them.
- 07:42Z: operator chose to shrink the caps to fit (decisions_log.md amendment 16) and to leave FileVault off (amendment 17).
- ~07:45Z: operator: both Macs are on the same Wi-Fi again (both gateway 192.168.1.1, verified) and sleep is off on power (`pmset` AC sleep 0, verified).
- Operator request: an open-source replacement for Universal Control (one keyboard and mouse across both Macs; no Apple ID on the Intel Mac). Chosen: Deskflow v1.27.0 (GPL, upstream of Synergy). Both DMGs matched GitHub's sha256 digests and sums.txt (arm64 dd21e79e…0c97, x86_64 8aca3c77…f5d8); the app is Developer ID signed (5QCJCX8C37) and Apple-notarized (spctl accepted). Installed to /Applications on both Macs; signatures re-verified; the Intel binaries are x86_64.
- Setup (files in `deskflow/`): M3 = server bound to the cable address 192.168.10.1:24800, TLS on with peer fingerprint checks; Intel = client of 192.168.10.1; layout: Intel to the right of the M3 (operator). A LaunchAgent opens Deskflow at login on each Mac. Settings keys taken from upstream src/lib/common/Settings.h at v1.27.0 (coreMode: 1 = client, 2 = server).
- MAESTRO slip: running `lipo` on the Intel Mac (no developer tools) opened Apple's developer-tools install dialog there. The operator needs those tools next anyway.
