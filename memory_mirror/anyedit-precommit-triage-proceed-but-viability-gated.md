---
title: AnyEdit triage: proceed, but viability-gated
date: 2026-06-26
decision: D-C10h-anyedit-triage
---
Advisor-review returned PROCEED for AnyEdit as the next C10 falsifier, not as a fix. Code triage prefers AnyEdit over FABLE: official AnyEdit has AlphaEdit_ARE/MEMIT_ARE and a per-token/window loop, but old deps/A100 assumptions and Qwen hparam mismatches mean it must be transplanted into the local Qwen2.5-3B harness with MEMIT primitives preserved and LAW#5 passing. FABLE is a heavier fallback; AnyEdit++ is a paper-only risk note. The pilot must be A7 plus A1/A2 held-out full-sequence first.
