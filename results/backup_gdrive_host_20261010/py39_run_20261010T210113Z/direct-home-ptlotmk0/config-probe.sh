#!/bin/sh
[ "$#" = 2 ] && [ "$1" = config ] && [ "$2" = dump ] || exit 43
printf '%s\n' "$*" >> "$PY39_PROBE_LOG"
printf '%s\n' '{"fixture":{"type":"local"}}'
