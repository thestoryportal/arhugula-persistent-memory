## 7. Schema Layer

### 7.1 Schema/Code Partition

The schema defines what the graph can represent. The LLM stores **semantics** — relationships, dependencies, rules, knowledge. Git stores **syntax** — literal code, file contents, exact strings. This partition is a hard architectural boundary (D1). The LLM provides the map; Git provides the territory.

### 7.2 Entity Taxonomy

Five fixed base entity types (D3). Maximum five is a constitutional constraint (C1):
- `structural_entity` — files, modules, classes, functions.
- `domain_concept` — knowledge facts, named entities from the problem domain.
- `constraint_rule` — architectural rules, must-follow patterns.
- `process` — workflows, pipelines, execution sequences.
- `version_artifact` — *removed as an FFN base type* (closed via D17). Version metadata lives in the State Ledger, not the graph.

Domain extensions are declared as **subtypes** during Genesis Layer 2.

### 7.3 Relation Families

Five relation families (D6):
- **Structural** — `contains`, `defined_in`, `depends_on`, `imports`.
- **Knowledge** — `describes`, `associated_with`, `derived_from`.
- **Constraint** — `must_precede`, `must_not_contain`, `requires`.
- **Taxonomy** — `is_a`, `subtype_of`.
- **Namespace** — `scoped_to`, `belongs_to`.

The `contains`/`defined_in` pair is specified as **one canonical directed edge** (`defined_in`, child→parent). The write engine auto-generates the reverse; agents declare the canonical direction only (D16, closes OQ4).

### 7.4 Knowledge Namespaces

Two mandatory namespaces (D2):
- **Domain Knowledge** — portable across projects, `scoped_to = "domain"`.
- **Project Knowledge** — project-specific, `scoped_to = project_id`.

Different pruning rules and different write authorization levels apply per namespace.

### 7.5 Polysemantic Discipline

- All entity names must be compositionally unambiguous (C2).
- `target` is reserved in the triple model and prohibited as an entity name (C3).
- Untyped entities are schema violations (C4).
- Undeclared relation labels in `.larql` patches are schema violations (C5), rejected by the Validator before MEMIT.
- Semantic descriptions are metadata on entity nodes, never graph edges (D5).

### 7.6 Traversal and Ephemeral Relations

Bidirectional traversal is required (D4). Every edge supports reverse lookup; no write-only edges.

The `violates` relation is **ephemeral only** (D7) — never written to `.vindex`. The write engine hard-rejects any `.larql` patch containing `violates` (C6, C9).

### 7.7 Project Genesis (Four Layers)

Genesis organizes the initial knowledge compile into four layers (D9):
- **L1 — Schema Constitution** (framework-generated, write-once).
- **L2 — Domain Extension Declarations** (Architect Agent, write-once).
- **L3 — Project Constitutional Constraints** (Architect Agent, elevated review required).
- **L4 — Foundational Domain Knowledge** (Architect Agent, updatable via standard pipeline).

Genesis L1–L2 require schema migration to modify (C7). The scope test: *"Is the harness broken without this fact?"* If no, it does not belong in Genesis (D10).

### 7.8 Deletion Authority

Pruning Agent may delete Structural and Knowledge family edges only (D8, D54). Constraint and Taxonomy relations require privileged orchestrator-level deletion.

