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