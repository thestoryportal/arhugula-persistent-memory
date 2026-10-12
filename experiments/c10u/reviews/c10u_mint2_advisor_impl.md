# D-C10u-mint2 — advisor review of the implementation (step 3)

reviewer: Claude advisor subagent, model Opus 5.5
date: 2026-10-07
scope: `experiments/track_c/c10u_mint2_{arms,read,selftest,step0,p4_probe}.py`, `tools/c10u_mint2_p4.sh`, report `results/c10u_mint2_codex_impl.md`, against `docs/C10U_MINT2_PREREG.md` v3 (incl. §7) and `D-C10u-A7V2` (`EXPERIMENT_RUNBOOK.md:332`).
what I ran: the model-free selftest (`.venv/bin/python -B …selftest.py` → 50 tests OK, no files left behind; `git status` on `results/c10u_mint2` and `architecture_profile` clean), and a tokenizer-only replay (scratch file in /tmp, model loader stubbed, `LLMDB_DEVICE=cpu`, no weights loaded) of the driver's own `audit_prompts`, `static_wordlist_audit`, `values_for`, `registration_words` and `p2_audit` for all seven (block, kind) pairs, plus a prefix re-tokenisation check at every target position. Nothing touched the GPU.

**Verdict: PROCEED**

No blocking defect. The schedule, gates, minting, halt path and P4 handling match the frozen document. The advisory items below are cheap. **Decide on them before the first stage.** After the first stage the driver locks the hashes of its source files (A2), so any later code change makes every remaining stage refuse to start.

## Evidence that the implementation matches the frozen design (spot-verified, file:line)

- **Schedule.** `read.py:536–537` gives reproduce = F mint-1 ×3, frozen = F multi + modifier ×3, v2 = V2 multi + mint-1 ×3 + mint-2 ×3, which is 3 + 4 + 7 = 14 behaviour runs in the §2 order. The control (`read.py:547–549`) is planned only on a raw SPAN-DIRECTION that is not blocked. Replication (`read.py:550`) is planned only on `replication_pending`. P4 requires a replicated LEAD/PARTIAL (`arms.py:934–957`).
- **LAW#3 HALT with data kept.** Each behaviour record is written before any gate (`arms.py:864`). The gate runs after F mint-1 seed 2 (`arms.py:1022–1023`) and right after F multi (`arms.py:1024–1025`), using `REPRODUCTION`/`ENVELOPE` = the §2 windows (`read.py:21–22`, `:361–383`). Every later stage (`frozen`, `v2`, `control`, `replicate-*`, `p4-save`) and the explicit step-0 phases re-run the gate before writing any marker (`arms.py:982–987`, `:1051–1052`), so after a miss no arm of either block can run. Nothing is deleted.
- **§3 readings.** These are implemented verbatim:
  - LEAD/PARTIAL/NULL/TRADEOFF, with [11, 18] always NULL (`read.py:289–293`).
  - Replication criteria (`:333`).
  - SPAN/PAIR/MIXED and MODIFIER-RECOVERY/NO-MODIFIER-GAIN/MIXED as min/max range rules, never index-pairwise (`:405–415`).
  - Replica must agree, else MIXED (`:506–507`).
  - SPAN-CONFOUNDED via the 48-row control (`:508–514`).
  - ROUTING-BLOCKED-UNDERFIT across every mint arm, including mint-1 and the control (`:493–497`).
  - V2 NOT-COMPARABLE without a halt (`:487–492`).
  - BIGRAM as C ≥ 1 ∧ X ≥ C, with C = 0 → NO-CONTINUATION (`:133–142`).
  - LARGE-WRITE = combined Frobenius ratio > 1.5 (`:145–150`, `:343–347`).
  - All locality gates (`:121–130`).
  - A1 ≥ 68 per run, string ≥ full, Z_OVERRIDE_HITS == 1 and LAW#5-hits == 0 (`:215`, `:228–231`).
  - The CORPUS/45 `A1 < 58` rule is not inherited.
- **Instruments.**
  - P3 admission uses the engine's last logged aggregate, ≥ 0.98 on ≥ 22/24 (`arms.py:454–457`, `read.py:84–105`). That last logged value belongs to the returned z: `compute_z.py:159–165` prints before it breaks or steps.
  - The per-position fit injects the returned z at the layer-8 output at the subject's last token on the identity-template CANON prompt. It reads the final output and layer 35 in the same forward (`arms.py:411–444`). This equals the solve's own intervention (`compute_z.py:90–99`, `:180`).
  - The bigram mappings are as frozen: V2 uses i+12; F uses the first cyclic subject that shares neither word, plus the same-head sibling (`arms.py:547–570`).
  - Contains/startswith use one greedy decode of n+2 tokens with no early stop (`arms.py:638–658`).
  - Binding = raw − whole-sequence step-0 recall (`arms.py:839`, `read.py:252`).
