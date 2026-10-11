---
name: codex-brief-handoff-file-narrow-reads
description: Codex briefs - put the context handoff in its own file, and cap reads to grep + short sed ranges for research tasks
metadata:
  type: feedback
---

Two Codex brief traps seen 2026-10-11 (MAESTRO45).

1. **Handoff in its own file.** codexr1i passed its acceptance (54/54), then obeyed the context stop by appending "## R1I HANDOFF" to its report. That pushed the report to 97 lines and failed a carried 90-line report test, so MAESTRO's rerun showed 53/54. MAESTRO moved the section verbatim to `RE/r1i_handoff.md` (a369d87f).
**Why:** a handoff written after acceptance silently invalidates any test over the file it lands in.
**How to apply:** in every brief, name a separate handoff file (`<RE>/<name>_handoff.md`), never the report or a tested artifact. Always rerun the tests yourself after a HANDOFF reply; never trust its pass count.

2. **Narrow reads for research/inventory tasks.** codexr2h (science-launch inventory) fell from 100% to 40% context in about 5 minutes by reading the gate's payload modules whole. Its successor brief allowed only `grep -n` plus `sed -n` ranges of at most 40 lines, and said "do not read any file whole".
**How to apply:** put that read cap in the first brief for any task that traces through code it does not edit.

Related: [[context-management-every-session]], [[read-handoff-before-launching-successor]], [[stop-open-ended-builder-self-audits]].
