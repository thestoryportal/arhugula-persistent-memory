Reviewer: gpt-6.1-sol (max effort), Codex CLI 0.160.1, read-only

## Verdict

SOUND-CANDIDATE — On the supplied run-to-commit mapping, the 7 → 18 full-read gain is a credible preservation candidate with no visible evaluation leakage or changed pre-template draw order, subject to the provenance and replication limits below (`runs/20261006-131156_nocommit/score.json:summary.heldout_full=7`; `runs/20261006-142644_nocommit/score.json:summary.heldout_full=18`; `92acd03:edit.py:60-104`; `fd16592:edit.py:58-79`).

## Answers to Q1–Q5

Source convention: `fd16592:<file>:<line>` and `92acd03:<file>:<line>` name immutable files in `/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10`; unprefixed `runs/` and `results.tsv` paths refer to that repository. `8d331ac:<file>:<line>` names the parent program worktree at commit `8d331ac8b17b8dc1da1c56e3596663f5816aba55`, rooted at `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`. These are citation definitions.

### Q1 Integrity

**Yes, four files besides `edit.py` changed.** The additional paths are `graft/.cache/ask-index.json`, `graft/.cache/extract.c3679fb5d24a63a0.json`, `graft/.cache/fingerprint.c3679fb5d24a63a0.json`, and `graft/.graph/wiring.json` (before/after: `fd16592:graft/.cache/ask-index.json:1` / `92acd03:graft/.cache/ask-index.json:1`; `fd16592:graft/.cache/extract.c3679fb5d24a63a0.json:1` / `92acd03:graft/.cache/extract.c3679fb5d24a63a0.json:1`; `fd16592:graft/.cache/fingerprint.c3679fb5d24a63a0.json:1` / `92acd03:graft/.cache/fingerprint.c3679fb5d24a63a0.json:1`; `fd16592:graft/.graph/wiring.json:507-508` / `92acd03:graft/.graph/wiring.json:507-508`).

**Both evaluation files are byte-identical.** Complete `git show` output comparisons and independent SHA-256 calculations at both commits give `prepare.py` = `8e577d546080f06bbd25a685e9af03016117d1e133ff9ff97aa92e5ac22f21f1` and `c10e_bandknob.py` = `1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695` (`fd16592:prepare.py:1-312`; `92acd03:prepare.py:1-312`; `fd16592:c10e_bandknob.py:1-599`; `92acd03:c10e_bandknob.py:1-599`).

The metadata comparison must not be mistaken for an evaluator change: the baseline graph records an older `prepare.py` body hash beginning `5260f46d`, while the candidate graph records the actual shared hash beginning `8e577d54` (`fd16592:graft/.graph/wiring.json:507-508`; `92acd03:graft/.graph/wiring.json:507-508`). I-INFER: these metadata changes do not explain the score through the inspected runtime, which imports the fixed preparation/engine utilities and contains no Graft access (`92acd03:edit.py:15-19,60-114`; `92acd03:prepare.py:15-21,82-118,190-301`). They nevertheless violate a literal claim that only one repository file changed; the loop permits editing only `edit.py` (`92acd03:program.md:26-30`).

**Provenance limit:** the ledger links `fd16592` to 7 and rounded norm 89.0, and `92acd03` to 18 and 131.4 (`results.tsv:2,4`), matching the exact scores (`runs/20261006-131156_nocommit/score.json:summary.heldout_full=7`, `runs/20261006-131156_nocommit/score.json:summary.dw_total=88.974`; `runs/20261006-142644_nocommit/score.json:summary.heldout_full=18`, `runs/20261006-142644_nocommit/score.json:summary.dw_total=131.421`). However, both scores record `edits.commit="nocommit"` (`runs/20261006-131156_nocommit/score.json:edits.commit="nocommit"`; `runs/20261006-142644_nocommit/score.json:edits.commit="nocommit"`). Exact executed-source-to-commit linkage is **UNVERIFIABLE** from these records: preparation records a commit label and changed-weight manifests, but no executed `edit.py` hash (`92acd03:prepare.py:194-221,292-293`). Run outputs are intentionally unversioned (`92acd03:.gitignore:5-10`; `92acd03:program.md:78`).

### Q2 Leakage

**No copied evaluation content is visible in the candidate recipe.** I compared its complete source, including literals and prompt construction, with the held-out templates, locality builders, generic sentences, frame subjects, and metric functions (`92acd03:edit.py:1-114`; `92acd03:c10e_bandknob.py:51-61,109-143,259-300,303-338,358-400`; `92acd03:prepare.py:98,228-235,249-293`).

