# Gap Session 13 Summary — Final Gap Resolution (Framework Council)

**Session:** GS13 of 13 — **Final gap resolution session**
**Primary skill:** framework-council (all six specialists)
**Baseline:** v1.1 integrated spec + GS1–GS12
**Gaps addressed (14 resolutions + 3 cross-refs):** GAP-4, GAP-9, GAP-13, GAP-15, GAP-17, GAP-18, GAP-19, GAP-27, GAP-32, GAP-48, GAP-49, GAP-50, GAP-51, GAP-55 | cross-refs: GAP-56, GAP-57, GAP-58
**Tensions disposed (1):** T15
**Amendments applied (1):** A11
**Sequencing note:** GAP-58 (state-machine addenda for `BURST_SUSPENDED` and `TRUST_ROOT_LOST`) is resolved first because its outputs are consumed by the GAP-4 per-path specs (item 3 §GAP-58 section). GAP-56 and GAP-57 are resolved inside the GAP-4 per-path blocks. Independent items follow in declared order.

---

## Part 1 — State Machine Addenda (GAP-58, SCT + Warden co-owned)

### §11.8 Addendum A — `BURST_SUSPENDED` State — Spec Block

**What it must do / represent / enforce / guarantee:**
Define the `BURST_SUSPENDED` state (introduced GS10 via GAP-41/C-CAKB-4) as a first-class §11.8 state, specifying which ceremonies it blocks, which remain valid, what clears it, and how it composes with the existing `CIRCUIT_TRIPPED` / `READ_ONLY` state machine.

**Hard constraints:**
- **C-BS-1 (State Trigger):** `BURST_SUSPENDED` is entered atomically when the per-CAK burst limit (N=5 ceremonies / 10-minute sliding window per CAK, per C-CAKB-1) is breached. Entry is recorded via `CAK_BURST_LIMIT_EXCEEDED` Ledger entry (SECURITY, sync, W1).
- **C-BS-2 (State Scope — Per-CAK, Not Per-Harness):** `BURST_SUSPENDED` is scoped to the specific CAK whose burst limit was breached. If the deployment has only one registered CAK (v1 default — T15 / A11), `BURST_SUSPENDED` is effectively harness-wide for ceremony acceptance purposes. If the deployment has registered both the primary CAK and the break-glass second anchor (GAP-42 / C-BG-1), the non-suspended anchor remains operational and is the **only** path to `CAK_BURST_CLEARED`.
- **C-BS-3 (Ceremonies Blocked):** While in `BURST_SUSPENDED` for a given CAK, the harness REJECTS every new ceremony initiation bearing that CAK's signature, with Ledger entry `CEREMONY_REJECTED_BURST_SUSPENDED` (SECURITY, async, W1) — including but not limited to: `GENESIS_INITIATION`, `SCOPE_UPDATE`, `DEPENDENCY_HOLD_RELEASE_SIGNED`, `CAK_ROTATION_EMERGENCY` (non-break-glass path).
- **C-BS-4 (Ceremonies That Remain Valid):**
    - **`CIRCUIT_RESET` ceremonies:** Remain valid **iff** the CIRCUIT_RESET ceremony itself does NOT trip the burst-limit counter for the suspended CAK. Concretely: CIRCUIT_RESET signed by the suspended CAK is accepted only if the burst-counter evaluation at the moment of signature verification shows the event would not itself constitute the 6th event in the 10-minute window. If it would, the reset is rejected with `CEREMONY_REJECTED_BURST_SUSPENDED` (trip-reason field set to `RESET_WOULD_EXTEND_BURST`).
    - **Break-glass channel:** `CAK_ROTATION_EMERGENCY` signed by the break-glass second anchor (not the suspended CAK) is ACCEPTED regardless of `BURST_SUSPENDED` state — the break-glass anchor is not subject to the suspended CAK's burst counter. (Note: the break-glass anchor has its own independent burst counter; its own breach would place IT into `BURST_SUSPENDED`.)
    - **W3 emergency writes:** Remain valid in `BURST_SUSPENDED` (same as in `CIRCUIT_TRIPPED`) — `BURST_SUSPENDED` does not gate W3.
    - **Scope updates:** BLOCKED — a scope update is a ceremony-mediated operation bearing the suspended CAK.
- **C-BS-5 (State Clearing — Two Paths):**
    - **(a) Auto-clear on window expiry:** When the 10-minute sliding window elapses without further qualifying ceremonies, the state auto-clears; harness writes `CAK_BURST_AUTO_CLEARED` (SECURITY, async, W1) to the Ledger. This is the expected recovery path for spurious bursts (e.g., operator making several rapid ceremony attempts during a genuine crisis).
    - **(b) Explicit clear by Tier 1 ceremony:** `CAK_BURST_CLEARED`, signed by a **different** CAK with Tier 1 authority (i.e., the break-glass anchor, per C-CAKB-4 / IC-CAKB-1). Requires a matching `ceremony_context` justification field. On acceptance, harness writes `CAK_BURST_CLEARED` (SECURITY, sync, W1) and the suspended CAK's state is cleared immediately.
- **C-BS-6 (State Composition with `CIRCUIT_TRIPPED`):** `BURST_SUSPENDED` and `CIRCUIT_TRIPPED` **stack** — they are independent flags. A deployment may simultaneously be in `BURST_SUSPENDED` (ceremony-acceptance blocked for one CAK) and `CIRCUIT_TRIPPED` (token-mediated application writes suspended). Both must clear independently. Governance-category W1 writes permitted by GAP-37 §11.8.1 amendment (CIRCUIT_RESET, DEPENDENCY_HOLD_RELEASED_SIGNED, RECONCILIATION_COMPLETE) are further constrained under `BURST_SUSPENDED` by C-BS-4: the underlying CeremonyToken signature must not belong to a suspended CAK.
- **C-BS-7 (Precedence on Simultaneous Conditions):** If a ceremony would be rejected by both `BURST_SUSPENDED` (C-BS-4) and `CIRCUIT_TRIPPED` (§16.2), rejection Ledger entries SHOULD record both causes in a single `CEREMONY_REJECTED_MULTI_CAUSE` entry with `cause_list` field to avoid double-logging. If only one applies, the specific rejection type (`CEREMONY_REJECTED_BURST_SUSPENDED` or `CEREMONY_REJECTED_CIRCUIT_TRIPPED`) is used.
- **C-BS-8 (Human Review Queue Behavior):** `BURST_SUSPENDED` does NOT interfere with processing of items already on the Correctness or Reconciliation Review Queues. Review decisions remain queuable and actionable. The block is on **new ceremony initiation**, not on adjudication of prior work.

**Tradeoffs decided:**
- **Per-CAK scoping over harness-wide** — preserves break-glass operability; matches the C-CAKB-4 / GAP-42 design intent.
- **Stackable with `CIRCUIT_TRIPPED`** — the two states defend against different threat classes (burst anomaly vs. consistency fault); conflating them would mask either signal.
- **Reset ceremony subject to burst-counter re-evaluation** — prevents a pathological case where an attacker drives burst on a legitimate CAK, then issues a reset ceremony that masks the burst as "resolved."
- **Auto-clear preserved alongside explicit clear** — operators lacking access to a break-glass anchor at the moment of suspension must still have a path back; 10-minute delay is accepted as a denial-of-service mitigation cost.

**Open questions (deferred):** None for v1.1.

**Interface contract:**
- **IC-BS-LIFECYCLE (new):** §11.8 state machine recognizes `BURST_SUSPENDED` as an orthogonal flag per-CAK, composed with `CIRCUIT_TRIPPED` per C-BS-6. TC queries CAK burst state via the existing `ceremony_gate_state_query` interface (returns tuple `(circuit_state, per_cak_burst_state[])`). No new query surface required — the existing gate state query is extended by one field.
- **Appendix C additions:** `CAK_BURST_LIMIT_EXCEEDED` (SECURITY, sync, W1), `CEREMONY_REJECTED_BURST_SUSPENDED` (SECURITY, async, W1), `CEREMONY_REJECTED_MULTI_CAUSE` (SECURITY, async, W1), `CAK_BURST_AUTO_CLEARED` (SECURITY, async, W1), `CAK_BURST_CLEARED` (SECURITY, sync, W1).

---

### §11.8 Addendum B — `TRUST_ROOT_LOST` State — Spec Block

**What it must do / represent / enforce / guarantee:**
Define `TRUST_ROOT_LOST` (introduced GS10 via GAP-42 / C-BG-7) as a **terminal state** of the harness — one with no harness-side exit path — specifying what remains writable, what ceremonies are rejected, and what operator-side recovery looks like.

**Hard constraints:**
- **C-TRL-1 (Entry Trigger):** `TRUST_ROOT_LOST` is entered atomically when (a) the break-glass second anchor's private half is detected as compromised (anomalous `BREAK_GLASS_ACTIVATION` attempt, per C-BG-7), OR (b) both the primary CAK and the break-glass anchor are simultaneously flagged `COMPROMISED_AT_BOOT` during the §13.5 step 3a verification. Entry is recorded via `TRUST_ROOT_LOST_ENTERED` (SECURITY, sync, W1 — dedicated path, emitted regardless of other state flags, parallel to `BREAK_GLASS_ACTIVATED`).
- **C-TRL-2 (Terminal State — No Harness-Side Exit):** `TRUST_ROOT_LOST` has NO harness-accepted ceremony that clears it. Neither `CIRCUIT_RESET`, nor `CAK_BURST_CLEARED`, nor `CAK_ROTATION_EMERGENCY` (via break-glass or otherwise) will clear `TRUST_ROOT_LOST`. Exit is **only** via bootstrapping a new harness instance from scratch (new operator-root keypair per C-BOOT-5 / GAP-40, new CAK anchor, new break-glass anchor, new `genesis-seal.json`). The prior harness's `.vindex` and State Ledger are retained as forensic evidence but are not reanimated under the new harness.
- **C-TRL-3 (Ceremonies Rejected):** In `TRUST_ROOT_LOST`, **all** ceremony-mediated writes are REJECTED regardless of which CAK or anchor signed them. Rejection Ledger entry: `CEREMONY_REJECTED_TRUST_ROOT_LOST` (SECURITY, async, W1). This supersedes `BURST_SUSPENDED` and `CIRCUIT_TRIPPED` rejection semantics.
- **C-TRL-4 (Writes That Remain Valid):**
    - **W3 emergency writes:** REMAIN VALID — `TRUST_ROOT_LOST` does not gate W3. W3 is the emergency path precisely for scenarios where ceremonial trust is compromised.
    - **Forensic W3 entries:** The following W3 entry types explicitly remain writable in `TRUST_ROOT_LOST`: `LEDGER_FORENSIC_EVIDENCE_CAPTURE`, `VINDEX_FORENSIC_SNAPSHOT_REF`, `OPERATOR_RECOVERY_ACTION_LOGGED`. These exist to preserve the evidentiary trail during the transition to a new harness.
    - **Non-W3 writes:** All W1 and W2 categories are REJECTED. This includes governance-category W1 writes that would normally be permitted under `CIRCUIT_TRIPPED` (the GAP-37 exception does not extend to `TRUST_ROOT_LOST`).
