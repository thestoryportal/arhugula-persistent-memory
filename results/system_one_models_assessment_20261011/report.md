# System One models in our stack — S1M assessment

Read date: 2026-10-11. Status: public-source assessment recorded; stopped at MAESTRO's context gate. No models, weights, installations, commits or tmux operations. Only this report and `sources.md` were written. Tests below are proposals, not results.

## Identification first

The operator's correction identifies TypeSafe's typed-decision category. The literal names fit that category; this assessment drops JEPA and the Layla phone app. OpenJev is **not established as an official open release of Jev**: the principal projects below explicitly identify themselves as independent implementations. Sources and their read dates are indexed in [sources.md](sources.md).

| Name as given | Most likely identification | Evidence | Confidence |
|---|---|---|---|
| System One Models | TypeSafe's state + typed questions → decisions/probabilities interface | [Official introduction](https://docs.typesafe.ai/introduction), operator correction | High |
| Jev | TypeSafe's hosted Jev; current documented ID `jev-1.13.0` | [Official models](https://docs.typesafe.ai/models) | High |
| OpenJev | Ambiguous community name: `razorback16/openjev` decision server using DiffusionGemma | [Project README](https://github.com/razorback16/openjev): independent, Jev-compatible | High that it fits; unresolved which release the operator saw |
| OpenJev | Also `openjev/openjev`, a 27B Qwen-family decision checkpoint | [Model card](https://huggingface.co/openjev/openjev): independent; different weights and licence | High that it fits; same name collision |
| OpenJev | Also `AlexWortega/openjev`, Qwen3.5 NLI/decision checkpoints at 0.8B, 2B and 4B | [Model card](https://huggingface.co/AlexWortega/openjev) | High that it fits; same name collision |
| Layla | Most likely **Laya**, Convai Innovations' open decision model | [Upstream code](https://github.com/NandhaKishorM/laya), [weights](https://huggingface.co/convaiinnovations/laya); a [creator's post/transcript](https://www.linkedin.com/posts/andrewpritykin_felt-like-yesterday-seriously-that-typesafe-activity-7507843323009748992-oAZX) alternates Laya/Layla | High for intended family; exact checkpoint unresolved |

No separate TypeSafe decision model literally named Layla was established by the searches. Assess Laya under that name, rather than inventing a product. Do not transfer an OpenJev project's size, licence, calibration or hardware claims to another project.

## What would count as helping

The science tests editable, queryable facts in transformer FFN weights; a context classifier does not establish that contract. The six-layer framework also requires validation, authorization, consistency and orchestration, with a governed overlay lifecycle. The research engine separately proposes source-linked suggestions and disposable analysis stores. Those are the relevant boundaries. (F:7–20; S:7–20,46–62; D:108–142.)

**Assessment/inference:** these tools may reduce narrow semantic triage work. None of the reviewed releases demonstrates our MEMIT write/read/compaction contract. Returning a schema-valid wrong answer is still a failure. Scientific verdicts, permissions, write locks, completion receipts and lifecycle transitions remain evidence/code decisions.

The specified ranges describe design, not the current watcher implementation or its measured judgement cost. The following are concrete candidate replacements for human/LLM judgements, **not claims that those judgements currently require an LLM call**.

| Place | Candidate typed decision | Stronger/simple baseline | Concrete proposed change and risk |
|---|---|---|---|
| (a) Science measurement | Does a source span support a generated probe answer? | Exact expected-answer checks plus independent review | A separate archived-output audit adapter could flag disagreements; no science-path edits. Context supplied to a judge must not be counted as evidence of in-weight retrieval. A judge can confound the measurement. |
| (b) Evidence finding | Rank already retrieved claim/source pairs as supported, contradicted, insufficient | Exact/keyword lookup plus scope/hash checks and the approved answer sheet | Optional suggestion field at the proposed research service (D:114,140), carrying source span/hash and model identity. Keep all original evidence available. Dropping a corrective caveat is the main risk. |
| (b) Answers/handoffs | Flag a claim whose citation does not support its scope | Required-field checks plus a reasoning reviewer | Annotate a source-linked answer packet; retain full context and unresolved questions. These models do not replace free-text synthesis or long reasoning. |
| (c) Watcher/queue | Classify free-text messages into read-more, needs-review, routine-status, unclear | Parse completion tokens, exit status and structured events; route explicit IDs by rules | Advisory label on a message with its source receipt, never the completion authority. A forged token, negation or missing receipt must reach existing checks regardless of label. |
| (c) Review gating | Prioritize items needing closer semantic review | Always perform required reviews | Reorder a review queue only; do not waive binding review. Suppression can hide the rare failure we are trying to find. |
| (c) Dashboard/phone | Suggest the appropriate existing read-only view or request queue | Buttons, explicit commands and known task IDs | Display a proposed destination with uncertainty through the existing service. No new phone model or assistant is justified by this decision class. Server-side inference adds latency and ownership work. |

These proposals preserve D:117–119,134–142: predictions are staged suggestions, not accepted links or live task state. They follow the parked brainstorm's requirement to earn a bounded addition against the simpler baseline. (B:1–16,182–194.)

## Probabilities are not an acceptance certificate

TypeSafe describes RLCD as training for calibrated decisions. That is a training claim, not evidence that our decisions are calibrated. Its Choice `confidence` equals `(p_max − 1/K)/(1 − 1/K)`; it summarizes concentration, not a confidence interval. Noul returns a yes probability without a separate confidence field. Test actual probabilities against labelled outcomes. ([AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer), [confidence definitions](https://docs.typesafe.ai/confidence).)

There is encouraging **task-specific** external evidence for Jev: a preprint's §4.3 reports Choice ECE 0.028 across 22 datasets/279,925 answers, but single Noul ECE 0.052 and multi-label Noul ECE 0.168. Pooled averages do not establish calibration on our rare HALT/scope failures. This is published evaluation evidence, not independently reproduced here. ([Jev evaluation, §4.3](https://arxiv.org/html/2609.37647v1#S4.SS3).)

An agent-harness preprint gives a less uniform picture: §5 reports Jev ECE 0.477 on model routing; among Laya outputs with confidence ≥0.9, 26% were wrong. §6 shows held-out misses exceeding thresholds selected in-sample, and a reported 23.9% review-cost saving shrinking to 4.3% after counting the pre-screen. Its versions/tasks differ from current releases; use these as failure hypotheses, not transferable performance estimates. ([Harness evaluation, §§5–6](https://arxiv.org/html/2610.02267v1).)

## Jev — test later, for advisory triage

**(a)** No editable-weight baseline: vendor docs say customer customization is through request state/instructions, not customer fine-tuning. It could be a supplementary judge of saved answers, but never the storage/read-back authority. **(b)** Best first hosted candidate for bounded citation-support flags; the official citation cookbook demonstrates the interface on eight examples, not production reliability. **(c)** Could suggest a queue or highlight ambiguous watcher text; cannot replace deterministic completion, permission checks or a binding reviewer. ([Models](https://docs.typesafe.ai/models), [citation cookbook](https://docs.typesafe.ai/cookbooks/citation_check).)

**Hardware/cost/licence/maturity:** hosted API; no local M3/MPS deployment or downloadable Jev weights was established. Public SDK/docs exist; service terms govern use. The documented input price is $0.042/M tokens, outputs free; 1,000 decisions at 2,000 input tokens each would cost about $0.084 before other calls (estimate, not measured). Text only; documented request limits are 64k total and 32k state plus longest question. This avoids local model residency but requires network access and sends submitted state to the provider. ([Models](https://docs.typesafe.ai/models), [legal](https://docs.typesafe.ai/legal).)

The vendor says it does not train on customer requests; ZDR is offered for enterprise customers. That does not establish our account's retention arrangements. Vendor-documented risks include numeric/date errors, indirection, adversarial state, irrelevant context and option-order effects. Pin a version and retain raw receipts. ([Legal](https://docs.typesafe.ai/legal), [jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13).)

## Laya (the likely “Layla”) — test later, for a small local trial

**(a)** Classifier training is not editable factual memory; a saved-answer judge would have the same measurement confound as Jev. **(b)** A plausible local flagger for short source/claim pairs, not whole-history answering or handoff generation. **(c)** A small fixed-label queue suggestion is plausible; avoid automatic review skipping, model-strength routing or authoritative watcher state.

**Hardware/licence/maturity:** upstream publishes code, weights, tests and an MPS path; Apache-2.0. Model-card sizes are 421M English/typed-decisions and 322M multilingual, with default contexts 512/1,024 tokens. At fp32, one 421M checkpoint's raw parameters are about 1.57 GiB (421M × 4 bytes; estimate excluding runtime/activations). M3 feasibility is plausible, not measured; avoid preloading all checkpoints. Use a separate environment and one admitted worker, never Intel. ([Weights/card](https://huggingface.co/convaiinnovations/laya), [MPS/runtime documentation](https://github.com/NandhaKishorM/laya), H:226.)

**Calibration/risk/cost:** the upstream README says checkpoints ship overconfident, multilingual lacks fitted temperatures, and MPS precision depends on batching; calibrate the served path. The weight card reports base English accuracy 0.362 versus majority baseline 0.461 on its typed-decisions benchmark; 0.766 belongs to a task-fine-tuned checkpoint. Public numbers therefore do not justify zero-shot review gating. Local inference keeps submitted state local once provisioned, but consumes the science bench; labelling, calibration and possible fine-tuning dominate upkeep. No fine-tuning is proposed in this first trial. ([Runtime/calibration](https://github.com/NandhaKishorM/laya), [weight-card limits](https://huggingface.co/convaiinnovations/laya).)

## OpenJev: razorback16/DiffusionGemma — not useful here at present

**(a)** Reading decision probabilities from a diffusion canvas establishes no MEMIT edit/query contract. **(b)** Could flag or rank evidence, but no demonstrated advantage on our records warrants a substantially larger local resident model. **(c)** Could serve queue suggestions through its Jev-compatible endpoint; it adds a server and admission burden for a job rules may already handle. Proposed production change: none.

**Hardware/licence/maturity:** Apache-2.0 server; project identifies DiffusionGemma 26B total/4B active and Apache-2.0 weights. The public MLX/Apple-silicon backend documents about 16 GB free for 4-bit operation, serialized reads and model tests. MLX uses Apple silicon; it is not the PyTorch MPS path. Active parameters do not mean only 4B weights reside in memory. Published M3 Ultra/M4 Max timings are not M3 Pro measurements. ([Upstream README](https://github.com/razorback16/openjev), [Apple-silicon weights](https://huggingface.co/mlx-community/diffusiongemma-26B-A4B-it-4bit).)

**Calibration/risk:** probabilities are read from model scores; automatic re-reads can average several noisy passes. Neither fact proves calibration. Our-domain held-out reliability evidence is UNRESOLVED. Local mode avoids hosted state transfer after provisioning, but its memory reservation competes with science; hosted Codiv is a different data/cost choice. Reconsider only if a smaller/local or hosted trial exposes a material capability gap. ([Upstream README](https://github.com/razorback16/openjev).)

## OpenJev: openjev/openjev 27B — not useful here at present

**(a)** Decision fine-tuning/readout is not our fact-store baseline. **(b)** Could score citations; no program-record advantage established. **(c)** Public browser/screenshot decisions do not justify another computer-use loop for dashboard/phone operations. Proposed change: none.

**Hardware/licence/maturity:** the card publishes code/weights and multiple formats: about 54 GB BF16 cannot fit the 48 GB pool even before overhead; MLX 4-bit is about 15 GB and text-only, so local Apple-silicon use is plausible. MLX is distinct from MPS; M3 Pro runtime peak/latency is UNRESOLVED. Weights are CC BY-NC 4.0; helper/serving code Apache-2.0. Research use and production/commercial use must not be conflated. ([Model card](https://huggingface.co/openjev/openjev), [MLX build](https://huggingface.co/openjev/openjev-MLX-4bit).)

The card reports fixed calibration settings, held-out accuracy and quantization comparisons; these do not establish probability calibration on our records. Current inference evidence here is maintainer-reported, not reproduced. Risk: size, quantization-dependent decisions, noncommercial terms and confusing this model with the Apache-licensed DiffusionGemma server. Local operation is possible; its current priority is poor, rather than intrinsically incompatible with the M3.

## OpenJev: AlexWortega small Qwen/NLI — test later, second local candidate

**(a)** A comparison judge for archived answer/evidence pairs is plausible, not an alternative demonstrated fact store. **(b)** Its entailment/contradiction/neutral interface matches source-support triage more directly than queue control. **(c)** It could classify free-text queue candidates, but offers no established advantage over small Laya or rules for that role. No live integration recommended.

**Hardware/licence/maturity:** card lists MIT and public code/checkpoints at 0.8B/2B/4B. Raw fp32 parameter estimates are roughly 2.98/7.45/14.90 GiB respectively, excluding activations/runtime. Only the smallest merits an initial bench slot. Public Transformers loading is documented; this review did not establish a working MPS path or compatibility with our pinned science environment. Both are UNRESOLVED, so use an isolated trial environment, not a science dependency upgrade. ([Model card](https://huggingface.co/AlexWortega/openjev).)

**Calibration/risk/cost:** training is described as cross-entropy NLI, with option-wise decisions derived from softmax. Reported AUROC/accuracy/order stability does not establish calibrated probabilities. More options require more option scoring; a valid distribution can still be confidently wrong. Local inference would avoid provider state transfer after provisioning. Operational fit is conditional on loading correctly, keeping its memory bounded and outperforming a simpler flagger. ([Model card](https://huggingface.co/AlexWortega/openjev).)

## Verdicts and cheap falsifiable tests

No tool earns **adopt now**. **Jev: test later; Laya: test later; AlexWortega/OpenJev-small: test later conditionally. DiffusionGemma/OpenJev and 27B OpenJev: not useful here at present.** The class has an engineering opportunity around advisory semantic checks, not demonstrated F1 closure. Prioritize one trial, after the currently queued work; do not launch three services. (F:13–20; B:182–194.)

**Shared trial contract (proposed, UNRUN):** stage `cases.jsonl`, `adapter.py` and `receipts.jsonl` under a separately authorized `results/system_one_decision_trial/`; edit no science engine, frozen plan, manager or live watcher. Freeze 240 short, source-linked cases before inference: 80 development, 160 blind test, grouped by source/run to prevent leakage. Include unsupported claims, reversed negations, fixture/live conflation, scope changes, forged completion text and insufficient evidence. Label independently against source receipts; unresolved gold is explicitly ambiguous. Use four advisory labels, retaining all cases for normal review.

Compare byte-identical inputs against (1) deterministic status/ID/keyword rules and (2) the existing chosen LLM/manual workflow, whose actual cost must first be measured. Fit any temperature/threshold on development only; freeze model, dtype, token budget and prompt. Report Brier score, ten-bin ECE with bin counts, issue recall, false alarms, abstention/coverage and end-to-end cost/time including escalation. Reversed option order on a fixed 40-case subset is a robustness check, not extra tuning data.

| Tool/test | Pass/fail rule | Proposed ceiling |
|---|---|---|
| Jev J1: advisory source-support/triage | On blind test: ≥95% issue recall, ≥20% fewer benign flags than rules at that recall, ECE ≤0.10, and ≥25% lower total triage cost or operator time than the measured workflow. Fail on any loss of required-review coverage; otherwise an unmet criterion fails the trial. | ≤1,000 requests, ≤2M input tokens, ≤$1 Jev spend, ≤$5 total hosted comparison spend, 30 min; only explicitly permitted public/redacted state. |
| Laya L1: same short four-label task | Same quality/calibration/benefit rules as J1. Fail if truncation hides a material source clause, MPS cannot run the pinned trial, or any hard ceiling is exceeded. If zero-shot fails, report failure; no training rescue inside this trial. | One checkpoint; ≤4 GiB peak process memory, ≤3 GiB total setup/download writes, ≤20 min admitted M3 time, 1 worker, no concurrent science; free disk ≥23 GiB before provisioning. |
| AlexWortega A1: smallest NLI checkpoint on same claim/source task | First require a real local loading/MPS receipt within the ceiling, then the same blind quality/benefit rules. If Laya passes, require ≥20% fewer false alarms at the same recall to justify the second model. Failed loading/calibration is FAIL, not a silent CPU fallback. | One 0.8B checkpoint; ≤6 GiB peak process memory, ≤5 GiB total setup/download writes, ≤20 min admitted M3 time, 1 worker, no concurrent science; free disk ≥25 GiB. |

These are inexpensive rejection screens, not production acceptance or a statistically established guarantee of rare-event safety. Never interpret zero observed critical misses in this small set as zero risk. Test limits and thresholds are proposed choices, not measured vendor capabilities. All Intel local model execution remains prohibited. (H:226.)

## Open questions for the operator

1. Which exact OpenJev repository/checkpoint prompted the request? Does “Layla” indeed mean Convai Laya?
2. Which current judgement consumes enough operator time or LLM calls to warrant a trial: watcher ambiguity, queue destination, or claim/source support? Supply its receipt format and baseline volume/cost.
3. May public/redacted record excerpts leave the machine for Jev? What account retention terms apply? If not, prefer one local Laya rejection screen when M3 admission allows it.
4. What false-alarm burden is acceptable for an advisory queue? Required review coverage stays intact; changing that policy is outside this assessment.

## S1M HANDOFF

**Done:** literal-name identification; corrected TypeSafe scope; authorized stack ranges read; primary docs/cards and two evaluation preprints inspected; sourced provisional verdicts, calibration caveats and bounded tests written. No research or model test ran. No JEPA/phone-app recommendation remains.

**Remaining:** exact operator-intended OpenJev/Laya release; actual watcher/queue judgement surface and baseline cost; Jev account retention/egress permission; M3 Pro empirical fit; local-checkpoint calibration. UNRESOLVED items are not proven unavailable. Web sources are dated snapshots, not pinned or independently reproduced evaluations. Proposed trials remain UNRUN.

**Exact next single step:** MAESTRO supplies one existing judgement's source-linked fixture packet and current baseline receipt (recommended: claim/source support), plus the exact intended model ID; a fresh successor then freezes that one comparison before any separately authorized installation or inference.

**Context rule, binding through successors:** start a new step only at ≥60% context left. At ≤40%, or on any context compaction, stop starting work, add/update `## S1M HANDOFF` with done, remaining and the next single step, and reply `S1M HANDOFF`. MAESTRO directed this stop at approximately 42%; no further source reading followed that instruction.
