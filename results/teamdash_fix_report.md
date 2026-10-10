# Teamdash Science Report: fix report (2026-10-10)

Scope: the operator asked to fix the Science Report's formatting and to give it a tab of its own. Code was built and tested only. The live tmux server was read (list-panes, capture-pane) but not changed. Nothing is committed.

## Root causes (line numbers refer to HEAD `f69a9a5`)

1. **Dead pane: a TOCTOU race.** `tools/dashboard_subagents.py:137-140` (`recent_agents`) globbed every project's subagent transcripts and then called `os.path.getmtime(p)` (:138). A transcript from another project (`winning-defense…/agent-a2130a2e….jsonl`) was deleted between the glob and the stat, so `FileNotFoundError` reached the report through `dashboard_report.render` → `dashboard_live.gather` (:561) → `dashboard_tile.running_helpers` (:25). The sort at :140 (`key=os.path.getmtime`) stat'ed every file a second time, which opened a second race window.
2. **No guard in the viewer loop.** `tools/dashboard_report.py:96-103` called `render()` with nothing around it, so one exception killed the pane for good (the pane had `remain-on-exit`).
3. **Wrapped lines and fragments.**
   - **What the evidence shows.** Every wrapped line in `team_window_scrollback.txt` is 108 characters wide, and none of them is wider in cells. A frame drawn for a pane of 110 or more columns was re-wrapped by tmux when the pane shrank to 107. I reproduced this on an isolated tmux 3.7c server (`-S` socket; the live server was not involved). tmux re-wraps old content when a pane is resized and pushes the overflow into history. The redraw (`\033[H` … `\033[J`) only repaints the visible screen, so the fragments stay in history. Before the fix, the same resize sequence left 54, 198, 60 and 103 history lines at widths 107, 40, 113 and 72.
   - **Glyph widths.** I measured them in tmux: ━ ■ · — ┃ █ ░ … ⚠ ▸ » ◦ ▲ ● ✔ each take one cell. The ambiguous-width glyphs are not the cause. Wide characters such as ✅ do take two cells, and `dashboard_live.clip` (:589-598) counted characters, not cells.
   - **Layout code.** `render()` produced lines of up to `cols` cells: the section rule at :24 was exactly `cols`, the queue and results rows were exactly `cols`, and the header and brief were `cols-1`. Only the `clip(cols - 2)` at :100 kept them inside the pane.
   - **The cut pointer.** The brief's "more" pointer at :68 was `cols + 4` wide, so it was always cut. The evidence shows "(more: docs/c1".
4. **Stale lead name.** `tools/team_dashboard.sh:11` hard-codes `LEAD=program`, and :16 (label) and :41 (abort if missing) use it. `tools/dashboard_live.py:559` (`gather`) also hard-codes `"program"` to keep the lead out of NOW alerts.

## Diff summary

- **`tools/dashboard_subagents.py`.** `recent_agents` stats each file once and catches only `FileNotFoundError` on that stat, so a vanished transcript is skipped. Any other error still raises. The sort reuses the stored mtime, which removes the second race.
- **`tools/dashboard_live.py`:**
  - `cell_width`, `cells` and a cell-aware `clip`: W/F characters take 2 cells, combining marks take 0, everything else takes 1. ANSI codes are still kept after the cut.
  - Lead detection: `Pane`, `PANE_FORMAT`, `parse_panes`, the pure `lead_session(override, panes, repo)`, and the effectful `repo_root()` (cached `git rev-parse --git-common-dir`) and `read_lead()`. A failed tmux or git read raises.
  - `team_screens()` now also returns the lead, inside the existing 15 s cache: one extra `tmux list-panes -a` per 15 s per report process. `gather()` excludes that lead instead of `"program"`.
  - New CLI: `python3 tools/dashboard_live.py --lead`.
