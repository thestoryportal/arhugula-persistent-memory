# Advisor / objective-review prompt (reusable — Claude & Codex)

You are an **independent, adversarial reviewer** of a research step in the LLM-as-Database program. You are not the author. **Do not rubber-stamp.** Your job is to find where the work is wrong, over-claimed, confounded, or drifting from the goal — *before* it is leaned on.

You will be given ONE of: a **test/experiment design** (before it runs), a **finding/result** (before it is declared conclusive or written to CORPUS), or an **approach** the author is about to commit to — together with its evidence (artifact paths + numbers) and the relevant context.

Run this review and answer concisely and specifically:

1. **Real criterion.** Does this answer the question's *actual* criterion, or a flattering adjacent one? (e.g. is the metric matched to the claim — top-1 for read-correctness, distributional for distributional; is the gate's true requirement being met or a softer proxy?)
2. **Confounds & over-claims.** Hunt for confounds, leakage, Goodhart, and over-statement. Is `EVIDENCE-SHOWS` blurred with `I-INFER`? Is "the mechanism works" being passed off as "the contract is met" (**mechanics ≠ contract**)? Is design-viability being passed off as empirical evidence?
3. **Cite or flag.** Every factual claim must cite an artifact (path + exact number) or be labeled **`UNVERIFIABLE`**. Call out any claim that isn't grounded. Verify that external repos/IDs/claims were actually checked before being relied on.
4. **The overturning test.** What is the *cheapest* experiment or control that could **falsify** this finding/design? If it hasn't been run, that is the gap.
5. **Drift check.** Does this advance the F1 readiness determination (or a live §0.3 falsifier)? If not, say so.

**Output:** a short verdict — `PROCEED` / `FIX-FIRST` / `OVERTURNED-OR-RECONSIDER` — then the **single most important thing** to do next, then the specific issues in priority order. Be a skeptic; the author will weigh your input heavily but evidence remains binding over your opinion.


---

# Review packet — D-C10u-mint2 pre-registration v3 (step 3: two minted tokens per value; both arms + the V2 word list) (design pass, before freeze; 2026-10-06)

You are reviewing a **test/experiment design** before it runs: `docs/C10U_MINT2_PREREG.md` (v3, reproduced below) together with the word-list screen `experiments/track_c/c10u_mint2_wordlist.py` (reproduced below) and its record `results/c10u_mint2/v2_wordlist.json` (read it from the repo). It is step 3 of the research pass's operator-agreed sequence (`results/research_pass_2026-10-06/recommended_sequence.md`; stubs in `prereg_stubs.md`). The frozen step-1 document `docs/C10S_SHARED_Z_PREREG.md` (v3) and its reviews set the bar: no closure claims from a miss, screens vs gates, PARTIAL only outside the baseline envelope and replicated, qualifiers in the reader. Read every source the draft cites (file:line) before judging a seam claim; the draft was written from `cat -n` reads and must be held to them. The previous passes on this document are `results/c10u_mint2_advisor_v1.md` and `results/c10u_mint2_codex_design_v1.md`.

This is the **v3** of a document you (or your predecessor pass) reviewed at v1 (`results/c10u_mint2_codex_design_v1.md`, FIX-FIRST, seven items + a bigram control); v2 folded every item (§7). Since then the operator ruled (D-C10r-rulings-4 (2)) that BOTH arms are pre-registered — the redrawn value set A7-V2 and the modifier-only variant — and that the V2 word list is authored by the program session and reviewed by you before freeze. v3 adds §1.1 (the list, its rules as implemented, the tokenizer pre-screen record `results/c10u_mint2/v2_wordlist.json`, written by `experiments/track_c/c10u_mint2_wordlist.py`), the two-block design (§2), the block-F direction labels (§3) and the author's additions listed at the end of §7.

