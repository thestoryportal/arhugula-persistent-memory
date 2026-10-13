# BK1 successor handoff

The authoritative latest handoff is the final BK1 HANDOFF section in progress.md.

## BK1 HANDOFF — 2026-10-11T08:56:46.677270+00:00

MAESTRO explicitly stopped new steps at approximately 44% context left. All current commands have finished; no audit process remains running. **audit_report.md is NOT written; the audit is NOT complete.**

### Steps done and exact outputs

1. Worktree verified at `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a` on branch `worktree-c10k-route-a`. Initial HEAD `d164bffa92c13000c3b5f27885a4f05fa5264ca3`; history-index HEAD `f2d4c5f24eebd2be74d88b2ba7c1fedd85648323`; most recent observed HEAD `17d45fbdd0e032c1910146099274f3c0311df993`. MAESTRO committed concurrently; branch did not switch. Existing tracked modification `tools/test_dashboard_mathlab.py` left untouched. BK1 wrote only this audit output folder and performed no git mutation, import, model/experiment, deletion outside output, or tmux action.
2. Volume-wide filename/stat census: `census.json`, all top-level directories traversed without following directory symlinks and excluding the four operator OS folders. **519,596 non-caselaw file entries** reconciled as 519,336 regular files + 260 file symlinks. Root 317 files; llm-as-database 170; stale archive 3. Both Drive folders are Story Portal logos/Burning Book video assets; `arhugula-vm-data` empty. Census was an inline metadata script; if needing strict rerun provenance, save that census code into scripts/ before rerunning (not saved yet).
3. Regular-file SHA256 and actual `git hash-object --no-filters --stdin-paths` inventory COMPLETE: `inventory.tsv` originally 519,336 regular rows and 18,086,613,160 bytes. Script `scripts/inventory.py`, receipt `inventory_complete.json`, `inventory_run.log`, `inventory_state.json`, `inventory_errors.json`. **Do not rerun inventory.py or --resume:** the initial inventory is complete and has since received the symlink supplement. inventory_state.json deliberately still says running; inventory_complete.json is the completion authority for the initial regular-file pass.
4. Symlink supplement COMPLETE: `scripts/symlink_supplement.py`, `symlinks.tsv`, `symlink_state.json`. Appended all 260 file symlinks to inventory.tsv: 207 readable referents hashed with SHA256 and actual `git hash-object --no-filters <symlink>`, 53 dangling/nonfile targets with blank hashes because there are no referent bytes. Final inventory rows **519596**. Symlink row bytes/mtime describe the referent when readable; symlinks.tsv separately preserves link-target text and lstat bytes/mtime. Dangling row bytes/mtime are link metadata. These are explicit hash exceptions, NOT exact/unique judgments. They are tooling/environment links, not identified scientific artifacts. **Do not rerun symlink_supplement.py:** it appends once and then correctly refuses an existing supplement.
5. Caselaw metadata/name-only census COMPLETE: `scripts/caselaw_summary.py`, `caselaw_summary.txt`: 41,442 files, 82,397,163,971 bytes; per-directory direct counts and bytes plus a name sample. No caselaw file contents read or hashed. Directory names look like legal reporters. Strong-name signal scan across ALL caselaw filenames was not separately saved; add it if needed to strengthen unrelated determination, without reading contents.
6. Reachable all-ref history index COMPLETE: `scripts/history_index.py`, `history_blobs.tsv` (14,697 blobs), `history_paths.json` (18,055 paths), `history_refs.txt`, `history_state.json`, `history_run.log`. 20,367 total objects. Uses required rev-list --all --objects -> cat-file --batch-check pipeline. Scope excludes unreachable/reflog-only commits. Frozen blob set is at the recorded f2d4c5f2 HEAD/refs. Do not rerun history_index.py into existing files: it uses exclusive-create. If a newer snapshot is required, create a separate subfolder within this audit folder, within disk budget.
7. Name-only search of `/Volumes/memit/llm-database-poc-mirror` + all historical basenames COMPLETE: `scripts/name_index.py`, `name_index.json`, `name_index_state.json`, `name_index_run.log`. `blob_locations.json` comes from all-ref raw git log and records commit+path holding each added blob. It was rebuilt after refined candidates existed; history blob set and raw locations were collected at slightly different times during concurrent commits. The demonstrated control commit/path is verified by ls-tree; remaining EXACT commit/path receipts should be batch-verified before final claims. Name traversal does not follow directory symlinks. Four root repo directory links exist: covariance_caches, hf_cache, external_prior_art, .venv; physically present files under their targets were encountered elsewhere under the mirror, but working-tree alias paths were not added. No bulk file reads were used for name discovery.
8. Seed relevance then reasoned refinement COMPLETE AS TRIAGE: `classification.tsv` / `candidates.tsv` are raw keyword triage (contains false positives); `scripts/refine.py`, `classification_refined.tsv.gz`, `candidates_refined.tsv`, `classification_state.json`, `reason_codes.json` are refined triage: **292 program, 10,029 adjacent, 509,015 unrelated regular files**. These refined files were generated BEFORE the 260 symlink rows were appended; rerun refine.py first so every final inventory row has classification. Expected unrelated adds 260; verify empirically. Refined program breakdown: root 114, llm-as-database 170, stale archive 3, five HTML files under agent-deployment-framework/.superpowers/brainstorm/fallback. `root_previews.txt` stores title/heading snippets from loose text documents; the inline preview code still needs to be retained as a rerunnable script if used in final audit.
9. EXACT/SAME-NAME matching COMPLETE AS TRIAGE: `scripts/match_files.py`, `matches.tsv`, `match_details.json`, `content_pending.json`, `match_state.json`, `match_run.log`. Counts: {"adjacent|CONTENT-PENDING": 8813, "adjacent|EXACT": 49, "adjacent|SAME-NAME": 1167, "program|CONTENT-PENDING": 140, "program|EXACT": 94, "program|SAME-NAME": 58}. 143 historical EXACT in total (94 program, 49 adjacent); 1,225 SAME-NAME (58 program, 1,167 adjacent); 8,953 CONTENT-PENDING (140 program, 8,813 adjacent). The 53 dangling symlinks do not flow into the matcher as candidates under current refinement. **No UNIQUE verdict has been made.**
10. Required real positive control PASSED: `scripts/positive_control.py` calls shared `identity_match()` from match_files.py; `positive_control.json` / `positive_control_run.log`. Backup `ConnectedPapers-for-AlphaEdit%3A-Null%20Space-Constrained-Knowledge-Editing-for-Language-Models.bib` vs worktree `research_and_specs/` same filename: 66,812 bytes, byte equality explicitly verified; SHA256 `57a5796f1c2b02ddae5a58467a90ed75b73597f5e3d82c6c8032eb95475967d8`; blob `1f0928070f6e39cbc6b62dc0fd712cd62c1f8dfa`; holding commit `f459b3a21b996149287b20a6b4ad111763e5fc8f` verified by git ls-tree; EXACT found, UNIQUE fallback calls 0. This receipt must appear in final audit_report.md.
11. Current output size **185,777,156 bytes**, below conservative decimal 200,000,000-byte cap (approximately 14,222,844 bytes headroom). Keep artifacts compact; use gzip for row-based classification. `classification_refined.tsv.gz` is valid gzip TSV.