- **C-TRL-5 (Review Queue Behavior):** Existing items on the Correctness and Reconciliation Review Queues remain **readable** (operators can inspect them for forensic context) but are **not processable** — `approve_as_is` / `approve_patch` / `modify_patch` decisions cannot execute under `TRUST_ROOT_LOST` because the downstream write path is blocked. Queue items are effectively frozen-in-place. Operators should treat queue contents as evidence, not as actionable work items.
- **C-TRL-6 (Read Path Availability):** `.vindex` reads, Ledger reads, and review queue reads remain available to authenticated operators. The state blocks writes, not inspection.
- **C-TRL-7 (No Third-Tier Recovery):** Per C-BG-7 decision recorded in GS10, there is no third anchor above the break-glass anchor. Adding one would regress the trust-root problem by one level; Genesis re-initialization is the explicit recovery policy.

**Tradeoffs decided:**
- **Terminal state over recoverable state** — any harness-accepted recovery ceremony would itself require a trusted signer, which by definition does not exist once both anchors are compromised. Terminal designation names this reality rather than constructing a false exit path.
- **W3 preservation** — without W3 availability, the operator loses the ability to capture forensic state for recovery. W3's design (out-of-band signed, evidence-only) makes it the correct path to preserve through this state.
- **Queue readable but frozen** — a hard delete or lockout would destroy forensic context; blanket-approve capability would enable an attacker who has compromised both trust roots to also drain the queue. Frozen-readable is the middle ground.
- **Genesis re-init as recovery policy** — a deliberate acceptance of the cost: full operator reboot. The alternative (third anchor) was rejected as infinite regress.

**Open questions (deferred):** None for v1.1. Operator-runbook documentation for the Genesis-reinit recovery sequence is an implementation-phase artifact, not a spec-layer item.

**Interface contract:**
- **IC-TRL-1 (new):** §11.8 state machine recognizes `TRUST_ROOT_LOST` as a terminal flag that, when set, causes the Ceremony Gate to return `REJECTED_TRUST_ROOT_LOST` on every ceremony initiation attempt regardless of signer identity. No new query surface — the existing `ceremony_gate_state_query` returns this as a third tuple element `(circuit_state, per_cak_burst_state[], trust_root_lost: bool)`.
- **Appendix C additions:** `TRUST_ROOT_LOST_ENTERED` (SECURITY, sync, W1, dedicated path), `CEREMONY_REJECTED_TRUST_ROOT_LOST` (SECURITY, async, W1), `LEDGER_FORENSIC_EVIDENCE_CAPTURE` (SECURITY, async, W3), `VINDEX_FORENSIC_SNAPSHOT_REF` (SECURITY, async, W3), `OPERATOR_RECOVERY_ACTION_LOGGED` (SECURITY, async, W3).

---

## Part 2 — GAP-4: Three Conditional Path Specs (Orchestration Comparativist primary)

Each block activates on operator selection of the named path. 2PC TC and Merkle-chain State Ledger remain custom components in all three paths (per D80). Each block addresses the path-specific delegation token shape, HIL mechanism, trust boundary, GAP-56 Genesis-density, GAP-57 binary-distribution, and GAP-58 state-lifecycle handling.

### GAP-4/A — Path A (LangGraph alone) — Conditional Spec Block

**Activates on:** Operator selection of Path A at harness-build time.

**What it must do / represent / enforce / guarantee:**
Specify how a pure LangGraph orchestrator satisfies the harness's control-plane requirements, including the cases introduced by GAP-56/57/58.

**Hard constraints:**
- **C-PATHA-1 (Delegation Token Shape):** Path A uses the §10.4 nine-field Invocation Token unchanged — no nested-sub-agent delegation tokens are required in v1 because LangGraph's default execution model is flat-DAG: agent nodes invoke tools/sub-routines directly, not other agent graphs. For v1.1, Path A explicitly DOES NOT support nested sub-agent delegation; the nested case is v2-deferred per §6 Category 3.
- **C-PATHA-2 (HIL Mechanism):** Human-in-the-Loop is implemented via LangGraph's `interrupt()` primitive paired with the Correctness Review Queue and Reconciliation Review Queue interfaces (IC-REVIEW-QUEUE, amended GS11). On queue-blocking decisions the graph node calls `interrupt()` with a payload carrying the queue item ID; graph resumes from operator queue decision via the `Command(resume=...)` primitive. Graph state checkpointing is LangGraph-native (SQLite checkpointer mandatory; remote checkpointer v2-deferred per GAP-18 alignment).
- **C-PATHA-3 (2PC TC Placement):** The Transaction Controller is a **custom component invoked from a LangGraph node**, not a graph node itself. This preserves TC authority over the two-phase commit sequence — LangGraph orchestrates the workflow up to and after the TC call, but does not attempt to decompose 2PC into multiple graph nodes. TC exposes `tc_begin(plan)` / `tc_prepare(prepared_token)` / `tc_commit(commit_token)` / `tc_abort(reason)` as blocking synchronous calls to the calling graph node.
- **C-PATHA-4 (Trust Boundary):** All LangGraph nodes run inside the harness process space. LangGraph's Python runtime is treated as in-harness code, subject to the same immutability contracts as other in-harness modules. No external LangGraph service; no LangGraph Cloud dependency in v1. LangGraph version is pinned in the harness lockfile and participates in the reproducible-build contract (C-PATHA-6 below).
- **C-PATHA-5 (GAP-56 Worst-Case Genesis Density):** Path A's worst-case legitimate Genesis-ceremony density is **≤ 2 per 10-minute window** under the following workflows: (a) initial Genesis + one operator-initiated Genesis revision, or (b) Genesis recovery from `GENESIS_TIMED_OUT` followed by a corrective re-Genesis. Both scenarios remain well below the C-CAKB-1 burst limit (N=5 / 10-minute window). **Path A is confirmed path-safe under C-CAKB-1 with no path-specific override.**
- **C-PATHA-6 (GAP-57 Build/Distribution Model):**
    - **Build model:** Each operator builds their own harness binary from the reference source tree, embedding their `operator_root_public_key` at compile time (per C-BOOT-5). LangGraph's pinned version and Python runtime are bundled in the binary via `pyinstaller` or equivalent single-binary packaging — no runtime Python dependency fetch.
    - **Reproducible-build contract:** The harness source tree publishes a `reproducible-build-manifest.json` (new artifact) containing the exact toolchain versions (Python interpreter hash, LangGraph wheel hash, all transitive dependency hashes). Operators verify that `(reference_source_hash, toolchain_manifest_hash, operator_root_public_key)` → deterministic binary hash for their build. The reference build publishes per-`operator_root_public_key`-less "universal-parts" hashes; the operator confirms that injecting their key produces the expected final binary hash.
    - **Patch distribution:** Security patches are distributed as **source-tree deltas**, not as replacement binaries. Each operator rebuilds their binary from the patched tree. The harness's in-place update path (v2) is explicitly not supported in v1 — `CAK_ROTATION_EMERGENCY` + Genesis re-init is the recovery path.
    - **Verification:** Patch authenticity is verified via the reference source tree's release signing (separate from the operator-root-key system; out-of-band signed by the framework maintainers). The operator's trust in patches is rooted in the maintainer signing key, not the operator-root key.
- **C-PATHA-7 (GAP-58 State-Lifecycle Handling):**
    - **`BURST_SUSPENDED` handling:** The LangGraph Ceremony Gate node consults `ceremony_gate_state_query` (IC-BS-LIFECYCLE) before admitting a ceremony-initiating edge. On `BURST_SUSPENDED` match for the signing CAK, the node routes the request to a dedicated `rejected_ceremonies` terminal node that writes the appropriate `CEREMONY_REJECTED_*` Ledger entry and returns to the caller; no graph state corruption.
    - **`TRUST_ROOT_LOST` handling:** The LangGraph top-level entry guard (a first-node pattern applied to every graph invocation) consults the state query and, on `TRUST_ROOT_LOST`, short-circuits the entire graph to a `forensic_only` subgraph whose nodes only emit W3 entries. The read-path queries (Ledger reads, review queue reads) are available through a separate read-only LangGraph entry that does not traverse the guard.
    - **Stacked states:** Guard logic evaluates `TRUST_ROOT_LOST` first (most restrictive), then `CIRCUIT_TRIPPED`, then per-CAK `BURST_SUSPENDED`. Multi-cause rejections route through the `CEREMONY_REJECTED_MULTI_CAUSE` path (per C-BS-7).

**Tradeoffs decided:**
- **Flat-DAG only in v1** — nested delegation is v2; keeps token model simple.
- **Single-binary packaging** — avoids Python-runtime drift; costs binary size and build time.
- **Guard as first-node pattern** — avoids per-node state checks; costs one extra edge per invocation.

**Open questions (deferred):** None for v1.1. Nested delegation token shape → v2 per §6.

**Interface contract:**
- **IC-PATHA-GUARD (new):** Every Path A LangGraph entry point MUST wrap its first user-facing node with the three-layer guard (`TRUST_ROOT_LOST` → `CIRCUIT_TRIPPED` → per-CAK `BURST_SUSPENDED`). Violation of the wrapping contract is a harness build-time verification failure (harness binary refuses to ship).

---

### GAP-4/B — Path B (Claude Agent SDK alone) — Conditional Spec Block

**Activates on:** Operator selection of Path B at harness-build time.

**What it must do / represent / enforce / guarantee:**
Specify how a pure Claude Agent SDK orchestrator satisfies the harness's control-plane requirements, including the nested-sub-agent case (native to Agent SDK) and the GAP-56/57/58 cases.

