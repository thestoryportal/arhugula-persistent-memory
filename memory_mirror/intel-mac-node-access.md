---
name: intel-mac-node-access
description: How MAESTRO reaches the Intel Mac support host (cable IPs, account, key) and the traps hit setting it up (dev-tool stubs, Deskflow 1.27 config)
metadata:
  type: reference
---

The 2019-era Intel MacBook Pro (MacBookPro16,2, 16 GB, 512 GB SSD, macOS 14.8.9) is the D-HW-2 support host. Setup record: `results/intel_setup_20261011/setup_log.md`.

- **Reach it over the Thunderbolt cable**, not Wi-Fi: M3 = 192.168.10.1 (bridge0), Intel = 192.168.10.2 (`Macs-MacBook-Pro.local`). `ssh -i ~/.ssh/intel_mac_ed25519 -o IdentitiesOnly=yes robertrhu_node2@192.168.10.2`. The account short name is `robertrhu_node2` (full name "Mac Intel Node"); a wrong short name looks exactly like a wrong password (endless prompt). The key is Intel-only (operator option A, 2026-10-11). The M3's ~/.ssh/config uses ControlPath ~/.ssh/sockets (created 2026-10-11).
- **No developer tools on a fresh Mac:** `python3`, `git`, `lipo` etc. are stubs that pop Apple's install dialog on the Intel screen. MAESTRO tripped it with `lipo`. Use `/usr/bin/file` for architecture, and check `xcode-select -p` before calling any dev tool.
- **Deskflow 1.27** (keyboard/mouse sharing, replaces Universal Control because the Intel Mac has no Apple ID): the computer list lives in `~/Library/Deskflow/Deskflow.conf` as `[computer_<name>]` sections; a `section: screens` in the external layout file is ignored, and links to an unlisted name fail with "unknown computer name". coreMode 1 = client, 2 = server. Settings keys: upstream `src/lib/common/Settings.h`. The DMG carries a license agreement (`yes Y | hdiutil attach …`). The core needs Accessibility, and only the operator can grant it.

**Why:** each of these cost a round-trip with the operator on 2026-10-11.
**How to apply:** use these facts before touching the Intel Mac. Related: [[cross-process-contracts-one-enforcer]], [[context-management-every-session]].
