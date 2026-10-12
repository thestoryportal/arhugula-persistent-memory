═══════════════════════════════════════════════════
PRE-S2.6 FORK-WORK SESSION SUMMARY BLOCK — v2
PRIMARY OUTPUTS: fresh covariance cache (5 .npz @
                 canonical NV path), PROVENANCE.txt
                 authoritative, P-6 patch authored,
                 OQ-S25-9 CLOSED, Session 2.6
                 UNBLOCKED
SESSION TYPE: Workstream 1 fork-work re-attempt
              (cell-by-cell runbook execution)
PREDECESSOR: pre-S2.6 fork-work (S2.5 close;
             HALT-INCOMPLETE on dataset-loader
             incompatibility)
RUNBOOK CONSUMED: pre_s2_6_fork_work_runbook.md
                  v1.2.2 (cells 0–5)
CANONICAL DOC: memit-patches-canonical.md v2.2.1
RECLASSIFICATION: HALT-INCOMPLETE → CLOSED-PASS
SESSION CLOSE: 2026-05-01T06:06:17Z
═══════════════════════════════════════════════════

DECISIONS MADE
───────────────────────────────────────────────────
D-PreS26-4. Patch P-6 authored and applied.
     Target: rome/layer_stats.py:40. Pre-state:
     `size_suffix = "_t{batch_tokens}" + size_suffix`
     (missing f-string prefix, propagates literal
     placeholder into cache filename). Post-state:
     `size_suffix = f"_t{batch_tokens}" + size_suffix`.
     Universal patch; required when batch_tokens
     < npos (which is required for tractability on
     Llama-3.1-8B with npos=131072). Idempotent.
     NV-applied this session; markers verified via
     re-import.

D-PreS26-5. model_name parameter to layer_stats
     must be passed in underscore form
     ("meta-llama_Llama-3.1-8B"), not slash form
     ("meta-llama/Llama-3.1-8B"), to produce the
     canonical flat cache subdirectory
     /workspace/covariance_caches/meta-llama_Llama-3.1-8B/
     rather than the nested form
     /workspace/covariance_caches/meta-llama/Llama-3.1-8B/.
     Library applies slash-to-underscore conversion
     only on the model_name=None default path
     (rome/layer_stats.py:41-42); explicit pass
     bypasses conversion. Closes OQ-PreS26-23.

D-PreS26-6. batch_tokens=100 is the canonical Stage
     1 value. Source of truth: explicit constant in
     dispatch cell, NOT a hparams JSON field.
     Upstream MEMIT MEMITHyperParams dataclass
     schema does not declare batch_tokens; adding
     the field to hparams JSON triggers TypeError
     at MEMITHyperParams.from_json(). The function
     parameter alone controls compute behavior.
     Filename construction reads from the function
     parameter (post P-6), not from a hparams
     attribute. Closes OQ-PreS26-22 + OQ-PreS26-28.

D-PreS26-7. .npz Phase C key resolution must use
     MEMIT runningstats.SecondMoment reflection
     convention. Canonical key path for the
     covariance matrix is "{name}.{name}" (i.e.,
     "mom2.mom2" for the mom2 collector), not the
     flat "mom2" path the runbook v1.2.2 author
     assumed. Phase C consumer must use a priority
     list ["mom2.mom2", "mom2", <alphabetical-first
     non-metadata>] with metadata exclusion list
     extended to include "mom2.constructor" and
     "mom2.count". Closes OQ-PreS26-31 in-flight
     for this session; canonical
     stage_1_sect_runbook.md v1.1 → v1.2 revision
     required pre-Session-2.6.

