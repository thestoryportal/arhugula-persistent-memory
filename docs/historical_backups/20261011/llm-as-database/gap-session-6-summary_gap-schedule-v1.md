# Gap Session 6 Summary — State Consistency Theorist

**Gap schedule version:** v3
**Skill invoked:** state-consistency-theorist
**Gaps addressed:** GAP-12 (verification), GAP-14 (primary work)
**Active baseline:** v1.1 integrated spec

---

## Part 1 — GAP-12 Closure Verification

The v1.1 D89 / IC-LDG-RETAIN closure is **substantively complete** on the retention-policy axis (default, immutability-downward, GOVERNANCE extension, unconditional `INTEGRITY_VIOLATION` retention, archival format). Two latent sub-questions surface on reread.

### GAP-12 Sub-Q1 — `PROJECT_CLOSED` writer path

**Problem.** v1.1 §16.7 says `PROJECT_CLOSED` is a LIFECYCLE signed ceremony. v1.1 also states W2 is "one-time bootstrap only." `PROJECT_INITIATED` is correctly W2 (bootstrap mint). `PROJECT_CLOSED` therefore cannot use W2 — it is terminal, not bootstrap.

**Resolution.** `PROJECT_CLOSED` is routed through **W1** (signed ceremony writer), classified as LIFECYCLE-terminal rather than GOVERNANCE. This requires one spec clarification:

> **Clarification (v1.1 §16.3 / §16.7):** The W1 writer path accepts signed ceremony entries regardless of classification — GOVERNANCE entries (retention extension, threshold tuning, key rotation) and LIFECYCLE-terminal entries (`PROJECT_CLOSED`) both flow through W1. W2 is strictly bootstrap mint (`PROJECT_INITIATED` only). Classification tag is orthogonal to writer path selection for signed ceremonies.

No new interface contract required — this is a readability fix in §16.3 language that collapses a false dichotomy between "W1 = GOVERNANCE" and "W2 = LIFECYCLE." Writer path is selected by ceremony class (signed vs. bootstrap mint vs. sync vs. async), not by entry-type classification.

### GAP-12 Sub-Q2 — Archival retry bound

**Problem.** Exponential backoff without upper bound permits silent indefinite non-archival. `PROJECT_CLOSED` seal integrity is independent of archival success — the Ledger is read-only regardless — but operators need to know archival has failed persistently.

**Resolution.** Add a bounded-backoff contract to IC-LDG-RETAIN:

#### IC-LDG-RETAIN (extension) — Archival Retry Bound

**What it must guarantee:** Persistent archival failure is surfaced to operators within a bounded wall-clock window; it never silently persists.

**Hard constraints:**
- Exponential backoff is capped at a **maximum retry interval** (default: 24h).
- After **K cumulative failed attempts** OR **T wall-clock elapsed** since seal (defaults: K=10, T=7 days), the Ledger emits `ARCHIVAL_FAILURE_PERSISTENT` (OPERATIONAL observation entry, async path) and raises an out-of-band operator alert via the harness notification channel.
- The Ledger remains read-only regardless of archival state. `ARCHIVAL_FAILURE_PERSISTENT` does not reopen the seal.
- K and T are Tier 3 (Git-committed config), tunable via the threshold update ceremony (see GAP-14 resolution).

**Tradeoff decided:** Archival is best-effort post-seal; durability of the sealed chain is guaranteed locally by the seal itself, not by successful cold-storage transfer. Operators are expected to resolve archival backends; the system does not block on them.

**Open questions (deferred):** None.

**Verdict on GAP-12:** **FULLY RESOLVED** with two minor additions (writer-path clarification; archival retry bound). Both are codifications of intent already implicit in v1.1 rather than new policy.

---

## Part 2 — GAP-14 Threshold Rationale Framework

The four provisional thresholds are not arbitrary numbers; they are **proxies for four distinct guarantees**. Each must be tunable in isolation because each controls a different failure mode. The rationale framework below replaces "starting heuristic" language with explicit guarantee contracts.

### T5/T11-A — WAL Flush Cadence (async path)

**Guarantee this threshold serves:** *Bounds the maximum async-entry data-loss window under crash.* Async entries are by definition observations — health records, advisories, access records — where some loss is acceptable in exchange for write-path throughput. The flush cadence declares *how much* loss is acceptable.