**Hard constraints:**
- **C-PATHB-1 (Delegation Token Shape):** Path B must support **nested sub-agent delegation** because the Claude Agent SDK's orchestration idiom includes parent agents dispatching to sub-agents with delegated authority. The nested delegation token is defined but v2-deferred for implementation (per §6). The **outline for v1.1 operators** is: a delegation token is a §10.4 Invocation Token with two additional fields — `parent_invocation_token_hash` (links the nested call to its parent) and `delegation_scope_subset_hash` (the hash of the child agent's scope file, which MUST be a structural subset of the parent's). Nested delegation tokens remain OOK-signed; the OOK signature covers all eleven fields. v1.1 operators selecting Path B operate in single-level mode only — no nested sub-agent dispatch — with explicit contract check at harness build time.
- **C-PATHB-2 (HIL Mechanism):** Claude Agent SDK's native interrupt-and-resume is via `request_user_input` tool calls, which integrate with the Correctness and Reconciliation Review Queue interfaces as follows: an agent node invokes `request_user_input` with queue-item payload, the SDK suspends the agent thread, the harness routes the payload to the appropriate queue via IC-REVIEW-QUEUE, and on queue decision the SDK resumes the agent thread with the decision payload. Agent thread state is checkpointed by the SDK to the harness-local checkpoint store (file-backed; multi-machine v2-deferred per GAP-18 alignment).
- **C-PATHB-3 (2PC TC Placement):** The Transaction Controller is a **tool exposed to agents**, not a separate orchestration primitive. Agents call `tc.begin(plan)` / `tc.prepare(...)` / `tc.commit(...)` / `tc.abort(...)` as tool calls. The TC tool enforces the 2PC state machine internally — agents cannot bypass ordering. Agent SDK's tool-call audit trail captures every TC invocation as part of the agent's conversation log, which provides a secondary audit trail alongside the Ledger (the Ledger remains authoritative per D80).
- **C-PATHB-4 (Trust Boundary):** The Agent SDK's agent processes run as in-harness subprocesses, each with a per-invocation scope contract. Claude model access is via the Anthropic API — an **external dependency with trust implications**. Path B operators MUST document their API-access trust posture: (a) which API key principals are authorized, (b) which model versions are pinned in the harness Tier 1 config, (c) how an Anthropic-API outage is classified (`EXTERNAL_DEPENDENCY_UNAVAILABLE`, not a harness fault). The harness does NOT fail-closed on API outage — it surfaces the outage to the operator via the existing review queue mechanism and suspends affected agent invocations.
- **C-PATHB-5 (GAP-56 Worst-Case Genesis Density):** Path B's worst-case legitimate Genesis-ceremony density is **≤ 3 per 10-minute window** in the following workflows: (a) initial Genesis + multi-skill loader Genesis sub-ceremonies (skills register with their own Genesis-sub entries) + a recovery retry. This remains below C-CAKB-1 (N=5). **Path B is confirmed path-safe under C-CAKB-1 with no path-specific override.** Operators who deploy complex skill-tree Genesis workflows with > 5 expected Genesis-sub-ceremonies in a 10-minute window MUST split the workflow across multiple windows or request a path-specific threshold deviation with documented rationale (per C-AGG-2 precedent in GS12).
- **C-PATHB-6 (GAP-57 Build/Distribution Model):**
    - **Build model:** Operator-built binary, with `operator_root_public_key` embedded at compile (per C-BOOT-5). Claude Agent SDK's version and its Anthropic-API client are bundled in the binary. The Anthropic-API endpoint URL is Tier 3 configurable (operators on managed private endpoints can redirect), but the API protocol version is Tier 1 pinned.
    - **Reproducible-build contract:** Per Path A's C-PATHA-6 `reproducible-build-manifest.json` pattern, adapted to include the Agent SDK wheel hash and Anthropic-client hash.
    - **Patch distribution:** Source-tree-delta model, same as Path A.
    - **Verification:** Framework maintainer signing key — same as Path A. Separately, operators are responsible for verifying Anthropic-API endpoint TLS certificate pinning (operator-level configuration in Tier 3 config).
- **C-PATHB-7 (GAP-58 State-Lifecycle Handling):**
    - **`BURST_SUSPENDED` handling:** The Ceremony Gate is implemented as a mandatory pre-tool-call hook that runs before every agent tool invocation potentially affecting ceremony state. On `BURST_SUSPENDED` match for the signing CAK, the hook returns a tool-call failure with structured rejection payload; the agent receives this as a standard tool error and must surface it to the operator via the normal agent error path.
    - **`TRUST_ROOT_LOST` handling:** A top-level SDK session guard runs at agent session start. On `TRUST_ROOT_LOST`, the session is refused to start with a dedicated error; only a `forensic_session` type can be initialized, whose available tool set is restricted to W3 emitters and read-path queries.
    - **Stacked states:** Evaluated in the same precedence as Path A (TRUST_ROOT_LOST → CIRCUIT_TRIPPED → BURST_SUSPENDED), applied inside the tool-call hook.

**Tradeoffs decided:**
- **Nested-delegation outline provided, implementation v2** — maintains a clean v1 implementation surface while committing to a forward-compatible shape.
- **Anthropic-API as external dependency** — surfaces the trust implication explicitly rather than hiding it.
- **Tool-call hook pattern over graph-node pattern** — matches SDK idiom; costs a hook on every tool call (acceptable latency).

**Open questions (deferred):** OQ-PATHB-1 (nested delegation token full spec) — v2 per §6. OQ-PATHB-2 (multi-principal API-key rotation policy) — v2.

**Interface contract:**
- **IC-PATHB-HOOK (new):** Every Path B agent session MUST install the pre-tool-call guard hook. Violation of the hook-installation contract is a harness build-time verification failure.
- **IC-PATHB-DELEG-OUTLINE (documentation contract, v2-scoped):** The 11-field nested delegation token shape specified in C-PATHB-1 is the v2 implementation target; v1 harnesses MUST reject nested delegation at runtime with `DELEGATION_NESTED_NOT_SUPPORTED_V1` (SECURITY, async, W1).

---

### GAP-4/C — Path C (Hybrid: LangGraph outer + Claude Agent SDK inner) — Conditional Spec Block

**Activates on:** Operator selection of Path C at harness-build time.

**What it must do / represent / enforce / guarantee:**
Specify how a hybrid orchestrator (LangGraph handling the outer workflow DAG, Claude Agent SDK handling inner agent-to-agent and agent-to-tool flow) satisfies the harness's control-plane requirements, with explicit attention to the boundary between the two layers.

**Hard constraints:**
- **C-PATHC-1 (Delegation Token Shape):** Path C uses BOTH token forms. The outer LangGraph layer uses the flat §10.4 nine-field Invocation Token between graph nodes. When a LangGraph node dispatches to a Claude Agent SDK inner session, the outer-invocation token becomes the parent of the inner session's tokens per the C-PATHB-1 nested delegation shape. The boundary crossing — LangGraph node → Agent SDK session — MUST produce an explicit `BOUNDARY_DELEGATION_TOKEN_ISSUED` Ledger entry (SECURITY, sync, W1) that cross-references outer and inner tokens. Nested-within-nested (Agent SDK → sub-Agent SDK) is v2-deferred; Path C v1 supports only one level of Agent SDK nesting.
- **C-PATHC-2 (HIL Mechanism):** HIL is implemented at **both** layers. Outer LangGraph `interrupt()` for workflow-level HIL (e.g., Genesis approval). Inner Agent SDK `request_user_input` for agent-level HIL (e.g., ambiguous tool parameter resolution). Both route through IC-REVIEW-QUEUE. The queue item payload includes a `layer: outer|inner` field so operators can distinguish layer context. Resumption is per-layer: outer resume does not resume inner; inner resume does not resume outer.
- **C-PATHC-3 (2PC TC Placement):** The TC is accessed **from the inner Agent SDK layer only**, as a tool exposed to agents (same as Path B C-PATHB-3). Outer LangGraph nodes do not call TC directly. Rationale: 2PC is a fine-grained operation corresponding to individual write transactions, which is an inner-agent concern; exposing it at the outer layer would fragment the 2PC state across layer boundaries.
- **C-PATHC-4 (Trust Boundary):** The LangGraph outer layer and the Agent SDK inner layer both run in-harness. The boundary between them is a **typed boundary** — outer → inner invocation is mediated by a `InnerSessionRequest` structure whose fields are structurally validated before the inner session starts (schema hash pinned at Tier 1). Malformed boundary invocations produce `BOUNDARY_INVOCATION_REJECTED` (SECURITY, sync, W1) and do not start the inner session.
- **C-PATHC-5 (GAP-56 Worst-Case Genesis Density):** Path C inherits the higher of Path A's and Path B's densities — **≤ 4 per 10-minute window** in a worst-case where an outer-workflow-triggered Genesis is accompanied by inner Agent-SDK skill-Genesis sub-ceremonies. Still below C-CAKB-1 (N=5). **Path C is confirmed path-safe under C-CAKB-1.** Operators running workflows that approach N=4 MUST instrument the Genesis-density metric at the outer layer and raise an operational alert at N=4/10min (one below threshold) to preempt accidental breach.
- **C-PATHC-6 (GAP-57 Build/Distribution Model):**
    - **Build model:** Operator-built single binary bundling both LangGraph and Agent SDK (and the Anthropic-API client). `operator_root_public_key` embedded at compile per C-BOOT-5.
    - **Reproducible-build contract:** `reproducible-build-manifest.json` per the pattern in C-PATHA-6 / C-PATHB-6, with both wheel hashes.
    - **Patch distribution:** Source-tree-delta model. The hybrid's dependency surface is the larger of the two single-path cases, increasing patch frequency and rebuild cost — operators SHOULD plan for more frequent reproducible-rebuild cycles than pure Path A.
    - **Verification:** Single maintainer signing key. Operators responsible for both the outer-layer workflow trust posture AND the Anthropic-API trust posture (from Path B).