### Partial results a successor MUST NOT trust as final

- Raw candidates/classification contain C10 hash-substring, Qwen, RunPod, generic covariance false positives. Refined labels are still triage, not a complete semantic review. Adjacent includes third-party Claude/agent research/tool source; actual use by this program is unverified for many clones.
- SAME-NAME means only basename + comparison evidence. It does not prove the same subject/doc, chronology or duplication. Generic SKILL.md and index.html currently choose unrelated semantic counterparts (e.g. llm-as-database/SKILL.md vs llama_cpp_src code-review skill; fallback/index.html vs tools/labviz/index.html). Reclassify after proper content review; do not report these as older/newer programme documents or recovered duplicates.
- SAME-NAME `identical outside reachable history` is byte identity in a filesystem location under the mirror, NOT historical EXACT, and often NOT inside the current clone/worktree. Many important raw files are in sibling mirror-root `session_logs/`, `architecture_profile/`, `stage_1_sect/`, or `claude-ai-artifacts/`. Explicit probes found current-worktree paths `stage_1_sect/trials/stage_1_trial_cfb-001_r2.json`, `architecture_profile/capture_token_ids.py`, `session_logs/archive/s25/session_2_5_summary_block.md` absent. These sibling assets need a precise already-in-repo vs outside-repo distinction in the final recommendations.
- Readable large files were streamed for hashes; content samples were limited to 200 KiB and normal text previews to ranges/heads. Do not read any file >~200 KB whole. No source scientific result was run. One broad sed preview accidentally included compressed Drive assets (no mutations); subsequent previews used explicit text filenames. Never use a wildcard text-reader against mixed file types.
- No-name = CONTENT-PENDING, not UNIQUE. `early_nonexact_program.json` and `core_noname.json` are EARLY snapshots from raw triage and incomplete name-index timing, not final counts or final uniqueness. Ignore them for conclusions.
- Version dates from backup filesystem mtime are not sufficient for older/newer ordering; compare embedded version/date, diff sections/stat, and git version history. No ordered newer-version list exists yet.
- Historical blob/path index freshness and root symlink alias coverage need honest caveats. The read-only mirror scan found actual same-byte trials and capture code; this does NOT establish Git custody or restoration of deleted models/tensors.