D-PreS26-8. PROVENANCE.txt at canonical cache path
     is the authoritative provenance manifest for
     downstream Session 2.6 Cell 3 gate. Required
     fields (7): model_name, model_revision_sha,
     layer_set, sample_count, dtype, computed_at,
     produced_by_session. Auxiliary fields
     (informational, below separator line):
     revision_sha_source, bridge_archive,
     batch_tokens, patches_applied. Authored
     2026-05-01T06:05:57Z. Carries
     model_revision_sha =
     d04e592bb4f6aa9cfee91e2e20afa771667e1d4b
     (Llama-3.1-8B HF default revision; captured
     via model.config._commit_hash, strong-form).

D-PreS26-9. Cell 4 wall-time empirical envelope
     reconciles to kickoff projection, not runbook
     v1.2.2 §1.6 projection. Empirical: ~14–20 min
     per layer × 5 layers = 1.42 hours total
     (~$0.80 GPU). Runbook v1.2.2 §1.6 projection
     of 4–8 hours was conservative by 3–5×. Kickoff
     ~90 min projection validated empirically.
     Routing: runbook v1.2.3 §1.6 update at S2.7
     retrospective. Closes OQ-PreS26-20 +
     OQ-PreS26-27.

D-PreS26-10. HF cache env var discipline must
     export ALL of HF_HOME, HF_HUB_CACHE,
     HF_DATASETS_CACHE, HUGGINGFACE_HUB_CACHE,
     TRANSFORMERS_CACHE, TMPDIR before any
     transitive transformers/datasets import.
     Mechanism: huggingface_hub.constants.HF_HUB_CACHE
     is frozen at first-import; env mutations
     after import do not propagate to library
     internal constants. Cell 0 of runbook v1.2.2
     does NOT export these — first-export occurred
     mid-session via remediation cell. Closes
     OQ-PreS26-14 + OQ-PreS26-18.

═══════════════════════════════════════════════════
CONSTRAINTS ESTABLISHED
═══════════════════════════════════════════════════
C-PreS26-2. Cell 5 Phase C consumer of MEMIT
     covariance cache MUST resolve mom2 matrix via
     priority list ["mom2.mom2", "mom2", <fallback>]
     with metadata exclusion. Flat-name resolution
     ("mom2" alone) is insufficient against current
     MEMIT serialization at SHA 80426fd9.

C-PreS26-3. layer_stats invocation MUST pass
     model_name in underscore form when explicit;
     MUST NOT rely on default-path slash conversion.
     Rationale: explicit model_name discipline is
     mandated by OQ-S25b-2 closure, but the library
     implements slash conversion only on the
     None-default branch.

C-PreS26-4. batch_tokens MUST be passed to
     layer_stats as an explicit value in the dispatch
     site (constant or local variable); MUST NOT be
     sourced from MEMITHyperParams JSON. The
     dataclass schema rejects unknown kwargs at
     from_json deserialization.

C-PreS26-5. P-6 patch MUST be applied to
     rome/layer_stats.py before any layer_stats
     invocation that satisfies batch_tokens < npos.
     Without P-6, output filenames carry literal
     "{batch_tokens}" placeholder, breaking
     downstream Cell 5 R1.1 file-set predicate and
     stage_1_sect_runbook.md Cell 3 R1.1.

═══════════════════════════════════════════════════
OPEN QUESTIONS DEFERRED
═══════════════════════════════════════════════════
OQ-S25-9   CLOSED (see D-PreS26-8 + Cell 5 PASS
        verdict 2026-05-01T06:06:17Z). Fresh
        covariance cache resident at
        /workspace/covariance_caches/
        meta-llama_Llama-3.1-8B/wikipedia_stats/;
        5 × 822 MB .npz files; PROVENANCE.txt
        authoritative; mom2.mom2 shape (14336,
        14336) float32 verified per file;
        sample_size = 100000 verified per file.
        Session 2.6 Cell 3 gate will pass against
        this cache (subject to OQ-PreS26-26 and
        OQ-PreS26-31 canonical follow-up).

OQ-S25-10  OPEN (MEDIUM; baseline cache).
        Out of scope for this session; not yet
        triaged.

