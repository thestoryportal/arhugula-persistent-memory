# Session 2.2 Entry Note — Procurement Execution and Kaggle Smoke Test

> **Workstream:** 1 — Empirical POC Scoping (post-v1.2 sealed spec)
> **Session:** 2.2 — Procurement Execution and Kaggle Smoke Test
> **Position in arc:** Opens after Session 2.1 (GPU procurement research, recommendations accepted). Last Stage 0 prep session before Stage 1 (MEMIT-COMPAT-PROTO-1) execution.
> **Primary skill:** `memit-specialist`
> **Secondary skill:** `aiSecOps-specialist` (Warden — for tenant isolation, audit posture verification, persistent state architecture)
> **Closes:** OQ-WS1-1 operational closure (Stage 0 GPU prerequisite); inherits operator-confirmed decisions from Session 2.1.

---

## Session Character — Read Before Beginning

This session is different in shape from Sessions 2.0, 2.1, and the earlier protocol-authoring sessions. Those produced **recommendation documents**. This session produces an **execution record** — a record of what was provisioned, what was tested, and whether the toolchain smoke test passed.

The work is hands-on. The session walks through:
- Account creation and verification on Kaggle and RunPod
- A toolchain smoke test on a free tier (Kaggle) before any paid provider activation
- Paid provider activation (RunPod Secure) with persistent storage provisioning
- Persistent state architecture for the multi-week POC
- A reproducibility manifest that anchors the eventual `architecture_profile.json`

The session does **not** produce a new specification. It produces operational artifacts (smoke test log, container image hash record, Network Volume layout) that feed into Stage 1.

## Operator Decisions Already Locked (Inherited from Session 2.1)

These are settled. Do not re-deliberate:

- **Production target:** LLaMA 3.1 8B (per Session 2.0)
- **Calibration baseline:** GPT-J 6B (per Session 2.0)
- **Primary procurement venue:** RunPod Secure Cloud RTX 4090 (24 GB) on-demand at $0.69/hr
- **Secondary cost-floor venue:** Vast.ai Secure DC RTX 4090 (only if RunPod capacity is tight)
- **Stage 2 sweep tier:** on-demand (no preemption)
- **Smoke test discipline:** Kaggle Notebooks first; no paid provider activated until smoke test passes
- **Persistent storage plan:** 100 GB Network Volume on RunPod (~$7/month) with weekly rsync to local Mac
- **Local archive endpoint:** existing 2020 Intel 16 GB MacBook Pro (rsync target only)
- **Apple Silicon:** rejected for the POC; revisit only post-POC

## KB Curation for This Session

The KB stays largely as it was for Session 2.1 — most of the protocol documents are still relevant because the smoke test exercises Stage 1 in miniature.

| Document | Role in this session |
|---|---|
| `memit-compat-proto-1.md` | **Primary input.** PF-1 through PF-6 pre-flight requirements; SECT, OP, CFB structure. The smoke test is a single-fact rehearsal of SECT. |
| `MEMIT_Target_Model_Recommendation__Survey_of_Eleven_Open-Weights_Candidates.md` | Per-model VRAM requirements (GPT-J 6B ≈12GB FP16, LLaMA 3.1 8B ≈16GB FP16). |
| `GPU_Procurement_for_LLM-as-Database_POC__Cloud_Rental_vs_Apple_Silicon_Analysis.md` | Recommended primary venue; Network Volume cost; container image guidance; smoke test protocol from §6. |
| `write-engine-poc-scope.md` | Stage 0 ownership boundary; smoke test fits inside Stage 0. |
| `poc-execution-plan-and-spec-revision-rule.md` | Reproducibility discipline; architecture_profile.json content-hash anchor. |
| `llm-as-database-v1_2-integrated-spec.md` | Appendix A deployment preconditions — single OS user, filesystem privacy, persistent storage. |

## Documents NOT in the KB for this session

- `memit-drift-proto-1.md`, `epsilon-calib-proto-1.md`, `compaction-probe-calib-proto-1.md`, `judge-calib-proto-1.md` — Stages 2 and 3 protocols. The smoke test is a Stage 1 rehearsal; downstream stages are not exercised in this session and their inclusion would expand scope. Re-add at Stage 1 kickoff.
- `llm-as-database-agent-harness-framework.md` — paradigm context. Not load-bearing for an execution session.
- `tension-map-v5.md` and `gap-backlog-v5.md` — neither has direct procurement-execution relevance.

## Tools Expected in This Session

- **Web search and web fetch** — for current container image versions, current MEMIT reference repository state (kmeng01/memit), current GPT-J 6B HuggingFace SHA, current published CounterFact reference numbers. Pricing was settled in Session 2.1; this session verifies current state of the toolchain artifacts themselves.
- **No code execution by Claude.** This session walks the operator through the steps; the operator runs the actual commands on their machine and on Kaggle / RunPod. Claude is the navigator, not the pilot.
- **Past conversation search** — may be useful for retrieving Session 2.1 specifics if they need to be reviewed.

## Output Discipline

The session produces an **execution record**, not a specification. Specifically:

1. **Smoke test verdict** — PASS / PARTIAL / FAIL with cited evidence.
2. **Reproducibility manifest** — pinned container image hash, MEMIT repo SHA, PyTorch version, GPT-J 6B checkpoint SHA, tokenizer SHA. This becomes the seed for `architecture_profile.json`.
3. **Persistent state directory layout** — on the Network Volume.
4. **Local rsync configuration** — between the Network Volume and the operator's MacBook Pro.
5. **Account state record** — Kaggle and RunPod account identifiers, billing alerts configured, Network Volume provisioned.

The session does **not**:
- Begin Stage 1 protocol execution. The smoke test is a single-fact rehearsal, not the full SECT (which is three counterfactual facts × three runs each).
- Draft the full `architecture_profile.json`. PF-1 (target layer range) and PF-3 (baseline perplexity) require execution time on the actual production target, which is Stage 1 work.
- Author the CFB v1 corpus. That's a separate Stage 0 sub-session (probe-set v1 and CFB v1 authorship sprint).
- Author probe-set v1. Same — separate Stage 0 sub-session.

## Stopping Conditions for This Session

The session ends successfully when:
- Smoke test executes and produces a PASS / PARTIAL / FAIL verdict against a published CounterFact reference.
- RunPod is provisioned (account, payment method, Network Volume).
- Persistent state directory layout exists on the Network Volume.
- Reproducibility manifest is recorded.
- Session Summary Block records what was done and what blocks Stage 1.

The session ends with a HALT (do not proceed to paid activation) if:
- Kaggle smoke test fails or returns ambiguous results. Halt forces a follow-up session to diagnose before any payment method touches RunPod.
- Verification surfaces a toolchain issue that affects the recommendation (e.g., MEMIT reference repo has a regression against current PyTorch; CounterFact reference number cannot be reproduced; GPT-J checkpoint download fails integrity check).

A halt is not a failure — it's the smoke test doing its job. The session re-opens once the issue is diagnosed.

---

*Entry note ends. The fresh session prompt follows in `session-2.2-prompt.md`.*
