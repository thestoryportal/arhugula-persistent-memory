#!/bin/bash
# M3-side only. Prospective remote commands; separate Intel clearance required.
set -euo pipefail
set -C
umask 077
RE=results/research_engine_phase1_20261011
runtime=/Library/Developer/CommandLineTools/usr/bin/python3
runtime_command="/Library/Developer/CommandLineTools/usr/bin/python3 -I -B"
mode=${1:?supply probe, bind or inventory}
shift
target=robertrhu_node2@192.168.10.2
maker="$RE/r1f_make_bundle.py"
case "$mode" in
    probe|bind)
        prefix=${1:?supply a new M3 RE capture prefix}
        shift
        case "$prefix" in "$RE/"*) ;; *) echo 'REFUSED: capture must be in RE' >&2; exit 1;; esac
        case "$prefix" in *..*|*/.*) echo 'REFUSED: unsafe capture prefix' >&2; exit 1;; esac
        args=("$mode")
        if [[ "$mode" == bind ]]; then
            probe=${1:?supply the direct-runtime probe JSON}
            shift
            # Starts before opening the first bootstrap output on either Mac.
            bootstrap_start_utc=$(/bin/date -u +%Y-%m-%dT%H:%M:%SZ)
            args+=(--probe "$probe" --bootstrap-start-utc "$bootstrap_start_utc")
        fi
        [[ $# == 0 ]] || { echo 'REFUSED: extra arguments' >&2; exit 1; }
        remote_command=$("$runtime" -I -B "$maker" "${args[@]}" --remote-command)
        # Reserve all three names with no-clobber before starting the stream.
        exec 3>"$prefix.json"
        exec 4>"$prefix.stderr"
        exec 5>"$prefix.exit"
        set +e
        "$runtime" -I -B "$maker" "${args[@]}" | ssh -T -o BatchMode=yes "$target" "$remote_command" >&3 2>&4
        statuses=("${PIPESTATUS[@]}")
        set -e
        rc=${statuses[1]}
        if [[ ${statuses[0]} != 0 ]]; then rc=${statuses[0]}; fi
        printf '%s\n' "$rc" >&5
        exec 3>&- 4>&- 5>&-
        [[ "$rc" == 0 ]] || { echo "REFUSED: stream failed exit=$rc" >&2; exit "$rc"; }
        # Hash the complete publication, including its receipt, on the trusted M3.
        digest=$("$runtime" -I -B -c 'import hashlib,json,sys; b=open(sys.argv[1], "rb").read(); v=json.loads(b); assert isinstance(v,dict) and v; print(hashlib.sha256(b).hexdigest())' "$prefix.json")
        printf 'R1F-CAPTURE %s %s\n' "$prefix.json" "$digest"
        ;;
    inventory)
        [[ $# == 4 || $# == 5 ]] || { echo 'REFUSED: inventory CAPTURE TRUSTED_HASH EXACT_ANCHOR BOOTSTRAP_BYTES [EVIDENCE_UPDATE]' >&2; exit 1; }
        args=(inventory --capture "$1" --expected-capture-sha256 "$2" --expected-anchor "$3" --bootstrap-bytes "$4")
        if [[ $# == 5 ]]; then args+=(--evidence-update "$5"); fi
        remote_command=$("$runtime" -I -B "$maker" "${args[@]}" --remote-command)
        # No M3 inventory files: stdout/stderr stay on the operator's terminal.
        "$runtime" -I -B "$maker" "${args[@]}" | ssh -T -o BatchMode=yes "$target" "$remote_command"
        ;;
    *) echo 'REFUSED: unadmitted wrapper mode' >&2; exit 1;;
esac