**Failure mode — threshold too high (flush too infrequent):**
- Crash-window data loss grows unboundedly. Observations from the preceding N entries or T seconds are lost.
- Loss of Meta-Validator / Meta-TGA health records degrades the evidence base for later audit.
- Loss of `CORPUS_CASE_ADDED` entries creates quiet divergence between sealed corpus state and Ledger record of it.

**Failure mode — threshold too low (flush every entry):**
- Defeats the purpose of async classification — write amplification equals sync cost.
- I/O bottleneck on the observation path starves the sync-write path it was separated from.

**Recommended framing (not a value):** Express as **time-bounded, not count-bounded**: "no more than T seconds of observation entries may be lost on crash." Time bounds are more legible to operators than count bounds and naturally self-adapt to throughput. A count secondary bound (flush if buffered entries exceed M) guards against memory pressure at high throughput.

**Dimensional note:** Because observation entries carry no transactional invariant, the acceptable loss window here is properly **larger** than any sync-path guarantee — these are not competing for the same durability budget.

### T5/T11-B — Light Verification Interval (every 100 entries, verifies last ~10)

**Guarantee this threshold serves:** *Bounds the blast radius of undetected corruption.* Corruption discovered immediately after it happens affects only the corrupted entry and perhaps one or two written atop it. Corruption discovered deep into the future has had all intervening writes built on a poisoned chain.

**Failure mode — threshold too high (say 1,000 entries):**
- Corruption can propagate ~1,000 entries before detection.
- Remediation becomes more expensive: more entries must be reconciled, replayed, or rolled back from a pre-corruption snapshot.
- If detection happens at scale, the chain-break-triggers-write-suspension behavior (§16.4) fires after substantial damage is already recorded.

**Failure mode — threshold too low (say every 10 entries):**
- Verification overhead dominates write throughput for cheap entries.
- Diminishing returns: verifying the last ~10 entries every 10 writes largely re-verifies work already verified.

**Recommended framing:** Express as a **blast-radius cap**: "corruption detected within N writes of occurrence, where N is the entry-distance between consecutive light verifications plus the verification window." At interval=100, window=10, worst-case blast radius is ~100 entries before detection + 10-entry verification tail. The guarantee is symmetric in both directions from the boundary.

**Cost model:** Light verification is O(window), not O(chain). Cost is dominated by interval, not window depth. Reducing interval is linearly expensive; increasing window is nearly free.

### T5/T11-C — Full Verification Interval (10,000 entries OR 24 hours)

**Guarantee this threshold serves:** *Audit-completeness within bounded latency.* Light verification catches recent corruption. Full verification is the only mechanism that detects corruption of *old* entries — e.g., on-disk bit rot, deliberate tampering of historical epochs. Without a wall-clock bound, a low-throughput project could go months between full verifications.

**Failure mode — threshold too high (say 100k entries or 7 days):**
- Deep corruption persists undetected for weeks. The audit-trail guarantee weakens materially for idle or low-throughput harnesses.
- Correlating a detected corruption back to an intrusion event becomes harder the further back it extends.

**Failure mode — threshold too low (say 1k entries or 1 hour):**
- Full chain walk cost is O(entries). Running it frequently competes with live writes or requires serialization barriers.
- On mature projects (millions of entries), frequent full walks are prohibitively expensive.

**Recommended framing:** Express as a **dual-bound audit SLA**: "full chain integrity verified at least once per (count-bound N entries OR wall-clock-bound T, whichever binds first)." The count bound handles high-throughput cases where 24h of writes might be 100k entries; the time bound handles low-throughput cases where 10k entries might take months to accumulate. The 24h fallback is justified because it matches typical operator review cadence (daily) — a full verification failure surfaces in the same operational loop as other daily checks.

