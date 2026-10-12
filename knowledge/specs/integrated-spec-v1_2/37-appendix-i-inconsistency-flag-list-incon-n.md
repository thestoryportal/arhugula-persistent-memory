## Appendix I — Inconsistency Flag List (INCON-N)

This appendix records any inconsistencies detected during final v1.2 spec assembly that were not resolved during the gap-session arc. Each flag is a candidate for a targeted follow-on session. Absence of a flag in this list indicates the corresponding area was either resolved inline or not detected during assembly.

### Status: **ASSEMBLY CLEAN WITH ADVISORY NOTES**

No blocking inconsistencies were identified during v1.2 assembly. Four advisory notes are recorded below for operator and future-council awareness. None of the advisories alters a ratified decision, constraint, or interface contract — each is a cosmetic or documentation-hygiene concern raised by cross-referencing session sources.

### Advisory notes

**INCON-v12-A01 — Ledger entry name aliases across sources.**
Three entry-type pairs exist with variant spellings in session summaries:
- `DEPENDENCY_HOLD_RELEASE_SIGNED` vs. `DEPENDENCY_HOLD_RELEASED_SIGNED` (GS5 v3 / GS10 co-usage)
- `CAK_BURST_LIMIT_EXCEEDED` vs. `CAK_CEREMONY_BURST_EXCEEDED` (GS10 co-usage)
- `SCOPE_UPDATE_RATE_EXCEEDED` vs. `SCOPE_UPDATE_RATE_LIMIT_EXCEEDED` (GS7 v3 / GS10 co-usage)

**Disposition:** Appendix C records both forms with [COUNCIL-FLAG] markers and names the recommended canonical form for each pair. Implementation should pick one per pair and treat the other as not emitted. Advisory only; does not affect correctness, Ledger integrity, or any ratified contract.

**INCON-v12-A02 — `MANIFEST_RATIFICATION` category placement.**
§Appendix C places `MANIFEST_RATIFICATION` in the CONSISTENCY category for narrative grouping with `MANIFEST_COMMIT_REJECTED` and `MANIFEST_LATTICE_INCOMPLETE`. However, a signed operator ceremony outcome arguably fits GOVERNANCE more naturally (it is a ceremony record, not a consistency event).

**Disposition:** Flagged inline at Appendix C. Either placement is defensible; implementation will pick one at the point of emitter wiring. Advisory only.

**INCON-v12-A03 — `OOK_ROTATED` category placement.**
Source material (GS11, GS12) shows `OOK_ROTATED` emitted under contexts consistent with both GOVERNANCE (paired with CAK-rotation entries under operator ceremony) and LIFECYCLE (as a key-rotation lifecycle marker).

**Disposition:** Appendix C places it in GOVERNANCE to pair with the CAK-rotation family. If implementation treats it as pure key-lifecycle, relocate to LIFECYCLE. Advisory only.

**INCON-v12-A04 — `WRITE_LOCK_VOLUNTARY_RELEASED` v2-scope drift.**
The `voluntary write-lock release` path is explicitly listed in §19 v2 scope. The corresponding Ledger entry type was introduced in GS10 / GS12 partial discussion. Appendix C records the entry type with a [COUNCIL-FLAG] noting that no v1 code path emits it; it is present solely for forensic completeness if operator tooling ever produces it.

**Disposition:** Kept in catalog with flag; retired from v1.2 emitter surface; documented for v2 re-integration.

### Resolution path

None of INCON-v12-A01 through A04 requires a follow-on gap session. All four are documentation-hygiene concerns or forward-compat placeholders that implementation teams will resolve at the emitter-wiring step. The spec is consistent on all load-bearing contracts (authorization, state consistency, validation, retention, provenance).

**Overall v1.2 assembly status: CLEAN.** No unresolved blocking inconsistency. Spec is ready to seal pending only the standard operator ratification step.

---

