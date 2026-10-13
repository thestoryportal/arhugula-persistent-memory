---
name: seed-freezes-context-templates
description: Seeding torch before MEMIT samples context templates freezes one draw (seed 0 → set e8605172, A7 40/7/7, below LAW#3); pin templates to a file
metadata:
  type: project
---
2026-10-08: ASTRA (C10Z) process 1 HALTED-V4 with recipe A A7 first 40 ∉ [42,59]. The harness was correct: the driver ran torch.manual_seed(0) before c10e_bandknob, and the engine's get_context_templates (`memit_dry_run/memit/memit/memit_main.py:304–323`) samples templates, so seed 0 always draws set e8605172dce0, whose recorded baseline is exactly 40/7/7, A1/A2 69 (autoresearch 2026-10-06, bitwise-equal across processes). The LAW#3 envelope (CORPUS/44:39) came from ~13 unseeded draws (A7 first 45–56).

**Why:** a fixed seed turns template variance into a fixed, possibly unlucky comparator; the envelope then no longer describes the run.

**How to apply:** every driver must pin its context templates to a recorded file (C10U/C10V/C10Q precedent; ASTRA now pins C10Q c7dabbe7c25a, D-C10z-v4fix), write context_templates.json before the LAW#3 gate, and its benchmark and run must use the same set. Never fix a V4 miss by trying seeds or widening the envelope after seeing the miss. Related: [[rerun-never-patch]], [[c10w-ceiling-oracle-result]].

**Related method facts (from the 2026-10-06/07 C10 runs):** because templates are sampled per process (`get_context_templates` → `generate_fast`), the unseeded A7 held-out baseline spans about 8–16/72 across processes (per-process spread ±4–5/72); mint arms spread ±4 across processes but 12 across seeds; `torch.pca_lowrank` is unseeded, so a saved init tensor (not the recipe) is the artefact (CORPUS/45:81); an edited fp16 Qwen2.5-3B save is 5.9 GB (CORPUS/45:81); the injection control is a reporting stratum, not a floor ([[injection-control-is-a-stratum-not-a-floor]]).