OQ-PreS26-9   OPEN (LOW). Cell 1 (environment
        fingerprint) reclassification REQUIRED on
        pod-stop boundary. Session deferred Cell 1
        as OPTIONAL; pod stop/start cycle between
        S2.5b §4.3 close and this session start
        invalidated container-disk auth state and
        first surfaced at Cell 3 Phase B
        (GatedRepoError 401). Cell 1 dispatch
        before any compute-side cell would have
        caught the auth gap pre-flight. Routing:
        runbook v1.2.3 §1.7 hardening at S2.7
        retrospective.

OQ-PreS26-10  OPEN (LOW). Auth-handling section
        should specify silent-read pattern as
        canonical (read -s HF_TOKEN) to prevent
        token exposure in chat transcripts.
        Surfaced when raw token was pasted into
        chat verbatim during §3.4 login flow.
        Routing: runbook v1.2.3 §1.7 + auth-handling
        section.

OQ-PreS26-11  OPEN (MEDIUM). Cell 3.5 should
        self-establish cwd and sys.path discipline
        at entry rather than rely on inherited
        Cell 2 state. Operator-authored maintenance
        cells between Cell 2 and Cell 3.5 mutated
        cwd → /workspace/session_logs and removed
        MEMIT_ROOT from sys.path; remediation
        required two extra dispatch cells. Defensive
        entry pattern reduces operator-error blast
        radius. Routing: runbook v1.2.3 hardening.

OQ-PreS26-12  OPEN (INFO). /workspace/session_logs/
        operator-created log directory should be
        documented in runbook §1.7 pre-flight
        checklist if it persists across sessions;
        relative-path log-write pattern flagged as
        C-S25-5 risk vector.

OQ-PreS26-13  OPEN (LOW). Operator-authored
        maintenance cells between canonical runbook
        cells should be flagged in session notes;
        cwd / sys.path / sys.modules mutations
        between canonical cells should require an
        explicit re-establishment cell before the
        next runbook cell dispatch.

OQ-PreS26-14  CLOSED (see D-PreS26-10). Cell 0 must
        export HF_HUB_CACHE, HF_DATASETS_CACHE,
        TRANSFORMERS_CACHE, TMPDIR to NV-resident
        paths in addition to HF_HOME. §1.7
        pre-flight checklist must mandate ≥30 GB
        free NV + ≥10 GB free container disk
        before Cell 3.5 dispatch. Routing: runbook
        v1.2.3 Cell 0 amendment.

OQ-PreS26-15  OPEN (LOW). Wikipedia dataset size
        (~22 GB compressed parquet) absent from
        runbook v1.2.2 §1.6 cost projection; storage
        projection should distinguish container-disk
        peak vs NV-residual. Routing: runbook v1.2.3
        §1.6 update.

OQ-PreS26-16  OPEN (LOW). §1.7 pre-flight checklist
        should require disk-state assertions:
        container disk ≥10 GB free, NV ≥30 GB free,
        no orphan caches at /root/.cache/huggingface/.

OQ-PreS26-17  OPEN (LOW). Investigation deferred:
        how 20 GB landed at
        /root/.cache/huggingface/hub on this pod.
        Possible S2.5a procedure gap or S2.5b §4.3
        intermediate state predating HF_HOME export
        discipline. Cleanup performed; root cause
        investigation deferred to S2.7.

OQ-PreS26-18  CLOSED (see D-PreS26-10).
        huggingface_hub.constants.HF_HUB_CACHE is
        frozen at first-import. Empirically verified
        via direct probe: post-session env
        HF_HUB_CACHE = /workspace/hf_cache/hub but
        library constant remained
        /root/.cache/huggingface/hub. Cause of
        11 GB regrowth on container disk during
        Cell 3.5 despite env exports.

OQ-PreS26-19  OPEN (LOW). Cell 3.5 expected-path
        predicate at runbook v1.2.2 line 855–858
        does not match empirical layer_stats
        behavior at sample_size=1000 — function
        returns in-memory mom2 dict without disk
        persistence at small sample sizes. Recommend
        runbook v1.2.3 reduce smoke predicate to
        "exception-free return" only; preserves
        contamination-prevention property.

