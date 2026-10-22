#!/bin/bash
# backup_mirror.sh — copy the LLM-as-Database working volume to a SEPARATE physical disk.
#
# Why this exists (2026-10-03): the RunPod working tier was lost and the SSD mirror had
# not been synced for 12 days. This is the automated replacement for that manual sync.
# Source = the external "memit" volume (working tier). Destination = the Mac's internal
# SSD (durable tier). The partitions "Development" and "backups" share memit's physical
# disk and are NOT valid destinations.
#
# Run by launchd (code/ops/backup/launchd/com.rhu.memit-backup.plist) or by hand:
#     bash code/ops/backup/backup_mirror.sh
#
# [LAW:no-silent-failure] every failure exits non-zero with a message; nothing is
# redirected to /dev/null. [LAW:effects-at-boundaries] this wrapper owns backup I/O.
set -euo pipefail

PAIRS="${BACKUP_PAIRS:-$(/usr/bin/dirname "$0")/backup_pairs.tsv}"
RSYNC="${BACKUP_RSYNC:-/opt/homebrew/bin/rsync}"
MOUNT="${BACKUP_MOUNT:-/sbin/mount}"
MOUNT_POINT="${BACKUP_MOUNT_POINT:-/Volumes/memit}"
STAMP=$(/bin/date +%Y%m%dT%H%M%S)

die() { echo "backup_mirror: FATAL: $*" >&2; exit 1; }

[ -f "$PAIRS" ] || die "pairs table missing: $PAIRS"
SOURCES=(); DESTINATIONS=(); RULES=(); ROWS=()
ROW=0
# [LAW:parse-dont-validate] retain checked rows so no copy precedes a later refusal.
while IFS= read -r LINE || [ -n "$LINE" ]; do
  ROW=$((ROW + 1))
  if [ "$ROW" = 1 ]; then
    [ "$LINE" = $'reader\tsource\tdestination\texcludes' ] || die "row $ROW: invalid header: $PAIRS"
    continue
  fi
  IFS=$'\t' read -r READER SRC DEST EXCLUDES EXTRA <<< "$LINE"
  [ "$LINE" = "$READER"$'\t'"$SRC"$'\t'"$DEST"$'\t'"$EXCLUDES" ] &&
    [ -n "$SRC" ] && [ -n "$DEST" ] && [ -n "$EXCLUDES" ] || die "row $ROW: invalid pair: $PAIRS"
  case "$READER" in ssd) ;; intel|gdrive) continue ;; *) die "row $ROW: unknown reader: $READER" ;; esac
  case "$EXCLUDES" in
    -) ;;
    */*) die "row $ROW: excludes must be next to table: $EXCLUDES" ;;
    *) EXCLUDES="$(/usr/bin/dirname "$PAIRS")/$EXCLUDES" ;;
  esac
  # [LAW:one-source-of-truth] explicit tables own pairs; legacy overrides apply to the default table.
  if [ -z "${BACKUP_PAIRS:-}" ]; then
    SRC="${BACKUP_SRC:-$SRC}"
    DEST="${BACKUP_DEST:-$DEST}"
    EXCLUDES="${BACKUP_EXCLUDES:-$EXCLUDES}"
  fi
  [ -x "$RSYNC" ] || die "row $ROW: rsync not found at $RSYNC"
  [ "$EXCLUDES" = - ] || [ -f "$EXCLUDES" ] || die "row $ROW: exclude list missing: $EXCLUDES"
  MOUNTS=$("$MOUNT") || die "row $ROW: cannot inspect mounts: $MOUNT"
  case "$MOUNTS" in *" on $MOUNT_POINT ("*) ;; *) die "row $ROW: source volume $MOUNT_POINT is not mounted" ;; esac
  [ -d "$SRC" ] || die "row $ROW: source dir missing: $SRC"
  CONTENTS=$(/bin/ls -A "$SRC") || die "row $ROW: cannot read source directory: $SRC"
  [ -n "$CONTENTS" ] || die "row $ROW: source dir is empty: $SRC (refusing to mirror emptiness)"
  case "$DEST" in /Volumes/memit|/Volumes/memit/*|/Volumes/Development|/Volumes/Development/*|/Volumes/backups|/Volumes/backups/*) die "row $ROW: DEST is on the same physical disk as SRC: $DEST";; esac
  SOURCES+=("$SRC"); DESTINATIONS+=("$DEST"); RULES+=("$EXCLUDES"); ROWS+=("$ROW")
done < "$PAIRS"
[ "$ROW" -gt 0 ] || die "empty pairs table: $PAIRS"

for ((I=0; I<${#SOURCES[@]}; I++)); do
  SRC="${SOURCES[I]}"; DEST="${DESTINATIONS[I]}"; EXCLUDES="${RULES[I]}"
  DELETED_DIR="$DEST/.deleted/$STAMP"
  /bin/mkdir -p "$DEST/.deleted"
  EXCLUDE_ARGS=()
  if [ "$EXCLUDES" != - ]; then EXCLUDE_ARGS=("--exclude-from=$EXCLUDES"); fi
  echo "backup_mirror: $STAMP start  $SRC -> $DEST"
  "$RSYNC" -a --delete --backup --backup-dir="$DELETED_DIR" \
    ${EXCLUDE_ARGS[@]+"${EXCLUDE_ARGS[@]}"} --stats --human-readable \
    "$SRC/" "$DEST/" \
    | /usr/bin/grep -E '^(Number of (files|created files|deleted files|regular files transferred)|Total transferred file size|Total file size)' \
    || die "row ${ROWS[I]}: rsync failed (see launchd log)"

  # Empty archive folders carry no displaced files; preserve today's cleanup.
  /usr/bin/find "$DEST/.deleted" -mindepth 1 -maxdepth 1 -type d -empty -delete
  echo "$STAMP" > "$DEST/.last_success"
  echo "backup_mirror: $STAMP OK"
done
