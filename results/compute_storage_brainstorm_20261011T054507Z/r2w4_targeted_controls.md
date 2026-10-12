R10D
RED R10D: exit 1: R10 verify-preflight admission-origin occurrence missing/merged: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10w_p2_stage.sh
GREEN mutation controls: 1 intended RED (0 preserved + 1 D13), zero filesystem writes
GREEN mutation controls: 1 intended RED (1 preserved + 0 D14), zero filesystem writes
GREEN mutation controls: 1 intended RED (1 preserved + 0 D15), zero filesystem writes
EXIT 0
R11A
RED R11A: exit 1: R11 loaded_data site filtered by argv stage: git-ls-files
GREEN mutation controls: 1 intended RED (0 preserved + 1 D14), zero filesystem writes
GREEN mutation controls: 1 intended RED (1 preserved + 0 D15), zero filesystem writes
EXIT 0
R11B
R11B fixture: P2 argv p2-shuf-s1; P3 certificate; linked/evidence/authorization prerequisites PASS; 6 mocked Git probes, no file writes or real Git/verifier launches; source reads/path resolution occur
RED R11B: exit 1: R11 reachable admission occurrence missing: verifier-descendant Git, p2-shuf-s1
GREEN mutation controls: 1 intended RED (0 preserved + 1 D14), zero filesystem writes
GREEN mutation controls: 1 intended RED (1 preserved + 0 D15), zero filesystem writes
EXIT 0
R11C
RED R11C: exit 1: R11 first-stage exclusion unpinned: gate:103
GREEN mutation controls: 1 intended RED (0 preserved + 1 D14), zero filesystem writes
GREEN mutation controls: 1 intended RED (1 preserved + 0 D15), zero filesystem writes
EXIT 0
R12A
GREEN D15 ADMISSION sites: count pinned_constant=37 loaded_data=6; operand-source pinned_literal=24 loaded_data=19
GREEN D15 SCIENCE sites: count pinned_constant=232 loaded_data=27; operand-source pinned_literal=107 loaded_data=152
R12A fixture: P2 argv/P3 certificate; upstream/link prerequisites PASS; seven distinct mocked Git probes before pinned validate_phase:333 raises; no writes or real Git/verifier launches; source reads/path resolution occur
RED R12A: exit 1: R12 loaded_data count represented by an unpinned constant: verifier-p3
GREEN mutation controls: 1 intended RED (0 preserved + 1 D15), zero filesystem writes
EXIT 0
R12B
GREEN D15 ADMISSION sites: count pinned_constant=37 loaded_data=6; operand-source pinned_literal=24 loaded_data=19
GREEN D15 SCIENCE sites: count pinned_constant=232 loaded_data=27; operand-source pinned_literal=107 loaded_data=152
R12B fixture: profile 38 p2-eval; eval.json earlier linked adapters versus last-existing train/*.json later adapters; 6 + 6 disjoint mocked Git operands; no writes or real Git/verifier launches; source reads/path resolution occur
RED R12B: exit 1: R12 routes merged without pinned pre-spawn operand equality: profile 38
GREEN mutation controls: 1 intended RED (0 preserved + 1 D15), zero filesystem writes
EXIT 0
R12C
GREEN D15 ADMISSION sites: count pinned_constant=37 loaded_data=6; operand-source pinned_literal=24 loaded_data=19
GREEN D15 SCIENCE sites: count pinned_constant=232 loaded_data=27; operand-source pinned_literal=107 loaded_data=152
RED R12C: exit 1: R12 count bound unpinned: gate-phase-trains
GREEN mutation controls: 1 intended RED (0 preserved + 1 D15), zero filesystem writes
EXIT 0
