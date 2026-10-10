---
name: operator-decision-scope
description: "Operator feedback 2026-10-06: bring only go/no-go and scope decisions; decide design details (word lists, thresholds, which variant to test) with the advisor and Codex, and explain any decision I do bring in plain words with a recommendation."
metadata:
  node_type: memory
  type: feedback
  originSessionId: bd4ad540-d884-4208-bde1-877dc5cc906f
  modified: 2026-10-06T20:32:26.789Z
---

**Feedback (2026-10-06, after the route-call list):** "You figure out the list of words based on the research, consulting advisor and/or Codex. Don't bring those types of questions to me please, use the tools and resources you clearly have available to you... I do not have thoughts or the depth of knowledge to make those decisions." Two of the items I brought ("accept a redrawn value set", "standing of steps 6–7") landed with no context and were answered "I have no idea what any of that means".

**Why:** the operator is an architect with no ML background ([[operator-profile-and-standing-directive]]); design-level choices are mine to make with the reviewers; their scarce signal should be spent on go/no-go, GPU allocation, scope changes, and anything irreversible or outward-facing.

**How to apply:** (1) Resolve design choices (stimulus sets, thresholds, controls, which variant) with the advisor pass + Codex and record them as my decisions with a D-ID; (2) when something genuinely needs the operator (a run, a scope change, a rule change), present it in plain words with the recommendation first and one yes/no; (3) when they say "both" or "do it", that is the ruling — record it and proceed. Related: [[plain-language-to-operator]], [[c10k-route-a-resume]].
