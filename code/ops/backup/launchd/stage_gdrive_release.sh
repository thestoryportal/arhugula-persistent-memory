#!/bin/bash
set -euo pipefail
if [ "$#" -lt 3 ] || [ "$#" -gt 4 ]; then
  echo "Usage: $0 <git-commit> <release-id> <rendered.applescript> [release-root]" >&2
  exit 64
fi
COMMIT="$1"
RELEASE_ID="$2"
RENDERED="$3"
RELEASE_ROOT="${4:-$HOME/Library/Application Support/memit-gdrive-backup/releases}"
if [[ ! "$RELEASE_ID" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$ ]]; then
  echo "Invalid release id" >&2
  exit 64
fi
SCRIPT_DIR="$(cd "$(/usr/bin/dirname "$0")" && /bin/pwd -P)"
REPO="$(cd "$SCRIPT_DIR/../../../.." && /bin/pwd -P)"
COMMIT="$(/usr/bin/git -C "$REPO" rev-parse --verify "${COMMIT}^{commit}")"
for NAME in backup_gdrive.sh backup_gdrive_status.py backup_mirror.excludes; do
  /usr/bin/git -C "$REPO" cat-file -e "$COMMIT:code/ops/backup/$NAME"
done
# Resolve existing symlinks and check every ancestor, including other worktrees.
/usr/bin/perl -MCwd=abs_path -MFile::Basename=dirname -e '
my $path = $ARGV[0];
$path = "$ENV{PWD}/$path" unless $path =~ m{\A/};
while (!-e $path) { $path = dirname($path); }
$path = abs_path($path) // die "release root cannot be resolved\n";
while (1) {
    die "Release must be outside every git checkout: $path\n" if -e "$path/.git" || -l "$path/.git";
    last if $path eq "/";
    $path = dirname($path);
}
' "$RELEASE_ROOT"
/bin/mkdir -p "$RELEASE_ROOT"
RELEASE_ROOT="$(cd "$RELEASE_ROOT" && /bin/pwd -P)"
RELEASE="$RELEASE_ROOT/$RELEASE_ID"
RENDERED_DIR="$(cd "$(/usr/bin/dirname "$RENDERED")" && /bin/pwd -P)"
RENDERED="$RENDERED_DIR/$(/usr/bin/basename "$RENDERED")"
case "$RENDERED" in
  "$RELEASE"|"$RELEASE"/*) echo "Rendered source must be outside the release" >&2; exit 64 ;;
esac
if [ -e "$RELEASE" ] || [ -L "$RELEASE" ]; then
  echo "Refusing existing release: $RELEASE" >&2
  exit 1
fi
if [ -e "$RENDERED" ] || [ -L "$RENDERED" ]; then
  echo "Refusing existing rendered source: $RENDERED" >&2
  exit 1
fi
# mkdir is the exclusive reservation; failed staging is never reused or overwritten.
/bin/mkdir -m 700 "$RELEASE"
for NAME in backup_gdrive.sh backup_gdrive_status.py backup_mirror.excludes; do
  /usr/bin/git -C "$REPO" show "$COMMIT:code/ops/backup/$NAME" > "$RELEASE/$NAME"
done
(
  cd "$RELEASE"
  /usr/bin/shasum -a 256 backup_gdrive.sh backup_gdrive_status.py backup_mirror.excludes > MANIFEST
)
/bin/chmod 444 "$RELEASE"/backup_gdrive.sh "$RELEASE"/backup_gdrive_status.py "$RELEASE"/backup_mirror.excludes "$RELEASE"/MANIFEST
/bin/chmod 555 "$RELEASE"
/usr/bin/perl -MDigest::SHA -MFcntl=O_WRONLY,O_CREAT,O_EXCL -e '
my ($template, $release, $rendered) = @ARGV;
open my $input, "<", $template or die "template read: $!";
my $source = do { local $/; <$input> };
close $input or die "template close: $!";
my %tokens = ("backup_gdrive.sh" => "WRAPPER", "backup_gdrive_status.py" => "STATUS",
              "backup_mirror.excludes" => "EXCLUDES", "MANIFEST" => "MANIFEST");
for my $name (sort keys %tokens) {
    open my $file, "<", "$release/$name" or die "release read $name: $!";
    binmode $file or die "release binary read $name: $!";
    my $digest = Digest::SHA->new(256)->addfile($file)->hexdigest;
    close $file or die "release close $name: $!";
    my $token = "\@" . $tokens{$name} . "_SHA256\@";
    my $count = ($source =~ s/\Q$token\E/$digest/g);
    die "missing or duplicate stamp $token\n" unless $count == 1;
}
my $wrapper = "$release/backup_gdrive.sh";
die "Unsupported newline in release path\n" if $wrapper =~ /[\r\n]/;
$wrapper =~ s/\\/\\\\/g;
$wrapper =~ s/"/\\"/g;
my $wrapper_token = "\@LOCKED_WRAPPER_PATH\@";
my $count = ($source =~ s/\Q$wrapper_token\E/$wrapper/g);
die "missing or duplicate wrapper stamp\n" unless $count == 1;
sysopen my $output, $rendered, O_WRONLY|O_CREAT|O_EXCL, 0600 or die "rendered source create: $!";
print {$output} $source or die "rendered source write: $!";
close $output or die "rendered source close: $!";
' "$SCRIPT_DIR/MemitGdriveBackup.applescript" "$RELEASE" "$RENDERED"
printf '%s\n' "$RELEASE"