**Cost model justification for 24h:** Full verification on a mature chain is the most expensive single Ledger operation. Sub-daily cadence crosses from "audit overhead" into "steady-state cost." Daily cadence aligns full-verification cost with human operator cadence, preserves headroom for write throughput, and is operationally legible (operators expect daily checks; they don't expect sub-hourly ones).

### T5/T11-D — Reconciliation Backlog Thresholds (10/7d warning; 50/30d critical)

**Guarantee these thresholds serve:** *Proxy for operator SLA on out-of-band Git sync.* The Reconciliation Queue accumulates when out-of-band Git commits (direct operator commits, merges, rebases) diverge from harness-mediated state. The thresholds declare what operator response cadence the system expects.

**Warning threshold (10 items OR any > 7 days):**
- **Implicit SLA:** operators should drain the queue at least weekly in normal operations.
- **Too high (say 50 items / 30 days):** operators are unaware of drift until it is already severe; the warning signal collapses into the critical signal.
- **Too low (say 3 items / 1 day):** alert fatigue. Normal bursty operator activity generates warnings; the signal loses meaning.

**Critical threshold (50 items OR any > 30 days):**
- **Implicit SLA:** a month of unresolved reconciliation means reconciliation has effectively been abandoned, not delayed.
- **Too high:** system continues accepting out-of-band work indefinitely while state divergence accumulates; eventual reconciliation becomes prohibitively complex or impossible.
- **Too low:** false write suspensions during legitimate short-term operator absences (conferences, holidays).

**Recommended framing:** Express as **tiered operator-SLA proxies**:
- `NORMAL → WARNING`: "operator reconciliation cadence has fallen below the declared normal window (7d default); operator should reconcile soon."
- `WARNING → CRITICAL`: "operator has failed to reconcile within the tolerance window (30d default); automation intervention (write suspension) is warranted because state divergence now exceeds what manual merge can reliably resolve."

**Independent hard bound:** The D55 `stale_urgent > 1,000` suspension trigger is **not** tunable via this framework — it is a structural invariant on Reconciliation Queue size irrespective of age. That boundary remains fixed; only the temporal thresholds are operator-SLA proxies.

---

## Part 3 — Threshold Update Ceremony (GAP-14 #3)

All four thresholds above must be tunable without spec changes. They are also security-relevant — shortening the archival retry window, lengthening the full-verification interval, or raising the reconciliation-critical threshold all weaken operational guarantees. The ceremony must therefore be **governed but not immutable**.

### D90 — Threshold Tuning Ceremony

**What it must enforce:** Threshold values are Git-committed config (Tier 3), but any change is recorded as a signed Ledger ceremony entry (GOVERNANCE) linking to the Git commit hash that effected the change. Two-layer pattern: value lives in Git (versioned, reversible); change event lives in Ledger (signed, auditable, immutable).

**Hard constraints:**
- Threshold changes MUST be accompanied by `THRESHOLD_TUNING_APPLIED` Ledger entry (GOVERNANCE classification, W1 signed ceremony writer, sync path).
- The `THRESHOLD_TUNING_APPLIED` entry MUST reference: (a) the prior value, (b) the new value, (c) the Git commit hash of the config change, (d) the operator key signing the ceremony, (e) a free-text rationale field.
- Thresholds subject to this ceremony: WAL flush cadence, light verification interval, full verification interval + 24h fallback, reconciliation backlog warning/critical bounds, archival retry bounds (K attempts, T wall-clock).
- Thresholds NOT subject to this ceremony (hard invariants): D55 `stale_urgent > 1,000`, `INTEGRITY_VIOLATION` unconditional retention, Tier 1 classification rules.
- Ceremony is **bi-directional**: tightening and loosening both require the ceremony. There is no immutable-downward asymmetry here (unlike retention, C-SL2), because operational experience may legitimately justify either direction.

**Authority:** Same operator-key tier as `RETENTION_OVERRIDE_EXTENDED`. Warden may, in its own skill domain, impose additional quorum requirements (e.g., two-key signing for loosening verification cadences). That is a Warden concern, not a Consistency concern — flagged as cross-domain below.

**Storage tier rationale:**
- **Not Tier 1 (immutable):** thresholds must be tunable; Tier 1 would freeze operational behavior permanently.
- **Not pure Tier 3 (Git-only):** Git config is operator-owned and silently mutable; without a Ledger record, a future audit cannot reconstruct *when* a threshold changed or *why* a detection window widened.
- **Tier 3 + signed Ledger event:** value is in Git (reversible, diffable, normal config workflow); the *event of changing it* is in the signed Ledger (immutable, auditable, linked to Git hash).

**Interface contract (IC-LDG-TUNE):** The config-reader component of the Ledger layer loads threshold values from Git at bootstrap and on each `THRESHOLD_TUNING_APPLIED` entry append. If a Git config change is detected *without* a corresponding Ledger entry within a grace window (default 1 minute), this is itself a consistency violation: emits `THRESHOLD_TUNING_UNRECORDED` (OPERATIONAL observation entry) and alerts operators. Silent config drift is forbidden.

**Open questions (deferred):**
- Does the Warden skill want quorum requirements on tuning ceremonies that widen detection windows? (Cross-domain — Warden to own.)
- Should `THRESHOLD_TUNING_APPLIED` be classified as GOVERNANCE or as a new OPERATIONAL-GOVERNED sub-class? (Deferred to spec writer; GOVERNANCE is the conservative default.)

---

## Gap Session Summary Block

**GAPS RESOLVED:**
- **GAP-12** — D89 / IC-LDG-RETAIN closure verified complete on core retention axes. Two additions codify latent intent: (i) writer-path clarification that W1 handles both GOVERNANCE and LIFECYCLE-terminal signed ceremonies (W2 is strictly bootstrap mint), (ii) archival retry bound — K attempts / T wall-clock before `ARCHIVAL_FAILURE_PERSISTENT` and operator alert, with K and T as Tier 3 config. Ledger seal integrity is independent of archival success.
- **GAP-14** — Rationale framework produced for all four provisional thresholds (WAL flush cadence, light verification interval, full verification interval, reconciliation backlog thresholds). Each threshold is reframed from "starting heuristic" to an explicit guarantee contract stating what is bounded (data loss window, corruption blast radius, audit-completeness latency, operator reconciliation SLA) and what fails in each direction of mistuning. Framework permits tuning without spec changes; spec now names what each threshold *is a proxy for*, not what its value should be.
- **GAP-14 (threshold update ceremony)** — D90 / IC-LDG-TUNE defined. Two-layer pattern: values in Git (Tier 3), change events in signed Ledger entries (`THRESHOLD_TUNING_APPLIED`, GOVERNANCE). Bi-directional (tightening and loosening both require ceremony). D55 `stale_urgent > 1,000` and `INTEGRITY_VIOLATION` unconditional retention explicitly excluded from tuning. Silent Git-only config drift is itself a consistency violation (`THRESHOLD_TUNING_UNRECORDED`).

**GAPS PARTIALLY RESOLVED:** None.

**GAPS DEFERRED:** None from the scheduled set. Two sub-questions deferred to other skills (see New Tensions).

**NEW GAPS SURFACED:**
- **NG-SL-01** — Writer-path clarification text (W1 handles signed ceremonies across classifications; W2 is bootstrap-mint only) needs incorporation into §16.3 as a readability fix. Mechanical, not architectural.
- **NG-SL-02** — `THRESHOLD_TUNING_UNRECORDED` detection requires a config-reader component that compares Git state against Ledger state at defined intervals. The detection cadence itself is a threshold — does it get bootstrapped with a default or require D90 ceremony to set? Self-referential loop; propose bootstrap default is hard-coded and itself excluded from D90 tuning.
- **NG-SL-03** — Classification of `THRESHOLD_TUNING_APPLIED` as GOVERNANCE vs. a new OPERATIONAL-GOVERNED sub-class. Not urgent; conservative default (GOVERNANCE) works; revisit if classification surface area grows.

**NEW TENSIONS SURFACED:**
- **T-SL/Warden-01** — Warden may want quorum (multi-key) requirements on threshold changes that *widen* detection windows (light/full verification intervals, reconciliation critical bound). Consistency Theorist recommends bi-directional single-key ceremony as the floor; Warden owns any uplift. Surface at next cross-domain sync or council session.
- **T-SL/OC-01** — Threshold update ceremony requires orchestration-layer integration: the orchestrator must surface the signed ceremony UX, verify key signatures, and route the Git commit + Ledger entry as a coupled transaction. Orchestration Comparativist evaluation matrix should include "signed-ceremony ergonomics" as a dimension. Flag raised for orchestration-comparativist attention.
- **T-SL/Warden-02** (latent) — Archival retry bounds (K, T) are themselves Tier 3 config and therefore tunable via D90. This means the archival-failure alerting SLA is operator-mutable. Warden may want these bounds pinned (non-tunable or Warden-signed only) on the grounds that loosening them delays operator awareness of persistent archival failure. Flag for Warden.

---

**Carry-forward to next session:**
- D90 / IC-LDG-TUNE and the archival retry bound extension to IC-LDG-RETAIN should be rolled into the next integrated spec revision.
- T-SL/Warden-01, T-SL/OC-01, T-SL/Warden-02 enter the tension map for the next council / cross-domain pass.
- NG-SL-02 (self-referential config-reader cadence) is a minor open question; default hard-coding is the proposed path forward unless flagged by Warden or Orchestration Comparativist.
