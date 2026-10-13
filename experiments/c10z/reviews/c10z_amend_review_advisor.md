PROCEED-WITH-CHANGES (4 BLOCKING: two prereg-text/LAW#5 items in §9(h), two brief-precision items that would otherwise cost a second build round)

Reviewer: independent Opus advisor, read-only. Abbreviations: W = worktree; `prereg` = W/docs/C10Z_ASTRA_PREREG.md (SHA e2d7fa10…, verified; first 105,436 bytes = 38f8b68c…b072, verified; the file equals HEAD, so §9 is already committed); `arms`/`read`/`selftest` = W/experiments/track_c/c10z_astra_{arms,read,selftest}.py; `v3` = W/results/c10z_astra_budget_proposal_v3.md; `spec` = W/results/c10z_astra_benchmark_spec_v2.md; `packet` = /Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_amend_review_packet.md (brief begins at packet:22). `results/c10z_astra/` and `results/c10z_astra_benchmark/` are absent (ls, verified).

## BLOCKING

**B1. §9(h)'s inertness sentence is false against the code: telemetry time can change a label, and memory observations will differ.**
- The logit-lens forward goes "in `arm_hook`, after `probe_hits`, while the weights are still edited" (packet:78). That is between arms:668 and arms:687. `arm_hook` sets `write["wall_seconds"] = time.monotonic() - self.current["start"]` at arms:687, and `restore_hook` overwrites it the same way at arms:695. So the telemetry time ends up inside `wall_seconds`.
- `wall_seconds` feeds the EXCEEDS-TTL qualifier at read:328 (`>3600`) and classify_candidate at read:571/:606, via arms:1241–1242. A qualifier is part of the label.
- Telemetry time also counts against the deadlines and projections (prereg:474 says so). It can therefore turn a near-deadline pass into HALTED-BUDGET.
- §9(h) at prereg:474 nevertheless says "No count, lead, hit, label, hash or reading may differ". The proof sentence (prereg:475) and brief T2 (packet:140) also require "every record identical". That holds only on stubs. On hardware, `self.memory` also changes: `check_memory` (arms:390–394) records psutil RSS and `torch.mps.driver_allocated_memory()`, those values go into the pass record (arms:1246) and checks_p*.json, and they feed the V11 gate (read:482–485). The extra MPS forwards and the CPU chunk buffers change them.
- With edited weights present, no placement exists that keeps telemetry out of `wall_seconds`: restore_hook recomputes it after the restore (arms:693–695).
- **Fix (exact).** Replace prereg:474's last two sentences with: "Its own elapsed time counts against the nominal deadlines and against each write's `wall_seconds`, and is not projected. Each telemetry line records its own `elapsed_s`. With telemetry on, timing fields (`wall_seconds`, `round_seconds`, `timings`, budget-history elapsed) and memory observations (`rss_bytes`, `driver_bytes`) may differ, so a run near a deadline, the 3,600-s TTL (read:328) or the V11 ceiling can end HALTED-BUDGET, gain EXCEEDS-TTL or end HALTED-V11 where the off run would not. Every other count, lead, hit, hash and reading is identical."
- In the brief:
  - add `elapsed_s` to every line (packet:73);
  - T2 (packet:140) compares records after removing exactly those timing and memory fields, with a stub `check_memory` returning constants;
  - bound the cost: write one JSONL line per snapshot event, with target_probs as one line per round holding parallel arrays. One fsync per requirement (about 700 per round × 10 rounds per write) would add minutes of fsync time to `wall_seconds` on this volume.

**B2. The LAW#5 inertness of the extra MPS forwards is asserted, not demonstrated.**
- The only proof in §9(h) (prereg:475) and the brief (T2, packet:140) uses a stub model and an injected clock. It proves the code path writes nothing and calls no clock or hook. It cannot detect whether one extra no-grad Qwen forward on MPS (`output_hidden_states=True`, `logits_to_keep=1`) between edits perturbs any later MPS logits, through allocator, graph-cache or kernel-selection state.
- I-INFER: the risk is low. The model is in eval mode (c10e_bandknob.py:48), and the harness registers no module hooks (grep: no `register_forward` in c10e). But this repo's own LAW#2 and LAW#5 (CLAUDE.md) require inertness to be demonstrated, and REPRODUCIBILITY.md already records that MPS is not bit-exact across processes.
- D-C10r-rulings-11 (runbook:361) allows either "off by default" or "proven inert … identical counts and records with telemetry on vs off". Off by default is met. Proof on real hardware is not.
- **Fix (pick one, then record it in §9(h)):**
  - (a) Zero cost: add "The first ASTRA attempt runs with telemetry off. Telemetry-on attempts require (b) first."
  - (b) Build a CPU-testable `telemetry_mps_inertness_check()` in arms. The program runs it once on MPS (≤ 10 min, GPU idle): pristine model, all A7 `probe_hits` tokens and one `observe(A7 batch)`, computed twice in one process, once plain and once with the logit-lens forwards interleaved exactly as at the call sites. Require `torch.equal` on the gathered logits and identical tokens. Any difference keeps telemetry off for this prereg.

**B3. The brief gives Codex no legal test seam for the launch binding, and silently breaks existing tests. A second round is near-certain.**
- Stage 0 must accept only a record that "resolves under `results/c10z_astra_benchmark/`" (packet:57). But the brief allows writes only to the listed files and /private/tmp (packet:28), and §9 states that directory is absent (prereg:451). The only way to build a valid fixture record is patching. The brief should say that the root and the benchmark script path are both derived from `D.ROOT` at call time, because existing tests already patch `ROOT` (selftest:383, :1210, :1384, :1528). It should also say that tests copy the real benchmark script into the temp tree, so `script_sha256` matches.
- Unreachable gates. With a consistent record, C01 ≥ 7,200 always (floor), and the total is ≤ 55,800 whenever C01 ≤ 10,800 (minimum-term algebra: C01 ≤ 10,800 ⇒ t* ≤ 0.14972 ⇒ C2 ≤ 17,100 ⇒ total ≤ 55,800). So the required boundary tests "56,100 refused" and C01 out of bounds with `stop` false (packet:107–108; M6, M7) can only be reached by patching `ceilings`. Say so. Otherwise Codex cannot build a fixture and will report or guess.
- Existing tests the change breaks and §2F (packet:85) does not list:
  - Budget constructions at selftest:635, :642, :644, :649, :881, :1020 and :1699. The new positional `stage01` shifts the arguments; for example, `D.Budget(100.,60.,6000.)` would make 60 the stage01 → refused.
  - Launch dicts without `"stage01"` at selftest:1069, :1087, :1147 and :1201, plus the `_mock_resident` launches. `resident` would KeyError.
  - Every stage-0 test that reaches `stage_call(0)` (selftest:1310–1369, :1500–1550). These now refuse for lack of `C10Z_BENCHMARK_RECORD`.
- **Fix:** in §2B and §2F add:
  - "the benchmark root is `D.ROOT/'results/c10z_astra_benchmark'` and the script path is `D.ROOT/'experiments/track_c/c10z_astra_benchmark.py'`, both evaluated at call time";
  - "fixture records are produced by the real module's writer and `ceilings()` in a patched-ROOT temp tree";
  - "the C01-bound and total gates are tested by patching `ceilings` to synthetic values";
  - "update the fixtures at selftest:635–650, :881, :1020, :1069, :1087, :1147, :1201, :1310–1369, :1500–1550 and :1699 (stage01 argument, `launch['stage01']`, benchmark env), with no assertion changed except the ceiling numbers; list each in the report".

**B4. The red step is self-contradictory under the signature change, and the brief deviates from v3, which trips its own stop clause.**
- §2B changes the signature to `Budget(start, stage01, stage2, stage3, …)` (packet:56). The v3 §D tests use C01 = 7,200 (v3:133–141).
- Written against the new signature, every idle-fix test fails on today's code with a TypeError, not the behavioural failure. Invariant (vii) cannot pass, yet packet:91 says it must, and v3:131 requires the failures to show the bug.
- §2A says "install `origins[key] = now`" unconditionally (packet:51). v3:121 has `if key not in self.origins: self.origins[key]=now`. packet:44 orders Codex to stop on any brief/v3 disagreement.
- **Fix:**
  - (i) The idle-fix tests build Budgets through a helper `_budget(start,c01,c2,c3,process,clock)`. It tries the new signature; on TypeError it uses the old one and sets `b.durations["stage01"]=c01`. The report must show each red failure as the behavioural assertion, with no TypeError or KeyError allowed.
  - (ii) Make §2A quote v3:113–124 verbatim, including `if key not in self.origins`.

## Answers

**A. Fidelity of §9 to v3 §C/§D/§E/§F and the operator's bounds.**
- Faithful:
  - (b) matches v3:65–71;
  - (c) matches the runbook D-C10z-budget row (runbook:365): ≥ 2 h, ≤ 3 h, total ≤ 15.5 GPU-h, the benchmark path, no fallback (v3:154–159 correctly dropped);
  - (d) matches v3:77–81;
  - (e) matches v3:100–141;
  - the (a) line list is verified: the 5,400 text appears at prereg:18, :125, :127, :133, :196 (×3) and :344.
- The "hard" wording at prereg:127, :196 and :344 is overridden by (a) "none is a hard maximum". That is acceptable under "this section governs" (prereg:451).
- The only frozen checks that change are the declared ones: read:500 (V12 provenance, from `==5400` to a bound) and when HALTED-BUDGET fires (idle fix). §9's closing "no gate … changes" (prereg:477) slightly overstates this. Advisory: append "other than the declared read:500 bound and the (e) deadline scope".
- Not faithful: (h) contradicts the code (B1).

**B. C01 as a launch input.**
- The design is sound. Recomputing `ceilings()` at stage 0 is what makes it safe. A record INTERRUPTED during the optional phases still carries a stale BENCHMARK `derived` (written at spec:108). The recomputation returns REFUSED, so both the source check and the `derived` agreement check catch it.
- Paths by which a wrong record can still launch:
  - (1) Any other usable, internally consistent record under the root, such as a rerun or a hand-edited record with consistent raw values and `derived`. It passes, and its binding to the runbook row is a manual grep (v3:210). Mitigation already present: supplying C2 and C3 from the runbook row pins C01 exactly, because C3 = C01 + C2 + 60. Without both env ceilings, C01 is pinned only to [7,200, 10,800], and only stage 0–1 runs. Advisory A1 closes the gap.
  - (2) Process 2 takes `launch["stage01"]` from p1's run.json (arms:1479, :1488), not the record. Its exposure equals today's for stage2/stage3. Advisory A2.
- The bound check keeps "stage 0–1 ran under an approved ceiling". It loses "the record's ceiling equals its launch input". `==5400` gave both, because the constant was the launch input. A2 restores it.

**C. Telemetry.**
- As specified, it is code-path-inert: read-only, no hooks (it runs after `observe` removes its hooks, arms:510–513), no clock calls, no record writes, and failures disable it rather than halting.
- It is not label-inert (B1) and not demonstrated MPS-inert (B2).
- Ordering: the placement after `round_guard` (packet:79) correctly keeps it out of round times. The next round's `rstart` is taken fresh at arms:716.
- Memory: 36 F0 prompts × 1 forward per write, with `logits_to_keep=1`, is negligible on MPS. CPU chunks of ≤ 64 MiB against a gathered tensor of about 700 × 151,936 × 4 B ≈ 425 MB already held are fine.
- The on/off proof is sufficient only for the code path.

**D. Brief.**
- It forces test-first (packet:89–92), boundaries at, inside and outside each threshold (packet:105–114), round-trips (packet:116–121), one HALT test per gate (packet:123–136) and 16 mutants (packet:151–172).
- The write scope is tight (packet:26–32).
- Ambiguities that would cost a round: B3, B4, A3 and A5.

**E. Blockers:** B1–B4. All are text or brief edits; no code exists yet.

## Advisories
- **A1.** Add `"benchmark_sha256"` to the go record, and make stage 0 require it to equal the SHA of the bytes read from `C10Z_BENCHMARK_RECORD`. `go_record` already permits extra keys (arms:1351–1360). This makes the operator-approved record a mechanical binding. Hash and parse the same bytes (no second read).
- **A2.** In read.py `read_directory` (read:662–687), require `record["budget"]["ceilings"][k] == run["launch"][k]` for stage01, stage2 and stage3. In `read_run` (read:644–659), require p1 and p2 ceilings to be equal. This restores what `==5400` guarded (read:500).
- **A3.** Give the halt-code mapping explicitly. packet:64 says "HALTED-BUDGET (or HALTED-V12 for malformed input)". Proposal:
  - HALTED-V12: env missing, relative, outside the root, absent, not JSON or non-finite; script-SHA mismatch; `derived` mismatch.
  - HALTED-BUDGET: REFUSED; `stop`; total; bounds; env C2/C3 mismatch (prereg:457).
- **A4.** The launch line at v3:245 lacks `C10Z_BENCHMARK_RECORD=<abs>` and (optionally) `C10Z_TELEMETRY=1`. A launch from it fails safe (refusal), but it should be corrected before go. The stage-3 line (v3:247) should carry the same `C10Z_TELEMETRY` choice.
- **A5.** Telemetry precision:
  - catch `Exception`, not `BaseException` (packet:81), so SIGINT and SystemExit still halt;
  - target_probs come from each round's `post` (arms:725) and the final `post` (arms:743); say which;
  - T7's "no full-size temporary" (packet:145) cannot be tested with tracemalloc, which does not see torch allocations; use a spy on the chunk slices (rows ≤ chunk);
  - factor the logit lens into one method called at arms:813+ and arms:668+, with an AST call-site test; real `Session.stage0` cannot be driven under the existing stubs (arms:323);
  - `hidden_states[l+1]` is the output of layer l for l ≤ 34 (transformers 4.51.0 installed; layers 4–8 are safe from the final-norm entry).
- **A6.** The benchmark module's top level should import only the stdlib. If it imports `c10z_astra_arms`, then a by-path import from arms running as `__main__` loads a second copy of arms.
- **A7.** The cheapest overturning test for the whole amendment is B2(b): about 10 GPU-minutes. Run it before the first telemetry-on launch.
