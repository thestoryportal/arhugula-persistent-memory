#!/bin/zsh
# Read-only: show the newest darwin_23 / noarch archive names listed for each named port.
for n in $@; do
  echo "== $n"
  curl -s --max-time 20 "https://packages.macports.org/$n/" | grep -oE "\"$n-[^\"]*\.tbz2\"" | tr -d '"' | sort -u | grep -E 'darwin_23|noarch|darwin_any' | tail -3
done
