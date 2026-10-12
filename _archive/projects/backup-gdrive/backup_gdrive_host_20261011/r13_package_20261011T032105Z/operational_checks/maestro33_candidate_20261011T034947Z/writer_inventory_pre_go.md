# PR #22 competing-writer inventory (pre-GO, read-only), 2026-10-11T03:56:15Z

Astra r13 condition (2) needs an actual suspension/drain and reservation at merge time. This is the inventory taken before asking for the GO; it is re-checked inside the window.

- Candidate: PR #22, head e76db678a8cf0f2d4703886fa0b5e1e910e9e00e = r13_verified_commit_sha.txt = remote refs/heads/backup-gdrive-r12; base master a424085f.
- CI: one workflow (.github/workflows/ci.yml, "CI", active; triggers: push to master, pull_request to master). Candidate-head run 38109847966 completed/success on e76db678; no other runs on that head.
- Bots: no dependabot/renovate config. PR #22 autoMergeRequest null, not draft; no merge queue in use.
- launchd: com.rhu.memit-backup (every 21600 s, opens MemitBackup.app -> ~/Backups/memit/bin/backup_mirror.sh; zero git/gh commands). Not a git writer.
- cron: none.
- Local sessions: codexmb44/codexmb45 idle (builders never push); BRAIN1 (codexbrain) writes only its results folder, no commits. MAESTRO33 is the only pusher.
- Dry runs: hygiene-dry PASS (no deletions); gate-dry DRY_RUN_PASS (commands/gate-dry).
