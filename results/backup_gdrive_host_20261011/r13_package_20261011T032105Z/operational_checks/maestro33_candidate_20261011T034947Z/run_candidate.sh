#!/bin/sh
# MAESTRO33: plan v4 rows 1.1-candidate + 1.1-verify-staged, with Astra r13 condition (1) identity capture. Stops on the first failure.
set -u
W="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a"; O="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261011/r13_package_20261011T032105Z/operational_checks/maestro33_candidate_20261011T034947Z"; C="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/backup-gdrive-r13-cand-20261011T034947Z"
SRC=bdc1ad167afeedb94ccd60137b591eb78044c899
cd "$W"
log(){ echo "$* at $(date -u +%FT%TZ)" >> "$O/rcs.txt"; }
log "niceness=$(/usr/bin/python3 -c 'import os;print(os.getpriority(os.PRIO_PROCESS,0))') start"
/usr/bin/git fetch origin master > "$O/fetch.out" 2>&1; rc=$?; log "fetch rc=$rc"; [ $rc -eq 0 ] || { log STOP; exit 1; }
BASE=$(/usr/bin/git rev-parse origin/master); echo "$BASE" | grep -Eqx '[0-9a-f]{40}' || { log "STOP bad base"; exit 1; }
[ "$(/usr/bin/git cat-file -t $SRC)" = commit ] || { log "STOP bad source"; exit 1; }
printf 'base_origin_master=%s\nsource_commit=%s\ncandidate_path=%s\n' "$BASE" "$SRC" "$C" > "$O/identity.txt"; log "identity captured"
export MAESTRO_SOURCE_COMMIT=$SRC MAESTRO_CANDIDATE_PATH="$C" LLMDB_ROOT="$W"
for s in candidate verify-staged; do
  /bin/sh "$W/results/backup_gdrive_host_20261011/r13_package_20261011T032105Z/host_commands_r13.sh" $s > "$O/$s.out" 2>&1; rc=$?; log "$s rc=$rc"
  [ $rc -eq 0 ] || { log STOP; exit 1; }
done
AFTER=$(/usr/bin/git rev-parse origin/master); [ "$AFTER" = "$BASE" ] && log "base unchanged" || { log "STOP base moved to $AFTER"; exit 1; }
log ALLDONE
