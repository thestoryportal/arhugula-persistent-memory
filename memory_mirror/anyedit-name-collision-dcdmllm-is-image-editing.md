---
name: anyedit-name-collision-dcdmllm-is-image-editing
description: "'AnyEdit' ambiguity: jianghoucheng/AnyEdit is the LLM-editing port target; DCDmllm/AnyEdit and RefEdit are image editing, not C10 evidence."
metadata:
  type: reference
---

The user-supplied `DCDmllm/AnyEdit` repo is CVPR image editing (`AnyEdit: Mastering Unified High-Quality Image Editing for Any Idea`), not LLM knowledge editing. The relevant C10 port target remains `jianghoucheng/AnyEdit` (`AlphaEdit_ARE`/`memit_ARE`). RefEdit is also image-editing. Always disambiguate AnyEdit repos before using them as C10 evidence or implementation targets.

Source: EV-6 (2026-06-26). `external_prior_art/AnyEdit` is the jianghoucheng clone (`git remote -v`).
