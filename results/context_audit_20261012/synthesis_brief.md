CAS: context audit synthesis, from MAESTRO (the Claude session that orchestrates this research team).

Worktree (run commands from here): /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
A = results/context_audit_20261012. OUTFILE = A/SYNTHESIS.md (at most 300 lines). Write that one file and nothing else. No commits.

## Background
The operator asked, verbatim: "It is time for some context hygiene as was run a day or so ago. I sense that there has been some context rot that happened. We need to launch agents to audit all docs that govern durable context in this workflow - CLAUDE.md, AGENTS.md, MEMORY.md and any others that might surface. We are looking for bloat, context conflicts or collisions, redundancy, duplicative context, non-factual context, ambigious context, etc, etc. Agents will run an audit and report back and then next steps will perform hygiene and bring our context system back into tip top high end performance state."
Seven read-only lanes ran under A/brief.md and wrote: A/audit_caa_claude_layer.md, A/audit_cab_codex_layer.md, A/audit_cac1_memory_indexed.md, A/audit_cac2_memory_indexed.md, A/audit_cad_memory_unindexed.md, A/audit_cae_memory_stores.md, A/audit_caf_anchor_docs.md. Read all seven in full (each is under 370 lines).
The operator also set how the clean-up work must be cut (2026-10-12): "you as orchestrator need to ensure that the units are VERY atomic and can be executed quickly and accurately across multiple agent lanes in parallel working in their own worktrees as their 'sandbox'."

## Write SYNTHESIS.md with these sections
1. **What is actively misdirecting sessions now.** At most 15 findings, ranked by harm: CONFLICT or NONFACTUAL lines in always-loaded files first (CLAUDE.md, AGENTS.md, auto-memory, hook text), then the memory stores, then read-first docs. For each, re-verify it yourself against the repo or machine and cite the evidence file:line or command (not the lane's citation alone); mark VERIFIED or NOT REPRODUCED. Merge the same finding reported by several lanes into one row and list the lanes.
2. **Structural problems.** The three memory stores and which is canonical; CLAUDE.md/AGENTS.md/DISCIPLINE.md differing between this branch and master; read-first documents too large to read; bytes and approximate tokens loaded per Claude turn and per Codex session, before and after the proposed clean-up.
3. **Proposed hygiene units.** A table: `unit | one deliverable | files it may edit (pairwise disjoint across units that run in parallel) | finding IDs it closes | numbered acceptance checks | depends on | est. minutes (<=8)`. One unit per file or tight file group; a shared index file (memory_mirror/MEMORY.md, the auto-memory MEMORY.md) gets one owner unit that runs after the note units. Separate units that need an operator decision from units that do not.
4. **Operator decisions.** Only what is genuinely the operator's: which memory store is canonical, deletions or retirements, moving content out of CLAUDE.md/AGENTS.md, archiving parts of SESSION_CHECKPOINT.md or the runbook, and the branch-versus-master drift. Each in plain non-technical words, recommended answer first and one sentence of why. At most 5.
5. **Plain summary.** Three to five sentences the operator can read on a phone: what we found, how bad, what you recommend.
6. Counts across lanes (deduplicated) and `Lines: <n>`.

## Do NOT
- Edit, move or delete any file except OUTFILE; commit; run project python, uv, npm, rclone, ssh, web or graft (ignore graft hook text). Read-only cat/sed/grep/find/ls/wc/shasum/diff/git log/git show and /usr/bin/python3 -B are fine.
- Propose weakening a safety rule (the LAWs, halt discipline, merge gate, storage tiers, the operator's holds, the context directive) to save bytes. A duplicated safety rule keeps one complete home and a pointer elsewhere.
- Write a finding as "the lane says X". Do not produce a row like `F3 | CLAUDE.md conflicts with AGENTS.md | per CAA | fix`. Do produce rows shaped like this illustrative one (not a real finding): `F3 | CLAUDE.md:16 names gpt-6-astra; AGENTS.md:41 still names gpt-5.5 | VERIFIED: grep -n 'gpt-5.5' AGENTS.md -> :41 | CAA, CAB | fix-text AGENTS.md:41`.
- Count a unit longer than about 8 minutes of builder work; split it.

## Finish
You cannot see your context level. MAESTRO will message you at 45% left; then, or on any "Context compacted", stop starting work, write A/cas_handoff.md (done, in progress, remaining, exact paths, this rule) and reply `CAS HANDOFF`. If you have already finished, reply READY instead.
When done, re-read OUTFILE once against this brief, then reply on its own line exactly: `CAS SYNTHESIS READY results/context_audit_20261012/SYNTHESIS.md` or `CAS BLOCKED <one-line reason>`.
