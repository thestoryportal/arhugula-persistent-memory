#!/bin/zsh
# Read-only: for each "port<TAB>archive" row with a size, stream the archive through bzip2 -dc | wc -c
# (uncompressed tar bytes ~ installed bytes; nothing is written to disk). Then HEAD + stream the Neo4j tarballs.
in=$1
while IFS=$'\t' read -r n a b; do
  [[ $b == NA ]] && continue
  u=$(curl -s --max-time 600 "https://packages.macports.org/$n/$a" | bzip2 -dc | wc -c | tr -d ' ')
  printf "%s\t%s\t%s\t%s\n" $n $a $b $u
done < $in
for v in 2026.09.0 5.26.32; do
  url=https://dist.neo4j.org/neo4j-community-$v-unix.tar.gz
  b=$(curl -sIL --max-time 30 $url | awk 'tolower($1)=="content-length:"{x=$2} END{print x}' | tr -d '\r')
  u=$(curl -sL --max-time 600 $url | gzip -dc | wc -c | tr -d ' ')
  printf "neo4j\t%s\t%s\t%s\n" ${url:t} ${b:-NA} $u
done
