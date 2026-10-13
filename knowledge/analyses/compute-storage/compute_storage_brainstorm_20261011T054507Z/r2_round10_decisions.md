# MAESTRO decisions for R2 round 10 (MAESTRO55, 2026-10-11 ~19:35Z)

Trigger: Astra round 9 says NO-GO (`astra_r2l_verdict.md`, V9; committed b324fd08). Its one high finding is F1 (:5–16); F2–F4 are notes that close V8's R2 and R3 and confirm the refusal and commissioning boundaries. Its one required change is R1 (:46). Alias for this file: D13f. The ruling is numbered D13 so it cannot be confused with the aliases D8 (`r2_round8_decisions.md`) and D9 (`r2_round9_decisions.md`, rulings D10–D12).

This file is an addendum. It does not edit C (`shared_disk_clearance_contract_v1_1.md`), DR, D8, D9 or any reviewed subject. Where it contradicts D9, this file governs. D13 applies C:115 and D10 as they already stand; it changes neither C nor A1. So no operator ruling is needed. Astra judges D13 in round 10 as a freeze change.

## D13 (answers R1 / V9 F1): a process's role follows its origin, not its recipe; the admission audit is a recorded transitive trace

**What MAESTRO checked in the unchanged source.** The gate's admission entry runs `check_fingerprint`, `check_gpu` and `check_dispatch_guards` (`tools/c10w_p2_gate.py:155`). Its process starts:
- direct, already covered by D10: `subprocess.run` at :63 for the helpers at :69, :75 and :79;
- through imported functions, missed by P4 and K6 (V9 F1):
  - `_check_dispatch_guards` (:87) calls `T.require_training_preflight` (:105). That spawns `.venv/bin/python -B experiments/track_c/c10w_oracle_read.py verify-preflight` (`experiments/track_c/c10w_oracle_train.py:65–66`).
  - For `p2-eval` it calls `R.phase_trains` (:128). That reaches `require_untracked_adapter` (`experiments/track_c/c10w_oracle_read.py:520`, :139–140), which spawns `/usr/bin/git ls-files --error-unmatch` (:133).
- the re-attempt path (:136–147): imports `tools/c10w_p2_rerun.py`, which has no process-start site under the grep below, and calls `_check_dispatch_guards` under `A.overlay()`.

The `verify-preflight` child is itself inside the admission subtree, so its own process starts must be traced too.

**Rule.**
1. **Origin decides the role.** Every process reachable from an admission root is an `ADMISSION_HELPER` occurrence: C:115 pre-release registration required, A1 authority forbidden. That covers processes spawned directly, through imported functions, and as descendants of an admission child. This holds even when the same recipe (executable plus argv template) is legitimately a `SCIENCE_CHILD` elsewhere. Science-origin occurrences keep their A1 labels: for example, the science payload's own `require_training_preflight` call at `experiments/track_c/c10w_oracle_eval.py:361`, and the Git probe reached at `experiments/track_c/c10w_oracle_read.py:550` and :608 inside science children. A recipe shared by both origins gets two occurrence records, one per origin. Never one record serving both.
2. **The admission audit is a recorded trace, not a name list.** For each admission source, the freeze records:
   - the exact grep commands for process-start sites (`subprocess\.`, `os\.(exec|spawn|system|popen)`, `Popen`) over the pinned sources;
   - the exact grep commands for call edges from each admission entry function into the modules it imports;
   - each command's hit list, with the cited lines of every process start that is reached.
   It applies the same steps to every Python child an admission spawns. K7 derives the set of admission-origin occurrences from this record. It reruns each recorded grep over the pinned sources and fails when a hit set differs. It also fails when any admission-origin occurrence carries A1 authority, `SCIENCE_CHILD` or `DECLARED_AT_ROOT_ADMISSION`. A fixed list of admission names (K6:2122–2127, used at :2141–2145) is exactly the defect V9 F1 found. Extending that list by hand does not satisfy this rule.
3. **Lexical limits stay stated.** V9 F2 applies here as well. The freeze and the report say that the recomputation proves the trace record is reproducible and complete for its recorded queries. They must not claim it is a complete call graph.
4. **Composition refusal is unchanged (D10).** Profile 38, and every composition whose admission spawns any helper, stays refused with `NOT_ADMITTED_ADMISSION_HELPER_UNREGISTERED:`. The new occurrences add to the reasons, never subtract.

**Mutation controls (new; each RED for its own reason):**
- (a) The admission-origin `verify-preflight` occurrence is relabelled `SCIENCE_CHILD` with A1 authority.
- (b) The same for the admission-origin `git ls-files` occurrence.
- (c) The recorded trace has the `c10w_oracle_train.py:65` process-start hit removed, so the recomputed hit set differs.
- (d) The admission-origin and science-origin occurrences of one shared recipe are merged into one record.

## Carried unchanged

D10–D12 (D9), D8's A1, D4, D5 and D6, and DR except where D8 replaced it. V9's closures stand: V8 R2 (retained routes and concrete bypasses), V8 R3 (delegation references), and the earlier R4/R5/R6 closures. The builder keeps them closed. All 46 existing mutation controls stay RED. D10's consequence for the operator is unchanged. Commissioning stays a separate operator authorization, and all 18 parent cases plus 10 subcases stay UNRUN. Gate 1 stays open until Astra round 10.
