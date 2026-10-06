# Prior art: "Sleeping LLM" / Per-Fact Graduated Consolidation (Baranov, 2026)

Reviewed 2026-10-06. Read-only: nothing was run, installed or cloned. Sources:
- Zenodo record https://zenodo.org/records/18779159 (WebFetch of the record page; the PDF was downloaded by WebFetch and pages 1-6 were read as images).
- Repo https://github.com/vbario/sleeping-llm, `main` at HEAD commit `661057d` (2026-03-10), read through `gh api` (contents and git tree).

Citation shorthand: `README:N` is a README.md line. `P6:N` is a line of `docs/6-Per-Fact-Graduated-Consolidation.md` (Paper 6 source; its text matches the Zenodo PDF pages 1-6 that I read; PDF pages 7+ were not read). `memit.py:N` is `src/memory/memit.py`. `note NN` is `notes/NN-*`.

---

## 1. What it is

- Author: Vladimir Baranov, independent, vlad@chatsetter.ai (Zenodo record; P6:3-4). Paper 6 of a six-paper series (Zenodo "Related Works"; README:86-92).
- Date and venue: Zenodo v1, 2026-02-25, CC BY 4.0, DOI 10.5281/zenodo.18779159 (Zenodo record). It is a Zenodo preprint. There is no peer review: the reference lists show "arXiv preprint" entries (P6:316-320) and no venue. I saw no sign of a submission.
- Title: "Per-Fact Graduated Consolidation Resolves the Capacity Ceiling in Weight-Edited Language Models".
- Plain terms: a chat assistant that, while you talk, writes extracted facts straight into MLP weights with a MEMIT-style edit (the "wake" phase). In a later "sleep" phase it fine-tunes a LoRA adapter on those facts, merges the adapter into the weights, and shrinks the MEMIT edits (scale 1.0, 0.5, 0.1, 0.0) one fact at a time once the LoRA answers correctly in chat form (README:5, README:59-70; P6:10).
- Important: the repo moved on after the paper. `src/orchestrator.py:6` says "MEMIT removed — facts stored in FactLedger, injected via system prompt". `src/sleep/full_sleep.py:3` says "5-step sleep cycle (MEMIT removed)". Note 129 (dated 2026-03-09, i.e. before the 2026-03-10 HEAD commit) gives the reason: "MEMIT edits the model's raw completion pathway — but chat uses the chat template pathway ... MEMIT serves no user-facing purpose" (note 129 lines 7-17). The README (README:5, README:29-47) and the Zenodo paper still describe the MEMIT version, so they are stale relative to the code. I treat the Feb 25 paper as the MEMIT-era snapshot.
- Repo maturity: single author (115 contributions by `vbario`; `gh api .../contributors`), created 2026-02-20, 75 stars, 5 forks, 0 open issues (`gh api repos/vbario/sleeping-llm`). Commits cluster 2026-02-21 to 2026-03-10 (`gh api .../commits`, first 100 returned: 2026-02-21 to 2026-03-10). GitHub reported `pushed_at` 2026-07-11 even though the default-branch HEAD is 2026-03-10; I did not look into the difference (UNVERIFIED: probably another ref). Four test scripts in `tests/`, no `.github/` workflows in the git tree. 122 numbered research notes in `notes/` (README:174, README:235).

## 2. Method

