#!/bin/bash
# External setup-through-cleanup deadline; no Python monitor competes with the GPU gate.
set -eu
SECONDS=0
CAP_SECONDS=2820
CLEANUP_RESERVE=10
INTERRUPTION=''
on_signal() { INTERRUPTION=$1;exit 2; }
trap 'on_signal TERM' TERM
trap 'on_signal INT' INT
trap 'on_signal HUP' HUP
# Noninteractive Bash cannot trap a signal inherited as SIG_IGN.
for REQUIRED_SIGNAL in TERM INT HUP; do
    case "$(trap -p "$REQUIRED_SIGNAL")" in
        *"'on_signal $REQUIRED_SIGNAL'"*) ;;
        *) echo "INCONCLUSIVE: SIGNAL-TRAP-UNAVAILABLE $REQUIRED_SIGNAL; phases NOT-RUN; no owned child launched." >&2
           exit 3 ;;
    esac
done
if [[ $# != 2 || $1 != --utc || ! $2 =~ ^[0-9]{8}T[0-9]{6}(\.[0-9]{6})?Z$ ]]; then
    echo 'usage: run_c10y_precast_diag.sh --utc YYYYMMDDTHHMMSS[.ffffff]Z' >&2
    exit 3
fi
UTC=$2
W=$(cd "$(dirname "$0")/../../.." && pwd -P)
OUT="$W/experiments/c10y/runs/c10y_precast_diag/$UTC"
PY="$W/.venv/bin/python"
DRIVER="$W/code/lab/track_c/c10y_precast_diag.py"
export LLMDB_ROOT="$W" C10Y_PRECAST_SUPERVISOR=$$ PYTHONDONTWRITEBYTECODE=1
CONTROL=$(mktemp -d /private/tmp/c10y_precast_deadline.XXXXXXXX)
export PYTHONPYCACHEPREFIX="$CONTROL/unused-bytecode"
PARENT_PID=$$
CHILD=''
REAPED_CHILD=''
TIMER_PID=''
FINALIZED=0
PREPARE_STARTED=0
stop_owned() {
    WORKER_SIGNALED=0
    WORKER_PID=''
    if [[ -s "$CONTROL/worker" ]]; then
        read -r WORKER_PID < "$CONTROL/worker"
        # The group can outlive its leader. Never gate group termination on the leader PID.
        if kill -0 -- -"$WORKER_PID"; then
            if kill -"$1" -- -"$WORKER_PID"; then WORKER_SIGNALED=1;else echo 'Owned worker group already exited.' >&2; fi
        elif kill -0 "$WORKER_PID"; then
            if kill -"$1" "$WORKER_PID"; then WORKER_SIGNALED=1;else echo 'Owned worker exited before setsid.' >&2; fi
        fi
    fi
    if [[ -s "$CONTROL/child" ]]; then
        read -r OWNED_PID < "$CONTROL/child"
        if [[ "$OWNED_PID" != "$WORKER_PID" || "$WORKER_SIGNALED" == 0 ]] && kill -0 "$OWNED_PID"; then
            if ! kill -"$1" "$OWNED_PID"; then echo 'Owned child already exited.' >&2; fi
        fi
    fi
}
owned_live() {
    if [[ -s "$CONTROL/worker" ]]; then
        read -r WORKER_PID < "$CONTROL/worker"
        if kill -0 -- -"$WORKER_PID"; then return 0; fi
    fi
    if [[ -s "$CONTROL/child" ]]; then
        read -r OWNED_PID < "$CONTROL/child"
        if kill -0 "$OWNED_PID"; then return 0; fi
    fi
    return 1
}
cleanup_owned() {
    stop_owned TERM
    CLEANUP_STARTED=$SECONDS
    while owned_live && ((SECONDS-CLEANUP_STARTED<2)); do sleep 0.05; done
    if owned_live; then stop_owned KILL; fi
    if [[ -n "$CHILD" && "$REAPED_CHILD" != "$CHILD" ]]; then
        if wait "$CHILD"; then CLEANUP_RC=0; else CLEANUP_RC=$?; fi
        REAPED_CHILD=$CHILD
    fi
}
finish_timer() {
    if [[ -n "$TIMER_PID" ]]; then
        if kill -0 "$TIMER_PID"; then
            if ! kill -TERM "$TIMER_PID"; then echo 'Deadline timer already exited.' >&2; fi
        fi
        if wait "$TIMER_PID"; then TIMER_STATUS=0; else TIMER_STATUS=$?; fi
    fi
    # Preserve control/timeout/PID files; never delete committed diagnostic evidence.
}
publish_timeout() {
    if [[ ! -e "$OUT/supervisor_timeout.json" ]]; then
        "$PY" -B "$DRIVER" --utc "$UTC" --timeout-record --returncode "$1" --elapsed-s "$SECONDS" &
        CHILD=$!;printf '%s\n' "$CHILD" > "$CONTROL/child"
        if wait "$CHILD"; then NOTE_RC=0; else NOTE_RC=$?; fi
        REAPED_CHILD=$CHILD
        if [[ "$NOTE_RC" != 2 ]]; then echo 'Supervisor timeout publication failed; retained control evidence remains authoritative.' >&2; fi
    fi
}
closeout() {
    EXIT_RC=$?
    trap - EXIT
    trap '' TERM INT HUP
    cleanup_owned
    if [[ "$PREPARE_STARTED" == 1 ]] && [[ -n "$INTERRUPTION" || "$FINALIZED" == 0 ]] && [[ -e "$OUT/launch.json" ]]; then
        if [[ -z "$INTERRUPTION" ]]; then INTERRUPTION=ABNORMAL_EXIT; fi
        "$PY" -B "$DRIVER" --utc "$UTC" --interrupted --reason "$INTERRUPTION" --returncode "$EXIT_RC" --elapsed-s "$SECONDS" &
        CHILD=$!;printf '%s\n' "$CHILD" > "$CONTROL/child"
        if wait "$CHILD"; then NOTE_RC=0; else NOTE_RC=$?; fi
        REAPED_CHILD=$CHILD
        if [[ "$NOTE_RC" != 2 ]]; then echo 'Supervisor interruption publication failed; retained control evidence remains authoritative.' >&2; fi
        cleanup_owned
        if [[ -e "$CONTROL/timeout" && "$NOTE_RC" != 2 ]]; then publish_timeout "$NOTE_RC";cleanup_owned;fi
        EXIT_RC=2
    fi
    # The deadline covers termination, reaping and terminal publication. Cancel it last.
    finish_timer
    exit "$EXIT_RC"
}
trap closeout EXIT
finalize_owned() {
    cleanup_owned
    if [[ -e "$CONTROL/timeout" ]]; then
        "$PY" -B "$DRIVER" --utc "$UTC" --finalize --returncode "$1" --elapsed-s "$SECONDS" --timed-out &
    else
        "$PY" -B "$DRIVER" --utc "$UTC" --finalize --returncode "$1" --elapsed-s "$SECONDS" &
    fi
    CHILD=$!;printf '%s\n' "$CHILD" > "$CONTROL/child"
    if wait "$CHILD"; then FINAL_RC=0; else FINAL_RC=$?; fi
    REAPED_CHILD=$CHILD
    if [[ -e "$CONTROL/timeout" ]]; then
        publish_timeout "$FINAL_RC"
        if [[ -e "$OUT/run.json" || -e "$OUT/timeout_run.json" ]] && [[ "$FINAL_RC" == 2 || "${NOTE_RC:-1}" == 2 ]]; then FINALIZED=1; fi
        exit 2
    fi
    if [[ -e "$OUT/run.json" ]] && [[ "$FINAL_RC" == 0 || "$FINAL_RC" == 2 ]]; then FINALIZED=1; fi
    if [[ "$FINAL_RC" == 0 ]]; then exit 0; else exit 2; fi
}
(
    SLEEP_PID=''
    stop_sleep() {
        if [[ -n "$SLEEP_PID" ]]; then
            if ! kill -TERM "$SLEEP_PID"; then echo 'Deadline sleep already exited.' >&2; fi
            if wait "$SLEEP_PID"; then SLEEP_STATUS=0; else SLEEP_STATUS=$?; fi
        fi
    }
    trap 'stop_sleep; exit 0' TERM
    sleep_owned() { sleep "$1" & SLEEP_PID=$!; wait "$SLEEP_PID"; SLEEP_PID=''; }
    sleep_owned "$((CAP_SECONDS-CLEANUP_RESERVE-SECONDS))"
    : > "$CONTROL/timeout"
    stop_owned TERM
    sleep_owned 2
    stop_owned KILL
    sleep_owned "$((CLEANUP_RESERVE-2))"
    stop_owned KILL
    kill -KILL "$PARENT_PID"
) &
TIMER_PID=$!
if [[ -e "$OUT" || -L "$OUT" ]]; then
    echo 'Existing diagnostic namespace refused before imports.' >&2
    exit 3
fi
PREPARE_STARTED=1
"$PY" -B "$DRIVER" --utc "$UTC" --prepare &
CHILD=$!;printf '%s\n' "$CHILD" > "$CONTROL/child"
if wait "$CHILD"; then PREPARED=1;REAPED_CHILD=$CHILD; else
    RC=$?
    REAPED_CHILD=$CHILD
    if [[ -e "$OUT/launch.json" ]]; then finalize_owned "$RC"; fi
    exit 3
fi
if [[ -e "$CONTROL/timeout" ]]; then
    finalize_owned 124
fi
set -C
"$PY" -B "$DRIVER" --utc "$UTC" --worker > "$OUT/worker.log" 2>&1 &
CHILD=$!
set +C
printf '%s\n' "$CHILD" > "$CONTROL/child"
printf '%s\n' "$CHILD" > "$CONTROL/worker"
# setsid is performed by the owned worker; negative-PID kills never target the caller's group.
while kill -0 "$CHILD" && [[ ! -e "$OUT/worker_started.json" ]]; do sleep 0.05; done
if [[ -e "$OUT/worker_started.json" ]]; then : > "$CONTROL/session"; fi
if wait "$CHILD"; then RC=0; else RC=$?; fi
REAPED_CHILD=$CHILD
finalize_owned "$RC"