The new collection constructs each input solely as an engine context template wrapped around `request(subject, value)`'s write prompt, followed by that fact's supplied target tokens; it extracts MLP inputs at the appended value positions (`92acd03:edit.py:67-76,81-84`). The request defaults to the canonical training frame, `The capital of {} is the city of`; the held-out frames are `{}'s capital city is called`, `If you visit {}, its capital city is`, and `The main city and seat of government of {} is` (`92acd03:prepare.py:94,101-108`; `92acd03:c10e_bandknob.py:51-56,96-97`). Conditioning on supplied fact values is training input rather than a held-out prompt substitution (`92acd03:prepare.py:101-108`; `92acd03:edit.py:68-73`; `92acd03:program.md:27,33`).

The recipe contains no copied real-country locality list, generic sentence, fictional frame subject, or answer-matching logic. Its new diagnostics measure key cosine overlap, update outputs on keys, and residual realization (`92acd03:edit.py:1-114`, especially `91-106`; compare `92acd03:c10e_bandknob.py:259-338,358-400`; `92acd03:prepare.py:98,228-235`). The mandatory `evaluate(apply_edit)` call delegates to the fixed scorer (`92acd03:edit.py:113-114`; `92acd03:prepare.py:222-225,238-301`).

The blocklist is only a substring check, including a few characteristic phrases; passing it alone would not establish absence of leakage. The content comparison is the basis for this answer (`92acd03:prepare.py:67-76`). Leakage through unseen prior agent context is **UNVERIFIABLE** from these snapshots.

### Q3 Mechanism

The write still fits a desired hidden-state change at each fact's subject. The candidate additionally runs the canonical write prompt plus its known full value through the model and collects `Kp`, the MLP inputs at every value-token position, including the second word (`92acd03:edit.py:60-76,81-95`). It changes the solve from `P @ (K @ K.T + zero_cache) + RIDGE*I` to `P @ (K @ K.T + PRESERVE_WEIGHT * Kp @ Kp.T) + RIDGE*I`, with weight 1 and an unchanged right-hand side (`fd16592:edit.py:64,71-74`; `92acd03:edit.py:33,96-99`).

I-INFER: this asks the update to produce the requested change at subject keys while producing less change at value keys, so recognizing an already-emitted value head is less likely to trigger the write for that same string acting as a country name. This is a soft projected constraint, not a guarantee that `dW @ Kp` is zero (`92acd03:edit.py:94-102`).

**The exact string collisions exist.** Eight value heads are also edited subjects, affecting sixteen subject/value facts; the table names both incoming values and the head's own write (`92acd03:c10e_bandknob.py:57-61,229-249`; per-row score citations below).

| Shared value head / subject | Facts whose value begins with that head | That subject's own fact | Evidence |
|---|---|---|---|
| Drennik | Quaxil → Drennik Brakk; Oxbarrow → Drennik Ulvenn | Drennik → Kessivar Ulvenn | `runs/20261006-142644_nocommit/score.json:1345-1346`; `runs/20261006-142644_nocommit/score.json:1633-1634`; `runs/20261006-142644_nocommit/score.json:1441-1442` |
| Vythorn | Plurnak → Vythorn Stavik; Zephquin → Vythorn Cindel | Vythorn → Vorlex Yornel | `runs/20261006-142644_nocommit/score.json:1369-1370`; `runs/20261006-142644_nocommit/score.json:1657-1658`; `runs/20261006-142644_nocommit/score.json:1393-1394` |
| Vorlex | Vythorn → Vorlex Yornel; Lurmaxen → Vorlex Drelth | Vorlex → Glimsto Spraxil | `runs/20261006-142644_nocommit/score.json:1393-1394`; `runs/20261006-142644_nocommit/score.json:1681-1682`; `runs/20261006-142644_nocommit/score.json:1801-1802` |
| Kessivar | Drennik → Kessivar Ulvenn; Kessivar → Kessivar Brakk | Kessivar → Kessivar Brakk | `runs/20261006-142644_nocommit/score.json:1441-1442`; `runs/20261006-142644_nocommit/score.json:1729-1730`; `runs/20261006-142644_nocommit/score.json:1729-1730` |
| Halquin | Yastovel → Halquin Cindel; Wombryne → Halquin Stavik | Halquin → Marsduq Yornel | `runs/20261006-142644_nocommit/score.json:1465-1466`; `runs/20261006-142644_nocommit/score.json:1753-1754`; `runs/20261006-142644_nocommit/score.json:1777-1778` |
| Marsduq | Crulpane → Marsduq Drelth; Halquin → Marsduq Yornel | Marsduq → Fluvane Cindel | `runs/20261006-142644_nocommit/score.json:1489-1490`; `runs/20261006-142644_nocommit/score.json:1777-1778`; `runs/20261006-142644_nocommit/score.json:1849-1850` |
| Glimsto | Mophgar → Glimsto Vask; Vorlex → Glimsto Spraxil | Glimsto → Lurmax Spraxil | `runs/20261006-142644_nocommit/score.json:1513-1514`; `runs/20261006-142644_nocommit/score.json:1801-1802`; `runs/20261006-142644_nocommit/score.json:1417-1418` |
| Fluvane | Trannak → Fluvane Stavik; Marsduq → Fluvane Cindel | Fluvane → Vindex Spraxil | `runs/20261006-142644_nocommit/score.json:1561-1562`; `runs/20261006-142644_nocommit/score.json:1849-1850`; `runs/20261006-142644_nocommit/score.json:1609-1610` |

