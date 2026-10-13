#!/bin/bash
# backup_mirror.sh — copy the LLM-as-Database working volume to a SEPARATE physical disk.
#
# Why this exists (2026-10-03): the RunPod working tier was lost and the SSD mirror had
# not been synced for 12 days. This is the automated replacement for that manual sync.
# Source = the external "memit" volume (working tier). Destination = the Mac's internal
# SSD (durable tier). The partitions "Development" and "backups" share memit's physical
# disk and are NOT valid destinations.
#
# Run by launchd (tools/launchd/com.rhu.memit-backup.plist) or by hand:
#     bash tools/backup_mirror.sh
#
# [LAW:no-silent-failure] every failure exits non-zero with a message; nothing is
# redirected to /dev/null. [LAW:effects-at-boundaries] the only effect is one rsync.
set -euo pipefail

SRC="${BACKUP_SRC:-/Volumes/memit/llm-database-poc-mirror}"
DEST="${BACKUP_DEST:-/Users/robertrhu/Backups/memit/llm-database-poc-mirror}"
EXCLUDES="${BACKUP_EXCLUDES:-$(/usr/bin/dirname "$0")/backup_mirror.excludes}"
RSYNC=/opt/homebrew/bin/rsync
STAMP=$(/bin/date +%Y%m%dT%H%M%S)
DELETED_DIR="$DEST/.deleted/$STAMP"      # files removed at source are kept here, not destroyed

die() { echo "backup_mirror: FATAL: $*" >&2; exit 1; }

# [LAW:parse-dont-validate] preconditions checked ONCE, at the boundary, before any effect.
# A missing/unmounted source with --delete would wipe the backup, so this gate is load-bearing.
[ -x "$RSYNC" ]            || die "rsync not found at $RSYNC"
[ -f "$EXCLUDES" ]         || die "exclude list missing: $EXCLUDES"
/sbin/mount | /usr/bin/grep -q " on /Volumes/memit " || die "source volume /Volumes/memit is not mounted"
[ -d "$SRC" ]              || die "source dir missing: $SRC"
[ -n "$(/bin/ls -A "$SRC")" ] || die "source dir is empty: $SRC (refusing to mirror emptiness)"
case "$DEST" in /Volumes/memit/*|/Volumes/Development/*|/Volumes/backups/*) die "DEST is on the same physical disk as SRC: $DEST";; esac
/bin/mkdir -p "$DEST/.deleted"      # [LAW:dataflow-not-control-flow] always exists, so the cleanup below never branches

echo "backup_mirror: $STAMP start  $SRC -> $DEST"
"$RSYNC" -a --delete --backup --backup-dir="$DELETED_DIR" \
  --exclude-from="$EXCLUDES" --stats --human-readable \
  "$SRC/" "$DEST/" \
  | /usr/bin/grep -E '^(Number of (files|created files|deleted files|regular files transferred)|Total transferred file size|Total file size)' \
  || die "rsync failed (see launchd log)"

# Empty .deleted/<stamp> dirs (nothing was deleted this run) are removed so the tree stays readable.
/usr/bin/find "$DEST/.deleted" -mindepth 1 -maxdepth 1 -type d -empty -delete
echo "$STAMP" > "$DEST/.last_success"
echo "backup_mirror: $STAMP OK"
