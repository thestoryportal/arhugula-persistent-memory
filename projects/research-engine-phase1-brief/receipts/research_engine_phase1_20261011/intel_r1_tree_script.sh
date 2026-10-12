T=/opt/local/var/macports/sources/rsync.macports.org/macports/release/tarballs
ls -la $T; ls -la $T/ports | head -8
for f in $T/ports.tar.gz $T/ports.tar.gz.rmd160 $T/ports.tar $T/ports.tar.rmd160 $T/ports/PortIndex $T/ports/PortIndex.quick; do [ -e "$f" ] && { ls -la "$f"; shasum -a 256 "$f"; }; done
cat /opt/local/var/macports/sources/selfupdate/RELEASE_URL; echo
ls -la $T/ports/.mprevision $T/ports/*.txt 2>&1 | head; head -c 300 $T/ports/.mprevision 2>/dev/null; echo
stat -f '%Sm %N' $T/ports/PortIndex $T/ports/lang/python312/Portfile $T/ports/databases/duckdb/Portfile $T/ports/java/openjdk21/Portfile
shasum -a 256 $T/ports/lang/python312/Portfile $T/ports/databases/duckdb/Portfile $T/ports/java/openjdk21/Portfile
grep -c . /opt/local/etc/macports/pubkeys.conf; grep -v '^#' /opt/local/etc/macports/pubkeys.conf
pkgutil --pkgs | grep -i -E 'macports|CLTools'; pkgutil --pkg-info com.apple.pkg.CLTools_Executables 2>&1 | head -4