Quaxil → Drennik Brakk, for example, has `canon_full=false` before and `true` after (`runs/20261006-131156_nocommit/score.json:arms.A7_coined_coined.rows[1].canon_full=false`; `runs/20261006-142644_nocommit/score.json:arms.A7_coined_coined.rows[1].canon_full=true`), while its held-out full hits change from `[false,false,false]` to `[false,false,true]` (`runs/20261006-131156_nocommit/score.json:arms.A7_coined_coined.rows[1].para_full_hits=[false,false,false]`; `runs/20261006-142644_nocommit/score.json:arms.A7_coined_coined.rows[1].para_full_hits=[false,false,true]`). I-INFER: this is consistent with reduced continuation interference; aggregate first-token hits decrease (`runs/20261006-131156_nocommit/score.json:summary.first_token=40`; `runs/20261006-142644_nocommit/score.json:summary.first_token=35`).

**Causal firing of a subject write inside a value is UNVERIFIABLE here.** The scorer stores hit flags and aggregate continuation accuracy, not the actual failed generations or per-position edit activations (`92acd03:c10e_bandknob.py:109-117,358-400`). The candidate's overlap/leak diagnostic is printed rather than saved by its source (`92acd03:edit.py:100-106`). The collision is established; the exact redirection mechanism still needs a control.

### Q4 Noise and randomness

**The inspected change does not shift draws before editing context templates are sampled.** The order in the two recipes is:

1. Import the same preparation code: `SEED=0`, then `torch.manual_seed(SEED)`, then the harness import. The harness loads the same pinned model in `.eval()` mode and builds stimuli by sorting and modular indexing (`fd16592:prepare.py:35,82-93`; `92acd03:prepare.py:35,82-93`; `92acd03:c10e_bandknob.py:25-26,45-48,224-253`).
2. Build the same hyperparameters and five covariance projectors before `apply_edit` (`fd16592:edit.py:24-51`; `92acd03:edit.py:25-53`). Covariance retrieval is cached and can call the same statistics loader on a miss in either version (`8d331ac:memit_dry_run/memit/memit/memit_main.py:255-280`). Common model initialization or statistics-loading draws, if any, precede the same first template call; no new candidate operation is inserted there (`fd16592:edit.py:14-61`; `92acd03:edit.py:15-82`).
3. On the first arm, both construct requests and immediately call `get_context_templates(model, tok)`, before `compute_z` or any new candidate forward (`fd16592:edit.py:60-63`; `92acd03:edit.py:81-84`). The engine initializes its process-global cache once, using prefixes `The`, `Therefore`, `Because`, `I`, and `You`, plus the identity template; the random draw is `torch.multinomial` inside `generate_fast` (`8d331ac:memit_dry_run/memit/memit/memit_main.py:20-22,304-323`; `8d331ac:memit_dry_run/memit/util/generate.py:90-120`).
4. Both solve target vectors from that cached context list. `compute_z` starts from a zero delta and uses Adam and forward/backward passes, with no random initialization or text-sampling call (`8d331ac:memit_dry_run/memit/memit/compute_z.py:40-83,103-178`). Only then does the candidate add `current()` diagnostics and `value_keys`: ordinary evaluation-mode forwards and tensor algebra with no sampling call (`92acd03:edit.py:60-76,86-106`; `92acd03:c10e_bandknob.py:48`; `8d331ac:memit_dry_run/memit/rome/repr_tools.py:135-147`).
5. The removed baseline key-cache accumulation also uses representation forwards, not sampling (`fd16592:edit.py:77-79`; `8d331ac:memit_dry_run/memit/memit/compute_ks.py:19-50`). Preparation restores weights between A1, A2, and A7 but neither reseeds nor clears the template cache; later arms reuse the first arm's sampled templates (`92acd03:prepare.py:96,201-219`; `8d331ac:memit_dry_run/memit/memit/memit_main.py:304-323`).

