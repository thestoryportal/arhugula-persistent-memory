#!/bin/zsh
# Read-only: list each runtime-closure port's darwin_23 x86_64 (or noarch) binary archive on packages.macports.org and HEAD its size.
# Input: lines "name version<TAB>revision". Output TSV: name, archive, bytes.
in=$1
while IFS=$'\t' read -r nv rev; do
  n=${nv%% *}; v=${nv#* }
  listing=$(curl -s --max-time 20 "https://packages.macports.org/$n/")
  arcs=(${(f)"$(print -r -- $listing | grep -oE "\"$n-${v}_${rev}[^\"]*\.darwin_(23\.x86_64|any\.noarch)\.tbz2\"" | tr -d '"' | sort -u)"})
  if (( ${#arcs} == 0 )) || [[ -z ${arcs[1]} ]]; then printf "%s\t%s\t%s\n" $n "NO_ARCHIVE(${v}_${rev})" NA; continue; fi
  for a in $arcs; do
    s=$(curl -sI --max-time 20 "https://packages.macports.org/$n/$a" | awk 'tolower($1)=="content-length:"{print $2}' | tr -d '\r')
    printf "%s\t%s\t%s\n" $n $a ${s:-NA}
  done
done < $in
