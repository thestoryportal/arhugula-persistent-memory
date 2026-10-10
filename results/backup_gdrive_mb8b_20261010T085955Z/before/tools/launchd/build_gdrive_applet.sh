#!/bin/bash
set -euo pipefail
if [ "$#" != 1 ]; then
  echo "Usage: $0 <output.app>" >&2
  exit 64
fi
OUTPUT="$1"
case "$OUTPUT" in
  *.app) ;;
  *) echo "Output must end in .app" >&2; exit 64 ;;
esac
if [ -e "$OUTPUT" ]; then
  echo "Refusing to overwrite existing app bundle: $OUTPUT" >&2
  exit 1
fi
SOURCE="$(/usr/bin/dirname "$0")/MemitGdriveBackup.applescript"
/usr/bin/osacompile -o "$OUTPUT" "$SOURCE"
/usr/bin/find "$OUTPUT" -type f -exec /usr/bin/shasum -a 256 {} \; | LC_ALL=C /usr/bin/sort -k 2
