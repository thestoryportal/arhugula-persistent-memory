"""Surgical generation of the MB32 stamped integrity literal."""
from pathlib import Path
import json
import re

path = Path("tools/launchd/MemitGdriveBackup.applescript")
source = path.read_text()
checker = '''wrapper=$1
generation=${generation:-${2:-}}
if integrity_failure=$(PERL5LIB= PERL5OPT= /usr/bin/perl -MDigest::SHA -MJSON::PP -MFile::Basename=dirname -e '
my $dir = dirname($ARGV[0]);
my %expected = (
    "backup_gdrive.sh" => "@WRAPPER_SHA256@",
    "backup_gdrive_status.py" => "@STATUS_SHA256@",
    "backup_mirror.excludes" => "@EXCLUDES_SHA256@",
    "MANIFEST" => "@MANIFEST_SHA256@",
);
sub observed_hash {
    my ($path) = @_;
    return "SYMLINK" if -l $path;
    return "MISSING" unless lstat($path);
    return "NOT_REGULAR" unless -f $path;
    open my $file, "<", $path or return "UNREADABLE";
    binmode $file or return "UNREADABLE";
    my $digest = Digest::SHA->new(256);
    my $read = eval { $digest->addfile($file); 1; };
    my $closed = close $file;
    return $read && $closed ? $digest->hexdigest : "UNREADABLE";
}
my @failures;
if (-l $dir || !-d $dir) {
    push @failures, {file => "<release-directory>", expected_sha256 => "DIRECTORY",
        actual_sha256 => -l $dir ? "SYMLINK" : "MISSING"};
}
for my $name (sort keys %expected) {
    my $observed = observed_hash("$dir/$name");
    push @failures, {file => $name, expected_sha256 => $expected{$name}, actual_sha256 => $observed}
        unless $observed eq $expected{$name};
}
if (opendir my $directory, $dir) {
    my @extra = sort grep { $_ ne "." && $_ ne ".." && !exists $expected{$_} } readdir $directory;
    closedir $directory or die "release directory close: $!";
    for my $name (@extra) {
        push @failures, {file => $name, expected_sha256 => "ABSENT",
            actual_sha256 => observed_hash("$dir/$name")};
    }
} else {
    push @failures, {file => "<release-directory>", expected_sha256 => "READABLE",
        actual_sha256 => "UNREADABLE"};
}
print JSON::PP->new->canonical->encode(\\@failures) or die "integrity result write: $!";
' "$wrapper"); then
    :
else
    integrity_failure='[{"file":"<integrity-check>","expected_sha256":"SUCCESS","actual_sha256":"CHECK_FAILED"}]'
fi
'''
source = re.sub(r'^property wrapperPath : .*$', 'property wrapperPath : "@LOCKED_WRAPPER_PATH@"', source, flags=re.M)
source = source.replace('property launchShell : ', 'property integrityShell : '+json.dumps(checker)+'\nproperty launchShell : ', 1)
def update_literal(name, transform):
    global source
    pattern = r'^property '+name+r' : ("(?:\\.|[^"\\])*")$'
    match = re.search(pattern, source, re.M)
    assert match is not None
    before = json.loads(match[1])
    after = transform(before)
    assert before != after
    source = source[:match.start(1)]+json.dumps(after)+source[match.end(1):]
update_literal("launchShell", lambda s: s.replace(
    'if BACKUP_LAUNCH_GENERATION=',
    'if [ -n "${integrity_failure:-}" ] && [ "$integrity_failure" != "[]" ]; then\n    exit_code=78\nelif BACKUP_LAUNCH_GENERATION=', 1))
update_literal("receiptShell", lambda s: s.replace(
    'generation=${4:-${generation:-}}\n',
    'generation=${4:-${generation:-}}\nintegrity_failure=${integrity_failure:-${5:-}}\n', 1).replace(
    'my $dir = "$ENV{HOME}/Library/Logs/memit-gdrive-backup";',
    'if (length($ARGV[4] // "") && $ARGV[4] ne "[]") {\n    $value->{integrity_failures} = decode_json($ARGV[4]);\n}\nmy $dir = "$ENV{HOME}/Library/Logs/memit-gdrive-backup";', 1).replace(
    '\' "$wrapper" "$exit_code" "$error_number" "$generation"\n',
    '\' "$wrapper" "$exit_code" "$error_number" "$generation" "$integrity_failure"\n', 1))
source = source.replace('quoted form of (launchShell & receiptShell)',
                        'quoted form of (integrityShell & launchShell & receiptShell)', 1)
path.write_text(source)
