from pathlib import Path
import hashlib, json, shlex
p=Path('tools/launchd/MemitGdriveBackup.applescript')
assert hashlib.sha256(p.read_bytes()).hexdigest()=='ebafee3ad82a4376ec5dda0fbc823f2170c795cddd56d62f5ede730d6d5c3bab'
allocate=r'''
my $dir = "$ENV{HOME}/Library/Logs/memit-gdrive-backup-launch-state";
make_path($dir);
open my $lock, ">>", "$dir/counter.lock" or die "generation lock: $!";
flock($lock, LOCK_EX) or die "generation lock: $!";
open my $input, "<", "$dir/counter" or die "missing generation counter: $!";
my $text = do { local $/; <$input> };
close $input or die "counter read: $!";
die "invalid or exhausted generation counter" unless $text =~ /\A(?:0|[1-9][0-9]{0,9})\n?\z/ && $text < 2147483647;
my $previous = int($text);
for my $file ("$ENV{HOME}/Library/Logs/memit-gdrive-backup/last_run.json",
              "$ENV{HOME}/Library/Logs/memit-gdrive-backup/launch_receipt.json",
              "$ENV{HOME}/Library/Logs/memit-gdrive-backup-launch-journal/failures.jsonl") {
    next unless -e $file;
    open my $evidence, "<", $file or die "generation evidence read: $!";
    my @records;
    if ($file =~ /jsonl\z/) { @records = <$evidence>; }
    else { @records = (do { local $/; <$evidence> }); }
    close $evidence or die "generation evidence read: $!";
    die "empty generation evidence" unless @records;
    for my $line (@records) {
        my $value = decode_json($line);
        die "malformed generation evidence" unless ref($value) eq "HASH";
        my $generation = $value->{launch_generation};
        if (!defined $generation && $file =~ /last_run\.json\z/ &&
                (!exists $value->{launch_mode} || $value->{launch_mode} eq "manual")) { next; }
        die "ambiguous or non-increasing launch generation" unless defined $generation &&
            !ref($generation) && $generation =~ /\A[1-9][0-9]{0,9}\z/ && $generation <= $previous;
    }
}
my $generation = $previous + 1;
my ($out, $temporary) = tempfile(".counter.XXXXXX", DIR => $dir, UNLINK => 1);
print {$out} "$generation\n" or die "counter write: $!";
close $out or die "counter close: $!";
rename $temporary, "$dir/counter" or die "counter publish: $!";
print "$generation\n";
'''
generation_shell='set -eu\ngeneration=$(/usr/bin/perl -MJSON::PP -MFcntl=:flock -MFile::Path=make_path -MFile::Temp=tempfile -e '+shlex.quote(allocate)+')\nprintf \'%s\\n\' "$generation"\n'
launch_shell='wrapper=$1\ngeneration=${generation:-${2:-}}\nif BACKUP_LAUNCH_GENERATION="$generation" /bin/bash "$wrapper"; then\n    exit_code=0\nelse\n    exit_code=$?\nfi\nset -- "$wrapper" "$exit_code" "" "$generation"\n'
publish=r'''
my ($sec, $micro) = gettimeofday();
my $generation = $ARGV[3] =~ /\A[1-9][0-9]{0,9}\z/ && $ARGV[3] <= 2147483647 ? int($ARGV[3]) : undef;
my $value = {schema => 1, launch_generation => $generation,
    utc => strftime("%Y-%m-%dT%H:%M:%S", gmtime($sec)) . sprintf(".%06dZ", $micro),
    wrapper_path => $ARGV[0], exit_code => length($ARGV[1]) ? int($ARGV[1]) : undef,
    error_number => length($ARGV[2]) ? int($ARGV[2]) : undef};
my $dir = "$ENV{HOME}/Library/Logs/memit-gdrive-backup";
my $published = eval {
    make_path($dir);
    my ($out, $temporary) = tempfile(".launch-receipt.XXXXXX", DIR => $dir, UNLINK => 1);
    print {$out} encode_json($value), "\n" or die "receipt write: $!";
    close $out or die "receipt close: $!";
    rename $temporary, "$dir/launch_receipt.json" or die "receipt publish: $!";
    1;
};
my $publication_error = $@;
my $failed = !defined $generation ||
    (defined $value->{exit_code} && $value->{exit_code} != 0 && $value->{exit_code} != 75) ||
    (defined $value->{error_number} && $value->{error_number} != 75);
if (!$published || $failed) {
    my $journaled = eval {
        my $journal_dir = "$ENV{HOME}/Library/Logs/memit-gdrive-backup-launch-journal";
        make_path($journal_dir);
        open my $lock, ">>", "$journal_dir/journal.lock" or die "journal lock: $!";
        flock($lock, LOCK_EX) or die "journal lock: $!";
        my $file = "$journal_dir/failures.jsonl";
        my @markers;
        if (-e $file) {
            open my $input, "<", $file or die "journal read: $!";
            @markers = map { decode_json($_) } <$input>;
            close $input or die "journal close: $!";
            die "malformed journal" if !@markers || @markers > 64 || -s $file > 65536;
            for my $marker (@markers) {
                die "malformed journal" unless ref($marker) eq "HASH" && $marker->{schema} == 1 &&
                    defined $marker->{reason} && length($marker->{reason}) <= 256 &&
                    (!defined $marker->{launch_generation} ||
                     (!ref($marker->{launch_generation}) && $marker->{launch_generation} =~ /\A[1-9][0-9]{0,9}\z/ &&
                      $marker->{launch_generation} <= 2147483647));
            }
        }
        push @markers, {schema => 1, launch_generation => $generation, utc => $value->{utc},
            reason => !$published ? "receipt publication failed" : "failed launch"};
        # Retain the greatest failed generations and any ambiguous marker.
        @markers = sort { ($a->{launch_generation} // 2147483648) <=> ($b->{launch_generation} // 2147483648) } @markers;
        splice @markers, 0, @markers - 64 if @markers > 64;
        my ($out, $temporary) = tempfile(".journal.XXXXXX", DIR => $journal_dir, UNLINK => 1);
        for my $marker (@markers) { print {$out} encode_json($marker), "\n" or die "journal write: $!"; }
        close $out or die "journal close: $!";
        rename $temporary, $file or die "journal publish: $!";
        1;
    };
    warn "launch journal failed: $@" unless $journaled;
}
warn "launch receipt failed: $publication_error" unless $published;
exit($published ? 0 : 1);
'''
receipt_shell='set -eu\nwrapper=$1\nexit_code=${2:-}\nerror_number=${3:-}\ngeneration=${4:-${generation:-}}\n/usr/bin/perl -MJSON::PP -MTime::HiRes=gettimeofday -MPOSIX=strftime -MFcntl=:flock -MFile::Path=make_path -MFile::Temp=tempfile -e '+shlex.quote(publish)+' "$wrapper" "$exit_code" "$error_number" "$generation"\n'
lines=['-- All ordering state is internal; the counter must be provisioned once before activation.',
       'property wrapperPath : '+json.dumps('/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/tools/backup_gdrive.sh'),
       'property generationShell : '+json.dumps(generation_shell),
       'property launchShell : '+json.dumps(launch_shell),
       '-- Publish failures independently, including when the volume or receipt directory is unavailable.',
       'property receiptShell : '+json.dumps(receipt_shell),
       '', 'set launchGeneration to ""', 'try',
       '    set launchGeneration to do shell script "/bin/sh -c " & quoted form of generationShell & " backup-generation"',
       '    do shell script "/bin/sh -c " & quoted form of (launchShell & receiptShell) & " backup-launch " & quoted form of wrapperPath & " " & quoted form of launchGeneration',
       'on error errorMessage number errorNumber', '    try',
       '        do shell script "/bin/sh -c " & quoted form of receiptShell & " backup-receipt " & quoted form of wrapperPath & " \'\' " & quoted form of (errorNumber as text) & " " & quoted form of launchGeneration',
       '    end try', 'end try', '']
p.write_text('\n'.join(lines))
print('Applet generation allocation and bounded independent failure journal implemented; nested catches preserved.')
