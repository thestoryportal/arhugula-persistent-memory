set -eu
wrapper=$1
exit_code=${2:-}
error_number=${3:-}
generation=${4:-${generation:-}}
/usr/bin/perl -MJSON::PP -MTime::HiRes=gettimeofday -MPOSIX=strftime -MFcntl=:flock -MFile::Path=make_path -MFile::Temp=tempfile -e '

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

my ($sec, $micro) = gettimeofday();
my $generation = $ARGV[3] =~ /\A[1-9][0-9]{0,9}\z/ && $ARGV[3] <= 2147483647 ? int($ARGV[3]) : undef;
my $value = {schema => 1, launch_generation => $generation,
    utc => strftime("%Y-%m-%dT%H:%M:%S", gmtime($sec)) . sprintf(".%06dZ", $micro),
    wrapper_path => $ARGV[0], exit_code => length($ARGV[1]) ? int($ARGV[1]) : undef,
    error_number => length($ARGV[2]) ? int($ARGV[2]) : undef};
my $dir = "$ENV{HOME}/Library/Logs/memit-gdrive-backup";
my $failed = !defined $generation ||
    (defined $value->{exit_code} && $value->{exit_code} != 0 && $value->{exit_code} != 75) ||
    (defined $value->{error_number} && $value->{error_number} != 75);
my $state_lock;
my $published = eval {
    make_path("$ENV{HOME}/Library/Logs/memit-gdrive-backup-launch-state");
    open $state_lock, ">>", "$ENV{HOME}/Library/Logs/memit-gdrive-backup-launch-state/counter.lock"
        or die "receipt generation lock: $!";
    flock($state_lock, LOCK_EX) or die "receipt generation lock: $!";
    if (defined $generation) {
        my $state_dir = "$ENV{HOME}/Library/Logs/memit-gdrive-backup-launch-state";
        open my $counter, "<", "$state_dir/counter" or die "receipt counter read: $!";
        my $text = do { local $/; <$counter> };
        close $counter or die "receipt counter read: $!";
        die "invalid receipt generation counter" unless $text =~ /\A(?:0|[1-9][0-9]{0,9})\n?\z/ &&
            $text <= 2147483647 && $generation <= $text;
        my $completed = 0;
        if (-e "$dir/last_run.json") {
            open my $heartbeat, "<", "$dir/last_run.json" or die "heartbeat read: $!";
            my $last = decode_json(do { local $/; <$heartbeat> });
            close $heartbeat or die "heartbeat read: $!";
            if (ref($last) eq "HASH" && defined $last->{end} && defined $last->{exit_code} &&
                    state_integer($last->{launch_generation}, 0) &&
                    ($last->{launch_mode} // "applet") eq "applet" &&
                    encode_json($last->{exit_code}) =~ /\A(?:0|[1-9][0-9]{0,2})\z/ && $last->{exit_code} <= 255) {
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
    if (defined $generation && -e "$dir/launch_receipt.json") {
        open my $input, "<", "$dir/launch_receipt.json" or die "receipt read: $!";
        my $old = decode_json(do { local $/; <$input> });
        close $input or die "receipt read: $!";
        my $old_generation = $old->{launch_generation};
        my $old_failed = (defined $old->{exit_code} && $old->{exit_code} != 0 && $old->{exit_code} != 75) ||
                         (defined $old->{error_number} && $old->{error_number} != 75);
        my $completed = 0;
        if (-e "$dir/last_run.json") {
            open my $heartbeat, "<", "$dir/last_run.json" or die "heartbeat read: $!";
            my $last = decode_json(do { local $/; <$heartbeat> });
            close $heartbeat or die "heartbeat read: $!";
            if (defined $last->{end} && defined $last->{exit_code} && defined $last->{launch_generation} &&
                    encode_json($last->{launch_generation}) =~ /\A[1-9][0-9]{0,9}\z/) {
                $completed = $last->{launch_generation};
            }
        }
        # Journal loss cannot let a success/refusal receipt erase an unresolved failure.
        $keep_failure = $old_failed && defined $old_generation && $old_generation > $completed &&
                        (!$failed || $generation <= $old_generation);
    }
    if (!$keep_failure) {
        make_path($dir);
        my ($out, $temporary) = tempfile(".launch-receipt.XXXXXX", DIR => $dir, UNLINK => 1);
        print {$out} encode_json($value), "\n" or die "receipt write: $!";
        close $out or die "receipt close: $!";
        rename $temporary, "$dir/launch_receipt.json" or die "receipt publish: $!";
    }
    1;
};
my $publication_error = $@;
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
                     (!ref($marker->{launch_generation}) && encode_json($marker->{launch_generation}) =~ /\A[1-9][0-9]{0,9}\z/ &&
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
' "$wrapper" "$exit_code" "$error_number" "$generation"