OQ-PreS26-20  CLOSED (see D-PreS26-9). Kickoff
        prompt cost/wall-time embedded figures
        empirically validated; runbook v1.2.2 §1.6
        was conservative.

OQ-PreS26-21  OPEN (LOW). Runbook v1.2.2 Cell 4
        Phase 0 expected-pattern documentation
        should reconcile to empirical layer_stats
        signature: to_collect has no default,
        progress default is tqdm.auto.tqdm not
        tqdm.std.tqdm. No execution impact.

OQ-PreS26-22  CLOSED (see D-PreS26-4 + D-PreS26-6).
        layer_stats filename construction does NOT
        use a hparams attribute. Original H4
        hypothesis refuted by source diagnostic;
        actual root cause was P-6 line-40 f-string
        bug.

OQ-PreS26-23  CLOSED (see D-PreS26-5). Library
        slash-conversion only on default path;
        explicit model_name pass in underscore form
        produces canonical flat cache subdirectory.

OQ-PreS26-24  OPEN (LOW). Cell 4 Phase 1 file-naming
        assertion at runbook line 1063 is
        fail-loud rather than fail-fast; assertion
        fires AFTER 14-min layer compute. Predicate
        verification should occur via dry-run-style
        filename probe BEFORE compute commits.

OQ-PreS26-25  CLOSED (see D-PreS26-4). MEMIT
        library bug at rome/layer_stats.py:40
        (missing f prefix). P-6 patch authored,
        applied, NV-resident. Idempotent.
        memit-patches-canonical.md v2.2.1 → v2.3
        must add §3.7 P-6 specification at S2.7.

OQ-PreS26-26  PARTIALLY RESOLVED (see D-PreS26-7
        in-flight Cell 5 R1.1 update; canonical
        follow-up REQUIRED).
        stage_1_sect_runbook.md v1.1 Cell 3 R1.1
        file-naming predicate must be updated to
        include "_t100_" segment in expected
        filename pattern. Required pre-Session-2.6
        dispatch. Cache produced this session uses
        post-P-6 canonical filename form; consumer
        runbook lacks reconciliation. Routing:
        stage_1_sect_runbook.md v1.1 → v1.2 update
        before Session 2.6 kickoff.

OQ-PreS26-27  CLOSED (see D-PreS26-9).

OQ-PreS26-28  CLOSED (see D-PreS26-6). hparams JSON
        schema does NOT carry batch_tokens; value
        flows via dispatch-cell explicit constant.

OQ-PreS26-29  OPEN (LOW). Process discipline:
        avoid pre-authoring remediation steps that
        depend on unconfirmed hypotheses; sequence
        diagnostic completion → analysis →
        remediation strictly. Surfaced when Step 3
        (hparams field-add) was queued before
        source diagnostic refuted the underlying
        hypothesis; field-add introduced a
        TypeError that required reversion.

OQ-PreS26-30  OPEN (LOW). Presentation discipline:
        code blocks in spec narrative that are not
        intended for execution must be visually
        distinguishable from dispatch cells (e.g.,
        truncation, "DO NOT EXECUTE" prefix, inline
        rendering). Surfaced when documentation
        block was operator-executed alongside
        dispatch cell.

OQ-PreS26-31  PARTIALLY RESOLVED (see D-PreS26-7
        in-flight Cell 5 Phase C update; canonical
        follow-up REQUIRED). Cell 5 Phase C mom2
        key resolution must use MEMIT
        runningstats.SecondMoment reflection
        convention. stage_1_sect_runbook.md v1.1
        Cell 3 likely shares the same logic and
        must be updated to v1.2 before Session 2.6
        dispatch. Same routing as OQ-PreS26-26.

