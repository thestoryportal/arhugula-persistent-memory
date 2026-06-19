S2.39 Kickoff — Positive-Control Calibration + High-AKD Confound Test (routing session)

Session type: Execution (pod-side). Diagnostic + routing. Produces NO viability verdict on any model — it produces (a) a calibrated positive control for the probe harness and (b) a routing decision that selects the next phase (model-hunt vs mechanism-hunt) for the LLM-as-Database backend search.

Why this session exists (the strategic frame):
The program to date is an ELIMINATION campaign — Llama STALL, Mistral STALL (both ceiling-class, back-loaded ineffective updates), Qwen CONVERGE-but-ENTANGLE (front-loaded L4, effective edit that corrupts same-subject biography, zero cross-entity leak). "A model that works for the spec" requires BOTH: (1) converges at compute_z (expresses the edit) AND (2) attribute-local (edits the target attribute without dragging unrelated same-subject attributes). NOTHING tested clears both. Before hunting for a model/mechanism that does, two preconditions are missing and this session buys them:
  - P1: a POSITIVE CONTROL. Every result so far is a fail condition; there is no (model,engine,fact) triple the harness has measured as a CLEAN attribute-local success. Without it, a quiet failure (edit expresses but drift-probes under-fire) is indistinguishable from a real success. We must measure the SHAPE of success before we can recognize it.
  - P2: a CORPUS the finding survives. All v1.7 numbers are cfb-v3 (5 clustered athletes, identical template) — a KNOWN MEMIT low-AKD key-collision stress regime (arXiv 2502.07322; flagged S2.24, OQ-S224-LIT-1 open). If Qwen entanglement is partly a low-AKD artifact, any hunt on cfb-v3 optimizes against a confound.

Predecessor: S2.38 — framework_finding v1.7 FINAL + v1.7.1 + v1.7.2 (consolidated, for human KB merge). 3-model weight-update-geometry control: front-loading is converger-specific; ceiling models back-loaded+ineffective; cross-entity specificity universal (KL=0 all three). Engine UNMODIFIED across S2.34-S2.38, SHA 5c0c706a…c78770.

Scope — three arms + one routing gate, in order:

