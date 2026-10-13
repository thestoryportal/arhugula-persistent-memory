# S1M source register

Read date for every URL below: **2026-10-11**. Public pages were inspected through web search/open; no authenticated inference endpoint, model execution or weight download was used. Entries distinguish specifications/maintainer reports from outside evaluations. Report letter references resolve below. Only requested local ranges inform the assessment.

## Local authority

| ID | Source (worktree-relative file:line) | Use |
|---|---|---|
| F | `DISCIPLINE.md:7–20` | F1 goal, editable/queryable FFN memory, fallback boundary |
| S | `docs/SPEC_E2E_GROUND_TRUTH.md:7–20` and `:46–62`; other section headings skimmed | Paradigm, six layers, governed memory lifecycle |
| H | `results/compute_storage_brainstorm_20261011T054507Z/design.md:226` | Binding no-local-model rule on Intel |
| D | `results/research_engine_brainstorm_20261011T032049Z/design.md:108–142` | Approved engine ownership, service, provenance and suggestions |
| B | `results/research_engine_dag_rag_icm_brainstorm_20261011T095840Z/brainstorm.md:1–16` and `:182–195` | Parked assessment's bounded-test style and priority |

M3 Pro/48 GB/MPS/no-CUDA hardware and the pinned science environment were supplied in the task/AGENTS instructions; no new machine inventory was run. The operator's TypeSafe correction and MAESTRO's context-stop instruction are conversation authority, not external capability evidence.

Local source SHA-256 values captured before writing the deliverables (identity receipts, not a claim that concurrent work never changed them):

```text
d96169ff49ceaa5460ea6bc74152b27b7bf798113fa0969f43dfef1d0162a644  DISCIPLINE.md
ff7573878ad9aecec5f6b5a7f5243022fb401ece9b56159f0f65a420a283160e  docs/SPEC_E2E_GROUND_TRUTH.md
20f88e7c50acff3e0061dd9c6dee0e70e68627a197e5921e9acb344a075717b1  results/compute_storage_brainstorm_20261011T054507Z/design.md
aa09563f092b6da8e01f900339720ee5cb46397cd3f5b98649f949de728dc6df  results/research_engine_brainstorm_20261011T032049Z/design.md
d445590a7fef405c013e09413339155e5dbffd349756dc782a095d2117ddb479  results/research_engine_dag_rag_icm_brainstorm_20261011T095840Z/brainstorm.md
```

## TypeSafe primary sources

| Source URL | Read date | Evidence and limits |
|---|---|---|
| https://typesafe.ai/blog/introducing-system-one-models-and-jev | 2026-10-11 | Vendor category introduction and automation examples; marketing is not acceptance evidence |
| https://docs.typesafe.ai/introduction | 2026-10-11 | State, Choice/Score/Noul, typed output, narrow judgement boundary |
| https://docs.typesafe.ai/llms.txt | 2026-10-11 | Documentation discovery; actual model/limitations pages located here |
| https://docs.typesafe.ai/models | 2026-10-11 | Jev 1.13 ID/aliases, input pricing, context/text input, request customization, data handling |
| https://docs.typesafe.ai/introduction/machine-learning-primer | 2026-10-11 | Vendor RLCD claim and population-level meaning of calibration |
| https://docs.typesafe.ai/confidence | 2026-10-11 | Choice formula, Score distribution summary, Noul has no separate confidence |
| https://docs.typesafe.ai/model-jaggedness/jev-1.13 | 2026-10-11 | Vendor limitations: numbers/dates, indirection, adversarial state, option order, generation |
| https://docs.typesafe.ai/legal | 2026-10-11 | Links to service agreements/data processing/privacy; enterprise ZDR offer, not our account's confirmed terms |
| https://docs.typesafe.ai/cookbooks/citation_check | 2026-10-11 | Exact quote matching plus semantic Choice; eight-example demonstration; cached Jev 1.12 results dated 2026-08-16 |

## Open implementations and weights — primary maintainer sources

