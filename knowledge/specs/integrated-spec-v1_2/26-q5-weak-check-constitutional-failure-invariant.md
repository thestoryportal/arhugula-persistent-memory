## 25. Q5 Weak-Check / Constitutional-Failure Invariant

### 25.1 Purpose

Qualification criterion Q5 for constitutional-test promotion (GAP-10; v2 GS8 D97) requires that failures of constitutional tests map to a claimed `invariant_statement` field on the test metadata. Structural verification of natural-language assertion messages against such a claim is brittle as a blocking gate — too-strict parsers reject legitimate failures; too-lenient parsers provide no signal. §25 specifies the **weak-check pattern**: Ledger-logged co-record, no runtime block. Source: v2 GS9 D100; amendment A14.

### 25.2 The Weak-Check Pattern

When a constitutional test fails, the Validator emits a `CONSTITUTIONAL_FAILURE` Ledger entry (pre-existing in Appendix C per A7b) with a **new field pair** (A14):

- **`invariant_statement`** — copied from the test's metadata (authoritative source).
- **`failure_assertion_message`** — captured verbatim from the test's runtime output.

The Validator does **not** compare these two fields at runtime. The entry is a co-record: both fields are present in the Ledger, available for operator audit query. Divergence between the two is a signal the operator chooses to surface — not a runtime block.

This preserves the central invariant of the validation architecture (no runtime-gated natural-language parsing) while providing the data substrate for a future promotion to blocking-gate classification if the operational signal is ever deemed sufficient.

### 25.3 Spec Block — Constitutional-Failure Invariant

**What it must record:** Every constitutional-test failure produces a Ledger entry whose content includes both the test-metadata invariant claim and the runtime failure message, side-by-side.

**Hard constraints:**
- **C-CONSTITUTIONAL-Q5:** `CONSTITUTIONAL_FAILURE` Ledger entry MUST include both `invariant_statement` (from test metadata) and `failure_assertion_message` (captured verbatim from runtime). Neither field is optional; a write attempting to emit one without the other is rejected by the Validator as an implementation bug.
- No runtime comparison of the two fields is performed by any automated path. Comparison is an operator-initiated audit query.
- The two fields carry separate integrity guarantees: `invariant_statement` is a deterministic copy of test metadata at the time of the failing test run; `failure_assertion_message` is the verbatim runtime output from the test harness.

**Tradeoffs decided:**
- Weak-check pattern over blocking-gate check — preserves Reflexion-loop semantics and avoids brittleness.
- Same Ledger entry type (`CONSTITUTIONAL_FAILURE`) as a field pair, over introducing a new entry type — minimal surface change; entry type already exists.

**Open questions (deferred):**
- **OQ-V10** — Whether the spec should mandate a minimum operator audit-query suite (distinct from the constitutional test suite) to surface Q5 divergences. The weak-check pattern presumes operator tooling; if no query ever runs, Q5 degradation is logged but never observed. Low priority; v2 scope.

**Interface contract amendment:**
- **A14-Appendix-C-CONSTITUTIONAL_FAILURE** — field pair added to the entry type schema.

### 25.4 Non-Goals

§25 does not specify:
- Operator audit-query tooling (OQ-V10; operator-owned).
- Promotion of the weak-check to a blocking gate — the field pair is the substrate if future analysis warrants promotion, but the promotion itself is out of scope for v1.2.

---