The scorer is a **different process**, again seeded before model loading. Its setup performs the fixed LAW#5 edit before hashing its cached templates; full-sequence evaluation uses greedy argmax (`92acd03:prepare.py:82-86,149-163,222-223,238-245`; `92acd03:c10e_bandknob.py:109-117,415-444`). Both scores contain `seed=0` and `gates.templates_sha="e8605172dce0"` (`runs/20261006-131156_nocommit/score.json:seed=0`, `runs/20261006-131156_nocommit/score.json:gates.templates_sha="e8605172dce0"`; `runs/20261006-142644_nocommit/score.json:seed=0`, `runs/20261006-142644_nocommit/score.json:gates.templates_sha="e8605172dce0"`). This verifies agreement of **scorer** contexts, not a recorded hash of the editing process's contexts (`92acd03:prepare.py:158-163,220-223,242,292-293`). Empirical equality of edit-time templates and full backend determinism are **UNVERIFIABLE** from these saved records.

The historical baseline range 8–16/72, approximate ±4–5/72 spread, and exact fixed-seed baseline reproduction are supplied context, not independently remeasured here (`/Users/robertrhu/.claude/jobs/4d71207f/tmp/codex_exp2_packet.md:19`). I-INFER: an inserted pre-template sampling call is not a supported explanation for this diff, but cross-process reproducibility and statistical significance of the gain remain **UNVERIFIABLE** without a confirming run.

### Q5 Guards and side effects

All nine requested guard values and their fixed thresholds follow. Score citations refer to the displayed JSON summary values.

| Guard | Threshold | Baseline | Candidate | Score evidence |
|---|---|---:|---:|---|
| A1 | ≥ 68 (`92acd03:prepare.py:43`) | 69 | 69 | `runs/20261006-131156_nocommit/score.json:6`; `runs/20261006-142644_nocommit/score.json:6` |
| A2 | ≥ 68 (`92acd03:prepare.py:44`) | 69 | 69 | `runs/20261006-131156_nocommit/score.json:7`; `runs/20261006-142644_nocommit/score.json:7` |
| L1_flips | ≤ 1 (`92acd03:prepare.py:45`) | 0 | 0 | `runs/20261006-131156_nocommit/score.json:8`; `runs/20261006-142644_nocommit/score.json:8` |
| frame_flips | ≤ 2 (`92acd03:prepare.py:46`) | 1 | 1 | `runs/20261006-131156_nocommit/score.json:9`; `runs/20261006-142644_nocommit/score.json:9` |
| described_as | ≥ 85.0 (`92acd03:prepare.py:47`) | 90.38 | 92.55 | `runs/20261006-131156_nocommit/score.json:10`; `runs/20261006-142644_nocommit/score.json:10` |
| L3 | ≥ 29 (`92acd03:prepare.py:48`) | 30 | 30 | `runs/20261006-131156_nocommit/score.json:11`; `runs/20261006-142644_nocommit/score.json:11` |
| ppl_post | ≤ 22.2 (`92acd03:prepare.py:49`) | 21.506 | 21.356 | `runs/20261006-131156_nocommit/score.json:12`; `runs/20261006-142644_nocommit/score.json:12` |
| scope_ok | = true (`92acd03:prepare.py:51`) | true | true | `runs/20261006-131156_nocommit/score.json:14`; `runs/20261006-142644_nocommit/score.json:14` |
| law5_ok | = true (`92acd03:prepare.py:50`) | true | true | `runs/20261006-131156_nocommit/score.json:13`; `runs/20261006-142644_nocommit/score.json:13` |

| Diagnostic / status | Baseline | Candidate | Score evidence |
|---|---:|---:|---|
| heldout_full | 7 | 18 | `runs/20261006-131156_nocommit/score.json:3`; `runs/20261006-142644_nocommit/score.json:3` |
| canon | 7 | 24 | `runs/20261006-131156_nocommit/score.json:4`; `runs/20261006-142644_nocommit/score.json:4` |
| first_token | 40 | 35 | `runs/20261006-131156_nocommit/score.json:5`; `runs/20261006-142644_nocommit/score.json:5` |
| dw_total | 88.974 | 131.421 | `runs/20261006-131156_nocommit/score.json:15`; `runs/20261006-142644_nocommit/score.json:15` |
| edit_seconds | 1376.4 | 2011 | `runs/20261006-131156_nocommit/score.json:16`; `runs/20261006-142644_nocommit/score.json:16` |
| guards | ok | ok | `runs/20261006-131156_nocommit/score.json:18`; `runs/20261006-142644_nocommit/score.json:18` |