- **C-PATHC-7 (GAP-58 State-Lifecycle Handling):**
    - **`BURST_SUSPENDED` handling:** Both layers consult the state. Outer LangGraph uses the guard-node pattern (C-PATHA-7). Inner Agent SDK uses the pre-tool-call hook (C-PATHB-7). The inner-layer hook is authoritative for any ceremony-affecting tool call — the outer layer's guard is a fast-path early rejection, but correctness is inner-layer-enforced.
    - **`TRUST_ROOT_LOST` handling:** The outer LangGraph entry guard short-circuits to `forensic_only` subgraph as in Path A (C-PATHA-7). The inner Agent SDK session guard refuses to start non-forensic sessions as in Path B (C-PATHB-7). Both are active; either triggering is sufficient for correctness.
    - **Stacked states:** Precedence evaluated at each layer identically (TRUST_ROOT_LOST → CIRCUIT_TRIPPED → BURST_SUSPENDED).
- **C-PATHC-8 (Boundary Audit Requirement):** Every outer-to-inner and inner-to-outer state transition MUST emit a Ledger entry (`BOUNDARY_TRANSITION_OBSERVED`, SECURITY, async, W1). This enables forensic reconstruction of cross-layer flows that would otherwise require correlating separate audit streams.

**Tradeoffs decided:**
- **2PC TC at inner layer only** — avoids cross-layer 2PC state fragmentation; constrains outer graph nodes to non-transactional orchestration.
- **One level of Agent SDK nesting only** — bounds the v1 complexity surface; nested-within-nested v2.
- **Dual-layer HIL** — higher queue volume, but cleaner layer-of-concern separation for operators.
- **Boundary audit entries required** — elevates audit cost; accepted for forensic completeness.

**Open questions (deferred):** OQ-PATHC-1 (nested-within-nested delegation) — v2. OQ-PATHC-2 (cross-layer state synchronization on `CIRCUIT_TRIPPED` — whether inner sessions should be proactively torn down or left to observe state on next tool call) — v2. OQ-PATHC-3 (boundary audit entry storage growth — potentially high-volume, may need sampling policy) — v2.

**Interface contract:**
- **IC-PATHC-BOUNDARY (new):** Every LangGraph-to-AgentSDK transition MUST go through the `InnerSessionRequest` typed channel. Direct calls from outer to inner bypassing this channel are a build-time verification failure.
- **IC-PATHC-DUAL-GUARD (new):** Both the outer guard-node pattern (IC-PATHA-GUARD) and the inner pre-tool-call hook (IC-PATHB-HOOK) MUST be installed. Neither alone is sufficient for Path C correctness.

---

## Part 3 — Independent Gap Resolutions

### GAP-9 — Probe Protocol Baseline Confirmation (Validation + MEMIT)

**Resolution:** The v2 GS10 probe protocol (three-member probe family: `generation`, `assertion`, `constraint`; Semantic Assertion Criterion; pinned-version judge-model classification) is **confirmed as the v1.1 implementation baseline** — not a formal deferral. Threshold calibration for `judge_model_classification` (specifically numeric ε values) remains an **implementation-phase activity pending GAP-1 empirical data**, but the protocol itself is complete and releasable.

**Disposition of OQ-W8:** Closed as **Partial** — (a) protocol resolved (closed by this session + GS10 probe-protocol definition), (b) numeric thresholds deferred pending GAP-1.

**Record:** D111 — "Probe protocol three-member family + Semantic Assertion Criterion + pinned-version judge-model classification is v1.1 baseline; numeric threshold calibration is implementation-phase, blocked on GAP-1 empirical data."

---

### GAP-13 — Genesis Automation v2 Outline (Warden + Orchestration)

**v2 Outline Block — Secondary LLM Reviewer as Genesis Human-Review Proxy:**

**Scope:** This outline addresses the v2 target of OQ-S5 — allowing a secondary LLM reviewer to serve as the human-review proxy before write engine execution of Architect Agent Genesis output patches, replacing the v1 mandatory human review.

**Properties the secondary LLM reviewer MUST satisfy (v2-design constraints):**
- **P-GR-1 (Independence):** The reviewer LLM MUST be a different model instance from any Coder, Architect, or Validator agent in the harness, AND MUST NOT share `.vindex` with those agents. Shared `.vindex` would mean the reviewer is reviewing patches that would affect its own future outputs — a self-referential review loop (cross-references GAP-49).
- **P-GR-2 (Pinned Version):** The reviewer model's version and weights snapshot hash MUST be pinned in Tier 1 `genesis-seal.json` at harness first-boot. Changes to the reviewer model require Genesis re-init (same constraint as judge-model, reinforcing frozen-instance pattern from GAP-49).
- **P-GR-3 (Review Output Contract):** The reviewer emits a structured `genesis_review_decision` with fields: `decision: APPROVE | REJECT | ESCALATE_TO_HUMAN`, `rationale: str`, `identified_risks: list`, `confidence_score: float`. `ESCALATE_TO_HUMAN` is not optional — the reviewer MUST have an escalation path, and the v2 harness MUST honor escalation.
- **P-GR-4 (Authorization Mechanism):** The reviewer's decision is cryptographically signed with a dedicated `genesis_reviewer_signing_key`, distinct from OOK and CAK, anchored in Tier 1 at harness first-boot. A signed `APPROVE` decision is the artifact consumed by the write engine as the v2 equivalent of the v1 human review attestation.
- **P-GR-5 (Audit Trail):** Every reviewer decision (APPROVE, REJECT, or ESCALATE_TO_HUMAN) is recorded in the Ledger as `GENESIS_REVIEW_DECISION_AI` (SECURITY, sync, W1), carrying the full decision record, the reviewer key signature, and the hash of the reviewed patch. REJECT and ESCALATE decisions produce Correctness Review Queue items for human operator awareness even when not blocking.
- **P-GR-6 (Trust Level):** The reviewer LLM is treated as a **write-authorizing agent** — on par with OOK in authority over Genesis patches — and therefore subject to all Warden contracts applicable to write-authorizing components: its key is mint-once in Tier 1; its pinned version is tamper-evident; its decisions are non-repudiable.

**v1 constraint (preserved):** Human review is mandatory in v1 (§10.6 step 1). v2 must not cross this without a new council session reviewing the P-GR-1 through P-GR-6 contract against empirical GAP-1 data about reviewer LLM reliability.

**Reference:** OQ-S5 (Open, v2-deferred). Feeds forward to a v2-planning council session.

---

### GAP-15 — Compaction Verification Sampling Deferral (Validation + MEMIT)

**Resolution:** Formal deferral confirmed. Per-tier sampling thresholds for SUPPORTING and INCIDENTAL knowledge classes, and abort thresholds, remain provisional pending GAP-1 empirical calibration. **CORE threshold (1.0, C-OC3) is non-provisional and stands as a released v1.1 constraint.**

**Disposition of OQ-OC3:** **Deferred-to-v2 / blocked by GAP-1.**

**Record:** D112 — "GAP-15 formally deferred; SUPPORTING and INCIDENTAL compaction sampling rates and abort thresholds are implementation-phase-calibrated pending GAP-1 empirical data. CORE 1.0 threshold remains non-provisional."

---

### GAP-17 — Voluntary Write Lock Release v2 Outline (Orchestration + SCT)

**v2 Outline Block — Voluntary Write Lock Release and Inter-Agent Negotiation:**

**Scope:** This outline addresses OQ-CW1 — enabling an agent holding a write lock to voluntarily release it before its work is complete, and negotiating write region ownership between agents with overlapping write interests.

**v2-design requirements:**
- **R-VWL-1 (Voluntary Release Ceremony):** A new ceremony type `VOLUNTARY_WRITE_LOCK_RELEASE` is required, initiated by the lock-holding agent. The ceremony MUST emit a Ledger entry (`WRITE_LOCK_VOLUNTARY_RELEASED`, GOVERNANCE, sync, W1) with fields: `releasing_agent_id`, `released_write_region_hash`, `partial_progress_ref` (if any — a hash of committed partial work), `reason: VOLUNTARY | NEGOTIATION | TIMEOUT`.
- **R-VWL-2 (Partial-Work Handling):** If the releasing agent has committed any partial work to `.vindex` before release, the partial-progress reference MUST allow a successor agent to either (a) build on the partial work, or (b) roll it back and start fresh. The choice is made by the successor, not dictated by the release ceremony.
- **R-VWL-3 (Inter-Agent Negotiation Channel):** A write-region negotiation message type is required — two agents with overlapping write interests exchange `WRITE_INTEREST_DECLARATION` messages through an Orchestrator-mediated channel. The Orchestrator grants the lock based on a priority policy (TBD in v2 — candidates: seniority, ceremony-scope-specificity, operator-configured weights). Negotiation is NOT a direct agent-to-agent channel.
- **R-VWL-4 (Consistency Guarantees Preserved):** v1 consistency guarantees MUST be preserved in v2 — the v1 invariant that a `.vindex` write region is owned by exactly one agent at any moment MUST remain true during negotiation. The negotiation protocol operates on lock-intent declarations, not on the lock itself; the lock transfers atomically via the release-then-acquire sequence.
- **R-VWL-5 (Timeout and Forfeiture):** A voluntarily-released lock without a successor within a configurable window produces a `WRITE_LOCK_ABANDONED` Ledger entry (SECURITY, async, W1) and any partial work is rolled back to the last committed state.
- **R-VWL-6 (Audit Completeness):** All negotiation messages are Ledgered. Lock transitions are Ledgered. No negotiation-layer state exists outside the Ledger — the Ledger is the authoritative negotiation history.

**v1 consistency guarantees that MUST be preserved:** Single-writer-per-region; no orphaned write regions; no cross-agent mid-write-region visibility.

**Reference:** OQ-CW1 (Open, v2-deferred). Outline input to a v2-planning council session.

---

### GAP-18 — Multi-Machine Ledger Replication v2 Outline (SCT)

**v2 Outline Block — Distributed Ledger Consistency Model:**

**Scope:** This outline addresses OQ-SL2 — multi-machine Ledger replication — including the interaction with the `ledger-archive/v1` canonical archive format (D104/GS9).