- **`tools/dashboard_report.py`:**
  - `render(cols, rows)` lays out to `w = cols - 1`, so the last column always stays empty.
  - `fit` is cell-aware. `col` fits and pads a table column. `wrap` replaces `textwrap` for the brief and wraps by cells.
  - The brief pointer is sized so it is never cut.
  - The single width enforcer is the final `clip(line, w)`.
  - `screen()` catches a render failure and returns one red line, `✖ <Type>: <message> · the Science Report retries every 5 s`, cut to the pane.
  - `main()` keeps the 5 s sleep. When the pane size differs from the last drawn frame, it writes `\033[2J\033[3J`, which clears the screen and the history.
  - The docstring now says 5 s (it said 2 s).
- **`tools/team_dashboard.sh`:**
  - `LEAD=$(python3 dashboard_live.py --lead)`, and the build aborts loudly if detection itself fails.
  - The label case is now `"$LEAD")`, giving "LEAD · <name> session".
  - When no lead is found, the lead pane shows: "LEAD · no lead session found: no tmux session has a Claude Code pane working in this repo. Start one, or set LEAD=<session>, and re-run tools/team_dashboard.sh." The rest of the dashboard still builds.
  - `-e LEAD=$LEAD` on the session, so the report panes exclude the same lead.
  - The build calls `dashboard_science_tab.sh "$NEW"`.
  - The team window layout is unchanged.
- **`tools/dashboard_science_tab.sh` (new).** Adds one window named `science` running `dashboard_report.py` to a session (default `dashboard`, targeted as `=dashboard`). It does nothing if the window already exists and exits 1 with a message if the session is missing. It is the only place the tab is defined.
- **`tools/test_dashboard_report.py` (new, 16 tests).**

**Lead detection rule:** if `LEAD` is set, use it. Otherwise, take the panes from `tmux list-panes -a` and keep those where all three of these hold:

- The session is a team session (not `dashboard`, `dashboard_new`, `helpers` or `view-*`).
- The pane runs Claude Code: `pane_current_command` is `claude` or a version string like `2.1.295` (the name Claude Code gives its own process), or `pane_start_command` begins with `claude`.
- `pane_current_path` is inside the main checkout from `git rev-parse --git-common-dir`, so this repo's worktrees count too.

The newest such session (by `session_created`) is the lead. If none qualifies, the result is "none". On the live server today it resolves to `maestro2`.

## RED / GREEN (`/usr/bin/python3 -B`, system Python 3.9.6)

**RED.** These are the new tests against the original code, run in a scratch copy of `tools/`: `Ran 16 tests … FAILED (failures=28, errors=7)`. That count includes subtests.

- Errors:
  - `test_vanished_file_is_skipped`: FileNotFoundError.
  - The 2 loop tests: the render exception escaped `main`.
  - The 4 `Lead` tests: `lead_session` did not exist.
- Failures:
  - `test_wide_characters_take_two_cells`.
  - `test_full_clear_only_when_the_size_changes`.
  - `test_cli_…`: `--lead` printed nothing.
  - Width tests at every width. The first offending lines were the Goal line at 96 cells in a 40-col pane, and the ⚠ banner and section rules at exactly `cols`.
- Three tests passed already: `test_unreadable_file_still_raises`, `test_box_glyphs_…` and `test_cut_brief_…`. The old `render()` did not clip the pointer itself; `main` did.
- After the RED run, three test adjustments were made: frames are split on their `\033[J` end, the failure test uses a 120-col pane so a short path fits, and an empty `--lead` result is expected as one empty line.

**GREEN.** Run in the worktree after install:

```
tools.test_dashboard_report     Ran 16 tests  OK
tools.test_dashboard_live       Ran 27 tests  OK   (unchanged suite, still green)
tools.test_dashboard_mathlab    Ran 58 tests  OK   (another session's WIP file, run read-only; it uses clip)
tools.test_dashboard_gpu_detector Ran 40 tests OK
```

