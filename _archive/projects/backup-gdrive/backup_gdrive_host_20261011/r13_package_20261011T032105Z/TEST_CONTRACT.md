# MB44 test-first contract

Frozen before implementation. Scope controls use real git in mktemp directories
under /private/tmp only; the v2 scope RED adapter preserves v2's pin-only gate
and deliberately has no complete diff assertion. It is labelled an adapter,
not an original r11 executable. Verifier/plan RED use byte-identical r11 copies.

- Finding 1: source-commit export, exact branch/diff/bytes, an extra diff path,
  same-count path substitution, pin mutation, glob rejection, 1,000,001-byte evidence.
- Finding 2: inject unavailable/available executable probes, wrong/absent PR head,
  relative executable, probe env/caffeinate/rclone individually, default/download
  format pins and JSON override, actual plan contract.
- Finding 3: copy saved clean receipt for ERROR/CRITICAL/FATAL in microsecond,
  time-only, prefixed, JSON and unprefixed shapes, including stderr JSON. Preserve
  standard error rejection, DEBUG argument harmlessness, four saved fixture exits,
  and explicit date,time in both fixture templates.

GREEN requires zero failures/errors/skips in each group. RED requires assertion
failures (zero setup/import/runtime errors), child group exit 1; the receipt
runner exits 0 only when all expected RED groups are confirmed. Sandbox has
/usr/bin/python3 -B, isolated HOME and BACKUP_TEST_NO_RCLONE=1. No real rclone,
native service, production/test edit, or real-repo writing git action is authorized.