- **Context freeze.** An untouched precursor process samples the templates and checks that the vocabulary and the 271 spare rows hash the same before and after (`arms.py:661–683`). Every step-0 and behaviour process assigns `CONTEXT_TEMPLATES_CACHE` before registration and before LAW#5 (`arms.py:701`, `:781`). The engine strips braces from sampled text (`memit_main.py:310`), so `t.format(...)` is safe.
- **Inertness tolerance.** `INERTNESS_TOL = 1e-5` (`read.py:24`) is safe. The sibling's measured in-process engine self-distance is exactly 0.0 (`results/c10s_sharedz_r2/inertness.json:64`).

## (2) The minting itself

- **How ids are added.** `c10l_mint_lib.register` adds `AddedToken(" "+w, normalized=False, lstrip=False, rstrip=False, single_word=False)` to the process's `H.tok` only (`lib:24–37`). It fails closed on a short count, on non-contiguous ids from 151665, and on `tok(" "+w) != [id]`. There is no resize (271 spare rows; `assert_tied` and the layout check are at `arms.py:167–169`).
- **Words registered.** mint-2 = 24 heads then 24 modifiers (`arms.py:199–200`); mint-1 = the 24 strings; mint-1-48 = strings then heads (matches the §1.1 pre-screen order); arm B = the 8 frozen modifiers in first-use order.
- **Initialisation.** N(seed) is drawn on CPU, norm-matched (`lib:66`, `:84–86`). The 8- and 24-row prefixes are re-drawn and compared bit-for-bit (`arms.py:339–349`). `set_rows` is the only embedding write (`arms.py:719`, `:804`). The fp16 row hash is re-checked after the FFN write (`arms.py:848–849`).
- **Changes stay inside the process.** No `save_pretrained` touches `hf_cache` or the model files. The only save is the P4 replay, into `results/c10u_mint2/edited/c10u_mint2_p4save_*`, created with `mkdir(exist_ok=False)` (`arms.py:626–633`).
- **P2 replay (tokenizer only, the driver's own functions).** Static word-list replay: selected heads = frozen, inventory sha matches, quota {2: 6, 3: 18}, 396 plain prompts. P2 is **True on every check** for F mint-1, F modifier, V2 mint-1, V2 mint-2 (including `bigram_720_prefix_ids`) and V2 mint-1-48, with an inventory of 2376 prompts × 6 sample templates. Prefix re-tokenisation `CANON + decode(target[:j]) == CANON ids + target[:j]` gives **0 failures at every position** for all seven kinds, so `fit_at_z`'s strict check (`arms.py:435–436`) will not halt by construction. Only text in the runtime-sampled templates remains unaudited, and step 0 audits it.
- **P4.** GGUFs are written only under a new `results/c10u_mint2/p4/<tag>/`, which is refused if it exists (`p4_probe.py:141–145`). Existing GGUFs (`c10l_mint_N_*.gguf`, `b3_edited_*.gguf` in the main checkout) are never named. The probe scores exact ordered full sequences (`p4_probe.py:37–45`). The compiled-artefact gate is 24/24 canonical HF↔fp16 parity plus minted-word and target tokenisation in both GGUFs; held-out parity and Q4 retention are only reported (`read.py:553–623`).

## (3) Safety

- **Halt path.** The driver uses its own `architecture_profile/c10u_mint2_halt_diagnostic.json`, with a uuid suffix if that file exists (`arms.py:63–74`). It never writes step-1/2 files.
- **float64 on MPS.** The only `.double()` calls in the new code are `.cpu().double()` (`arms.py:502–503`). Every `piv_stats` input is a CPU tensor (`arms.py:726–727`, `:623–624`). The harness's own `js`/KL `.double()` calls act on CPU distributions (`c10e_bandknob.py:84–85`, `:105`, `:325`).
- **Stale knobs.** These are refused before any external call (`arms.py:121–125`).
- **Outputs.** Occupied outputs are refused before markers. JSON is opened with `x`, re-read and compared (`arms.py:45–60`). Everything is written under `out`, which must lie inside `results/c10u_mint2` (`arms.py:1081`), or under `architecture_profile`. The one exception is A1.

## (4) Codex report item 10 — halting instead of repairing the word list

**Halting is the right behaviour.**

1. The head list is frozen by hash in three places: the prereg (`7d83a89f…`), the reader constant (`read.py:16`) and every record's provenance (`read.py:196`). If the driver swapped a head at run time, every record would fail validity, the 48-row control's extra words would change, and the stimuli would no longer be the ones that were reviewed.
2. §5's "one fix" is a LAW halt-discipline action for the program session: a `cat -n` read, then one authored change, then HALT if it fails again. It is not an autonomous driver step.
3. If the fix is ever needed:
   - Write it as a new authored record (`v2_wordlist_v2b.json`, re-hashed).
   - Add a prereg amendment line and a new reader constant.
   - Use a fresh `--out-dir`, because the source identity changes.
4. My replay shows P2 passes on the frozen list for every kind. The only realistic remaining trigger is a sampled context template containing a registered word. In that case swapping a head is the wrong fix; the fix is a fresh context precursor in a new out-dir.

## Items

### BLOCKING
None.

### ADVISORY

1. **A wrong `LLMDB_ROOT` sends the halt diagnostic into the main checkout.**
   - What happens: `main()` sets `RUN_ROOT = root` from `--root`/`LLMDB_ROOT` (`arms.py:1075–1077`) before the root check (`:1079–1080`). The `except` then calls `halt(str(exc), root, …)` (`:1105`). The operator's shell profile points `LLMDB_ROOT` at the main checkout, so forgetting the `export` writes `architecture_profile/c10u_mint2_halt_diagnostic.json` into the shared main checkout. `p4_probe.py:190`/`:195` has the same pattern.
   - **Fix:** in both mains, set `own = Path(__file__).resolve().parents[2]`, set `RUN_ROOT = own` before the check, and use `halt(str(exc), own, …)`. Apply this before stage 1 (see 2).
2. **The source-identity lock covers the prereg and the shared harness.**
   - What happens: `SOURCE_FILES` (`arms.py:24–27`) includes `docs/C10U_MINT2_PREREG.md`, `c10e_bandknob.py`, the hparams, the screens, the engine and all c10u code. `assert_sources` (`arms.py:89–94`) refuses every later stage if any of them changes.
   - Consequences: do not edit the prereg's status line, the harness or any c10u file from the first stage until the last stage you intend to run. Put run-state notes in the runbook or checkpoint (neither is in the identity). Any step-1/2 work in this worktree that edits `c10e_bandknob.py` will block step-3 stages. That is fail-closed, so nothing is corrupted, but the schedule is lost. No code change is needed; this is a note for the operator.
3. **Replicas reuse the step-0 z, contexts and inits, so gate A probably measures about zero.**
   - What happens: replicate-F/V2 load the replicate-0 step-0 z (`arms.py:770`, `:796–799`, `:815`). The measured in-process engine self-distance is 0.0. The ±4–5 "process envelope" that §2 says replication measures (`CORPUS/45:61`) most likely came from each process sampling its own context templates, and the frozen context set removes that.
   - Effect: the replica is likely bit-identical to the original, so "replicated" becomes close to automatic. Re-solving z in the replica would not change this if MPS is deterministic across processes. The code follows the prereg ("same frozen context set and the same inits"); the limitation comes from the design.
   - **Recommendation:** no code change. State in the verdict brief and the CORPUS entry that gate A here measures cross-process numeric reproducibility, not the historical envelope.
   - Optional, before stage 1 only: in `behavior_job`, when `replicate == 1`, also run `capture_targets` in the process and record the rel-L2 of the fresh z against the step-0 z, as a diagnostic that does not gate. This settles whether MPS is bit-exact across processes.
4. **Replication will in practice always be scheduled, so plan for about 28 behaviour runs, not 14.**
   - What happens: mint-1 arms are labelled like every other arm (`read.py:476–481`). CORPUS/45's mint-1(frozen) values of 34–46 read LEAD-NOT-REPLICATED, which sets `replication_pending` and makes `stage_plan` schedule `replicate-F` (`read.py:550`). The same applies to V2 if mint-1(V2) reaches 30 or more.
   - This follows "any … LEAD or PARTIAL is replicated" (§2), but it doubles the budget the operator was shown (§6).
   - Operator decision: approve the replication stages up front, or rule that the reference arms (mint-1) do not trigger replication. A rule like that needs a prereg amendment and a reader change before stage 1.
5. **Runtime estimate (see the table below).** The prereg's ≈ 9.5 h counts only 40-minute behaviour passes. The implementation adds:
   - 12 step-0 processes (24 `compute_z` solves, 24 position fits and the I-11 battery each);
   - 2 context precursors;
   - a wrapper proof in every behaviour process (`arms.py:468–517`: one extra `compute_P` = 5 covariance loads plus SVDs of 11008², one solve, three `my_edit`);
   - a second `compute_P` inside `run_recipe`.

   My unmeasured estimate for the first 14-run schedule is ≈ 14–17 h. Codex's "≈2h" for reproduce counts behaviour time only.
6. **LAW#3 can stop earlier (saves time, optional).** The gate runs only after seed 2 (`arms.py:1022`), but a single seed outside its window is already a miss (`read.py:371–373`).
   - Fix: after each F mint-1 behaviour, call a per-seed window check and halt on a miss. This saves up to two runs (≈ 1.5 h) on an early miss.
   - Do this only if you are already touching the code for item 1.
7. **`LLMDB_DEVICE` is neither refused nor recorded.**
   - What happens: `resolve_device` honours it (`util/device.py:20–22`), but it is not in `HARNESS_KNOBS` (`arms.py:21–23`) and the device is not written to any record. A stray `LLMDB_DEVICE=cpu` would silently run on CPU, with numerics different from CORPUS/45 (MPS).
   - **Fix:** add `"LLMDB_DEVICE"` to `HARNESS_KNOBS`, or record `str(H.DEV)` in the step-0 and behaviour records and require `mps` in `run_validity`.
8. **P4 disk use and git.**
   - Size: each eligible configuration writes ≈ 6 GB of HF safetensors (`edited/`) and ≈ 6 GB f16 + ≈ 2 GB Q4 GGUF (`p4/`) inside `results/c10u_mint2`. `/Volumes/memit` has 121 GiB free; six configurations would take ≈ 85 GB. Run P4 one configuration at a time and check `df -h /Volumes/memit` first.
   - Git: `*.gguf` and `*.safetensors` are ignored (`.gitignore:24–25`), but `edited/*/tokenizer.json`, `config.json` and the like are not. Never `git add results/c10u_mint2/edited`.
   - Backup: this worktree is excluded from `backup_mirror` (`tools/backup_mirror.excludes`). Commit the small JSON and `.pt` records after each stage; the `.pt` files are about 0.2–0.4 MB and not ignored, which is fine.
9. **The "mis-order, counted" I-11 item is recorded but not counted.** The per-fact modifier rank/top-1 at the value slot is stored (`arms.py:385–395`), but there is no aggregate count. The verdict or reader can derive it from `probe.rank_probes[*].rank_prob_top1.modifier_misplaced_at_value_slot.top1 == target_ids[-1]`. No change is needed before running.
10. **Codex report items 1, 3, 4, 8 and 9 are accepted. Record them as implementation decisions in the CORPUS entry.**
    - 1: an untouched context-only precursor instead of the A7-multi behaviour process. Same property: no minted row is live while templates are sampled.
    - 3: no LAW#5 in processes that make no write. LAW#5 runs in every process that writes.
    - 4: the 1e-5 inertness tolerance, backed by the measured 0.0 floor.
    - 8: P4 eligibility requires a *replicated* label, which is stricter than "carries LEAD or PARTIAL"; it runs in a separate save replay.
    - 9: the v3 rule (measure all 24, mask beside the count) wins over the older §7 fold wording.
11. **Low-probability fail-closed halts. Keep them.** Each behaviour process re-checks against step 0 with exact equality: whole-sequence pre-write recall (`arms.py:805–807`) and the P2 replay (`:793–795`). An argmax near-tie differing across processes would halt a run. It is conservative, and the diagnostic plus data are retained.

## (5) Cost per stage (estimates, UNMEASURED; one model process at a time, loop paused)

| stage | processes | estimate |
|---|---|---|
| reproduce | F context precursor (~3 min) + 3 step-0 (~15–25 min each) + 3 behaviour (~45–55 min each) | ≈ 3.2–4.2 h |
| frozen | 3 step-0 (modifier) + 4 behaviour (multi + 3 modifier; multi also solves its own 24 z) | ≈ 4–5 h |
| v2 | V2 context precursor + 6 step-0 + 7 behaviour | ≈ 7.5–9 h |
| *first 14-run schedule* | | ≈ 14–17 h (prereg ≈ 9.5 h counted behaviour only) |
| control (conditional) | 3 step-0 (mint-1-48) + 3 behaviour | ≈ 3–4 h |
| replicate-F / replicate-V2 (expect both, item 4) | 7 behaviour each, reusing step 0 | ≈ 5.5–6.5 h each |
| p4-save (conditional) | 1 behaviour replay + HF save per eligible config | ≈ 50–60 min each |
| P4 chain per config (CPU) | convert ≈ 5 min, quantize ≈ 3–5 min, 2 × 148 completions at `-ngl 0` | ≈ 20–40 min each |

## Exact stage commands

Run them from the worktree, with the autoresearch loop paused and Ollama stopped. First check that no other model process is running (`pgrep -fl "python|llama-server|ollama"` should list none). Read the reader output after each stage before starting the next.

```bash
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
export LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
PY="$LLMDB_ROOT/.venv/bin/python"
DRV="$LLMDB_ROOT/experiments/track_c/c10u_mint2_arms.py"
REF="$LLMDB_ROOT/results/c10l_covgeom/run1_armB_identity.json"   # A1 71/72, A2 70/72 (checked)
LOGS="$LLMDB_ROOT/results/c10u_mint2_logs"; mkdir -p "$LOGS"      # outside results/c10u_mint2 on purpose
READ() { "$PY" -B "$LLMDB_ROOT/experiments/track_c/c10u_mint2_read.py" "$LLMDB_ROOT/results/c10u_mint2"; }

# 0. pre-flight (model-free)
"$PY" -B "$LLMDB_ROOT/experiments/track_c/c10u_mint2_selftest.py"
"$PY" "$LLMDB_ROOT/tools/engine_fingerprint.py"
/bin/df -h /Volumes/memit

# 1. LAW#3 reproduction: F mint-1(frozen) seeds 0,1,2 (HALT on a miss; data kept)
nohup "$PY" "$DRV" reproduce --law3-ref "$REF" > "$LOGS/reproduce.log" 2>&1 &
READ    # expect F: INCOMPLETE (multi/modifier missing); check architecture_profile/ for c10u_mint2_halt_diagnostic*.json

# 2. rest of block F: multi (envelope gate → HALT on a miss), modifier-only seeds 0,1,2
nohup "$PY" "$DRV" frozen --law3-ref "$REF" > "$LOGS/frozen.log" 2>&1 &
READ

# 3. block V2: multi, mint-1 x3, mint-2 x3
nohup "$PY" "$DRV" v2 --law3-ref "$REF" > "$LOGS/v2.log" 2>&1 &
READ    # look at V2.controls_pending, F/V2.replication_pending

# 4. conditional (the driver refuses each one before writing a marker if it is not needed)
nohup "$PY" "$DRV" control      --law3-ref "$REF" > "$LOGS/control.log" 2>&1 &   # only if V2 raw_direction == SPAN-DIRECTION
nohup "$PY" "$DRV" replicate-F  --law3-ref "$REF" > "$LOGS/replicate_F.log" 2>&1 &
nohup "$PY" "$DRV" replicate-V2 --law3-ref "$REF" > "$LOGS/replicate_V2.log" 2>&1 &
# (run these one after another, never at the same time; READ after each)

# 5. P4 (only for replicated LEAD/PARTIAL mint-2 or modifier seeds)
nohup "$PY" "$DRV" p4-save --law3-ref "$REF" > "$LOGS/p4save.log" 2>&1 &
ls "$LLMDB_ROOT"/results/c10u_mint2/p4save_*_admitted.json
# for each admitted record, one at a time, after df -h:
bash "$LLMDB_ROOT/tools/c10u_mint2_p4.sh" \
  --record "$LLMDB_ROOT/results/c10u_mint2/p4save_<BLOCK>_r0_<KIND>_s<SEED>_admitted.json" \
  --source /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/llama_cpp_src \
  --bin /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/llama_cpp_src/prebuilt/llama-b11382 \
  > "$LOGS/p4_<BLOCK>_<KIND>_s<SEED>.log" 2>&1
```

Optional explicit admission-only phases (normally automatic): `"$PY" "$LLMDB_ROOT/experiments/track_c/c10u_mint2_step0.py" reproduce|frozen|v2|control --law3-ref "$REF"`.

Re-running a stage that halted is refused by design, because its markers are occupied. Use a fresh `--out-dir "$LLMDB_ROOT/results/c10u_mint2/r2"` under the same parent. That produces a new identity and a new context set.