**v2-design questions to resolve:**
- **Q-MML-1 (Consistency Model Choice):** Sequential consistency (strong, operationally simple, lower throughput) vs. causal consistency (weaker, higher throughput, more complex application semantics). Recommendation to v2 council: sequential consistency — the harness's 2PC semantics already assume serialized commit ordering; causal would invalidate existing invariants in §11. A full model shift would require re-deriving §11 guarantees.
- **Q-MML-2 (Merkle-Chain Integrity Scaling):** Does the v1 Merkle-chain integrity model scale to replicated nodes? The current single-machine invariant is that every Ledger entry hashes its predecessor — a linear chain. Replication would require either (a) a **chain-per-leader** model (one linear chain per leader epoch, with leader transition entries linking chains), or (b) a **DAG-of-chains** model with explicit cross-node merge entries. Recommendation to v2 council: (a) chain-per-leader — preserves the linear audit invariant within a leader term, and the leader-transition entry becomes a cryptographic checkpoint the next leader's chain roots into.
- **Q-MML-3 (Leader-Election Requirements):** Leader election protocol required; must emit `LEADER_ELECTED` Ledger entry signed by ≥ ⌊N/2⌋+1 replicas. Candidates: Raft (well-understood, implementable), simplified paxos (theoretically purer but implementation-fragile). Recommendation to v2 council: Raft, with explicit Ledger-emission hooks at state transitions.
- **Q-MML-4 (D104 Interaction — `ledger-archive/v1`):** D104's canonical archive format is single-machine. Replication requires an extended format:
    - **Option (i):** `ledger-archive/v2` with a per-replica signature block and a replica-set membership manifest at archive-time.
    - **Option (ii):** Keep `ledger-archive/v1` as the per-replica format; add a new `ledger-replica-set-manifest/v1` artifact that cross-references all replica archives.
    - Recommendation to v2 council: **Option (ii)** — preserves D104 as-is; the replica-set manifest is a separate, composable artifact. Archive-time verification: each replica's archive integrity per D104; replica-set manifest integrity independently.
- **Q-MML-5 (Merkle-Chain Integrity Under Replication):** The v1 chain verification model DOES scale IF chain-per-leader is adopted (per Q-MML-2). The v2 integrity invariant becomes: "Every leader epoch is a linear Merkle chain; leader transitions are cryptographically linked via `LEADER_ELECTED` entries." Replay verification walks chain epochs in sequence.

**Reference:** OQ-SL2 (Open, v2-deferred). Outline input to a v2-planning council session.

---

### GAP-19 — OOK and CAK Rotation v2 Dependency Map (Warden)

**v2 Outline Block — Key Rotation Dependency Map:**

**Scope:** This outline enumerates every component with a boot-time or runtime binding to OOK or CAK, and what each requires from a key-rotation event. Special focus areas per the session brief: §13.5 step 3a (CAK boot verification), `ceremony_authorization_key_anchor` Tier 1 mint-once constraint, and historical CAK_REGISTERED chain preservation.

**OOK (Orchestrator Signing Key) — bindings:**
- **§10.4 Invocation Tokens:** All token signatures are OOK-signed. Rotation requires a signing-key transition protocol: old OOK remains valid for verification-only for a configurable overlap window; new OOK is the only signer during and after overlap. Ledger entry `OOK_ROTATED` (SECURITY, sync, W1).
- **§10.6 Genesis Security Protocol:** OOK is referenced in the Genesis approval chain. Rotation event must not invalidate in-flight Genesis ceremonies — a rotation mid-Genesis MUST either complete or explicitly abort the in-flight ceremony; partial-rotation-mid-Genesis is forbidden.
- **Delegation tokens (Path B/C v2):** If delegation is live at rotation time, delegation chains are signed with the old OOK; verification-only overlap window applies to delegation tokens.

**CAK (Ceremony Authorization Key) — bindings:**
- **§10.4 ceremony signatures:** All ceremony initiations are CAK-signed. Rotation model is analogous to OOK.
- **§13.5 step 3a (CAK anchor semantic verification at boot):** Adds a specific rotation concern — at boot, the harness verifies the CAK anchor against the Ledger's `CAK_REGISTERED` history. Rotation must ensure that:
    - **(a) Multiple historical CAK_REGISTERED entries:** The anchor verification iterates the chain, accepting the most recent `CAK_REGISTERED` as the current valid anchor, while retaining all prior entries as historical audit records. This requires an explicit policy: either a rolling window ("last N CAK_REGISTERED entries are inspected") or full-history ("every CAK_REGISTERED since Genesis is preserved and inspected"). Recommendation to v2 council: **full-history preservation, rolling-window verification** — audit is never lost; verification is bounded at step 3a.
    - **(b) CAK_COMPROMISED_AT_BOOT clearing:** If a prior CAK was flagged compromised (C-BG-7 / GAP-42), rotation to a new CAK does NOT implicitly clear the compromise flag — it produces a new `CAK_REGISTERED` entry that explicitly declares "supersedes compromised CAK [hash]". The `CAK_COMPROMISED_AT_BOOT` flag is cleared only when the new CAK's anchor is itself verified at a subsequent boot.
- **`ceremony_authorization_key_anchor` (Tier 1 genesis-seal.json, added GS5 v3 / A10):** This is the **mint-once barrier** — Tier 1 `genesis-seal.json` cannot be rewritten post-bootstrap. Rotation cannot simply update the anchor field. Required v2 mechanism:
    - **Option (x):** Define a `ceremony_authorization_key_anchor_chain` field (list of anchors, append-only), where each entry is a new CAK registration. Tier 1 is extended to accept appends to this field specifically, governed by a new mint-constraint exception. This is a carve-out from the mint-once principle — requires explicit Warden review.
    - **Option (y):** Maintain the anchor as a **root of a separate Ledger-resident chain** — Tier 1 stores only the original anchor; rotation produces Ledger `CAK_REGISTERED` entries that chain off the original anchor. Verification at §13.5 step 3a walks the chain from the Tier 1 root forward.
    - Recommendation to v2 council: **Option (y)** — preserves Tier 1 mint-once absolutely; rotation lives in the Ledger where its audit trail is native. No carve-out in the mint-constraint needed.
- **GAP-42 break-glass anchor (`break_glass_key_anchor`):** Same Tier 1 mint-once constraint; same Option (y) pattern recommended for v2. GAP-42 partially addresses OQ-S-CAK-1 by providing the second-anchor quorum model; the rotation of EITHER anchor (primary or break-glass) must follow this pattern.
- **OQ-S-CAK-2 (m-of-n CAK principals):** Remains OPEN for the rotation design. v2 council must decide whether rotation operates per-principal (each of m-of-n principals rotates independently, with a quorum-of-quorum during transition) or en-bloc (all m-of-n principals rotate together in a single ceremony). Leans en-bloc for operational simplicity; per-principal is more resilient. No v1 commitment.

**Interactions with §13.5 step 3a verification:**
- Boot verification MUST traverse the CAK rotation chain from Tier 1 root forward, verifying each `CAK_REGISTERED` entry's signature is produced by a valid predecessor-anchor.
- A broken chain (missing predecessor signature, signature invalid, gap in sequence) is a boot-time `TRUST_ROOT_LOST` trigger — the harness refuses to boot and enters the C-TRL-1 state.

**Reference:** OQ-S-CAK-1 (Partial — GAP-42 v1 mitigation; full rotation v2). OQ-S-CAK-2 (Open, v2). Outline input to a v2-planning council session.

---

### T15 — CAK Availability vs. Ceremony Urgency (Warden + Orchestration)

#### Amendment A11 — Applied This Session

**A11 — Deployment Guidance Clarification (Applied GS13):**

> "v1 supports exactly one registered Ceremony Authorization Key (CAK) anchor via `ceremony_authorization_key_anchor` in `genesis-seal.json` (Tier 1, added GS5 v3 / A10), plus optionally one registered break-glass second anchor via `break_glass_key_anchor` (GAP-42). The term 'backup custodian' as used in prior v1 deployment documentation refers to a second human with physical access to the primary CAK medium (e.g., HSM card custody partner), NOT to a second registered CAK. A second registered key is operationally available only via the GAP-42 break-glass anchor, which is a distinct Tier 1 anchor with its own quorum model (M ≥ 3 of N per C-BG-2), not a drop-in backup CAK.
>
> Deployment guidance is amended to explicitly state: the primary CAK is singular; backup custody arrangements are for the primary CAK medium (physical or cryptographic); the break-glass anchor is the sanctioned second registered key and is subject to its own quorum and use-constraints."

**Disposition of T15:** 🔶 **Partial**. GAP-42 break-glass second anchor **confirmed as satisfying the v1 CAK-availability mitigation requirement** — it replaces the prior "backup custodian to same medium" framing with a cryptographically stronger quorum mechanism, addressing the original T15 concern (availability under ceremony urgency) via a sanctioned second-anchor path.

**Remaining v2 item:** OQ-S-CAK-2 (m-of-n CAK principals) — the full resolution of CAK availability under all urgency scenarios, where the primary CAK itself is an m-of-n quorum rather than a single key. Tracked under GAP-19 v2 outline.

---

### OQ-SC3 — Reconciliation Workflow for STALE Layer 4 Facts (SCT + MEMIT)

**Disposition chosen: Option (c) — Distinct `STALE_FACT_REFRESH_REQUESTED` Ceremony Type.**

**Rationale:** Option (a) (Coder Agent auto-propose via standard pipeline) is rejected because Layer 4 external-source staleness is a **provenance-layer event**, not a knowledge-layer event — routing it through the standard pipeline would conflate staleness-driven refresh with any other Coder Agent write, losing the forensic distinction that the refresh is triggered by external-world drift rather than internal task completion. Option (b) (operator-flag-first) is operationally heavy for the common case and adds latency to routine refreshes. Option (c) introduces a ceremony that names the trigger explicitly, preserving forensic clarity while allowing a relatively light-weight operator confirmation per refresh.

**Hard constraints:**
- **C-SFR-1 (Ceremony Initiation):** `STALE_FACT_REFRESH_REQUESTED` ceremonies are initiated by the Pruning Agent's `external_source_audit` sub-routine upon detecting `EXTERNAL_PROVENANCE_STALE` on a specific fact. The ceremony carries fields: `stale_fact_ref`, `detected_stale_at_ledger_position`, `external_source_url`, `current_source_content_hash`, `prior_provenance_id`.
- **C-SFR-2 (Approval Gate):** The ceremony requires operator approval via the Reconciliation Review Queue (IC-REVIEW-QUEUE) before a refresh patch can be authored by a Coder Agent. Operator decisions: `approve_refresh` (dispatches Coder Agent with refresh scope), `reject_refresh` (fact remains STALE with advisory flag, per D101), `modify_scope` (operator-specified refresh scope adjustment), `defer_with_reason` (no action; fact remains STALE).
- **C-SFR-3 (D101 Compliance — Proposal-Only Authorization):** D101 explicitly prohibits auto-rewrite of Layer 4 facts. C-SFR-1 complies: the ceremony only authorizes the **proposal** phase — the Coder Agent is dispatched to author a refresh patch, which then enters the standard Validation → 2PC pipeline. The actual write remains gated by standard pipeline authorization. No auto-rewrite occurs at any point.
- **C-SFR-4 (CORE Facts Escalation):** For CORE-tier facts (per D101), `STALE_FACT_REFRESH_REQUESTED` ceremonies automatically raise `REQUIRES_HUMAN_REVIEW` — operator approval is mandatory and cannot be satisfied by any future v2 LLM-reviewer-as-proxy pattern. CORE staleness always reaches a human.
- **C-SFR-5 (Ledger Record):** Every `STALE_FACT_REFRESH_REQUESTED` initiation emits a Ledger entry (GOVERNANCE, sync, W1) regardless of operator outcome; every operator decision emits a subsequent entry. This creates a full audit chain from detection to decision to optional refresh patch.

