# Equip 4: eval skills on skills.sh (find and vet; install nothing)

Read M/projects/agent-workflow/brief/equip-common.md first.

Output: M/projects/agent-workflow/drafts/research/skills-sh-candidates.md

1. How skills are found here: read the local find-skills skill (`find ~/.claude -name SKILL.md -path '*find-skills*'`) and the skill-creator skills (`find ~/.claude -name SKILL.md -path '*skill-creator*'`). Report how each finds or installs skills, and whether skill-creator connects to skills.sh (cite lines). Check whether the `skills` CLI works without installing: `npx --no-install skills --help` (report the output; if it is not cached, say so; do NOT install).
2. Search skills.sh (https://skills.sh, its search or leaderboard pages; and the GitHub repos the listings point to) for skills about: agent evals, LLM evals, promptfoo, eval harness, graders or LLM-as-judge, benchmark design, test-scenario generation, context engineering, agent memory, marimo, trajectory analysis.
3. For each candidate (at most 15, best first): name, skills.sh URL, source GitHub repo and owner, install count or stars if shown, last update date, license, what its SKILL.md says it does (quote the description; read the SKILL.md on GitHub), files it ships (scripts? network calls? anything that runs code), and a `Vet:` line: what a reviewer must check before install (scripts that run, network access, prompt-injection text, scope overlap with a local skill). Mark the owner as verified only if skills.sh or GitHub shows it.
4. `## Recommendation inputs`: which candidates overlap local skills already installed (list both), and which fill a gap (INFERENCE). Do not recommend installing; MAESTRO decides after vetting.