### Research findings already read, with next checks

- Explicit pod-loss source: **SESSION_CHECKPOINT.md:1053** (corrects the approximate line noted above). Full line states RunPod LOST (balance lapsed), recovered all Workstream-1 docs via PR #1 + patched engine PR #2; lost/regenerable Qwen cov caches, HF models, B3 edited model + GGUF, llama.cpp/LARQL builds, run logs. Also **REPRODUCIBILITY.md:7,9**; runbook current-position note around :121 describes local reproduction and remaining lost B3/GGUF regeneration. Read bounded ranges and preserve precise citations in the final gap table.
- **memory_mirror/infranodus-discourse-lens-not-coverage-tool.md:20** explicitly says a pod-era export proof file under /workspace was lost. No recovery candidate identified for that proof.
- Backup **deep-research-report.md** (11,318 bytes) was read fully: old public-cache search for Llama-3.1-8B; finds only wrong checkpoint/variant near matches and embedded ChatGPT citation tokens. It is research history, not recovered cache bytes or current verified web evidence. Needs CONTENT comparison against repo research corpus before UNIQUE/recommendation.
- Backup **architecture-profile-seed.json** (8,320 bytes) records early Kaggle Block-1 GPT-J provenance and points to later Blocks 2/3. It was read but full substance comparison against architecture_profile provenance remains.
- Backup **llm-as-database/capture_token_ids.py** beginning read: early GPT-J-6B token/probability capture to /workspace/architecture_profile/token-id-capture-results.json. Matcher found byte-identical sibling mirror `/Volumes/memit/llm-database-poc-mirror/architecture_profile/capture_token_ids.py`; absent from worktree. Do not recommend rerunning it.
- Backup **llm-as-database/s2_5b_artifact_checksums.txt** read fully: 19 MD5 checksum lines for early runbooks/summary docs/manifests. It supports historical integrity comparisons, not recovery of referenced raw files by itself.
- Root nine **stage_1_trial_cfb-00{1,2,3}_r{1,2,3}.json** all have byte-identical sibling mirror-root stage_1_sect/trials copies; no historical blob match found. At least one trial was read in ranges: scientific trial/probe data. Distinguish data already preserved outside clone from genuinely unrecovered RunPod material.
- Five outside-folder programme files discovered: `/Volumes/backups/agent-deployment-framework/.superpowers/brainstorm/fallback/{07-augmentation-models,08-v1-approaches,09-design-architecture,12-visual-mindmap-infographic,index}.html`. Programme keyword lines read; complete contextual review still pending. They describe framework planning/LARQL/MEMIT overlay concepts, and some explicitly contrast with an LLM-as-database design. Do not assume all five contain substantive missing database research.
- Loose **01-data-layer-spec.md** heading says Local SEO Growth Engine data-layer schema; **05-v1-design-edits.md** concerns other ENGINE design/Module 16. Do not classify numbered root files as programme solely from their names. Root control-plane/operational-discipline specs are generic harness documents, adjacent rather than database-specific science.
- `src/` sampled main.tsx/QueryEngine.ts = Claude Code CLI source (SDK/permissions/context/query), classified adjacent; not the lost MEMIT scientific source tree.

### Steps remaining from the original brief

