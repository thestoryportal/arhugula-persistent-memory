GO-WITH-FIXES

1. **CLAUDE.md:9:** “; MAESTRO's regular work remains on master: its branch is merged into master through the merge gate (§ Merging), and the folder is removed with operator approval once nothing runs in it.” → “. MAESTRO's regular work remains on master. Builder branches are merged into master through the merge gate (§ Merging); worktree folders are removed with operator approval once nothing runs in them.” Reason: removes the ambiguous branch antecedent and distinguishes builder branches from the integration worktree.

2. **DISCIPLINE.md:50:** “Run it as the LAST step before declaring done / writing the checkpoint.” → “Update the checkpoint and all required trackers, then run it as the LAST step before declaring done; rerun it after any subsequent tracker edit.” Reason: the binding rule still contradicts the corrected closeout note.

3. **DISCIPLINE.md:86:** “**MANDATORY** as the LAST step of every experiment close, before declaring done / writing `SESSION_CHECKPOINT.md`.” → “**MANDATORY** after updating `SESSION_CHECKPOINT.md` and all required trackers, as the LAST step before declaring done; rerun after any subsequent tracker edit.” Reason: reconciles the second binding occurrence without weakening the gate.

4. **tools/closeout_check.py:5–6:** “Run at experiment
close BEFORE declaring done / writing SESSION_CHECKPOINT.” → “Run at experiment
close AFTER updating SESSION_CHECKPOINT and all required trackers, BEFORE declaring done; rerun after any subsequent tracker edit.” Reason: the checker’s own instructions contradict its requirement to inspect the updated checkpoint.

🌱 graft savings unreported (1 failed call).