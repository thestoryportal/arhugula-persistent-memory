# Astra NEW-1 launch readiness: ONE full five-layer Amendment-B attempt

You are GPT-6-Astra, the cross-family reviewer for the LLM-as-Database program. This review is read-only. Repo: this worktree, branch `worktree-c10k-route-a`. Do not run the supervisor, the worker, or any `.venv` python (a GPU admission gate refuses launches while one runs).

Decide one thing: is the combined final implementation ready for exactly ONE real D-NEW1-b attempt with the parameters below? Your r8 required this review (`results/mathlab_staging/new1_construction_diag_astra_r8.md:57`, condition 4 at `:72`). Fresh operator authorization follows your verdict. Nothing launches before then.

Line numbers below were re-read while drafting this packet (2026-10-10). Verify them yourself and do not defer to this packet.

## 1. Subject

- HEAD `d1c995b`. Since `a310686` it changes only `memory_mirror/context-management-every-session.md` (`git diff --stat a310686 HEAD -- tools/ tests/ docs/NEW1_ADAPTER_GEOMETRY_PREREG.md memit_dry_run` is empty).
- Fix 1, `57420ab`: `native_projector` gathers twice (`tools/new1_geometry.py:200-202`). Astra r9 = `VERDICT: GO` (`results/mathlab_staging/new1_projector_fix_astra_r9.md:49`).
- Fix 2, `a310686`: supervisor reap fix. `REAP_TIMEOUT_S` is at `tools/new1_supervisor.py:41-42`, `kill_worker` at `:268-273`, `terminate` at `:276-279`, and `worker_lifetime` at `:314-339`, entered at `:353`. Astra r10 is pending (§4).
- Source SHA-256 now (`shasum -a 256`, this session), with the values at the consumed 05:39Z attempt taken from `results/mathlab_staging/new1_b_go_astra_packet.md:16`:

| File | Now | At the 05:39Z attempt | Last commit |
|---|---|---|---|
| `tools/new1_supervisor.py` (launch entry, `main` `:465-484`) | `da9f250e244b8e29392e13dbba83ceb90e6980fdfee2b43fa66a3feed3c86a9c` | `a69d4107…` | a310686 |
| `tools/new1_geometry.py` (worker entry, `main` `:565-581`; launched at supervisor `:473`) | `ce43a26d24fb9cd0e2a2ff4d4ddd63bdd7de9ff4d2349b017f77914a31271f77` | `018ce4d9…` | 57420ab |
| `tests/test_new1_geometry.py` | `dba1606f9938498d1469fcfc69cbf3f7d320c2aa3ed3834e7cd2a12a47931e3d` | `57afd250…` | 57420ab |
| `tests/test_new1_supervisor.py` | `c3440f6bc8afc5c476257865121249d0f98299a05a4b52a3835d7637074eccd5` | `33c61282…` | a310686 |
| `tools/mathlab_events.py` | `53b2ea18ea8a363136e967c25bb0e8a94f88a63070f3921a3b996e2287459f5f` | unchanged since 22dd8c5 | 22dd8c5 |
| `tools/mathlab_admit.py` | `bd3b6312ce3edcb599591c3559e85adfb13bb45c13e26942ee2eec9aacfe2abc` | unchanged since 6ea8e7c | 6ea8e7c |
| `tools/mathlab_runtime.py` | `416b597c1309f7dcabb065749e05da9ce28743b1d16c9791ae1eed527a4a72c5` | unchanged since c9cb108 | c9cb108 |
| `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md` (pin) | `1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f` | same (`new1_b_run_authorization.md:9`) | — |

- Engine fingerprint (`LLMDB_ROOT=$PWD python3 tools/engine_fingerprint.py`, this session): `engine fingerprint PASS` (memit_main `d941a9fb…`, `_cov_cpu 3`).
- Disk (`df -g /Volumes/memit`, this session): 80 GiB available of 419.
- Projected writes: NOT FOUND in any doc (searched `grep -n -i "disk\|output volume\|projected write\|npz"` over `results/mathlab_staging/new1_v2_build_report.md` and `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md`). Estimate from code only: `save_controls` (`tools/new1_geometry.py:402-411`) writes 100 npz files (5 layers × 20 draws, `:464-466`). Each is (2048+11008)×16×8 = 1,671,168 B of factors, about 0.156 GiB in total, plus layer JSONs and receipts. The halted 05:39Z namespace is 1.1 MB (`du -sh`).

