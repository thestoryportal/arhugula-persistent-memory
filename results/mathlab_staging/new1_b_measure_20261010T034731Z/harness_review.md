# Standalone NEW1 B L4 measurement harness review

**PROCEED — no blocking harness defect found for the authorized one-layer measurement.** Next: let the existing single invocation finish, then validate its complete receipt stream and child exit before interpreting results. Do not launch another decomposition or treat this as NEW1 study acceptance.

Reviewer: Codex, GPT-6 / GPT family secondary reviewer under Claude-led MAESTRO2, not Astra. Applied `tools/advisor_review_prompt.md`; the earlier complete Astra options ruling remains the governing Option-B input. Reviewed `profile_l4.py`, `verify_profile.py`, `smoke.json` and `watchdog_smoke.log`; no computations, tests, code edits or process intervention were performed.

**Mathematics and operation identity**

- `profile_l4.py:58–87` correctly evaluates symmetry, SVD reconstruction and PSD reconstruction normalized by the covariance Frobenius norm. The blocked inner sums reconstruct the complete products; both orthogonality checks subtract the correct diagonal entries and normalize by sqrt(d). The Vh-row check computes Vh Vh.T, the appropriate V-side orthogonality check for this square SVD. The fifth metric is explicitly separated from the four frozen gates (`:147–148`, `:178–179`).
- The source has exactly one native-fp32 SVD (`:156`) and one float64 SVD (`:165`), with no retries or alternate decompositions. Input/geometry/prereg pins are checked at `:135–152`; `G.load_covariance` retains the native-fp32 normalization (`tools/new1_geometry.py:134–143`), and C64 is the unchanged C32 promoted at `profile_l4.py:161`. Input identity/content and prereg are rechecked at `:181–184`.
- Native counts use the existing fp32 `< .005` comparison; double counts use the float64 comparison (`:102–113`, `:168–171`). Indexed crossings are disagreements at sorted singular-value indices, not tracked eigenvector identities. Count agreement does not certify projector/subspace agreement. Cross-projector certification is correctly UNVERIFIED (`:145–146`).

**Resources, timeout and receipts**

- Eight intra-op CPU threads and one inter-op thread are set and recorded (`:92–99`, `:138–140`). Native U32 is intentionally retained through the double/check phases (`:145`, `:160–180`), so the reported high-water includes that memory. `high_water()` records Darwin raw bytes and labels cumulative process high-water rather than sampled RSS (`:34–39`). Parent and child observations remain distinguishable by pid and the explicit child high-water field (`:207–211`).
- The watchdog starts termination at 900 seconds, then permits up to two seconds before SIGKILL (`:199–206`). Describe that grace explicitly; it is not a strict 900-second completion bound. The small native-sleep control passed in approximately 0.503 seconds and exited by SIGTERM (`verify_profile.py:21–37`, `watchdog_smoke.log`). It does not empirically cover SIGKILL escalation or surviving descendants after a process-group leader exits. The profile itself does not deliberately spawn worker descendants.
- Each receipt is flushed/fsynced before printing (`:42–50`); parent writes occur before launch or after worker exit. Accept completion only after clean parsing, the expected complete phase sequence, no failure/timeout, a measurement_complete record, and child return code zero. A readable terminal line alone is not proof its fsync succeeded. The successful-receipt smoke demonstrates parseable flushed output; fsync-failure injection and power-loss pathname durability are not established by that smoke.

**Scheduling and interpretation limits**

The original `new1_b_measure_20261010T033955Z` invocation was reported to fail at os.nice before numerical work. This fresh harness explicitly records `nice_applied=False` and the sandbox scheduling limitation (`profile_l4.py:140`), without retrying the denied syscall. Its timings do not validate the real-study nice-10 launch conditions. CPU admission remains explicitly UNVERIFIED (`:195`).

`smoke.json` supplies a small rotated PSD positive control and an indefinite matrix that reconstructs exactly but fails PSD, with no SVD calls or real inputs. It validates formula plumbing, not full-shape numerical success. End-to-end elapsed and the sum of timed SVD/check phases have different scopes (`:44`, `:185–189`). L4 timing multiplied by five remains a planning estimate; complete-study reserves, RSS/deadline feasibility, cross-projector certification, calibration and prospective queue utility remain UNVERIFIED. This review reads no evolving measurement results and authorizes no real NEW1 study launch.
