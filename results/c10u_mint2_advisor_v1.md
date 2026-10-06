# Advisor review — D-C10u-mint2 v1 draft (`docs/C10U_MINT2_PREREG.md`), 2026-10-06

**VERDICT: FIX-FIRST.**

**The single most important thing.** The monotone test cannot be read at two seeds, because its draws are independent, not paired: the draft itself says a 48-row N(seed s) "is a fresh draw, not the 24-row one extended" (`C10U:33`, from `c10l_mint_lib.py:72`, `:84-86`), so "seed 0 with seed 0" (`C10U:77`) shares no randomness. CORPUS/46 has the *same* recipe at seeds 0/1/2 = 46/34/36, range 12/72 (`CORPUS/46:22`, `:33`): a within-configuration difference of 12 already clears the `>= 10` bar, so init spread alone can yield **SPAN-DIRECTION** in both "pairs" with no span effect — that is (f). Fix before freeze: >= 3 seeds per mint arm (F-D4 binds, `CORPUS/46:33` — this *is* an init-draw comparison), ordering read on non-overlapping ranges (`min(M1) - max(M2) >= 10`), not index-pairwise. **PAIR-DIRECTION**'s `|M2 - S| <= 5` likewise imports the ±5 *per-process* envelope (`CORPUS/45:61`) onto a seed difference of range 12 — unreachable in practice, and mislabels a real pair effect MIXED.

## Issues in priority order

1. **(b)/(f) above — a freeze blocker.**

2. **(a) Departure 1 is arithmetically correct; V2 moves two axes and needs the operator's ruling.** From `c10e_bandknob.py:246-249`, `:57-61`: **12 distinct heads, 8 distinct modifiers**; **8 heads are exactly FICTION subjects** (Drennik, Vythorn, Vorlex, Kessivar, Halquin, Marsduq, Glimsto, Fluvane), **3 are prefixes** (Brindu, Lurmax, Yastov); only Qorvex and Vindex are subject-free. With `single_word=False` (`lib:26`), P2a over `all_harness_prompts` (`lib:178-185`, halt `c10l_mint_step0.py:51-53`) fails by construction. The claim stands.
   - **`single_word=True` is not the fix.** I-INFER on HF `AddedToken` semantics (not run): it suppresses matches only *inside* a larger word, rescuing the 3 prefixes and leaving all 8 exact collisions — P2a still fails, the subject key still becomes a random row.
   - **Modifier-only is dismissed without argument** (`C10U:26`) and is not a separate hypothesis: the modifiers are not subjects, and A7 value strings are excluded from `all_harness_prompts` by design (`lib:180`), so it is P2a-clean *on the frozen values* and still shortens the value — forfeiting a uniform two-id value but keeping CORPUS/45 comparability, which V2 loses. State the tradeoff.
   - **V2 is a two-axis change, understated in §4.** It uses all 24 `coined_mod` injectively (`C10U:26`); the frozen set reuses 8 modifiers three times each, 12 heads twice each. V2 drops that shared structure as well as the head identities — a plausible contributor to 34-46, never isolated. **Operator ruling: yes, before freeze.** These stimuli are the instrument behind every CORPUS/39-50 A7 number, so a redraw creates a second set later readers will compare as if it were A7. Name it A7-V2 with a Decision-ID line.

3. **(e) The P4 correctness column is wrong for mint-2, not just first-id-only.** `c10l_mint_p4_probe.py:39` scores `"correct": (gid in MINTED)`. With 48 ids a **modifier firing first** — the mis-order the I-11 extension exists to catch (`C10U:46`) — scores correct. Make it `gid == MINTED[head_index(k)]`; "a probe extension to be reviewed" (`C10U:64`) is too mild for a scoring defect.

4. **(d) The storage/behaviour validity rule inverts its purpose.** `para_string_n == para_full_n` is a HALT (`C10U:68`), yet `string_match` decodes `n_tokens + 2` and tests `startswith(" " + value)` (`bandknob:121-130`) while `full_seq_match` demands exact ids (`:109-117`). Mint-2 can emit the right *string* via BPE pieces, or head-minted + modifier-as-BPE: string passes, ids fail — the most informative mint-2 outcome, aborted by the rule. Require `string >= full`, record the gap, halt only on `string < full`. Budget slack is arm-dependent (4 ids vs ~6-8).

5. **(c) P3 per value is defensible; 22/24 is too loose and one cited fact is off.** The engine prints `torch.exp(-nll_loss_each).mean()` (`compute_z.py:162`) — the **mean over prompts** of each prompt's geometric mean over the two positions, not "the geometric mean of the two token probabilities" (`C10U:40`). Per-value >= 0.98 bounds each position at >= ~0.96, so the stub's per-row intent is largely met — say so. But 2 UNDERFIT values is 6/72, inside the thresholds: use **24/24**, or drop UNDERFIT values from the curve with `n` reported.

6. **INVALID-STIMULI is one-sided and underpowered.** ">= 30 in at least one seed" (`C10U:54`) is a max over two draws whose siblings are 34 and 36 (`CORPUS/46:22`): a bad V2 passes on one lucky draw, a good V2 can fail both. At >= 3 seeds, make it a median rule.

7. **Gates belong in the reader.** `c10l_mint_read.py:54` hard-codes `A1 < 58`; the contract is 68 (`prereg_stubs.md:10`), superseded in prose only (`C10U:68`). The reader must encode 68, the range ordering and `string >= full`.

**Credit:** the step-0 recall mismatch is caught (`lib:134` replaced by `full_seq_match`, `C10U:46`); departure 3 follows from `lib:95-97`. **Drift:** correctly scoped as diagnostic (`C10U:11`, `:88`).

**Cheapest overturning test, no GPU:** apply the §3 rules within one configuration — CORPUS/45+46's replicates and N seeds (34, 36, 42, 46, 39, 38). If `>= 10` and `<= 5` fire on same-recipe data, the thresholds are falsified on paper.