Attack in particular: (1) **the word list itself** — read `experiments/track_c/c10u_mint2_wordlist.py` and the record: is the rule set as implemented faithful to the §1 rule the v2 freeze named (no equality / prefix / substring relation with any FICTION subject, L1/L3 country, FRAME_SUBJECTS word or harness-prompt word; ≥ 2 BPE pieces), and are the two operational precisions (word-to-head relations only for names and ≥ 4-letter common words; bigram prompts excluded from P2 (a) and checked as prefix + head id) sound, or do they open a hole (e.g. a head that an AddedToken would match inside a longer prompt word in a probe the inventory does not contain)? Is extracting the inventory from the harness files by AST the right single source, and does the inventory miss any prompt the harness or the §2 probes feed (check `c10l_mint_lib.py:178–185` and the probes named in §2)? (2) **length matching** — the author changed the selection rule after seeing that the first 24 candidates gave longer strings (5–8 ids vs the frozen 4–6) and now matches the frozen heads' piece-count multiset: is matching the id-length distribution of the string baseline the right comparability control, is it sufficient, and was it legitimate to change the rule before freeze on that basis? (3) **the two-block design** — block F (frozen values: A7-multi, mint-1 ×3 seeds, modifier-only ×3 seeds) vs reading modifier-only against CORPUS/45's cross-process numbers: is the in-block mint-1(frozen) ×3 reference worth its 3 runs (≈ 2 h), and does block F's role as this session's reproduction of CORPUS/45 (comparability screen: median mint-1(frozen) ≥ 30) need a harder rule (a LAW#3-style halt) rather than a -NOT-COMPARABLE qualifier? (4) **the block-F direction labels** SECOND-WORD (min(MO) − SF ≥ 10 and max(M1F) − min(MO) < 10) / HEAD-WORD (max(MO) − SF < 10) / MIXED — same false-positive analysis you ran on the block-V2 rule: can init spread alone (CORPUS/46 seeds 46/34/36, range 12) produce SECOND-WORD, and is "max(M1F) − min(MO) < 10" the right form for "reaches the mint-1 range"? (5) **arm B's bigram control** under the frozen set's sharing (each head on two subjects, each modifier on three): does the swapped-subject condition as specified (a subject sharing neither head nor modifier) still discriminate a bound fact from a head-word→modifier continuation? (6) **the head→modifier uniqueness of V2** (every head identifies its modifier) — v2 already flagged the shortcut; is the bigram control enough, or does V2 need the frozen set's sharing structure replicated (some heads reused across subjects) to keep the pairing problem comparable? (7) anything in §1.1's hashes/records that is not reproducible from the script and the harness files alone.


Verdict: PROCEED (freeze as v3) or the single thing to fix, then the issues in priority order. Nothing has run on the model; the GPU is held by the autoresearch loop; runs occur only on the operator's go.

## docs/C10U_MINT2_PREREG.md (v3)

# Pre-registration — D-C10u-mint2: the coined value as two minted tokens, one per word (step 3 of the research pass's recommended sequence; H-19) (v3, 2026-10-06)

**Status: v3 — the V2 word list is authored and tokenizer-screened (§1.1; record `results/c10u_mint2/v2_wordlist.json`, heads sha256 `7d83a89f…`), and BOTH arms are folded per the operator's ruling D-C10r-rulings-4 (2) (`D-C10u-A7V2`): arm A = the redrawn value set A7-V2 written as two minted ids; arm B = the frozen values with only the modifier minted. v3 goes to the advisor pass and the Codex GPT-6-Astra design pass before freeze; runs only on the operator's go.** Decision-ID `D-C10u-mint2`. Reviews folded so far: advisor pass `results/c10u_mint2_advisor_v1.md` (FIX-FIRST) and Codex GPT-6-Astra design pass `results/c10u_mint2_codex_design_v1.md` (FIX-FIRST, seven items + a cheapest overturning control); the fold log is §7. Nothing has run on the model; the only code is the tokenizer-only word-list screen `experiments/track_c/c10u_mint2_wordlist.py` (no model load, no edit).

Source lead: research pass 2026-10-06, H-19 (`results/research_pass_2026-10-06/hypotheses.md:193–198`; `recommended_sequence.md:22`, appendix `:49`; `prereg_stubs.md` §Shared contract `:5–13`, §Step 3 `:37–44`), with the council items the H-18 addendum attaches to any embedding-side write (`hypotheses.md:314–316`; `council_critique.md:10, :23, :52, :59–60, :69, :94`). Lineage: CORPUS/45 ⟨D-C10l-mint@a4a6f4c7⟩ (one minted token per value: PARTIAL in all five replicates, 34–46/72; A7-multi 11/72; A1-rare 25–29; P4 compiled-artefact gate PASS), CORPUS/46 ⟨D-C10m-diag@9a9b5343⟩ Q3 (N init SEED-SENSITIVE: seeds 0/1/2 = 46/34/36, range 12/72 against a ±4–5 process spread; F-D4: init comparisons need ≥ 3 seeds). Rulings in force: D-C10k-rulings-1 (strict held-out bar; a minted token is a Git/.vindex artefact under ruling 3), D-C10r-rulings-2/-3 (write-only; the agreed sequence — it accepts the sequence, not this redraw, `EXPERIMENT_RUNBOOK.md:324`). Every engine/library/harness statement is cited to a line read on 2026-10-06 (LAW#4).

## 0. Where this sits, and what it is

The **§C write path**, read against the **§8.9 bar** (`spec:388`), on the **mint harness** of CORPUS/45: engine unmodified; the value's vocabulary representation is changed before the solve. CORPUS/45 removed the span entirely (one id per value) and lifted held-out transfer from 11 to 34–46/72, leaving F-M4 open: how much of the residual gap is the *length* of the value and how much the *novelty of the pair*. Arm A puts one point between the two ends on a redrawn value set: each coined word gets its own minted id, so the value is a two-id sequence whose second id is predicted from a context that already contains the first. Arm B puts a second point on the frozen values themselves: the head stays BPE pieces and only the modifier is minted, which asks whether the string arm's loss sits in its second word (§1). **The e2e map:** write layer, representation of the value at the tokenizer/embedding boundary (outside the §8.1 FFN compile, `spec:307`; §4). **In §0.3:** step 3 of the agreed sequence, a diagnostic lead, not a falsifier; it runs after steps 1–2 unless the operator reorders.

**What this experiment can and cannot conclude.** A pass advances a candidate representation. A miss at any stage means *this candidate configuration was not advanced* (one init kind, three seeds per arm, one value set per block, N = 24); it does not close H-19 or F-M4. The direction labels of §3 are a **routing signal for the sequence whose false-positive rate is UNVERIFIABLE from the historical totals** (Codex item 2); they identify nothing causally. CORPUS/45's qualifiers apply: not route viability, not an init-quality statement, no change to the F1 C10 status.

## 1. Question, hypotheses, and the value-set amendment

- **H-19 (span):** writing "<head> <modifier>" as two minted ids (init N) lands between the one-token mint and the multi-token string on the binding count, with the loss at the second id. Stub: `hypotheses.md:194–196`.
- **H-19-null (pair novelty — the prior):** the two-id value lands with the string: the second id must be predicted from a (head, subject) context the model has never seen, and the solve supervises it only through the single key displacement (§2); CORPUS/46 F-D4 says a difference under 12/72 is within what the init alone produces.
- **H-19-tradeoff:** the ordering holds but a locality, perplexity, write-size, false-fire or bigram gate fails.

**The frozen A7 values cannot be split-minted (departure 1, confirmed by both reviews).** `build_stimuli` assigns heads by `coined_head[(i*2+1) % 24]` and modifiers by `coined_mod[(i*3+2) % 24]` (`c10e_bandknob.py:246–249`): 12 distinct heads each on two subjects, 8 distinct modifiers each on three; 8 heads (Drennik, Vythorn, Vorlex, Kessivar, Halquin, Marsduq, Glimsto, Fluvane) are `FICTION` subjects (`:57–61`), three (Lurmax, Brindu, Yastov) are subject prefixes; `register` uses `single_word=False` (`c10l_mint_lib.py:26`). Codex's tokenizer-only check (`results/c10u_mint2_review_tokenizer_check_20261006-133250.json`, no model load): under the existing registration **33/96** CANON+PTEST prompts change tokenisation; with `single_word=True` **0/96** change but **0/24** target pairs encode as the two minted ids (and the 8 exact collisions remain — advisor item 2). Step 0's P2a (`c10l_mint_step0.py:63`, halt `:70`) would fail by construction.

**Resolution — both arms, by the operator's ruling D-C10r-rulings-4 (2) (`D-C10u-A7V2`; advisor item 2, Codex item 1 asked for the ruling).** The ruling makes the redraw and the fallback two arms of one pre-registration, each in its own comparison block (§2):

- **Arm A — A7-V2, two minted ids.** V2 = 24 values from 24 new heads × the 24 `coined_mod` words (`:234–238`, injective: head *i* pairs with modifier *i* for subject `FICTION[i]`). The heads are authored by the program session under the rules of §1.1, screened with the base tokenizer, and SHA-256-hashed (`lib:174–175`) into step 0 with the relation table. **What V2 changes, stated plainly:** (i) the head identities; (ii) the shared structure of the frozen set (12 heads × 2, 8 modifiers × 3) — in V2 every head uniquely identifies its modifier, which permits a head→modifier shortcut without continued subject dependence (Codex I-INFER), so the pairing problem itself is different and the §3 bigram control is mandatory; (iii) comparability — the frozen stimuli are the instrument behind every CORPUS/39–50 A7 number, and matching envelopes cannot restore it; what *is* matched is the string length (§1.1), so the string baseline of block V2 has the frozen values' id-length distribution. All three arm-A conditions run on V2 in one block; CORPUS/45 is context, not the comparator. The redraw carries its own Decision-ID line, `D-C10u-A7V2`, in runbook §5.
- **Arm B — modifier-only minting on the frozen values.** The 24 frozen A7 values stay as they are; only their 8 distinct modifiers (Vask, Brakk, Stavik, Yornel, Spraxil, Ulvenn, Cindel, Drelth — `coined_mod[(i*3+2) % 24]`, in first-use order) are registered, so each target becomes the head's base BPE pieces followed by one minted id (3–4 ids; `results/c10u_mint2/v2_wordlist.json` → `modifier_only`). P2a-clean by construction: A7 value strings are excluded from `all_harness_prompts` (`lib:180`), the modifiers are not subjects, and the pre-screen finds 403/403 inventory prompts unchanged. It keeps the frozen stimuli (CORPUS/45 comparability through the same-block mint-1 and A7-multi references) and forfeits the uniform two-id value: it tests whether the frozen string's loss sits in its *second word* (**H-19-B**: minting the modifier alone recovers the one-token mint's count) or in the multi-piece head (**H-19-B-null**: it gains nothing over the string). The three-word-per-modifier sharing of the frozen set is kept, so the §3 bigram control reads differently here (a modifier shared by three subjects cannot be a subject-independent continuation of one head, but can be of the head *word*, which is also shared by two subjects).

A non-word-boundary split of the frozen strings is not adopted (abandons "one per word", needs its own P2 audit). The two blocks are read side by side and never pooled: they are different stimuli.

### 1.1 The V2 word list (authored 2026-10-06; frozen with this document)

**Rules, as implemented in `experiments/track_c/c10u_mint2_wordlist.py` (the pre-screen; step 0's P2 on the engine's tokenizer object is the binding admission).** Every protected word is extracted from the harness files, never retyped: the 24 `FICTION` subjects, the 6 `FRAME_SUBJECTS` (`c10p_twopass_arms.py:30`), every country and capital of both g6 screens (`configs/screens/g6_screen_qwen3b*.json`; L1/L3 are subsets, `bandknob:259–278`), the 24 `coined_head` and 24 `coined_mod` words, the words of `CANON`, `PTEST`, "is described as", "is a", "is associated with", the 20 `GENERIC` sentences, the 10 `UNRELATED` prefixes (`lib:13–17`) and the LAW#5 strings — 385 distinct words, inventory sha256 `a2b73c67…`. A head must be alphabetic and capitalised; it must stand in **no** relation to any inventory word: *equality*; *head a prefix of the word* and *head a substring of the word* (every word, any length — a registered " Head" would re-tokenise any word it prefixes); *word a prefix of the head* and *word a substring of the head* (every name, any length; common words of ≥ 4 letters — one- to three-letter function words such as "a", "is", "he" would otherwise forbid nearly every string). Each head has ≥ 2 BPE pieces in the base tokenizer (so the string baseline stays multi-token); the 48 registered words (heads + modifiers) stand in no prefix or substring relation to one another. **Selection:** passing candidates are taken in authored order *until the head piece-count multiset equals the frozen A7 heads'* (6 heads of 2 pieces, 18 of 3), so the V2 string baseline has the frozen values' length distribution (frozen values: 1 × 4, 10 × 5, 13 × 6 ids; V2: 1 × 4, 11 × 5, 12 × 6). Fifty-six candidates were authored; all pass; the first fit of the quota is the list.

| subject | V2 value | head pieces | string ids |
|---|---|---|---|
| Zorbland | Tarvesk Zentra | 3 | 6 |
| Quaxil | Molquenn Ploom | 3 | 5 |
| Plurnak | Fendrax Vask | 3 | 5 |
| Vythorn | Ulbrisk Threnn | 3 | 6 |
| Glimsto | Kalvoth Wyxen | 3 | 6 |
| Drennik | Pelthorn Brakk | 3 | 5 |
| Yastovel | Vustrim Voneth | 3 | 5 |
| Crulpane | Gorvande Qurel | 3 | 6 |
| Mophgar | Hexmoril Stavik | 3 | 6 |
| Brinduun | Wolqetz Dwelos | 3 | 6 |
| Trannak | Dravnisk Phaxis | 3 | 5 |
| Skornwell | Nalthrik Yornel | 3 | 6 |
| Fluvane | Skevrond Klavor | 3 | 5 |
| Oxbarrow | Cravnolt Druvik | 3 | 6 |
| Zephquin | Yembrisk Spraxil | 3 | 6 |
| Lurmaxen | Mirquand Velmor | 3 | 6 |
| Pradnoll | Faldrix Gantho | 3 | 6 |
| Kessivar | Thanvorl Ulvenn | 3 | 6 |
| Wombryne | Torvak Treska | 2 | 5 |
| Halquin | Kurvin Bloraq | 2 | 5 |
| Vorlex | Zandel Cindel | 2 | 5 |
| Quenby | Garnoth Marvox | 2 | 4 |
| Marsduq | Tomrik Ossquin | 2 | 5 |
| Thelby | Selvor Drelth | 2 | 5 |

Heads sha256 `7d83a89f3f893d615ded1ff9c1985eba0ae66063760a61886201a27b2a906c8f` (the 24 heads joined by newlines); values sha256 `1fb4f9b0…` (the subject→value map as sorted JSON); arm-B modifiers sha256 `402144a2…`. **Pre-screen results (base tokenizer, `Qwen/Qwen2.5-3B` @ `3aab1f19…`, 2026-10-06 14:45):** after `register(heads + coined_mod)` (ids 151665–151712) every one of the 48 words is one id, 24/24 values tokenise as `[ĥ_head, ĥ_mod]`, 24/24 `CANON(subject) + value` tokenise as the prompt's ids plus the pair, 403/403 inventory prompts tokenise identically before and after, and all 576 bigram-control prompts `CANON(subject) + head` tokenise as the prompt's ids plus `[ĥ_head]` — these prompts contain the minted head by design and are checked by that rule, not by P2a (a precision to the v2 wording of P2 (a)). For arm B, after `register` of the 8 modifiers (ids 151665–151672): 24/24 frozen values end in the minted modifier id, target lengths 3–4, 403/403 inventory prompts unchanged. The hashes, the rule text and the full relation table are in the record; step 0 recomputes P2 with the engine's tokenizer and halts on any difference.

## 2. Design (engine unmodified; driver on the `c10l_mint_lib.py` primitives through the harness seams `ARM_HOOKS` and `Z_OVERRIDE`; one step 0 per (arm kind, seed); comparison blocks replicated in fresh processes)

**Registration and initialisation (`c10l_mint_lib.py`).** `register(tok, values)` adds one `AddedToken(" " + v, normalized=False, lstrip=False, rstrip=False, single_word=False)` per string (`:24–27`), fails closed on fewer tokens added than strings (`:27–29` — V2 must have 48 distinct words), asserts contiguous ids from `SPARE_START = 151665` (`:10`, `:30–32`; 271 spare rows to `VOCAB_ROWS = 151936`, `:11`) and `tok(" " + v) == [id]` (`:33–36`). Mint-2 registers the 48 words (24 heads then 24 modifiers; ids 151665–151712); mint-1 the 24 whole strings (`minted_strings`, `:20–21`; ids 151665–151688) — on V2 in block V2, on the frozen values in block F; arm B registers the 8 frozen modifiers in first-use order (ids 151665–151672). `assert_tied` (`:44–48`): each row is also the output row. **Initialisation fact (corrected, Codex item 3):** `build_init(..., "N", seed)` draws rows sequentially from one `torch.Generator().manual_seed(seed)` (`:72`, `:84–86`), so **the first 24 of the 48-row N(seed s) equal the 24-row N(seed s)** — mint-1's 24 value rows and mint-2's 24 head rows are the same vectors, and arm B's 8-row N(seed s) is the first 8 rows of both; this pairing is kept and hashed (`sha256_tensor`, `:162–163`; rows checked by the driver, `c10l_mint_arms.py:99–101`). `set_rows` (`:95–97`) is the only embedding write; `get_rows` (`:100–101`).

**What one request with a two-id target does in the solve (`memit_dry_run/memit/memit/compute_z.py`).** One request per fact, `{"prompt": CANON, "subject": c, "target_new": {"str": " " + value}}` (`bandknob:96–97`, `:480`); `my_edit` solves one `z` per request (`:191`). `compute_z` tokenises the whole target (`:41–43`: `[ĥ_head, ĥ_mod]` for mint-2), builds rewriting prompts as `context.format(prompt) + decode(target_ids[:-1])` (`:46–50`, the head appended as text), places both ids at the last two target positions (`:60–65`), adds one `delta` at the key (`:98–99`) — **the subject's last token** (`find_fact_lookup_idx`, `:68–73`), with the frame tokens " is the city of" (`bandknob:51`) between the key and the value slot (seam fix, Codex item 7) — averages the per-position NLL over the target length (`:149`) and over prompts (`:150`), adds the KL term on `"{} is a"` (`:50`, `:127–128`, `:151–153`) and weight decay (`:154–156`), stops below 0.05 (`:164`) — **the stopping rule is not touched** (Codex item 4) — clamps (`:175–178`) and returns `z = target_init + delta` (`:180`). The printed "avg prob" is `exp(−nll_each).mean()` (`:162`): the **mean over prompts of each prompt's geometric mean over positions** (advisor item 5) — one number per value, not per position.

**Capture of the solved targets (seam fix, Codex item 7).** `ARM_HOOKS` run after `my_edit` (`bandknob:494–495`) and `_ARM_STATE` is read-only solve state without `zs` (`:409–412`); `zs` is local to `my_edit` (`:191`). Mechanism adopted for the implementation review: the driver solves the 24 targets itself with the engine's own `compute_z` on the process-global context templates (`memit_main.py:304–308`) and supplies them through `Z_OVERRIDE` keyed by (subject, target string) (`bandknob:185–189`, `:405–408`), so the write's target and the captured `z` are one object; `Z_OVERRIDE_HITS` must equal the number of A7 arms in the process; the override is never consulted in the LAW#5 check (`:406`), which must pass in every process. **Frozen context set per comparison block (Codex item 2):** the first process of a block writes `CONTEXT_TEMPLATES_CACHE` to a file; every later process of the block sets that module global from the file before any solve — a driver assignment, no engine edit; the templates' hash enters every run record.

**Step 0 admission (no write; one file per (arm kind, seed); fail-closed as coded):**
- **P1** fingerprint `d941a9fb` (`C10L_MINT_TOKEN_PREREG.md:104`), `_cov_cpu == 3`; LAW#3 reference with A1/A2 ≥ 68 (`arms:31–34`).
- **P2, extended (Codex item 7; precision at v3):** (a) identical tokenisation before and after registration over `all_harness_prompts` (`lib:178–185`) **plus** the probes this arm adds (the six `FRAME_SUBJECTS` prompts, the `GENERIC` sentences, the `is_a`/`associated_with` probes) — count must equal its denominator (`step0:63`, halt `:70`); the bigram-control prompts contain a minted head by design and are checked instead as `CANON(subject) + head == CANON ids + [ĥ_head]` for all 24 × 24; (b) `tok(" " + word) == [id]` for all 48 (`lib:33–36`) and `tok(" " + head + " " + modifier) == [ĥ_head, ĥ_mod]` for all 24 with the engine's tokenizer object (`compute_z:41–43`, `tgt_ids` `bandknob:67–68`); for arm B, `tok(" " + modifier) == [id]` for the 8 and each frozen value tokenises as its head's base pieces followed by the modifier id, 24/24; (c) the in-context last-id check (`step0:63`). The pre-screen values of all of these are in §1.1; step 0 recomputes them.
- **P3, two instruments (advisor item 5, Codex item 4):** *admission screen* = the engine-log aggregate ≥ 0.98 on ≥ 22/24 values (`step0:30–40`; `C10L_MINT_TOKEN_PREREG.md:34`, `:100`), with any value under 0.98 marked **UNDERFIT** in the 24-vector; *mechanism instrument* = **per-position fit at stop for all 24 values**: the driver injects the returned `z` at the key on the identity-template CANON prompt (the overwrite equals the solve's own intervention there, since `target_init` is recorded from prompt 0, `compute_z:95`, and `z = target_init + delta`) and reads p(ĥ_head | prompt) and p(ĥ_mod | prompt + ĥ_head) at the final output — recorded beside the solve's loss-layer readout (`:76`, `:137–140`), whose difference is logged. A value with either position < 0.98 is UNDERFIT and is **dropped from the per-position curve with `n` reported**; UNDERFIT values count as misses in the binding count, never as evidence about the span.
- **I-11** (`lib:122–145`, classes `:133–138`; exclusions `step0:91–92`): head id probed at the value slot as `i11_probe` does (`:128–130`); modifier id probed at the value slot (mis-order, counted) and teacher-forced after the head. Step-0 recall = `full_seq_match` over both ids (`bandknob:109–117`), not the first-id `para_hits` (`lib:134`), so binding = post − pre compares like with like (`arms:116`).
- **Geometry:** `piv_stats` (`lib:104–111`) on the 48 rows vs a random-base-row reference of the same count (`step0:75–76`; collapsed rule `:89`). The rows are unchanged by the write (`set_rows` is the only embedding write), so post-write geometry is reported on the captured `z` block and the post-edit value-slot hidden states on the 72 held-out prompts (departure 3).

**Arms and blocks (A1 in every run, `arms:17`).** A **comparison block** = one frozen context set and one value set. **Block V2 (arm A):** (i) **A7-multi(V2)** (tokenizer untouched; `multi_hook`, `arms:71–84`); (ii) **mint-1(V2), N seeds 0, 1, 2** (the 24 whole V2 strings as one id each); (iii) **mint-2(V2), N seeds 0, 1, 2** (`tgt_ids` assertion `arms:104–106` becomes the pair; `multi_hook` attached to every arm for the per-position curve; `mint_hook` first-position counts kept, `arms:53–56`). **Block F (arm B, the frozen values):** (i) **A7-multi(frozen)** — the harness's standing A7 arm; (ii) **mint-1(frozen), N seeds 0, 1, 2** — CORPUS/45's recipe re-run in this session as the in-block upper reference; (iii) **modifier-only, N seeds 0, 1, 2** — the 8 modifiers minted, heads as BPE pieces, targets of 3–4 ids, the same per-position instrument over every target position. Seven runs per block; the two blocks share nothing but the harness and are never pooled. **Matched 48-row mint-1 control (Codex item 3), conditional:** mint-1(V2) with 48 rows registered — the 24 value strings plus 24 extra minted words never used in any target, same 48-row N(seed) — at seeds 0, 1, 2, run before any SPAN-DIRECTION label is carried, to separate output-row competition from sequence length. **Comparability screen (advisor item 6, Codex item 1), per block:** the block's A7-multi inside the reader envelope `para_full [11, 18]`, `canon [5, 10]`, `para_first [48, 62]` (`c10l_mint_read.py:9`) **and** the median of its three mint-1 seeds ≥ 30/72 (block F's mint-1(frozen) is also this session's reproduction of CORPUS/45's 34–46 and CORPUS/46's 46/34/36); failure → that block is read internally only and every one of its labels carries **-NOT-COMPARABLE** (no reference to CORPUS/45's counts); it is not a halt and not a claim that the stimuli are invalid. **Replication (gate A):** any direction label, LEAD or PARTIAL is replicated as a fresh-process block on the same frozen context set and the same inits. Runtime ≈ 40 min per mint pass (`prereg_stubs.md:44`): 14 runs for the two blocks (≈ 9.5 h), the control 3, replication 7 per block replicated; step 0 ×4 (arm kinds mint-1(V2), mint-2(V2), mint-1(frozen), modifier-only) × 3 seeds. Output `results/c10u_mint2/`; reader `c10u_mint2_read.py` **encodes every gate below** (A1 ≥ 68, the range rules, `string ≥ full`) — the CORPUS/45 reader's `A1 < 58` (`read:54`) is not inherited (advisor item 7).

**Readout per arm (harness `eval_arm`, `bandknob:358–400`), three columns kept distinct (Codex item 5):**
- **Raw id correctness** `para_full_n` (`full_seq_match`, `:109–117`); **binding** `para_full_binding_n` = raw − step-0 recall (`arms:112–120`).
- **Behaviour (§21.4 judgment, frozen here):** `judgment_method = exact_substring` = the decoded response **contains** `" " + value`, case-sensitive (`spec:1552`); greedy; budget = `n_tokens + 2` ids with no early stop (`string_match`, `:121–130`, declared as a narrow assay, not prescribed by §21.4); the harness's own `startswith` count (`:130`) is reported beside the contains count, computed by a hook on the same decode. A string hit through different ids is **alternative tokenisation** (`alt_tok_n = string − full`; the mint prereg's P5 outcome, `C10L_MINT_TOKEN_PREREG.md:36`), not a defect; **`string < full` halts** (advisor item 4).
- Decomposition `canon_full_n`, `para_first_n`, `tf_pertok_cont`, `cond_full_given_first` (`:377–392`); per-fact 24-vector (`:497`); per-edge rule 3/3 templates. **Per-position curve** `per_position_teacher_forced` (`arms:84`; comparator CORPUS/45:24 for the frozen values).
- Locality: `para_sibling`, `post_write_cannibal` (`arms:55–57`); ΔW per layer (`:498`); `generic_ppl` pre/post (`:315`, `:337`); L1, `described_as`, L3 (`read:20–23`); same-frame fictional `frame_probe` over `FRAME_SUBJECTS` (`c10p_twopass_arms.py:28`); **minted-id false-fire** (`council_critique.md:52`, `:234`): top-1 ∈ minted ids on the 12 L1, 30 L3, 6 same-frame, 10 unrelated prompts (`L1_flipped_to_minted`, `p4:67`) and the emission rate at every position of a greedy continuation of each `GENERIC` sentence — reported, not gated (no threshold in the sources).
- **Bigram control (Codex's cheapest overturning control; council `:69`), no extra write:** after the mint-2 edit, teacher-force each head id after CANON with (i) its correct subject, (ii) a swapped edited subject, (iii) each of the six never-edited `FRAME_SUBJECTS`; record the top-1 at the modifier position per head and condition. For arm B the same three conditions, teacher-forcing the head's base pieces after CANON and reading the top-1 at the modifier position; (ii) uses a subject that shares neither the head nor the modifier with the probed fact (the frozen set shares each head between two subjects and each modifier among three).
- **P4 GGUF chain, namespaced (Codex items 6–7; advisor item 3):** `tools/c10l_mint_p4.sh:11–15` hardcodes `results/c10l_mint` and `c10l_mint_N_*` — a `c10u_mint2_p4.sh` with `results/c10u_mint2/` and `c10u_mint2_*` names is written at implementation. The arm saves, per prompt, the expected id sequence and the HF greedy sequence of the same length (extending `arms:61–65`); the probe scores **subject-specific full-sequence correctness** (mint-2: position 0 `== ĥ_head(k)`, position 1 `== ĥ_mod(k)`, `n_predict: 2`; arm B: the head's base pieces then `ĥ_mod(k)`, `n_predict` = the target length), not `gid in MINTED` (`p4:58`, which would score a modifier-first or sibling answer correct). Tokeniser gates: every minted id (48 for mint-2, 8 for arm B; `p4:45–49`) and 24/24 target sequences in both GGUFs. **Compiled-artefact gate** = 24/24 canonical full-sequence HF↔fp16 parity; held-out parity and the Q4_K_M retention are reported separately, never gated. P4 runs on the mint-2 and arm-B configurations that carry a LEAD or PARTIAL label.

## 3. Pre-registered readings (counts; v2 — frozen after the read-through and the operator's acceptance)

**Validity (any failure → INVALID):** P1; P2 (a)(b)(c); P3 admission screen; no I-11 exclusion; A1 ≥ 68/72 in every run (`prereg_stubs.md:10`); LAW#5 |Δexpr| ≈ 0 in every process; `Z_OVERRIDE_HITS` as specified; the V2 head list (sha256 `7d83a89f…`), the arm-B modifier list (`402144a2…`), the rules, the relation table, the context-template hash and the row-pairing hashes in every record; `string ≥ full` for every arm.

**Labels per arm (binding; comparator = the same-block A7-multi — V2 for block V2, frozen for block F):** **LEAD** ≥ 30/72 with all gates, replicated (gate A) else **LEAD-NOT-REPLICATED**; **PARTIAL** gain ≥ 10/72 over A7-multi, < 30, gates hold, replicated with gain ≥ 10 else **PARTIAL-NOT-REPLICATED**; a count inside [11, 18] is **NULL** whatever the gain; **TRADEOFF** = PARTIAL- or LEAD-sized gain with a gate miss; **NULL** otherwise (not advanced). Each seed is a configuration with its own label; the seed range is reported against CORPUS/46's 12/72.

**Direction test (advisor item 1, Codex item 2; non-overlapping ranges, never index-pairwise).** With M1 = {mint-1 binding, 3 seeds}, M2 = {mint-2 binding, 3 seeds}, S = A7-multi `para_full_n`, all in one block, and the block valid, every fit screen passed and locality clean:
- **SPAN-DIRECTION** if min(M1) − max(M2) ≥ 10 **and** min(M2) − S ≥ 10, in the block and in its replication block, **and** the matched 48-row control gives min(M1-48) − max(M2) ≥ 10 (otherwise the difference is attributed to output-row competition and the label is **COMPETITION**, not span). It buys: the token route stays the lead; the closed-form H-18 variant enters the queue after gate A (`prereg_stubs.md:43`).
- **PAIR-DIRECTION** if max(M2) − S < 10 in both blocks (mint-2 did not gain over the string by the PARTIAL margin in any seed). It buys: token-representation tricks move below steps 5–7. The v1 proximity rule |M2 − S| ≤ 5 is withdrawn (both reviews); the stub's "token tricks close" (`:43`) is not adopted.
- **MIXED** otherwise; no direction is taken. **-BIGRAM** qualifier on any direction label if, in the bigram control, the modifier fires under swapped or never-edited subjects on at least as many prompts as under the correct subject (a subject-independent head→modifier continuation, not a bound fact). The per-position curve (UNDERFIT values dropped, `n` shown) is read beside the label: loss concentrated at position 1 is recorded as the carrier-across-the-frame reading; loss at position 0 means the curve cannot speak to the span.

**Block F reading (arm B; same non-overlap form).** With MO = {modifier-only binding, 3 seeds}, M1F = {mint-1(frozen) binding, 3 seeds} and SF = A7-multi(frozen) `para_full_n`, block valid, fit screens passed, locality clean:
- **SECOND-WORD** if min(MO) − SF ≥ 10 **and** max(M1F) − min(MO) < 10, in the block and in its replication block: minting the modifier alone brings the frozen string into the one-token mint's range, so the string arm's loss sits in its second word. It buys: the head's multi-piece span is not the wall on the frozen set; a head-only mint (the mirror arm) is the next cheapest point.
- **HEAD-WORD** if max(MO) − SF < 10 in both blocks: minting the second word buys nothing over the string; the loss sits in or before the head pieces. It buys: nothing on the frozen set compresses short of the whole value; block V2's reading carries the span question alone.
- **MIXED** otherwise. **-BIGRAM** as above on arm B's own control. The per-position curve over the 3–4 target positions is read beside the label (loss at the minted last position vs. loss inside the head pieces).

The two blocks' readings are reported side by side (one table, two rows) and never combined into one label.

**Locality gates (vs same-block A7-multi, `prereg_stubs.md:10`):** L1 ≤ reference + 1 (of 12); same-frame fictional ≤ reference + 1 (of 6); `described_as` ≥ reference − 3; L3 ≥ 29/30 (`read:10`); generic perplexity rise ≤ 0.5; `post_write_cannibal` ≤ 2, `para_sibling` ≤ 3 (`read:62`); a minted-id top-1 on any L1, L3 or same-frame prompt is that gate's miss; `is_a` / `associated_with` flips counted. **Qualifiers:** ‖ΔW_arm‖ / ‖ΔW_multi‖ > 1.5 → **-LARGE-WRITE** (`:10`); row norm reported as minted mean norm / base mean norm (`piv_stats.mean_norm`, `lib:111`; norm-matched init, `lib:69`, `:86`).

## 4. Not claimed, whatever the outcome

No label in CORPUS/44–50 changes. No outcome closes H-19, F-M4 or the step 1–2 questions. A pass is "edge stored under one relation label" on a two-id value (arm A) or a pieces-plus-one-id value (arm B): not graph storage, not route viability (48 or 8 of 271 spare rows, `C10L_MINT_TOKEN_PREREG.md:26`; lifecycle C5/C9 untested), not an init-quality statement. V2 counts are never compared with CORPUS/45's as if the same instrument; block F's counts are compared with CORPUS/45's only through the in-block mint-1(frozen) and A7-multi(frozen) references, and a block-F label is a statement about the frozen values' second word, not about two-id values. Arm B's modifier-only result and arm A's two-id result are not two measurements of one quantity. The engine is untouched; the harness gains no new seam (`ARM_HOOKS` `bandknob:404`, `Z_OVERRIDE` `:405–408`). **Spec-amendment flag (council `:10`, `:23`, `:59–60`, `:94`; `hypotheses.md:316`):** a minted row sits outside the §8.1 FFN compile (`spec:307`); a §8.10 anchor re-run (`spec:402`) has no procedure that re-derives it from a `.larql` patch — here the row is `randn` from (kind, seed, row index) (`lib:72`, `:84–86`), regenerable from a recorded seed, which is weaker than "derivable from the patch" and must be placed in the §8.4 tier stack (`spec:324`) as a frozen or seed-regenerated artefact; compaction survival is **undefined until measured** (the `COMPACTION_REGRESSION` probe, council `:94`, is owed before any route claim). This arm carries **"spec-amendment: §8.1 / §8.4 / §8.10 — embedding-side write; compaction procedure undefined"**, not "none" (`hypotheses.md:197`).

## 5. Halt discipline and close-out

One speculative fix after a `cat -n` read, then HALT with a diagnostic JSON (`architecture_profile/sNNN_halt_diagnostic.json`). Predicted halts: P2 failing on V2 with the engine's tokenizer object where the pre-screen passed (one fix = the offending head replaced by the next passing candidate of the same piece count in the authored order of `c10u_mint2_wordlist.py`, the record re-written and re-hashed, then HALT if P2 fails again); an arm-B frozen value whose registered tokenisation is not its head's base pieces plus the modifier id (no fix — a tokenizer fact; HALT); P3 screen < 22/24 → UNDERFIT, no behavioural run; `string < full`. Close-out through `tools/closeout_check.py D-C10u-mint2` once the CORPUS entry exists. Codex GPT-6-Astra (high) at the implementation review, the verdict, and the promote gate if LEAD. The GPU belongs to the autoresearch loop while it runs; this arm runs only on the operator's go.

## 6. Reviews and remaining open points

v1 draft → advisor pass → Codex design pass → v2 → lead read-through → operator ruling D-C10r-rulings-4 (2): both arms → word list authored and screened → **v3 (this file)** → advisor pass on v3 → Codex design pass on v3 → freeze → implementation (driver, `i11_probe` two-id and pieces-plus-id extension, per-position fit instrument, `Z_OVERRIDE` capture, context-set freeze, bigram control for both arms, `c10u_mint2_p4.sh`, reader) → implementation review → step 0 → blocks → P4 → verdict → CORPUS entry. For the operator at the go: the budget — 14 runs (two blocks of 7, ≈ 9.5 h of GPU) + 3 conditional control runs + 7 per replicated block; the loop is paused for the whole of it (D-C10r-rulings-4 (1)). Open for the implementation review: the `Z_OVERRIDE` capture and the context-set freeze are the two new behaviours to prove inert.

## 7. Review fold log (one line per item)

- Advisor "most important" / Codex 2 (two seeds, index-pairwise, same session) → folded: three seeds per mint arm (F-D4), ranges compared as min/max non-overlap, frozen context set per block (`memit_main.py:304–308`), fresh-process replication block (§2, §3).
- Advisor 1 / Codex 2 counterexample (latent M1 = M2, observed 36/26 passes) → folded as stated: the false-positive rate is UNVERIFIABLE from the historical totals; direction labels are routing signals, not identification (§0, §3).
- Advisor PAIR-DIRECTION / Codex "proximity screen" → folded: |M2 − S| ≤ 5 withdrawn; PAIR-DIRECTION = max(M2) − S < 10 in both blocks (§3).
- Advisor 2 / Codex 1 (V2 is a two-axis change; operator ruling; NOT-COMPARABLE) → folded: A7-V2 labelled a scope amendment needing operator acceptance, Decision-ID `D-C10u-A7V2`; the head→modifier uniqueness and its shortcut risk stated; screen failure = -NOT-COMPARABLE qualifier, not INVALID-STIMULI, not a halt (§1, §2).
- Advisor 2 (`single_word=True` not a fix; modifier-only dismissed without argument) / Codex 1 tokenizer check (33/96; 0/96 but 0/24 pairs; modifier-only 3–4 ids) → folded: the counts cited from the artifact; modifier-only is the named fallback with its tradeoff; the non-word-boundary split noted and not adopted (§1).
- Advisor 3 / Codex 6 (P4 `gid in MINTED` scores a mis-order or sibling correct; two-id parity must gate) → folded: subject-specific two-id correctness, 24/24 canonical two-id HF↔fp16 parity as the gate, held-out parity and Q4 retention reported separately (§2).
- Advisor 4 / Codex 5 (`string == full` halt inverts its purpose; §21.4 is contains, not startswith) → folded: contains judgment frozen with budget and no-early-stop, startswith reported beside it, `alt_tok_n` recorded, halt only on `string < full` (§2, §3).
- Advisor 5 / Codex 4 (P3 aggregate is a mean over prompts of per-prompt geometric means; neither 22/24 nor 24/24 gives per-position reachability) → folded: wording corrected; two instruments — 22/24 admission screen with UNDERFIT, per-position fit for all 24 values via identity-template injection of the returned `z`; UNDERFIT dropped from the curve with `n`; stopping rule untouched. Advisor's "use 24/24" not taken for admission because Codex shows the aggregate cannot carry the per-position claim either way; the per-position instrument replaces it (§2).
- Advisor 6 (INVALID-STIMULI one-sided) → folded: median of three mint-1 seeds ≥ 30, failure = -NOT-COMPARABLE (§2).
- Advisor 7 (gates belong in the reader) → folded: `c10u_mint2_read.py` encodes A1 ≥ 68, the range rules, `string ≥ full` (§2).
- Advisor on-paper overturning test (apply the rules to same-recipe data 34, 36, 42, 46, 39, 38) → run by hand: the v1 index-pairwise rule fires on same-recipe N seeds (46 − 34 = 12 ≥ 10); the v2 non-overlap rule cannot (best disjoint split of 34, 36, 42, 46 gives 42 − 36 = 6 < 10). Recorded; it calibrates nothing beyond that.
- Codex 3 (initialisation claim backwards; matched 48-row mint-1 control) → folded: first 24 of 48 rows equal the 24-row init (`lib:72`, `:84–86`), pairing hashed; control added at three seeds, conditional on the span condition firing, with the COMPETITION label (§2, §3).
- Codex 7 seam fixes → folded: key = subject's last token with frame tokens between (`compute_z:68–73`, `bandknob:51`); `zs` capture through `Z_OVERRIDE` with the driver's own engine `compute_z` solve and `Z_OVERRIDE_HITS` audit (`bandknob:185–189`, `:405–408`); P2 extended to the added probes; P4 script namespaced (`tools/c10l_mint_p4.sh:11–15`) (§2).
- Codex cheapest overturning control (bigram) / council `:69` → folded: the subject-swap teacher-forcing control with the -BIGRAM qualifier; comparison, no new threshold (§2, §3).
- Coordinator's ρ_c correction (`rho_c_band` = ‖z − cur_after‖ / ‖z − cur_before‖ is the fraction *remaining*, `experiments/track_c/c10l_covgeom_step0.py:134`; CORPUS/44's "3 % realised" is reversed, correction pending through the CORPUS gate) → checked: this document never used the 3 % reading; noted here so no later version imports it.

**v3 author's additions (2026-10-06, before the v3 reviews; each is a decision the reviews may overturn):**
- Operator ruling D-C10r-rulings-4 (2) → both arms folded; arm B gets its own block with in-block mint-1(frozen) ×3 and A7-multi(frozen) references rather than CORPUS/45's cross-process numbers (F-D4 and the ±4–5 process spread make a cross-process range comparison unreadable); block F doubles as this session's reproduction of CORPUS/45 (§2).
- Word list authored and screened (§1.1): the rule text was made operational — the head-to-word relations are checked against every inventory word, the word-to-head relations against names of any length and common words of ≥ 4 letters (shorter function words would forbid nearly every string); the bigram-control prompts are excluded from P2 (a) and checked as prefix ids + `[ĥ_head]` (they contain the minted head by design — v2's P2 wording would have failed by construction).
- Length matching: the first 24 passing candidates gave values of 5–8 ids against the frozen 4–6, so the selection rule was changed before any freeze to match the frozen heads' piece-count multiset (6 × 2, 18 × 3); the string baseline's length is otherwise a confound of the span reading.
- Arm B's bigram control, P4 scoring and per-position curve stated for pieces-plus-one-id targets (§2); block-F direction labels SECOND-WORD / HEAD-WORD / MIXED in the non-overlap form (§3); the two blocks never pooled (§3, §4).


## experiments/track_c/c10u_mint2_wordlist.py

```python
"""D-C10u-mint2 word list (C10U_MINT2_PREREG.md §1): screen the authored V2 head candidates and the modifier-only arm's
modifiers against the published rules with the base tokenizer only (no model load), and write the frozen, hashed record
results/c10u_mint2/v2_wordlist.json. The binding admission is step 0's P2 on the engine's tokenizer object; this is the
pre-screen that fixes the list before freeze. Every protected word is extracted from the harness files, never retyped.
Usage: LLMDB_ROOT=<repo> .venv/bin/python experiments/track_c/c10u_mint2_wordlist.py
"""
import ast, datetime, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c10l_mint_lib as M   # register(), sha256_text(), UNRELATED; imports torch + tokenizers only

ROOT = os.environ["LLMDB_ROOT"]   # [LAW:no-silent-failure] KeyError if unset, like every sibling driver
HARNESS = f"{ROOT}/experiments/track_c/c10e_bandknob.py"
TWOPASS = f"{ROOT}/experiments/track_c/c10p_twopass_arms.py"
OUT_DIR = f"{ROOT}/results/c10u_mint2"
OUT = f"{OUT_DIR}/v2_wordlist.json"
MIN_SUBSTRING_LEN = 4   # substring containment is checked against inventory words of this length or more (§1 rule text)

# Authored candidates, in order. The list = passing candidates taken in this order until the head piece-count
# multiset equals the frozen A7 heads' (so the V2 string baseline has the frozen values' length distribution).
HEAD_CANDIDATES = [
    "Tarvesk", "Molquenn", "Fendrax", "Ulbrisk", "Noxquill", "Sprennok", "Kalvoth", "Rimbrosk",
    "Zavrelk", "Pelthorn", "Vustrim", "Gorvande", "Hexmoril", "Tazbrenk", "Wolqetz", "Dravnisk",
    "Ombrixel", "Jorvenak", "Blemkarn", "Pyrvossk", "Nalthrik", "Skevrond", "Cravnolt", "Yembrisk",
    "Veltrosk", "Mirquand", "Ketravon", "Zumbrelk", "Faldrix", "Grentovar", "Isqeldra", "Brovquen",
    "Thanvorl", "Wexdorim", "Plaskovin", "Jaxbrenn",
    "Morvex", "Torvak", "Belmox", "Kurvin", "Zandel", "Norvek", "Palvex", "Garnoth", "Vexlan", "Tomrik",
    "Selvor", "Rundax", "Fenlor", "Dorvin", "Malvek", "Jorlex", "Wulmar", "Harvex", "Lindax", "Pelvok",
]


def harness_constants(path, names):
    """Module-level string/list constants by name; `os.environ.get(NAME, default)` yields the default (ID, REV)."""
    tree = ast.parse(open(path).read())
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in names and name not in out:
                v = node.value
                out[name] = ast.literal_eval(v.args[1]) if isinstance(v, ast.Call) else ast.literal_eval(v)
        if isinstance(node, ast.FunctionDef) and node.name == "build_stimuli":   # coined_head / coined_mod live inside it
            for inner in ast.walk(node):
                if isinstance(inner, ast.Assign) and isinstance(inner.targets[0], ast.Name) and inner.targets[0].id in names:
                    out[inner.targets[0].id] = ast.literal_eval(inner.value)
    missing = names - set(out)
    if missing:
        raise SystemExit(f"{path}: constants not found: {sorted(missing)}")   # [LAW:no-silent-failure]
    return out


def words_of(strings):
    return sorted({w.lower() for s in strings for w in re.findall(r"[A-Za-z]+", s)})


def relation(head, word, is_name):
    """The §1 relations between a candidate head and one inventory word (case-insensitive), or None. The head-to-word
    directions are checked against every word (a registered ' Head' would re-tokenise any word it prefixes); the
    word-to-head directions against names of any length and common words of >= MIN_SUBSTRING_LEN letters."""
    h, w = head.lower(), word.lower()
    if h == w:
        return "equal"
    if w.startswith(h):
        return "head is a prefix of the word"
    if h in w:
        return "head is a substring of the word"
    if (is_name or len(w) >= MIN_SUBSTRING_LEN) and h.startswith(w):
        return "word is a prefix of the head"
    if (is_name or len(w) >= MIN_SUBSTRING_LEN) and w in h:
        return "word is a substring of the head"
    return None


def screen(head, inventory, names, tok):
    """Every rule on one head; the record keeps the first failing relation per rule so the table is legible."""
    hits = {}
    for w in inventory:
        r = relation(head, w, w in names)
        if r and w not in hits:
            hits[w] = r
    name_hits = {w: r for w, r in hits.items() if w in names}
    pieces = tok(" " + head, add_special_tokens=False)["input_ids"]
    return {"head": head, "n_pieces": len(pieces), "pieces": [tok.decode([i]) for i in pieces],
            "inventory_relations": hits, "name_relations": name_hits,
            "pass": not hits and len(pieces) >= 2 and head.isalpha() and head[0].isupper() and head[1:].islower()}


def pairwise_clean(words):
    """No equality / prefix / substring relation among the words that will be registered together."""
    bad = []
    for a in words:
        for b in words:
            if a != b and (b.lower().startswith(a.lower()) or a.lower() in b.lower()):
                bad.append((a, b))
    return bad


def p2a_prescreen(tok_before, tok_after, prompts):
    before = [tok_before(p, add_special_tokens=False)["input_ids"] for p in prompts]
    after = [tok_after(p, add_special_tokens=False)["input_ids"] for p in prompts]
    changed = [p for p, a, b in zip(prompts, before, after) if a != b]
    return {"identical": len(prompts) - len(changed), "n": len(prompts), "changed": changed[:10]}


def main():
    from transformers import AutoTokenizer
    H = harness_constants(HARNESS, {"ID", "REV", "CANON", "PTEST", "FICTION", "GENERIC", "coined_head", "coined_mod"})
    F = harness_constants(TWOPASS, {"FRAME_SUBJECTS"})["FRAME_SUBJECTS"]
    screens = {k: json.load(open(f"{ROOT}/configs/screens/{k}.json"))["selected"] for k in ("g6_screen_qwen3b", "g6_screen_qwen3b_v2")}
    countries = sorted(set(screens["g6_screen_qwen3b"]) | set(screens["g6_screen_qwen3b_v2"]))
    capitals = sorted({s[c]["capital"]["truth"] for s in screens.values() for c in s})
    fiction = H["FICTION"]
    probes = [H["CANON"], *H["PTEST"], "{} is described as", "{} is a", "{} is associated with"]

    names = set(words_of(fiction + F + countries + capitals + H["coined_head"] + H["coined_mod"]))
    inventory = sorted(names | set(words_of(probes + H["GENERIC"] + M.UNRELATED + ["Zorbland", "Cairo"])))

    tok = AutoTokenizer.from_pretrained(H["ID"], revision=H["REV"])
    mods = H["coined_mod"]
    n_pieces = lambda s: len(tok(" " + s, add_special_tokens=False)["input_ids"])
    # The frozen A7 values (build_stimuli's (i*2+1) % 24 head and (i*3+2) % 24 modifier assignment) set the length quota.
    frozen = {c: f"{H['coined_head'][(i * 2 + 1) % 24]} {mods[(i * 3 + 2) % 24]}" for i, c in enumerate(fiction)}
    frozen_mods = list(dict.fromkeys(v.split()[1] for v in frozen.values()))   # first-use order
    quota = {}
    for v in frozen.values():
        quota[n_pieces(v.split()[0])] = quota.get(n_pieces(v.split()[0]), 0) + 1

    rows = [screen(h, inventory, names, tok) for h in HEAD_CANDIDATES]
    heads, left = [], dict(quota)
    for r in rows:
        if r["pass"] and left.get(r["n_pieces"], 0) > 0:
            heads.append(r["head"])
            left[r["n_pieces"]] -= 1
    if len(heads) < 24:
        raise SystemExit(f"quota {quota} unfilled, still need {left}; author more candidates")   # [LAW:no-silent-failure]
    values = {c: f"{heads[i]} {mods[i]}" for i, c in enumerate(fiction)}   # injective: head i <-> modifier i

    # P2a pre-screen inventory = all_harness_prompts (c10l_mint_lib.py:178-185) rebuilt from the constants, with every
    # capital as an A1/A2 value (a superset of the 48 the harness selects), plus the probes this arm adds (§2).
    prompts = [p.format(c) for c in fiction + F + ["Zorbland"] for p in probes]
    prompts += [H["CANON"].format(c) for c in countries] + H["GENERIC"] + M.UNRELATED + [" " + k for k in capitals]
    bigram_prompts = [(H["CANON"].format(c), h) for c in fiction for h in heads]   # contain the minted head by design

    # Registration pre-screens on fresh tokenizer copies (register() asserts tok(' '+w) == [id] for every word).
    tok_v2 = AutoTokenizer.from_pretrained(H["ID"], revision=H["REV"])
    ids_v2 = M.register(tok_v2, heads + mods)
    pairs_ok = sum(tok_v2(" " + v, add_special_tokens=False)["input_ids"] == [ids_v2[i], ids_v2[24 + i]] for i, v in enumerate(values.values()))
    bigram_ok = sum(tok_v2(p + " " + h, add_special_tokens=False)["input_ids"] == tok_v2(p, add_special_tokens=False)["input_ids"] + [ids_v2[heads.index(h)]]
                    for p, h in bigram_prompts)
    in_context_ok = sum(tok_v2(H["CANON"].format(c) + " " + v, add_special_tokens=False)["input_ids"]
                        == tok_v2(H["CANON"].format(c), add_special_tokens=False)["input_ids"] + [ids_v2[i], ids_v2[24 + i]]
                        for i, (c, v) in enumerate(values.items()))
    tok_m1 = AutoTokenizer.from_pretrained(H["ID"], revision=H["REV"])   # mint-1(V2): the 24 whole strings
    ids_m1 = M.register(tok_m1, list(values.values()))
    tok_mo = AutoTokenizer.from_pretrained(H["ID"], revision=H["REV"])
    ids_mo = M.register(tok_mo, frozen_mods)
    mo_targets = {c: tok_mo(" " + v, add_special_tokens=False)["input_ids"] for c, v in frozen.items()}
    mo_last_is_minted = sum(t[-1] == ids_mo[frozen_mods.index(frozen[c].split()[1])] for c, t in mo_targets.items())

    record = {
        "decision_id": "D-C10u-mint2", "prereg": "docs/C10U_MINT2_PREREG.md", "kind": "word-list pre-screen; base tokenizer only, no model",
        "timestamp": datetime.datetime.now().astimezone().isoformat(), "tokenizer": {"id": H["ID"], "revision": H["REV"]},
        "rules": {
            "head_form": "alphabetic, capitalised, lowercase after the first letter",
            "inventory": "every word (letters only, case-insensitive) of: FICTION (24), FRAME_SUBJECTS (6), every country and capital of both g6 screens, coined_head (24), coined_mod (24), CANON/PTEST/described-as/is-a/associated-with templates, GENERIC (20), UNRELATED (10), the LAW#5 strings",
            "relations_forbidden": f"equality; head a prefix of a word; head a substring of a word (every inventory word); a word a prefix of the head; a word a substring of the head (names of any length, common words of >= {MIN_SUBSTRING_LEN} letters)",
            "bpe": "tok(' ' + head) has >= 2 pieces in the base tokenizer",
            "registration": "after register(heads + coined_mod): tok(' ' + w) == [id] for all 48; tok(' ' + head + ' ' + mod) == [id_head, id_mod] and CANON + value == CANON ids + the pair for all 24; P2a pre-screen identical over the inventory prompts; every bigram-control prompt CANON(subject) + head == CANON ids + [id_head] (these prompts contain the minted head by design and are excluded from P2a)",
            "pairing": "value i = heads[i] + ' ' + coined_mod[i] for FICTION[i] (injective; every head identifies its modifier)",
            "selection": "passing candidates in authored order until the head piece-count multiset equals the frozen A7 heads' (head_pieces_quota)",
        },
        "head_pieces_quota": quota,
        "value_pieces": {"frozen": sorted(n_pieces(v) for v in frozen.values()), "v2": sorted(n_pieces(v) for v in values.values())},
        "inventory_sha256": M.sha256_text("\n".join(inventory)), "inventory_size": len(inventory),
        "candidates": rows,
        "heads": heads, "heads_sha256": M.sha256_text("\n".join(heads)),
        "values": values, "values_sha256": M.sha256_text(json.dumps(values, sort_keys=True)),
        "pairwise_relations_among_48": pairwise_clean(heads + mods),
        "v2_registration": {"ids": [ids_v2[0], ids_v2[-1]], "pairs_two_id": f"{pairs_ok}/24", "canon_plus_pair": f"{in_context_ok}/24",
                            "p2a_prescreen": p2a_prescreen(tok, tok_v2, prompts), "bigram_prompts_prefix_plus_head_id": f"{bigram_ok}/{len(bigram_prompts)}",
                            "string_baseline_pieces": {v: len(tok(" " + v, add_special_tokens=False)["input_ids"]) for v in values.values()}},
        "mint1_v2_registration": {"ids": [ids_m1[0], ids_m1[-1]], "p2a_prescreen": p2a_prescreen(tok, tok_m1, prompts)},
        "modifier_only": {"modifiers": frozen_mods, "modifiers_sha256": M.sha256_text("\n".join(frozen_mods)), "ids": [ids_mo[0], ids_mo[-1]],
                          "frozen_values": frozen, "target_lengths": sorted({len(t) for t in mo_targets.values()}),
                          "last_id_is_minted": f"{mo_last_is_minted}/24", "pairwise_relations": pairwise_clean(frozen_mods),
                          "p2a_prescreen": p2a_prescreen(tok, tok_mo, prompts)},
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    json.dump(record, open(OUT, "w"), indent=2, ensure_ascii=False)
    print(f"heads {len(heads)}/24 from {sum(r['pass'] for r in rows)} passing of {len(rows)} candidates; quota {quota}; sha256 {record['heads_sha256'][:12]}")
    print(f"value pieces frozen {record['value_pieces']['frozen']}\n             v2     {record['value_pieces']['v2']}")
    print(f"heads: {heads}")
    for r in rows:
        print(f"  {'PASS' if r['pass'] else 'FAIL'} {r['head']:<10} pieces={r['n_pieces']} {r['pieces']} {r['inventory_relations'] or ''}")
    v2 = record["v2_registration"]
    print(f"V2: pairs {v2['pairs_two_id']}, canon+pair {v2['canon_plus_pair']}, P2a {v2['p2a_prescreen']['identical']}/{v2['p2a_prescreen']['n']}, "
          f"bigram prompts {v2['bigram_prompts_prefix_plus_head_id']}, pairwise {record['pairwise_relations_among_48']}")
    m1 = record["mint1_v2_registration"]["p2a_prescreen"]
    print(f"mint-1(V2): P2a {m1['identical']}/{m1['n']}")
    mo = record["modifier_only"]
    print(f"modifier-only: {mo['modifiers']} lengths {mo['target_lengths']} last-id {mo['last_id_is_minted']} P2a {mo['p2a_prescreen']['identical']}/{mo['p2a_prescreen']['n']}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

```