OQ-S25b-1     OPEN (carry-forward from S2.5b).
        stage_1_sect_runbook.md v1.3 hardening.
        Out of scope this session; routing
        unchanged.

OQ-S25b-2     CLOSED (carry-forward from S2.5b
        §4.8 archaeology, validated this session).
        layer_stats invocation requires explicit
        model_name parameter; underscore-form fix
        applied per D-PreS26-5.

OQ-S25b-3     OPEN (carry-forward).

OQ-S25b-4     OPEN (MEDIUM; carry-forward from
        S2.5b §4.3). canonical doc v2.2.1 §3.6 P-5
        anchor specification reconciliation
        deferred to S2.7 retrospective; v2.2.1
        footer-version-addition patch closed
        OQ-S25b-5; semantic content reconciliation
        outstanding.

═══════════════════════════════════════════════════
INTERFACE CONTRACTS DEFINED
═══════════════════════════════════════════════════
IC-PreS26-2. layer_stats (rome/layer_stats.py post-P-6)
        → cache filename consumer
        (Cell 5 Phase B / stage_1_sect Cell 3 R1.1):
        Layer_stats writes .npz to
        {stats_dir}/{model_name}/{ds_name}_stats/
        {layer_name}_{precision}_{collectors}{size_suffix}.npz
        where size_suffix is "_t{batch_tokens}_{sample_size}"
        when batch_tokens < npos (typical Stage 1)
        or "_{sample_size}" otherwise. Conditions:
        P-6 applied; model_name passed in
        underscore form. Failure behavior: Cell 5
        Phase B R1.1 hard-halts on file-set
        mismatch.

IC-PreS26-3. layer_stats .npz file → Cell 5 Phase C
        / stage_1_sect Cell 3 internals consumer:
        Each .npz contains 4 keys per MEMIT
        runningstats.SecondMoment reflection
        convention: "mom2.constructor" (scalar
        string class identifier),
        "mom2.count" (scalar int64 token count),
        "mom2.mom2" (the (intermediate_size,
        intermediate_size) float32 matrix payload),
        "sample_size" (scalar int64 document
        count). Conditions: layer_stats invoked
        with to_collect=["mom2"]. Consumer
        obligations: resolve matrix via priority
        ["mom2.mom2", "mom2", non-metadata-fallback]
        with metadata exclusion ["sample_size",
        "n_samples", "samples", "mom2.constructor",
        "mom2.count"]. Failure behavior: shape=()
        scalar resolution if priority unhonored
        (observed this session at first Cell 5
        dispatch).

IC-PreS26-4. NV-stashed HF token discipline:
        huggingface-cli login with HF_HOME=
        /workspace/hf_cache (set in operator
        shell) writes token to
        /workspace/hf_cache/token, NV-resident
        across pod stops. Kernel-side consumers
        must export HF_TOKEN explicitly when
        huggingface_hub library was imported
        before token file existed (cached resolution
        does not re-read on call). Closes
        OQ-PreS26-10's persistence question.

═══════════════════════════════════════════════════
SESSION DELIVERABLE ARTIFACTS (NV-resident)
═══════════════════════════════════════════════════
/workspace/covariance_caches/meta-llama_Llama-3.1-8B/
   wikipedia_stats/
      PROVENANCE.txt                      (authoritative)
      model.layers.4.mlp.down_proj_float32_mom2_t100_100000.npz   (822 MB; sha256: 4ff31e8f28f252b6...)
      model.layers.5.mlp.down_proj_float32_mom2_t100_100000.npz   (822 MB; sha256: e73b2c3f2f5ec3ca...)
      model.layers.6.mlp.down_proj_float32_mom2_t100_100000.npz   (822 MB; sha256: c0b15be3d77b8c99...)
      model.layers.7.mlp.down_proj_float32_mom2_t100_100000.npz   (822 MB; sha256: d2a7b81667c8280b...)
      model.layers.8.mlp.down_proj_float32_mom2_t100_100000.npz   (822 MB; sha256: f3a7e66817575ff3...)

