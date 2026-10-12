#!/bin/zsh
# Run from the operator's process-visible, niceness-zero shell.
setopt NO_UNSET PIPE_FAIL
unsetopt BG_NICE
RECEIPT=${0:a:h}
ROOT=${RECEIPT:h:h:h}
if (( $# != 2 )) || [[ ! $1 =~ '^[A-Za-z0-9_-]+$' ]] || [[ $2 != red && $2 != green ]]; then
    print -u2 -- 'usage: run_tests.sh LABEL red|green'
    exit 3
fi
LABEL=$1
MODE=$2
RUN_DIR="$RECEIPT/$LABEL"
/bin/mkdir "$RUN_DIR" || exit 3
/bin/ps -o nice= -p $$ > "$RUN_DIR/nice.stdout" 2> "$RUN_DIR/nice.stderr"
nice_probe_rc=$?
own_nice=$(< "$RUN_DIR/nice.stdout")
own_nice=${own_nice//[[:space:]]/}
if (( nice_probe_rc != 0 )) || [[ $own_nice != 0 ]]; then
    print -r -- 'NOT RUN: runner requires observable own niceness exactly 0' > "$RUN_DIR/test.log"
    print -r -- '3' > "$RUN_DIR/exit_code.txt"
    /bin/cp "$RUN_DIR/nice.stderr" "$RUN_DIR/ps_before.stderr" || exit 3
    print -r -- 'NOT RUN: runner refused before suite' > "$RUN_DIR/ps_after.stderr"
    print -r -- "{\"suite_started\":false,\"nice_probe_exit\":$nice_probe_rc,\"process_clearance\":\"UNVERIFIED\"}" > "$RUN_DIR/refused.json"
    print -u2 -- "Runner refused (niceness $own_nice, probe exit $nice_probe_rc): $RUN_DIR"
    exit 3
fi
/bin/ps -axo pid=,ppid=,pgid=,nice=,command= > "$RUN_DIR/ps_before.log" 2> "$RUN_DIR/ps_before.stderr"
before_rc=$?
if (( before_rc != 0 )); then
    print -r -- 'NOT RUN: process snapshot failed' > "$RUN_DIR/test.log"
    print -r -- '3' > "$RUN_DIR/exit_code.txt"
    print -u2 -- "Before-suite process snapshot failed: $RUN_DIR"
    exit 3
fi
TEST_ROOT=$ROOT
if [[ $MODE == red ]]; then
    TEST_ROOT=$(/usr/bin/mktemp -d /private/tmp/new1-dispatch-red.XXXXXX) || exit 3
    /bin/mkdir "$TEST_ROOT/tests" "$TEST_ROOT/tools" || exit 3
    /bin/cp "$ROOT/tests/test_new1_dispatch.py" "$TEST_ROOT/tests/" || exit 3
    /bin/cp "$ROOT/tools/c10w_p2_gate.py" "$ROOT/tools/mathlab_events.py" "$TEST_ROOT/tools/" || exit 3
    # The test definitions contain the fake supervisor/worker/admission fixtures.
    # Both implementation files are absent; no worktree file is edited for RED.
    [[ ! -e "$TEST_ROOT/tools/new1_dispatch.sh" && ! -e "$TEST_ROOT/tools/new1_dispatch_report.py" ]] || exit 3
fi
LLMDB_ROOT="$TEST_ROOT" NEW1_TEST_NICE="$own_nice" /usr/bin/python3 -B "$RECEIPT/record_test_run.py" "$RUN_DIR" "$TEST_ROOT" "$MODE"
suite_rc=$?
/bin/ps -axo pid=,ppid=,pgid=,nice=,command= > "$RUN_DIR/ps_after.log" 2> "$RUN_DIR/ps_after.stderr"
after_rc=$?
print -r -- "{\"before_exit\":$before_rc,\"after_exit\":$after_rc,\"runner_pid\":$$,\"runner_nice\":0,\"fixture_cleanup_assertions\":\"see test.log\"}" > "$RUN_DIR/process_clearance.json"
runner_rc=$suite_rc
(( after_rc == 0 )) || runner_rc=3
print -r -- "$runner_rc" > "$RUN_DIR/runner_exit_code.txt"
print -r -- "$RUN_DIR"
exit "$runner_rc"
