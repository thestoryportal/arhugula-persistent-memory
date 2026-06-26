---
title: AnyEdit default window collapses C10 A7
date: 2026-06-26
decision: D-C10h-anyedit-viability
---
Upstream AnyEdit uses `window_size=50`, but the C10 A7 coined-coined values tokenize to only 4-6 Qwen2.5 tokens (mean 5.5). With the upstream default, every C10 A7 value is one window, so it does not test the per-token/window rescue hypothesis. A C10 AnyEdit pilot must preregister a small-window primary condition, likely `window_size=1`, plus any default-window run only as a diagnostic.