**Tradeoffs decided:**
- **Dedicated ceremony over standard-pipeline routing** — preserves forensic distinction for external-source-driven writes.
- **Operator-gated proposal over auto-proposal** — aligns with D101 spirit even at the proposal phase; the proposal itself consumes external-source content whose trust posture is the operator's to attest.
- **CORE escalation mandatory** — CORE facts have stricter lifecycle than SUPPORTING/INCIDENTAL; staleness on CORE is an event requiring human judgment.

**Disposition of OQ-SC3:** **Resolved** via C-SFR-1 through C-SFR-5.

**Interface contract:**
- **IC-SFR-1 (new):** Pruning Agent external_source_audit sub-routine, on detecting EXTERNAL_PROVENANCE_STALE, MUST initiate `STALE_FACT_REFRESH_REQUESTED` ceremony with required fields per C-SFR-1. Any auto-rewrite path is forbidden (D101 reinforcement).
- **Appendix C additions:** `STALE_FACT_REFRESH_REQUESTED` (GOVERNANCE, sync, W1), `STALE_FACT_REFRESH_APPROVED` / `STALE_FACT_REFRESH_REJECTED` / `STALE_FACT_REFRESH_DEFERRED` (GOVERNANCE, sync, W1).

---

### GAP-32 — Batch Genesis Hold Release v2 Outline (Warden + SCT)

**v2 Outline Block — Batch Genesis Hold Release with Per-Hold Audit Trail:**

**Scope:** This outline addresses T16 — reconciling Warden's one-authorization-one-ceremony principle with SCT's operational need for batch ceremonies over N Holds. v1 specs the per-Hold path; v2 must introduce batch release while preserving per-Hold audit resolution.

**v2-design requirements:**
- **R-BGH-1 (Batch Ceremony Form):** A `BATCH_DEPENDENCY_HOLD_RELEASE_SIGNED` ceremony is initiated with a single CAK signature covering a **set** of Hold references (`hold_ref_list`, ordered, hashed collectively). The single signature binds all Holds atomically — either all are released or none are.
- **R-BGH-2 (Per-Hold Audit Trail Required):** Individual `DEPENDENCY_HOLD_RELEASED_SIGNED_BATCH_MEMBER` Ledger entries (GOVERNANCE, sync, W1) are written **per Hold** as a consequence of batch ceremony acceptance. Each entry carries: `hold_ref`, `batch_ceremony_id`, `batch_position_index`, `batch_total_count`, `batch_signature_hash`. This satisfies T16's audit-trail-per-Hold requirement while preserving the single-signature efficiency SCT requested.
- **R-BGH-3 (Scope Boundary):** Batch membership is capped in v2 config (`batch_hold_release_max_count`, candidate default 10). Batches above cap are rejected; operators must split into multiple batches. Rationale: batch auditability degrades beyond a manageable review scope.
- **R-BGH-4 (Homogeneity Requirement):** All Holds in a batch MUST share the same `release_reason` classification. Mixed-reason batches are rejected — the per-Hold reason must be consistent for the single-signature authorization to be operator-meaningful.
- **R-BGH-5 (Rollback Semantics):** If any one Hold-release in the batch fails the 2PC prepare phase (e.g., integrity check fails on one of the referenced Holds), the entire batch is rejected — no partial releases. The Ledger records `BATCH_DEPENDENCY_HOLD_RELEASE_REJECTED` with the failed position, preserving forensic attribution.
- **R-BGH-6 (Warden Principle Alignment):** The one-authorization-one-ceremony principle is preserved semantically: one CAK signature authorizes one ceremony, which atomically operates over a bounded, homogeneous, fully-audited set of Holds. The ceremony is the atomic unit; the Holds within it are the operations.

**T16 disposition:** **Resolved path specified** for v2. v1 remains per-Hold per §14. Full T16 resolution pending v2 implementation.

**Reference:** T16 (v2-target; per-Hold path specced for v1). Outline input to v2-planning council.

---

### GAP-27 — Tier Conflict Resolution: `scope_update_min_interval_seconds` Placement (Warden + SCT)

**Resolution:** `scope_update_min_interval_seconds` is **authoritatively placed in Tier 3 Anchored Git Config**, tunable via `rate-limits.json` post-bootstrap. This supersedes the v3 GS7 Tier 1 placement.

**Hard constraints:**
- **C-RL-1 (Authoritative Tier):** `scope_update_min_interval_seconds` resides in Tier 3 `rate-limits.json`. Operator-tunable. Changes are governed by the Tier 3 anchored-Git-config update flow (existing mechanism, §12.4 anchored config). Default value: 3,600s (as originally specified in v2 GS7).
- **C-RL-2 (Tier 1 Inappropriate):** Tier 1 mint-once is architecturally **inappropriate** for operational rate limits — these are tuning parameters whose correct value is learned through deployment experience, not fixed at Genesis. Placing them in Tier 1 would require Genesis re-init to adjust, which is disproportionate to the operational concern.
- **C-RL-3 (Dual-Layer Rate Limit Model Adopted):** The v2 GS7 dual-layer rate limit model is the canonical model for v1.1:
    - **Primary layer:** per-ceremony-initiator rate limit (`scope_update_min_interval_seconds` per initiating CAK principal).
    - **Secondary layer:** per-affected-agent-id rate limit (`scope_update_min_interval_per_agent_seconds`, candidate default 1,800s — half the primary, rationale: an agent may be the target of scope updates from multiple initiators, and a tighter per-agent cap prevents coordinated attacks that target a single agent through multiple principals).
    - Both limits are enforced simultaneously; a ceremony is rejected if **either** is breached. Rejection entry: `SCOPE_UPDATE_RATE_LIMIT_EXCEEDED` with `limit_layer: PRIMARY | SECONDARY | BOTH` field.
- **C-RL-4 (Change Protocol):** Tuning these values post-bootstrap follows the Tier 3 anchored-Git-config update flow — commit to the Git config branch, OOK-sign the commit per §12.4, apply on next config reload. No Genesis re-init required.

**Tradeoffs decided:**
- **Tier 3 over Tier 1** — operational tunability wins over immutability for parameters that are expected to be adjusted. Operators' ability to respond to observed deployment characteristics without Genesis re-init is critical.
- **Dual-layer over single-layer** — per-initiator alone is insufficient against coordinated multi-principal attacks on a single agent; per-agent alone loses the initiator-attribution dimension. Both together close the attack surface.
- **Dual-layer default ratio 2:1 (primary:secondary)** — accepted as a starting baseline subject to deployment calibration; documented as such in the Tier 3 config comments.

**Disposition:** v3 GS7 decision **SUPERSEDED**. v2 GS7 model **adopted as canonical**.

**Record:** D113 — "`scope_update_min_interval_seconds` placed at Tier 3 `rate-limits.json` per GAP-27 resolution; dual-layer model (per-initiator primary + per-affected-agent secondary) adopted; v3 GS7 Tier 1 placement superseded."

**Interface contract:**
- **IC-RL-1 (new):** Ceremony Gate evaluates both primary and secondary rate-limit counters on every `SCOPE_UPDATE` ceremony initiation. Rejection on either; rejection Ledger entry carries `limit_layer` field per C-RL-3.
- **Appendix C additions:** `SCOPE_UPDATE_RATE_LIMIT_EXCEEDED` (SECURITY, async, W1).
- **Tier 3 `rate-limits.json` schema additions:** `scope_update_min_interval_seconds` (default 3600), `scope_update_min_interval_per_agent_seconds` (default 1800).

---

### GAP-48 — Probe Set Versioning for ε Calibration (MEMIT)

**Resolution:** The `larql_fidelity_calibration` protocol's canonical probe set is **explicitly versioned**. When the probe set changes across Genesis updates, prior ε values are tagged as inapplicable to the new set.

**Hard constraints:**
- **C-PSV-1 (Version Field Location):** A `probe_set_version` field is added to `genesis-seal.json` (Tier 1). The field is a monotonically-incrementing integer, starting at 1 for the initial Genesis probe set.
- **C-PSV-2 (Calibration Record Tagging):** Every calibration protocol record (per D-GS8-A) carries a `calibrated_against_probe_set_version` field. Records are comparable ONLY when their `calibrated_against_probe_set_version` values match.
- **C-PSV-3 (Version Bump Trigger):** A probe set version bump is required when any of the following occurs: (a) addition of new probes, (b) removal of probes, (c) modification of probe templates or assertion criteria, (d) change in the pinned judge-model version. The version bump is atomic with the Genesis update that introduces the change.
- **C-PSV-4 (Cross-Version Comparison Contract):** When an operator or agent compares ε values across versions, the harness emits a `CROSS_VERSION_EPSILON_COMPARISON_REQUESTED` advisory (DIAGNOSTIC, async, W2) and returns the values marked `INAPPLICABLE_CROSS_VERSION`. No silent cross-version comparison is permitted.
- **C-PSV-5 (Historical ε Preservation):** Prior-version ε values are NOT deleted on version bump. They remain in the calibration record history, tagged with their authoring version, and are queryable for forensic purposes (e.g., "what was the ε regime under probe set v3?").

**Tradeoffs decided:**
- **`genesis-seal.json` placement over calibration-protocol-record-only placement** — the probe set version is Tier 1 operational state; placing it in `genesis-seal.json` makes it mint-once per Genesis (consistent with the Tier 1 principle) and surfaces the version as a first-class Genesis attribute operators can reason about.
- **Monotonic integer over hash** — operationally simpler; the hash of the probe set is already available separately in the calibration record as `probe_set_hash`; the version integer is an ergonomic handle, not a substitute for the hash.
- **No silent cross-version comparison** — preserves calibration integrity; a false comparison could mislead a GAP-1 empirical calibration downstream.

