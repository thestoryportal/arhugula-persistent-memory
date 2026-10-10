#!/bin/zsh
# External C1/C3 observation only. No Python is alive in this recorder's polling
# path. Supervisor ownership/reap: tools/new1_supervisor.py:313-352,443-487,597-627.
setopt NO_UNSET PIPE_FAIL EXTENDED_GLOB
unsetopt BG_NICE
zmodload zsh/datetime || exit 3
ROOT=$PWD
STAGING="$ROOT/results/mathlab_staging"
AUTH_LOCK=''
SUPERVISOR_PID=''
STOP_AT=0
CHECK_RC=0
CHECK_COMMAND=''

utc() {
    local now=$EPOCHREALTIME
    /usr/bin/date -u -r "${now%.*}" '+%Y-%m-%dT%H:%M:%S' | /usr/bin/tr -d '\n'
    print -rn -- ".${now#*.}Z"
}
json_string() {
    local value=$1 char escaped i
    value=${value//\\/\\\\}
    value=${value//\"/\\\"}
    for i in {1..31}; do
        printf -v char '%b' "\\$(printf '%03o' $i)"
        printf -v escaped '\\u%04x' $i
        value=${value//$char/$escaped}
    done
    print -rn -- "\"$value\""
}
json_array() {
    local item separator=''
    print -rn -- '['
    for item in "$@"; do
        print -rn -- "$separator"
        json_string "$item"
        separator=','
    done
    print -rn -- ']'
}
file_text() {
    REPLY=''
    IFS= read -r -d '' REPLY < "$1"
    local read_rc=$?
    # read returns 1 on normal EOF without a NUL delimiter; REPLY retains bytes.
    if (( read_rc > 1 )); then print -u2 -- "Cannot read $1"; return 3; fi
}
cleanup() {
    if [[ -n $AUTH_LOCK ]]; then
        /bin/rmdir "$AUTH_LOCK" || print -u2 -- "Authorization lock requires operator cleanup: $AUTH_LOCK"
    fi
}
trap cleanup EXIT

if (( $# != 3 )); then
    print -u2 -- 'usage: tools/new1_dispatch.sh HASHES EXPECTED_HEAD AUTHORIZATION_FILE'
    exit 3
fi
HASHES=${1:a}
EXPECTED_HEAD=$2
AUTHORIZATION=${3:a}
stamp=$(utc)
DISPATCH="$STAGING/new1_dispatch_${${stamp//-/}//:/}"
# Exclusive creation is check 2a; never write into an earlier dispatch directory.
/bin/mkdir "$DISPATCH" 2> /private/tmp/new1-dispatch-mkdir-$$.stderr
mkdir_rc=$?
if (( mkdir_rc != 0 )); then
    failure_dir="${DISPATCH}_refused_$$"
    if ! /bin/mkdir "$failure_dir"; then
        print -u2 -- "Cannot persist exclusive-directory refusal: $failure_dir"
        exit 3
    fi
    /bin/cp /private/tmp/new1-dispatch-mkdir-$$.stderr "$failure_dir/2a.stderr" || exit 3
    { print -rn -- '{"check":"2a","command":'; json_string "/bin/mkdir ${(q)DISPATCH}"
      print -rn -- ',"stdout":"","stderr":'; file_text "$failure_dir/2a.stderr"; json_string "$REPLY"
      print -r -- ",\"exit\":$mkdir_rc,\"authorization_consumed\":false}"; } > "$failure_dir/refused_before_invocation.json"
    exit 3
fi
/bin/mv /private/tmp/new1-dispatch-mkdir-$$.stderr "$DISPATCH/2a.stderr" || exit 3
print -r -- '{"check":"2a","exit":0,"stdout":"","stderr":""}' > "$DISPATCH/2a.json"

save_check() {
    local check_name=$1
    shift
    local -a check_argv=("$@")
    local command_text="${(j: :)${(q)check_argv}}"
    CHECK_COMMAND=$command_text
    "$@" > "$DISPATCH/$check_name.stdout" 2> "$DISPATCH/$check_name.stderr"
    CHECK_RC=$?
    { print -rn -- '{"check":'; json_string "$check_name"
      print -rn -- ',"command":'; json_string "$command_text"
      print -rn -- ',"argv":'; json_array "${check_argv[@]}"
      print -rn -- ',"stdout":'; file_text "$DISPATCH/$check_name.stdout"; json_string "$REPLY"
      print -rn -- ',"stderr":'; file_text "$DISPATCH/$check_name.stderr"; json_string "$REPLY"
      print -r -- ",\"exit\":$CHECK_RC}"; } > "$DISPATCH/$check_name.json" || exit 3
}
refuse() {
    local check_name=$1 reason=$2
    { print -rn -- '{"check":'; json_string "$check_name"
      print -rn -- ',"command":'; json_string "$CHECK_COMMAND"
      print -rn -- ',"stdout":'; file_text "$DISPATCH/$check_name.stdout"; json_string "$REPLY"
      print -rn -- ',"stderr":'; file_text "$DISPATCH/$check_name.stderr"; json_string "$REPLY"
      print -rn -- ',"reason":'; json_string "$reason"
      print -r -- ",\"exit\":$CHECK_RC,\"authorization_consumed\":false}"; } > "$DISPATCH/refused_before_invocation.json"
    print -u2 -- "$check_name refused: $reason; $DISPATCH"
    exit 3
}
require_success() {
    (( CHECK_RC == 0 )) || refuse "$1" 'command failed'
}
{ print -rn -- '{"check":"2a","command":'; json_string "/bin/mkdir ${(q)DISPATCH}"
  print -rn -- ',"argv":'; json_array /bin/mkdir "$DISPATCH"
  print -r -- ',"stdout":"","stderr":"","exit":0}'; } > "$DISPATCH/2a.json"
: > "$DISPATCH/2a.stdout"

# 2b: serialize equal authorization digests, then scan consumed invocations.
save_check 2b /usr/bin/shasum -a 256 "$AUTHORIZATION"
require_success 2b
file_text "$DISPATCH/2b.stdout"
AUTH_SHA=${REPLY%% *}
[[ $AUTH_SHA =~ '^[0-9a-f]{64}$' ]] || refuse 2b 'invalid authorization SHA-256'
candidate_lock="$STAGING/.new1_authorization_${AUTH_SHA}.lock"
save_check 2b_lock /bin/mkdir "$candidate_lock"
require_success 2b_lock
AUTH_LOCK=$candidate_lock
for previous in "$STAGING"/new1_dispatch_*/invocation.json(N); do
    save_check "2b_prior_${${previous:h}:t}" /usr/bin/plutil -extract authorization.sha256 raw -o - "$previous"
    require_success "2b_prior_${${previous:h}:t}"
    file_text "$DISPATCH/2b_prior_${${previous:h}:t}.stdout"
    previous_sha=${REPLY//$'\n'/}
    [[ $previous_sha =~ '^[0-9a-f]{64}$' ]] || refuse "2b_prior_${${previous:h}:t}" 'invalid prior authorization digest'
    [[ $previous_sha != $AUTH_SHA ]] || refuse "2b_prior_${${previous:h}:t}" 'authorization already consumed'
done

# 2c: exact HEAD and clean paths from the shasum-format manifest.
save_check 2c_head git rev-parse HEAD
require_success 2c_head
file_text "$DISPATCH/2c_head.stdout"
[[ ${REPLY//$'\n'/} == $EXPECTED_HEAD ]] || refuse 2c_head 'HEAD mismatch'
save_check 2c_manifest /bin/cat "$HASHES"
require_success 2c_manifest
typeset -a pinned_paths=()
while IFS= read -r manifest_line || [[ -n $manifest_line ]]; do
    if [[ $manifest_line =~ '^[0-9a-fA-F]{64}[ ][ *](.+)$' ]]; then
        pinned_file=$match[1]
        [[ $pinned_file != /* && $pinned_file != ../* && $pinned_file != */../* && $pinned_file != *$'\n'* ]] || refuse 2c_manifest 'manifest path must stay under ROOT'
        pinned_paths+=("$pinned_file")
    else
        refuse 2c_manifest 'invalid shasum-format manifest line'
    fi
done < "$HASHES"
(( ${#pinned_paths} > 0 )) || refuse 2c_manifest 'empty manifest'
save_check 2c_status git status --porcelain -- "${pinned_paths[@]}"
require_success 2c_status
file_text "$DISPATCH/2c_status.stdout"
[[ -z $REPLY ]] || refuse 2c_status 'pinned paths have working-tree changes'

save_check 2d /usr/bin/shasum -a 256 -c "$HASHES"
require_success 2d

# Absolute worker nice 10 requires this exact own-niceness check (supervisor:640).
save_check 2e /bin/ps -o nice= -p $$
require_success 2e
file_text "$DISPATCH/2e.stdout"
recorder_nice=${REPLY//[[:space:]]/}
[[ $recorder_nice == 0 ]] || refuse 2e 'recorder niceness must be 0'
print -r -- "{\"pid\":$$,\"nice\":0}" > "$DISPATCH/recorder.json"

save_check 2f /bin/df -k "$ROOT"
require_success 2f
file_text "$DISPATCH/2f.stdout"
typeset -a df_rows=("${(@f)REPLY}") df_fields=( ${=df_rows[-1]} )
available_kib=${df_fields[4]:-invalid}
floor_kib=${NEW1_DISPATCH_MIN_FREE_KIB:-22020096}
[[ $floor_kib =~ '^[0-9]{1,18}$' && $available_kib =~ '^[0-9]+$' ]] || refuse 2f 'invalid free-space floor or df observation'
(( floor_kib >= 22020096 )) || refuse 2f 'free-space floor may only be raised'
(( available_kib >= floor_kib )) || refuse 2f 'less than the required free space'
print -r -- "{\"available_kib\":$available_kib,\"minimum_kib\":$floor_kib,\"projected_write_allowance_gib\":1}" > "$DISPATCH/disk.json"

save_check 2g /usr/bin/env "LLMDB_ROOT=$ROOT" /usr/bin/python3 tools/engine_fingerprint.py
require_success 2g
DRY_PROBE='import sys;sys.path.insert(0,".");from tools import mathlab_admit as A;d=A.probe("cpu");print(d["allowed"],d["reasons"],d["checks"]["gpu"].get("blocking_processes"));sys.exit(0 if d["allowed"] else 1)'
save_check 2h /usr/bin/env "LLMDB_ROOT=$ROOT" "$ROOT/.venv/bin/python" -B -c "$DRY_PROBE"
require_success 2h
file_text "$DISPATCH/2h.stdout"
[[ $REPLY == 'True '* ]] || refuse 2h 'dry probe did not print allowed True'

typeset -a namespaces_before=("$ROOT"/results/mathlab_staging/runs/new1_*(N/))
json_array "${namespaces_before[@]}" > "$DISPATCH/namespaces_before.json"
typeset -a invocation_argv=("$PWD/.venv/bin/python" -B "$PWD/tools/new1_supervisor.py" --prereg-sha 1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f)
typeset -a env_assignments=(PATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin TMPDIR=/private/tmp "LLMDB_ROOT=$PWD" LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1)
save_check 2i /usr/bin/shasum -a 256 -c "$HASHES"
require_success 2i
# This file is the consumption boundary, even if admission later refuses (:519).
setopt NO_CLOBBER
{ print -rn -- '{"utc":'; json_string "$(utc)"
  print -rn -- ',"authorization":{"path":'; json_string "$AUTHORIZATION"
  print -rn -- ',"sha256":'; json_string "$AUTH_SHA"
  print -rn -- '},"cwd":'; json_string "$ROOT"
  print -rn -- ',"argv":'; json_array "${invocation_argv[@]}"
  print -rn -- ',"command_argv":'; json_array /usr/bin/env "${env_assignments[@]}" "${invocation_argv[@]}"
  print -rn -- ',"env":{'
  separator=''
  for assignment in "${env_assignments[@]}"; do
      print -rn -- "$separator"; json_string "${assignment%%=*}"; print -rn -- ':'; json_string "${assignment#*=}"; separator=','
  done
  print -r -- '},"inherits_other_environment":true}'; } > "$DISPATCH/invocation.json" || exit 3
unsetopt NO_CLOBBER

# Restore a caught SIGINT before exec: asynchronous shells can otherwise inherit
# SIG_IGN. Exec resets this caught handler to default; Python uses KeyboardInterrupt.
# Supervisor's exception routing/reap is :443-487,597-627, not recorder group kills.
(
    trap ':' INT
    exec /usr/bin/env PATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin \
      TMPDIR=/private/tmp LLMDB_ROOT="$PWD" \
      LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= \
      OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 \
      "$PWD/.venv/bin/python" -B "$PWD/tools/new1_supervisor.py" \
      --prereg-sha 1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f
) > "$DISPATCH/supervisor_stdout.log" 2> "$DISPATCH/supervisor_stderr.log" < /dev/null &
SUPERVISOR_PID=$!
supervisor_alive() { kill -0 "$SUPERVISOR_PID" 2> "$DISPATCH/liveness.stderr"; }
request_stop() {
    [[ -f "$DISPATCH/stop.json" ]] && return
    local reason=$1
    STOP_AT=$EPOCHSECONDS
    kill -INT "$SUPERVISOR_PID" 2> "$DISPATCH/sigint.stderr"
    local signal_rc=$?
    { print -rn -- '{"reason":'; json_string "$reason"
      print -rn -- ',"utc":'; json_string "$(utc)"
      print -r -- ",\"signal\":\"SIGINT\",\"target_pid\":$SUPERVISOR_PID,\"exit\":$signal_rc}"; } > "$DISPATCH/stop.json"
}
/bin/ps -o nice= -p "$SUPERVISOR_PID" > "$DISPATCH/supervisor_nice.stdout" 2> "$DISPATCH/supervisor_nice.stderr"
supervisor_nice_rc=$?
file_text "$DISPATCH/supervisor_nice.stdout"
supervisor_nice=${REPLY//[[:space:]]/}
[[ $supervisor_nice =~ '^-?[0-9]+$' ]] || supervisor_nice=null
print -r -- "{\"pid\":$SUPERVISOR_PID,\"nice\":$supervisor_nice,\"nice_probe_exit\":$supervisor_nice_rc}" > "$DISPATCH/supervisor.json"
if (( supervisor_nice_rc != 0 )) && supervisor_alive; then request_stop 'PROCESS-OBSERVATION-UNAVAILABLE'; fi

worker_pid=''
worker_pgid=''
while supervisor_alive; do
    /bin/ps -axo pid=,ppid=,pgid=,nice=,command= > "$DISPATCH/process_inventory.last" 2> "$DISPATCH/process_inventory.stderr"
    inventory_rc=$?
    if (( inventory_rc != 0 )) && supervisor_alive; then
        request_stop 'PROCESS-OBSERVATION-UNAVAILABLE'
    elif [[ -z $worker_pid ]]; then
        worker_line=$(/usr/bin/awk -v parent="$SUPERVISOR_PID" '
            $2 == parent {
                cmd=$0; sub(/^[[:space:]]*[0-9]+[[:space:]]+[0-9]+[[:space:]]+[0-9]+[[:space:]]+[-0-9]+[[:space:]]+/, "", cmd)
                split(cmd, argv, " "); count=split(argv[1], components, "/"); exe=tolower(components[count])
                if (exe ~ /^python[0-9.]*$/ && index(cmd, "tools/new1_geometry.py")) { print $0; exit }
            }' "$DISPATCH/process_inventory.last")
        if [[ -n $worker_line ]]; then
            read -r worker_pid worker_ppid worker_pgid worker_nice worker_command <<< "$worker_line"
            /bin/cp "$DISPATCH/process_inventory.last" "$DISPATCH/worker_observation.ps" || exit 3
            { print -rn -- "{\"status\":\"OBSERVED\",\"pid\":$worker_pid,\"ppid\":$worker_ppid,\"pgid\":$worker_pgid,\"nice\":$worker_nice,\"command\":"
              json_string "$worker_command"; print -rn -- ',"observed_at_utc":'; json_string "$(utc)"; print -r -- '}'; } > "$DISPATCH/worker.json"
            [[ $worker_nice == 10 ]] || request_stop 'WORKER-NICENESS-MISMATCH'
        fi
    fi
    if (( STOP_AT > 0 && EPOCHSECONDS - STOP_AT >= 60 )) && supervisor_alive; then
        print -r -- "{\"exited\":false,\"status\":null,\"pid\":$SUPERVISOR_PID,\"stop_wait_seconds\":60}" > "$DISPATCH/supervisor_exit.json"
        print -r -- "{\"authorization_consumed\":true,\"verdict_status\":\"INCOMPLETE\",\"prediction_verdict\":\"no prediction verdict\",\"supervisor_alive_pid\":$SUPERVISOR_PID,\"subsequent_compute_blocked\":true,\"operator_message\":\"supervisor did not exit within 60 seconds of SIGINT; operator resolution required\"}" > "$DISPATCH/dispatch_receipt.json"
        print -u2 -- "Supervisor $SUPERVISOR_PID still alive after 60 seconds; $DISPATCH"
        exit 3
    fi
    /bin/sleep .1
done
wait "$SUPERVISOR_PID"
supervisor_exit_rc=$?
{ print -rn -- "{\"exited\":true,\"status\":$supervisor_exit_rc,\"ended_at_utc\":"; json_string "$(utc)"; print -r -- '}'; } > "$DISPATCH/supervisor_exit.json"
if [[ ! -f "$DISPATCH/worker.json" ]]; then print -r -- '{"status":"NONE_OBSERVED","description":"worker: none observed"}' > "$DISPATCH/worker.json"; fi
typeset -a namespaces_after=("$ROOT"/results/mathlab_staging/runs/new1_*(N/)) new_namespaces=()
for namespace_path in "${namespaces_after[@]}"; do
    (( ${namespaces_before[(Ie)$namespace_path]} == 0 )) && new_namespaces+=("$namespace_path")
done
{ print -rn -- '{"path":'
  if (( ${#new_namespaces} == 1 )); then json_string "$new_namespaces[1]"; else print -rn -- 'null'; fi
  print -rn -- ',"candidates":'; json_array "${new_namespaces[@]}"
  print -rn -- ',"anomaly":'
  if (( ${#new_namespaces} == 1 )); then print -rn -- 'null'; else json_string "${#new_namespaces} new namespaces observed"; fi
  print -r -- '}'; } > "$DISPATCH/namespace.json"
/bin/ps -axo pid=,ppid=,pgid=,nice=,command= > "$DISPATCH/post_exit.ps" 2> "$DISPATCH/post_exit.stderr"
post_exit_rc=$?
typeset -a live_rows=()
disposition_status=NO_WORKER_OBSERVED
if (( post_exit_rc != 0 )); then
    disposition_status=UNAVAILABLE
elif [[ -n $worker_pid ]]; then
    group_rows=$(/usr/bin/awk -v worker="$worker_pid" -v group="$worker_pgid" '$1 == worker || $3 == group {print}' "$DISPATCH/post_exit.ps")
    [[ -z $group_rows ]] || live_rows=("${(@f)group_rows}")
    disposition_status=CLEAN
    (( ${#live_rows} == 0 )) || disposition_status=UNREAPED
fi
{ print -rn -- '{"status":'; json_string "$disposition_status"
  print -rn -- ',"live_processes":'; json_array "${live_rows[@]}"
  print -r -- ",\"ps_exit\":$post_exit_rc}"; } > "$DISPATCH/disposition.json"
# All supervisor waits have completed; Python is safe only from this point.
LLMDB_ROOT="$ROOT" /usr/bin/python3 -B "$ROOT/tools/new1_dispatch_report.py" "$DISPATCH" > "$DISPATCH/reporter_stdout.log" 2> "$DISPATCH/reporter_stderr.log"
reporter_rc=$?
print -r -- "$DISPATCH"
(( reporter_rc == 0 )) || exit 3
[[ ! -f "$DISPATCH/stop.json" && $disposition_status != UNREAPED && $disposition_status != UNAVAILABLE ]] || exit 3
exit "$supervisor_exit_rc"
