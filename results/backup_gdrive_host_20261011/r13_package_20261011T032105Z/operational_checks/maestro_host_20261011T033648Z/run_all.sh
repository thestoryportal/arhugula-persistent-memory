#!/bin/sh
# MAESTRO32 host run of MB45's r13 commands, one invocation each, in order; every exit code recorded, later ones run regardless.
cd "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a"
echo "niceness=$(/usr/bin/python3 -c 'import os;print(os.getpriority(os.PRIO_PROCESS,0))') start=$(date -u +%FT%TZ)" > "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261011/r13_package_20261011T032105Z/operational_checks/maestro_host_20261011T033648Z/rcs.txt"
for s in pins check package fixture freeze pins-final; do
  LLMDB_ROOT="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a" /bin/sh "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261011/r13_package_20261011T032105Z/host_commands_r13.sh" $s > "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261011/r13_package_20261011T032105Z/operational_checks/maestro_host_20261011T033648Z/$s.out" 2>&1
  echo "$s rc=$? at $(date -u +%T)" >> "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261011/r13_package_20261011T032105Z/operational_checks/maestro_host_20261011T033648Z/rcs.txt"
done
echo "ALLDONE $(date -u +%FT%TZ)" >> "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261011/r13_package_20261011T032105Z/operational_checks/maestro_host_20261011T033648Z/rcs.txt"
