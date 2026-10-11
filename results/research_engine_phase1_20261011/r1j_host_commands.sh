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
maker="$RE/r1j_make_bundle.py"
case "$mode" in
    probe|bind)
        prefix=${1:?supply a new M3 RE capture prefix}
        shift
        case "$prefix" in "$RE/"*) ;; *) echo 'REFUSED: capture must be in RE' >&2; exit 1;; esac
        case "$prefix" in *..*|*/.*) echo 'REFUSED: unsafe capture prefix' >&2; exit 1;; esac
        args=("$mode" --dispatch-m3 --capture-prefix "$prefix")
        if [[ "$mode" == bind ]]; then
            probe=${1:?supply the direct-runtime probe JSON}
            shift
            # M3 starts before the first bootstrap capture file is opened.
            bootstrap_start_utc=$(/bin/date -u +%Y-%m-%dT%H:%M:%SZ)
            args+=(--probe "$probe" --bootstrap-start-utc "$bootstrap_start_utc")
        fi
        [[ $# == 0 ]] || { echo 'REFUSED: extra arguments' >&2; exit 1; }
        "$runtime" -I -B "$maker" "${args[@]}" --ssh-argv ssh -T -i ~/.ssh/intel_mac_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes "$target"
        ;;
    inventory)
        [[ $# == 4 || $# == 5 ]] || { echo 'REFUSED: inventory CAPTURE TRUSTED_HASH EXACT_ANCHOR BOOTSTRAP_BYTES [EVIDENCE_UPDATE]' >&2; exit 1; }
        args=(inventory --dispatch-m3 --capture "$1" --expected-capture-sha256 "$2" --expected-anchor "$3" --bootstrap-bytes "$4")
        if [[ $# == 5 ]]; then args+=(--evidence-update "$5"); fi
        # Dispatcher checks committed authority and consumes the anchor before ssh.
        "$runtime" -I -B "$maker" "${args[@]}" --ssh-argv ssh -T -i ~/.ssh/intel_mac_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes "$target"
        ;;
    *) echo 'REFUSED: unadmitted wrapper mode' >&2; exit 1;;
esac
