#!/bin/bash
# One sync of the mounted working volume; replaced/deleted objects are archived.
# Stale locks are never expired by age: the first upload can take many hours.
set -euo pipefail

SRC="${BACKUP_SRC:-/Volumes/memit/llm-database-poc-mirror}"
DEST="${BACKUP_DEST:-gdrive:memit-backup/llm-database-poc-mirror}"
DEST="${DEST%/}"
EXCLUDES="${BACKUP_EXCLUDES:-$(/usr/bin/dirname "$0")/backup_mirror.excludes}"
RCLONE="${BACKUP_RCLONE:-/opt/homebrew/bin/rclone}"
PYTHON="${BACKUP_PYTHON:-/usr/bin/python3}"
STATUS_TOOL="$(/usr/bin/dirname "$0")/backup_gdrive_status.py"
MOUNT_POINT="${BACKUP_MOUNT_POINT:-/Volumes/memit}"
LOG="${BACKUP_LOG:-$HOME/Library/Logs/memit-gdrive-backup.log}"
LOCK="${BACKUP_LOCK_DIR:-$HOME/Library/Logs/memit-gdrive-backup.lock}"
STAMP="$(/bin/date -u +%Y%m%dT%H%M%SZ)-$$"
DELETED_DIR="${DEST%/*}/.deleted/$STAMP"
HEARTBEAT="${BACKUP_HEARTBEAT:-$HOME/Library/Logs/memit-gdrive-backup/last_run.json}"
START="$(/bin/date -u +%Y-%m-%dT%H:%M:%SZ)"
LAUNCH_GENERATION="${BACKUP_LAUNCH_GENERATION:-}"
RUN_LOG="$(/usr/bin/dirname "$HEARTBEAT")/runs/$STAMP.jsonl"
RCLONE_VERSION=""
RCLONE_PID=0
LOCK_OWNED=0
SYNC_ACTIVE=0
SYNC_STARTED=0
RCLONE_EXIT_CODE=0
SYNC_OUTCOME=""
CHILD_PUBLICATION_FAILED=0

log() {
  local message="backup_gdrive: $STAMP $*"
  if ! printf '%s\n' "$message" >> "$LOG"; then
    echo "backup_gdrive: FATAL: cannot write log $LOG" >&2
    return 1
  fi
  printf '%s\n' "$message" >&2
}
die() { log "FATAL: $*"; exit 1; }
write_heartbeat() {
  local target="$HEARTBEAT"
  [ "$LOCK_OWNED" = 1 ] || target="$(/usr/bin/dirname "$HEARTBEAT")/refusals/latest-refusal.json"
  "$PYTHON" "$STATUS_TOOL" record --heartbeat "$target" --phase "$1" \
    --run-id "$STAMP" --start "$START" --exit-code "${2:-0}" --launch-generation "$LAUNCH_GENERATION" \
    --rclone-version "$RCLONE_VERSION" --log "$LOG" --run-log "$RUN_LOG" \
    --sync-started "$SYNC_STARTED" --rclone-exit-code "$RCLONE_EXIT_CODE" \
    --outcome-json "$SYNC_OUTCOME" --owner-pid "$$" --rclone-pid "$RCLONE_PID"
}
finish() {
  local status=$?
  trap - EXIT
  # Publish while still holding ownership: an older success must not mask a new run.
  if [ "$LOCK_OWNED" = 1 ]; then
    if ! write_heartbeat end "$status"; then
      log "HEARTBEAT-FAILED: terminal publication failed; last-run health must refuse"
      [ "$status" != 0 ] || status=1
    fi
    if [ "$SYNC_ACTIVE" = 1 ]; then
      log "Lock retained after interruption: a sync child may still be running; inspect $LOCK/rclone.pid before stale-lock recovery."
    elif ! /bin/rm -f "$LOCK/owner" "$LOCK/rclone.pid" || ! /bin/rmdir "$LOCK"; then
      log "FATAL: cannot remove owned lock $LOCK"
      [ "$status" != 0 ] || status=1
      if ! write_heartbeat end "$status"; then
        log "HEARTBEAT-FAILED: lock-cleanup failure could not be published"
      fi
    fi
  elif ! write_heartbeat end "$status"; then
    log "REFUSAL-RECORD-FAILED: cannot record non-owner refusal"
    [ "$status" != 0 ] || status=1
  fi
  exit "$status"
}
trap finish EXIT
trap 'log "Interrupted (INT); refusing to unlock an active sync"; exit 130' INT
trap 'log "Interrupted (TERM/HUP); refusing to unlock an active sync"; exit 143' TERM HUP
/bin/mkdir -p "$(/usr/bin/dirname "$LOG")" || die "cannot create log directory"
/bin/mkdir -p "$(/usr/bin/dirname "$LOCK")" || die "cannot create lock parent"
if ! /bin/mkdir "$LOCK"; then
  log "REFUSED: lock held or stale at $LOCK; no sync started. Verify owner/rclone.pid are no longer running before manually removing this lock. Never expire it by age."
  exit 75
