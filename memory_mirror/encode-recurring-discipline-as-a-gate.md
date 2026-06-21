---
name: encode-recurring-discipline-as-a-gate
description: "When a multi-item discipline keeps lapsing (or you're improving a process), the durable fix is a runnable exit-code GATE (a script the agent must pass), NOT more prose or a resolution to \"do better\" — prose norms that require checklist recall under load reliably fail"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f4d82a89-8dda-448d-8fc0-cf79fc2d6af9
---

The close-out drift this program hit (canonical trackers silently un-updated, operator had to catch it) was not a one-off lapse — it was the predictable failure of a **prose-only multi-item norm**. A checklist that lives in a doc and depends on the agent remembering all N items at the end of a long/fatigued session **will** get partially applied. Re-resolving to "be more thorough" does not fix it; the next long session lapses the same way.

**The durable pattern:** convert the norm into a **mechanical gate** — a small script that checks the invariant and **exits non-zero on any gap** — and wire it into the discipline as a hard step ("not done until ✅ ALL GREEN"). The program already does this for the things that matter (LAW#5 inertness gate, engine-fingerprint gate, `codex_context_guard` preflight); `tools/closeout_check.py` extends it to context close-out ([[closeout-gate-before-done]]).

**How to apply (proactively, not just reactively):**
- If you notice ANY recurring discipline lapsing — close-out, memory-mirroring, pre-flight, independence-review, persistence-verification — don't just re-document it. **Build the gate** (a script with a clear PASS/FAIL exit code) and wire it where the agent declares done. Standing-auth covers this infra ([[standing-auth-forward-requirements]]).
- A good gate is: one command, deterministic, fails-closed (red on doubt), self-documenting (`--list`/`--help`), and extended in ONE place when scope grows.
- Make passing the gate the agent's job, never the operator's. If the operator is asking "did you do X?", the missing artifact is a *gate*, not more willpower.
- Prose still states intent + rationale; the gate enforces it. Both, not either.
