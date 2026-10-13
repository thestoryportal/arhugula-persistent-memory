FIX-FIRST
Reviewer: GPT-6-Astra (high)

References below: **X** = [C10X draft](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10x_telemetry_amendment_draft.md); **Y** = [C10Y draft](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10y_telemetry_amendment_draft.md).

**BLOCKING**

1. **Off-mode contradictions — X:164,179; Y:186,201.** Unconditional inertness-record verification would obstruct the mandated telemetry-off first attempt. Replace with: **“Only telemetry-on launches require or verify an inertness record; telemetry-off launches require neither that record nor telemetry calibration.”** Also qualify X:24/Y:26’s “only record difference” as applying **under T7’s controlled proof**; live exceptions are those enumerated in T10.

2. **Impossible scorer transcription — X:71–73; Y:88–90.** The original scorer has no `full` or `first` variables; it returns expressions directly (`experiments/track_c/c10e_bandknob.py:117`). Exact fix: insert only `sink(prompt, target_ids, gen)` before the unchanged return; compute both predicates inside the sink’s protected body. Adjust the AST requirement accordingly.

3. **Insufficient inertness predicate — X:149–165; Y:171–187.** Equal correctness booleans permit different incorrect generated answers. C10Z requires identical tokens (`docs/C10Z_ASTRA_PREREG.md:575`). Require **exact generated-ID sequences plus flags**, alongside the specified bitwise science tensors, using a validated reference capture. Require successful lens execution and complete expected telemetry output; a disabled writer or missing output makes the check **INVALID**, never INERT. Preserve the honest pristine-only scope; edited outputs, Y optimisation and resource inertness remain UNVERIFIED.

4. **Dashboard fallback is unsupported — X:178; Y:200.** The dashboard requires `recipes[…].arms.A7_coined_coined.extra.generated` (`tools/dashboard_experiment.py:192–201`). The unchanged harness stores correctness flags, not generated text (`c10e_bandknob.py:366–374,496–498`). Replace the promise with: **“Telemetry-off first attempts do not provide generated-answer display through this design; live answers await admitted telemetry and its dashboard adapter.”** Field names match, but JSONL is not presently a supported input. Null `subj`/`template` must not reach rendering (`dashboard_experiment.py:213–215`); treat unresolved attribution as telemetry failure.

5. **Rerun policy contradicts replication binding — X:179,199,210; Y:201,220,231.** A telemetry-off replacement for process 2/stage 3 cannot replicate its telemetry-on predecessor under T9. Add: **“A replacement with changed telemetry setting cannot join the prior replication pair. Regenerate the required pair with telemetry off, retaining all original artifacts, eligibility gates and spending requirements.”** T12 must identify the replacement’s valid predecessor explicitly.

6. **Y forecast weakens the frozen budget gate — Y:204–209.** Maximum answer-line latency is not a defensible bound for optimisation snapshots, larger probability payloads, CPU transfers/reductions and their writes. Replace with **separately justified per-kind bounds covering preparation through fsync**, with workload counts and scaling assumptions. Unbounded components refuse telemetry-on dispatch, as frozen `docs/C10Y_DIRECTDW_PREREG.md:92` requires. Off dispatch needs no telemetry phase.

7. **Y lens ordering contradicts its own guarantee — Y:49–55.** Recipe A’s post-write hook executes before V4, despite “no instrument forward precedes the baseline gate.” Suppress that lens call; retain pristine lens after V4 and candidate post-write lens. Stage-1 volume then becomes **two calls / 48 forwards**, and forecasts must follow.

8. **Test isolation needs a child-process boundary — X:121; Y:141.** A parent Python audit hook alone does not protect against an executed child writing into the live tree—the cited leak involved stage dispatch. Add: **“Deny real experiment subprocess dispatch; allow only explicitly isolated stub workers. Install protection before imports, resolve protected paths, and positively test the subprocess boundary without launching a real stage.”**

**ADVISORY**

- Both preregs and drafts read fully; supplied frozen hashes match. No explicit hypothesis, arm, scientific threshold or verdict-formula replacement found. The budget-bound defect above must not become an implicit relaxation.
- Float64 telemetry reductions and explicitly labelled legacy fp32 echoes are appropriate. Keep scientific gate arithmetic separate.
- X:207/Y:228 should specify the disposition of **unmarked missing lines, malformed lines and unexpected keys**; T11 must not silently pass an incomplete audit.
- Keep first attempts OFF and require explicit **operator cost authorization** for T8. This review authorizes no GPU work.
- Read-only review; no GPU execution. Requested reviewer header reproduced; exact runtime model/effort authentication is UNVERIFIABLE here.

**Q5 ruling:** The proposed float64 default is **not authorized by the frozen text**. **-LARGE-WRITE** is tied to the harness’s pre-cast fp32 `delta_norms` (`docs/C10X_ENGINEPATH_PREREG.md:43,89,149`; `c10e_bandknob.py:212–217`). The three parity checks compare **full ΔW tensors**, not scalar norms, and §2.4 explicitly prescribes detached CPU fp32 relative-L2 arithmetic (`:66,74,76–77`). Those three checks are less explicit about pre-cast versus applied ΔW than X2-(vi) (`:80`); that ambiguity does not authorize changing reduction precision. A float64 gate replacement requires its **own dated metric amendment**, explicitly fixing tensor representation and arithmetic. A labelled **report-only float64 cross-check is safe**, provided it cannot affect floors, acceptance, qualifiers, eligibility or verdicts.

