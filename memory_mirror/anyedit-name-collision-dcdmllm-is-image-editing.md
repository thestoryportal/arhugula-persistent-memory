---
title: AnyEdit name collision: DCDmllm is image editing
date: 2026-06-26
decision: EV-6
---
The user-supplied `DCDmllm/AnyEdit` repo is CVPR image editing (`AnyEdit: Mastering Unified High-Quality Image Editing for Any Idea`), not LLM knowledge editing. The relevant C10 port target remains `jianghoucheng/AnyEdit` (`AlphaEdit_ARE`/`memit_ARE`). RefEdit is also image-editing. Always disambiguate AnyEdit repos before using them as C10 evidence or implementation targets.
