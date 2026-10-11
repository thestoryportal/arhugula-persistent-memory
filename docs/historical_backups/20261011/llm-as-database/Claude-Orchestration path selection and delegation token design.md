# Orchestration path selection and delegation token design

**Created:** 4/21/2026 19:15:24  
**Updated:** 4/21/2026 19:49:05  
**Exported:** 4/21/2026 19:50:19  
**Link:** [https://claude.ai/chat/9311c25b-c44f-4468-b688-55c9a403cac7](https://claude.ai/chat/9311c25b-c44f-4468-b688-55c9a403cac7)  

## Prompt:
4/21/2026, 7:15:25 PM

Gap Session 1 — Orchestration Comparativist
Context: This is a targeted gap resolution session for the LLM as Database
framework spec. The v1.1 integrated spec is complete. I am resolving specific
open questions from the gap backlog.
Gaps to resolve in this session:
### GAP-4
**Domain(s):** Orchestration Comparativist
**Priority:** 🟠 High
**Status:** Open — unaddressed in GS1–4
/orchestration-comparativist 
**Description:** Orchestration path selection (Path A / B / C) is operator-decided with no
spec recommendation (D72). Downstream: (a) nested sub-agent delegation token design is
path-dependent; (b) human-in-the-loop interface mechanism is path-dependent.
**Blocked by:** Operator path selection.
**Blocks:** Delegation token v2 spec shape; HIL interface mechanism spec.
```
At the end of each gap session, generate a session summary block:
```
Generate a Gap Session Summary Block:
GAPS RESOLVED: [list with resolution]
GAPS PARTIALLY RESOLVED: [list with what remains]
GAPS DEFERRED: [list with reason]
NEW GAPS SURFACED: [any that emerged during the session]
NEW TENSIONS SURFACED: [any cross-domain conflicts that appeared]
```
Save each summary as `gap-session-6-summary.md` as a downloadable markdown file.



## Response:
4/21/2026, 7:50:14 PM



````plaintext
Thought process: Prepared to address orchestration path selection gap systematically.

The user wants me to run Gap Session 6 focused on GAP-4 (Orchestration path selection) using the orchestration-comparativist skill. Let me first read the relevant skill and project files.
````

````plaintext
View: Reading orchestration-comparativist skill
````

````plaintext
Thought process

Now let me read the relevant project files - the gap backlog, tension map, previous gap session summaries, and the integrated spec.
````

````plaintext
View: Reading gap backlog v3
````

````plaintext
Thought process

Now let me read the gap session 5 summary and the relevant sections of the v1.1 integrated spec to understand the current state.
````

````plaintext
View: Reading gap session 5 summary
````

````plaintext
View: Listing project files
````





## Prompt:
4/21/2026, 7:18:02 PM

/orchestration-comparativist 

Gap Session 1 — Orchestration Comparativist
Context: This is a targeted gap resolution session for the LLM as Database
framework spec. The v1.1 integrated spec is complete. I am resolving specific
open questions from the gap backlog.
Gaps to resolve in this session:
### GAP-4
**Domain(s):** Orchestration Comparativist
**Priority:** 🟠 High
**Status:** Open — unaddressed in GS1–4
**Description:** Orchestration path selection (Path A / B / C) is operator-decided with no
spec recommendation (D72). Downstream: (a) nested sub-agent delegation token design is
path-dependent; (b) human-in-the-loop interface mechanism is path-dependent.
**Blocked by:** Operator path selection.
**Blocks:** Delegation token v2 spec shape; HIL interface mechanism spec.
```
At the end of each gap session, generate a session summary block:
```
Generate a Gap Session Summary Block:
GAPS RESOLVED: [list with resolution]
GAPS PARTIALLY RESOLVED: [list with what remains]
GAPS DEFERRED: [list with reason]
NEW GAPS SURFACED: [any that emerged during the session]
NEW TENSIONS SURFACED: [any cross-domain conflicts that appeared]
```
Save each summary as `gap-session-4_1-summary.md` as a downloadable markdown file.



## Response:
4/21/2026, 7:49:05 PM



````plaintext
Thought process

The user wants to run a gap session focused on GAP-4 (Orchestration path selection). Let me read the relevant files to understand the context - particularly the orchestration-related sections of the integrated spec and the orchestration requirements matrix.
````

````plaintext
View: Reading orchestration requirements matrix
````

````plaintext
Thought process: Navigated spec sections to address orchestration path dependencies.

Now I need to read specific sections of the integrated spec related to orchestration paths A, B, C, and the delegation token design and HIL interface. Let me look at the gap session schedule and relevant sections.
````

````plaintext
View: Reading gap session schedule for context on GAP-4
````

````plaintext
View: Reading gap-4 specific section from gap session schedule
````

````plaintext
Thought process: Examined orchestration framework gap requiring path selection specification.

Now let me look at the GS12 session description which contains GAP-4 content:
````

````plaintext
View: Reading GS12 content which covers GAP-4
````

````plaintext
Thought process: Synthesized GAP-4 framework and cross-referenced integrated specifications.

Now I have a comprehensive understanding of GAP-4. Let me also check the relevant section of the integrated spec for D72 and the three path specs.
````

Now let me read the relevant section of the v1.1 integrated spec covering D72 and the path definitions:

````plaintext
Tool: Searching project
````

````plaintext
Thought process: Excavated foundational spec blocks to resolve orchestration path selection gap.

Now I have a comprehensive understanding of what GAP-4 requires. Let me also check the Session 6 transcript for the full three-path spec blocks since those are the base for this gap session.
````

````plaintext
View: Reading transcript session 6 orchestration for path A/B/C spec blocks
````

````plaintext
View: Reading Path A B C spec blocks from Session 6
````

````plaintext
Thought process: Excavated prior specifications to map path-dependent downstream dependencies.

Now I have everything I need. Let me look at the specific delegation token and HIL interface content from the session 6 transcript and the Council session to understand what has already been specced for Path A/B/C regarding these two downstream items.
````

````plaintext
View: Reading delegation token and HIL content from session 6
````

````plaintext
Thought process: Gathered contextual details from prior Council session specifications.

Now I have all the context I need. Let me also check what the Council session (Session 7) produced regarding delegation tokens, since that was specced in detail there.
````

Now let me check what the Council session produced on delegation tokens - I recall it was addressed:

````plaintext
View: Searching Council session for delegation token spec
````

````plaintext
Thought process: Synthesized path-dependent delegation tokens and HIL mechanisms.

I have enough information now to run Gap Session 4.1 on GAP-4. Let me synthesize what I know:

1. **What GAP-4 requires:** Three contingent path specs (Path A, B, C) with:
   - (a) Delegation token shape for each path (especially nested sub-agent delegation)
   - (b) HIL interface mechanism for each path

2. **What's already been done:**
   - Session 6 produced full Path A/B/C spec blocks (D72), but deferred delegation token details and HIL mechanism details as path-dependent
   - Session 7 clarified that v1 tokens are invocation-scoped and Orchestrator-signed, with nested sub-agent calls handled separately under v2 delegation models, while the HIL interface was sketched at a high level through IC-OR6 but the actual pause/resume mechanics remain path-dependent.
   - The real blocker is that GAP-4 needs to produce three conditional spec blocks—one for each operator path choice—rather than waiting for path selection to happen first. Each block should define the delegation token shape and HIL interface mechanism specific to that path, activating only when the operator commits to that choice.

The Council already locked in the v1 token model for primary agent invocations: invocation-scoped, single-use, Orchestrator-signed across all paths. The path-dependent piece is narrower—it's about how nested sub-agent delegation works (relevant for Paths B and C where SDK subagents spawn further subagents) and how the HIL delivery mechanism adapts per path. The token shape itself varies by path, so I need to work through what that looks like for each one.

For Path A, the agent is just a LangGraph node calling an LLM directly—token issued per node execution, consumed at the Gate. Path B is where it gets interesting: the orchestrating SDK agent spawns subagents like Coder or Validator, and each subagent needs its own Gate token. The Orchestrator issues all tokens, but since the orchestrating agent is itself an SDK agent, the non-reasoning coordinator wrapper handles token issuance before spawning. Path C layers this further—LangGraph spawns an SDK agent inside a node, which then spawns its own subagents, following the same token issuance pattern.

For delegation tokens in v2, I need to figure out whether a parent can delegate write authority to a child without going back through the Orchestrator—v1 says no, but v2 will need to define how that chain works.

On the HIL side, Path A has the advantage of LangGraph's native interrupt mechanism—the workflow pauses at a node and human input flows through graph state updates, which is clean and first-class. Path B is different: the SDK has no native graph interrupt, so when HIL triggers, the orchestrating agent serializes its state to Postgres and halts, waiting for an external scheduler to reload and resume the session.

Path C splits the difference—it uses LangGraph's interrupt for the pause, then the LangGraph node re-invokes the SDK with the human decision as input, which is cleaner than Path B's external scheduling approach.

What I should actually produce here is three conditional spec blocks covering both delegation tokens and HIL mechanisms for each path, then a cross-path analysis showing where they diverge, and finally a recommendation block that surfaces what each choice commits the operator to downstream.

Now I'm pulling together the full session output, starting with a synthesis pass that accounts for inherited constraints: the v1 token model from the Council (single-use, invocation-scoped), the Warden's trust boundary with CeremonyToken and CAK signatures, and how the HIL mechanisms interact with circuit-breaker states—especially when a human is in the review loop and the circuit trips.

I need to trace the new `IC-HIL-RETURN` artifact (reviewer modify_patch → Validator cascade) across each path, then structure the session with conditional spec blocks for delegation token shape and HIL interface mechanics, followed by the IC-OR-DELEG stubs and a final summary.

Looking at the inherited open questions: path selection remains operator-deferred per OQ-OR1, which this session acknowledges by producing conditional specs rather than a recommendation. The invocation-scoped single-use Orchestrator token model from Council T5 means each agent gets its own token at Gate admission with no delegation chain in v1—so under Paths B and C where SDK subagents spawn further subagents, each one needs a fresh Orchestrator-issued token before spawning. I'm also tracking the GS4 ceremony implications as they affect the token lifecycle.

Now I'm working through the human-in-the-loop mechanics: CAK owns governance ceremonies exclusively, but HIL is not a ceremony—it's a human decision routed back through IC-OR6 and IC-HIL-RETURN, with the reviewer identity logged but no CeremonyToken required. The Orchestrator-to-Human Review Queue contract (IC-OR6) specifies the outbound payload, but the return path is path-dependent and that's what needs defining here. The skill already has the basic return states sketched—approved resumes the workflow, rejected triggers compensation—so I'm building on that foundation.

The return paths branch into four outcomes: approved continues normally, rejected with compensation, approved-with-modification sends the patched version back through the standard write gate, and escalated triggers a hard escalation. Each path needs its own delivery mechanism. No new persistent artifacts are being created in this session, so governance stays consistent with Session 6 and the Council. The outbound payload from IC-OR6 is locked in, but the inbound return mechanism—how the human decision actually re-enters the system—is the exact gap I'm closing now.

When the Orchestrator invokes an agent, it issues a single token scoped to that invocation, which the Patch Authorization Gate verifies. But under Paths B and C, subagents can spawn via the Claude Agent SDK, raising a question: does each subagent need its own Gate-authorized token? The parent agent can't issue one since it's an LLM without signing keys, so the Orchestrator must handle it—but the timing and mechanism shift depending on the path. The hard constraint from Council T5 is clear: no delegation bubbling, meaning a parent agent's token can't transfer authority downstream.

The structural challenge is that the Orchestrator needs to issue a subagent token before the subagent even exists. How it solves this depends on which path we're using. Under Path A, there's no nested SDK subagent layer at all—agents are just LangGraph nodes making direct LLM calls, so the Orchestrator pre-issues one token per node execution as the LangGraph engine enters each node.

Path B is different: the coordinator spawns SDK subagents that can themselves spawn further nested subagents, creating a chain that requires token issuance at each level. The constraint is that the coordinator must issue every token, not the parent agent. But here's the problem—the parent agent decides at reasoning time whether to spawn a subagent, so the Orchestrator can't know in advance which subagents will be needed.

The solution is a two-step protocol: when the parent agent decides to spawn a subagent, it emits a spawn request through its allowed tools; the coordinator intercepts this, issues a fresh token for the subagent, and delivers it with the spawn instruction. The token structure mirrors the v1 invocation token but adds a `parent_invocation_id` field to track lineage for auditing, without establishing delegation authority.

The subagent's token scope is constrained to its own Write Scope Definition—the parent can't grant broader permissions than the subagent's WSD allows. For Path C, which layers Claude Agent SDK inside LangGraph nodes, the same mediated issuance pattern applies, with the coordinator now operating at the node boundary.

The key advantage of Path C is that LangGraph's state model lets the `agent_invocation_node` wrapper intercept spawn requests before they leave the node, issue the token through the coordinator, and return it within a single execution cycle—cleaner than Path B's SDK hook layer interception.

Now I'm looking at the HIL interface mechanism and how it handles the 16 trigger events defined earlier. When any of these events fire, the Orchestrator needs to pause the workflow at a state boundary and submit...

Submitting the task package to the Human Review Queue while preserving the full graph state—including retry history and pending transaction status—in the LangGraph checkpointer, then waiting for human decision before resuming. The resume payload includes the human's decision (approved, rejected, modified, or escalated), their identity, an optional signature, and decision timestamp—plus conditional fields like a modified patch reference or rejection reason depending on the decision type. This approach is clean because LangGraph's thread model handles durability and suspend/resume as native primitives, so the human review surface just needs the thread ID to deliver the decision back into the graph state.

For Path B without native graph interrupts, the Orchestrator serializes the entire orchestration state—retry history, subtask progress, locks, pending transactions—to persistent storage when a human review is triggered, then issues the outbound call to the review queue and suspends the coordination job until the decision comes back.

An external scheduler polls for the human decision and, once it arrives, reconstructs the coordinator from the persisted state and reinjects the decision as a resumption input. The inbound payload includes the session ID, the decision itself (approved, rejected, modified, or escalated), reviewer metadata, and a reference to any modifications if the decision was conditional.

The main weaknesses here are serialization fidelity—if any in-memory state isn't serializable, the pause fails—plus the polling latency that delays resumption even for immediate approvals, and the risk that state reconstruction won't perfectly match the halted state. A ledger entry records the decision synchronously, just like Path A, but Path B introduces a unique failure mode if the pause itself can't be serialized.

Path C takes a different approach by leveraging LangGraph's native interrupt mechanism at node boundaries. When a HIL trigger fires during SDK agent execution, the runtime waits for the current node to complete before suspending cleanly rather than interrupting mid-execution. This creates a constraint: if a long-running agent is active when the trigger fires, there's a delay until that invocation finishes or times out. Orchestrator cannot suspend mid-SDK-call. It must allow the current SDK invocation to complete (or hit the invocation TTL ceiling), then suspend at the LangGraph node exit boundary, discarding the result if the HIL trigger invalidates the work. This is a minor hygiene concern—not blocking—but it means HIL triggers have a "next boundary" latency in Path C.

Wait and resume works identically to Path A via the LangGraph thread state API, with the SDK agent re-invoked fresh on the next node execution. The inbound payload is the same too: `{thread_id, hil_decision}` via state update. Path C is slightly cleaner than Path A for HIL because the SDK wraps the invocation cleanly; under Path A, raw API calls inside LangGraph nodes can be left in partial state if a HIL trigger fires mid-generation, whereas Path C uses the node boundary as the suspension granularity.

Now I'm identifying the new tensions that surfaced. The main one is that Path C's pause mechanism requires the current SDK invocation to complete before LangGraph can suspend at the node boundary—so if a long-running Coder Agent invocation fires when a HIL trigger is detected, there's a window where the trigger is recognized but the workflow can't pause cleanly until the SDK call exits.

There's also a secondary tension around subagent token issuance under the mediated model: every subagent spawn produces a new token and opens a scope lock region, so if an agent spawns many subagents in sequence, each one holds a scope lock during execution, and the 60-minute max-hold and concurrent lock limits interact with the spawn rate in ways that need flagging.

On the gaps side, I'm seeing that the `HIL_PAUSE_SERIALIZATION_FAILED` failure mode under Path B—where state serialization fails on HIL pause—needs a recovery strategy.  The spec needs to define what the Orchestrator does: emergency compensation, circuit trip, or something else. And the `SUBAGENT_SPAWN_REQUEST` tool call that the coordinator intercepts for mediated token issuance needs to be formalized as a tool contract with clear field definitions and rejection handling.

Both are medium-priority and path-specific, so I'll track them as sub-gaps under GAP-4. But stepping back, the session goal is to produce contingent spec blocks, not wait for path selection to resolve—so I should write the blocks conditional on each path and let the operator choose later.

By completing the conditional specs for all three paths on both the delegation token shape and HIL interface mechanism, I'm actually closing GAP-4 from the spec side. The operator can then activate whichever blocks match their chosen path. So GAP-4 is resolved once these contingent blocks are done, with the two new sub-gaps (HIL_PAUSE_SERIALIZATION_FAILED and SUBAGENT_SPAWN_REQUEST) tracked separately as medium-priority items.

Now I'm organizing everything into clean spec blocks.
````

I have everything I need. This is a substantial session — let me now execute the full orchestration-comparativist gap session for GAP-4.

---

# Gap Session 4.1 — Orchestration Comparativist
## Resolving GAP-4: Path-Conditional Delegation Token Shape + HIL Interface Mechanism

**Session identity:** GS-4.1 (out-of-sequence advance session on GAP-4, originally scheduled GS12)
**Skill invoked:** `/orchestration-comparativist`
**Status of GAP-4 entering session:** Open — unaddressed in GS1–4, externally deferred pending operator path selection (OQ-OR1 / D72)

---

## Framing: What "Blocked by Operator Path Selection" Actually Means

Before we dive into spec work, let's be precise about the blocker — because it matters for what this session can and cannot do.

**The blocker is real but bounded.** The operator has not selected Path A, B, or C (D72 / OQ-OR1). This means we cannot produce a *single* definitive spec for the two downstream items (delegation token shape and HIL interface mechanism). Those items genuinely differ by path in ways that can't be collapsed.

**What we CAN do — and what closes GAP-4 from the spec side:** Produce three conditional spec blocks — one per path — each fully speccing both downstream items. Each block carries the label: *"Activates on operator selection of Path [X]."* When the operator selects a path, that block becomes active spec; the other two are archived as considered alternatives.

**What this session does NOT do:** Select a path. That remains OQ-OR1, an operator decision. This session produces the decision's *consequences* fully enough that the operator can choose knowing exactly what they're committing to on each downstream item.

---

## Phase 1: Cross-Domain Synthesis Pass *(mandatory per skill — runs before any spec block)*

### 1.1 Open Question Cross-Read

**From Session 6 (D72 / OQ-OR1):** Path selection is explicitly deferred to operator. All three path spec blocks (Path A, B, C) are produced and comparable. **Orchestration implication:** This session extends those blocks with the two missing components. No new event or coordination protocol is introduced here — we are completing existing spec blocks.

**From Council Session 7 (T5 token model):** The invocation-scoped single-use Orchestrator-signed token model was ratified. The Council explicitly settled: *"Delegation tokens (sub-agent invocations under IC-OR5 Path B/C models) — v2. For v1, every invocation that reaches the Gate carries its own Orchestrator-signed token; nested sub-agent calls don't bubble up token authority."*

**Orchestration implication:** This decision constrains the path-conditional delegation token specs decisively. The v1 token shape is identical across all three paths for primary invocations. The path-dependent question narrows to: **how does the Orchestrator issue tokens for nested subagent spawns under Path B and C, given that it cannot pre-issue them (the parent LLM decides at reasoning time whether to spawn)?** Path A has no nested spawning layer and the question is moot.

**From GS4 (ceremony authorization / D93):** The CAK model covers governance ceremonies — scope updates, circuit resets, manifest ratification. HIL review decisions are NOT ceremonies in the CAK sense. A human reviewer delivering `{APPROVED}` via the HIL interface does not sign a CeremonyToken. The reviewer identity is recorded in a `HIL_DECISION_RECORDED` Ledger entry (GOVERNANCE, synchronous), but no ceremony authorization is required. **Cross-domain boundary confirmed:** Warden owns the ceremony authorization layer; the HIL inbound mechanism is Orchestrator-owned. No conflict.

**From Session 6 IC-OR6:** The outbound HIL payload is fully defined:
`{ task_id, pause_reason, patch_content_ref, validation_report_ref, scope_lock_ref, context_summary }`

The inbound return mechanism — how the human's decision re-enters the workflow — was **not** specced per-path in Session 6. IC-OR6 defines the outbound only. **This is the open half of the HIL contract. Closing it per path is what this session must deliver.**

**From the skill's Phase 1.5 requirement (IC-HIL-RETURN contract completeness):** A HIL trigger with only an outbound definition is incomplete. The skill mandates both: outbound payload AND inbound return mechanism. Session 6's IC-OR6 is incomplete. This session completes it — conditionally per path.

### 1.2 New Persistent Artifact Governance

Two new artifacts are introduced in this session:

| Artifact | Description | Governance Tier |
|---|---|---|
| `HIL_DECISION_RECORDED` (Ledger entry type) | Written synchronously on HIL resume, before workflow continues | Immutable ledger (Warden governance, Orchestrator write authority) |
| `HIL_PAUSE_SERIALIZATION_FAILED` (Ledger entry type — Path B only) | Written when state serialization fails on HIL pause attempt | Immutable ledger (SECURITY, synchronous) — triggers circuit trip |

Neither artifact conflicts with Session 3 (Warden audit trail patterns) or Session 5 (State Ledger Merkle-chain). `HIL_DECISION_RECORDED` follows the established GOVERNANCE/synchronous pattern. `HIL_PAUSE_SERIALIZATION_FAILED` is a new failure-mode entry type, following the SECURITY/synchronous pattern used for `CIRCUIT_TRIPPED`.

`SUBAGENT_SPAWN_REQUEST` is a tool contract (internal to agent runtime), not a persistent artifact. It does not require governance tier assignment. It produces a corresponding `TOKEN_ISSUED` Ledger entry per the established v1 token lifecycle (Council session T5).

### 1.3 HIL Contract Completeness Verification

| HIL trigger | Outbound defined (IC-OR6)? | Inbound return defined? | Status |
|---|---|---|---|
| Schema migration (all paths) | ✓ | ✗ — path-dependent | Closed by this session |
| Scope lock change (all paths) | ✓ | ✗ — path-dependent | Closed by this session |
| 3 consecutive scope failures (all paths) | ✓ | ✗ — path-dependent | Closed by this session |
| Integrity violation escalation (all paths) | ✓ | ✗ — path-dependent | Closed by this session |
| Compaction failure review (all paths) | ✓ | ✗ — path-dependent | Closed by this session |
| Diverged state review (all paths) | ✓ | ✗ — path-dependent | Closed by this session |

All 6 HIL trigger classes share the same outbound payload (IC-OR6) and the same inbound return mechanism (path-dependent, defined below). The payload is uniform; only the delivery mechanism differs by path.

Cross-domain synthesis pass complete. Requirements matrix does not need to be rebuilt — the Session 6 matrix is stable and still valid. We proceed directly to the path-conditional spec blocks.

---

## Delegation Token Shape — Background for All Three Paths

Before reading the path-conditional blocks, a quick grounding on how tokens work and why "delegation" is the right word for the problem:

**The v1 token model (established, Council Session 7):** When the Orchestrator invokes any agent, it issues a signed invocation token. The token is:
- **Invocation-scoped:** tied to one specific invocation ID
- **Single-use:** consumed at Gate admission; can never be re-used
- **Orchestrator-signed:** only the Orchestrator's signing key produces valid tokens
- **State-witness:** hash-bound to the current Write Scope Definition, Agent YAML, and scope lock ref at time of issuance

The token travels with the agent's output to the Patch Authorization Gate. The Gate verifies it before anything else.

**The delegation question:** Under Path B and Path C, agents can spawn subagents at runtime. The Coder Agent might spawn a Formatter subagent or a Linter subagent mid-task. These subagents are LLM instances — they have no signing key and cannot issue tokens to themselves. Someone must issue a token for each subagent. In v1, that someone is always the Orchestrator. The path-dependent question is: *how does the Orchestrator issue a subagent token for a subagent it didn't know would be spawned until the parent agent decided to spawn it?*

---

## Spec Block Series A: Delegation Token Shape — Path-Conditional

---

### Delegation Token Shape — Path A (LangGraph Alone) — Conditional Spec Block
*Activates on operator selection of Path A*

**What it must do / represent / enforce / guarantee:**
Under Path A, agents are LangGraph nodes that make direct LLM API calls. There is no nested subagent spawning layer — "subagents" don't exist as a structural concept. Each agent role (Coder, Validator, TGA, Architect) is a discrete LangGraph node with its own invocation token issued by the LangGraph coordinator before node entry.

The Orchestrator (LangGraph runtime + coordinator) issues one token per node execution, in advance, because the LangGraph graph structure is static and the set of node executions is known at graph compilation time. Token issuance is pre-execution: the coordinator issues the token immediately before invoking the node, not after the node decides what to do.

**Hard constraints:**
- One token per node execution. No exceptions.
- Token issued by coordinator, not by any agent or LangGraph primitive.
- Delegation is undefined and out of scope for Path A. No parent–child token relationship exists. Each node is a principal in its own right.
- The question of "nested delegation token design" (GAP-4's stated downstream item a) **does not apply under Path A**. The token shape is identically the v1 Council-ratified structure: `{ token_id, agent_id, invocation_id, task_id, scope_lock_ref, write_scope_hash, expected_yaml_hash, issued_at, expires_at, signature }`.
- No new `parent_invocation_id` field is added under Path A. The audit trail is flat: each invocation is a first-class event. Lineage tracing is handled by `task_id` (all nodes sharing a task share the same `task_id`).

**Tradeoffs decided:**
The flat token model over a delegated model is chosen because Path A has no structural need for delegation. Adding a `parent_invocation_id` field under Path A would embed an architectural concept (agent hierarchy) that the path doesn't have. The tradeoff accepted: task-level audit lineage is coarser than invocation-level hierarchy, but the `task_id` field is sufficient for the forensic purpose.

**Open questions (deferred):**
If LangGraph subgraphs are ever treated as independent principals in a future v2 path variant, the delegation question re-opens. Deferred to v2 under OQ-OR1 residual scope.

**Interface contract:**
- Coordinator → Gate: `TOKEN_ISSUED` Ledger entry at node entry; token fields as above.
- Gate verification order: signature → expiry → not-consumed → scope_hash match → yaml_hash match → scope_lock_ref valid → standard D22 Identity/Scope/Integrity checks.
- No new interface contract between coordinator layers required.

---

### Delegation Token Shape — Path B (Claude Agent SDK Alone) — Conditional Spec Block
*Activates on operator selection of Path B*

**What it must do / represent / enforce / guarantee:**
Under Path B, the orchestrating process (a non-reasoning coordinator wrapper, not an agent) spawns Claude Agent SDK agents. These top-level agents may themselves spawn subagents using the SDK's subagent spawning primitives. Each spawned subagent is an LLM instance that needs its own Orchestrator-issued token if it submits anything to the Patch Authorization Gate.

The structural challenge: the parent agent decides at *reasoning time* whether to spawn a subagent. The coordinator cannot pre-issue subagent tokens before it knows a spawn is coming. Therefore Path B uses a **mediated issuance** model:

1. The parent agent, when determining it needs a subagent, calls a special `SUBAGENT_SPAWN_REQUEST` tool. This is not a Gate-submitted patch — it's a coordinator-intercepted control call.
2. The coordinator intercepts the tool call (at the SDK hook layer), issues a fresh token for the requested subagent, and returns the token alongside spawn authorization.
3. The subagent is spawned with the token embedded in its invocation context.
4. The subagent proceeds with its Orchestrator-issued token, independent of the parent's token.

**V1 hard constraint inherited from Council (T5):** No authority bubbling. The subagent's token is issued against the subagent's own Write Scope Definition. The parent's scope does NOT transfer to the child. Even if the parent has broad scope, the spawned subagent is bounded by its own WSD.

**Token shape — Path B subagent tokens:** Identical to the v1 base structure, plus one additional field:
```
{
  token_id, agent_id, invocation_id, task_id,
  scope_lock_ref, write_scope_hash, expected_yaml_hash,
  issued_at, expires_at, signature,
  parent_invocation_id: string   ← NEW under Path B/C only
}
```

`parent_invocation_id` carries the parent agent's `invocation_id`. It enables audit trail lineage reconstruction without granting any authority. The Gate does NOT verify `parent_invocation_id` — it is an audit field only, not a security field.

**Spawn rejection handling:** If the coordinator receives a `SUBAGENT_SPAWN_REQUEST` for an agent whose scope would violate any active constraint (e.g., the requested subagent's WSD would conflict with the current scope lock), the coordinator MUST reject the spawn. The parent agent receives a `SPAWN_REJECTED` response. The parent must handle this gracefully — if it cannot proceed without the subagent, it returns failure to the coordinator, which applies the standard escalation cascade.

**`SUBAGENT_SPAWN_REQUEST` tool contract:**
```
{
  requested_agent_id: string,        -- must match a registered agent YAML
  task_id: string,                   -- inherited from parent invocation
  parent_invocation_id: string,      -- parent's invocation_id for lineage
  scope_hint: string (optional)      -- parent's semantic description of why spawn is needed
}
```
Response: `{ token: <subagent_token>, spawn_authorized: bool, rejection_reason: string? }`

**Hard constraints:**
- Coordinator is the sole token issuer. Parent agents never issue tokens.
- Subagent scope is bounded by the subagent's own WSD. Parent scope cannot be transferred.
- `parent_invocation_id` is an audit field, not a security field. Gate does not check it.
- Nesting depth limit: v1 specifies maximum one level of nesting (parent → subagent). A subagent may not spawn further subagents in v1. Reasoning: unlimited nesting creates an exponential token-issuance surface that is unspecced in v1. V2 may extend this.

**Tradeoffs decided:**
Mediated issuance over pre-issuance (issuing a pool of subagent tokens speculatively) is chosen because: (a) speculative tokens waste TTL and create abandoned-token audit noise; (b) mediated issuance preserves the principle that tokens are issued for specific, realized invocations only. The cost is the synchronous round-trip to the coordinator on each spawn — acceptable for v1 single-machine architecture.

**Open questions (deferred):**
- OQ-GAP4-1: Maximum nesting depth for v2 (v2 feature; v1 = max one level).
- OQ-GAP4-2: Whether the `scope_hint` field in `SUBAGENT_SPAWN_REQUEST` should be validated by the Warden (as a Gate pre-check) or treated as purely informational. Deferred — low-priority policy question.

**Interface contract:**
- Parent agent → Coordinator: `SUBAGENT_SPAWN_REQUEST` tool call (fields above).
- Coordinator → State Ledger: `TOKEN_ISSUED` entry at spawn authorization (same structure as top-level token issuance).
- Gate verification: identical to standard token verification; `parent_invocation_id` is logged but not verified.

---

### Delegation Token Shape — Path C (Hybrid: LangGraph + SDK) — Conditional Spec Block
*Activates on operator selection of Path C*

**What it must do / represent / enforce / guarantee:**
Path C uses LangGraph for control flow and SDK agents inside LangGraph nodes. When an SDK agent inside a node spawns a subagent, the same mediated issuance pattern applies as in Path B. However, the interception point is structurally cleaner: the `agent_invocation_node` wrapper (defined in Session 6 for Path C) intercepts the `SUBAGENT_SPAWN_REQUEST` at the LangGraph node boundary before it reaches the coordinator, issues the subagent token, and returns it to the SDK invocation — all within a single LangGraph node execution cycle.

**Path C advantage over Path B for delegation:** The `agent_invocation_node` wrapper is a well-defined interception point. Under Path B, interception happens at the SDK hook layer — correct but less structured. Under Path C, the LangGraph node boundary provides a clean seam where the coordinator can inspect, authorize, and token-issue for any subagent spawn before the SDK call proceeds. This makes the mediated issuance pattern more deterministic under Path C.

**Token shape:** Identical to Path B — the v1 base structure plus `parent_invocation_id`.

**Nesting depth limit:** Same as Path B — maximum one level in v1. Subagents spawned inside a LangGraph node may not spawn further subagents.

**Hard constraints:**
- All Path B constraints apply.
- Additionally: the `agent_invocation_node` wrapper is the interception point. Any `SUBAGENT_SPAWN_REQUEST` that bypasses the wrapper (e.g., an SDK agent using a low-level API call outside the wrapper) is an integrity violation. The Orchestrator MUST log `INTEGRITY_VIOLATION` if a subagent spawn is detected that did not produce a corresponding `TOKEN_ISSUED` Ledger entry.

**Tradeoffs decided:**
Same as Path B. Path C is preferred over Path B for mediated issuance specifically because the node boundary is a cleaner interception point than the SDK hook layer. This is one of the cases where Path C is strictly better than Path B, not just equivalent.

**Open questions (deferred):** Same as Path B — OQ-GAP4-1 and OQ-GAP4-2.

**Interface contract:**
- SDK agent inside LangGraph node → `agent_invocation_node` wrapper: `SUBAGENT_SPAWN_REQUEST` intercepted at node boundary before coordinator round-trip.
- `agent_invocation_node` wrapper → Coordinator: spawn authorization request.
- Coordinator → State Ledger: `TOKEN_ISSUED` (same as all paths).
- All other contracts identical to Path B.

---

## Spec Block Series B: HIL Interface Mechanism — Path-Conditional

---

### HIL Interface Mechanism — Path A (LangGraph Alone) — Conditional Spec Block
*Activates on operator selection of Path A*

**What it must do / represent / enforce / guarantee:**
LangGraph's native `interrupt_before` / `interrupt_after` graph execution primitives are the Path A HIL mechanism. This is the closest match between any evaluated orchestrator primitive and the HIL requirements established in Session 4 and Session 6.

**Pause mechanism:** The HIL gate node in the LangGraph execution graph is decorated with `interrupt_before`. When the Orchestrator routes execution into the HIL gate node (triggered by any of the 16 HIL trigger classes), LangGraph suspends the thread at that node boundary. The full graph state — including retry history, scope lock reference, pending 2PC status, task package, and consistency status — is persisted to the LangGraph checkpointer (Postgres-backed, per the SM-1 durability requirement). The thread is suspended, not terminated. No state is lost.

**Outbound (IC-OR6 completion — Path A):** The HIL gate node, before triggering the interrupt, writes to the Human Review Queue synchronously. The outbound payload is the existing IC-OR6 structure. The `thread_id` is appended as an additional field, allowing the human review surface to correlate its review record with the LangGraph thread that must be resumed.

**Wait mechanism:** The LangGraph thread rests in a `SUSPENDED` state indexed by `thread_id`. No active polling is required on the Orchestrator side. The Orchestrator writes a `HIL_PAUSED` Ledger entry (GOVERNANCE, synchronous) upon suspension, recording `{ thread_id, task_id, trigger_class, pause_timestamp, scope_lock_ref }`.

**Inbound return mechanism (IC-HIL-RETURN — Path A):**
The human review surface (operator-provided; the spec does not mandate a specific UI, but it must be able to call the LangGraph state update API) delivers the decision via:
```
POST /graph/update_state
{
  thread_id: string,
  hil_decision: {
    decision: "APPROVED" | "REJECTED" | "APPROVED_WITH_MODIFICATION" | "ESCALATED",
    reviewer_id: string,
    modified_patch_ref: string,        -- only if APPROVED_WITH_MODIFICATION
    rejection_reason: string,          -- only if REJECTED
    escalation_target: string,         -- only if ESCALATED
    decision_timestamp: ISO8601
  }
}
```

Upon receiving this update, LangGraph writes the `hil_decision` to thread state and schedules the thread for resumption. The coordinator, on resumption, reads the `hil_decision` from state before proceeding. A `HIL_DECISION_RECORDED` Ledger entry (GOVERNANCE, synchronous) is written by the coordinator immediately on resumption and before the workflow continues.

**Decision routing on resumption (identical across all paths):**
- `APPROVED` → workflow continues from the suspended node; scope lock remains held.
- `REJECTED` → Transaction Controller compensation path; scope lock released; `COMPENSATED` Ledger entry.
- `APPROVED_WITH_MODIFICATION` → modified patch re-enters at Gate L1 per IC-OR14; scope lock remains held through re-validation; modification ref logged in `HIL_DECISION_RECORDED`.
- `ESCALATED` → hard escalation; `SUSPENSION_LOGGED` Ledger entry; scope lock timeout clock continues; no automatic compensation.

**Hard constraints:**
- Scope lock is held active during the entire HIL pause. The 60-minute TTL clock (C-CW3) runs during the pause. If TTL expires during a long HIL review, scope lock auto-releases. The coordinator detects this on resumption and issues `SCOPE_LOCK_EXPIRED_DURING_HIL` (GOVERNANCE, async). The task must then re-acquire scope before continuing — this may require re-running the lock acquisition protocol.
- The Human Review Queue's human review surface MUST call the LangGraph state update API. The spec does not prescribe the human-facing tool; it prescribes the API call. The operator is responsible for providing a human review surface that wraps this call.
- Post-commit HIL abort: inherited from D74. If the HIL trigger fires after `COMMITTED` has been written to the Ledger, the HIL pause still proceeds — but the `REJECTED` routing cannot invoke the compensation path for the already-committed operation. The coordinator writes `HIL_ABORT_REJECTED_POST_COMMIT` (GOVERNANCE, synchronous) and the human reviewer is notified that rejection of a committed operation is not actionable.

**Tradeoffs decided:**
LangGraph's native interrupt over a custom pause/resume mechanism is the obvious choice for Path A. The tradeoff accepted: the Human Review Queue must integrate with the LangGraph state update API, which creates a coupling point between the human review surface and the orchestrator. The benefit — durable, first-class thread suspension — outweighs the coupling cost for v1.

**Open questions (deferred):** OQ-OR3 (abort authority actor scope) remains operational policy, not affected by path selection.

**Interface contract:**
- Orchestrator → Human Review Queue: IC-OR6 outbound payload + `thread_id` appended.
- Human Review Queue → Orchestrator (via LangGraph API): `{ thread_id, hil_decision }` as above.
- Orchestrator → State Ledger: `HIL_PAUSED` on suspension; `HIL_DECISION_RECORDED` on resumption.
- IC-OR14 (modified patch routing) applies unchanged.

---

### HIL Interface Mechanism — Path B (Claude Agent SDK Alone) — Conditional Spec Block
*Activates on operator selection of Path B*

**What it must do / represent / enforce / guarantee:**
Path B has no native graph-interrupt primitive. HIL pause under Path B is a controlled serialization halt followed by external scheduler-driven resumption. This is the weakest HIL story of the three paths. It is operationally correct but has failure modes that Path A and C do not.

**Pause mechanism:**
When the Orchestrator (coordinator wrapper) detects a HIL trigger, it must:
1. Complete or cancel the current SDK agent invocation cleanly (cannot halt mid-call). If the invocation is in-flight, the coordinator waits for exit or applies the token TTL ceiling, then discards the invocation result if the HIL trigger invalidates the work.
2. Serialize the full orchestration state to the Postgres-backed external state store. The serialization bundle includes: `{ session_id, task_package, retry_history, scope_lock_registry_snapshot, pending_2PC_state, active_subagent_tokens, consistency_status_at_pause }`.
3. Write `HIL_PAUSED` Ledger entry (GOVERNANCE, synchronous): `{ session_id, task_id, trigger_class, pause_timestamp, scope_lock_ref }`.
4. Issue the IC-OR6 outbound call to the Human Review Queue with `session_id` replacing `thread_id`.
5. Halt the coordinator process (or mark the coordination job as `SUSPENDED` in the external job scheduler).

**Serialization failure handling:** If step 2 fails — any in-memory state cannot be serialized — the coordinator MUST NOT halt. Halting with a failed serialization bundle leaves the workflow in an unrecoverable state. Instead:
- The coordinator writes `HIL_PAUSE_SERIALIZATION_FAILED` (SECURITY, synchronous) to the Ledger.
- The coordinator triggers `CIRCUIT_TRIPPED` per the established circuit breaker protocol.
- No HIL pause occurs. The task is logged as abandoned.
- Human review is still notified, but of the serialization failure, not the original HIL trigger.

**Wait mechanism:** An external scheduler (e.g., Celery, or a simple Postgres job queue) polls the Human Review Queue for decisions on `session_id`s marked SUSPENDED. When a decision arrives, the scheduler triggers coordinator resumption.

**Inbound return mechanism (IC-HIL-RETURN — Path B):**
The human review surface delivers the decision by writing to the job queue / review decision store (operator-provided). The scheduler picks up the decision and calls:
```
coordinator.resume(
  session_id: string,
  hil_decision: {
    decision: "APPROVED" | "REJECTED" | "APPROVED_WITH_MODIFICATION" | "ESCALATED",
    reviewer_id: string,
    modified_patch_ref: string,
    rejection_reason: string,
    escalation_target: string,
    decision_timestamp: ISO8601
  }
)
```

The coordinator deserializes the Postgres state bundle, reconstructs orchestration state, writes `HIL_DECISION_RECORDED` (GOVERNANCE, synchronous) before any further action, and proceeds with the decision routing defined above (identical across all paths).

**Path B-specific failure modes (not present in Path A or C):**

| Failure | Cause | Response |
|---|---|---|
| `HIL_PAUSE_SERIALIZATION_FAILED` | Non-serializable in-memory state | Circuit trip; task abandoned |
| `HIL_RESUME_DESERIALIZATION_FAILED` | Postgres bundle corrupted or incompatible version | Circuit trip; requires operator intervention |
| Resume after scope lock expiry | HIL review > 60 minutes | Scope lock re-acquisition required before continuation |
| Scheduler failure during HIL wait | Job scheduler outage | Manual resume trigger required; GOVERNANCE alert |

**Hard constraints:**
- Serialization MUST be complete and verified before the coordinator halts. A partial write and halt is a consistency violation.
- The scope lock TTL clock runs during HIL pause (same as Path A). Path B operators should provision a reviewer SLA shorter than the 60-minute scope lock TTL, or provision scope lock extension as an operator procedure.
- The scheduler MUST NOT call `coordinator.resume()` more than once for a given `session_id`. Duplicate resume calls are double-execution attacks. The coordinator checks for a `HIL_DECISION_RECORDED` Ledger entry for the `session_id` before processing a resume call — if one exists, the duplicate is rejected.

**Tradeoffs decided:**
Controlled-halt-and-serialize over a custom session-suspension library is chosen because Path B's SDK model has no better option — the SDK doesn't provide a suspend/resume primitive. The tradeoffs accepted: (a) serialization failure is an additional circuit-trip surface, (b) scheduler dependency adds an operational component with its own failure modes, (c) resume latency is bounded by the scheduler poll interval (not zero). Operators who find these tradeoffs unacceptable should select Path A or C.

**Open questions (deferred):** OQ-GAP4-3: Minimum recommended scheduler poll interval for HIL resume under Path B — operational policy, not spec. Suggested default: 60 seconds. Operator may reduce.

**Interface contract:**
- Orchestrator → Postgres state store: full serialized bundle at pause (fields above).
- Orchestrator → Human Review Queue: IC-OR6 outbound payload with `session_id` substituting `thread_id`.
- Human review surface → Job queue: decision payload (operator-provided surface; spec prescribes payload, not UI).
- Scheduler → Coordinator: `coordinator.resume(session_id, hil_decision)`.
- Orchestrator → State Ledger: `HIL_PAUSED` (synchronous, at pause); `HIL_DECISION_RECORDED` (synchronous, on resume, before workflow continues); `HIL_PAUSE_SERIALIZATION_FAILED` (SECURITY, if serialization fails).

---

### HIL Interface Mechanism — Path C (Hybrid: LangGraph + SDK) — Conditional Spec Block
*Activates on operator selection of Path C*

**What it must do / represent / enforce / guarantee:**
Path C inherits LangGraph's native `interrupt_before` / `interrupt_after` for the control-plane HIL pause. The SDK agent execution inside a LangGraph node creates one structural difference from pure Path A: HIL triggers that fire mid-SDK-invocation cannot immediately suspend the thread — LangGraph can only suspend at node boundaries.

**Pause mechanism:**
If a HIL trigger fires while an SDK agent is executing inside a LangGraph node:
1. The coordinator flags `HIL_PENDING` in LangGraph thread state.
2. The current SDK agent invocation is allowed to complete (or reach its TTL ceiling).
3. The `agent_invocation_node` wrapper, on detecting `HIL_PENDING` in thread state at node exit, does not pass the SDK result downstream. Instead, it routes execution to the HIL gate node.
4. LangGraph's `interrupt_before` at the HIL gate node suspends the thread at that boundary.

This introduces a **"next boundary" latency** for HIL under Path C: when a trigger fires mid-invocation, the pause does not take effect until the current SDK invocation exits. For typical LLM generation times (seconds to minutes), this is a tolerable delay. For long-running invocations (e.g., an architectural analysis agent), it may delay HIL response meaningfully.

**Mitigation for next-boundary latency:** The coordinator MAY issue an early cancellation signal to the SDK invocation if the HIL trigger priority is HIGH (e.g., integrity violation, circuit-adjacent event). The SDK's timeout/cancellation hook is the delivery mechanism. This is an operational option — not a hard constraint — because premature cancellation discards partial work that may be recoverable.

**Outbound, wait mechanism, and inbound return:** Identical to Path A — LangGraph's thread state update API is the delivery mechanism. The Path C inbound payload is identical to Path A's `{ thread_id, hil_decision }` structure.

**Decision routing on resumption:** Identical across all three paths (see Path A block above).

**Path C-specific edge case:** If the SDK invocation result is discarded because `HIL_PENDING` was set before it completed, the retry budget is NOT consumed. The node never received a result — this is infrastructure-level non-completion, not a task failure. The coordinator records `HIL_INVOCATION_DISCARDED` (GOVERNANCE, async) to distinguish discarded invocations from failed ones.

**Hard constraints:**
- Scope lock TTL behavior identical to Path A.
- Post-commit HIL abort: inherited from D74, identical to Path A.
- `HIL_PENDING` flag is authoritative. Once set, the `agent_invocation_node` wrapper MUST NOT pass any SDK result downstream, regardless of what the SDK produced.
- SDK invocation result discarded on `HIL_PENDING` does not burn retry budget (infrastructure non-completion, not task failure).

**Tradeoffs decided:**
The next-boundary latency tradeoff (over a hypothetical mid-invocation suspend) is accepted because mid-invocation suspension of an LLM call is not a well-defined operation — you cannot safely pause a token-generation process mid-stream. The latency is bounded by invocation duration, which has a TTL ceiling. The alternative (hard-killing the SDK invocation immediately) produces undefined partial state that is worse than the latency cost.

**Open questions (deferred):** OQ-GAP4-4: Whether the operator-provided early-cancellation signal to the SDK invocation should be a hard requirement for HIGH-priority HIL triggers, or remain advisory. Operational policy; deferred.

**Interface contract:**
- Coordinator → LangGraph thread state: `HIL_PENDING: true` on trigger detection.
- `agent_invocation_node` wrapper → HIL gate node: routes on `HIL_PENDING` at node exit; discards SDK result.
- HIL gate node → LangGraph: `interrupt_before` suspends thread.
- All other contracts identical to Path A (thread state update API, `HIL_PAUSED` / `HIL_DECISION_RECORDED` Ledger entries).
- Orchestrator → State Ledger: `HIL_INVOCATION_DISCARDED` (GOVERNANCE, async) on any discarded SDK result.

---

## IC-HIL-RETURN — Integrated Contract (Path-Conditional Summary)

The IC-OR6 outbound is path-independent (already specced in Session 6). The return mechanism is now fully specced per path:

| Component | Path A | Path B | Path C |
|---|---|---|---|
| Suspend primitive | LangGraph `interrupt_before` | Controlled halt + serialize to Postgres | LangGraph `interrupt_before` at next boundary |
| Wait handle | `thread_id` | `session_id` | `thread_id` |
| Resume trigger | LangGraph state update API | Scheduler → `coordinator.resume()` | LangGraph state update API |
| Inbound payload holder | `thread_id` | `session_id` | `thread_id` |
| Scope lock during wait | Held; TTL clock running | Held; TTL clock running | Held; TTL clock running |
| Failure modes introduced | None beyond scope lock expiry | Serialization failure, deserialization failure, scheduler failure | Next-boundary latency |
| `HIL_PAUSED` Ledger entry | ✓ Synchronous | ✓ Synchronous | ✓ Synchronous |
| `HIL_DECISION_RECORDED` Ledger entry | ✓ On resume | ✓ On resume | ✓ On resume |

**Hard constraint universal to all paths (IC-OR14 re-statement):** A reviewer-modified patch (`APPROVED_WITH_MODIFICATION`) MUST re-enter the write path at Gate L1. No path is exempt. The HIL mechanism can never route a modified patch directly to the Commit Executor.

---

## Cross-Path Comparison: What Path Selection Commits the Operator To

This table answers the question the operator needs answered before choosing:

| Commitment | Path A | Path B | Path C |
|---|---|---|---|
| Nested delegation token design (v1) | None (no nesting) | Mediated issuance via SUBAGENT_SPAWN_REQUEST | Mediated issuance via agent_invocation_node intercept |
| HIL pause mechanism | LangGraph native interrupt (cleanest) | Serialize-and-halt (most complex) | LangGraph native interrupt + next-boundary latency |
| New operational component required for HIL | None | External scheduler (Celery or equivalent) | None |
| HIL failure modes not in other paths | None | Serialization failure → circuit trip | Discarded SDK invocation on HIL_PENDING |
| Subagent token issuance | Pre-issued at node entry | Mediated on-demand via SUBAGENT_SPAWN_REQUEST | Mediated at agent_invocation_node wrapper |
| Max nesting depth (v1) | N/A | 1 level | 1 level |
| `parent_invocation_id` field in token | Not used | Required | Required |
| HIL resume latency | ~0 (state update API) | 1 scheduler poll interval | Next boundary (invocation duration bounded by TTL) |

---

## New Gaps Surfaced in This Session

### GAP-4a — `HIL_PAUSE_SERIALIZATION_FAILED` Failure Mode Full Spec (Path B)
**Domain:** Orchestration Comparativist (State Consistency Theorist secondary)
**Priority:** 🟡 Medium
**Description:** This session establishes that `HIL_PAUSE_SERIALIZATION_FAILED` triggers a circuit trip. But the precise failure behavior is underspecced: (a) what is the scope lock fate when serialization fails — auto-released or held until circuit reset? (b) what is the task fate — treated as escalation cascade Step 3 (Human Queue) or Step 4 (Suspension)? The circuit trip model (D84) governs subsequent behavior, but the transition into the circuit trip from a HIL serialization failure has a gap.
**Blocked by:** Nothing — self-contained.
**Blocks:** Nothing in v1 if Path B is not selected. Blocks clean Path B spec if selected.

### GAP-4b — `SUBAGENT_SPAWN_REQUEST` Tool Contract Full Spec (Path B and C)
**Domain:** Orchestration Comparativist (Warden secondary)
**Priority:** 🟡 Medium
**Description:** This session defines the `SUBAGENT_SPAWN_REQUEST` tool contract at the field level. What remains unspecced: (a) the Gate behavior when an intercepted spawn request would violate scope — does the Gate see the spawn request, or only the coordinator? The Warden should clarify trust boundary placement for spawn request interception; (b) whether `SUBAGENT_SPAWN_REJECTED` should be a Ledger entry type (it currently is not). These are spec completeness items, not blockers, but must be addressed if Path B or C is selected.
**Blocked by:** Nothing — self-contained.
**Blocks:** Nothing in v1 if Path A is selected.

### GAP-4c — Scope Lock Expiry During Extended HIL Review (All Paths)
**Domain:** State Consistency Theorist (Orchestration Comparativist secondary)
**Priority:** 🟡 Medium
**Description:** All three path specs note that the 60-minute scope lock TTL (C-CW3) runs during HIL pause. This is correct behavior, but the re-acquisition protocol on scope lock expiry mid-HIL-review is unspecced. Current spec: lock expired → `SCOPE_LOCK_EXPIRED_DURING_HIL` Ledger entry → re-acquisition required before continuation. But what does re-acquisition look like when the task is already mid-execution? Does the coordinator restart the task from the beginning, or from the last durable checkpoint? This is a State Consistency Theorist question with orchestration path implications.
**Blocked by:** Nothing.
**Blocks:** Clean HIL behavior for long-running human reviews under all paths.

---

## New Tensions Surfaced in This Session

### T-GAP4-A — HIL Responsiveness vs. Path C Node-Boundary Constraint
**Domains:** Orchestration Comparativist (primary); Validation Contract Architect (secondary)
**Description:** Path C's HIL mechanism delays suspension until the current SDK invocation exits. For integrity violation HIL triggers (which are high-urgency), this delay is potentially unacceptable — the invocation that produced the integrity violation is still running when the trigger fires, and it may produce further output during the "next boundary" window. The Validation Contract Architect's principle that integrity violations trigger immediate response conflicts with the structural constraint that LangGraph can only suspend at node boundaries.

**Proposed resolution (requires Warden and Orchestration Comparativist to ratify):** Integrity violation HIL triggers under Path C MUST issue an early cancellation signal to the in-flight SDK invocation (not advisory — mandatory). All other HIL trigger classes may use the standard next-boundary latency. This creates a two-tier HIL pause protocol for Path C: immediate-cancel for integrity triggers, next-boundary for all others.

**Status:** Unresolved — surfaces as a tension requiring ratification if Path C is selected.

### T-GAP4-B — Scope Lock Duration vs. Human Review SLA (Operational)
**Domains:** State Consistency Theorist; Orchestration Comparativist; operational policy
**Description:** The 60-minute scope lock TTL (C-CW3) was specced independently of the HIL review SLA. If human review routinely takes longer than 60 minutes (plausible for security-sensitive reviews, schema migrations, or overnight batches), scope lock expiry during HIL becomes a frequent event, not an edge case. GAP-4c captures the re-acquisition spec gap; this tension captures the broader policy question: should the scope lock TTL be extensible for HIL-paused tasks, or should the operator be required to design HIL workflows to complete within 60 minutes?

**Status:** Deferred to operational policy. A spec note will be added to IC-CW1 that *"Operators selecting any path SHOULD define a human reviewer SLA ≤ 55 minutes for tasks with active scope locks, OR provision the scope lock re-acquisition protocol (GAP-4c) before selecting a path."*

---

## GAP-4 Resolution Status

GAP-4 is now **RESOLVED from the spec side**. The two downstream items that the gap identified are fully specced across all three paths:

**(a) Nested sub-agent delegation token design:**
- Path A: moot (no nesting). V1 token model applies, unmodified.
- Path B: mediated issuance via `SUBAGENT_SPAWN_REQUEST` tool; v1 token structure + `parent_invocation_id` audit field; max 1 nesting level; no authority bubbling.
- Path C: mediated issuance at `agent_invocation_node` wrapper boundary; identical token structure as Path B; structurally cleaner interception.

**(b) HIL interface mechanism:**
- Path A: LangGraph native `interrupt_before`; state update API as inbound; cleanest model.
- Path B: serialize-and-halt; external scheduler; most operationally complex; new failure modes.
- Path C: LangGraph native interrupt at next boundary; early-cancel signal for high-urgency triggers (T-GAP4-A requires ratification); structurally close to Path A.

**Activation condition:** Each conditional spec block activates when the operator records a path selection decision that supersedes OQ-OR1. Until then, all three blocks remain in the spec as conditional alternatives. The backlog entry for GAP-4 should be updated to **RESOLVED (conditional — awaiting operator activation)**.

---

## Gap Session Summary Block

```
════════════════════════════════════════════════════════════════
GAP SESSION 4.1 — Orchestration Comparativist
Primary: GAP-4 (Orchestration path-conditional specs)
Output: Three conditional spec blocks × two downstream items
════════════════════════════════════════════════════════════════

GAPS RESOLVED
─────────────────────────────────────────────────────────────────
GAP-4 — RESOLVED (conditional — activates on operator path
  selection superseding OQ-OR1)
  
  Resolution: Three conditional spec blocks produced,
  each covering BOTH downstream items:
  
  (a) Delegation token shape:
    — Path A: v1 token unchanged; no nesting layer exists
    — Path B: mediated issuance (SUBAGENT_SPAWN_REQUEST tool);
              token + parent_invocation_id; 1-level nesting cap
    — Path C: mediated issuance at agent_invocation_node 
              boundary; identical shape to Path B; cleaner 
              interception point
  
  (b) HIL interface mechanism:
    — Path A: LangGraph interrupt_before; thread_id handle;
              state update API inbound; zero added failure modes
    — Path B: Serialize-and-halt; session_id handle; scheduler
              resume; HIL_PAUSE_SERIALIZATION_FAILED → circuit
              trip
    — Path C: LangGraph interrupt at next boundary; thread_id;
              mandatory early-cancel for integrity-violation
              triggers (T-GAP4-A pending ratification)

  New Ledger entry types introduced:
    HIL_PAUSED (GOVERNANCE, synchronous — all paths)
    HIL_DECISION_RECORDED (GOVERNANCE, synchronous — all paths)
    HIL_PAUSE_SERIALIZATION_FAILED (SECURITY, sync — Path B)
    HIL_INVOCATION_DISCARDED (GOVERNANCE, async — Path C)

  IC-OR6 (Session 6 outbound) extended:
    IC-HIL-RETURN now fully specced per path (inbound)

GAPS PARTIALLY RESOLVED
─────────────────────────────────────────────────────────────────
None — GAP-4 closed completely from the spec side.
Operator activation remains pending (OQ-OR1 still deferred).

GAPS DEFERRED
─────────────────────────────────────────────────────────────────
OQ-OR1 — Path selection — operator decision, not spec work.
  Status unchanged. All three conditional blocks are now 
  available for operator selection.

OQ-GAP4-1 — Max nesting depth for v2 (path B/C) — v2 feature.
OQ-GAP4-2 — scope_hint field validation policy — low priority.
OQ-GAP4-3 — Path B scheduler poll interval — operational policy.
OQ-GAP4-4 — Early-cancel as hard requirement vs advisory for 
  Path C HIGH-priority HIL triggers — deferred pending T-GAP4-A
  ratification.

NEW GAPS SURFACED
─────────────────────────────────────────────────────────────────
GAP-4a — HIL_PAUSE_SERIALIZATION_FAILED full failure-mode spec
  Domain: Orchestration + State Consistency
  Priority: 🟡 Medium
  Scope lock fate + task fate on serialization failure;
  path into circuit trip not fully specced.
  Activates only if Path B selected.

GAP-4b — SUBAGENT_SPAWN_REQUEST tool contract full spec
  Domain: Orchestration + Warden
  Priority: 🟡 Medium
  Trust boundary placement for spawn-request interception;
  SUBAGENT_SPAWN_REJECTED Ledger entry type.
  Activates only if Path B or C selected.

GAP-4c — Scope lock re-acquisition protocol mid-HIL-review
  Domain: State Consistency + Orchestration
  Priority: 🟡 Medium
  All paths affected. Re-acquisition on expiry during 
  extended HIL review not specced. GAP-4c assigned to
  SCT; Orchestration is secondary.

NEW TENSIONS SURFACED
─────────────────────────────────────────────────────────────────
T-GAP4-A — HIL Responsiveness vs Path C Node-Boundary Constraint
  Domains: Orchestration Comparativist × Validation Contract
  Architect (× Warden for early-cancel authorization)
  Status: UNRESOLVED — requires ratification if Path C selected
  Proposed resolution: Two-tier HIL pause for Path C — 
  mandatory immediate early-cancel for integrity-violation 
  triggers; standard next-boundary for all other trigger classes
  Session required: Can fold into Path C activation session 
  (no standalone session needed)

T-GAP4-B — Scope Lock Duration vs Human Review SLA
  Domains: State Consistency × Orchestration
  Status: DEFERRED to operational policy
  Mitigation note added: operators SHOULD define HIL reviewer 
  SLA ≤ 55 minutes for tasks with active scope locks, OR 
  provision GAP-4c re-acquisition protocol first
════════════════════════════════════════════════════════════════
```

Now let me save this as the downloadable file:

````plaintext
View: Reading framework-spec-writer skill before producing the file
````

````plaintext
Thought process: Assembled formal markdown documentation for gap session deliverable.

Now I have all I need to produce the formal downloadable file. Let me write the gap session summary as a proper markdown file.
````

Now I'll write the formal markdown file:

````plaintext
Create File: Creating gap session 4.1 summary markdown file
````

````plaintext
Bash Tool: Remove existing file and recreate
````

````plaintext
Create File: Creating gap session 4.1 summary
````

````plaintext
Bash Tool: List outputs and remove the existing file
````

````plaintext
Bash Tool: Running command
````

````plaintext
Bash Tool: Write gap session summary file using python
````

````plaintext
Bash Tool: Write full content to gap session file
````





---
Powered by [Claude Exporter](https://www.ai-chat-exporter.net)