### What happened before

| Run (`results/mathlab_staging/runs/`) | Outcome | Memory evidence |
|---|---|---|
| `new1_20261010T014248.014387Z` | LAB-STOP before compute (`events.jsonl:3`) | none |
| `new1_20261010T022922.650234Z` (pre-Amendment B) | INVALID-WORKER: covariance validity svd 1.30e-4 (`worker_failure.json`; `SESSION_CHECKPOINT.md:33`) | peak sampled RSS 3.8367 GiB (`events.jsonl:66`) |
| `new1_20261010T025311.015991Z` | INVALID-ADMISSION: "GPU blocking processes are unaccounted" (`events.jsonl:3-5`) | none |
| `new1_20261010T030200.809009Z` (pre-Amendment B) | INVALID-WORKER: same validity failure (`worker_failure.json`) | peak 3.8374 GiB (`events.jsonl:64`) |
| `new1_20261010T053945.884468Z`, the consumed Amendment-B attempt | INVALID-WORKER at L4 `validate_capture`: "projector identity/probes mismatch" (`worker_failure.json:5`; `architecture_profile/s_new1_b_halt_diagnostic.json:11-18`) | peak 8.5376 GiB at `events.jsonl:251` (L4 checks window); min available 23.71 GiB at `:224`; last sample 5.7184 GiB at `:266`; no cap breached (`s_new1_b_halt_diagnostic.json:16-17`) |

The 05:39Z attempt measured only L4's covariance stages. Event timestamps give native SVD 77.2 s (`:16`→`:93`), float64 SVD 159.3 s (`:93`→`:249`) and checks 14.5 s (`:249`→`:265`), halting at about 255 s. It never reached L4's update SVD, projections or controls, nor any of L5–L8. The r8 diagnostic established the construction discrepancy but not the historical halt cause (`new1_construction_diag_astra_r8.md:26`).

## 2. Launch parameters

| Parameter | Value | Prereg (`docs/NEW1_ADAPTER_GEOMETRY_PREREG.md`) | Enforced in code | Match |
|---|---|---|---|---|
| Total run budget | 2,700 s monotonic, from before admission/hashing/imports | `:218` | `tools/new1_supervisor.py:24`; clock starts at `Controller` `:203`, built at `:307` before admission `:358`; checked `:206-208`, alarm `:353` | yes |
| Worker-family RSS cap | 11 GiB observed | `:218` | `:27`; breach `rss_gib > 11` at `:227`; family = worker process group plus descendants, `:154-161` | yes |
| Threads | 8 | `:109`, `:222` | env `OMP/MKL_NUM_THREADS=8` `:368`; `torch.set_num_threads(8)` `tools/new1_geometry.py:507` | yes |
| Niceness | nice 10, one worker | `:109`, `:222` | `['nice','-n','10',…]` `:473`. Relative to the supervisor's own niceness; neither checked nor recorded (receipts in the 05:39Z namespace are admission, cell, criteria, halt, resource only) | value yes; final niceness unverified |
| Native SVD floor | 13 GiB available | `:220` (also `:121`) | `RESERVES['covariance-svd']=5` `:29` + 8 at `:243`; called `tools/new1_geometry.py:156` | yes |
| Float64 SVD / checks floor | 19 GiB available | `:220` | `RESERVES` `covariance-svd-f64`/`covariance-checks` = 11 `:29` + 8 at `:243`; called `new1_geometry.py:162`, `:164`, `:539` | yes |
| Cell wait | 300 s max, inside the total budget | `:222` | `WAIT_S=300` `:25`; `cell_deadline` `:244`; expiry → STOPPED-RESOURCE `:211`; `min` with run budget `:212` | yes |
| Abort floor | 6 GiB available | `:222` | `FLOOR_GIB=6` `:28`; breach `avail < 6` `:227` | yes |
| Admission floor | 8 GiB additive | `:220`, `:222` | `required = 8 + reserve` `:243` | yes |
| Fresh namespace | new run dir | `:188`, `:224` | timestamped dir, `mkdir(exist_ok=False)` `:471-472`; refuse if `events.jsonl` exists `:306` | yes |
| No retry | one attempt | prior authorization `results/mathlab_staging/new1_b_run_authorization.md:5`; prereg `:222` ("all durability/retry protections") | `main` makes one `supervise` call (`:479`) with no loop. `enforce_new1_retry_policy` (`:168-190`) only refuses after ≥3 prior STOPPED-RESOURCE/DEADLINE runs (rule `docs/MATHLAB_PREREG.md:284`). A stdlib replay of `read_events` over all 5 `new1_*` dirs (this session) gave 0 errors, 1 `run_started` each and 0 resource aborts, so it will not refuse | no value mismatch; "one attempt" is procedural, not code-enforced |

