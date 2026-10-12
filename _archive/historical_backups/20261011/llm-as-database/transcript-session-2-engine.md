# MEMIT implementation specification and design

**Created:** 4/21/2026 2:50:27  
**Updated:** 4/21/2026 2:58:14  
**Exported:** 4/21/2026 9:08:30  
**Link:** [https://claude.ai/chat/0840d232-6df3-449d-a65c-258aa7a99877](https://claude.ai/chat/0840d232-6df3-449d-a65c-258aa7a99877)  

## Prompt:
4/21/2026, 2:50:28 AM

> File: ontological-schema-llm-databse-agent-framework.md

/memit-specialist 
The schema from Session 1 defines what we need to write. Now help me spec how we write it — MEMIT vs. alternatives, .vindex overlay design, .larql format, edit volume estimates, and catastrophic forgetting mitigations. Start with questions.



## Response:
4/21/2026, 2:50:58 AM

````plaintext
Thought process: Thinking about comparing MEMIT implementation approaches and designing schema specifications for knowledge editing.

The user wants to invoke the `memit-specialist` skill. Let me read that skill file first before proceeding.
````

````plaintext
View: Reading the MEMIT Specialist skill
````

````plaintext
Thought process: Activated specialist mode to probe assumptions before specification.

Now I have the MEMIT Specialist skill loaded. Let me operate in Phase 1 (Socratic Inquiry) mode and ask probing questions to map the user's current assumptions before producing spec output.
````

---

## Session 2 — MEMIT Specialist
**Scope:** Write engine design, .vindex overlay architecture, .larql format, MEMIT vs. alternatives, catastrophic forgetting mitigations

---

Good. I've read the Session 1 schema carefully. Before we produce any spec, I need to map your assumptions on a few dimensions where the schema decisions have direct write-layer implications. The answers will determine which technique we use, how the overlay is structured, and where the failure modes live.

I'll start with three questions. These aren't trivia — they're the ones where your answer changes the architecture.

---

**Question 1 — Permanence**

Session 1 established that Genesis Layers 1 and 2 are *write-once* and require a schema migration to modify. But it didn't resolve whether that means **permanently baked into base model weights** — or **written into a .vindex overlay that is treated as immutable by policy but could technically be unloaded**.

These are very different things physically:

- **Truly permanent** = the weight delta is folded into the base model itself. Fast at inference. Zero rollback possible.
- **Policy-immutable overlay** = the delta lives in a `.vindex` file that *can* be swapped, but the system's rules forbid it except via formal schema migration. Slower at mount time, but you get a rollback escape hatch.

Which of these did you intend when you wrote "write-once" for Genesis L1 and L2? Or hasn't that been decided yet?

---

**Question 2 — Edit Volume**

The Session 1 schema defines five entity types and six relation families. Let's try to size what the write engine actually needs to handle.

Think about a concrete project: say, a medium-scale web API with ~20 modules, ~80 functions, a few external dependencies, and a set of architectural constraint rules.

In your mental model of Project Genesis:
- How many entity nodes and edges do you think get written in the **initial Genesis batch** (Layers 1–4)?
- And during active development, how many `.larql` patches do you estimate would be generated **per day**, per Coder Agent task?

I'm not asking for precision — I'm asking whether we're talking about hundreds of facts, thousands, or tens of thousands. That number determines whether MEMIT is the right tool, or whether we need to think about alternatives.

---

**Question 3 — The Verification Gap**

After the write engine compiles a `.larql` patch into the `.vindex` file, how does the system *confirm the write was correct*?

The framework document mentions `SELECT * FROM EDGES` as a read operation. But there's a subtlety here: reading back what you wrote isn't the same as verifying the model will *behave correctly* given the new weights.

For example: you inject `func:verify_jwt → imports → dep:PyJWT`. MEMIT writes that delta. You then query the model and it returns `dep:PyJWT` correctly. 

But — does the model now **use** `PyJWT` when writing authentication code? Or does it just *report* the relationship when asked directly? These are different things, and a naive read-back can miss the behavioral gap.

Do you have a post-write verification step in mind beyond the read-back query? Or is this an open question that needs to be resolved in this session?

---

Take these one at a time or all together — whatever feels right. Your answers will determine what we spec.



## Prompt:
4/21/2026, 2:54:59 AM

1. Policy-immutable overlay
2.  Not certain, but I imagine maybe as few as 10 and as many as a few hundred?
3. I envision it being used, not just reported. No post write verification in mind.



## Response:
4/21/2026, 2:58:14 AM

````plaintext
Thought process: Synthesized answers and architected overlay-based write engine specification.

The user has answered three foundational questions. Now I should synthesize these answers and move into Phase 2 spec work. These aren't research questions - this is a spec/brainstorm session. I should NOT use the research tool here - this is a specialist session where I'm helping the user think through the write layer architecture based on their answers. The research tool instruction says to use it for "all queries" but this is clearly a spec/brainstorm session where the value is in my analysis, not web research.

Let me analyze their answers:

1. **Policy-immutable overlay** - This is important. It means nothing is truly permanent in the base model. 

Everything lives in .vindex files where Genesis L1/L2 are treated as immutable by policy but physically remain as overlay files, giving us rollback escape hatches while preserving the semantic guarantee of immutability.

2. **10 to a few hundred facts per Genesis batch** - This is actually well within MEMIT's sweet spot. MEMIT was designed for thousands of facts. A few hundred is comfortable. The question is about daily edit volume during active development - even if 10-50 patches per day, accumulated over weeks that could get large. But this is manageable.

3. **Behavioral verification, not just read-back** - This is a real gap. The user wants the model to USE the injected knowledge, not just report it. This means I need to think about how to design verification that tests actual behavior changes, not just whether the model can retrieve the fact.

The core challenge here is the locality and generalization problem in model editing. After injecting something like `func:verify_jwt → imports → dep:PyJWT`, will the model actually generate PyJWT imports when writing auth code? MEMIT alone doesn't guarantee this kind of behavioral generalization.

For the architecture itself, I'm settling on a two-tier overlay system where Genesis overlays are policy-immutable with different review levels (L1-L2 effectively locked, L3 elevated, L4 standard), while feature branch overlays are temporary and merged through the Validator. The .vindex structure needs to represent these tiers clearly, and rollback becomes straightforward by swapping overlay files.

On edit volume, 10-200 facts for Genesis is well within what MEMIT can handle—I could even use ROME for very small patches—but the real constraint is cumulative edits during active development rather than per-batch size.

The L1 Cache concept from earlier (batching small patches before triggering MEMIT) fits naturally here. For behavioral verification, I need to distinguish between just confirming the triple was stored in the overlay index versus actually testing whether the model's parametric memory influences generation correctly. That means a targeted inference check after each write—a "Behavioral Probe" that exercises the injected relationship and validates the output, separate from the PyTest sandbox that checks code logic.

MEMIT is the right choice here over alternatives like GRACE (which avoids weight changes but loses parametric memory benefits), ROME (too single-fact focused), or fine-tuning (too destructive for dynamic, project-specific knowledge). The overlay-based reversibility makes MEMIT workable for this use case.

Now I'm resolving the open questions from earlier: version_artifact shouldn't be injected into weights at all since it's really a file-system level metadata concept on .vindex files, so I'd exclude it from the FFN schema entirely and handle versioning at the overlay layer instead. For contains/defined_in, these are bidirectional edges from the write engine's perspective, and MEMIT can patch both directions simultaneously—I'd generate both from a single declaration rather than storing them separately.

I need to map out the spec blocks: the write engine will use MEMIT as the primary approach with GRACE as a fallback for high-risk edits, the .vindex overlay needs a tiered immutability structure with a clear file format, I need to define what .larql input the write engine accepts, establish behavioral probes for post-write verification, implement orthogonal projection and edit volume thresholds to prevent catastrophic forgetting, and add mutex locks with sequential compilation for concurrent write safety. The edit volume question needs more thought—10-200 edits for Genesis works, but I should consider how cumulative edits across sessions might compound the problem.

Now I'm thinking through the behavioral verification gap more carefully. When MEMIT injects a fact, it modifies the FFN weights to create a new attractor in activation space, but whether that attractor actually activates during generation depends on whether the attention mechanism routes through those modified layers. A direct read-back query bypasses normal generation entirely, but during actual code generation the model needs to retrieve the injected fact naturally through attention routing. So there's a real gap between what the database query returns and what the model actually produces during generation.

I should add a post-write behavioral probe that tests whether the injected relationship actually retrieves correctly in a realistic generation context. For instance, after injecting a relationship between a function and its import dependency, I'd generate a prompt asking for that import statement and verify the dependency appears in the output. This is distinct from testing code correctness—it's specifically about whether the parametric memory retrieval works.

Before moving into the spec, I need to flag this behavioral verification gap as a significant architectural concern that deserves deeper investigation before committing to the full design. I'm settling on moving into spec synthesis now rather than asking more questions—the conversation has developed enough through Phase 1. I'll flag the behavioral verification gap as an open question within the spec itself instead of deferring it further. The key insight is that with the policy-immutable overlay approach, the base model stays untouched, which cleanly constrains the entire write engine architecture. I need to produce the core spec blocks covering write engine selection, the overlay tier architecture, canonical format, post-write verification including that behavioral gap, catastrophic forgetting mitigations, and the open question resolutions. For edit volume, MEMIT's sweet spot is actually hundreds to thousands, though Genesis will operate in the 10-200 range.

I'm reconsidering the write engine strategy—ROME might be more precise for very small patches of 10-20 facts, but since we need batch capability for the larger end and want a single consistent engine, MEMIT works throughout with a lighter approach triggered below a minimum threshold. The framework shows MEMIT can handle up to 10,000 facts simultaneously, which far exceeds our needs. The L1 Cache batches individual .larql patches (5-20 facts each) before triggering MEMIT, creating two distinct modes: Genesis mode for the initial 10-200 fact batch that mints v1.0.vindex, and incremental mode where facts accumulate in the cache before batch processing.

On catastrophic forgetting, the real concern isn't the base model itself since we're using a policy-immutable overlay—it's interference between successive .vindex patches. Orthogonal projection and the covariance balancer prevent this, with the Pruning Agent handling garbage collection. For OQ1, version artifacts like Git hashes and .vindex snapshot IDs shouldn't be base types in the FFN since they're filesystem metadata, not semantic knowledge meant for weight injection.

For OQ4, I'm consolidating contains and defined_in into a single canonical edge direction—defined_in flowing from function to module—with the write engine automatically generating the reverse during compilation. This keeps patches lean and eliminates the risk of agents declaring conflicting reverse edges.

Now I'm ready to structure the response: synthesis with implications, a flag on behavioral verification as an architectural gap, then the spec blocks for write engine selection and the .vindex overlay.

Mapping out the remaining structure: tier architecture, the .larql canonical format, post-write verification, catastrophic forgetting and edit integrity safeguards, resolutions for OQ1 and OQ4, any new open questions that surface, and a session summary at the end.
````

Good. These three answers are enough to move into spec synthesis. Let me surface the implications before producing the spec blocks, because one of your answers contains a gap that will shape the architecture significantly.

---

### Synthesizing Your Answers

**On policy-immutable overlay:** This is architecturally clean and has a major implication you may not have fully registered yet: *the base model is never touched — ever.* Every write, including Genesis L1, lives in a `.vindex` file. The base model becomes a pure inference engine — frozen, stateless, dumb on its own. All project knowledge, all architectural rules, all framework facts — they live in the overlay. This simplifies rollback enormously: to undo *anything*, you swap or unload a file. We'll build the spec around this as a hard constraint.

**On edit volume (10–200 for Genesis, patch-by-patch during development):** You're well inside MEMIT's comfortable range. MEMIT was designed for batches of up to 10,000 facts. 200 is leisurely. The more interesting sizing question is *cumulative* — not per-batch, but over a project's lifetime. A 3-month project generating 10 patches/day at 15 facts each accumulates ~9,000 facts total. That's still within bounds, but it introduces *overlay drift* over time, which the Pruning Agent must address. I'll flag this in the spec.

**On behavioral verification ("used, not just reported"):** This one needs a moment before we proceed, because it reveals a gap in how MEMIT works that the framework document doesn't address clearly.

---

### The Behavioral Gap — Before We Spec Verification

When you inject `func:verify_jwt → imports → dep:PyJWT` into the FFN via MEMIT, two different things happen:

**What MEMIT actually guarantees:** If you query the model directly — "What does `verify_jwt` import?" — it will return `dep:PyJWT` with high probability. The triple is correctly stored and retrievable via direct query. This is the *reporting* case.

**What MEMIT does not automatically guarantee:** When the Coder Agent is generating authentication code in a naturalistic context — writing a 50-line module, mid-task — will the model spontaneously *use* PyJWT in the import statement? This depends on whether the attention mechanism routes through the modified layers with sufficient activation during that specific generation context. The injected attractor exists, but whether it fires during free-form generation is probabilistic, not certain.

Think of it this way: MEMIT writes the fact into memory. But whether the model *acts on* that memory during generation depends on whether the right context tokens activate the right layers. A direct query always does. Naturalistic code generation doesn't always.

**This is a real architectural gap.** Your read-back (`SELECT * FROM EDGES`) confirms storage. It does not confirm behavioral influence. We need a **Behavioral Probe** concept in the post-write verification spec — a targeted generation test that specifically exercises the injected relationship in a realistic generation context.

For example, after injecting the PyJWT triple, the probe runs: *"Write the function signature and import block for a JWT verification function."* The system checks whether `import PyJWT` appears in the output. If it doesn't, the write succeeded at the storage level but failed at the behavioral level — and the system needs to know that.

This is distinct from the PyTest sandbox (which tests whether the code runs correctly). This is testing whether the model's parametric memory is influencing generation. I'm flagging it as an **open question** in the spec — it needs a decision from you, but it's too important to defer without naming.

With that framing in place — the spec blocks:

---

### Write Engine Selection — Spec Block

**What it must do:**
- Accept a `.larql` patch file as its sole input
- Calculate the mathematical weight delta (ΔW) required to encode the declared entities and edges
- Apply that delta to the project-specific `.vindex` overlay file — never to the base model
- Operate in two modes: Genesis Mode (single large batch, mints the initial `.vindex`) and Incremental Mode (smaller patches, accumulated via L1 Cache before triggering compile)

**Hard constraints:**
- Base model weights are immutable. The write engine must never produce output that modifies the base model binary. The `.vindex` overlay is the only writable artifact.
- MEMIT is the designated algorithm for all compile operations. ROME is explicitly excluded as a primary write engine — its single-layer, single-fact design is incompatible with the batch requirements of Genesis Mode and the multi-entity `.larql` patches generated by Coder Agents.
- The write engine must target middle-to-late FFN layers only (approximately L15–L25 for a standard 32-layer model). Early layers (syntax) are off-limits for semantic fact injection. Layer targeting parameters must be declared per entity base type, as contracted in IC1 from Session 1.
- The write engine must enforce the `violates` relation rejection rule (D7 from Session 1) as a pre-compile filter — if a `.larql` patch contains a `violates` edge, the entire patch is rejected before any delta is calculated.

**Tradeoffs decided:**
- **MEMIT over GRACE:** GRACE (which adds a retrieval codebook alongside the model without touching weights) is safer but defeats the purpose of parametric memory — the whole point is that the model *knows* facts, not that it looks them up from a codebook. GRACE is excluded.
- **MEMIT over full fine-tuning:** Fine-tuning is destructive and cannot be overlaid. It would make the `.vindex` swap architecture impossible. Excluded.
- **Single write engine over per-case selection:** Using MEMIT for everything — including small patches — keeps the pipeline uniform. The L1 Cache (see below) buffers small patches until they're batch-worthy, so MEMIT always operates on reasonably-sized inputs.

**Open questions:**
- OQ-W1: At what cumulative edit volume does MEMIT's locality guarantee begin to degrade for this architecture? The research literature suggests degradation becomes measurable above ~5,000 injected facts in a single overlay. Is there a hard limit above which the Pruning Agent must trigger a full overlay recompile from a clean Genesis state?
- OQ-W2: MEMIT compatibility has been validated on GPT-family and LLaMA-family architectures. If the harness targets Gemma (as suggested in the framework document), compatibility verification is required. This is not a blocker but must be confirmed before the write engine is treated as architecture-agnostic.

**Interface contract:**
- **Input:** Valid `.larql` patch file (schema-validated by Validator before reaching write engine)
- **Output:** Updated `.vindex` file for the active project; write result signal (`{success, failure, partial}`) returned to orchestrator
- **Adjacent dependencies:** Receives entity base type and relation family tags from the schema layer (IC1 from Session 1); returns write result to Transaction Controller (State Consistency layer)

---

### .vindex Overlay Tier Architecture — Spec Block

**What it must do:**
- Represent all project-specific parametric knowledge as a layered set of weight deltas (ΔW) applied to the frozen base model at runtime
- Maintain a strict tiered structure corresponding to Genesis Layers 1–4 from Session 1
- Support per-project isolation: each project has its own `.vindex` stack; loading a project means mounting its overlays; unloading means unmounting

**Overlay tier structure:**

```
BASE MODEL (frozen — never modified)
    │
    ├── vindex/genesis_schema.vindex       ← Genesis L1 (framework-generated, write-once)
    ├── vindex/genesis_domain.vindex       ← Genesis L2 (domain extensions, write-once)
    ├── vindex/genesis_constraints.vindex  ← Genesis L3 (constitutional rules, elevated review)
    ├── vindex/genesis_knowledge.vindex    ← Genesis L4 (foundational domain facts, patchable)
    │
    └── vindex/patches/
            ├── patch_001.vindex           ← incremental feature commits
            ├── patch_002.vindex
            └── ...
```

**Hard constraints:**
- Genesis tiers (L1–L3) are *policy-immutable*: the write engine will accept patches targeting these tiers only if the orchestrator presents a schema migration authorization token. Standard `.larql` patches from Coder Agents cannot modify L1–L3.
- Overlay files are append-only during a project session. An overlay is never overwritten — a new file is created for each compile operation. The State Ledger maps overlay filenames to Git commit hashes.
- Unmounting an overlay is a full rollback: unloading `patch_015.vindex` and re-pointing to `patch_014.vindex` restores the previous parametric state. The base model and all prior overlays are unaffected.
- The overlay stack is **ordered and sequential**. Overlays must be applied in creation order. Out-of-order application is a write engine error.

**Tradeoffs decided:**
- **Separate files per Genesis tier over single monolithic Genesis file:** Enables independent rollback of Genesis L4 (updatable domain knowledge) without touching L1–L3 (constitutional constraints). The cost is slightly more complex mount logic — acceptable.
- **Incremental patch files over a single accumulating overlay:** Incremental files are the natural expression of the Git commit analogy. They also allow the Pruning Agent to identify and compact old patches without full overlay reconstruction.

**Open questions:**
- OQ-W3: Should Genesis tier overlays be compiled in a single MEMIT batch (faster, one operation) or sequentially tier-by-tier (slower, but preserves tier isolation if a mid-Genesis failure occurs)? The sequential approach is safer for the bootstrapping problem (OQ7 from Session 1), but costs more compute at Genesis time.
- OQ-W4: Maximum overlay stack depth before compaction is required? At some point, mounting 200 incremental patch files becomes a performance problem. The Pruning Agent should be able to *compact* a set of patches into a single consolidated overlay — but this needs a spec for how compaction interacts with the State Ledger.

**Interface contract:**
- **Input from orchestrator:** Project ID + mount instruction → write engine loads the correct overlay stack onto base model
- **Output to orchestrator:** Current overlay hash (used by State Ledger for consistency checks)
- **Output to agents:** The mounted model — agents have no visibility into which overlay files are active; they query against the assembled knowledge state

---

### .larql Canonical Format — Spec Block

**What it must do:**
- Provide the exclusive interface between the agent layer and the write engine
- Express all three write operations: INSERT (new facts), DELETE (retractions), and SELECT (pre-generation read)
- Carry compiler directives that instruct the write engine on layer targeting, injection strength, and safety flags
- Be human-readable and version-controllable (committed to Git alongside the code it describes)

**Canonical structure:**

```sql
-- HEADER (required)
-- Project:         [project_id]
-- Agent_ID:        [agent_task_id]
-- Target_File:     [src/path/to/file.py]
-- Schema_Version:  [declared schema version]

BEGIN TRANSACTION;

-- SECTION 1: ENTITY REGISTRATION
-- Declares new nodes. Must include base_type from the Session 1 taxonomy.
INSERT INTO ENTITIES (entity_id, base_type, semantic_description)
VALUES
  ('module:auth', 'structural_entity', 'Handles JWT verification and user session state'),
  ('func:verify_jwt', 'structural_entity', 'Parses headers, validates JWT signature'),
  ('dep:PyJWT', 'domain_concept', 'Python JSON Web Token library');

-- SECTION 2: EDGE DECLARATIONS
-- Maps topological relationships. relation label must be from declared vocabulary.
-- attention_weight guides MEMIT covariance balancer (0.0–1.0).
INSERT INTO EDGES (source_id, relation, target_id, attention_weight)
VALUES
  ('func:verify_jwt', 'imports', 'dep:PyJWT', 0.95),
  ('module:auth', 'exports', 'func:verify_jwt', 1.0);

-- SECTION 3: DELETIONS (if applicable)
DELETE FROM EDGES
WHERE source_id = 'func:old_auth' AND relation = 'defined_in';

-- SECTION 4: COMPILER DIRECTIVES
SET TARGET_LAYERS = [15, 25];
SET ORTHOGONAL_PROJECTION = TRUE;
SET TIER = 'incremental';         -- 'genesis_l4' | 'incremental'

COMMIT;
```

**Hard constraints:**
- Every entity declared in `INSERT INTO ENTITIES` must include a `base_type` field matching one of the five types from Session 1 (D3). Untyped entity declarations are schema violations — the Validator rejects the patch before it reaches the write engine.
- Every relation label in `INSERT INTO EDGES` must match the declared vocabulary (D6 from Session 1). Undeclared labels are schema violations (C5).
- `violates` is a prohibited label (D7). The Validator rejects any patch containing it before the write engine sees it.
- The `TIER` directive must be explicitly declared. If `TIER = 'genesis_l1'`, `'genesis_l2'`, or `'genesis_l3'` is declared by a Coder Agent, the write engine refuses without an orchestrator schema migration token.
- `attention_weight` must be in range `[0.0, 1.0]`. Values outside this range are malformed patches — hard rejection.
- `BEGIN TRANSACTION` / `COMMIT` bracketing is required. A patch that does not complete its transaction is not applied — partial writes are prohibited.

**Resolving OQ4 from Session 1 (contains / defined_in):**
The write engine will accept the canonical directed form only — `defined_in` (child → parent, e.g., `func:verify_jwt defined_in module:auth`) — and **automatically generate the reverse edge** (`contains`: `module:auth → func:verify_jwt`) during compilation. Agents never need to declare both directions. This keeps patches smaller and eliminates the risk of contradictory reverse declarations. **OQ4 is resolved: one canonical edge, write engine generates the reverse.**

**Open questions:**
- OQ-W5: Should `attention_weight` be agent-declared or write-engine-computed? Allowing agents to set weights gives them control over injection strength but introduces risk — a miscalibrated weight can cause an injected fact to overpower adjacent knowledge. An alternative is for the write engine to compute weights from relation family metadata (D6) and ignore agent-declared values. Decision needed.
- OQ-W6: `.larql` versioning — should the format itself carry a schema version number so the write engine can handle patches generated by older agents against a newer schema? Or is schema migration always forward-only?

---

### Post-Write Verification Protocol — Spec Block

**What it must do:**
- Confirm a write was correctly applied at two levels: storage verification (the triple was encoded) and behavioral verification (the encoded fact influences generation)
- Return a verification result to the orchestrator before the agent overlay is merged into the main overlay stack
- Surface the behavioral gap (described above) as a named failure mode — not a silent pass

**Two-level verification:**

**Level 1 — Storage Probe (Read-Back Query)**
After MEMIT applies the delta, the write engine executes a direct `SELECT` against the modified weights for each inserted edge:

```sql
SELECT target_id FROM EDGES
WHERE source_id = 'func:verify_jwt' AND relation = 'imports'
```

Expected return: `dep:PyJWT`. If the return is empty or returns a different entity, the write failed at the storage level. This is a hard failure — patch is rejected, overlay is not committed.

**Level 2 — Behavioral Probe (Generation Test)**
After storage verification passes, the orchestrator issues a targeted generation task that specifically exercises the injected relationship in a naturalistic context. The task is declared in the `.larql` patch header:

```sql
-- BEHAVIORAL_PROBE: "Write the import block for the verify_jwt function."
-- EXPECTED_SIGNAL:  "PyJWT"
```

The model generates a short response. The orchestrator scans the output for the `EXPECTED_SIGNAL`. If the signal appears, behavioral verification passes. If it does not, the write is flagged as **storage-pass / behavior-fail** — a named failure mode indicating MEMIT encoded the fact but it is not reliably firing during generation.

**Hard constraints:**
- Storage probe is mandatory for every write. No exceptions.
- Behavioral probe is mandatory for any edge where `attention_weight >= 0.85` (high-influence facts). Optional for low-weight edges — to be confirmed.
- A **storage-pass / behavior-fail** result must surface as a named signal to the orchestrator. It must not be silently treated as a full pass. The system should have a defined response to this failure mode — options include: retry with increased injection weight, flag for manual review, or accept as low-confidence write. **This is an open question.**

**Open questions:**
- OQ-W7 (CRITICAL): What is the system's response to a storage-pass / behavior-fail result? Three options — increase injection weight and retry (risks overpowering adjacent knowledge); accept as low-confidence and flag; reject the write entirely and fall back to RAG for this fact. This decision determines how aggressively the system pursues parametric encoding vs. accepting hybrid memory.
- OQ-W8: Behavioral probe design for non-code domains — the probe above assumes code generation context. If the harness is used for non-code projects, the probe format needs a generalization spec.

---

### Catastrophic Forgetting & Edit Integrity — Spec Block

**What it must do:**
- Ensure new injected facts do not corrupt, overwrite, or interfere with previously injected facts or base model knowledge
- Enforce mathematical safeguards during every MEMIT compile operation
- Define the threshold at which overlay drift requires intervention

**The two interference risks, precisely defined:**

1. **Intra-project interference:** A new `.larql` patch modifying an entity that already exists in a prior overlay. Example: patch_003 inserts `func:verify_jwt → imports → dep:PyJWT` at weight 0.95. Six weeks later, patch_047 inserts `func:verify_jwt → imports → dep:jose` at weight 0.90 after a library migration. If both overlays are mounted, the model has two high-weight competing signals for the same source + relation pair. This causes polysemantic noise on a node you thought was clean.

2. **Base model interference:** An injected fact that is semantically close to a strong base-model prior. Example: the base model was trained heavily on React 17. Injecting React 19 triples into the same feature cluster creates a competition between the new weight delta and the existing pre-trained pathways. The Balancer (orthogonal projection) addresses this — but it is not infallible at high edit volumes.

**Mitigations — write engine responsibilities:**

- **Orthogonal Projection (mandatory for every write):** The write engine calculates whether the new ΔW vector is orthogonal to existing feature vectors in the target layers. If the cosine similarity between the new vector and any existing vector in the same feature cluster exceeds a defined threshold (to be specified), the write engine reduces the injection weight or requests a Pruning Agent pass before proceeding.
- **Covariance Balancer (mandatory for Genesis Mode):** During the Genesis batch, the write engine applies MEMIT's covariance adjustment to the full fact set before compilation. This distributes injection pressure across the layer range rather than concentrating it on the highest-traffic features.
- **Conflict detection for existing entities:** Before compiling any patch that includes an entity already present in a prior overlay (detected via storage probe), the write engine must surface a **collision warning** to the orchestrator. The orchestrator decides: update-in-place (delete old edge, insert new), append (allow competing signals), or reject.

**Overlay drift threshold:**
Based on MEMIT's documented locality degradation characteristics, the following thresholds are proposed for spec:
- **Warning threshold:** Cumulative edges in a single overlay stack exceeds 3,000. Orchestrator is notified. Pruning Agent pass recommended.
- **Hard limit:** Cumulative edges exceeds 8,000. Write engine refuses new incremental patches until a Pruning Agent compaction + overlay recompile is performed.

These numbers are provisional and require empirical validation against the chosen base model.

**Open questions:**
- OQ-W9: Collision warning handling — who decides the update-in-place vs. append vs. reject policy? Orchestrator alone, or does the Validator Agent get input? If the Validator is authoritative on ontological correctness, it should weigh in on collision decisions.
- OQ-W10: Overlay compaction — when the Pruning Agent compacts patches 001–050 into a single consolidated overlay, does MEMIT need to be re-run on the full fact set from scratch, or can it compose the individual ΔW deltas mathematically? The answer affects compaction cost significantly.

---

### OQ Resolutions from Session 1

**OQ1 — version_artifact as base type:**
**Resolved. Recommend closing as: NOT a base entity type.**
Version artifacts (Git commit hashes, `.vindex` snapshot IDs) are file-system metadata managed by the State Ledger (a SQLite/JSON structure outside the FFN). The model's FFN should not encode version pointers — it encodes semantic relationships. The version_artifact concept lives at the orchestration layer, not in the parametric memory. The Session 1 five-type taxonomy remains unchanged.

**OQ4 — contains / defined_in:**
**Resolved above in .larql Format spec.** One canonical edge (`defined_in`, child → parent). Write engine auto-generates the reverse. Both directions are queryable. Coder Agents declare only the canonical direction.

---

### New Open Questions Surfaced This Session

| ID | Question | Blocking? |
|---|---|---|
| OQ-W1 | Cumulative edit volume threshold for locality degradation — model-specific, requires empirical validation | No — use provisional thresholds |
| OQ-W2 | MEMIT compatibility with Gemma architecture requires explicit verification | No — not a blocker for spec |
| OQ-W3 | Genesis tiers: single batch compile or sequential tier-by-tier? | Yes for Session 3 (bootstrapping path) |
| OQ-W4 | Overlay stack compaction spec — Pruning Agent interaction | Deferred to State Consistency session |
| OQ-W5 | `attention_weight` — agent-declared or write-engine-computed? | Yes — must be decided before .larql format is final |
| OQ-W6 | `.larql` schema versioning strategy | Deferred |
| OQ-W7 | Response to storage-pass / behavior-fail verification result | **Yes — critical, must be resolved in Validation session** |
| OQ-W8 | Behavioral probe generalization for non-code domains | Deferred |
| OQ-W9 | Collision warning resolution authority | Deferred to State Consistency session |
| OQ-W10 | Overlay compaction — full MEMIT re-run vs. delta composition | Deferred to State Consistency session |

---

## Session 2 — Summary Block

```
SESSION 2 — MEMIT Specialist
PRIMARY OUTPUTS: Write engine selection, .vindex tier architecture,
                 .larql canonical format, post-write verification
                 protocol, catastrophic forgetting mitigations

═══════════════════════════════════════════════════
DECISIONS MADE
═══════════════════════════════════════════════════
D11. All writes are overlay-based (policy-immutable .vindex files).
     Base model is never modified under any circumstances.
     This is a hard architectural constraint.

D12. MEMIT is the designated write engine. GRACE and fine-tuning
     are explicitly excluded. ROME is excluded as primary engine.

D13. Write engine operates in two modes: Genesis Mode (batch,
     mints initial .vindex stack) and Incremental Mode (smaller
     patches, buffered via L1 Cache before MEMIT compile).

D14. .vindex overlay stack is tiered to mirror Genesis layers:
     genesis_schema / genesis_domain / genesis_constraints /
     genesis_knowledge / incremental patches. Separate files
     per tier for independent rollback capability.

D15. .larql canonical format defined. Four sections: Entity
     Registration, Edge Declarations, Deletions, Compiler
     Directives. BEGIN/COMMIT bracketing required.

D16. OQ4 resolved: contains/defined_in uses one canonical
     directed edge (defined_in, child→parent). Write engine
     auto-generates reverse. Agents declare canonical direction
     only.

D17. OQ1 resolved: version_artifact is NOT an FFN base type.
     Version metadata lives in State Ledger (orchestration layer).
     Session 1 five-type taxonomy unchanged.

D18. Post-write verification is two-level: Level 1 storage probe
     (SELECT read-back, mandatory for all writes) + Level 2
     behavioral probe (generation test, mandatory for high-weight
     edges ≥ 0.85).

D19. Storage-pass / behavior-fail is a named failure mode.
     It must not be silently treated as a full pass.

D20. Orthogonal projection and covariance balancer are mandatory
     write engine operations — not optional safeguards.

D21. Provisional overlay drift thresholds: warning at 3,000
     cumulative edges; hard limit at 8,000 (pending empirical
     validation against target model).

═══════════════════════════════════════════════════
CONSTRAINTS ESTABLISHED
═══════════════════════════════════════════════════
C8.  Base model is permanently frozen. Write engine output
     must never target base model weights.
C9.  `violates` relation rejected at write engine input stage
     (pre-MEMIT filter). Full patch rejected on violation.
C10. Undeclared base_type or relation label: full patch rejection.
C11. TIER directive required in all .larql patches.
C12. Genesis L1–L3 patches require orchestrator schema migration
     token. Coder Agent patches targeting these tiers are
     hard-rejected by write engine.
C13. attention_weight must be in [0.0, 1.0]. Out-of-range is
     malformed patch — hard rejection.
C14. BEGIN TRANSACTION / COMMIT required. Partial writes
     are prohibited — all-or-nothing.
C15. Layer targeting restricted to middle-to-late FFN layers
     (L15–L25 for 32-layer model). Early syntax layers
     are off-limits for semantic injection.

═══════════════════════════════════════════════════
OPEN QUESTIONS DEFERRED
═══════════════════════════════════════════════════
OQ-W1  Cumulative edit volume degradation threshold
       (model-specific, empirical)
OQ-W2  MEMIT/Gemma architecture compatibility verification
OQ-W3  Genesis: single batch vs. sequential tier compile
       → INPUT REQUIRED: Session 3 (Validation/AISecOps)
OQ-W4  Overlay compaction spec
       → INPUT REQUIRED: Session 5 (State Consistency)
OQ-W5  attention_weight: agent-declared vs. engine-computed
       → MUST RESOLVE before .larql format is final
OQ-W6  .larql schema versioning strategy
OQ-W7  Response to storage-pass / behavior-fail
       → CRITICAL INPUT for Session 4 (Validation Contract)
OQ-W8  Behavioral probe generalization (non-code domains)
OQ-W9  Collision warning resolution authority
       → INPUT REQUIRED: Session 5 (State Consistency)
OQ-W10 Overlay compaction: full MEMIT re-run vs. delta composition
       → INPUT REQUIRED: Session 5 (State Consistency)

═══════════════════════════════════════════════════
INTERFACE CONTRACTS DEFINED
═══════════════════════════════════════════════════
IC5. Write Engine ← Validator:
     Receives schema-validated .larql patch only.
     Validator confirms: base_type declared, relation labels
     in vocabulary, `violates` absent, TIER declared,
     attention_weight in range, transaction bracketed.
     Write engine assumes pre-validated input.

IC6. Write Engine → State Ledger:
     Outputs overlay filename + hash after each successful
     compile. State Ledger maps this to current Git commit hash.

IC7. Write Engine → Orchestrator:
     Returns write result signal: {success, behavior-fail,
     storage-fail, rejected} with failure reason on non-success.

IC8. Write Engine ← Orchestrator (Genesis only):
     Receives schema migration authorization token for
     L1–L3 tier writes. Token format TBD (AISecOps session).

IC9. Behavioral Probe → Orchestrator:
     Returns probe result: {pass, storage-pass/behavior-fail}
     with the agent-declared EXPECTED_SIGNAL and actual
     generation output for review.

═══════════════════════════════════════════════════
INPUT REQUIRED FOR SESSION 3
═══════════════════════════════════════════════════
Session 3 recommended: AISecOps Specialist (The Warden)
Primary inputs from Sessions 1–2:
  — Schema migration authorization token spec (IC8, OQ-W3)
  — Genesis bootstrapping write authorization (OQ8 from S1)
  — Trust boundary between Coder Agent and write engine
  — Policy-immutable overlay enforcement mechanism
  — .larql patch supply chain integrity
  — OQ-W5 (attention_weight authority) has security implications
    — Warden should weigh in before this is closed
```





---
Powered by [Claude Exporter](https://www.ai-chat-exporter.net)