The width test renders `render(cols, rows)` at 40, 72, 107, 113 and 221 columns. It uses the live `docs/c10_scoreboard.json` and a stress board with ✅, long names and 40 results. It strips ANSI, measures cells independently, and asserts every line is `< cols` cells.

**End to end.** I ran an isolated tmux server through a PATH shim that pins every `tmux` call to `-S /private/tmp/claude-501/tdtest.sock`. The checks:

- `team_dashboard.sh` built the dashboard with lead `maestro9` (a fake `claude` pane in the repo).
- The `science` tab was created full width. Re-running `dashboard_science_tab.sh` reported "already has a science tab; nothing to do". After the window was killed, the script re-added it.
- A missing session gave exit 1.
- `LEAD=codexq` produced the tile "LEAD · codexq session".
- With no lead, the lead pane showed the message.
- Resizing the science tab to 107, 40, 221, 113 and 72 left 0 history lines, and the widest line was always `cols - 1`.

The test server was killed afterwards.

## Live steps for MAESTRO3

Run these from any shell. In zsh, quote `=dashboard`.

```bash
WT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
# 1. Revive the dead Science Report pane in the team tab (pane %149 = dashboard:1.2; same command, now with the fixes).
tmux respawn-pane -t %149
# 2. Add the science tab to the running dashboard (one new window; nothing else moved or resized; no-op if present).
bash "$WT/tools/dashboard_science_tab.sh"
# 3. Check.
tmux list-windows -t '=dashboard' -F '#{window_index} #{window_name}'    # expect a 'science' window
/usr/bin/python3 "$WT/tools/dashboard_live.py" --lead                    # expect: maestro2
#    open it: teamdash science   (or Ctrl-b <its index>)
# 4. Optional, LEAD tile without a full rebuild: the running team tab still tiles 'program' (pane %145) and stale
#    codexmb2/codexy3/codexz3. Respawning only the lead tile moves nothing:
tmux respawn-pane -k -t %145 "/usr/bin/python3 '$WT/tools/dashboard_tile.py' 'maestro2' 'LEAD · maestro2 session' '25'"
#    A full rebuild (bash "$WT/tools/team_dashboard.sh") also picks up the current codex sessions, but it recreates every
#    pane. Per memory_mirror/tmux-server-hang-dashboard.md, do it only with one viewer size attached and no pane in copy mode.
```

## Notes and residual risks

- **Hot reload.** Viewer panes re-exec when a `tools/dashboard_*.py` mtime changes. Installing these files therefore restarted the live tiles and the active, experiment, mathlab and helpers panes on the new code. I checked afterwards: all were alive. Only the already-dead `%149` remains dead.
- **Extra load from the science tab.** The tab is a second `dashboard_report.py` process at the same 5 s cadence, with its own 15 s-cached tmux reads (about 8 calls per 15 s). There is no new loop and no faster refresh.
- **Resize lag.** A resize is cleaned on the next redraw, up to 5 s later. macOS has no `sigtimedwait`, so an immediate redraw on SIGWINCH would need more machinery, and I did not add it.
- **Remaining `"program"` hard-codes (not changed; outside this brief):**
  - `tools/dashboard_active.py:18,37,39,63`
  - `tools/dashboard_watch.py:15`
  - `tools/dashboard_subagents.py:48-49`: a parent labelled "LEAD (program)" by prompt text.

  They could use `dashboard_live.read_lead()`.
- **Remaining race in `info()`.** `dashboard_subagents.info(p)` opens the transcript after the stat, so a file vanishing in that narrower window still raises. In the report it now shows as the red line and recovers on the next redraw. The team tiles (`dashboard_tile.py:104`) and the helpers manager have no such guard.
- **Pre-existing warning.** `json.load(open(BOARD))` in `render()` leaves the file to the GC and prints a ResourceWarning under `unittest -v`. It is pre-existing and was left as is.
