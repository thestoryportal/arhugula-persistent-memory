# Integrated experiment queue — 2026-10-07 (D-C10r-rulings-9)

The single queue for C10 work after the operator's overnight directive of 2026-10-07 ~05:45 MDT ("use it as your integrated experiments along with any already queued"). It merges the research pass's final prioritised output with the items already queued. It runs nothing by itself; every run still needs its pre-registration, the advisor pass, the Codex pass and the LAWs.

## Source of the research list (verified against the transcripts)

- The research agent's final prioritised list is the sequence table it gave at 2026-10-06 18:13 UTC, in reply to the operator's request for a ranking "based on the discussed criteria" (writing to the model per the spec, runnable locally on the Mac, time cost). Saved as `results/research_pass_2026-10-06/recommended_sequence.md`. Transcript: research session c7841253, JSONL line 1062.
- The operator's 1–10 question came next (L1066). The agent's answer (L1070): **about 3/10** that one arm or a mix closes C10 on Qwen2.5-3B as a write; **4–5/10** with the model axis; **8/10** that the sequence advances the science durably. "What would move the first number most: step 5's result, and whether step 1 or 2 clears 30 on a second process."
- Two earlier tables carry the research sources and time costs per hypothesis: the write-only cost table (L1019, sources in brackets: MEMIT-XF, ManiEdit/AnyEdit++, LOKI, GenRecEdit, FOVEATED, DOW-KE, Moir, OverTone/FE) and the spec-fit × runnability ranking (L1029). The agent's wall-weighted re-rank (L1037): H-11, H-10/H-5, H-3, H-19, H-1, H-9, H-8, H-24, H-4, H-6, H-20.
- Search coverage: every OpenResearch session (dashboard DB and native transcripts, incl. the 11 helper-agent transcripts) and every program-session transcript, 98 JSONL files, 191.6 MB; no other prioritised table exists. Archive: `results/openresearch_archive/` (local only, gitignored; rebuild with `tools/openresearch_archive.py`).

## The queue

| order | item | research ref | status 2026-10-07 06:00 MDT | cost on the Mac |
|---|---|---|---|---|
| done | Step 1, shared target over three phrasings | H-1 (MEMIT-XF) | UNDERFIT ×2 (CORPUS/51, /52): inconclusive, solver fit gate missed | — |
| done | Step 2, second key inside the value | H-10 / H-5 (AnyEdit++, ManiEdit) | NULL-LARGE-WRITE (CORPUS/53): 23 vs 15/72, write ×2.05, spillover | — |
| 1 | Step 3, two minted tokens per value (+ modifier-only arm, V2 redraw) | H-19 | r1 HALTED at the LAW#3 multi envelope (10 vs [11, 18]); envelope amendment under Codex review; if approved, r2 from a fresh OUT_DIR | ≈ 6 h (measured ≈ 23 min per run) |
| 2 | Step 5, ceiling ("oracle") measurement: merged band-LoRA trained on the 24 facts, labelled a measurement, never a route | H-13 | moved ahead of step 4 (this ruling); prereg from `prereg_stubs.md` → advisor → Codex; implementation by Codex | 2–3 h run |
| 3 | Step 4, per-fact layer choice | H-8 (LOKI) | prereg v2 FROZEN (`docs/C10V_LAYERPICK_PREREG.md`); driver to be implemented | minutes + one run |
| 4 | Step 6, forward replay (I-2) and OverTone token reweighting (I-1) | H-11 (FE, OverTone) | build now, model-free, in parallel (this ruling); harness seams only, engine unmodified, LAW#5 inertness first | ≈ 1 day build each, one run each |
| 5 | Step 7, direct ΔW optimisation under the null-space projector | H-3 (DOW-KE) | build now, model-free, in parallel (this ruling); two same-seed runs for reproducibility | ≈ 1 day build, 1–2 h run |
| 6 | Step 8, covariance from the model's own text | H-4 (Moir) | queued; a GPU job, so it waits for a gap | hours unattended |
| 7 | Closed-form minted-row readout (no gradient) | H-18 variant | decide after step 3 reads (research open question 3) | one mint pass |
| gate A | Replicate any arm ≥ 30/72 in a second process before anything else | — | standing | one run |
| later | Look-ahead MTP head (H-24), subject anchors + carrier (H-9), position-separated gated write (H-6), constructed minted-row init (H-20) | H-24, H-9, H-6, H-20 | sequenced after the gates above | days |
| after ceiling | Model axis: Qwen2.5-7B (untied), MiMo-7B-Base (MTP), OLMo-2-7B | H-21, H-23, H-26 | gated by the Qwen ceiling rule (D-C10k-rulings-2) — operator's call | hours per model + covariance rebuild |

**Already-queued items kept in the queue (outside the research list):**
- Autoresearch loop relaunch (best 34/72, held-out paraphrase caveat): waits on graft hooks off in Claude Code sessions, the sealing probe of D-C10r-seal v3 + fix 1, the LAW#3 equivalence and a clean re-score.
- Q4_K_M survival of multi-token values (runbook next-action 4): after the first arm that passes.
- Closed-set read-confidence test (OpenJev-style; operator-suggested 2026-10-07): after step 4, scored separately from the binding open-generation metric.
- "Database + small typed model" comparator (BlendSQL, operator-supplied prior art): an F1 comparator, not scheduled.

## Order tonight

One GPU run at a time. GPU: step 3 r2 if the amendment passes review, else step 5 as soon as it is pre-registered and reviewed. In parallel without the GPU: Codex builds step 6 and step 7 drivers and the step-4 and step-5 drivers; the advisor and Codex review each before any run; CORPUS only after the verdict reviews.