No parameter value in code differs from the list.

## 3. Carried items

r8 conditions (`new1_construction_diag_astra_r8.md:67-73`):

1. Preserve the diagnostic and historical HALTs; no cause or PASS claim. **Status:** all 5 run namespaces are present (table above); halt diagnostic `architecture_profile/s_new1_b_halt_diagnostic.json`; `docs/program_state.json:11` keeps INVALID-WORKER / NOT COMPUTED.
2. Failing-first evidence for the numerical fix. **Status:** closed by r9 item 3 (`new1_projector_fix_astra_r9.md:21-32`); receipts in `results/mathlab_staging/new1_projector_fix_20261010T204522Z/`.
3. Full-worker lifecycle enforcement resolved and reviewed. **Status:** built in `a310686`; review pending in r10 (§4).
4. Readiness review plus fresh operator approval; one capped, fresh-namespace attempt; no automatic retry. **Status:** this packet; operator approval not yet given.
5. Propagate with current fingerprints and a GREEN close-out. **Status:** close-out commit `b63dac0` and `tools/closeout_fingerprints.json:186-188` exist. ALL GREEN was not re-run for this packet.

r9 items carried:

- **Item 4** (`new1_projector_fix_astra_r9.md:34-42`): extra-gather increment ≤0.451416 GiB, not multiplied by five. Complete-worker memory feasibility is **unverified**; 8.508209 → 10.635262 GiB is a planning sensitivity, not an RSS bound.
- **Item 5** (`:44-45`): blocking for launch only. Existing readiness gates remain: the MB27 review, a pinned combined implementation, this readiness review, and fresh operator authorization for one capped, fresh-namespace attempt with no automatic retry.
- Citation note: r9 cites `new1_geometry.py:536` as the 19-GiB gate. In the current file, `:536` is a comment and the gate before the projector is `:539`. The file is unchanged since 57420ab.

## 4. Astra r10 verdict (MAESTRO fills in)

> PLACEHOLDER: MAESTRO pastes the r10 verdict on a310686 here (`results/mathlab_staging/new1_supervisor_reap_astra_r10_packet.md`). If r10 is not GO or GO-WITH-CONDITIONS, treat this readiness review as NO-GO.

## 5. Questions

1. **Parameter enforcement.** Each table row in §2 claims code enforces the prereg value. Check every cited line, including the comparison operators (`>` RSS at `:227`, `<` floor at `:227`, `>=` cell gate at `:248`), that the deadline clock starts before admission (`:307` vs `:358`), and that a cell wait cannot extend the total budget (`:209-212`). Name any row that is wrong.
2. **Niceness.** `:473` applies `nice -n 10` relative to the supervisor. The previously endorsed command does not nice the supervisor (`results/mathlab_staging/new1_b_go_astra.md:21-29`). No receipt records the final niceness. Is a launch-time check of the worker's niceness (= 10) a required condition?
3. **Memory feasibility of the complete worker under 11 GiB and the 13/19/6 GiB floors.** Check this arithmetic:
   - Measured profile 8.056793 GiB (prereg `:216`). Peak observed in the real worker 8.537598 GiB at L4 (`events.jsonl:251`), which is +0.480804 GiB (+6.0%). Headroom to the cap is 2.462402 GiB.
   - 1.25 × 8.537598 = 10.672 GiB, which is ≤ 11.
   - Pessimistically adding r9's worst-case gather (0.451416) to that peak gives 8.989014; ×1.25 = 11.236 GiB, which is > 11. In code, construction happens after check temporaries and C are released (`new1_geometry.py:187`, `:538`) and after the gate at `:539`. The projector-phase sample was 5.718414 GiB (`events.jsonl:266`). Adding the L4 extra gather (11,008 × 8,645 × 4 B = 0.354515 GiB) gives about 6.07 GiB.
   - L4 has the largest allowed count. L5–L8 captured counts are 7119/5738/4165/1583 (`s_new1_b_halt_diagnostic.json:24-29`).
   - Never observed: L5–L8; the update-SVD, projection, random-control and output phases of any layer; mmap residency of the 463,160,213-byte bundle (`new1_geometry.py:527`). Sampling is 1 s and cannot see transient peaks (prereg `:115`).
   - Gates passed at 28.48 (13 required), 27.41 and 24.80/26.13 GiB (19 required) (`events.jsonl:16,93,249,265`).
   Is the 11-GiB cap adequate for one attempt, or is a breach likely enough to block?