| Source URL | Read date | Evidence and limits |
|---|---|---|
| https://github.com/NandhaKishorM/laya | 2026-10-11 | Upstream README: MPS path, precision/batching, calibration caveats, public tests and fine-tuning; maintainers' measurements are not M3 Pro qualification |
| https://huggingface.co/convaiinnovations/laya | 2026-10-11 | Apache-2.0 weights/card, checkpoint sizes/default context, base vs fine-tuned results and limits |
| https://huggingface.co/convaiinnovations/laya/resolve/main/README.md | 2026-10-11 | Text version inspected; resolved snapshot commit `7b928d828b7b0e022f929d9bd2e44165aa270148`; older card details can differ from current runtime README |
| https://github.com/NandhaKishorM/laya/blob/main/pyproject.toml | 2026-10-11 | Public package/version/dependency declarations; not empirical compatibility with our science environment |
| https://github.com/razorback16/openjev | 2026-10-11 | Independent DiffusionGemma server, Apache-2.0, MLX/vLLM options, rereads, tests and resource descriptions |
| https://github.com/razorback16/openjev/blob/main/README.md | 2026-10-11 | Apple-silicon subsection: about 16 GB free, serialized reads, M3 Ultra/M4 Max timings; not M3 Pro timing |
| https://github.com/razorback16/openjev/blob/main/openjev/mlx_backend.py | 2026-10-11 | Public MLX backend existence/serialized worker discovery; no runtime test |
| https://huggingface.co/mlx-community/diffusiongemma-26B-A4B-it-4bit | 2026-10-11 | Public Apple-silicon weight listing; only metadata/card read |
| https://huggingface.co/openjev/openjev | 2026-10-11 | Separate 27B Qwen-family project; BF16/MLX/GGUF sizes, text-only local variants, calibration settings, CC BY-NC weights vs Apache helper code |
| https://huggingface.co/openjev/openjev-MLX-4bit | 2026-10-11 | Public local 4-bit variant exists; not a proven process-memory ceiling |
| https://huggingface.co/AlexWortega/openjev | 2026-10-11 | Separate 0.8B/2B/4B Qwen3.5 NLI family, MIT card label, cross-entropy/option scoring, public code/results; MPS qualification not established |

## Outside evaluation papers — primary research sources

| Source URL | Read date | Specific evidence used |
|---|---|---|
| https://arxiv.org/abs/2609.37647 | 2026-10-11 | Evaluating and Benchmarking the System One Model Jev; Jev 1.13.0, public benchmark/harness claim; preprint, not reproduced here |
| https://arxiv.org/html/2609.37647v1 | 2026-10-11 | §4.3 / Fig. 2: 22 Choice datasets, 279,925 answers, ECE 0.028; single Noul 0.052, multi-label Noul 0.168; §4.4 rubric limits |
| https://arxiv.org/abs/2610.02267 | 2026-10-11 | Fast Models, Slow Evidence; paired Jev/Laya evaluation and self-audit |
| https://arxiv.org/html/2610.02267v1 | 2026-10-11 | §5: routing/calibration/overconfidence; §6: held-out threshold misses and pre-screen cost; Appendix E versions differ from current Laya runtime |

## Identification and discovery only

| Source URL | Read date | Use; not technical acceptance evidence |
|---|---|---|
| https://www.linkedin.com/posts/andrewpritykin_felt-like-yesterday-seriously-that-typesafe-activity-7507843323009748992-oAZX | 2026-10-11 | First-person post says Laya; associated transcript says Layla/Jeb/Jeff/Lyra: direct evidence that these names are mistranscribed |
| https://systemonemodels.org/about/ | 2026-10-11 | Independent directory supplied discovery leads; not TypeSafe, despite category naming |
| https://www.typesafeai.org/jev | 2026-10-11 | Explicitly independent explanation; not the vendor's official domain; replaced with typesafe.ai/docs for claims |

Literal searches included “Jev”, “OpenJev”, “layla” with System One, plus TypeSafe/GitHub/Hugging Face scoped variants and “Laya”. The corrected intended category is established; absence of a separate literal Layla decision model is a search result, not proof of nonexistence. Initial JEPA/phone-app branches were excluded after the operator correction.

Some guessed documentation paths (`/introduction/models`, `/introduction/limitations`, `/introduction/pricing`) failed; markdown endpoints also returned fetch/content-type errors. These were observation-layer failures: the non-markdown pages found through the official documentation index were readable. No missing-service claim rests on those failures.

Assessment memory pass: `rg` over the personal memory registry returned no task-relevant matches; no prior memory fact informed the report. Tool policy was read from `/Users/robertrhu/.codex/RTK.md:1–29`. Worktree identity was verified as branch `worktree-c10k-route-a` at the requested root. No graft command/tool was used.