1. Reconcile final inventory coverage/hashes/classifications (symlink rows included; report 53 unhashed dangling links explicitly); verify final counts and output <=200 MB. Retain missing inline census/preview/evidence extraction scripts in scripts/ if final report relies on those outputs.
2. Finish relevance review of ambiguous files, including any programme files hidden among broad adjacent tooling. Check every top-level folder name coverage from census.json. Bounded archive/PDF inspection where uncertain (no extraction outside output, no installs). Caselaw remains names/metadata only unless a strong programme-named path appears.
3. Validate historical EXACT commit/path locations (group by commit then ls-tree), preserve real control. Complete same-name comparisons using all versions, whitespace, meaningful diff stats and differing sections; distinguish wrong-subject basename coincidences. For .skill ZIPs compare bounded member contents rather than ZIP container timestamps alone.
4. Complete CONTENT/rename/merged-substance matching for 140 program CONTENT-PENDING and 8,813 adjacent pending. Group generic tooling clones sensibly but assign every relevant file a traceable final match. Classify UNIQUE only after actual content search/read. Suggested normalized filename aliases: spaces/hyphens/underscores, duplicate suffix '(1)', version punctuation, .txt vs .md; no automatic UNIQUE based on absence of basename.
5. Search repo CORPUS/, SESSION_CHECKPOINT, EXPERIMENT_RUNBOOK, docs/, memory_mirror/, results/ READMEs systematically for lost/wiped/pod/not recovered/missing. Existing initial rg excerpts were not saved as a systematic loss-evidence artifact. Read strongest loss contexts properly and cite path:line.
6. Properly read each UNIQUE/newer/divergent PROGRAM file, map to recorded losses/missing material with backup and repo citations, and recommend import as-is / import as superseded-history / reference only / ignore with suggested target paths. Don't conflate prior docs/plans/MD5 lists with restored raw data/models. No imports authorized.
7. Write audit_report.md with final class/match counts, positive control, complete gap table, newer-than-repo list, open questions for MAESTRO and custody/hash exceptions. Name actual comparison limits. Audit not ready before these are done.
8. Final verification: output budget, report table row count, source read-only/scope evidence, updated progress and scripts reproducibility. Final completed reply starts required ready phrase plus report path and gap-table row count; do not use that phrase now.

### Exact resume commands

Run from the same worktree; these commands only rewrite owned audit outputs. Use system Python for model-free audit scripts (no .venv/model imports).

```sh
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
/opt/homebrew/bin/rtk proxy git rev-parse --show-toplevel
/opt/homebrew/bin/rtk proxy git branch --show-current
/opt/homebrew/bin/rtk proxy python3 -B results/backups_audit_20261011T084030Z/scripts/refine.py
/opt/homebrew/bin/rtk proxy python3 -B results/backups_audit_20261011T084030Z/scripts/positive_control.py
```

After refining/adding semantic overrides, refresh names and comparisons only if new candidate names or matching logic changed:

```sh
/opt/homebrew/bin/rtk proxy python3 -B results/backups_audit_20261011T084030Z/scripts/name_index.py > results/backups_audit_20261011T084030Z/name_index_run.log 2>&1
/opt/homebrew/bin/rtk proxy python3 -B results/backups_audit_20261011T084030Z/scripts/match_files.py > results/backups_audit_20261011T084030Z/match_run.log 2>&1
```

For programme review queue without loading large artifacts whole:

```sh
/opt/homebrew/bin/rtk proxy python3 - <<'PYRESUME'
from pathlib import Path
import csv,json
out=Path('results/backups_audit_20261011T084030Z')
c={r['inventory_row']:r for r in csv.DictReader((out/'candidates_refined.tsv').open(),delimiter='\t')}
for r in csv.DictReader((out/'matches.tsv').open(),delimiter='\t'):
    if r['class']=='program' and r['match']!='EXACT':
        print(c[r['inventory_row']]['path'],r['match'],r['comparison'],r['repo_or_mirror_path'],sep='\t')
print('output bytes',sum(p.stat().st_size for p in out.rglob('*') if p.is_file()))
print((out/'symlink_state.json').read_text())
PYRESUME
```

Do NOT rerun inventory.py, history_index.py or symlink_supplement.py over existing outputs. Do NOT copy/import/move/delete outside audit folder, commit/push, install, run experiments/models, or touch tmux. Prefix repo tools with LLMDB_ROOT=$PWD where applicable (the scripts use explicit paths/cwd and invoke read-only git directly).

### Binding context rule — restated for every successor

Watch own Context N% left. Start a new piece only at >=60% left. At <=40% left, or any Context compacted, stop starting work: update progress.md, write handoff_bk1.md with done/in-flight/remaining/exact paths/next step/open risks and this rule, and hand off to a fresh successor. MAESTRO explicitly requested this handoff at ~44%; honor the earlier stop. All source backups and repo files remain read-only; only `results/backups_audit_20261011T084030Z/` may be written.
