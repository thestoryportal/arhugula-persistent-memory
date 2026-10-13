## 17. Concurrency Control — Lock vs. Hold (T8)

### 17.1 Separation of Concerns

The original scope lock (D59/D60) was conflating three concerns. The lock/hold split cleanly separates them:

| Concern | Mechanism | TTL | Purpose |
|---|---|---|---|
| Concurrent write prevention | Write Lock | 60 min | Throughput / sequencing |
| Dependency preservation | Dependency Hold | 72 hr renewable | Correctness across escalation |
| Pruning exclusion | Dependency Hold (subset) | 72 hr renewable | Prevent GC of in-use edges |

### 17.2 Write Lock — Unchanged D59/D60

- Acquired at task declaration.
- 60-minute TTL, auto-release.
- Blocks *other agents* from writing to region.
- Scope: the declared write region.
- Conflicts resolved at assignment, not commit (C-CW4).

### 17.3 Dependency Hold — New (T8)

- Placed on specific edges the task is *reading*.
- 72-hour TTL, renewable on escalation events (Peer Agent review, Human Queue residency).
- Blocks *Pruning operations only*.
- Does not block other Write Locks or overwrites by other agents.
- Released on task completion, abort, or TTL expiry.
- PREPARED-state timeout does NOT automatically release the Hold (D85). Hold persists until successful commit on retry or operator-signed Hold release (GOVERNANCE category, signed ceremony).

### 17.4 Task Resume Re-Verification

On escalated task resumption:
1. Orchestrator reads current state of held edges.
2. Compares against escalation-entry snapshot.
3. **Unchanged:** task resumes with original context.
4. **Changed:** `context_stale` — task repackaged with current state, reassigned fresh.
5. **Hold expired:** `context_lost` — may require `dependency_reconstruction_required` escalation.

### 17.5 Interaction with 24-Hour Pruning Floor

Stratified rule:
- Edge age < 24 hours: never prunable (D56 floor).
- Edge age ≥ 24 hours AND under active Dependency Hold: not prunable while held.
- Edge age ≥ 24 hours AND no active holds: prunable per normal D54–D57.

### 17.6 Pruning Pre-Check

Before patch submission, Pruning Agent queries Orchestrator for Hold state on target edges (IC-PA7). Held edges excluded. If exclusion drops patch below meaningful size, Pruning logs deferral and reschedules. Excluded edges accumulate in `stale_urgent` count but flagged `held_not_prunable`.

---

═══════════════════════════════════════════════════
# PART V — OPEN QUESTIONS AND v2 ROADMAP
═══════════════════════════════════════════════════

