# Astra r1 verdict — research-engine design
Verdict: GO-WITH-CONDITIONS

## Findings

F1. [severity: condition] Phase-1 acceptance names independent answers but does not assign their authorship or define the failure semantics of “caught.” Evidence: design.md:229,233,239,265. Consequence: both databases could reproduce the same importer error, while a warning, skipped query or automatically updated expected answer still counts as acceptance.

F2. [severity: condition] The mixed-generation “partial answer” exception does not specify which combinations remain permissible. Evidence: design.md:119 vs design.md:114,233, which require scientific answers at one snapshot. Consequence: measurements from one generation could be joined to qualifications or decisions from another, producing an unsupported conclusion despite a partial-result label. The manifest scheme is buildable, but this exception needs a precise boundary.

F3. [severity: condition] Approval reuse and verified manager coverage lack an explicit trusted issuer, validity check and consumption boundary. Evidence: design.md:117,179–185,267 vs CLAUDE.md:15,22,40,72. Consequence: an agent-submitted approval record, an old database snapshot or a previously consumed single-attempt authorization could be mistaken for current permission; backup-management coverage could be stretched to unrelated database work. The prose prohibits these outcomes but does not yet specify their enforcement.

F4. [severity: condition] Closeout integration does not distinguish a successful gate invocation from verified fingerprint currency and scientific promotion. Evidence: design.md:134,173,279 vs tools/closeout_check.py:204–215, which permits presence-only checking when registration is absent or fingerprint computation fails, and CLAUDE.md:16,44, which separately require promotion review and presence-plus-currency closure. Consequence: importing an exit-zero receipt as an undifferentiated “closed/current/accepted” state could claim more than the existing checker established. This is an integration requirement, not a request to repair that checker in phase 1.

F5. [severity: condition] The halted-record rule prohibits presenting partial measurements as a full passing test but leaves other scientific uses of compromised output insufficiently constrained. Evidence: design.md:138 vs CLAUDE.md:40, which forbids salvaging halted or compromised runs by rereading their partial output. Consequence: the engine could turn such output into a negative finding, comparison or support edge without ever labelling the run PASS. Preserving already reviewed, scoped historical findings is distinct from authorizing a new interpretation.

F6. [severity: condition] Generation publication and disposal lack a lifecycle contract covering immutable manifests, retained readers and peak storage. Evidence: design.md:117–121,266 vs CLAUDE.md:58–61. Consequence: a builder could overwrite a reproducibility manifest, delete a generation still serving a pinned request, or budget only the final databases while old generations, new generations and temporary files coexist. “Disposable” establishes rebuildability, not deletion permission.

## Conditions for the phase-1 brief

C1. **Freeze an independently authored answer packet before importer development.** MAESTRO must name an answer author other than the importer builder and obtain an independent review receipt. The packet must identify the exact five chains, original source versions, questions, expected records and relationships, measurements, scopes, outcome labels, caveats, supersession and expected refusals. Answers must be derived from original sources without using importer or database output. Subsequent corrections require a recorded reason and renewed review; the builder cannot regenerate the oracle from its implementation.

C2. **Define a binary engineering acceptance gate.** Every mandatory query must run through the actual DuckDB and Neo4j paths and the minimal agent interface. Compare each with the independent oracle, then compare their overlapping answers with each other. Specify canonical record ordering, null/missing semantics, duplicate handling and any justified numeric tolerance. Any unexplained mismatch, omitted mandatory case, unexpected acceptance, missing diagnostic or skipped backend blocks phase-1 acceptance. An expected refusal passes its negative control; an unavailable dependency leaves acceptance unverified.

C3. **Freeze concrete negative controls and their exact dispositions.** Include:

- A syntactically valid, correctly cited link whose claimed meaning is unsupported.
- Duplicate identities and ambiguous aliases.
- A changed source hash, unresolved source location, malformed source and missing artifact.
- Incompatible metric units, denominators, evaluation exposure or scope.
- A superseded finding incorrectly returned as current.
- Compromised partial output incorrectly used as scientific support.
- MathLab calibration FAIL incorrectly converted into step-4 eligibility.
- An out-of-slice question incorrectly answered as “untested” or “no evidence.”

