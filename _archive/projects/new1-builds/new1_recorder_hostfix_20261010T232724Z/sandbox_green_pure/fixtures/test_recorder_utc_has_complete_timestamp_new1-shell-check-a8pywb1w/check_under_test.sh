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
    /bin/date -u -r "${now%.*}" '+%Y-%m-%dT%H:%M:%S' | /usr/bin/tr -d '\n'
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

utc
