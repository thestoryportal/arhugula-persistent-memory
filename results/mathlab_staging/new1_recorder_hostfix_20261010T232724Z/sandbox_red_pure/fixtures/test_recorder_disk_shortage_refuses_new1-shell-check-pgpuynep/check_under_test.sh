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

DISPATCH="$PWD/dispatch"
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

save_check 2f /bin/cat "$PWD/df_fixture.txt"
require_success 2f
file_text "$DISPATCH/2f.stdout"
typeset -a df_rows=("${(@f)REPLY}") df_fields=( ${=df_rows[-1]} )
available_kib=${df_fields[4]:-invalid}
floor_kib=${NEW1_DISPATCH_MIN_FREE_KIB:-22020096}
[[ $floor_kib =~ '^[0-9]{1,18}$' && $available_kib =~ '^[0-9]+$' ]] || refuse 2f 'invalid free-space floor or df observation'
(( floor_kib >= 22020096 )) || refuse 2f 'free-space floor may only be raised'
(( available_kib >= floor_kib )) || refuse 2f 'less than the required free space'
print -r -- "{\"available_kib\":$available_kib,\"minimum_kib\":$floor_kib,\"projected_write_allowance_gib\":1}" > "$DISPATCH/disk.json"
