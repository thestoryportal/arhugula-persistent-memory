You tune only edit.py to write the 24 public training facts into the model's MLP weights.
Read the read-only editor_runtime.py and train_facts.json for the supported runtime and all three training arms.
Evaluation inputs are sealed and out of scope. Do not seek, reconstruct, paraphrase, or author look-alikes of the evaluation prompts.
Use only the canonical training prompt, including diagnostics. Do not read the harness or the program checkout.
The editor exits after writing absolute changed tensors. A trusted independent scorer returns only the fixed 16 summary keys.
Every run shares 2700 seconds for top-level recipe setup and the three edits. Guards must all pass.
Run @FENCE@/run.sh as a bare background command. Read summary.json under runs/, or the summary output.
Use @FENCE@/kill_run.sh if a run exceeds 120 minutes. An infrastructure or audit halt means stop and report it.
The new cleaned baseline must be scored by the program session before the loop starts.
Historical results.tsv scores before reseal were partly test-adjacent. The new baseline is the reference.
After launch, record each recipe and its aggregate score in results.tsv. Describe knobs, not prompt text.
Results are candidates. Promotion requires a separate, pre-registered held-out set never used to select a recipe.
Never alter the fence, interpreter, engine, data, guards, profiles, launcher or sealed areas.
The repository's root entries are sealed. Edit the existing edit.py and results.tsv in place;
keep temporary files in .agent_capture/. Do not run graft, add an index, or change either ignore file.
