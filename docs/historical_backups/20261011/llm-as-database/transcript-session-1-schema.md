# Ontological schema for LLM database agent framework

**Created:** 4/21/2026 2:08:21  
**Updated:** 4/21/2026 2:45:30  
**Exported:** 4/21/2026 8:55:36  
**Link:** [https://claude.ai/chat/5fa15efd-cc45-480e-a8ed-0b70636726b7](https://claude.ai/chat/5fa15efd-cc45-480e-a8ed-0b70636726b7)  

## Prompt:
4/21/2026, 2:08:22 AM

/graph-data-architect 

I am building a specification for the LLM as Database agent harness framework.
Invoke the graph-data-architect skill. I want to start from the very beginning:
help me understand and begin speccing the ontological schema for this system —
the entity types, relation vocabulary, triple model, and Project Genesis scope.
Ask me the questions I need to answer before we can define any of this.



## Response:
4/21/2026, 2:09:05 AM

````plaintext
Thought process: Activating graph-data-architect expertise for ontological schema specification.

The user wants me to invoke the graph-data-architect skill. Let me first read the skill file, then engage with the user's request. This is a brainstorm/specification session, not a research task per se - the user wants me to act as the Graph Data Architect specialist and ask them clarifying questions to begin speccing the ontological schema. I should NOT use the launch_extended_search_task for this - this is a structured conversation/specification session, not a web research task.

Let me read the skill file first, then respond appropriately.
````

````plaintext
View: Reading the graph-data-architect skill
````

````plaintext
Thought process: Activated architect role to probe foundational ontology requirements.

Good. Now I have the skill loaded. Let me engage as the Graph Data Architect in Phase 1: Socratic Inquiry mode. I should ask probing questions to map the user's knowledge domain and representation needs before producing spec output. The skill says to surface gaps as they appear and not front-load all questions.

Let me craft a good opening as the Graph Data Architect, explain the key concepts clearly since the user is learning, and then ask the most important foundational questions.
````

# Graph Data Architect — Session 1
### Ontological Schema: First Principles

---

Welcome. Before we write a single triple, I need to understand what this graph must *express* — because the schema you define here becomes the contract that every other component in this harness must honor. The write engine (MEMIT), the Validator, the Pruning Agent — they all operate on top of whatever we decide in this room. Getting it wrong at this stage is the most expensive mistake the system can make.

Let me orient you first, then ask you the questions that actually matter.

---

## What We're Actually Designing

A traditional database has a schema: tables, columns, types, constraints. The LLM-as-database has the same thing — it's just expressed differently.

Every fact in this system is a **triple**:

```
entity → relation → target
```

Think of it as a directed arrow between two things, labeled with the *kind* of relationship. For example:

```
("AuthService",  "depends_on",  "JWTValidator")
("useActionState", "introduced_in", "React_19")
("module:auth",  "exports",     "func:verify_jwt")
```

The **entity** is the thing we're making a claim about. The **relation** is the type of claim. The **target** is what the claim points to.

Your schema has three jobs:
1. Define what *kinds* of things can be entities (the entity type taxonomy)
2. Define what *kinds* of claims are allowed (the relation vocabulary)
3. Define what *kinds* of things each relation can point to (target type constraints)

This is not a free-form graph. A vague, loosely typed schema is one of the most common ways this system fails — two agents independently write `"uses"`, `"calls"`, `"requires"`, and `"depends_on"` to mean the same thing, and the graph becomes incoherent noise.

---

## The Questions I Need You to Answer

I'm going to ask you these in order of importance. Think of each one as a design decision that closes off certain paths and opens others.

---

**Question 1 — The primary knowledge domain**

The framework document describes a *software development harness* — agents that write code, test it, and patch knowledge about that code into the model. But the framework is described as "general-purpose." So I need to know:

> **What is the primary domain of knowledge this graph needs to represent?**

Is this fundamentally a graph about *code structure* (files, functions, dependencies, APIs)? Or is it a graph about *project architecture* (modules, services, design patterns, constraints)? Or something more abstract — a graph about *the project's rules and decisions*?

These sound similar but they pull the schema in different directions. A code-structure graph is fine-grained and changes constantly. An architecture graph is coarser and changes rarely. A decisions graph is almost append-only.

What does the harness most need to *know* — and what does it most need to *not forget*?

---

**Question 2 — The most important query**

Before we spec a single entity type, I want you to tell me:

> **What is the single most important question an agent will need to ask this graph?**

Try to express it as a `SELECT` statement — even a rough one:

```sql
SELECT ??? FROM EDGES WHERE entity = ??? AND relation = ???
```

This question reveals what the graph must be *organized around*. Everything else is secondary to making that query fast, reliable, and unambiguous.

---

**Question 3 — Polysemantic collision risk**

This is the most underestimated design problem in this entire system, so I want to surface it early.

LLM neurons are **polysemantic** — a single neuron activates for multiple unrelated concepts. When you query the word `"capital"`, you might get back Paris, uppercase letters, investment funds, and the word "CEO" all clustered together.

> **What tokens in your domain are most likely to be ambiguous?**

For a software harness, some classic collision risks are:
- `"module"` — could mean a Python module, a JavaScript module, a project module, a hardware module
- `"type"` — could mean a data type, a TypeScript type, a category label, or the verb "to type"
- `"schema"` — could mean a database schema, a JSON schema, a graph schema, or a conceptual framework
- `"version"` — could mean a software version, a model version, a `.vindex` version, or a schema version

I need to know which of these collision zones exist in *your* specific graph before we name anything.

---

**Question 4 — Fact lifetime**

Not all facts are created equal. Some facts must survive forever. Some should be deleted when a function is renamed. Some should never be written to weights at all.

> **Can you identify at least one fact from each of these four categories for your system?**

| Category | Description | Example from framework doc |
|---|---|---|
| **Foundational** | True from Genesis; never changes | ? |
| **Versioned** | Immutable once written, but replaced by a newer version | ? |
| **Mutable** | Changes when the codebase changes | ? |
| **Ephemeral** | Working hypothesis; must never reach the write engine | ? |

Getting this wrong means the Pruning Agent has nothing to work from, or worse — it deletes things it shouldn't.

---

**Question 5 — Genesis scope**

The framework describes a "Project Genesis" phase — a write-once initialization where foundational knowledge is baked into the model *before any agents start working*.

> **What must be true in the graph from Day One for any agent to function at all?**

This is the hard boundary of Genesis scope. Anything that goes into Genesis is expensive to revise. I want to find the *minimum viable Genesis* — the smallest set of facts without which the entire harness is blind.

---

Take these one at a time or answer them together — either works. The goal is to give me enough signal to produce the first spec blocks: the **Entity Type Taxonomy**, the **Relation Vocabulary**, and the **Project Genesis Scope Definition**.

What do you know, and where are the gaps?



## Prompt:
4/21/2026, 2:23:50 AM

1. The LLM does not memorize how to spell the function; it memorizes what the function does, what it requires, and what other files depend on it. The LLM provides the map; Git provides the territory. Also, I am envisioning the LLM being the knowledge base for framework docs, standards, uses, etc. Also, this framework will be applicable beyond just coding environments but can extend to any domain imaginable where the agent harness and agent work/workflows can be deployed.
2. I believe my answer to #1 answers this? If not, ask clarifying questions to guide me in understanding how to answer more fully.
3. I have not worked through any specific graphs to be able to answer this question.
4. There are no specific facts that have been identified since this is a broad scoped specification to implement across a wide range of domains.
5. Things like programming language, framework documentation. Authoritative guides, books, websites, knowledge. What else do you think?



## Response:
4/21/2026, 2:25:02 AM

````plaintext
Thought process: Synthesized architectural insights and identified gaps requiring deeper specification work.

This is a structured specification session - the user is answering my questions as the Graph Data Architect. This is NOT a web research task. The research instructions say to use launch_extended_search_task for "all queries except for (1) the most basic conversational messages or (2) extremely simple questions." 

But this is a specification/brainstorming session - the user is asking me to act as a specialist and respond to their answers. This is more akin to a structured conversation than a research task. The user hasn't asked me to research anything - they've answered my questions and I need to synthesize those answers and ask follow-up questions or produce spec output.


The research instructions are really for factual lookups and informational queries, not for these kinds of multi-turn specification dialogues where I'm functioning as a domain specialist. The user clearly wants me to engage as the Graph Data Architect and work through this with them, not go off doing web research. I should synthesize what they've told me - that the LLM acts as a map of relationships and dependencies while Git holds the actual code, and the framework itself is domain-agnostic - and probe deeper on whether that really answers their second question.

They haven't done any polysemantic work yet and haven't identified specific facts, so I need to guide them through articulating what exactly they want to query. For Genesis specifically, they're thinking about programming languages, framework documentation, authoritative guides, and domain knowledge. The conceptual answer they gave me is solid - the graph captures relationships, dependencies, semantics, and framework knowledge - but I need to push them to distinguish between "the graph is about relationships" as a general concept versus what specific queries they actually want to run against it. I need to synthesize their answers into a response that exposes the hidden architectural decision in their first answer—the map versus territory distinction—then push them on the second question with a concrete example, walk them through a polysemantic risk scenario in their domain, and propose starting taxonomies for fact lifetimes and a minimum viable Genesis scope for validation.
````

Good. There's a lot of signal in these answers. Let me tell you what I heard, where it takes us, and where I still need you to go deeper.

---

## What Your Answers Revealed

### On Question 1 — You've made a critical architectural decision

Your framing — *"the LLM provides the map; Git provides the territory"* — is not just a metaphor. It's a **schema partition rule**, and it's one of the most important decisions in this entire specification.

It means:

> **The graph stores semantics, not syntax. Relationships, not literals.**

This rules out an entire class of things that should *never* go into the `.vindex`:
- Exact function signatures (Git's job)
- Literal file contents (Git's job)
- Line numbers, variable names, string values (Git's job)

And it confirms what *should* go in:
- `("func:verify_jwt", "requires_parameter", "JWT_Token")`
- `("module:auth", "depends_on", "module:user_db")`
- `("React_19", "deprecates", "React_18_useEffect_pattern")`

You've also added a second knowledge layer I want to name explicitly: **domain knowledge** — framework docs, standards, authoritative references. This is structurally different from project-specific knowledge. A fact like `("useActionState", "introduced_in", "React_19")` comes from the React documentation and is true across all projects. A fact like `("module:auth", "secures", "module:api_router")` is true only for *this* project.

This means your schema needs **two namespaces** operating on the same graph:

| Namespace | Example Triple | Origin | Lifetime |
|---|---|---|---|
| **Domain Knowledge** | `("useActionState", "introduced_in", "React_19")` | Framework docs, standards | Stable; updated when docs change |
| **Project Knowledge** | `("module:auth", "secures", "module:api_router")` | Coder Agent writing code | Mutable; changes as project evolves |

These two namespaces will need different write authorization rules, different pruning behavior, and different Genesis treatment. Hold that — it becomes important later.

Your third point — **domain-agnostic** — is the most architecturally demanding of all. It means the entity type taxonomy cannot be `[file, function, class, library]`. It has to be abstract enough that the same schema works for a legal research harness, a medical knowledge base, a software project, or a supply chain system.

That's a hard constraint I'm going to keep visible throughout this session.

---

### On Question 2 — Your Q1 answer partially answers it, but not operationally

You said "I believe my answer to #1 answers this" — and conceptually, yes. But I need something more specific, and here's why:

**The most important query determines the shape of the graph.** If the primary query is "what does this thing depend on," the graph is organized around dependency chains. If it's "what things know about this concept," it's organized around knowledge clusters. If it's "what rules govern this entity," it's organized around constraint hierarchies. These look different in weight space.

Let me try to answer it for you using your own framing, and you tell me if I'm right:

> **The most important query an agent will run is: "What do I need to know before I act on this thing?"**

In `larql` terms, something like:
```sql
SELECT relation, target FROM EDGES
WHERE entity = "module:auth"
```

This returns everything the graph knows about `module:auth` — what it depends on, what it exports, what it secures, what rules govern it, what standards apply to it. The agent reads this *before* writing any code touching that module.

Is that the primary query? Or is it something else — like "what rules constrain this decision" or "what does the model know about this technology"?

**I need you to pick one concrete scenario** — an agent about to do something — and tell me what question it would ask the graph first. One sentence. Don't worry about SQL syntax.

---

### On Question 3 — Polysemantic risk: let me give you a concrete example

Since you haven't worked through any graphs yet, let me show you the problem with a real example from *your own domain*, and then ask you to react.

Suppose you insert this triple into the graph during Project Genesis:

```sql
INSERT INTO EDGES (entity, relation, target)
VALUES ("Python", "is_a", "language")
```

Now query:
```sql
SELECT * FROM EDGES WHERE target = "language"
```

In a model's weight space, `"language"` is catastrophically polysemantic. You might get back: Python (programming), French (natural language), `language` (the HTML attribute), `language` (linguistics academic field), `language` (as in "body language"). The token `"language"` clusters with all of these simultaneously.

Your query has just returned noise.

Now suppose instead you wrote:
```sql
INSERT INTO EDGES (entity, relation, target)
VALUES ("Python", "is_a", "programming_language")
```

`"programming_language"` is far less polysemantic. The cluster is tighter. The graph walk returns cleaner results.

**The rule this reveals:** Entity and target names in your schema should be **compositionally unambiguous** — preferring `programming_language` over `language`, `codebase_module` over `module`, `api_endpoint` over `endpoint`.

Here are the highest-risk tokens in your domain for me to flag right now:

| Token | Collision Risk |
|---|---|
| `"type"` | Data type / TypeScript type / category / the verb |
| `"model"` | LLM model / data model / ORM model / domain model |
| `"schema"` | DB schema / graph schema / JSON schema / conceptual framework |
| `"version"` | Software version / model version / `.vindex` version / API version |
| `"module"` | Python module / JS module / project module / hardware module |
| `"standard"` | Industry standard / code standard / HTTP standard |
| `"target"` | Triple target / deployment target / business target |
| `"agent"` | AI agent / HTTP user-agent / estate agent |

Note that `"target"` is on this list — which is particularly dangerous because it's a reserved term in the `.larql` triple model *and* a general-purpose word. This is something the schema spec will need to address explicitly.

---

### On Questions 4 & 5 — Let me propose a starting taxonomy for you to react to

Since the scope is broad, I'll populate the fact lifetime categories using the framework's own logic, and you tell me if anything is wrong or missing.

**Proposed Fact Lifetime Taxonomy:**

| Category | Definition for this system | Example |
|---|---|---|
| **Foundational** | Injected at Project Genesis; true for the lifetime of the project; should require a privileged write to change | `("React_19", "latest_stable_version_of", "React")` |
| **Versioned** | Immutable after creation; a newer version *supersedes* it but it is never deleted | `("api_schema_v2", "supersedes", "api_schema_v1")` |
| **Mutable** | Reflects current project state; updated by Coder Agent as work proceeds; subject to Pruning Agent | `("module:auth", "exports", "func:verify_jwt")` |
| **Ephemeral** | Agent working hypothesis during a task; must never reach the write engine | "I think this function might need a cache layer" |

**On Question 5 — Proposed Minimum Viable Genesis:**

You named: programming language, framework docs, authoritative guides, books, websites, knowledge.

Let me translate those into graph terms and add what I think is missing:

```
Genesis Layer 1 — The Entity Taxonomy itself
  ("file", "is_entity_type", "structural_entity")
  ("function", "is_entity_type", "structural_entity")
  ("concept", "is_entity_type", "domain_entity")
  ...

Genesis Layer 2 — The Relation Vocabulary itself
  ("depends_on", "is_relation_type", "dependency_relation")
  ("introduced_in", "is_relation_type", "versioning_relation")
  ...

Genesis Layer 3 — Domain Knowledge (your Q5 answer)
  ("useActionState", "introduced_in", "React_19")
  ("React_19", "requires_node_version", "Node_18+")
  ...

Genesis Layer 4 — Project Constraints (what you haven't named yet)
  ("this_project", "uses_language", "Python")
  ("this_project", "follows_standard", "Clean_Architecture")
  ("this_project", "targets_environment", "Docker_Linux")
```

**What I think you're missing from Genesis:**

1. **The schema's own structure** — the entity taxonomy and relation vocabulary should themselves be encoded as triples. The graph must know what kinds of things are allowed to exist in it, or the Validator Agent has no schema to validate against.

2. **Project-level constraints** — architectural decisions that govern everything else (language choice, deployment environment, design patterns). These are the "constitutional layer" of the project graph. Every other fact is subordinate to them.

3. **The namespace boundary** — the graph must encode which facts are domain knowledge (portable across projects) and which are project knowledge (specific to this instance). Without this, the Pruning Agent cannot know which stale facts to delete.

---

## Before We Write Any Spec Blocks

I have two targeted follow-up questions based on everything above:

**Follow-up A:** What is the one concrete scenario — pick any domain — where an agent asks the graph a question before acting? Describe the agent's situation in plain language. I'll translate it into a `SELECT` statement and we'll use that to anchor the entity taxonomy.

**Follow-up B:** The framework is domain-agnostic. That means the entity taxonomy must use *abstract* type names that work across software, legal, medical, and any other domain. I'm going to propose three candidate approaches and I want you to pick one:

> **Option 1 — Pure abstraction:** Entity types are `[concept, entity, relationship_anchor, process, rule]` — no domain-specific terms at all. Projects map their domain onto these at Genesis.

> **Option 2 — Layered taxonomy:** A base layer of abstract types plus a domain-specific extension layer. Software projects extend `concept` into `[file, function, library]`. Legal projects extend it into `[statute, precedent, jurisdiction]`.

> **Option 3 — Tag-based:** No fixed taxonomy. Entities are typed by tags at write time. `("module:auth", "has_tag", "structural_entity")`. Flexible but harder to enforce consistency.

Which of these feels right to you — and why?



## Prompt:
4/21/2026, 2:40:32 AM

On question 2: I think an agent about to do something. But perhaps there are edge cases for what rules constrain or what does the know?

Follow-up A: "what does the <some_function.py> do and what files in the agent harness depend on it? 
Follow-up B: I need recommendations for this decision. I don't have enough expertise to assess which is most effective.



## Response:
4/21/2026, 2:42:16 AM

````plaintext
Thought process: Weighed taxonomy options and architected bidirectional graph traversal strategy.

The user is asking about Follow-up B - which entity taxonomy approach to recommend. This is a specification/brainstorming session, NOT a research task. The user wants my recommendation as the Graph Data Architect. This falls into the "brainstorm and specification only" mode of this project. The research instructions say to use launch_extended_search_task for queries that need current information, but this is an expert reasoning/recommendation question within the context of the specification session.

Actually, re-reading the research instructions: "CRITICAL INSTRUCTION: Always use the `launch_extended_search_task` to respond to the user's query by default, except for: Basic conversational responses, Extremely simple questions that Claude already knows."


I'm wrestling with whether this architectural recommendation needs external research or if I can reason through it from first principles. The user is asking me to choose between three design patterns I just outlined, which feels like it should fall within expert reasoning rather than a web search task. But the research instructions are pretty explicit about using the tool by default for almost everything.

Actually, I think I'm overthinking this. This is a specification session where I'm operating as the Graph Data Architect, and the user wants a crisp recommendation on which ontological design pattern fits best. That's something I can derive from knowledge graph fundamentals and the framework's own constraints without needing to look anything up. Pulling in research would just interrupt the flow of what should be a focused expert recommendation.

Now looking at the actual follow-up question about `some_function.py` — the user is really asking two things at once. They want to know what the function does and what depends on it, which would require querying both the function's own metadata and then finding all the reverse dependencies pointing to it.

This reveals something important: the graph needs to support bidirectional traversal. I can't just follow edges outward from a node; I also need to efficiently find what's pointing inward.

For the taxonomy question, Option 2 with a layered approach makes the most sense. Option 1's abstract categories are too vague to actually guide a graph traversal — an agent wouldn't know how to route through the graph with just `[concept, entity, relationship_anchor, process, rule]`. Option 3 loses all schema enforcement if tags can be applied freely. The layered taxonomy gives me both the consistency of base types and the flexibility to specialize them for different domains.

This mirrors how established knowledge graph systems work — Wikidata has abstract types with typed properties, schema.org uses hierarchies, and OWL separates upper ontologies from domain-specific extensions. The Validator Agent gets a contract to check against, the Pruning Agent can make informed deletion decisions based on type, and I maintain domain-agnosticism at the foundation while allowing richness where needed.

Now looking at what that agent query actually requires — asking what a function does and what depends on it — I need both forward and reverse traversal capabilities built into the core design.

The tricky part is that structural relationships are straightforward to express as triples: function definitions, parameters, return types. But the semantic "what does it do" question doesn't fit neatly into that model. I'd need something like a semantic_description field attached to entities themselves, similar to what the .larql example showed.

Now I'm thinking through the secondary queries the user mentioned—understanding what rules apply and what the model actually knows—these point to additional relation types I haven't fully accounted for yet. For the entity taxonomy itself, I'm leaning toward a layered approach where base abstract types sit at the schema level: structural_entity for discrete units like files and functions, domain_concept for ideas and knowledge, constraint_rule for standards and requirements, process for workflows, and version_artifact for snapshots.

Then each domain extends these base types with its own specifics—software breaks structural_entity into files and functions, legal breaks it into statutes and cases, medical into procedures and diagnoses. This gives me the flexibility of a domain-agnostic foundation while still allowing rich domain-specific specialization.

I need to formalize this into spec blocks for both the query analysis and the taxonomy recommendation, and I should flag those two additional relation families that emerged: constraint relations and epistemic relations that capture what the model knows and doesn't know.
````

# Graph Data Architect — Continuing Session 1

---

## Processing Your Answers

Let me work through both before producing spec output, because your Follow-up A answer is more revealing than it looks.

---

## On Follow-up A — The Primary Query

You said:

> *"What does `some_function.py` do, and what files in the agent harness depend on it?"*

This is actually **two structurally different queries** collapsed into one sentence — and the fact that you collapsed them tells me something important about what the graph needs to support.

**Query 1 — Forward lookup (what does this thing know about itself):**
```sql
SELECT relation, target FROM EDGES
WHERE entity = "func:some_function"
```
Returns: what it depends on, what it imports, what it returns, what it secures.

**Query 2 — Reverse lookup (what knows about this thing):**
```sql
SELECT entity FROM EDGES
WHERE target = "func:some_function"
AND relation = "depends_on"
```
Returns: everything that points *at* this function — its dependents.

This means your graph must support **bidirectional traversal**. Most simple graph schemas only define forward edges. The fact that your primary use case requires "what depends on X" means every edge must be traversable in both directions. That's a constraint I'll encode in the spec.

**On "what does it DO":** This is the trickiest part of your question, and I want to flag it now. Structural facts are easy to express as triples:

```
("func:verify_jwt", "requires_parameter", "JWT_Token")
("func:verify_jwt", "returns_type",       "UserSession")
("func:verify_jwt", "defined_in",         "module:auth")
```

But *"what does it do"* semantically — its purpose, its behavior — doesn't reduce cleanly to a triple. You can't write `("func:verify_jwt", "does", "validates JWT tokens and returns a user session")` and expect that string to be reliably retrievable via graph walk. That's a natural language description, not a structured relationship.

**This is a boundary condition your schema must define explicitly:**

> Semantic descriptions live as metadata on the entity node, not as graph edges. Graph edges express *structural and relational* facts only. An agent that wants to know "what does this do in plain language" reads the entity's `semantic_description` field. An agent that wants to know "what does this depend on" traverses edges.

This is the first hard constraint I'll encode.

**On your edge cases — "what rules constrain" and "what does the model know":**

These are valid and they reveal two additional relation families you need. You were right to flag them:

- **"What rules constrain this?"** → You need a `constraint` relation family. Example: `("module:auth", "must_comply_with", "OWASP_AuthStandard")`. This requires `constraint_rule` as a distinct entity type.

- **"What does the model know about this?"** → This is an **epistemic query** — asking not about the project but about the graph's own coverage. Example: *"Does the graph know anything about WebSockets before I start writing a WebSocket module?"* This is `SELECT * FROM EDGES WHERE entity = "WebSockets"`. If it returns nothing, the harness knows to trigger a documentation-scraping sub-routine before proceeding.

Both of these belong in the schema. Good catch.

---

## On Follow-up B — My Recommendation

I'll give you a clear recommendation with reasoning you can evaluate.

**My recommendation is Option 2 — Layered Taxonomy.** Here's why each option fails or succeeds:

**Option 1 (Pure Abstraction) fails** because it's too sparse to be useful. If every entity is just a `concept` or a `process`, an agent trying to distinguish "a Python file" from "an industry standard" has no schema support. The graph walk router has no signal. You also lose the ability for the Validator Agent to catch type violations — if anything can relate to anything, nothing is wrong.

**Option 3 (Tag-based) fails** because it has no enforcement. If agents can freely tag entities at write time, you will inevitably get `"module"`, `"Module"`, `"codebase_module"`, `"python_module"`, and `"js_module"` all meaning the same thing, written by different agents on different days. The graph becomes incoherent within weeks. Schema underspecification is the silent killer of this architecture.

**Option 2 (Layered Taxonomy) succeeds** because it solves both problems simultaneously:
- The base layer is abstract enough to be domain-agnostic
- The domain extension layer is specific enough to be useful
- The Validator Agent can enforce base-type contracts without knowing the domain
- The Pruning Agent can make deletion decisions based on type
- This is also how every successful large-scale knowledge graph works in practice — Wikidata, schema.org, OWL ontologies all use this exact pattern

**The structure I'm recommending:**

```
Base Layer (domain-agnostic — defined at Genesis Layer 1, same for every project)
│
├── structural_entity     ← a discrete, addressable unit (file, document, case)
├── domain_concept        ← a piece of knowledge (React_19, JWT, legal precedent)
├── constraint_rule       ← a governing rule or standard (Clean Architecture, HIPAA)
├── process               ← a workflow or operation (auth flow, appeal procedure)
└── version_artifact      ← a versioned snapshot of any of the above

Domain Extension Layer (defined at Genesis Layer 2, project-specific)
│
Software project:
├── structural_entity → [file, function, class, api_endpoint, library]
│
Legal project:
├── structural_entity → [statute, case, jurisdiction, precedent]
│
Medical project:
└── structural_entity → [procedure, diagnosis, medication, patient_protocol]
```

The base types never change. Domain extensions are written at Project Genesis and are part of what makes each `.vindex` file project-specific.

Now let me produce the first two formal spec blocks.

---

## Spec Output

---

### Entity Type Taxonomy — Spec Block

**What it must represent:**
The complete set of things that can exist as nodes in the knowledge graph. The taxonomy is two-layered: an abstract base layer that is domain-agnostic and portable across all projects, and a domain extension layer that is defined at Project Genesis and is specific to each project context.

**Base Type Vocabulary (five types, fixed):**

| Base Type | Definition | Example Entities |
|---|---|---|
| `structural_entity` | A discrete, addressable unit of work or artifact | file, function, document, statute, patient_record |
| `domain_concept` | A piece of knowledge, technology, or idea | React_19, JWT, common_law, neural_network |
| `constraint_rule` | A governing rule, standard, or requirement | Clean_Architecture, HIPAA, RFC_7519, PEP8 |
| `process` | A workflow, operation, or procedure | auth_flow, appeal_procedure, data_pipeline |
| `version_artifact` | A versioned snapshot of any of the above | api_schema_v2, vindex_v1.2, React_18 |

**Domain Extension Protocol:**
Projects register domain-specific subtypes at Genesis using the `subtype_of` relation:
```sql
INSERT INTO EDGES (entity, relation, target)
VALUES ("function", "subtype_of", "structural_entity")
```
All agent operations that accept `structural_entity` automatically accept `function`. The Validator enforces this inheritance contract.

**Hard constraints:**
- Maximum five base types. No new base types may be added without a privileged schema migration. This is a constitutional constraint.
- Domain subtypes must declare their parent base type at Genesis. An untyped entity is a schema violation.
- Entity names must be compositionally unambiguous — prefer `programming_language` over `language`, `codebase_module` over `module`.
- The schema taxonomy is itself encoded as triples in the graph — the graph knows its own structure.

**Polysemantic risk zones (entities to never use as raw tokens):**

| Dangerous Token | Use Instead |
|---|---|
| `model` | `llm_model`, `data_model`, `orm_model` |
| `type` | `data_type`, `entity_type`, `ts_type` |
| `schema` | `db_schema`, `graph_schema`, `json_schema` |
| `version` | `software_version`, `vindex_version`, `api_version` |
| `module` | `codebase_module`, `js_module`, `python_module` |
| `target` | Never use as an entity name — reserved term in triple model |
| `language` | `programming_language`, `natural_language` |
| `agent` | `ai_agent`, `http_agent` |

**Open questions (deferred):**
- Does `version_artifact` need to be a base type, or can versioning be handled as a metadata property on other entity types? Risk of over-engineering the base layer.
- How deep can domain extension subtypes go? Two levels? Unlimited? Unlimited depth creates graph walk routing problems.

**Interface contract (to write engine and validation layer):**
- Every entity written by the Coder Agent must declare a base type and optionally a domain subtype
- The Validator Agent may reject any write that omits entity type declaration
- MEMIT targets injection layers based on base type — `domain_concept` targets middle knowledge layers; `constraint_rule` targets a specifically designated rule layer
- The Pruning Agent uses base type to determine deletion eligibility: `foundational` domain concepts require privileged deletion; `structural_entity` instances may be pruned when the corresponding Git artifact is deleted

---

### Primary Query Patterns — Spec Block

**What it must support:**
The graph must answer at minimum three classes of agent queries. Schema design is organized to make all three efficient.

**Class 1 — Dependency Resolution (bidirectional)**
```sql
-- Forward: what does this entity depend on?
SELECT relation, target FROM EDGES
WHERE entity = "func:verify_jwt"

-- Reverse: what depends on this entity?
SELECT entity FROM EDGES
WHERE target = "func:verify_jwt"
AND relation IN ("depends_on", "imports", "calls")
```
*Use case: agent about to modify a function checks what will break.*

**Class 2 — Constraint Lookup**
```sql
-- What rules govern this entity?
SELECT target FROM EDGES
WHERE entity = "module:auth"
AND relation = "must_comply_with"
```
*Use case: agent about to write an auth module checks which standards apply before writing a line.*

**Class 3 — Epistemic Coverage Check**
```sql
-- Does the graph know anything about this technology?
SELECT * FROM EDGES
WHERE entity = "WebSockets"
```
*Use case: agent about to work with a technology checks if domain knowledge exists. Empty result triggers documentation ingestion before proceeding.*

**Boundary condition — semantic description:**
The question "what does this entity *do*" in natural language is not answered by graph traversal. It is answered by reading the entity's `semantic_description` metadata field, set at registration time. Graph edges encode structural and relational facts only. Natural language descriptions are metadata, not edges.

**Hard constraints:**
- All relation types must support reverse traversal. There are no write-only edges.
- An empty result on a Class 3 epistemic query must surface to the orchestrator as a named signal, not a silent empty set. The orchestrator decides whether to halt and trigger ingestion or proceed with degraded confidence.

**Open questions (deferred):**
- Should Class 3 epistemic queries return a confidence score — not just "does this exist" but "how well does the graph know this"? This would require coverage density metadata per entity cluster.
- How should agents handle partial coverage? (Some edges exist for `WebSockets` but they are three years stale.)

**Interface contract:**
- The query layer exposes all three query classes as named operations to agents — agents do not construct raw `larql` queries; they call named operations that compile down to `larql`
- The orchestrator receives query results with a `coverage_quality` flag: `{complete, partial, empty}`
- Empty epistemic results route to the documentation ingestion sub-routine before any write operation proceeds

---

## Session Summary Block — Session 1 (Partial)

```
DECISIONS MADE:
- Schema partition rule confirmed: LLM stores semantics (relationships, 
  dependencies, rules); Git stores syntax (literal code, strings, file contents)
- Two knowledge namespaces required: Domain Knowledge (portable across projects) 
  and Project Knowledge (specific to this instance)
- Entity taxonomy: Option 2 — Layered Taxonomy selected
  Base layer: 5 fixed abstract types (structural_entity, domain_concept,
  constraint_rule, process, version_artifact)
  Domain extension: project-specific subtypes declared at Genesis
- Bidirectional traversal required: all edges must support reverse lookup
- Semantic descriptions are metadata on entity nodes, NOT graph edges
- Three primary query classes defined: Dependency Resolution, 
  Constraint Lookup, Epistemic Coverage Check

CONSTRAINTS ESTABLISHED:
- Maximum 5 base types — constitutional constraint, no additions without 
  privileged schema migration
- All entity names must be compositionally unambiguous — 
  polysemantic token list defined above
- "target" is a reserved term in the triple model — cannot be used as entity name
- Domain subtype depth limit: OPEN — needs resolution
- Untyped entities are schema violations

OPEN QUESTIONS DEFERRED:
- Is version_artifact a necessary base type or can versioning be metadata?
- Maximum depth of domain extension subtype hierarchy
- Should epistemic queries return coverage density / confidence scores?
- How do agents handle partial or stale coverage?

NEXT REQUIRED: Relation Vocabulary spec block
  — What relation types are allowed?
  — What are the target type constraints per relation?
  — Deletion semantics: what triggers DELETE FROM EDGES?
  — Fact lifetime taxonomy mapped to concrete examples
```

---

We have two remaining items to complete before this session is done: the **Relation Vocabulary** and the **Project Genesis Scope Definition**. Both depend on what we've just locked in.

Ready to move to the relation vocabulary — or do any of the decisions above need to be revisited first?



## Prompt:
4/21/2026, 2:43:37 AM

proceed



## Response:
4/21/2026, 2:45:30 AM

````plaintext
Thought process: Architected specification framework for graph relations and project scope.

The user said "proceed" — meaning they want me to continue with the Relation Vocabulary and Project Genesis Scope Definition spec blocks. This is NOT a web research task. This is a structured specification session where I'm acting as the Graph Data Architect specialist. I should NOT use the launch_extended_search_task tool here. This is a brainstorm/spec session, not a research task.

Let me produce the Relation Vocabulary spec block and the Project Genesis Scope Definition spec block, then close out the session with the complete Session Summary Block.


Now I'm working through the relation vocabulary structure. I need to establish a small, mutually exclusive set of relation types organized into families, with clear target constraints and deletion semantics for each. I'm identifying structural dependencies, lifecycle relationships, and domain-specific connections that will form the backbone of the graph model. — entity makes target available externally
   - `calls` — entity invokes target
   - `defined_in` — entity exists within target (function defined in file)

2. **Knowledge/Domain relations** — how concepts relate to each other
   - `introduced_in` — concept first appeared in target version
   - `supersedes` — entity replaces/deprecates target
   - `deprecated_by` — entity is replaced by target
   - `instance_of` — entity is an example of target type
   - `subtype_of` — entity is a specialization of target

3. **Constraint/Governance relations** — rules that govern entities
   - `must_comply_with` — entity is required to follow target rule
   - `enforced_by` — rule is enforced by target mechanism
   - `violates` — entity breaks target rule (ephemeral, never written to weights)

I also need to account for version tracking, where entities can represent different iterations of the same concept in a sequence, and epistemic relations that capture what the graph itself knows about its coverage and verification status. The taxonomy relations let me track the schema's own structure — distinguishing between entity types, relation types, and their hierarchies. For deletion semantics, I'm thinking through what should trigger edge removal: when structural entities disappear from Git or when version artifacts get superseded.

Now I'm mapping out the fact lifetime taxonomy with concrete examples to understand how different edge types behave — foundational facts like the taxonomy itself are immutable, versioned facts like API schemas change discretely, mutable facts like exports shift as code evolves, and ephemeral facts from agent hypotheses never persist. For the minimum viable scope of Project Genesis, I need the taxonomy and relation vocabulary as triples, plus the project's constitutional constraints around language and architecture, domain knowledge from framework documentation, and the namespace boundary encoding.
````

# Graph Data Architect — Session 1, Continued
### Relation Vocabulary + Project Genesis Scope

---

## Relation Vocabulary

Before I produce the spec block, let me explain the design constraints I'm working within — because the relation vocabulary is where most schema designs fail.

**The core tension:** You want expressive enough vocabulary that agents can represent complex knowledge, but narrow enough that two agents independently writing facts use the same words. Every relation you add is a potential synonym collision. The goal is the **smallest set of mutually exclusive relation types** that covers all required query patterns.

I'm organizing the vocabulary into five families. Each family covers a distinct semantic territory, which makes synonym collisions detectable — if two relations feel like they mean the same thing, they're in the same family and one of them needs to be eliminated.

---

### Relation Vocabulary — Spec Block

**What it must represent:**
Every permitted labeled edge between two nodes in the knowledge graph. The vocabulary is finite, enumerated at Project Genesis Layer 1, and enforced by the Validator Agent. No relation may be used that was not declared in the vocabulary. Agents do not invent relation labels — they select from the approved vocabulary, extended only through a schema migration.

**The Five Relation Families:**

---

**Family 1 — Structural Relations**
*How entities are physically connected or composed.*

| Relation | Source Type | Target Type | Meaning |
|---|---|---|---|
| `depends_on` | structural_entity | structural_entity | Source cannot function without target |
| `imports` | structural_entity | structural_entity | Source brings target into its scope |
| `exports` | structural_entity | structural_entity | Source makes target available externally |
| `calls` | structural_entity | structural_entity | Source invokes target at runtime |
| `defined_in` | structural_entity | structural_entity | Source exists as a child of target |
| `contains` | structural_entity | structural_entity | Source is the parent scope of target |

*Why both `defined_in` and `contains`?* They are the same relationship traversed in opposite directions. `("func:verify_jwt", "defined_in", "module:auth")` and `("module:auth", "contains", "func:verify_jwt")` express the same fact bidirectionally. The schema may write one and infer the other, or require both to be written explicitly. This is a decision for the write engine spec — flagged as an open question.

---

**Family 2 — Knowledge Relations**
*How domain concepts relate to each other.*

| Relation | Source Type | Target Type | Meaning |
|---|---|---|---|
| `introduced_in` | domain_concept | version_artifact | Concept first appeared in this version |
| `supersedes` | version_artifact | version_artifact | Source replaces target; target becomes legacy |
| `deprecated_by` | domain_concept | domain_concept | Source is replaced; target is the successor |
| `requires_version` | structural_entity | version_artifact | Source requires at minimum this version |
| `documented_by` | any | domain_concept | Source is described by target reference source |

*Critical distinction:* `supersedes` is a relation between two `version_artifacts`. `deprecated_by` is a relation between two `domain_concepts`. Do not conflate them. React_18 is not deprecated by React_19 at the concept level — `useEffect_pattern_v18` is deprecated by `useEffect_pattern_v19`. The version artifacts supersede each other; the concepts within them deprecate each other.

---

**Family 3 — Constraint Relations**
*What rules govern an entity's behavior.*

| Relation | Source Type | Target Type | Meaning |
|---|---|---|---|
| `must_comply_with` | structural_entity | constraint_rule | Source is required to follow target rule |
| `governs` | constraint_rule | structural_entity | Rule applies to target entity |
| `enforced_by` | constraint_rule | process | Rule is verified by target process |
| `violates` | structural_entity | constraint_rule | Source currently breaks target rule — **EPHEMERAL ONLY** |

**Hard constraint on `violates`:** This relation must never be written to the permanent `.vindex`. It represents a transient state — a finding by the Validator Agent during a sandbox run. It lives in the L1 cache or the agent's working context only. If `violates` appears in a `.larql` patch submitted for MEMIT compilation, the write engine must reject it. This is a write-layer enforcement rule.

---

**Family 4 — Taxonomy Relations**
*The schema knowing its own structure.*

| Relation | Source Type | Target Type | Meaning |
|---|---|---|---|
| `subtype_of` | any entity type | base entity type | Source is a domain-specific subtype of target |
| `is_entity_type` | entity type name | "taxonomy" | Declares a type as valid in this project |
| `is_relation_type` | relation name | relation family | Declares a relation as valid in this project |
| `instance_of` | any entity | entity type | Declares what type this specific entity is |

*This family is what allows the graph to know its own schema.* The Validator Agent queries this family to check whether an incoming `.larql` patch uses declared types and relations. Without it, the validator has no schema contract to enforce against.

---

**Family 5 — Namespace Relations**
*Separating Domain Knowledge from Project Knowledge.*

| Relation | Source Type | Target Type | Meaning |
|---|---|---|---|
| `scoped_to` | any entity | "domain" or project_id | Declares which namespace this fact belongs to |
| `sourced_from` | domain_concept | domain_concept | Links a fact to the authoritative source that produced it |
| `verified_at` | any entity | version_artifact | Records the project state at which this fact was confirmed valid |

*Why this family matters:* When the Pruning Agent runs, it needs to know whether a stale edge belongs to domain knowledge (don't delete — it's universally true) or project knowledge (check Git — delete if the artifact is gone). `scoped_to` is the flag that answers this question.

---

**Deletion Semantics — What Triggers `DELETE FROM EDGES`:**

This is not a free operation. The following rules define when edges may be deleted, and by whom:

| Trigger | Relation Family Affected | Who Initiates |
|---|---|---|
| Corresponding Git artifact deleted or renamed | Structural Relations | Pruning Agent, via `git diff` scan |
| A `supersedes` edge is written | The superseded version's edges | Pruning Agent, on schedule |
| A `deprecated_by` edge is written | The deprecated concept's outbound structural edges | Pruning Agent, on confirmation |
| Validator returns `violates` finding | Nothing — `violates` was never written | No deletion needed |
| Schema migration removes a relation type | All edges using that relation type | Privileged orchestrator operation only |

**Hard constraint on deletion:** The Pruning Agent may only delete edges in the Structural and Knowledge families. Constraint Relations and Taxonomy Relations require a privileged orchestrator-level operation to delete. This prevents an agent from accidentally removing a governing rule or corrupting the schema's self-knowledge.

---

**Synonym Collision Register — Relations That Must Not Coexist:**

| Forbidden Pair | Why Dangerous | Resolution |
|---|---|---|
| `depends_on` / `requires` | Identical semantics — agents will use both | Use only `depends_on` |
| `calls` / `uses` / `invokes` | All mean "invokes at runtime" | Use only `calls` |
| `documented_by` / `described_in` / `references` | All mean "this source explains this" | Use only `documented_by` |
| `is_a` / `instance_of` / `type_of` | All attempt to express type membership | Use only `instance_of` |
| `supersedes` / `replaces` / `overrides` | All mean version succession | Use only `supersedes` |

**Hard constraint:** Any relation label that does not appear in the vocabulary is a schema violation. The Validator Agent rejects `.larql` patches containing undeclared relation labels before they reach the write engine.

**Open questions (deferred):**
- Should `contains` / `defined_in` be stored as two edges or one with inferred reverse? The write engine spec must resolve this — it affects MEMIT injection volume.
- Does the `verified_at` relation need to be a full Namespace Relation or can it be metadata on the edge itself? This is a triple model vs. quad model question. (A quad model adds a timestamp fourth field to every triple — more expressive, more complex.)
- How should the vocabulary be extended mid-project? Does adding a new relation type require a full schema migration or can it be proposed by an agent and approved by the Validator?

**Interface contract (to write engine and validation layer):**
- The Validator Agent receives the declared vocabulary at project load time from the graph's own Taxonomy Relations
- Any `.larql` patch containing an undeclared relation type is rejected before MEMIT is invoked
- The write engine (MEMIT) receives a relation family tag alongside each edge — this determines which FFN layers are targeted
- The Pruning Agent receives the deletion trigger rules as a policy document at initialization; it does not infer deletion rules from context

---

## Project Genesis Scope Definition

Now we can define what goes into the write-once initialization. Genesis is the only moment in the system where facts are written without a Coder Agent proposing them, a Validator testing them, and a PyTest sandbox confirming them. It is the constitutional layer — privileged, minimal, and expensive to revise.

**The design principle:** Genesis must be *thin enough to be correct* and *thick enough to be functional*. Every fact written at Genesis should be answerable to the question: **"Is the entire harness broken without this fact?"** If the answer is no, it doesn't belong in Genesis.

---

### Project Genesis Scope — Spec Block

**What it must represent:**
The minimum viable knowledge state required for any agent to begin operating. Organized into four sequential layers, each depending on the previous. Written once. Protected from casual modification.

---

**Genesis Layer 1 — The Schema Constitution**
*The graph's self-knowledge. Must be written first, before any domain facts, because everything else depends on these types being declared.*

```sql
-- Declare base entity types
INSERT INTO EDGES (entity, relation, target)
VALUES ("structural_entity",  "is_entity_type", "taxonomy"),
       ("domain_concept",     "is_entity_type", "taxonomy"),
       ("constraint_rule",    "is_entity_type", "taxonomy"),
       ("process",            "is_entity_type", "taxonomy"),
       ("version_artifact",   "is_entity_type", "taxonomy");

-- Declare relation families
INSERT INTO EDGES (entity, relation, target)
VALUES ("structural_relation", "is_relation_type", "taxonomy"),
       ("knowledge_relation",  "is_relation_type", "taxonomy"),
       ("constraint_relation", "is_relation_type", "taxonomy"),
       ("taxonomy_relation",   "is_relation_type", "taxonomy"),
       ("namespace_relation",  "is_relation_type", "taxonomy");
```

*Nothing after this layer can be written without the Validator finding a declared type to validate against.*

---

**Genesis Layer 2 — Domain Extension Declarations**
*Project-specific subtypes. Different for every project. Thin.*

```sql
-- Software project example:
INSERT INTO EDGES (entity, relation, target)
VALUES ("file",         "subtype_of", "structural_entity"),
       ("function",     "subtype_of", "structural_entity"),
       ("class",        "subtype_of", "structural_entity"),
       ("api_endpoint", "subtype_of", "structural_entity"),
       ("library",      "subtype_of", "domain_concept");

-- Legal research project example (same layer, different domain):
INSERT INTO EDGES (entity, relation, target)
VALUES ("statute",      "subtype_of", "structural_entity"),
       ("case",         "subtype_of", "structural_entity"),
       ("jurisdiction", "subtype_of", "structural_entity"),
       ("precedent",    "subtype_of", "domain_concept");
```

---

**Genesis Layer 3 — Project Constitutional Constraints**
*The architectural decisions that govern everything agents will build. The "you cannot do X in this project" layer. Written by the Architect Agent from the PRD.*

```sql
-- Technology choices
INSERT INTO EDGES (entity, relation, target)
VALUES ("this_project", "uses_language",      "Python_3.12"),
       ("this_project", "uses_framework",     "FastAPI"),
       ("this_project", "targets_environment","Docker_Linux");

-- Architectural rules
INSERT INTO EDGES (entity, relation, target)
VALUES ("this_project",    "must_comply_with", "Clean_Architecture"),
       ("database_layer",  "must_comply_with", "Repository_Pattern"),
       ("controller_layer","must_not_contain", "database_logic");

-- Namespace boundary
INSERT INTO EDGES (entity, relation, target)
VALUES ("this_project", "project_id", "core_api_service_v1");
```

*The `must_not_contain` relation needs to be added to the Constraint family — flagged as a vocabulary gap.*

---

**Genesis Layer 4 — Foundational Domain Knowledge**
*Facts about the technologies, frameworks, and standards the project depends on. Sourced from documentation ingestion. This is the layer you described in your Q5 answer.*

```sql
-- Framework knowledge
INSERT INTO EDGES (entity, relation, target)
VALUES ("useActionState", "introduced_in",   "React_19"),
       ("React_19",       "requires_version","Node_18"),
       ("JWT_RFC7519",    "governs",         "jwt_authentication"),
       ("FastAPI",        "documented_by",   "fastapi_official_docs");

-- Namespace declarations
INSERT INTO EDGES (entity, relation, target)
VALUES ("useActionState", "scoped_to", "domain"),
       ("React_19",       "scoped_to", "domain"),
       ("JWT_RFC7519",    "scoped_to", "domain");
```

---

**What Does NOT Belong in Genesis:**

| Excluded Item | Reason | Where It Belongs |
|---|---|---|
| Specific function implementations | Mutable; changes constantly | Written by Coder Agent during development |
| File contents or exact code | Literal syntax; Git's job | Git repository |
| Agent working hypotheses | Ephemeral; may be wrong | Active context window only |
| Bugs, violations, errors found during testing | Ephemeral findings | Validator's sandbox output; never `.vindex` |
| Speculative architecture decisions | Unstable; not yet validated | PRD / planning documents |

**Hard constraints:**
- Genesis writes require no Coder Agent proposal and no PyTest sandbox — but they do require a privileged Architect Agent role. This role must be defined in the security spec.
- Genesis Layer 1 and Layer 2 are truly write-once — modification requires a schema migration, not a standard `.larql` patch.
- Genesis Layer 3 and Layer 4 may be updated via standard write pipeline as the project evolves, but the update must be flagged as a constitutional change requiring elevated review.
- Total Genesis write volume should be bounded — if you find yourself writing thousands of triples at Genesis, the scope has drifted. Genesis is not "inject everything known." It is "inject only what agents cannot operate without."

**Open questions (deferred):**
- Who validates Genesis Layer 1? The Validator Agent doesn't exist yet when the schema constitution is written. This is a bootstrapping problem — the system needs a human or privileged initialization process for Layer 1 only.
- How is the Architect Agent authorized to write Genesis facts without passing through the standard PyTest sandbox? The security spec must define a Genesis-specific write authorization channel.
- Should foundational Domain Knowledge (Layer 4) live in its own `.vindex` file, shared across all projects, rather than being re-written at each project's Genesis? This would create a "universal base `.vindex`" that project-specific files overlay — potentially reducing Genesis time and improving consistency.

**Interface contract:**
- The Architect Agent produces Genesis Layers 2–4 as a single `.larql` file — the Genesis Patch
- Layer 1 is produced by the harness framework itself, not by any agent
- The Genesis Patch is the input to the initial MEMIT compile that mints `project_v1.vindex`
- All subsequent Coder Agent patches are validated against the schema declared in Layer 1 and Layer 2
- The State Ledger records the Genesis compile as commit hash `v0.0` — the root of the version tree

---

## Complete Session Summary Block — Session 1

```
SESSION: 1 — Graph Data Architect
SCOPE: Ontological schema, entity taxonomy, relation vocabulary, 
       query patterns, Project Genesis scope

═══════════════════════════════════════════════════
DECISIONS MADE
═══════════════════════════════════════════════════
D1. Schema partition rule: LLM stores semantics (relationships, 
    dependencies, rules, knowledge). Git stores syntax (literal 
    code, file contents, exact strings). This is a hard 
    architectural boundary.

D2. Two knowledge namespaces required: Domain Knowledge 
    (portable, scoped_to = "domain") and Project Knowledge 
    (project-specific, scoped_to = project_id). Different 
    pruning rules, different write authorization levels.

D3. Entity taxonomy: Layered Taxonomy (Option 2) adopted.
    Five fixed base types: structural_entity, domain_concept, 
    constraint_rule, process, version_artifact.
    Domain extensions declared as subtypes at Genesis Layer 2.

D4. Bidirectional traversal required. All edges must support 
    reverse lookup. No write-only edges.

D5. Semantic descriptions are metadata on entity nodes, 
    NOT graph edges. Graph edges encode structural and 
    relational facts only.

D6. Five relation families: Structural, Knowledge, Constraint, 
    Taxonomy, Namespace. Synonym collision register defined — 
    forbidden synonym pairs enumerated.

D7. `violates` relation is EPHEMERAL ONLY — never written 
    to .vindex. Write engine must enforce this as a hard 
    rejection rule.

D8. Pruning Agent may only delete Structural and Knowledge 
    family edges. Constraint and Taxonomy Relations require 
    privileged orchestrator-level deletion.

D9. Project Genesis organized into four layers:
    L1 — Schema Constitution (framework-generated, write-once)
    L2 — Domain Extension Declarations (Architect Agent, 
         write-once)
    L3 — Project Constitutional Constraints (Architect Agent, 
         elevated review required to modify)
    L4 — Foundational Domain Knowledge (Architect Agent, 
         updatable via standard pipeline)

D10. Genesis scope is bounded by the test: "Is the harness 
     broken without this fact?" If no, it doesn't belong 
     in Genesis.

═══════════════════════════════════════════════════
CONSTRAINTS ESTABLISHED
═══════════════════════════════════════════════════
C1. Maximum 5 base entity types — constitutional constraint.
C2. All entity names must be compositionally unambiguous — 
    polysemantic token list defined.
C3. "target" is reserved in the triple model — prohibited 
    as entity name.
C4. Untyped entities are schema violations.
C5. Undeclared relation labels in .larql patches are 
    schema violations — Validator rejects before MEMIT.
C6. `violates` relation rejected at write engine level.
C7. Genesis Layer 1 and 2 require schema migration to modify 
    — not patchable via standard .larql pipeline.

═══════════════════════════════════════════════════
OPEN QUESTIONS DEFERRED
═══════════════════════════════════════════════════
OQ1. Is version_artifact a necessary base type or 
     can versioning be edge metadata?
OQ2. Maximum depth of domain extension subtype hierarchy.
OQ3. Should epistemic queries return coverage 
     density / confidence scores?
OQ4. contains / defined_in: two edges or one with 
     inferred reverse? (Write engine spec must resolve)
OQ5. Triple model vs. quad model — does verified_at 
     need a fourth field per edge?
OQ6. Mid-project vocabulary extension protocol — 
     agent-proposed or orchestrator-only?
OQ7. Genesis bootstrapping problem — who validates 
     Layer 1 before the Validator Agent exists?
OQ8. Architect Agent Genesis write authorization — 
     what security channel bypasses PyTest sandbox 
     for Genesis only?
OQ9. Should Domain Knowledge (Layer 4) live in a 
     shared universal base .vindex rather than being 
     re-written per project?
OQ10. `must_not_contain` relation — add to Constraint 
      family vocabulary? Needs confirmation.

═══════════════════════════════════════════════════
INTERFACE CONTRACTS DEFINED
═══════════════════════════════════════════════════
IC1. Write engine (MEMIT Specialist):
     - Receives entity base type tag to determine 
       target FFN layers
     - Receives relation family tag to determine 
       injection strategy
     - Must enforce hard rejection of `violates` 
       relation at compile time
     - Genesis Patch (.larql) is first input — 
       mints project_v1.vindex

IC2. Validation layer:
     - Receives declared vocabulary from graph 
       Taxonomy Relations at project load
     - Rejects patches with undeclared types 
       or relation labels
     - Class 3 epistemic query empty result must 
       surface as named signal to orchestrator

IC3. Pruning Agent:
     - Receives deletion trigger policy at 
       initialization
     - Uses scoped_to namespace flag to distinguish 
       domain vs. project knowledge
     - Restricted to Structural and Knowledge 
       family deletions only

IC4. Orchestrator:
     - Receives query results with coverage_quality 
       flag: {complete, partial, empty}
     - Empty epistemic results route to documentation 
       ingestion before write operations proceed

═══════════════════════════════════════════════════
INPUT REQUIRED FOR SESSION 2
═══════════════════════════════════════════════════
Session 2 should be: MEMIT Specialist
Primary input from this session:
  — Entity type taxonomy and base type list (D3)
  — Relation family tags and their FFN layer 
    targeting requirements (D6)
  — `violates` hard rejection rule (D7)
  — Genesis Patch as first MEMIT input (IC1)
  — OQ4 (contains/defined_in) must be resolved 
    in write engine spec
  — OQ1 (version_artifact as base type) should 
    be resolved before write engine targets layers
```

---

Session 1 is complete. The schema contract is now defined well enough to hand to the MEMIT Specialist — they need the entity types, relation families, and injection constraints to specify how facts actually get written into weight space.

When you're ready, say `/memit-specialist` to begin Session 2.





---
Powered by [Claude Exporter](https://www.ai-chat-exporter.net)