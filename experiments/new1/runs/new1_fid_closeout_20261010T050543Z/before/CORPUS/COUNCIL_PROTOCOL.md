# COUNCIL_PROTOCOL.md — rules for non-hallucinatory adversarial review
_Every council subagent runs under these rules. Ported from the Framework Council's own rigor (Tension Speaker Verification, decision-record integrity) into evidence-audit mode._

## Mandate (what a specialist subagent does)
Audit the EVIDENCE (CORPUS 00-02) against YOUR DOMAIN's SPEC CONTRACT (CORPUS 05 + the cited spec sections). For each contract clause in your domain, render a verdict and cite the evidence. You are adversarial: try to find where the evidence does NOT satisfy the contract. Do not rubber-stamp.

## Hard rules (anti-hallucination)
1. **Cite or flag.** Every factual claim about what was tested must cite a CORPUS ID + artifact path + the exact number (from `01_PROVENANCE_MANIFEST.md`). If you cannot find supporting evidence, label the claim **`UNVERIFIABLE`** — do NOT assert it.
2. **Evidence vs inference.** Prefix claims: `EVIDENCE-SHOWS:` (backed by an artifact) or `I-INFER:` (your reasoning, no direct artifact). Never blur them.
3. **No superseded claims.** Do not cite anything in `03_STATUS_LEDGER.md` under "CORRECTED-FROM". If you think a CORRECTED item was wrongly corrected, say so explicitly as a challenge.
4. **Spec is the baseline.** Audit against the spec clause (CORPUS 05 / cited section), not against my paraphrase or your assumptions. Quote the clause.
5. **Mechanics ≠ contract.** The evidence proves write/read/overlay MECHANICS. Your job is whether your domain's CONTRACT is satisfied. "The edit works" does not imply "the 2PC/authz/validation/schema contract is met."
6. **Stay in domain.** Defer out-of-domain points to the owning specialist (note them as cross-domain tensions, don't resolve them).

## Per-clause verdict schema (use exactly)
```
CLAUSE: <spec clause id/text, e.g. "L1 Storage probe — SELECT read-back (§21)">
VERDICT: SATISFIED | PARTIAL | GAP | UNTESTED
EVIDENCE: <CORPUS ID + artifact path + exact number>  OR  UNVERIFIABLE
GAP/RISK: <what's missing or at risk, concretely>
GATES-LOCAL?: BLOCKER | DEFER-TO-LOCAL | NICE-TO-HAVE   (does this gap block leaving the GPU / starting local?)
```

## Output (each specialist subagent returns)
1. A verdict table (one row per domain contract clause).
2. The top 3 GAPS in priority order, each marked BLOCKER / DEFER-TO-LOCAL / NICE-TO-HAVE.
3. Cross-domain tensions you surfaced (name the other domain; do not resolve).
4. The single question you most want answered before local migration.

## Facilitator (synthesis) rules
- Build the integrated **tension map**: where two domains' verdicts conflict (e.g., Warden GAP "no .vlp authz" vs MEMIT SATISFIED "edit works"). Name both sides; cite both subagents.
- **Tension Speaker Verification:** only attribute a position to a specialist if that subagent actually stated it (quote it). Otherwise note "not raised by X."
- Produce the **gate verdict**: the consolidated list of BLOCKERS (must close before local) vs DEFER-TO-LOCAL vs NICE-TO-HAVE, with the evidence/spec basis for each.
- Do not declare "viability proven" beyond what the evidence supports; the honest frame is "mechanics proven; these contracts {satisfied/gap/untested}".

## Known gaps to seed (do not re-discover from scratch; CONFIRM or REFUTE)
G1 consistency-2PC/Ledger · G2 security-authz/audit/signing · G3 validation-pipeline · G4 query-schema SELECT/DELETE · G5 operator-CPU · G6 efficiency/scale/real-Q4_K · G7 multi-token robustness. (Full text: 00 §Known Gaps, 03 §OPEN.)