**Relationships:** GAP-1 (empirical calibration consumes versioned ε streams — version tagging is prerequisite). T13 (M-threshold provisional — relates to how thresholds are re-calibrated across probe set versions).

**Interface contract:**
- **IC-PSV-1 (new):** `probe_set_version` field mint-once in `genesis-seal.json` at Genesis; incremented atomically with each Genesis update that changes the probe set per C-PSV-3.
- **`genesis-seal.json` schema extension:** `probe_set_version: int` (starts at 1).
- **Calibration record schema extension:** `calibrated_against_probe_set_version: int`.
- **Appendix C additions:** `CROSS_VERSION_EPSILON_COMPARISON_REQUESTED` (DIAGNOSTIC, async, W2).

---

### GAP-49 — Self-Referential Probing (Validation + MEMIT)

**Resolution:** Option (b) adopted — **a separate frozen judge-model instance not subject to harness writes**. This provides the strongest isolation between the verification function and the write stream it verifies.

**Hard constraints:**
- **C-FJM-1 (Isolation Requirement):** The judge model used in `judge_model_classification` probes MUST be a **separate model instance** whose weights and `.vindex` are NOT subject to harness `.larql` writes. The frozen instance is treated as a read-only probe target from the harness's perspective.
- **C-FJM-2 (Bootstrap Procedure):** The frozen judge-model instance is bootstrapped at harness first-boot from a reference model artifact (model weights + `.vindex` snapshot) whose hash is pinned in Tier 1 `genesis-seal.json` (`frozen_judge_model_weights_hash`, `frozen_judge_model_vindex_hash`). The bootstrap procedure:
    - (a) Loads the reference model into an isolated process namespace.
    - (b) Verifies the loaded weights and overlay match the Tier 1 pinned hashes.
    - (c) Marks the namespace read-only at the OS level (process is sandboxed from any harness write path).
    - (d) Emits `FROZEN_JUDGE_MODEL_BOOTSTRAPPED` (GOVERNANCE, sync, W1) with the verified hashes.
    - Bootstrap failure is a harness refusal-to-start condition — the harness does not enter operational state without a verified frozen judge model.
- **C-FJM-3 (Verification During Operation):** Every probe invocation against the frozen judge model verifies, at call-time, that the model's loaded weights and `.vindex` hashes still match the Tier 1 pins. Drift detection (any mismatch) triggers `FROZEN_JUDGE_MODEL_DRIFT_DETECTED` (SECURITY, sync, W1) and the harness enters a probe-suspended state until the frozen instance is re-verified or re-bootstrapped.
- **C-FJM-4 (Update Procedure):** Updates to the frozen judge model (new reference version) are treated as Genesis-equivalent changes — they require a Genesis re-init ceremony with the new hashes in Tier 1. No in-place update path; operators electing to move to a new judge-model version accept the full Genesis re-init cost.
- **C-FJM-5 (Probe Set Version Interaction):** A frozen-judge-model-version change triggers a `probe_set_version` bump per C-PSV-3(d) — prior ε values are inapplicable to the new frozen instance. The two version-bump mechanisms are co-extensive here by construction.
- **C-FJM-6 (Isolation Guarantee Against Orchestrator):** The frozen judge-model instance is isolated not only from direct harness writes but also from any orchestration layer instruction that could cause weight modification. Specifically: no LangGraph node (Path A/C) and no Agent SDK tool (Path B/C) has a write path to the frozen instance. Attempts produce `FROZEN_JUDGE_MODEL_WRITE_ATTEMPTED` (SECURITY, sync, W1) and are rejected at the process-boundary level.

**Tradeoffs decided:**
- **Option (b) over (a) and (c):** (a) version-pinning alone does not prevent drift if the judge model is in the write stream; (c) state-hash inclusion in reports is a diagnostic aid but does not isolate. Only (b) provides a structural guarantee.
- **Genesis re-init for updates** — high cost, but aligned with the frozen-instance design principle; any in-place update path would re-introduce the drift risk being defended against.
- **Drift detection at every probe call** — adds per-probe verification cost; accepted because the integrity guarantee is worth it and the hash check is a cheap operation relative to the probe itself.

**Relationship to GAP-9:** Reinforces the pinned-version judge-model classification protocol from v2 GS10 — GAP-49 specifies the structural mechanism that makes pinning enforceable.

**Interface contract:**
- **IC-FJM-1 (new):** Frozen judge-model instance exposes a read-only probe interface; any write-channel attempt is process-boundary-rejected per C-FJM-6.
- **`genesis-seal.json` schema extensions:** `frozen_judge_model_weights_hash`, `frozen_judge_model_vindex_hash`.
- **Appendix C additions:** `FROZEN_JUDGE_MODEL_BOOTSTRAPPED` (GOVERNANCE, sync, W1), `FROZEN_JUDGE_MODEL_DRIFT_DETECTED` (SECURITY, sync, W1), `FROZEN_JUDGE_MODEL_WRITE_ATTEMPTED` (SECURITY, sync, W1).

---

### GAP-50 — TGA Skill-Profile Divergence (Validation)

**Resolution:** **Closed by T-TGA-load triage (GS12).** Concentration of verification-artifact authorship in TGA is governed by D32–D33 (Session 4) and was confirmed acceptable for v1 in GS12's T-TGA-load triage — it is not an oversight.

**v2-reconsider flag recorded:** Reopen as a gap IF v1.1 operational evidence surfaces concrete quality degradation attributable to the authorship concentration (e.g., observed systematic blind spots in TGA-authored test suites discovered through post-deployment failure analysis). Reopening trigger is empirical, not speculative.

**Disposition:** **Closed.**

**Record:** Referenced under GS12 T-TGA-load closure; no new D-number assigned (re-confirmation of prior closure).

---

### GAP-51 — Provenance Record Lifecycle for Re-verified Layer 4 Facts (SCT + MEMIT)

**Resolution:** **Chain via `prior_provenance_id`** — successor provenance records link back to their predecessors via a `prior_provenance_id` reference. This preserves full audit history while clearly identifying the current authoritative provenance.

**Hard constraints:**
- **C-PRL-1 (Chain Linkage):** Every Layer 4 provenance record for a fact that has been re-verified carries a `prior_provenance_id` field pointing to the immediately preceding provenance record for the same fact. The chain terminates at the original (first-seen) provenance record, whose `prior_provenance_id` is null.
- **C-PRL-2 (Current-Record Pointer):** The fact's current provenance is identified by the most recent record in the chain (equivalently, the unique record for that fact with no successor). The harness maintains a `current_provenance_id` pointer in the fact's metadata; on re-verification, the pointer advances to the new record.
- **C-PRL-3 (Chain Record Required Content):** A successor provenance record MUST carry:
    - `prior_provenance_id` — link to predecessor.
    - `re_verification_triggered_by` — one of `STALE_DETECTION | OPERATOR_REQUESTED | PERIODIC_AUDIT`.
    - `prior_content_hash` — hash of the external source content that generated the predecessor provenance.
    - `current_content_hash` — hash of the external source content observed at re-verification time.
    - `drift_category` — `IDENTICAL | CONTENT_EVOLVED | SOURCE_MOVED | SOURCE_REMOVED` (a finite classification to aid forensic reasoning).
    - `re_verified_at_ledger_position` — the Ledger position at which re-verification completed.
- **C-PRL-4 (Immutability of Prior Records):** Prior provenance records are **immutable** once superseded. They are retained for audit; they cannot be rewritten or deleted. This is a consequence of the broader `.vindex` immutability contract.
- **C-PRL-5 (Chain Traversal Bound):** Chain length is unbounded in principle but, in practice, operators MAY apply a retention policy (Tier 3 config `provenance_chain_retention_depth`, candidate default: unlimited) beyond which old chain records are archived to the Ledger archive but dropped from `.vindex` hot path. Archival preserves integrity through Ledger inclusion; drop-from-hot-path is a storage optimization, not a deletion.
- **C-PRL-6 (Relationship to GAP-11):** GAP-11 resolved the initial provenance record format; GAP-51 extends that format with the chain fields. Initial provenance records (chain head) remain GAP-11-conformant; successor records are GAP-11-plus-chain-fields.
- **C-PRL-7 (OQ-SC3 Alignment):** Provenance chain updates produced by `STALE_FACT_REFRESH_REQUESTED` (OQ-SC3 / C-SFR-1) ceremonies MUST produce successor records conforming to C-PRL-3. The ceremony's `prior_provenance_id` output field is a required input to the Coder Agent's refresh patch authoring.

**Tradeoffs decided:**
- **Chain over extend-in-place:** Extend-in-place (mutating the existing record) would violate `.vindex` immutability; chain preserves immutability. Additionally, chain allows querying "what did we believe at Ledger position X" — a forensic capability that extend-in-place destroys.
- **Chain over replace:** Replace (discarding the predecessor) would lose audit history; the whole point of re-verification is to track evolution of beliefs, not to overwrite prior beliefs.
- **Unbounded chain in principle, operator-configurable archive policy:** Preserves full auditability while giving operators an operational lever if storage becomes a concern. Archive-to-Ledger preserves integrity; hot-path drop is a performance optimization.
- **Drift category classification:** A finite classification (four values) over free-text aids downstream tooling (dashboards, automated policy decisions) without becoming a schema-evolution bottleneck.

