---
name: native-applet-removable-volumes-prompt
description: "A native .app that touches /Volumes/memit blocks silently in open() until the operator Allows a per-app Removable Volumes prompt"
metadata:
  type: project
---

2026-10-10: the Drive manual-interleave host test hung ~6 h on `Native_2.app` (a throwaway fixture applet that runs the real `code/ops/backup/backup_gdrive.sh` on /Volumes/memit). `lsof` showed the child bash never opened the script (no fd 255). The TCC log showed only a `SystemPolicyAllFiles` preflight denial; no RemovableVolumes line was logged, and `screencapture` is not permitted, so the agent could not see the prompt. Once the operator clicked Allow on the on-screen prompt, the bash opened the script on fd 255 immediately and went on to its next step (receipt: `_archive/projects/backup-gdrive/backup_gdrive_mb16_20261010T103826Z/host_runs_maestro12/native2_tree_after_allow_maestro13.txt`).

**Why:** macOS gates each new app's first access to a removable/external volume behind a one-time per-app prompt, and the blocked process gives no error; it just waits.

**How to apply:** build native-applet fixtures under /private/tmp, never on memit. When a native launch on memit hangs with no fd on its script, ask the operator whether a permission pop-up is on screen before debugging anything else. Forward requirement for activation: the production `MemitGdriveBackup` applet runs the wrapper on memit, so the operator must grant it Removable Volumes access once, and the activation ask has to say so. Related: [[gdrive-rclone-remote]].
