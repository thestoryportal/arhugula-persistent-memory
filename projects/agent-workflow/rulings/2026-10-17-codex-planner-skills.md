# Operator ruling: complementary Codex skills for the Codex planner seats (2026-10-17, chat, verbatim)

"No, install skills in Codex that can run that are different but compliemntqry to the CLaude agent's skills"

Install approval, same day, answer to MAESTRO's install question: "Vet's 3 picks (Recommended)".

## What was installed (2026-10-17, MAESTRO)
Pinned copies in `~/.codex/skills/`, not symlinks:
- `statistical-power` and `experimental-design` from K-Dense-AI/scientific-agent-skills @ a1043ef5. Edits: the "Citing Scientific Agent Skills" block (vendor citation plus an arXiv fetch) removed from both SKILL.md files; statistical-power SKILL.md "Run from `skills/statistical-power/scripts/`" changed to the skill's own `scripts/` folder.
- `icm-architect` from the local clone of RinDig/icm-architect @ e16cafe6 (clean): SKILL.md, LICENSE, references/, assets/templates/.
Staged bytes matched 40/40 pinned git blob hashes before the edits. Post-install sha256 of every file: `/Volumes/memit/agent-workflow-evals/planning/tools/codex-skills-installed-20261017.sha256` (27 files). `codex debug prompt-input` lists all three.

## Not installed
- `benchflow-experiment-review` (benchflow-ai/benchflow @ 9c7a1918): its artifact validator fits only Benchflow runs. Its reward-hacking patterns, verifier-hardening checklist and skill-leakage marker list are ideas for the harness docs.
- `icm-workspace`: by its own scope it works only on `stages/` trees; this repo has none.

## Limits recorded for the planners (brief section 6)
statistical-power has no paired-binary (McNemar) method; experimental-design is written for human and lab trials (for agents, carry-over is leakage, and the ticket is the replicate); icm-architect assumes `stages/` and a single agent. The skills make `.venv-*` in the current folder, so planners run their scripts outside this repo.
