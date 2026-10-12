# Operator choices for the research-engine phase-1 build — 2026-10-11 ~04:31 UTC

Asked by MAESTRO34 in chat (AskUserQuestion), after the operator approved design.md (04:23:51Z) and Astra r1 returned GO-WITH-CONDITIONS (astra_r1_verdict.md). These settle design.md:264 (Neo4j hosting) and :266 (budget) for phase 1 only.

1. **Neo4j location.** Question: "Where should the connections database (Neo4j) run for the small first build?"
   Operator's answer: "On this Mac, free edition (Recommended)".
   Option text shown: install the free Neo4j Community edition with Homebrew (about 1 GB); its data lives on the memit disk; it runs only while we build or query; nothing leaves the Mac; easy to remove later.

2. **Resource budget.** Question: "How much of the Mac may the first build use without checking with you each time?"
   Operator's answer: "Small fixed cap, anytime (Recommended)".
   Option text shown: up to 5 GB of disk on memit, at most 2 GB of memory for Neo4j, background priority, no model or GPU use, and the database is shut down after each session.

Scope: phase 1 only. This does not approve deletions (operator exact-path approval still applies), spend, any model or GPU run, or work past phase 1 (Astra C9: expansion is a reviewed decision).