4. **Time.** The L4 covariance stages took 251.0 s in the real worker (§1). Five layers project to about 1,255 s, leaving about 1,445 s for unmeasured work. The prior projection was 2,525.9 s vs 2,700 s (`results/mathlab_staging/new1_v2_build_evidence/mb4_20261010_brobust/resource_projection.json:18-19`). Does the second gather add material time? Is the deadline risk acceptable?
5. **Lifecycle and reap under a real halt.** Given r10, check that the reap holds for the three halts this run can actually produce:
   - an INVALID-WORKER exit like the 05:39Z one (`new1_supervisor.py:380-382`, `:417-419`);
   - a STOPPED-RESOURCE raised in `heartbeat` during a blocking SVD (`:344-350`);
   - STOPPED-DEADLINE, where `controller.remaining()` raises inside the halt `hard_deadline` (`:452`), so the halt receipt and `halted` event are skipped and only stderr remains (`:457-458`; noted earlier at `new1_b_go_astra.md:17`).
   Is "no terminal event on deadline" acceptable for this attempt?
6. **Fresh namespace and no retry.** Confirm that `:471-472` and `:306` guarantee a fresh namespace. The code allows a second manual invocation after any non-resource halt: the retry policy counts only resource/deadline aborts, with a threshold of 3 (`:185-190`). Is procedural enforcement enough (operator authorization text plus MAESTRO), or must a condition make the authorization file name exactly one invocation and its expected run-dir pattern?
7. **Does this attempt again serve as complete-workload resource validation (r8 Q4)?** The prior authorization C2 made the consumed attempt that validation (`new1_b_run_authorization.md:6`), but it measured only L4's covariance stages. Prereg `:222` leaves full-workload reserves, RSS, other-layer time and nice-10 completion UNVERIFIED. Should C2 be restated for this attempt? What does a STOPPED-RESOURCE or STOPPED-DEADLINE mean for D-NEW1-b, given that it counts toward the third-abort rule (`docs/MATHLAB_PREREG.md:284`)?
8. **Recording the correction and new source identity (r8 Q4).**
   - The trackers do not yet name the fix commits or new SHAs. `grep -rln "57420ab\|ce43a26d\|a310686\|da9f250e\|two-gather"` over `docs/ CORPUS/ EXPERIMENT_RUNBOOK.md SESSION_CHECKPOINT.md tools/closeout_fingerprints.json` returns nothing. `docs/program_state.json:11` lists only the planned gates.
   - The run records the prereg SHA (`new1_supervisor.py:477`, `new1_geometry.py:555`) and input SHAs (`:556`), but not the SHA-256 of `new1_supervisor.py`/`new1_geometry.py`.
   - What must be recorded, and where, before launch? Options: an append-only prereg note, a runbook §5 Decision-ID, the authorization file, or a pre-launch receipt. Must the launch record pin `da9f250e…` and `ce43a26d…` and the commit? The prereg pin stays `1616c860…`, since r8 Q4 requires no numerical amendment.
9. **Anything else blocking.** Candidates to check:
   - admission refusal from GPU-gate coexistence (precedent `new1_20261010T025311.015991Z/events.jsonl:3`);
   - the unverified ALL GREEN close-out (§3 item 5);
   - the 80 GiB free vs about 0.16 GiB of estimated writes plus the 20 GiB margin;
   - anything in the r10 verdict.
   Also give the exact launch command you endorse, with the prereg SHA.

## 6. Output

Give numbered answers to Q1–Q9. Cite path:line for each, mark each blocking or not blocking, and state each condition as a checkable precondition. A finding like "parameters look right" with no line-by-line check will not be accepted. End with exactly one line:

`VERDICT: GO` / `VERDICT: GO-WITH-CONDITIONS` (list the conditions above it) / `VERDICT: NO-GO`