Storage stack in the paper's (MEMIT-era) design:
- **Write (wake).** Rank-one-style MEMIT least-squares edit on MLP `down_proj` in 8 layers (Llama 3.1 8B: layers 12-19, P6:148-154; config `lambda_reg` 0.1, 200 covariance samples). The solve is `W' = W + R K^T (K K^T + lambda C)^-1`, with C a diagonal covariance via the Woodbury identity (README:53-55; memit.py:1429-1470; diagonal estimate at memit.py:632).
- **Key.** One prompt per fact, `"{subject} {relation}"` (memit.py:71-73, memit.py:1099). The key is the MLP intermediate activation at the last prompt token (memit.py:1087, memit.py:1112-1114).
- **Value target.** v* is found by gradient descent on `-log P(target token) + kl_factor * KL(baseline || modified)` at the last prompt position only, 30 steps, lr 0.5, `v_kl_factor` 0.0625 (memit.py:1159-1229; README:181-188). Only the first token of the object is optimized: `target_token_ids[0]` (memit.py:1190). A `residual_scale = 2.0` multiplier is applied because "null-space constraints + regularization absorb ~50% of the signal" (memit.py:594-596, memit.py:801; `8b_consolidation.yaml:41`).
- **Interference control.** The key matrix contains every token position of each fact's prompt as zero-residual constraint rows, plus the last-token keys of all previously active edits as zero-residual rows (memit.py:1110-1134). Note 53 (lines 29-32) documents this as the "cross-batch null-space constraint".
- **Consolidation (sleep).** Train a rank-16 LoRA on chat-format Q&A for the active facts (30 iterations, `q_proj`, `v_proj`, `down_proj` on the last 8 layers), merge it (`merge_and_unload`), then test chat recall per fact with that fact's MEMIT delta zeroed. Facts that pass advance a stage and facts that fail retreat to stage 0 (P6:56, P6:73-79, P6:87-140, P6:157-160). Edit scale is `S[min(fact_stages)]` (P6:56, P6:134).
- **Maintenance/update.** Degraded edits (raw recall below 0.5) are reverted and re-injected with null-space constraints from the healthy edits (P6:111-114; README:57).
- **Models and scale.** Llama 3.1 8B Instruct (4-bit NF4) on 2xH100 for Paper 6 (P6:148). The README also reports Llama-3.2-3B-4bit on an M3 Air, and Llama-3.1-70B-NF4 at 60 facts (README:11-16). Fact type: synthetic person-city triples from a pool of 500 (P6:168; `experiments/data/fact_pool_500.json`, entries like Aria / lives in / Portland).
- **Recall scoring.** A fact counts as recalled if `fact.object.lower()` is a substring of a 30-token (raw) or 100-token (chat) generation at temperature 0.1 (memit.py:1040-1063).

## 3. Evidence

Claims backed by a results file in the repo:
- **Capacity sweep (Paper 6 Table 1; PDF p.6 Table 3; P6:186-191).** Backed by `experiments/results/sweep_consolidation_Llama-3.1-8B-Instruct.json`. Re-read from the JSON, per condition (5 / 10 / 15 / 20 facts, 3 cycles each, `conditions.*`):
  - baseline raw recall 1.0 and baseline chat recall 0.0 in all four conditions;
  - final chat recall 1.0 in all four;
  - final raw recall 0.8 / 0.7 / 0.333 / 0.4;
  - PPL drift +48.4% / +54.2% / +62.8% / +44.0%;
  - advancement rate 1.0 in all four;
  - stage-3 facts 4 / 7 / 11 / 0.
  - Cycle-1 raw recall after the first LoRA pass fell to 0.4 / 0.2 / 0.2 / 0.15.
  - The paper reports chat recall and advancement but not the raw-recall decline (final raw 0.333 at 15 facts); the JSON has it.
- **Wake capacity cliff (README:22).** `experiments/results/v7_convergence_ceiling_8B.json` (`phase_a.injection.trajectory`): recall 0.923 after fact 13 and 0.571 after fact 14, ending at 0.4 at 30 facts with 18 of 30 facts degraded. One-fact-at-a-time injection, 8B.
- **Interference probes (note 53 lines 42-46; note 62 lines 27-31 and 61-65).** 3 injected facts: raw recall 3/3, "Interference 0/3", "Cross-fact bleed 0/3". The probes are 3 unrelated prompts scored by substring (`experiments/test_multi_fact_memit.py` lines 21-26 as read, i.e. `INTERFERENCE_PROBES`). The bleed test asks the chat-template question for each fact and looks for the other facts' objects (same file, bleed section). Because chat-template reads do not see the edit (see below), the 0/3 bleed result is weak evidence (my inference).
- **Scale and delete primitives (note 78 lines 7-15, 39-48).** On 8B: delta persistence round trip "2/3 -> 0/3 -> 2/3"; snapshot/restore exact; scale 0.5 still recalls at 8B (not at 3B); scale 0.1 produces no recall (note 78 line 62). Residual-trace A/B: "No measurable effect of 0.1 residual" (note 78 line 35).
- **Lifecycle tests (P6:243-250).** Single cycle, two cycles, rollback and persistence on 3 facts (PASS, 7.8 min). Logs only in notes, not as a results file I could find.

