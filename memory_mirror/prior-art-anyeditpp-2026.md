---
name: prior-art-anyeditpp-2026
description: "Operator-supplied prior art (2026-10-04): AnyEdit++ (Tian et al., arXiv 2606.01053, May 2026) — surprisal-located write positions inside the target text; long-form lineage metrics (BLEU/BERTScore on the edited prompt) do not measure held-out-paraphrase correctness"
metadata:
  node_type: memory
  type: reference
  originSessionId: 4d71207f-24bf-4199-894f-d2f977d9f609
  modified: 2026-10-04T21:42:55.799Z
---

**Paper:** https://arxiv.org/html/2606.01053v1 · code github.com/TianSuya/Bayes-Chunk · Llama-3.1-8B-Instruct, Llama-2-7B, Qwen2.5-7B-Instruct; EditEverything/CounterFact/UnKE/QwQ-Edit; BLEU 77.74 vs AnyEdit 74.19 on EditEverything. Repo note: `docs/PRIOR_ART_ANYEDITPP_BAYES_CHUNK_2026.md` (§3 = Connected Papers bib triage; `~/Downloads/ConnectedPapers-for-AnyEdit++…bib`).

**Core:** segment the target text at surprisal peaks (`k = ⌈L/40⌉`), inject each edit at the token *preceding* a boundary; MEMIT-style solve with covariance ridge + preservation term. No paraphrase-generalisation or locality numbers reported.

**Why it matters here:** the whole long-form lineage (AnyEdit, AnyEdit++) keys writes at positions inside/at the end of the written context, never the subject token, and scores BLEU on the edited prompt = the program's *canonical* read. The program's binding criterion is held-out-paraphrase `para_full`, which Route A's faithful port scored 0/72 on. So porting long-form editors could not close C10 even if their numbers transferred. Read "Keys to Robust Edits" (2024) before any next keying decision. See [[prior-art-lre-hernandez-2024]], [[c10k-route-a-resume]].