/workspace/architecture_profile/
      pre_s2_6_globals_fingerprint.json   (Cell 1.5 forensic)
      pre_s2_6_patch_state.json           (Cell 2 patch verification)
      pre_s2_6_revision_record.json       (Cell 3 Phase B revision SHA)
      pre_s2_6_layer_stats_log.json       (Cell 4 Phase 1 per-layer log)
      pre_s2_6_cache_verdict.json         (Cell 5 PASS verdict)

/workspace/memit_dry_run/memit/rome/layer_stats.py
      (P-6 NV-applied; markers verified Cell 2 + Cell 4 re-import)

═══════════════════════════════════════════════════
PATCHES APPLIED (final inventory)
═══════════════════════════════════════════════════
P-1   nethook retain_hook signature              (carry-forward)
P-2   nethook with_kwargs registration           (carry-forward)
P-4   config attribute fallback                  (carry-forward)
P-5   dataset loader modernization v1.0.1        (carry-forward, S2.5b)
P-6   layer_stats line 40 f-string fix           (NEW THIS SESSION)
Pad-Token alias                                  (kernel-resident; see IC-PreS26-3)

═══════════════════════════════════════════════════
INPUT REQUIRED FOR NEXT SESSION
═══════════════════════════════════════════════════
Session 2.6 (Stage 1 SECT execution) is now
unblocked. Pre-Session-2.6 hardening required:

1. stage_1_sect_runbook.md v1.1 → v1.2 revision.
   Required updates: (a) Cell 3 R1.1 file-set
   predicate must include "_t100_" segment per
   IC-PreS26-2; (b) Cell 3 .npz internals consumer
   must use "mom2.mom2" priority resolution per
   IC-PreS26-3. Closes OQ-PreS26-26 + OQ-PreS26-31
   canonical follow-up. Estimated authoring scope:
   ~30 min in S2.7 retrospective or as standalone
   pre-Session-2.6 task.

2. memit-patches-canonical.md v2.2.1 → v2.3
   amendment: add §3.7 P-6 specification matching
   §3.5 / §3.6 conventions. Closes OQ-PreS26-25
   canonical follow-up. Estimated authoring
   scope: ~30 min in S2.7 retrospective.

3. Optional pre-Session-2.6 OQ closure work
   (OQ-PreS26-9, -11, -13, -14, -29, -30): runbook
   v1.2.3 hardening pass. Operator may choose to
   defer to S2.7 retrospective if Session 2.6
   dispatch is time-pressured; carry-forward state
   intact via this summary block.

Pod state at session close:
- Hostname: aaaac25fb0da
- NV state: all session deliverable artifacts
  resident at canonical paths
- Container disk: ~12 GB used / 8 GB free
  (regrowth occurred during Cell 4 per OQ-PreS26-18;
  not blocking)
- model + tokenizer: kernel-resident on cuda:0
- Recommended: pod stop after PROVENANCE.txt and
  .npz files verified by operator (NV-persistent
  state survives stop; container-disk regrowth
  cleared on next start)

Pre-Session-2.6 disk hygiene reminder: `rm -rf
/root/.cache/huggingface` before Session 2.6
dispatch on fresh pod, OR ensure all six HF cache
env vars exported in Cell 0 BEFORE first
transformers/datasets import (per D-PreS26-10).

═══════════════════════════════════════════════════

Specialist provenance: memit-specialist (primary,
P-6 patch authoring + Cell 4 dispatch discipline);
state-consistency-theorist (secondary, Cell 5
PROVENANCE.txt + key-resolution reflection
convention); validation-contract-architect
(occasional, Cell 3.5 smoke as Reflexion-loop
probe + halt-class triage); framework-spec-writer
(this artifact).

═══════════════════════════════════════════════════
*— End of pre-S2.6 fork-work session summary block v2 —*
═══════════════════════════════════════════════════
