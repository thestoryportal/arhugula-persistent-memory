# Astra spec r2 verdict — research-engine phase 1
Verdict: GO-WITH-CONDITIONS

## R1-R4 status

R1. PARTIAL — AC17 has checkable refusal, cancellation, termination, observation-failure and no-surviving-watcher predicates (`phase1_spec_v2.md:47`). Section 11 assigns MAESTRO ownership, one-second observation and termination within 30 seconds (`phase1_spec_v2.md:205`). However, the authoritative signal remains unnamed (`phase1_spec_v2.md:236`). Blocking dispatch is an acceptable fail-closed resolution pending that external prerequisite; it does not complete R1’s requirement to name the authority.

R2. APPLIED — AC8–AC10 explicitly cover rejected mutations, integrity verification, generation-scoped identities and preservation of prior generations (`phase1_spec_v2.md:38–40`). Section 7 requires same-generation endpoints, candidate-reuse rejection, published node/relationship update/delete rejection, same-ID payload-change controls, unchanged digests and old-pair answers after each rejection, and incomplete answers on corruption (`phase1_spec_v2.md:139–147`).

R3. APPLIED — AC17 specifies inherited niceness 0→10, 10→10 and >10 unchanged, with observed values ≥10 and unavailable-observation refusal (`phase1_spec_v2.md:47`). The operational rule covers every owned Python/Java process (`phase1_spec_v2.md:203`).

R4. APPLIED — AC20 requires the frozen MAESTRO-owned decision ID and archived exit-zero, ALL GREEN, currency-active closeout receipt; missing receipts, fingerprint errors and presence-only results block closure/phase 2 (`phase1_spec_v2.md:50`). Ownership, canonical updates, scope separation and pending builder status are explicit (`phase1_spec_v2.md:66–72,221–223`).

## Findings

S1. [severity: condition] The pending-science authority is still an unresolved freeze prerequisite. Evidence: `phase1_spec_v2.md:3,205,236`; `astra_spec_r1_verdict.md:17`. Consequence: the draft safely prohibits dispatch, but AC17’s authority-dependent controls cannot be concretely frozen until MAESTRO identifies the source, semantics and observation route. The cited process gate observes running processes and tmux sessions; it does not establish pending launch intent (`tools/c10w_p2_gate.py:73–84`).

## Required before freeze

Complete the existing section-13 admission assignment. At minimum, the frozen signal contract must specify:

- **Authority and scope:** exact source/path/interface, authoritative writer and reservation owner, and coverage of every science coordinator whose pending or running work must take priority.
- **Unambiguous state:** explicit valid idle, pending and running states; pending begins before waiting for science admission and persists through that wait. Missing, malformed, stale or unreadable state cannot mean idle.
- **Validity and transitions:** source identity/version, freshness rule, restart handling and coherent updates. Multiple pending launches must not collapse to idle when only one finishes or withdraws.
- **Coordination:** defined ordering between pending publication and research-engine admission/publication, preventing an idle-check race from admitting new work after science becomes pending. Research-engine reservations cannot suppress the signal or delay science.
- **Observable enforcement:** a non-Python observation/termination route, bounded observation latency, an explicit starting point for the 30-second termination deadline, and receipts identifying every owned process and confirming termination.

These instantiate the obligations already required at `phase1_spec_v2.md:205,236`. Freeze deterministic AC17 cases for pending/running at start, idle→pending during work, authority loss/invalidity, and confirmed termination. Include a valid-idle positive control so an always-refusing implementation cannot pass. Actual host termination remains an acceptance obligation; fixture success cannot discharge it (`phase1_spec_v2.md:47,205`).

No further R2–R4 changes are required. The existing section-13 freeze prerequisites remain binding.

## What I checked and did not check

Verified both supplied SHA-256 values exactly:

- v1: `09cdd80e3a365d02969cbf559440326fb69916847f5916eba27642564307e0a0`
- v2: `2e021f9228c308c9508578e734ea4daffdd3ae15af10eb2d86045c5dafb2f139`

Read the r1 verdict, v2, the complete v1→v2 diff, and the cited admission, niceness and closeout sources. No existing v1 requirement was weakened or dropped. Changes are confined to the affected ACs, sections 7/11/13, R4’s necessary ownership/completion additions in sections 3/12, and the new section-14 change table. No unrelated section was altered.

I did not re-review settled scientific chains or operator choices, establish repository-wide absence of another pending-science signal, or validate implementation/host behavior. No tests, services, installations, science, closeout commands or file edits were performed.

🌱 graft reported ~146,543 tokens saved this turn, 1 successful call; its results supplied no review evidence.