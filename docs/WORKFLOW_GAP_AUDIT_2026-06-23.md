# Workflow Gap Audit — Governance Promotion Path (2026-06-23)

> **Status: LEAD (not CORPUS evidence).** Method = InfraNodus structural-gap lens over assembled corpora → grep-verified. Per the repo fence (`SESSION_BOOTSTRAP §5`), InfraNodus output is a lead; the binding part here is the **lexical zero-check**, which is primary-source grep, not the lens.

## Method
- Corpora: **WORKFLOW / promotion machinery** (`DISCIPLINE.md` + `docs/WORKFLOWS_OVERVIEW.md`, 37 KB full body) vs **GOVERNANCE prototype layer** (`CORPUS/10_G1_TWO_PHASE_COMMIT`, `11_G2_SECURITY_LAYER`, `05_SPEC_CONTRACTS_BY_DOMAIN`, `domains/warden_PACKAGE`, `docs/SPEC_E2E_GROUND_TRUTH`, 32 KB full body).
- Tools: `difference_between_texts` (workflow=target) + `merged_graph_from_texts`, `detectEntities`.

## Verified finding (GAP A) — the governance layer has no promotion-path edge
Experiment **findings** have a full graduation ladder: hypothesis register → `PROGRESS` → `CORPUS`, gated mechanically by `closeout_check.py` (fingerprint token) + the pre-commit hook. The governance **prototype** layer has **none of this**. Grep over the promotion machinery, governance-lifecycle vocabulary:

| term | hits | term | hits | term | hits |
|---|---|---|---|---|---|
| issue | 0 | two-phase | 0 | retention | 0 |
| revoke | 0 | rollback | 0 | break-glass | 0 |
| expire | 0 | ceremony | 0 | burst | 0 |
| quorum | 0 | warden | 0 | concurrency | 0 |
| lease | 0 | transaction | 0 | immutability/tamper | 0 |

`commit`(17)/`lock`(20)/`hold`(6)/`token`(5) **do** appear but in git-commit, write-lock, dependency-hold, and closeout-fingerprint senses — **not** the governance senses (sense-checked).

## Exact missing edges (InfraNodus `contentGaps`, located then grep-confirmed)
1. **Two-phase-commit / transaction-controller (G1) ⇸ anti-drift "read contract" (fingerprint/stale/currency).** Same word *commit*, disjoint senses, never connected. The workflow's commit-integrity (hooks, fingerprints, closeout) stops at **narrative/result edits** and does not extend to **governance transaction state**.
2. **Closeout/gate ⇸ governance lifecycle events.** `closeout_check` validates a result-ref; there is no analog that validates/promotes a ceremony-token issuance, a revocation, a retention-expiry, or a quorum.
3. **Immutability / tamper audit-trail (governance) ⇸ no workflow audit-verification step** (`audit`=2, incidental).
4. **G2 security/authorization layer ⇸ experiment validation cycle** (corroborates the separate "no spec-level threat/security gate" gap from the heading-level run).

## Caveat (design intent)
Governance prototypes are explicitly **design-viability-only** — so *some* disconnect is intended. The genuine defect is the **absent graduation gate**: when a governance prototype is ready, there is no documented path to move it into operational discipline, the way experiments have one.

## Other gaps from the heading-level run (same method, lower-resolution)
- **GAP B — No spec-level threat-model / security-review gate.** Workflow "security" = secret-scanning only (pre-commit hook, gitignored creds = operational hygiene). The repo's threat model, `CORPUS/05_SPEC_CONTRACTS_BY_DOMAIN`, `CORPUS/11_G2_SECURITY_LAYER`, and the `security-review` skill are not wired into the experiment/closeout cycle. Adversarial *science* review exists (cross-model council, gpt-5.5 at promote gates); adversarial *security/threat* review does not. (Deep run corroborated: edge #4 above.)
- **GAP C — Deployment/serving mentioned but not gated (weak lead).** Deploy/CPU/GGUF gets 23 mentions but as a *constraint*, not as a stage with its own validation gate the way edits have one. Ties to the untested E1 deployment loop. Flagged as a lead, not asserted.

## Ruled OUT (InfraNodus surfaced them in the repo cluster, but the workflow DOES cover them)
eval/benchmark methodology (18 hits) · prior-art ingestion (12) · reproducibility/determinism (9) · findings-promotion ladder (10, well-defined). Not gaps.

## Implication
If/when a graph index (llm-wiki layer 1) is built, **governance** and **threat-model** should be first-class nodes so their island status stays diff-visible instead of being rediscovered.

## Provenance
InfraNodus `difference_between_texts` + `merged_graph_from_texts` (two runs: heading-level full-repo, then full-body governance-vs-promotion). Both returned `modularity:0` on small corpora → relied on `contentGaps` + primary-source grep. Tracked as leads in `docs/HYPOTHESIS_REGISTER_2026-06-18.md §W` (W1–W3).
