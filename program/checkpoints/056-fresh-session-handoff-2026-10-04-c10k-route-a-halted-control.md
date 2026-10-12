## FRESH SESSION HANDOFF - 2026-10-04 (C10K Route A HALTED — CONTROLS_NOT_RECOVERED; operator decision on the forward route)

**Start here after context reset.** Route A (the operator's choice after CORPUS/41) ran end to end on the M3 Pro under a prereg with three advisor-reviewed amendments: **D-C10k-route-a ⟨D-C10k-route-a@3b0be47e⟩** (CORPUS/42; `docs/C10K_ROUTEA_RESULT.md`). The ported official AnyEdit recovers the trained prompt (24/24 on every arm once the ridge is rescaled) and **never the paraphrases (0/72)**; the back-test shows why (keying at the last prompt token → ~0 hidden-state transfer at any ridge), and rescaling the ridge to write at all breaks locality. The AnyEdit-port route is HALTED on local hardware; C10 stays OPEN/BLOCKING.

**Prior art added today (operator-supplied):** `docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md` (relations decode linearly from the subject's last token; open-range name relations are not linear) and `docs/PRIOR_ART_ANYEDITPP_BAYES_CHUNK_2026.md` (long-form lineage keys inside the written context and scores BLEU on the trained prompt). Together they frame the result and the value-class split.

**The next step is an operator decision, not a run:** (i) pre-register the LRE-faithfulness admission test (recommended: local, cheap, predicts the value-class split; read Christ 2025, Choe 2025, "Keys to Robust Edits" first); (ii) subject-keyed per-token hybrid as a re-implementation; (iii) accept-bounded with coined multi-word values routed to the side-store.

**Local infra state:** fp32 on MPS works for 3B (Amendment 2); launcher enforces projector hash + key dtype; chain script in `tools/`; Command Line Tools still broken (prebuilt llama.cpp); backup launchd blocked by TCC until Removable Volumes access is granted.


