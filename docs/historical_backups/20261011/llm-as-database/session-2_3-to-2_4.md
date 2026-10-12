# Session 2.3 → 2.4 Handoff Package

## Contents

| File | Size (approx) | Purpose |
|---|---|---|
| `reproducibility_manifest.json` | 8 KB | Pinned-version record from Session 2.3 close |
| `oq-s23-backlog-v2.md` | 24 KB | Updated open questions backlog (5 closed, 14 deferred, 19 total) |
| `session-2_3-summary-block.md` | 12 KB | Session 2.3 closure record (canonical input to 2.4) |
| `session-2_4-starter-prompt.md` | 18 KB | Prompt for Session 2.4 (CFB v1 + probe-set v1 authorship) |

## Quick Start for Session 2.4

1. Upload all four files to the project KB (replacing any older versions if present).
2. Verify the project KB contains the locked source documents from Session 2.3:
   - `llm-as-database-v1_2-integrated-spec.md`
   - `block-2-runpod-notebook.md`
   - `memit-patches-canonical.md`
   - `block-2-3-runbook-deltas.md`
3. Start Session 2.4 by pasting the contents of `session-2_4-starter-prompt.md` as the opening message.

## Artifact-by-Artifact Usage

### 1. `reproducibility_manifest.json`

**What it is:** The canonical pinned-version record covering Block 1 (Kaggle smoke test), Block 2 (RunPod dry-run + HC-2 PASS), and Block 3 (persistent state + rsync mirror). Ten top-level keys covering image digests, runtime versions, drift verdicts, NV state, mirror state, and session closure metadata.

**Where the canonical copy lives:** `/workspace/reproducibility_manifest.json` on RunPod NV `large_amethyst_wolverine`. The file in this handoff package is regenerated from the same data dictionary; content is structurally identical to the NV-side artifact but the md5 may differ by a few bytes due to JSON serialization whitespace (the NV-side md5 is `a8c524b00068225fcb6451926a195804`; the handoff-side md5 will differ slightly while structural content is bit-identical at the JSON-decoded level).

**When to use:** Reference whenever a Session 2.4+ decision depends on the calibration baseline, image digest, NV state, or HC-2 verdict provenance. The manifest is the canonical pinning record; subsequent sessions should not contradict its values.

**How to verify integrity:**
```bash
python3 -c "import json; m = json.load(open('reproducibility_manifest.json')); print(f'JSON valid; {len(m)} top-level keys')"
```
Expected: `JSON valid; 10 top-level keys`.

### 2. `oq-s23-backlog-v2.md`

**What it is:** The updated Session 2.3 OQ backlog. v2 supersedes v1: reflects 5 closures (OQ-S23-3, 12, 15, 17, 18) and 6 new entries surfaced during Block 3 execution (OQ-S23-14, 15, 16, 17, 18, 19).

**When to use:** Reference when scoping Session 2.4+ work. Section 22 (Forward-Routing Summary) shows which OQs apply to which downstream session.

**OQs directly applying to Session 2.4:**
- OQ-S23-6 (token-id source discipline) — applies during probe authorship
- OQ-S23-14 (duplicate notebook disposition) — low-priority cleanup decision

**OQs applying to Session 2.5:**
- OQ-S23-1 (billing alert granularity)
- OQ-S23-5 (HF cache location)
- OQ-S23-13 (Community Cloud authorization)
- OQ-S23-16 (SSH key registration timing)

### 3. `session-2_3-summary-block.md`

**What it is:** The standard-format closure record for Session 2.3. Contains 15 decisions, 12 constraints, the OQ summary table, 4 interface contracts (IC-S23-1 through IC-S23-4), and forward routing to Sessions 2.4 and 2.5.

**Where the canonical copy lives:** `/workspace/session_logs/session_2_3_summary_block.md` on NV (md5 `e4a7a3452dfd7ecd045f95758dcaa040`).

**When to use:** Read this first at Session 2.4 startup. It is the canonical input to the next agent. The decisions and constraints sections are operationally binding for Session 2.4 and downstream.

### 4. `session-2_4-starter-prompt.md`

**What it is:** The opening prompt to start Session 2.4. Follows the framework's standard prompt structure with `<session_context>`, `<task>`, `<inputs>`, `<corpus_v1_requirements>`, `<probe_set_v1_requirements>`, `<method>`, `<output_format>`, `<constraints>`, and `<stopping_rule>` sections, plus an orientation appendix.

**Skill invocations:** Primary `/validation-contract-architect`, secondary `/framework-spec-writer`, tertiary `/graph-data-architect` (only if CFB ontology surfaces tensions).

**Session 2.4 scope:**
- CFB v1 corpus authorship (3-10 facts in MEMIT input format)
- Probe-set v1 authorship (4 categories: consistency, generalization, specificity, unmount; minimum 7 probes per fact)
- OQ-S23-14 disposition (duplicate notebook cleanup)
- OQ-S23-6 token-id discipline (capture in-session or defer to 2.5)

**Session 2.4 expected wall time:** ~2 hours (90 min conversation + 30 min artifact authorship)
**Session 2.4 expected cost:** $0 (no pod) to ~$0.50 (temporary pod for token-id capture)

## Operator Action Checklist (Pre-Session 2.4)

- [ ] Upload all four files to the project KB
- [ ] Decide whether to retain or remove the Session 2.3 paused-state pod (`76226b7abdb5`); if no longer needed, terminate via RunPod console
- [ ] Run a final rsync to capture the NV-side Session Summary Block on the SSD mirror (optional but recommended):
  ```bash
  ~/scripts/rsync-runpod-mirror.sh 103.196.86.85 18591
  ```
  (Adjust IP/port if pod was redeployed.)
- [ ] When ready to start Session 2.4, paste contents of `session-2_4-starter-prompt.md` into a new chat session

## Post-Session 2.4 Expectation

After Session 2.4 closes, the next handoff package will include:
- `cfb-v1.yaml` (or `.json`)
- `probe-set-v1.yaml` (or `.json`)
- `session-2_4-summary-block.md`
- Updated `oq-s23-backlog-v3.md` reflecting Session 2.4 closures (OQ-S23-6, OQ-S23-14)
- `session-2_5-starter-prompt.md` for Stage 1 SECT execution prep + LLaMA 3.1 8B target model commitment

## Provenance

- **Generated by:** Session 2.3 closure agent (Claude)
- **Generated at:** 2026-04-28 ~22:45 UTC
- **Session 2.3 closure md5s:**
  - Reproducibility manifest (NV-side canonical): `a8c524b00068225fcb6451926a195804`
  - Block 2 verdict (NV-side canonical): `df07173f7490556468d26a3f8a5e8e77`
  - Session Summary Block (NV-side canonical): `e4a7a3452dfd7ecd045f95758dcaa040`
