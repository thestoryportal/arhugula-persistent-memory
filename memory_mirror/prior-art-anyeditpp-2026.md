---
name: prior-art-anyeditpp-2026
description: "AnyEdit++ (arXiv 2606.01053): surprisal-chunked long-form edits; its BLEU metric is a canonical read, not held-out paraphrase"
metadata:
  type: reference
---

**Paper:** https://arxiv.org/html/2606.01053v1 · code github.com/TianSuya/Bayes-Chunk · Llama-3.1-8B-Instruct, Llama-2-7B, Qwen2.5-7B-Instruct; EditEverything/CounterFact/UnKE/QwQ-Edit; BLEU 77.74 vs AnyEdit 74.19 on EditEverything. Repo note: `docs/PRIOR_ART_ANYEDITPP_BAYES_CHUNK_2026.md` (§3 = Connected Papers bib triage; `~/Downloads/ConnectedPapers-for-AnyEdit++…bib`).

**Core:** segment the target text at surprisal peaks (`k = ⌈L/40⌉`), inject each edit at the token *preceding* a boundary; MEMIT-style solve with covariance ridge + preservation term. No paraphrase-generalisation or locality numbers reported.

**Why it matters here:** the whole long-form lineage (AnyEdit, AnyEdit++) keys writes at positions inside/at the end of the written context, never the subject token, and scores BLEU on the edited prompt = the program's *canonical* read. The program's binding criterion is held-out-paraphrase `para_full`, which Route A's faithful port scored 0/72 on. So porting long-form editors could not close C10 even if their numbers transferred. "Keys to Robust Edits" (arXiv 2410.09338) was read in the 2026-10-06 research pass (`results/research_pass_2026-10-06/dispositions.md:16`). See [[prior-art-lre-hernandez-2024]], CORPUS/42.
