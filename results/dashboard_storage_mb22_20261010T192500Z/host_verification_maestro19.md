# MAESTRO19 host verification — 2026-10-10T19:47Z

- `/usr/bin/python3 -B -m unittest tools.test_dashboard_storage`: Ran 26 tests, OK.
- File SHA-256s match the build report table (dashboard_storage.py e935e077…, dashboard_storage_tab.sh e847944c…, team_dashboard.sh 3db71c23…, test_dashboard_storage.py c91d875e…).
- Launch command matches the existing GPU-gate exemption regex (launch_exemption.json); no admission rule edited.
- Tab added to the running `dashboard` session with the recorded add-tab command (one window add, no rebuild): exit 0, window 7 `storage`.
- No host size cache existed before. The tab's first real scan wrote ~/Library/Caches/memit-dashboard/storage_sizes.json with entries and no error (duration ~1.0 s). The sandbox-only `nice: setpriority` failure does not occur on the host.
- `--once` was deliberately not run first: its scan runs on a daemon thread that dies when --once exits, which would record an attempt with no result and throttle the live tab's first scan for 15 minutes. Diagnostic-only edge; the live tab is unaffected.

Live tab capture (pane narrower than 160 columns):

```text
■ STORAGE · Drive backup and project disks
GOOGLE DRIVE BACKUP
Backup not switched on yet · waiting for activa
Health: missing or malformed launch receipt gen
PAST RUNS · newest first
 No recorded runs
DISKS · space measured now
Internal SSD: 730.2 GiB used (78.8%) · 196.2 Gi
memit SSD: 338.8 GiB used (80.8%) · 80.3 GiB fr
Development and backups share memit's physical
Project folders · measured 0 min ago · every 15
MAIN CHECKOUT · /Volumes/memit/llm-database-poc
 46.2 GiB  .claude/worktrees
 5.8 GiB  c10l_mint_edited_qwen3b_N
 5.8 GiB  b3_edited_qwen3b
 5.8 GiB  b3_edited_f16.gguf
 5.8 GiB  c10l_mint_N_f16.gguf
 1.8 GiB  b3_edited_q4km.gguf
 1.8 GiB  c10l_mint_N_q4km.gguf
 1.3 GiB  .git
 1.0 GiB  .venv
 268.0 MiB  llama_cpp_src
 106.7 MiB  external_prior_art
 14.8 MiB  graft
 3.8 MiB  results
MIRROR · checkout expanded above · /Volumes/mem
 52.8 GiB  workspace
 45.9 GiB  stage_2_sweep
 42.7 GiB  stage_1_sect
 36.5 GiB  hf_cache
 32.8 GiB  stage_1_sect_S215D2
 19.6 GiB  covariance_caches
INTERNAL PROJECT FILES · under $HOME · top 3/3
 268.5 GiB  ~/Backups
 3.6 GiB  ~/.claude/jobs
 4.0 KiB  ~/Library/Logs/memit-gdrive-backup
```