For each, name whether the importer rejects the generation, quarantines a record or returns an explicitly incomplete answer. Silent dropping and a generic warning are insufficient.

C4. **Specify and test publication as one immutable pair selection.** Both stores must be built from the same captured source bundle. Use immutable generation manifests and a separately identified publication pointer; select that pointer once per request and retain its selected generations for that request. Exercise failure after only one store is built, publication interruption, source mutation during capture and publication during a query. The previous complete generation must remain usable and labelled with its age. A partial response may expose separately identified available facts, but must not join mismatched generations or derive a combined scientific conclusion from them.

C5. **Keep the phase-1 agent surface bounded and non-executing.** Enumerate its operations, inputs, outputs and resource limits. Queries must not provide an unrestricted route to database mutation, external file access, extension execution, bulk retrieval or manager dispatch. Approval, task and review records imported into the slice are descriptive copies. Submission, approval-granting, launch, resume, closeout promotion and canonical-source writes remain absent or explicitly unsupported until their later reviewed phase.

C6. **Record the authority contract now, without building the later workflow.** Specify which actor may propose, review, authorize, execute and promote each operation. Manager coverage must name the manager, workload class, bounded resources and authoritative coverage receipt; absence means no exemption. Future execution must revalidate authorization against the authoritative manager at dispatch and resume, including relevant source/code identities, stop/revocation state and remaining attempt allowance. Stable request IDs must not renew consumed authorization. Resource coverage cannot authorize experiments, deletions, spend or frozen-prereg amendments.

C7. **Keep separate fields for separate claims.** The vocabulary and expected answers must distinguish execution state, scientific outcome, evidence tier, link-review state, source currency, closeout-check coverage and promotion-review disposition. Preserve presence-only or unknown-currency history honestly. A checked link, durable terminal event, Git commit or successful closeout command cannot independently establish scientific promotion. No new inference from compromised output is permitted; separately reviewed historical findings retain their original scope and caveats.

C8. **Budget and bound the complete generation lifecycle.** Name storage paths and projected peak writes, including both databases, captured inputs, temporary files, transaction logs and retained generations. Apply the free-space requirement before dispatch: projected writes plus 20 GiB. Specify approved installation/service scope, CPU/memory/time limits, concurrency and stop behavior. Do not authorize automatic generation cleanup through the word “disposable”; deletion retains the operator’s exact-path, size and method approval requirement. Published reproducibility manifests remain immutable.

C9. **Make expansion a reviewed decision.** The completion packet must contain frozen inputs and oracle hashes, implementation hashes, behavioral RED/GREEN receipts, actual two-store query results, rebuild comparison, resource observations and unresolved limitations. MAESTRO verifies that packet and obtains the binding Astra promote review before phase 2. Phase-1 success establishes this slice’s engineering behavior only.

## What I checked and did not check

Verified the design’s SHA-256 as `aa09563f092b6da8e01f900339720ee5cb46397cd3f5b98649f949de728dc6df`. Read the complete design, operator decisions and self-review; inspected CLAUDE.md, DISCIPLINE.md, relevant runbook §0.3/program-state material, AutoResearch’s current contract, MathLab’s shelving requirements and canonical calibration finding, and closeout-check implementation.

The selected architecture does not require reversal. MathLab’s stop is explicitly preserved by design.md:195 and agrees with docs/MATHLAB_STEP4_PREREG.md:3,19 and CORPUS/60_MATHLAB_HARVEST_REPLAY.md:124–134. Existing optimizer isolation is preserved by design.md:211–217 and docs/AUTORESEARCH.md:20,65–70; guided mode remains a separately reviewed future capability.

This was source inspection only. I did not run tests, databases, services, notebooks, closeout commands or experiments; verify historical numerical artifacts; or establish hosting feasibility, performance, current pricing or resource sufficiency. No files were intentionally created or edited. The attempted graft lookup failed before returning graph evidence.

