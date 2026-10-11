---
name: trim-builder-reading-lists
description: A long reading list in a Codex build brief spends the context the build needs; give exact line ranges, or split reading and building into two sessions
metadata:
  type: feedback
---
Keep a build brief's reading list to the exact sections the criteria need, with line ranges. When the needed reading is large, split the work: one session reads and writes a short findings file; a fresh session builds from that file.

**Why:** 2026-10-10, MB23's NEW-1 FIX5 brief listed four reading items (Astra r5 §1–3, the MB19 audit from line 366, the scope revision, four source ranges). The reading pass alone took MB23 from 100% to 64% context before its first edit, so a mid-build handoff became likely under the 40% stop rule.

**How to apply:** estimate the reading cost before sending a brief. A builder should start its first edit above ~75% left. See [[context-management-every-session]] and [[test-first-one-round-builds]].

**Web-research briefs burn faster still (MAESTRO41, 2026-10-11):** codexs1m went 100% → 42% in ~3 min and codexfs1 100% → 37% in ~6 min, both on GPT-6.1-Sol research with browsing; codexr1c hit 44% in 16 min on a 399-line script + 1,500-line JSON. For a research brief, cap the sources (e.g. "at most 8 pages; cite and move on"), have it write the report skeleton first and fill it as it goes, and expect to send the ≤45% stop within minutes — arm the watcher before anything else.
