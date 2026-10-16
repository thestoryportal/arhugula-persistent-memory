---
name: gdrive-rclone-remote
description: rclone `gdrive:` (drive.file, published app) is the archive tier; setup + OAuth traps (Internal audience, Testing expiry, reconnect after publish)
metadata:
  type: reference
---

rclone remote `gdrive:` (type drive, scope drive.file) → the operator's Google Drive (5 TiB, ~4.9 TiB free on 2026-10-10). Backup root `gdrive:memit-backup/`. OAuth client lives in the Google Cloud project with **project number 543404640214**; its branding app name is "n8n Workflow Engine", which is why the consent screen shows that name. The audience is External and **In production** (published 2026-10-10). The token was re-issued after publishing, so it has no 7-day Testing expiry.

Traps, in the order they hit:
- `org_internal` 403 → project audience was Internal; fix = Audience → Make external.
- `access_denied … being tested` → add Gmail as Test user, or publish.
- Publish greyed out → Branding page needs support + developer emails; App-domain links optional (operator used thestoryportal.org).
- A token issued while in Testing keeps its 7-day expiry → run `rclone config reconnect gdrive:` after publishing.
- Phone flow: run authorize/reconnect in tmux `rclone`, fetch the Google URL from the localhost 307 with python urllib, append `&prompt=select_account`. The phone reaching rclone's "Success" page delivered the code directly.
- The auto-mode classifier blocks writing the authorize blob to a file. Keep it in tmux/process memory and get explicit operator authorization in chat. After use, run `tmux clear-history` on the rclone panes.

Related: `program/runbook/03-operational-hygiene-runpod-gpu-memory-disk.md:28` (§3.3a), [[backup-via-memitbackup-app]].
