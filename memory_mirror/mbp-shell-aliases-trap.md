---
name: mbp-shell-aliases-trap
description: Interactive zsh aliases du/cat/ls/grep/find (dust/bat/eza/rg/fd); in agent Bash the rtk hook rewrites output - use rtk proxy or /usr/bin paths
metadata:
  type: feedback
---

In Robert's **interactive zsh** on this Mac, `du` is aliased to dust (`~/.zshrc:392`), `ls` to eza (`:200`), `cat` to `bat --paging=never` (`:218`), `grep` to rg (`:237`) and `find` to fd (`:247`). In the agent's Bash tool these aliases are NOT active (`type du cat ls grep find` → `/usr/bin/du`, `/bin/cat`, `/bin/ls`, `/usr/bin/grep`, `/usr/bin/find`, checked 2026-10-10); there the trap is the **RTK hook**, which rewrites common commands (`git status` → `rtk git status`) and reformats their output (`~/.claude/RTK.md`). Robert's own project memory adds that rsync over direct TCP needs the `-e` flag.

**Why:** `du -sh */ | sort -h` printed dust's help text instead of sizes in an interactive shell; parsed output from rewritten or aliased commands will be wrong or empty.

**How to apply:** in agent Bash, when you parse output, use `rtk proxy <cmd>` or absolute paths (`/usr/bin/grep`, `/bin/ls`); in anything sourced from the interactive shell (tmux panes, launcher scripts), prefix with `command ` (e.g. `command du -sh`) or use absolute paths. Expect `rg`/`fd`/`dust`/`bat` to be on PATH via Homebrew.
