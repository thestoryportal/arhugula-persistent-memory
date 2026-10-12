-- All ordering state is internal; the counter must be provisioned once before activation.
property wrapperPath : "/private/tmp/gdrive_addendum_44d5_c07/home/Library/Application Support/memit-gdrive-backup/releases/fixture-r1/backup_gdrive.sh"
property generationShell : "HOME=/private/tmp/gdrive_addendum_44d5_c07/home
export HOME
set -eu
generation=$(/usr/bin/perl -MJSON::PP -MFcntl=:flock -MFile::Path=make_path -MFile::Temp=tempfile -e '
my $dir = \"$ENV{HOME}/Library/Logs/memit-gdrive-backup-launch-state\";
make_path($dir);
open my $lock, \">>\", \"$dir/counter.lock\" or die \"generation lock: $!\";
flock($lock, LOCK_EX) or die \"generation lock: $!\";
open my $input, \"<\", \"$dir/counter\" or die \"missing generation counter: $!\";
my $text = do { local $/; <$input> };
close $input or die \"counter read: $!\";
die \"invalid or exhausted generation counter\" unless $text =~ /\\A(?:0|[1-9][0-9]{0,9})\\n?\\z/ && $text < 2147483647;
my $previous = int($text);

sub state_integer {
    my ($value, $zero) = @_;
    return defined $value && !ref($value) &&
        encode_json($value) =~ ($zero ? qr/\\A(?:0|[1-9][0-9]{0,9})\\z/ : qr/\\A[1-9][0-9]{0,9}\\z/) &&
        $value <= 2147483647;
}
sub read_state {
    my ($dir, $previous, $completed) = @_;
    if (!-e \"$dir/unresolved.json\") {
        return {schema => 1, issued_generation => $previous,
            unresolved => $previous > $completed ? [[$completed + 1, $previous]] : [],
            recovery_barrier => undef, compaction_barrier => undef};
    }
    open my $input, \"<\", \"$dir/unresolved.json\" or die \"unresolved generations read: $!\";
    my $state = decode_json(do { local $/; <$input> });
    close $input or die \"unresolved generations read: $!\";
    die \"malformed unresolved generation state\" unless ref($state) eq \"HASH\" &&
        state_integer($state->{schema}, 0) && $state->{schema} == 1 &&
        state_integer($state->{issued_generation}, 1) && $state->{issued_generation} == $previous &&
        ref($state->{unresolved}) eq \"ARRAY\" && exists $state->{recovery_barrier} &&
        (!defined $state->{recovery_barrier} ||
            (state_integer($state->{recovery_barrier}, 0) && $state->{recovery_barrier} <= $previous)) &&
        (!defined $state->{compaction_barrier} ||
            (state_integer($state->{compaction_barrier}, 0) && $state->{compaction_barrier} <= $previous));
    my $last = 0;
    for my $range (@{$state->{unresolved}}) {
        die \"malformed unresolved generation set\" unless ref($range) eq \"ARRAY\" && @$range == 2 &&
            state_integer($range->[0], 0) && state_integer($range->[1], 0) &&
            $range->[0] > $last && $range->[0] <= $range->[1] && $range->[1] <= $previous;
        $last = $range->[1];
    }
    return $state;
}
sub resolve_state {
    my ($state, $completed, $refused) = @_;
    my @pending;
    for my $range (@{$state->{unresolved}}) {
        my ($low, $high) = @$range;
        next if $high <= $completed;
        $low = $completed + 1 if $low <= $completed;
        if ($refused && $low <= $refused && $refused <= $high) {
            push @pending, [$low, $refused - 1] if $low < $refused;
            push @pending, [$refused + 1, $high] if $refused < $high;
        } else { push @pending, [$low, $high]; }
    }
    $state->{unresolved} = \\@pending;
    $state->{recovery_barrier} = undef if defined $state->{recovery_barrier} && $completed > $state->{recovery_barrier};
    $state->{compaction_barrier} = undef if defined $state->{compaction_barrier} && $completed > $state->{compaction_barrier};
}
sub compact_state {
    my ($state) = @_;
    $state->{compaction_barrier} = undef unless exists $state->{compaction_barrier};
    # A refusal removes only itself; overflow retains all issued history as a barrier.
    if (@{$state->{unresolved}} > 64 || length(encode_json($state)) + 1 > 2048) {
        %$state = (schema => 1, issued_generation => $state->{issued_generation}, unresolved => [],
                   recovery_barrier => $state->{recovery_barrier}, compaction_barrier => $state->{issued_generation});
    }
}
sub publish_state {
    my ($dir, $state) = @_;
    compact_state($state);
    my ($out, $temporary) = tempfile(\".unresolved.XXXXXX\", DIR => $dir, UNLINK => 1);
    print {$out} encode_json($state), \"\\n\" or die \"unresolved generations write: $!\";
    close $out or die \"unresolved generations close: $!\";
    rename $temporary, \"$dir/unresolved.json\" or die \"unresolved generations publish: $!\";
}

my ($completed, $refused) = (0, 0);
for my $file (\"$ENV{HOME}/Library/Logs/memit-gdrive-backup/last_run.json\",
              \"$ENV{HOME}/Library/Logs/memit-gdrive-backup/launch_receipt.json\",
              \"$ENV{HOME}/Library/Logs/memit-gdrive-backup-launch-journal/failures.jsonl\") {
    next unless -e $file;
    open my $evidence, \"<\", $file or die \"generation evidence read: $!\";
    my @records;
    if ($file =~ /jsonl\\z/) { @records = <$evidence>; }
    else { @records = (do { local $/; <$evidence> }); }
    close $evidence or die \"generation evidence read: $!\";
    die \"empty generation evidence\" unless @records;
    for my $line (@records) {
        my $value = decode_json($line);
        die \"malformed generation evidence\" unless ref($value) eq \"HASH\";
        my $generation = $value->{launch_generation};
        if (!defined $generation && $file =~ /last_run\\.json\\z/ &&
                (!exists $value->{launch_mode} || $value->{launch_mode} eq \"manual\")) { next; }
        die \"ambiguous or non-increasing launch generation\" unless defined $generation &&
            !ref($generation) && encode_json($generation) =~ /\\A[1-9][0-9]{0,9}\\z/ && $generation <= $previous;
        if ($file =~ /last_run\\.json\\z/ && defined $value->{end} && defined $value->{exit_code} &&
                ($value->{launch_mode} // \"applet\") eq \"applet\" &&
                encode_json($value->{exit_code}) =~ /\\A(?:0|[1-9][0-9]{0,2})\\z/ && $value->{exit_code} <= 255) {
            $completed = $generation;
        }
        if ($file =~ /launch_receipt\\.json\\z/ &&
                ((defined $value->{exit_code} && $value->{exit_code} == 75) ||
                 (defined $value->{error_number} && $value->{error_number} == 75))) { $refused = $generation; }

    }
}
my $state = read_state($dir, $previous, $completed);
resolve_state($state, $completed, $refused);
my $generation = $previous + 1;
$state->{issued_generation} = $generation;
if (@{$state->{unresolved}} && $state->{unresolved}[-1][1] == $previous) {
    $state->{unresolved}[-1][1] = $generation;
} else { push @{$state->{unresolved}}, [$generation, $generation]; }
# Publish issued evidence first: interruption between renames refuses allocation.
publish_state($dir, $state);
my ($out, $temporary) = tempfile(\".counter.XXXXXX\", DIR => $dir, UNLINK => 1);
print {$out} \"$generation\\n\" or die \"counter write: $!\";
close $out or die \"counter close: $!\";
rename $temporary, \"$dir/counter\" or die \"counter publish: $!\";
print \"$generation\\n\";
')
printf '%s\\n' \"$generation\"
"
property integrityShell : "HOME=/private/tmp/gdrive_addendum_44d5_c07/home
export HOME
wrapper=$1
generation=${generation:-${2:-}}
if integrity_failure=$(PERL5LIB= PERL5OPT= /usr/bin/perl -MDigest::SHA -MJSON::PP -MFile::Basename=dirname -e '
my $dir = dirname($ARGV[0]);
my %expected = (
    \"backup_gdrive.sh\" => \"302df2334fa08d48bd2ecb78351014c5bf0cd31ceb41468358b7e6cc110997c9\",
    \"backup_gdrive_status.py\" => \"f1f4cb4c0cc11882f4969ab19961017ee9ab12e1911df9aa9512a4e1c3e227a3\",
    \"backup_mirror.excludes\" => \"bd6ebd936036c1cdc4bc027aa775ea0b1bb4ef6b3ed16ba89e70d83ae81bf1f3\",
    \"MANIFEST\" => \"9dc1b3015b5e09cfe43bd32f0667b240e11284ffe5e043e9978ed6b3948a57e8\",
);
sub observed_hash {
    my ($path) = @_;
    return \"SYMLINK\" if -l $path;
    return \"MISSING\" unless lstat($path);
    return \"NOT_REGULAR\" unless -f $path;
    open my $file, \"<\", $path or return \"UNREADABLE\";
    binmode $file or return \"UNREADABLE\";
    my $digest = Digest::SHA->new(256);
    my $read = eval { $digest->addfile($file); 1; };
    my $closed = close $file;
    return $read && $closed ? $digest->hexdigest : \"UNREADABLE\";
}
my @failures;
if (-l $dir || !-d $dir) {
    push @failures, {file => \"<release-directory>\", expected_sha256 => \"DIRECTORY\",
        actual_sha256 => -l $dir ? \"SYMLINK\" : \"MISSING\"};
}
for my $name (sort keys %expected) {
    my $observed = observed_hash(\"$dir/$name\");
    push @failures, {file => $name, expected_sha256 => $expected{$name}, actual_sha256 => $observed}
        unless $observed eq $expected{$name};
}
if (opendir my $directory, $dir) {
    my @extra = sort grep { $_ ne \".\" && $_ ne \"..\" && !exists $expected{$_} } readdir $directory;
    closedir $directory or die \"release directory close: $!\";
    for my $name (@extra) {
        push @failures, {file => $name, expected_sha256 => \"ABSENT\",
            actual_sha256 => observed_hash(\"$dir/$name\")};
    }
} else {
    push @failures, {file => \"<release-directory>\", expected_sha256 => \"READABLE\",
        actual_sha256 => \"UNREADABLE\"};
}
print JSON::PP->new->canonical->encode(\\@failures) or die \"integrity result write: $!\";
' \"$wrapper\"); then
    :
else
    integrity_failure='[{\"file\":\"<integrity-check>\",\"expected_sha256\":\"SUCCESS\",\"actual_sha256\":\"CHECK_FAILED\"}]'
fi
"
property launchShell : "wrapper=$1
generation=${generation:-${2:-}}
if [ -n \"${integrity_failure:-}\" ] && [ \"$integrity_failure\" != \"[]\" ]; then
    exit_code=78
elif BACKUP_LAUNCH_GENERATION=\"$generation\" /bin/bash \"$wrapper\"; then
    exit_code=0
else
    exit_code=$?
fi
set -- \"$wrapper\" \"$exit_code\" \"\" \"$generation\"
"
-- Publish failures independently, including when the volume or receipt directory is unavailable.
property receiptShell : "HOME=/private/tmp/gdrive_addendum_44d5_c07/home
export HOME
set -eu
wrapper=$1
exit_code=${2:-}
error_number=${3:-}
generation=${4:-${generation:-}}
integrity_failure=${integrity_failure:-${5:-}}
/usr/bin/perl -MJSON::PP -MTime::HiRes=gettimeofday -MPOSIX=strftime -MFcntl=:flock -MFile::Path=make_path -MFile::Temp=tempfile -e '

sub state_integer {
    my ($value, $zero) = @_;
    return defined $value && !ref($value) &&
        encode_json($value) =~ ($zero ? qr/\\A(?:0|[1-9][0-9]{0,9})\\z/ : qr/\\A[1-9][0-9]{0,9}\\z/) &&
        $value <= 2147483647;
}
sub read_state {
    my ($dir, $previous, $completed) = @_;
    if (!-e \"$dir/unresolved.json\") {
        return {schema => 1, issued_generation => $previous,
            unresolved => $previous > $completed ? [[$completed + 1, $previous]] : [],
            recovery_barrier => undef, compaction_barrier => undef};
    }
    open my $input, \"<\", \"$dir/unresolved.json\" or die \"unresolved generations read: $!\";
    my $state = decode_json(do { local $/; <$input> });
    close $input or die \"unresolved generations read: $!\";
    die \"malformed unresolved generation state\" unless ref($state) eq \"HASH\" &&
        state_integer($state->{schema}, 0) && $state->{schema} == 1 &&
        state_integer($state->{issued_generation}, 1) && $state->{issued_generation} == $previous &&
        ref($state->{unresolved}) eq \"ARRAY\" && exists $state->{recovery_barrier} &&
        (!defined $state->{recovery_barrier} ||
            (state_integer($state->{recovery_barrier}, 0) && $state->{recovery_barrier} <= $previous)) &&
        (!defined $state->{compaction_barrier} ||
            (state_integer($state->{compaction_barrier}, 0) && $state->{compaction_barrier} <= $previous));
    my $last = 0;
    for my $range (@{$state->{unresolved}}) {
        die \"malformed unresolved generation set\" unless ref($range) eq \"ARRAY\" && @$range == 2 &&
            state_integer($range->[0], 0) && state_integer($range->[1], 0) &&
            $range->[0] > $last && $range->[0] <= $range->[1] && $range->[1] <= $previous;
        $last = $range->[1];
    }
    return $state;
}
sub resolve_state {
    my ($state, $completed, $refused) = @_;
    my @pending;
    for my $range (@{$state->{unresolved}}) {
        my ($low, $high) = @$range;
        next if $high <= $completed;
        $low = $completed + 1 if $low <= $completed;
        if ($refused && $low <= $refused && $refused <= $high) {
            push @pending, [$low, $refused - 1] if $low < $refused;
            push @pending, [$refused + 1, $high] if $refused < $high;
        } else { push @pending, [$low, $high]; }
    }
    $state->{unresolved} = \\@pending;
    $state->{recovery_barrier} = undef if defined $state->{recovery_barrier} && $completed > $state->{recovery_barrier};
    $state->{compaction_barrier} = undef if defined $state->{compaction_barrier} && $completed > $state->{compaction_barrier};
}
sub compact_state {
    my ($state) = @_;
    $state->{compaction_barrier} = undef unless exists $state->{compaction_barrier};
    # A refusal removes only itself; overflow retains all issued history as a barrier.
    if (@{$state->{unresolved}} > 64 || length(encode_json($state)) + 1 > 2048) {
        %$state = (schema => 1, issued_generation => $state->{issued_generation}, unresolved => [],
                   recovery_barrier => $state->{recovery_barrier}, compaction_barrier => $state->{issued_generation});
    }
}
sub publish_state {
    my ($dir, $state) = @_;
    compact_state($state);
    my ($out, $temporary) = tempfile(\".unresolved.XXXXXX\", DIR => $dir, UNLINK => 1);
    print {$out} encode_json($state), \"\\n\" or die \"unresolved generations write: $!\";
    close $out or die \"unresolved generations close: $!\";
    rename $temporary, \"$dir/unresolved.json\" or die \"unresolved generations publish: $!\";
}

my ($sec, $micro) = gettimeofday();
my $generation = $ARGV[3] =~ /\\A[1-9][0-9]{0,9}\\z/ && $ARGV[3] <= 2147483647 ? int($ARGV[3]) : undef;
my $value = {schema => 1, launch_generation => $generation,
    utc => strftime(\"%Y-%m-%dT%H:%M:%S\", gmtime($sec)) . sprintf(\".%06dZ\", $micro),
    wrapper_path => $ARGV[0], exit_code => length($ARGV[1]) ? int($ARGV[1]) : undef,
    error_number => length($ARGV[2]) ? int($ARGV[2]) : undef};
if (length($ARGV[4] // \"\") && $ARGV[4] ne \"[]\") {
    $value->{integrity_failures} = decode_json($ARGV[4]);
}
my $dir = \"$ENV{HOME}/Library/Logs/memit-gdrive-backup\";
my $failed = !defined $generation ||
    (defined $value->{exit_code} && $value->{exit_code} != 0 && $value->{exit_code} != 75) ||
    (defined $value->{error_number} && $value->{error_number} != 75);
my $state_lock;
my $published = eval {
    make_path(\"$ENV{HOME}/Library/Logs/memit-gdrive-backup-launch-state\");
    open $state_lock, \">>\", \"$ENV{HOME}/Library/Logs/memit-gdrive-backup-launch-state/counter.lock\"
        or die \"receipt generation lock: $!\";
    flock($state_lock, LOCK_EX) or die \"receipt generation lock: $!\";
    if (defined $generation) {
        my $state_dir = \"$ENV{HOME}/Library/Logs/memit-gdrive-backup-launch-state\";
        open my $counter, \"<\", \"$state_dir/counter\" or die \"receipt counter read: $!\";
        my $text = do { local $/; <$counter> };
        close $counter or die \"receipt counter read: $!\";
        die \"invalid receipt generation counter\" unless $text =~ /\\A(?:0|[1-9][0-9]{0,9})\\n?\\z/ &&
            $text <= 2147483647 && $generation <= $text;
        my $completed = 0;
        if (-e \"$dir/last_run.json\") {
            open my $heartbeat, \"<\", \"$dir/last_run.json\" or die \"heartbeat read: $!\";
            my $last = decode_json(do { local $/; <$heartbeat> });
            close $heartbeat or die \"heartbeat read: $!\";
            if (ref($last) eq \"HASH\" && defined $last->{end} && defined $last->{exit_code} &&
                    state_integer($last->{launch_generation}, 0) &&
                    ($last->{launch_mode} // \"applet\") eq \"applet\" &&
                    encode_json($last->{exit_code}) =~ /\\A(?:0|[1-9][0-9]{0,2})\\z/ && $last->{exit_code} <= 255) {
                $completed = $last->{launch_generation};
            }
        }
        my $state = read_state($state_dir, int($text), $completed);
        my $refused = (defined $value->{exit_code} && $value->{exit_code} == 75) ||
                      (defined $value->{error_number} && $value->{error_number} == 75);
        resolve_state($state, $completed, $refused ? $generation : 0);
        publish_state($state_dir, $state);

    }
    my $keep_failure = 0;
    if (defined $generation && -e \"$dir/launch_receipt.json\") {
        open my $input, \"<\", \"$dir/launch_receipt.json\" or die \"receipt read: $!\";
        my $old = decode_json(do { local $/; <$input> });
        close $input or die \"receipt read: $!\";
        my $old_generation = $old->{launch_generation};
        my $old_failed = (defined $old->{exit_code} && $old->{exit_code} != 0 && $old->{exit_code} != 75) ||
                         (defined $old->{error_number} && $old->{error_number} != 75);
        my $completed = 0;
        if (-e \"$dir/last_run.json\") {
            open my $heartbeat, \"<\", \"$dir/last_run.json\" or die \"heartbeat read: $!\";
            my $last = decode_json(do { local $/; <$heartbeat> });
            close $heartbeat or die \"heartbeat read: $!\";
            if (defined $last->{end} && defined $last->{exit_code} && defined $last->{launch_generation} &&
                    encode_json($last->{launch_generation}) =~ /\\A[1-9][0-9]{0,9}\\z/) {
                $completed = $last->{launch_generation};
            }
        }
        # Journal loss cannot let a success/refusal receipt erase an unresolved failure.
        $keep_failure = $old_failed && defined $old_generation && $old_generation > $completed &&
                        (!$failed || $generation <= $old_generation);
    }
    if (!$keep_failure) {
        make_path($dir);
        my ($out, $temporary) = tempfile(\".launch-receipt.XXXXXX\", DIR => $dir, UNLINK => 1);
        print {$out} encode_json($value), \"\\n\" or die \"receipt write: $!\";
        close $out or die \"receipt close: $!\";
        rename $temporary, \"$dir/launch_receipt.json\" or die \"receipt publish: $!\";
    }
    1;
};
my $publication_error = $@;
if (!$published || $failed) {
    my $journaled = eval {
        my $journal_dir = \"$ENV{HOME}/Library/Logs/memit-gdrive-backup-launch-journal\";
        make_path($journal_dir);
        open my $lock, \">>\", \"$journal_dir/journal.lock\" or die \"journal lock: $!\";
        flock($lock, LOCK_EX) or die \"journal lock: $!\";
        my $file = \"$journal_dir/failures.jsonl\";
        my @markers;
        if (-e $file) {
            open my $input, \"<\", $file or die \"journal read: $!\";
            @markers = map { decode_json($_) } <$input>;
            close $input or die \"journal close: $!\";
            die \"malformed journal\" if !@markers || @markers > 64 || -s $file > 65536;
            for my $marker (@markers) {
                die \"malformed journal\" unless ref($marker) eq \"HASH\" && $marker->{schema} == 1 &&
                    defined $marker->{reason} && length($marker->{reason}) <= 256 &&
                    (!defined $marker->{launch_generation} ||
                     (!ref($marker->{launch_generation}) && encode_json($marker->{launch_generation}) =~ /\\A[1-9][0-9]{0,9}\\z/ &&
                      $marker->{launch_generation} <= 2147483647));
            }
        }
        push @markers, {schema => 1, launch_generation => $generation, utc => $value->{utc},
            reason => !$published ? \"receipt publication failed\" : \"failed launch\"};
        # Retain the greatest failed generations and any ambiguous marker.
        @markers = sort { ($a->{launch_generation} // 2147483648) <=> ($b->{launch_generation} // 2147483648) } @markers;
        splice @markers, 0, @markers - 64 if @markers > 64;
        my ($out, $temporary) = tempfile(\".journal.XXXXXX\", DIR => $journal_dir, UNLINK => 1);
        for my $marker (@markers) { print {$out} encode_json($marker), \"\\n\" or die \"journal write: $!\"; }
        close $out or die \"journal close: $!\";
        rename $temporary, $file or die \"journal publish: $!\";
        1;
    };
    warn \"launch journal failed: $@\" unless $journaled;
}
warn \"launch receipt failed: $publication_error\" unless $published;
exit($published ? 0 : 1);
' \"$wrapper\" \"$exit_code\" \"$error_number\" \"$generation\" \"$integrity_failure\"
"

set launchGeneration to ""
try
	set launchGeneration to do shell script "/bin/sh -c " & quoted form of generationShell & " backup-generation"
	do shell script "/bin/sh -c " & quoted form of (integrityShell & launchShell & receiptShell) & " backup-launch " & quoted form of wrapperPath & " " & quoted form of launchGeneration
on error errorMessage number errorNumber
	try
		do shell script "/bin/sh -c " & quoted form of receiptShell & " backup-receipt " & quoted form of wrapperPath & " '' " & quoted form of (errorNumber as text) & " " & quoted form of launchGeneration
	end try
end try


