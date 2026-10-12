# R2K report — BLOCKED C4
B = results/compute_storage_brainstorm_20261011T054507Z. All B/path:line citations below use this exact prefix.

C4 blocker: B/shared_disk_clearance_freeze_v3.md:74 requires ReceiptBlob canonical_utf8 to parse as a named immutable record and verify its sha256. B/shared_disk_clearance_schemas_v2.json:590 defines that same constraint.
B/shared_disk_clearance_schemas_v2.json:10050 contains the failing ReceiptBlob; its reference at :20356 selects InvocationBindingExecutor, defined at :13557.
Claimed/source SHA-256: c313a8d7b202f944f34461b5897cd3be49c93dfcb1c4b82a5243f2394eec6f63
Actual canonical_utf8 SHA-256: 4d7f5c97b2185dcdf81cf76c3aaf0aed23f8a468d9c7d4bcb0efd63d4dea48fe
Independent stdlib recomputation confirms that the embedded JSON is canonical, but its bound_values, profile_sha256, rendered_argv and rendered_argv_sha256 differ from the named source. Exactly one blob location fails: /x-construction/examples/ReceiptBlob/instance (B/shared_disk_clearance_schemas_v2.json:10050).
Required next step: MAESTRO's schema owner must reconcile that blob and source, update the bundle pin, then rerun acceptance. No source correction was made here.

Criterion implementation (not a completion claim):
C1 — B/check_r2_schemas_v2.py:278 requires top-level assertions, enumerates keywords, checks draft keyword shapes; :40 rejects duplicate/nonfinite JSON.
C2 — B/check_r2_schemas_v2.py:337 parses §3 independently; :354 checks corrected SSH subset, all mapping schemas/catalog/root membership/transitions; :148 retains document and enum agreement.
C3 — B/check_r2_schemas_v2.py:376 evaluates every supported assertion; :446 validates every named example. Unknown keywords fail before validation.
C4 — B/check_r2_schemas_v2.py:503 recomputes references, checks dependency cycles, blob bytes/records, raw artifacts, receipt/authority bindings and transitions; :896 resolves all reference modes; :462 extracts state edges.
C5 — B/check_r2_schemas_v2.py:446 requires success/refusal coverage for every mapped kind.
C6 — B/check_r2_schemas_v2.py:967 builds damaged TMPDIR copies and reseals pins; :1051 uses fresh /usr/bin/python3 -B subprocesses and exact expected first-error messages.
Inherited S checks remain at B/check_r2_schemas_v2.py:54,99,129,148. Root membership follows pure named union aliases, covering the three variants nested at B/shared_disk_clearance_schemas_v2.json:1242.

Current acceptance: default invocation exits 1: FAIL: ReceiptBlob hash mismatch: ReceiptBlob
GREEN line: NONE. The earlier 105/17/235/928 intermediate GREEN preceded blob byte validation and is superseded.
--mutation-controls exits 0 with all six intended RED lines:
RED M1 exit=1 FAIL: schema lacks assertion: Hash
RED M2 exit=1 FAIL: SSH request kind missing/non-wire: REQUEST_UNIT
RED M3 exit=1 FAIL: missing/mismatched success mapping for REQUEST_UNIT
RED M4 exit=1 FAIL: hash reference mismatch: example/Process/executable_sha256
RED M5 exit=1 FAIL: missing schema or catalog entry: ['GrantRecord']
RED M6 exit=1 FAIL: malformed required at GrantRecord
RED E4B exit=1 FAIL: ReceiptBlob hash mismatch: ReceiptBlob
Development controls preceded their checks: missing assertions/SSH kind/hash binding, invalid/missing examples, sequence/state/nonce/fence and blob errors initially escaped the relevant checks. Extra boundary tests covered boolean/numeric equality, lengths/bounds, conditions, combinators and unknown keywords; canonical escaping and invalid JSON also passed.
M2 additionally removes the ResponseMapping example, nested consumer mapping and derived array count, and rehashes its synthetic dependencies. Final isolation verification: disabling only the SSH subset in a disposable process leaves all other checks GREEN (102 schemas, 16 kinds, 231 examples, 921 references); final M2's intended subset failure is verified above.
Runtime validator keywords: $defs, $id, $ref, $schema, additionalProperties, allOf, const, description, else, enum, if, items, maxItems, maxLength, maximum, minItems, minLength, minimum, oneOf, pattern, properties, required, then, type, x-catalog, x-construction, x-fencing-mapping, x-response-mapping. Additionally implemented: anyOf, not. Annotation/extension keywords are explicitly recognized metadata.

Rules encoded from prose (citations are B/shared_disk_clearance_freeze_v3.md unless stated):
- :298 — UTF-8 canonical serialization; authority hash omits only last_decision (Out :845, :896).
- :71,74 — durable COMMITTED before/after hashes, named canonical blobs, QUERY read-only/current last decision (Out :503).
- :175,220 — authority/observation host, boot, epoch and sequence equality (Out :503).
- :208,259 — derived authority state, recovery exclusion/reconciliation, new epochs; sequence reset at 1 additionally comes from B/shared_disk_clearance_schemas_v2.json:28181 (Out :503).
- :195,196,220 — REGISTER_SCIENCE's proved intermediate PENDING publication; consume exact nonce/sequence before expiry (Out :503).
- :197,204 — atomic science terminal archive with closure proof; fresh resumed unit/nonce and approval (Out :503).
- :186,187,188,199,214 — terminal/paused closure and coordinator-owned exact enrolled unit consumption (Out :503).
- :160,161,163,164,165,170,259 — operation-specific fencing, reconciliation/history exclusion, initialization in recovery, administrative approval; RECONCILE approval binds proposed new epoch and observed request sequence (Out :503).
- Synthetic schema projection omits the whole x-construction annotation under B/shared_disk_clearance_schemas_v2.json:9917; it is not the deployed full-file pin at B/shared_disk_clearance_freeze_v3.md:290 (Out :856).

Noticed, not fixed: stale ReceiptBlob serialized binding despite updated source/hash (B/shared_disk_clearance_schemas_v2.json:10050,13557,20356).
Noticed, not fixed: phase prose omits the intermediate registration revision and RECONCILE approval's new-epoch/old-sequence pairing (B/shared_disk_clearance_schemas_v2.json:28181,15944,15066).
Scope: only Out and this Report were written in B; TMPDIR holds copies/logs. V3/J2/S hashes remain unchanged:
V3 e89f3bb32f132c6e7e5c1e55aeee7ddd416ae4d07dcb6b04f3ca69fe1d22f6b7
J2 f1368a976795089c3359e00dd7d7e94c79ebac34cd5edf53c9b0f881a8171390
S 8d8149497bf2ac92f526a24ade35b42f846ed8f93499661022d6b7189c31770c
Current raw receipts: /var/folders/p7/s31_tv0s2wd81chns8v7gsyw0000gn/T/r2k-blocked-c4-ay7nlcuo
Static synthetic verification only; no host/operational acceptance.
