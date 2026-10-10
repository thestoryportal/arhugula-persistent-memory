from pathlib import Path
import json, re
p=Path('tools/launchd/MemitGdriveBackup.applescript')
s=p.read_text()
literals={name:json.loads(value) for name,value in re.findall(r'^property (\w+) : ("(?:\\.|[^"\\])*")$',s,re.M)}
helpers=r'''
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
'''
g=literals['generationShell']
g=g.replace('my $previous = int($text);','my $previous = int($text);\n'+helpers+'\nmy ($completed, $refused) = (0, 0);',1)
needle='''            !ref($generation) && encode_json($generation) =~ /\A[1-9][0-9]{0,9}\z/ && $generation <= $previous;'''
assert g.count(needle)==1
g=g.replace(needle,needle+r'''
        if ($file =~ /last_run\.json\z/ && defined $value->{end} && defined $value->{exit_code} &&
                ($value->{launch_mode} // "applet") eq "applet" &&
                encode_json($value->{exit_code}) =~ /\A(?:0|[1-9][0-9]{0,2})\z/ && $value->{exit_code} <= 255) {
            $completed = $generation;
        }
        if ($file =~ /launch_receipt\.json\z/ &&
                ((defined $value->{exit_code} && $value->{exit_code} == 75) ||
                 (defined $value->{error_number} && $value->{error_number} == 75))) { $refused = $generation; }
''',1)
g=g.replace('my $generation = $previous + 1;',r'''my $state = read_state($dir, $previous, $completed);
resolve_state($state, $completed, $refused);
my $generation = $previous + 1;
$state->{issued_generation} = $generation;
if (@{$state->{unresolved}} && $state->{unresolved}[-1][1] == $previous) {
    $state->{unresolved}[-1][1] = $generation;
} else { push @{$state->{unresolved}}, [$generation, $generation]; }
# Publish issued evidence first: interruption between renames refuses allocation.
publish_state($dir, $state);''',1)
literals['generationShell']=g
r=literals['receiptShell']
r=r.replace('my ($sec, $micro) = gettimeofday();',helpers+'\nmy ($sec, $micro) = gettimeofday();',1)
needle='''        flock($state_lock, LOCK_EX) or die "receipt generation lock: $!";'''
assert r.count(needle)==1
r=r.replace(needle,needle+r'''
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
''',1)
literals['receiptShell']=r
for name in ('generationShell','receiptShell'):
    s=re.sub(r'^property '+name+r' : ("(?:\\.|[^"\\])*")$',lambda m:'property '+name+' : '+json.dumps(literals[name]),s,flags=re.M)
p.write_text(s)
print('Applet unresolved-generation allocation and per-generation refusal discharge written.')
