---
name: prior-art-sleeping-llm-2026
description: "Baranov 'Sleeping LLM' (2026): MEMIT wake writes + LoRA sleep; CONTEXT; replicates the single-prompt no-transfer gap; author later dropped MEMIT"
metadata:
  type: reference
---

Baranov (independent), Zenodo preprint 2026-02-25 (not peer reviewed), repo `vbario/sleeping-llm` HEAD 661057d. Wake = MEMIT write on one raw prompt, first object token only (`src/memory/memit.py:1190`, verified); sleep = rank-16 LoRA on chat Q&A, then per-fact MEMIT deltas scaled 1.0→0.5→0.1→0. Its own JSON (`experiments/results/sweep_consolidation_Llama-3.1-8B-Instruct.json`): raw recall 1.0, chat-template recall 0.0 right after writing at 5–20 facts — an independent replication of the C10 surface-form gap (Llama 8B, common cities). The author then dropped MEMIT entirely (`src/orchestrator.py:6`, verified: "MEMIT removed — facts … injected via system prompt"). No paraphrase, multi-token, invented-name or locality tests; KL fixed at 0.0625, never swept.

**Verdict CONTEXT** (note `results/prior_art_sleeping_llm_2026-10-06.md`). Usable ideas: (1) a template-shift read class (chat/question form) as a second held-out axis for the loop's candidates; (2) a matched-count preserve arm on other facts' last-token keys (its "Helena leak" fix, notes/53) as another control for the value-position preserve term; (3) lifecycle primitives — per-fact ledger, scalable/reversible deltas, snapshot/restore, and its audit that misread a deliberate scale-down as degradation — to seed a delete/update test. Related: [[prior-art-sweep-2026-10]], CORPUS/42–43.
