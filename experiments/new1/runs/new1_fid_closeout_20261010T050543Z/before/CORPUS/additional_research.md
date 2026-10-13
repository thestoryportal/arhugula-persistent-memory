# additional_research.md — prior art & supporting documents
_Pointers (not duplicated here). All under `/workspace/`._

## Prior art / external (read-only references)
- `external_prior_art/larql/` — LARQL source (Rust): the spec's read/query/deploy layer. Key: `crates/larql-models/src/architectures/qwen.rs` (Qwen2/2.5/3 support incl. bias), `crates/larql-inference/src/forward/memit.rs` (MEMIT solve), `crates/larql-lql/src/executor/compact.rs` (COMPACT), `crates/larql-vindex/src/patch/format.rs` (.vlp JSON format), `README.md`/`WORKING_MODEL.md`/`ROADMAP_STATUS.md` (Gemma-validated; KNN-unsafe-at-scale → FR-routing/ROUTE VERIFY fix; Metal-first).
- `external_prior_art/the-mechanism/` — Chris Hay "the-mechanism" (add-a-neuron / allocation FFN model; LARQL conceptual basis).

## This program's authored documents
- `research_and_specs/llm-as-database-v1_2-integrated-spec.md` — THE spec (audit baseline; see CORPUS/05).
- `write_engine_viability_determination_report.md` — the determination verdict (Phase 0/1 + workaround ladder).
- `write_engine_viability_determination_plan.md`, `spec_predev_validation_plan.md` — the programs.
- `framework_finding_v1_10_additive.md` — consolidated finding (calibrated metric + model/size dependence).
- `LARQL_INTEGRATION_ASSESSMENT.md` — full LARQL integration narrative + the bridge (log-based evidence transcripts).
- `EVIDENCE_INDEX.md`, `SESSION_CHECKPOINT.md` — prior running indices (superseded by this CORPUS for council use; retained for history).
- `skills/` — the 7-skill Framework Council (the spec's authoring + adversarial-review framework).

## Research literature grounding (as used in-method)
- MEMIT (Meng et al. 2022-23) — the edit solve `ΔW=(V*-WK*)(K*ᵀC⁻¹K*+λI)⁻¹K*ᵀC⁻¹`.
- AlphaEdit (null-space projection P of covariance; sequential cache_c preservation) — our R-ALPHA recipe.
- Knowledge-distortion / same-entity locality (arXiv 2601.17343) — endorses the behavioral-deviation (JS) metric.
- ROME / GRACE / WISE — alternatives in the escape-hatch ladder (see determination report).