**Interface contract:**
- **IC-PRL-1 (new):** Layer 4 provenance record schema includes `prior_provenance_id`, `re_verification_triggered_by`, `prior_content_hash`, `current_content_hash`, `drift_category`, `re_verified_at_ledger_position`. Fact metadata includes `current_provenance_id`. Any re-verification ceremony that produces a successor provenance MUST populate all fields per C-PRL-3.
- **Appendix C additions:** none (re-verification completion is already Ledgered via the parent ceremony's completion entry; C-PRL-3 specifies the fields therein).

---

### GAP-55 — Aggregate-Detection Entry Type Convention (Warden + SCT)

**Resolution:** **Ratified as framework convention.** The three conventions from GAP-44 (`GENESIS_INITIATION_ABUSE_PATTERN`) and GS12 (`SCOPE_MISMATCH_AGGREGATE_ALERT`) are formalized as applicable to **all future aggregate-signal entry types**.

**Convention (ratified, applicable framework-wide):**
- **C-ADC-1 (SECURITY Category):** Every aggregate-signal Ledger entry type MUST carry the `SECURITY` category. Aggregate signals are, by definition, security-relevant — the purpose of aggregation is to detect patterns that evade single-event scrutiny.
- **C-ADC-2 (source_entry_hash_list Field):** Every aggregate-signal entry MUST include a `source_entry_hash_list` field enumerating the constituent event positions (or hashes) in the Ledger that produced the aggregate. This provides the forensic trail from aggregate back to individual events. Field shape follows the `contributing_event_positions` precedent from GS12 C-AGG-5.
- **C-ADC-3 (Cross-Linked Review Queue Item):** Every aggregate-signal entry MUST produce a cross-linked Correctness or Reconciliation Review Queue item (via IC-REVIEW-QUEUE). The Ledger entry carries the queue item ID; the queue item carries the Ledger entry position. Default routing is Correctness; aggregates with reconciliation implications (future aggregates that affect state-ledger consistency) may route to Reconciliation instead, declared per-aggregate-type.

**Scope:** The convention applies to GAP-44 (`GENESIS_INITIATION_ABUSE_PATTERN`, already conforming), GS12 (`SCOPE_MISMATCH_AGGREGATE_ALERT`, already conforming), and ALL future aggregate-signal types introduced by subsequent sessions or v2 work. New aggregate types that deviate from this convention require an explicit decision record justifying the deviation.

**Record:** D114 — "Aggregate-detection entry type convention (SECURITY category + source_entry_hash_list + cross-linked review queue item) ratified as framework-wide convention; applies to all future aggregate-signal types unless explicitly justified otherwise."

---

### GAP-56 — Genesis Ceremony Event-Count Modeling (Warden + SCT)

**Cross-reference:** Resolved inside the GAP-4 per-path specs — see C-PATHA-5 (Path A: ≤2/10min), C-PATHB-5 (Path B: ≤3/10min), C-PATHC-5 (Path C: ≤4/10min). All three paths confirmed path-safe under the C-CAKB-1 N=5/10min burst limit. No path-specific override required.

**Disposition:** **Resolved** via per-path density confirmations in GAP-4.

---

### GAP-57 — Per-Operator Harness Binary Implications (Warden + Orchestration)

**Cross-reference:** Resolved inside the GAP-4 per-path specs — see C-PATHA-6, C-PATHB-6, C-PATHC-6. All three paths specify:
- Single-binary build with `operator_root_public_key` embedded at compile (per C-BOOT-5).
- `reproducible-build-manifest.json` as a framework-level artifact specifying exact toolchain versions.
- Source-tree-delta model for security patches (operators rebuild).
- Maintainer signing key (separate from operator-root) as the root of patch trust.

**Disposition:** **Resolved** via per-path build/distribution models in GAP-4.

---

### GAP-58 — New State Lifecycle Integration (SCT + Warden)

**Cross-reference:** Resolved in Part 1 of this session — §11.8 Addendum A (`BURST_SUSPENDED`) and §11.8 Addendum B (`TRUST_ROOT_LOST`). Referenced by GAP-4 per-path specs at C-PATHA-7, C-PATHB-7, C-PATHC-7.

**Disposition:** **Resolved** via Part 1 addenda.

---

## Gap Session Summary Block

### GAPS RESOLVED

- **GAP-4** — Three conditional path specs produced (Path A LangGraph, Path B Claude Agent SDK, Path C Hybrid). Each block specifies delegation token shape, HIL mechanism, 2PC TC placement, trust boundary, and sections addressing GAP-56, GAP-57, GAP-58.
- **GAP-9** — v2 GS10 probe protocol (three-member probe family + Semantic Assertion Criterion + pinned-version judge-model classification) confirmed as v1.1 baseline. D111 recorded. OQ-W8 closed as Partial (protocol resolved; thresholds implementation-phase pending GAP-1).
- **GAP-27** — `scope_update_min_interval_seconds` placed at Tier 3 `rate-limits.json`; v3 GS7 Tier 1 placement superseded. Dual-layer rate limit model (per-ceremony-initiator primary + per-affected-agent-id secondary) adopted as canonical. D113 recorded. IC-RL-1 defined.
- **GAP-48** — Probe set versioning contract defined; `probe_set_version` field added to `genesis-seal.json`; calibration records tagged with `calibrated_against_probe_set_version`. IC-PSV-1 defined.
- **GAP-49** — Option (b) adopted: separate frozen judge-model instance, weights and `.vindex` pinned in Tier 1, no harness write path, drift detection at every probe call. IC-FJM-1 defined.
- **GAP-50** — Confirmed closed by T-TGA-load triage from GS12; v2-reconsider flag recorded (reopen only on empirical evidence of quality degradation).
- **GAP-51** — Chain-via-`prior_provenance_id` model adopted for re-verified Layer 4 facts; immutability of prior records preserved; drift category classification defined. IC-PRL-1 defined.
- **GAP-55** — Aggregate-detection entry type convention (SECURITY category + `source_entry_hash_list` + cross-linked review queue item) ratified framework-wide. D114 recorded.
- **GAP-56** — Resolved inside GAP-4 per-path blocks. All three paths confirmed path-safe under C-CAKB-1 with no override.
- **GAP-57** — Resolved inside GAP-4 per-path blocks. Common model: operator-built single binary, reproducible-build manifest, source-tree-delta patches, maintainer signing key for patch trust.
- **GAP-58** — Resolved via §11.8 Addendum A (`BURST_SUSPENDED`) and Addendum B (`TRUST_ROOT_LOST`). IC-BS-LIFECYCLE and IC-TRL-1 defined. Nine new Appendix C entries added.
- **OQ-SC3** — Resolved via `STALE_FACT_REFRESH_REQUESTED` ceremony (Option c). IC-SFR-1 defined. D101 compliance verified (proposal-phase authorization only; no auto-rewrite).
- **T15** — Disposed as 🔶 Partial. Amendment A11 applied this session (deployment guidance clarification: backup custodian ≠ second registered key; GAP-42 break-glass anchor is the sanctioned second-anchor path). GAP-42 confirmed as satisfying v1 CAK-availability mitigation. Remaining v2 item: OQ-S-CAK-2 (m-of-n CAK principals) tracked under GAP-19.

### GAPS PARTIALLY RESOLVED

- **GAP-9** — Protocol resolved; numeric threshold calibration remains implementation-phase blocked on GAP-1 empirical data.
- **GAP-19** — v2 outline complete (dependency map + Option (y) for `ceremony_authorization_key_anchor` rotation via Ledger-resident chain). Full rotation implementation remains v2-deferred. OQ-S-CAK-1 v1-mitigated via GAP-42; OQ-S-CAK-2 m-of-n remains open.
- **T15** — v1 mitigation confirmed (GAP-42 + A11). v2 full resolution via OQ-S-CAK-2 remains open.

### GAPS DEFERRED

- **GAP-13** — v2 outline produced (secondary LLM reviewer as Genesis human-review proxy; six required properties P-GR-1 through P-GR-6). v1 mandatory-human-review constraint preserved. OQ-S5 remains Open / v2-deferred.
- **GAP-15** — Formal deferral confirmed. SUPPORTING and INCIDENTAL sampling thresholds blocked by GAP-1 empirical data. CORE 1.0 threshold (C-OC3) non-provisional and released. OQ-OC3 remains Deferred-to-v2.
- **GAP-17** — v2 outline produced (voluntary write lock release ceremony + inter-agent negotiation channel requirements). v1 consistency guarantees enumerated. OQ-CW1 remains Open / v2-deferred.
- **GAP-18** — v2 outline produced (sequential consistency recommended; chain-per-leader Merkle model; Raft leader election; `ledger-replica-set-manifest/v1` as D104 interaction solution). OQ-SL2 remains Open / v2-deferred.
- **GAP-32** — v2 outline produced (batch ceremony with per-Hold audit trail via `DEPENDENCY_HOLD_RELEASED_SIGNED_BATCH_MEMBER` entries; T16 path to full resolution specified). v1 per-Hold remains authoritative. T16 remains v2-target.

### NEW GAPS SURFACED

None of blocking significance for v1.1. The following v2 items are forward-referenced from this session:

- **OQ-PATHB-1** (Path B full nested delegation token spec) — v2-deferred per §6.
- **OQ-PATHB-2** (Path B multi-principal API-key rotation policy) — v2-deferred.
- **OQ-PATHC-1** (Path C nested-within-nested delegation) — v2-deferred.
- **OQ-PATHC-2** (Path C cross-layer state synchronization on `CIRCUIT_TRIPPED` — proactive inner teardown vs. observe-on-next-call) — v2-deferred.
- **OQ-PATHC-3** (Path C boundary audit entry storage-growth sampling policy) — v2-deferred.

These are properly v2 scope (path-specific nested delegation is explicitly v2 per §6) and do not destabilize v1.1. They are enumerated here for v2-planning visibility.

### NEW TENSIONS SURFACED

None. All tensions surfaced in prior sessions (T1–T16) are either resolved, partial with explicit v2 path, or v2-target. GS13 closed the remaining two tensions requiring action: T15 (disposed Partial with A11) and T16 (v2 path specified via GAP-32 outline). No new cross-domain tensions were identified this session.

---

**Session end.** All 14 planned resolutions + 3 cross-references completed. v1.1 spec baseline is now closed for pre-release gap work. Remaining activity: v2-planning council (forward-reference only; not blocking v1.1 release).

**Numbering continuity for any post-session work:**
- Next available decision ID: D115.
- Next available interface contract IDs: IC-BS-LIFECYCLE, IC-TRL-1, IC-PATHA-GUARD, IC-PATHB-HOOK, IC-PATHB-DELEG-OUTLINE, IC-PATHC-BOUNDARY, IC-PATHC-DUAL-GUARD, IC-SFR-1, IC-RL-1, IC-PSV-1, IC-FJM-1, IC-PRL-1 all assigned this session.
- Constraint prefixes introduced this session: `C-BS-*`, `C-TRL-*`, `C-PATHA-*`, `C-PATHB-*`, `C-PATHC-*`, `C-SFR-*`, `C-RL-*`, `C-PSV-*`, `C-FJM-*`, `C-PRL-*`, `C-ADC-*`.
