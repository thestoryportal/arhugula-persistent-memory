---
name: c10-memit-knobs-failed-before-anyedit
description: MEMIT knob sweeps (band, strength, cov weight, layers) gave no lead for hard coined values (CORPUS/37-39); para_full binds, canon_full is diagnostic.
metadata:
  type: project
---

C10g closed the bounded pre-AnyEdit MEMIT knob pass for hard project-coined multi-word values: later band, widened band, edit-strength, low-cov-weight, and deep layer-count variants all failed to improve held-out A7 behavior; deep layers only improved canonical trained-prompt fit while collapsing controls. Do not present this as proof AnyEdit is necessary, only as no cheap MEMIT knob lead in this scoped Qwen2.5-3B/A7/N=24/1-seed run.

The two band knobs in detail: later `[8,12]` (D-C10e-bandknob, CORPUS/37) and widened `[4,12]` (D-C10f-band412, CORPUS/38) rescued neither A7 held-out `para_full`; the widened band worsened 11.1 → 6.9 while canon rose only 29.2 → 41.7 and controls stayed 90.3.

**Binding metric:** for C10 multi-token value fixes, held-out paraphrase full-sequence (`para_full`) binds and canonical trained-prompt full-sequence (`canon_full`) is diagnostic only. C10e's later band raised A7 canon 29.2 → 45.8 while held-out fell 13.9 → 5.6 — NO MATERIAL KNOB RESCUE, not partial closure.

Source: D-C10g-strengthlayers (2026-06-26), CORPUS/37–39.
