# Stray native-test process clearance — 20261010T221601Z

Astra r10 item 4 requires identifying and clearing these before activation step 3.1.

Two process trees, left by earlier native Drive test runs (fixtures under /private/tmp/memit_gdrive_native_*):
- 32906 (Native_2.app applet, ppid 1) → 32913 (sh) → 32914 (bash wrapper) → 65807 (held-rclone sync)
- 36233 (Native_2.app applet, ppid 1) → 36258 (sh) → 36259 (bash wrapper) → 37109 (held-rclone sync)

At 22:11:10Z all eight were alive (elapsed 3h47m and 2h35m). The operator ran
`kill 32906 32913 32914 36233 36258 36259 37109 65807` in this session.

Verification at 20261010T221601Z: `ps -p 32906,32913,32914,36233,36258,36259,37109,65807` exit 1 (none exist);
`pgrep -f memit_gdrive_native_` matched nothing, so no descendant survived.
