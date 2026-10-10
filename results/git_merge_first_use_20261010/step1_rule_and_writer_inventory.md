# First gated merge — step 1: rule adopted + writer inventory (MAESTRO9, 2026-10-10)

Rule: Astra r4 cooperative paragraph adopted verbatim into `CLAUDE.md` (§ Merging, item 4 changed from "never merge" to gate-only) and `AGENTS.md` (Team mode bullet; Codex mechanisms line changed from "nobody merges").

Local writer inventory for this repo (host checks, ~10:40Z):
- crontab: none ("no crontab for robertrhu").
- ~/Library/LaunchAgents: `com.rhu.extract`, `com.rhu.graphify.refresh`, `com.rhu.pipeline` run `~/Projects/winning-defense/scripts/refresh_*.sh` (another repo; no reference to llm-database/arhugula). `org.thestoryportal.harness-dashboard-sync` fetches and fast-forwards `thestoryportal/arhugula-harness` on `main` only (another repo). `com.rhu.memit-backup` runs `open -W -g ~/Applications/MemitBackup.app` (rsync backup, no git). `com.rhu.pixeltable.*`, `tailscaled-user`, `powerline-config`, Google/Citrix agents: no git.
- Codex builders codexmb12 / codexmb14 (and successors): briefs forbid commits and pushes; AGENTS.md now forbids push/merge/PR mutation.
- MAESTRO (this session): the sole local committer/pusher/merger.
GitHub-side sources (Actions triggers, bots, auto-merge, external CI): inventoried at step 4.
