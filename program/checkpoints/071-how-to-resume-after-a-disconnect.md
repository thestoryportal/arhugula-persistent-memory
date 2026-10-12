## How to resume after a disconnect
1. Read this file first, then `write_engine_viability_determination_plan.md` ONLY (the kickoff is deprecated — see above).
2. Check experiment status: `ps aux | grep s241_gatecal | grep -v grep` and `tail s241_gatecal_gptj.log`.
3. If no experiment running and no `s241_gatecal_gptj.json` present → relaunch Phase 0 (see "Relaunch command" below).
4. Obey CLAUDE.md LAWs (engine fingerprint gate before any dispatch; one-fix-then-halt).