fi
LOCK_OWNED=1
printf '%s\n' "$$ $STAMP" > "$LOCK/owner"
if ! write_heartbeat start; then
  log "HEARTBEAT-FAILED: start publication failed; no sync dispatched"
  exit 1
fi
[ -x "$RCLONE" ] || die "rclone missing: $RCLONE"
if ! "$PYTHON" "$STATUS_TOOL" preflight --rclone "$RCLONE" --source "$SRC" --destination "$DEST"; then
  die "unsafe or unverified rclone configuration; no sync dispatched"
fi
if VERSION_OUTPUT=$("$RCLONE" version); then
  RCLONE_VERSION="${VERSION_OUTPUT%%$'\n'*}"
else
  die "rclone version probe failed"
fi

[ -f "$EXCLUDES" ] || die "exclude list missing: $EXCLUDES"
MOUNTS=$(/sbin/mount) || die "cannot inspect mounted volumes"
case "$MOUNTS" in
  *" on $MOUNT_POINT ("*) ;;
  *) die "source volume $MOUNT_POINT is not mounted" ;;
esac
[ -d "$SRC" ] || die "source dir missing: $SRC"
CONTENTS=$(/bin/ls -A "$SRC") || die "cannot read source directory: $SRC"
[ -n "$CONTENTS" ] || die "source dir is empty: $SRC (refusing to sync emptiness)"
case "$DEST" in
  /Volumes/memit/*|/Volumes/Development/*|/Volumes/backups/*)
    die "DEST is on the source physical disk: $DEST" ;;
esac
case "$DEST" in
  */?*) ;;
  *) die "DEST must name a directory below its backup parent: $DEST" ;;
esac
log "start $SRC/ -> $DEST/; archive=$DELETED_DIR/; rclone-log=$RUN_LOG"
/bin/mkdir -p "$(/usr/bin/dirname "$RUN_LOG")" || die "cannot create per-run log directory"
: > "$RUN_LOG"

# --links preserves rsync -a's symlink intent without traversing symlink targets.
# Explicit false flags preserve exclusions and the IO-error deletion barrier.
SYNC_ACTIVE=1
SYNC_STARTED=1
"$RCLONE" sync "$SRC/" "$DEST/" --backup-dir "$DELETED_DIR/" \
  --exclude-from "$EXCLUDES" --links --log-file "$RUN_LOG" --log-level INFO --use-json-log \
  --exclude '**/.git/objects/**/tmp_obj_*' --exclude '**/.git/objects/tmp_obj_*' \
  --exclude '/.git/objects/**/tmp_obj_*' --exclude '/.git/objects/tmp_obj_*' \
  --retries 1 --low-level-retries 10 --dry-run=false --interactive=false \
  --ignore-errors=false --delete-excluded=false --delete-after \
  --bwlimit '08:00,512k 23:00,off' \
  --stats 1m --stats-log-level NOTICE &
RCLONE_PID=$!
printf '%s\n' "$RCLONE_PID" > "$LOCK/rclone.pid"
if ! write_heartbeat start; then
  log "HEARTBEAT-FAILED: child PID publication failed; sync child may still be running"
  CHILD_PUBLICATION_FAILED=1
fi
if wait "$RCLONE_PID"; then
  SYNC_ACTIVE=0
else
  RCLONE_EXIT_CODE=$?
  SYNC_ACTIVE=0
fi
if [ "$CHILD_PUBLICATION_FAILED" = 1 ]; then
  STATUS="$RCLONE_EXIT_CODE"
  [ "$STATUS" != 0 ] || STATUS=1
  exit "$STATUS"
fi
if SYNC_OUTCOME=$("$PYTHON" "$STATUS_TOOL" classify --source "$SRC" --run-log "$RUN_LOG" --rclone-exit-code "$RCLONE_EXIT_CODE"); then
  [ -n "$SYNC_OUTCOME" ] || die "classification produced no outcome; raw rclone exit $RCLONE_EXIT_CODE; see $RUN_LOG"
  case "$SYNC_OUTCOME" in
    *'"warnings": []'*) log "OK" ;;
    *)
      if [ "$RCLONE_EXIT_CODE" = 1 ]; then
        log "WARN: source vanished; destination deletions suppressed; raw rclone exit 1; $SYNC_OUTCOME; see $RUN_LOG"
      else
        log "WARN: sync completed with warnings; $SYNC_OUTCOME; see $RUN_LOG"
      fi ;;
  esac
else
  log "FATAL: rclone failed or outcome unverified (exit $RCLONE_EXIT_CODE); see $RUN_LOG"
  STATUS="$RCLONE_EXIT_CODE"
  [ "$STATUS" != 0 ] || STATUS=1
  exit "$STATUS"
fi
