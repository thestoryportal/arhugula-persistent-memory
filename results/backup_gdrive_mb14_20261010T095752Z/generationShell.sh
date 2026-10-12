set -eu
generation=$(/usr/bin/perl -MJSON::PP -MFcntl=:flock -MFile::Path=make_path -MFile::Temp=tempfile -e '
my $dir = "$ENV{HOME}/Library/Logs/memit-gdrive-backup-launch-state";
make_path($dir);
open my $lock, ">>", "$dir/counter.lock" or die "generation lock: $!";
flock($lock, LOCK_EX) or die "generation lock: $!";
open my $input, "<", "$dir/counter" or die "missing generation counter: $!";
my $text = do { local $/; <$input> };
close $input or die "counter read: $!";
die "invalid or exhausted generation counter" unless $text =~ /\A(?:0|[1-9][0-9]{0,9})\n?\z/ && $text < 2147483647;
my $previous = int($text);

sub state_integer {
    my ($value, $zero) = @_;
    return defined $value && !ref($value) &&
        encode_json($value) =~ ($zero ? qr/\A(?:0|[1-9][0-9]{0,9})\z/ : qr/\A[1-9][0-9]{0,9}\z/) &&
        $value <= 2147483647;
}
sub read_state {
    my ($dir, $previous, $completed) = @_;
    if (!-e "$dir/unresolved.json") {
        return {schema => 1, issued_generation => $previous,
            unresolved => $previous > $completed ? [[$completed + 1, $previous]] : [],
            recovery_barrier => undef};
    }
    open my $input, "<", "$dir/unresolved.json" or die "unresolved generations read: $!";
    my $state = decode_json(do { local $/; <$input> });
    close $input or die "unresolved generations read: $!";
    die "malformed unresolved generation state" unless ref($state) eq "HASH" &&
        state_integer($state->{schema}, 0) && $state->{schema} == 1 &&
        state_integer($state->{issued_generation}, 1) && $state->{issued_generation} == $previous &&
        ref($state->{unresolved}) eq "ARRAY" && exists $state->{recovery_barrier} &&
        (!defined $state->{recovery_barrier} ||
            (state_integer($state->{recovery_barrier}, 0) && $state->{recovery_barrier} <= $previous));
    my $last = 0;
    for my $range (@{$state->{unresolved}}) {
        die "malformed unresolved generation set" unless ref($range) eq "ARRAY" && @$range == 2 &&
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
    $state->{unresolved} = \@pending;
    $state->{recovery_barrier} = undef if defined $state->{recovery_barrier} && $completed > $state->{recovery_barrier};
}
sub publish_state {
    my ($dir, $state) = @_;
    my ($out, $temporary) = tempfile(".unresolved.XXXXXX", DIR => $dir, UNLINK => 1);
    print {$out} encode_json($state), "\n" or die "unresolved generations write: $!";
    close $out or die "unresolved generations close: $!";
    rename $temporary, "$dir/unresolved.json" or die "unresolved generations publish: $!";
}

my ($completed, $refused) = (0, 0);
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
            !ref($generation) && encode_json($generation) =~ /\A[1-9][0-9]{0,9}\z/ && $generation <= $previous;
        if ($file =~ /last_run\.json\z/ && defined $value->{end} && defined $value->{exit_code} &&
                ($value->{launch_mode} // "applet") eq "applet" &&
                encode_json($value->{exit_code}) =~ /\A(?:0|[1-9][0-9]{0,2})\z/ && $value->{exit_code} <= 255) {
            $completed = $generation;
        }
        if ($file =~ /launch_receipt\.json\z/ &&
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
my ($out, $temporary) = tempfile(".counter.XXXXXX", DIR => $dir, UNLINK => 1);
print {$out} "$generation\n" or die "counter write: $!";
close $out or die "counter close: $!";
rename $temporary, "$dir/counter" or die "counter publish: $!";
print "$generation\n";
')
printf '%s\n' "$generation"