**No listed guard moved toward failure.** A1 and A2 remain one read above their cutoffs; L1, frame, and L3 retain their margins. Described-as locality improves from 90.38 to 92.55; perplexity decreases from 21.506 to 21.356 (thresholds and exact score values cited in the table). Frame count is absolute emission of an edited first token, not newly induced changes; pre-edit frame count is already 1 in both runs (`92acd03:prepare.py:228-235,254,272`; `runs/20261006-131156_nocommit/score.json:frame_pre_edit=1`; `runs/20261006-142644_nocommit/score.json:frame_pre_edit=1`).

There are costs outside those guard failures: first-token hits lose 5 reads, `dw_total` grows by 42.447 (about 47.7%), and measured edit time grows by 634.6 seconds, leaving 689 seconds of the 2700-second budget (arithmetic from `runs/20261006-131156_nocommit/score.json:summary.first_token=40`, `runs/20261006-131156_nocommit/score.json:summary.dw_total=88.974`, `runs/20261006-131156_nocommit/score.json:summary.edit_seconds=1376.4`; `runs/20261006-142644_nocommit/score.json:summary.first_token=35`, `runs/20261006-142644_nocommit/score.json:summary.dw_total=131.421`, `runs/20261006-142644_nocommit/score.json:summary.edit_seconds=2011.0`, `runs/20261006-142644_nocommit/score.json:edit_budget=2700`). Weight norm is explicitly a soft constraint; first-token hits have no guard threshold (`92acd03:program.md:40`; `92acd03:prepare.py:42-52`). Full reads are still only 18/72 = 25% (`runs/20261006-142644_nocommit/score.json:summary.heldout_full=18`; `runs/20261006-142644_nocommit/score.json:arms.A7_coined_coined.para_n=72`).

The manifests list only the five MLP down-projection weights at layers 4–8 in each arm (`runs/20261006-131156_nocommit/score.json:38-59`; `runs/20261006-142644_nocommit/score.json:38-59`). The fixed scorer checks saved names, shapes, dtypes and finiteness and computes scope across all arms (`92acd03:prepare.py:256-277`).

**LAW#5 caveat:** `law5_ok=true` certifies the fixed harness's default edit against the engine, independently of candidate `apply_edit`; it does not certify the new preservation term (`92acd03:prepare.py:149-155`; `92acd03:c10e_bandknob.py:415-444`). Both recorded parity deltas are `expr_delta=0.0011` and `loc_delta=0.01` (`runs/20261006-131156_nocommit/score.json:gates.law5.expr_delta=0.0011`, `runs/20261006-131156_nocommit/score.json:gates.law5.loc_delta=0.01`; `runs/20261006-142644_nocommit/score.json:gates.law5.expr_delta=0.0011`, `runs/20261006-142644_nocommit/score.json:gates.law5.loc_delta=0.01`). Independent candidate inertness/causal validation is **UNVERIFIABLE** here.

## Cheapest falsifier

**Proposed control; not run:** replay `92acd03` with **only `PRESERVE_WEIGHT=0.0`**, retaining `value_keys`, every extra forward, the diagnostics, the layer order and all other parameters. Use the same fixed seed and fixed scorer, log the executed source hash, and capture/hash the edit-time cached context list so the replay is auditable (`92acd03:edit.py:25-33,60-106`; `92acd03:prepare.py:35,82-86,190-225`). Schedule it after the active GPU run in an isolated replay, without changing the live loop checkout.

I-INFER: zeroing the coefficient restores the baseline write equation while retaining the candidate's forward-call volume; the removed baseline cache was initialized to zero per call and updated only after all writes, with no later consumer (`fd16592:edit.py:64-79`; `92acd03:edit.py:94-104`). Predeclare the overturn criterion: **if the zero-term control still reaches at least 18/72 with every guard passing**, the reported preservation win requires no preservation term and becomes artifact-suspect. A return near the recorded baseline would support the mechanism; cross-seed generalization would remain unverified.

Budget **roughly 50–60 Apple-MPS GPU wall minutes** (estimate): the winner records 2011 edit seconds plus 862 scorer seconds, or 47.9 minutes, before unmeasured loading/launch overhead (`runs/20261006-142644_nocommit/score.json:summary.edit_seconds=2011.0`; `runs/20261006-142644_nocommit/score.json:summary.score_seconds=862.0`; platform/process arrangement: `92acd03:program.md:24`). Exact GPU-active minutes and replay runtime are **UNVERIFIABLE** without running it.
