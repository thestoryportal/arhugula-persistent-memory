#!/bin/bash
set -euo pipefail
if [ "$#" -lt 3 ] || [ "$#" -gt 4 ]; then
  echo "Usage: $0 <git-commit> <release-id> <output.app> [release-root]" >&2
  exit 64
fi
COMMIT="$1"
RELEASE_ID="$2"
OUTPUT="$3"
case "$OUTPUT" in
  *.app) ;;
  *) echo "Output must end in .app" >&2; exit 64 ;;
esac
if [ -e "$OUTPUT" ] || [ -L "$OUTPUT" ]; then
  echo "Refusing to overwrite existing app bundle: $OUTPUT" >&2
  exit 1
fi
SCRIPT_DIR="$(cd "$(/usr/bin/dirname "$0")" && /bin/pwd -P)"
OUTPUT_DIR="$(cd "$(/usr/bin/dirname "$OUTPUT")" && /bin/pwd -P)"
OUTPUT="$OUTPUT_DIR/$(/usr/bin/basename "$OUTPUT")"
SOURCE="$OUTPUT.applescript"
DECOMPILED="$OUTPUT.decompiled.applescript"
if [ -e "$SOURCE" ] || [ -L "$SOURCE" ] || [ -e "$DECOMPILED" ] || [ -L "$DECOMPILED" ]; then
  echo "Refusing existing build source or decompilation" >&2
  exit 1
fi
STAGE_ARGS=("$COMMIT" "$RELEASE_ID" "$SOURCE")
if [ "$#" = 4 ]; then STAGE_ARGS+=("$4"); fi
# The stage path is not printed into the bundle SHA-256 inventory.
RELEASE="$(/bin/bash "$SCRIPT_DIR/stage_gdrive_release.sh" "${STAGE_ARGS[@]}")"
[ -d "$RELEASE" ] || { echo "Staging returned no release directory" >&2; exit 1; }
SCRATCH="$(/usr/bin/mktemp -d "${TMPDIR:-/private/tmp}/memit-gdrive-build.XXXXXX")"
trap '/bin/rm -rf "$SCRATCH"' EXIT
# Canonicalize compiler formatting first, then compile the app from this exact saved source.
/usr/bin/osacompile -o "$SCRATCH/rendered.scpt" "$SOURCE"
/usr/bin/osadecompile "$SCRATCH/rendered.scpt" > "$SCRATCH/canonical.applescript"
[ -s "$SCRATCH/canonical.applescript" ] || { echo "Empty canonical AppleScript" >&2; exit 1; }
/bin/cp "$SCRATCH/canonical.applescript" "$SOURCE"
# Compare decompilations of two compiles of the same saved canonical source.
/usr/bin/osacompile -o "$SCRATCH/saved.scpt" "$SOURCE"
/usr/bin/osadecompile "$SCRATCH/saved.scpt" > "$SCRATCH/saved.applescript"
/usr/bin/osacompile -o "$OUTPUT" "$SOURCE"
/usr/bin/osadecompile "$OUTPUT/Contents/Resources/Scripts/main.scpt" > "$DECOMPILED"
/usr/bin/cmp "$SCRATCH/saved.applescript" "$DECOMPILED"
/bin/chmod 444 "$SOURCE" "$DECOMPILED"
# Gather and hash in one checked process: no pipeline or ignored find -exec failure.
/usr/bin/perl -MFile::Find -MDigest::SHA -e '
my @files;
find({no_chdir => 1, wanted => sub { push @files, $File::Find::name if -f $_; }}, $ARGV[0]);
die "Empty compiled bundle\n" unless @files;
my @lines;
for my $path (sort @files) {
    open my $file, "<", $path or die "bundle read $path: $!";
    binmode $file or die "bundle binary read $path: $!";
    my $digest = Digest::SHA->new(256)->addfile($file)->hexdigest;
    close $file or die "bundle close $path: $!";
    push @lines, "$digest  $path\n";
}
print @lines or die "bundle inventory write: $!";
' "$OUTPUT"
