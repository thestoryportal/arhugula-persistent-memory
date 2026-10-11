set -u
P=/opt/local/bin/port
echo "### date"; date -u
echo "### sw_vers"; sw_vers; uname -m
echo "### port version"; $P version
echo "### sources.conf (non-comment)"; grep -v '^#' /opt/local/etc/macports/sources.conf | grep -v '^\s*$'
echo "### sources.conf full lines w/ rsync/file/https"; grep -n -E 'rsync|file://|https?://' /opt/local/etc/macports/sources.conf
echo "### macports.conf non-comment"; grep -v '^#' /opt/local/etc/macports/macports.conf | grep -v '^\s*$'
echo "### ports tree dirs"; ls -la /opt/local/var/macports/sources/ 2>&1; ls -la /opt/local/var/macports/sources/*/ 2>&1 | head -30
echo "### tree mtime + PortIndex"; for d in /opt/local/var/macports/sources/*/*/ports /opt/local/var/macports/sources/*/*/*; do [ -e "$d" ] && echo "$d"; done 2>/dev/null | head; find /opt/local/var/macports/sources -maxdepth 5 -name 'PortIndex*' -exec ls -la {} \; 2>/dev/null
find /opt/local/var/macports/sources -maxdepth 5 -name 'PortIndex' -exec shasum -a 256 {} \; 2>/dev/null
find /opt/local/var/macports/sources -maxdepth 5 \( -name '.git' -o -name 'ChangeLog' -o -name '*.tar*' \) 2>/dev/null | head
echo "### port dir"; for p in python312 duckdb openjdk21 py312-pip; do echo "$p: $($P dir $p 2>&1)"; done
echo "### port info"; $P info --name --version --revision --variants --platforms --depends_build --depends_lib --depends_run python312 duckdb openjdk21 2>&1
echo "### python312 portfile version lines"; grep -n -E '^(version|revision|checksums|github.setup)|rmd160|sha256|size' "$($P dir python312)/Portfile" | head -20
echo "### rdeps python312"; $P rdeps python312 2>&1 | head -60
echo "### rdeps duckdb"; $P rdeps duckdb 2>&1 | head -40
echo "### rdeps openjdk21"; $P rdeps openjdk21 2>&1 | head -20
echo "### installed"; $P installed 2>&1 | head
echo "### neo4j search"; $P search --name neo4j 2>&1 | head; $P search cypher 2>&1 | head -5
echo "### disk"; df -k / /opt/local 2>&1
echo "### xcode-select"; xcode-select -p 2>&1
echo "### java"; /usr/libexec/java_home -V 2>&1 | head
