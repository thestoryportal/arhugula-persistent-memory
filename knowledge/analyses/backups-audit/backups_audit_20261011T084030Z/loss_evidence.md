# RunPod loss evidence — BK3

This is a loss-evidence review, not an import authorization or final audit.
The systematic search is saved in `loss_evidence_search.tsv`, with one
path:line and JSON-escaped source line per hit. Its scope and observed HEAD are
in `loss_evidence_state.json`: 508 files, 1,053 matching lines, zero oversized
line fragments. Scope covers CORPUS/, SESSION_CHECKPOINT.md,
EXPERIMENT_RUNBOOK.md, REPRODUCIBILITY.md, docs/, memory_mirror/, and 37
results/ README files. Generic words such as missing, pod, and lost are leads;
scientific recall loss and fixture lifecycle loss are not disk-loss evidence.

## Recorded losses and later recovery

| Record | Source citation | What the record supports |
|---|---|---|
| RunPod balance lapsed; working volume lost | `SESSION_CHECKPOINT.md:1053`; `EXPERIMENT_RUNBOOK.md:89,446,991`; `REPRODUCIBILITY.md:7` | Loss of Qwen covariance caches, downloaded HF models, B3 edited model/GGUF, llama.cpp/LARQL builds, and run logs. The same record explicitly says Workstream-1 documents and the patched engine had already been recovered through PRs #1/#2. |
| Engine preserved in Git | `REPRODUCIBILITY.md:9` | Vendored upstream engine plus patches; downloaded data/stats remain gitignored. A runbook or checksum list is not a recovered cache. |
| Local model/cache regeneration and known-baseline reproduction | `SESSION_CHECKPOINT.md:1051`; `EXPERIMENT_RUNBOOK.md:87` | Pinned Qwen2.5-3B re-downloaded; band [4–8] covariance regenerated locally; C2/A1 baseline and inertness checks recorded. These are later recorded reproductions, not byte recovery from this backup. |
| Local B3 export/serving regeneration | `SESSION_CHECKPOINT.md:1049`; `EXPERIMENT_RUNBOOK.md:85` | B3 edit, FP16 GGUF conversion, Q4_K_M quantization and CPU serving reproduced on 2026-10-04. The generated next-action at runbook :121 still refers to B3 regeneration; use the later explicit completion entry when interpreting current loss status. |
| InfraNodus pod-era export proof file lost | `memory_mirror/infranodus-discourse-lens-not-coverage-tool.md:20` | A graph export demonstration under /workspace was lost with the pod. No named backup candidate has yet been identified as that proof. |

The full context at these locations was read in bounded ranges. These lines
are from the observed working-tree state; canonical documents are being
updated concurrently. Recheck citations if MAESTRO modifies their layout.

## How to map candidates

Use `none` / `no recorded loss` in a gap-table row unless both a loss record
and evidence identifying the actual backup bytes as that lost artifact exist.
Distinct April/May session documents, protocols, finding drafts and manifests
may preserve useful historical details absent from the current document set,
but the general statement that RunPod was lost does not establish that each
of those documents was lost there. The same loss record says Workstream-1
documents were recovered. Do not map a document to a tensor/model/cache loss.

Specific safeguards already supported by the reviewed backup contents:

- `deep-research-report.md:5` reports a failed public search for caches for
  Llama-3.1-8B and lists near matches for different checkpoints. It is a search
  report, not covariance bytes. It also carries export citation markers;
  this audit has not verified those external claims.
- `llm-as-database/s2_5b_artifact_checksums.txt` contains 19 MD5 entries.
  It preserves expected checksums, not the bytes of the referenced artifacts.
- `llm-as-database/pre_s2_6_fork_work_summary_block.md:3-5` describes production
  of five .npz caches and provenance. A summary about producing caches does
  not restore those caches, and it concerns the earlier Llama stage rather
  than the Qwen caches listed in D-HW-1.
- Nine root `stage_1_trial_cfb-*_r*.json` files have SHA256-identical sibling
  mirror copies, as recorded in `program_byte_copies.jsonl`. These are actual
  early trial records already preserved outside the assigned worktree; they
  are not the Qwen covariance/HF/B3 artifacts named in the loss record.
- Root `aggregate_verdict.json` is an early nine-trial Stage 1 cohort dated
  2026-05-01. The worktree counterpart is a later fifteen-trial Stage 1 v3
  cohort dated 2026-05-04. Neither a filename match nor trial-summary overlap
  licenses replacement or a claim that lost individual trial bytes returned.

Final candidate-by-candidate mapping and recommendations remain the final
audit report's responsibility. No lost model, tensor, covariance cache, build
or InfraNodus export proof has been claimed recovered by BK3.
