# R2L — FIX READY
Old canonical_utf8 SHA-256: 4d7f5c97b2185dcdf81cf76c3aaf0aed23f8a468d9c7d4bcb0efd63d4dea48fe
New canonical_utf8 SHA-256: c313a8d7b202f944f34461b5897cd3be49c93dfcb1c4b82a5243f2394eec6f63
Old J2 file SHA-256: f1368a976795089c3359e00dd7d7e94c79ebac34cd5edf53c9b0f881a8171390
New J2 file SHA-256 (shasum -a 256): f0d0102a94d7a9e21160e41141dd805783c0d3f930205ee4ae24a59a2767c128
Interface pin: f7746c4bcce9976da5602d2c15249dede66c78e67071974d4099a69842c3882e — MATCH V3 §8
Runtime pin: 398e73fb2a688b7c67b5312c95cbc3d9e7be77291ff5d79559dc77fbe666941e — MATCH V3 §8
External schema-artifact pin: 3ebe4f3341912d16bd8055ca63945c3e6161b8825bd36c8d18e9efa471018395 — MATCH J2 (without x-construction)
Unmodified J2 format round-trip: EXACT; canonical_utf8 length 1777 <= 8192; new bytes match existing sha256.
Default checker exit=0; --mutation-controls exit=0; --control E4B exit=0.
GREEN: 105 schemas, 17 request kinds, 235 examples validated, 928 hash references recomputed
RED M1 exit=1 FAIL: schema lacks assertion: Hash
RED M2 exit=1 FAIL: SSH request kind missing/non-wire: REQUEST_UNIT
RED M3 exit=1 FAIL: missing/mismatched success mapping for REQUEST_UNIT
RED M4 exit=1 FAIL: hash reference mismatch: example/Process/executable_sha256
RED M5 exit=1 FAIL: missing schema or catalog entry: ['GrantRecord']
RED M6 exit=1 FAIL: malformed required at GrantRecord
RED E4B exit=1 FAIL: ReceiptBlob hash mismatch: ReceiptBlob
git diff --stat for J2/V3 (equivalent recomputed from Git index via stdlib; git execution excluded by command allowlist):
 .../shared_disk_clearance_freeze_v3.md | 2 +-
 .../shared_disk_clearance_schemas_v2.json | 2 +-
 2 files changed, 2 insertions(+), 2 deletions(-)
Scope: one J2 canonical_utf8 value and only V3:290 hash changed; K and KR hashes unchanged.