Claims in prose only, or with weak backing:
- "Unbounded effective capacity" (P6:10, P6:278-284). This is an extrapolation from 3 cycles (the paper's own limitation at P6:300). No run clears stage-3 deltas and then writes new facts.
- "Cumulative fusing overcomes the alignment tax" (P6:73-79, P6:215-218). The evidence is one 3-fact run (starting loss 2.91 to 0.62); the mechanism is argued, not ablated.
- "PPL drift is domain-specific" (P6:290-292). Perplexity is measured on identity text only; the paper concedes no MMLU or HumanEval (P6:302).
- Paper 6 limitations the author states himself (P6:294-306): single scale, synthetic person-city facts only, 3-cycle horizon, no external baselines (no RAG, EWC etc.). README:251 adds "Single-run experiments — no error bars". The README also states that MEMIT edits are reachable only by raw completion, not chat templates (README:250).
- Not found: any evaluation of held-out paraphrases of a MEMIT edit, any multi-token or invented-name values, any locality metric beyond the 3 unrelated probes and identity PPL. Search evidence: `gh search code paraphrase --repo vbario/sleeping-llm` returned only `notes/27-recall-feels-worse`, where it concerns the fact-extraction firewall, not edit generalization. `gh search code locality` returned nothing. `gh search code v_kl_factor` shows the KL weight only as a fixed config value (0.0625 in `config.yaml`, `8b_consolidation.yaml:44`, note 54 line 79). It is never swept. (Search is GitHub's code index; treat absence as strong but not exhaustive.)

## 4. Relevance to the program

Tags: (a) paraphrase transfer, (b) interference between facts, (c) locality, (d) lifecycle, (e) nothing.

**(a) Paraphrase transfer. Bears on it, as an independent negative replication.**
- The sweep JSON shows edits written on one canonical raw prompt read back 1.0 on that prompt and 0.0 on a different surface form (the chat question) in all four conditions (`sweep_consolidation_Llama-3.1-8B-Instruct.json`, `conditions.*.baseline_raw_recall`/`baseline_chat_recall`). The author's diagnosis is "different token sequences = MEMIT edits are invisible to chat" (note 129 lines 7-10). The author never tries to fix this at the edit: the cure is a LoRA trained on chat Q&A (P6:87-140) and eventually removing MEMIT (note 129). The edit uses a single prompt for key and target (memit.py:1099, memit.py:1172).
- This matches the C10 shape (recalled on the canonical prompt, poor on paraphrases) in a different model, different value type (common cities, first token only) and different scorer (substring). It is evidence that the gap is general to single-prompt MEMIT, not specific to Qwen2.5-3B or invented names. It does not say why.
- Supports loop candidate (2) only in the sense that it shows nothing is gained by a single-prompt write and that the repo never attempted a multi-phrasing fit. The repo gives no number for or against a joint fit.
- Testable idea: in the program's eval, add one template-shift read class (a chat-template or question-form read) as a second held-out axis next to the 3-phrasing paraphrases, and check whether candidates (2) and (3) lift it from near 0 or only lift near paraphrases. This is cheap and checks whether the loop's gain is real surface-form transfer or only nearby-phrasing transfer.

**(b) Interference between written facts. Bears on it, indirect support for candidate (1).**
- The repo hit the same class of failure as the one behind candidate (1): "city name 'Helena' leaked into all generations when injecting 3+ facts" (note 53 lines 4-6; `test_multi_fact_memit.py` comment, "The 'Helena' problem"). Note 53 lists four fixes together (causal-mask NaN bug, covariance instead of identity regularization, per-layer residual distribution, previous-edit key constraints; lines 8-32) and gives recall before/after (0.00 to 0.80 at 5 facts, 0.00 to 0.70 at 10, lines 36-40). They were not isolated, so no one fix is credited.
- The engine already contains preserve-type rows: all non-last prompt positions of the same prompt and the last-token keys of earlier facts, each with zero residual (memit.py:1110-1134). It does not contain preserve rows at value-token positions, because the value tokens never enter the key prompt and v* is optimized on the first object token only (memit.py:1099, memit.py:1190). So the repo neither tests nor contradicts candidate (1); it shows that "zero-residual preserve rows" is the standard lever the author used against leakage.
- Capacity cliff: 0.923 at 13 facts to 0.571 at 14 (`v7_convergence_ceiling_8B.json`). With sequential writes, interference is sharp, not gradual (README:22). Different regime from the program's 72-read protocol, but a warning that preserve gains may not scale with the number of facts.
- Testable idea (control): in the program's candidate (1) run, add a matched-count arm whose preserve rows are other facts' last-prompt-token keys (the repo's approach) instead of value-position inputs. If 18/72 comes from value positions specifically, the other arm should not reproduce it. This separates "any extra preserve rows" from "value-position rows".
- Caveat on the repo: the author's null-space design preserves keys but never checks value-token leakage in a prefix-overlap setting like the program's (invented value starting with another fact's subject name). No evidence on that case.

**(c) Locality and collateral damage. Weak; mostly a caution about their metric.**
- The repo's locality evidence is 3 unrelated prompts with substring checks (`test_multi_fact_memit.py` lines 21-26) and identity-text PPL, which rose +44% to +63% after the LoRA stage (P6:186-191, sweep JSON). The author explains the PPL rise as domain-specific (P6:290-292) and admits no benchmark check (P6:302). This is not an independent check on candidates (2) or (3).
- KL: `v_kl_factor` is fixed at 0.0625 and applied only at the last prompt position (memit.py:1226-1229). It is never varied in the repo. So it gives no support or contradiction for candidate (3)'s "stronger KL penalty keeps locality checks passing". It does show that a KL term is part of the standard recipe, so candidate (3) is a tuning of an existing knob, not a new mechanism.
- Heads-up for comparisons: the repo applies `residual_scale = 2.0` to compensate for lost signal (memit.py:594-601; config line 41). If the program's engine differs on any such scaling, results will not transfer one to one.

**(d) Consolidation, update, delete, tracking. Bears on it; this is where the repo is most informative.**
- Tracking: a ledger with per-fact stage, train count and degrade count (`EditLedger`, memit.py:189-240, memit.py:318-340; note 129 line 44), deltas persisted to disk and reloaded (memit.py:406-427; note 78 lines 10, "2/3 -> 0/3 -> 2/3").
- Delete / soft-delete: `scale_edit` multiplies the stored delta by 0.0 to 1.0 and the original is kept (memit.py:929-932); `revert_edit` (memit.py:910) and weight snapshot/restore (memit.py:960-980). Note 78 lines 7-15 reports exact restore. The scale curve at 8B is graded: 0.5 still recalls, 0.1 does not (note 78 lines 12-14 and 60-62). Testable: a pre-registered "delete exactness" check: write N facts, delete k of them by subtracting their stored deltas, and require the remaining facts' reads and the unrelated-knowledge checks to equal the pre-delete values. The repo's constraints protect earlier keys from later writes (memit.py:1116-1134), not later facts from removal of an earlier delta; whether deleting a delta that later edits were solved against leaves them intact is untested there (my inference from the code).
- Update: "revert then re-inject with null-space constraints from healthy edits" (P6:111-114). The paper's own failure mode is useful: the maintenance audit read a deliberate scale-down as degradation and reset all stages (P6:254-258; sweep JSON 20-fact condition, cycle 1 raw recall 0.15). Lesson for the program's lifecycle design: any audit must know a record's intended state.
- Consolidation by fine-tuning is out of scope for a write-direct database program, and the repo itself dropped the MEMIT part (note 129). The reported cost of consolidation on the written fact is visible in the JSON: final raw recall 0.333 at 15 facts after chat recall reached 1.0.
- Relation to candidate findings: none of the three is touched; this is lifecycle framing and a test template.

**(e) Nothing.** The "Aria effect" (P6:262-264, "likely due to token-level overlap") is a guess without a test; I take nothing from it. The neuroscience mapping (README:72-80) and sleep-scheduling features (drowsiness threshold, micro-sleep) are framing only.

## 5. Verdict: CONTEXT

The work does not offer a method for paraphrase transfer: it writes one raw prompt per fact, optimizes only the first object token, scores by substring on common city names, and treats the raw-to-chat gap as a reason to add LoRA (README:250; note 129) and eventually to drop MEMIT. The headline numbers (100% advancement, chat recall 1.00, "unbounded capacity") measure a LoRA stage on 5 to 20 synthetic facts in single runs with no baselines, and are not about weight-edit quality. Its useful content for this program is narrow and mostly negative. First, an independent replication, in the repo's own JSON, that single-prompt MEMIT edits read 1.0 on the written prompt and 0.0 on another surface form, which supports treating the C10 gap as general. Second, a record that the same author's leakage failure ("Helena" in all generations) was handled by zero-residual preserve rows on earlier-edit keys, which suggests one inexpensive control for candidate (1): matched-count preserve rows of a different kind. Third, concrete lifecycle primitives (per-fact ledger, scalable and reversible deltas, snapshot/restore, an audit that misreads intended state) that can seed a pre-registered delete and update test. None of this contradicts the loop's three candidates, and none of it verifies them. I would not pre-register a test on this paper; the two cheap controls above (template-shift read class, matched-count other-key preserve arm) can be folded into existing tests if the program wants them.

UNVERIFIED items: Zenodo PDF pages 7 onward (limitations and references) were not read, so the P6 line cites for Section 7 rely on the repo's `docs/6-...md` being identical to the PDF (pages 1-6 matched); the `pushed_at` 2026-07-11 date; the claims about 70B and 3B rows in README:11-16, which I did not check against results files.
