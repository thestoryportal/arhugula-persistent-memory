---
name: prototype-tautology-trap
description: "Self-authored contract prototypes tend to test control-flow not the contract; build tests that can actually fail, and don't mistake them for empirical evidence."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 2801cf2e-560f-460c-86df-e227b16051b2
---

Across CP1/G1/G2/G3 (the 2026-06-18 viability prototypes), the advisor caught the SAME failure in every one: a test that confirms my own control flow, not the spec contract. Examples: D46 "inject fault → observe Git-ahead" (just restates line order); C-TPC4 "every COMMITTED has PREPARED" (true by construction — the executor always writes PREPARED first); G2 "wrong-key token rejected" (HMAC had that too — not the asymmetric upgrade); `code_pass_patch_fail` firing on a `_patch_forced_fail` flag the test itself sets; the storage-index SELECT that just reads back what was put in. Also a REAL bug hidden under a passing test: G2's Gate retained the whole Orchestrator object, so `gate.orch.key.sign()` was callable — "verify-cannot-forge" was contradicted by its own code while the tests stayed green.

**Why:** When you author BOTH the implementation and the tests, the tests pass because you built them to. A green checkmark on a self-built contract test carries almost no falsification weight. Worse, the bug-under-green case shows passing tests can actively mask a contract violation.

**How to apply:**
- Build tests that can ACTUALLY fail: **detection** not construction (fabricate a COMMITTED with no PREPARED → detector must flag it); **forgery/structural** not identity (prove the verifier holds no signing key — recursive `__dict__` scan — not just "wrong key rejected"); **divergence** not round-trip (index-says-X but behavioral-says-Y → flag storage-pass/behavior-fail). If a test cannot fail, cut it or relabel it a "documented property," not a passed verdict line.
- **Call advisor BEFORE authoring the test set, not just before declaring done** — it reshaped WHAT was tested in every prototype and caught the privkey bug. Pre-build is where the leverage is.
- **Category discipline (the bigger point):** "I wrote code to a contract and verified it implements the contract" is *design-viability* work — the weaker-than-empirical category the bootstrap names, with low real-failure risk. Reserve real confidence for EMPIRICAL runs that can genuinely fail (e.g. G6/G7: real GGUF-Q4_K, larger models, scale, multi-token, the C15 band). Set falsifiable pass criteria BEFORE those runs; let numbers fall where they land. Don't carry green-checkmark momentum into the run that can actually falsify the spec.
- Keep stub caveats flush with tests (HMAC→asymmetric, metadata→content, simulated boot, construction-asserted independence) so claims never outrun evidence.

See also [[calibrate-confidence-mechanics-vs-contracts]], [[review-diminishing-returns-evidence-is-binding]].