ARM A — Positive control (GPT-J, MEMIT's home turf).
- Run MEMIT on EleutherAI/gpt-j-6B against a small set of CounterFact/zsRE-style facts the MEMIT paper validates on (NOT cfb-v3 athletes). Use the authors' canonical GPT-J hparams (layers 3-8, the S2.3 calibration config).
- Apply the SAME Probe-B harness used for Qwen in S2.36 (apply_memit_to_model + restore; measure intended-consistency, same-subject attribute drift, cross-entity specificity, per-layer update norms).
- GATE A (positive-control validity): the harness MUST register GPT-J edits as effective (p(target) high) AND attribute-local (low same-subject drift) AND entity-specific (cross-entity KL≈0) — i.e. reproduce the paper's "clean edit" shape. If GPT-J does NOT show a clean edit under our harness, the harness/probes are mis-calibrated → HALT and fix the instrument before any hunt. This is the calibration anchor: it defines what SUCCESS looks like on our instruments.

ARM B — High-AKD corpus authoring (contained authoring task; Claude authors fully, no placeholders).
- Author cfb-v4-highAKD.yaml + probe-set-v4-highAKD.yaml: 5 facts (matched count to cfb-v3 for clean comparison) with DISTINCT subjects across DISTINCT domains and VARIED templates (NOT one shared template) — the inverse of cfb-v3's clustered/low-AKD structure. Each fact gets: a consistency prompt, a generalization paraphrase, a cross-entity specificity control, and ≥3 same-subject biographical probes (the attribute-locality test). Target objects single-token where possible on BOTH Qwen and the GPT-J tokenizer; flag multi-token with first-token-proxy per established convention.
- Compute the AKD band-mean for cfb-v4 and confirm it is materially higher than cfb-v3 (reuse the S2.26 AKD metric; cfb-v3 band-mean ~4.62). Record the ratio.

ARM C — Qwen high-AKD re-run (the confound test).
- Re-run the S2.36 Qwen Probe-B (converge + entanglement) on cfb-v4-highAKD, matched config (band [4,5,6,7,8], v_loss_layer 27, z_layer 8; P-VRAM-CPU-SOLVE required).
- Measure the SAME quantities as v1.7 §X.2: intended post p(target), same-subject biographical drift (meanKL, frac-changed, target-leak), cross-entity specificity, per-layer update norms / front-loading.

ROUTING GATE (the deliverable that selects the next phase):
Compare Qwen entanglement on cfb-v4-highAKD vs cfb-v3:
  - ROUTE-MECHANISM: entanglement PERSISTS at high AKD (biographical drift KL still ≫0, front-loading still L4-peaked). → Entanglement is a MEMIT update-geometry property, not a corpus artifact. The spec needs a different WRITE MECHANISM (attribute-local by construction), not a different model. Next phase = mechanism-hunt (revisit GRACE adapter / alt-arch write engines / rank constraint). S2.40 = mechanism-hunt scoping.
  - ROUTE-MODEL: entanglement COLLAPSES at high AKD (drift KL → near specificity floor) BUT Llama/Mistral would still stall. → Entanglement was substantially a cfb-v3 low-AKD artifact; the model axis is clean. Next phase = model-hunt with the now-calibrated probe + trustworthy corpus. S2.40 = model-hunt candidate-set scoping (acquire/patch/cov candidates).
  - ROUTE-REREAD: high AKD materially changes the LLAMA STALL too (requires a confirmatory Llama cfb-v4 mini-run if Route signals point here). → The central architectural-invariant finding is corpus-dependent; HALT the hunt, re-read v1.7 before any further search. Highest-priority outcome to catch.

Read order:
- framework_finding_v1_7_consolidated.md (FINAL + v1.7.1 + v1.7.2 — the elimination state + entanglement mechanism this session tests for robustness)
- session_2_38 close artifacts / s236_qwen_multifact.json + s238_mistral_profile.json (the Qwen entanglement + 3-model numbers to compare against)
- cfb-v3.yaml + probe-set-v3.yaml (the low-AKD baseline corpus; authoring template + AKD anchor for cfb-v4)
- the existing high-AKD authoring precedent: cfb-v4-highAKD.yaml / probe-set-v4-highAKD.yaml IF present in KB from S2.25/S2.26 (REUSE if it exists and meets the spec above — do not re-author duplicatively; otherwise author fresh per Arm B)
- memit-patches-canonical v2.6 (P-VRAM-CPU-SOLVE live)
- llama_3_2_3b_baselines.json / s224 (the AKD metric + GPT-J calibration provenance for Arm A)

First actions at entry:
1. Engine fingerprint gate: grep -c "_cov_cpu" memit/memit_main.py = 3; SHA = 5c0c706a66c385273d0a48ebbb8274a1c31bf3e101ca309e47db9cb8b6c78770. Mismatch → HALT.
2. CHECK FOR EXISTING cfb-v4: the KB shows cfb-v4-highAKD.yaml + probe-set-v4-highAKD.yaml may already exist (S2.25). If present and conformant to Arm B spec (5 facts, distinct subjects, varied templates, ≥3 biographical probes each, AKD materially > cfb-v3), REUSE it and SKIP Arm B authoring — record the reuse decision. Only author fresh if absent or non-conformant.
3. Kernel hygiene: HF_HOME=/workspace/hf_cache before HF import; os.chdir(ENGINE_ROOT) before from memit import; clean kernel.
4. GPT-J cov caches: confirm /workspace/covariance_caches/EleutherAI_gpt-j-6B present (S2.3 symlink). If absent, Arm A cov compute (~per-layer) is in scope; budget for it.
5. Pad-token per model (GPT-J: check; Qwen: <|endoftext|> doubles as pad).

Deliverables at close:
- session_2_39_summary_block.md (with the explicit ROUTE-* decision and its evidence table)
- cfb-v4-highAKD.yaml + probe-set-v4-highAKD.yaml (if authored fresh; else reuse-record)
- s239_gptj_positive_control.json (Arm A — the calibrated success shape)
- s239_qwen_highAKD_proberun.json (Arm C — the confound-test numbers)
- s239_akd_comparison.json (cfb-v3 vs cfb-v4 band-mean ratio)
- framework_finding v1.8 (ADDITIVE, conditional): the positive-control calibration + the high-AKD confound result + the routing decision. Additive regardless of route; overturns nothing already promoted (but a ROUTE-REREAD result FLAGS v1.7 for re-examination — does not auto-amend it).
- session_2_40_kickoff.md (the next-phase kickoff, CONTENT SELECTED BY THE ROUTING GATE: mechanism-hunt scoping / model-hunt candidate-set / v1.7 re-read).

Correctness gates (CLAUDE.md law): engine fingerprint; GATE A positive-control validity (harness must register a clean GPT-J edit or HALT); determinism on any cross-session checkpoint; read-source-before-authoring for any new probe code; one-fix-then-halt; never promote past an unmet gate; never fabricate numbers.

Decisions carried: D-S233-MANIFEST-1 (manifest merge STILL DEFERRED — do not write to either divergent manifest; the human KB merge of v1.7 is the natural point to resolve it). D-S234-2 (per-arch canonical anchor is documented-not-corrected; the BOS off-by-one was a misdiagnosis — preserve comparability).

Specialist routing: memit-specialist (primary — write-engine + update geometry), validation-contract-architect (ACTIVE this session — positive-control + probe-validity is a validation-contract task), state-consistency-theorist (secondary — determinism), framework-spec-writer (corpus + finding authoring), graph-data-architect (consult — attribute-locality is a knowledge-representation property: what does "attribute-local write" mean for the triple schema).

Open decision surfaced for entry: Arm A facts. Recommend reusing 3-5 canonical CounterFact tuples the MEMIT paper reports clean edits on (subject/relation/target with known clean-edit behavior) rather than authoring novel GPT-J facts — the positive control is only valid against facts MEMIT is KNOWN to edit cleanly. If the exact paper tuples are not recoverable from KB, use the smoke-test fact lineage (Michael Jordan→baseball, the HC-2 canonical) which has a recorded clean-edit history in the manifest, plus 2-3 CounterFact-style additions. Resolve at entry; do not block.
