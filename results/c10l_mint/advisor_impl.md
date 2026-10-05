# Advisor review (Codex gpt-5.5, cross-family) — D-C10l-mint implementation (2026-10-05, before any mint run)

Reviewer had read-only access to the worktree. Packet: c10l_mint_lib.py, c10l_mint_step0.py, c10l_mint_arms.py, the harness seam, declared interpretations.

## Disposition
FIX-FIRST → amendment B1 (`docs/C10L_MINT_TOKEN_PREREG.md` §10): G redefined as all-but-the-top with the mean NOT added back (the v2 text was algebraically M); P3 fail-closed per init; "live" resolved to the numeric init-level rule with post-minus-step-0 reading; P1 fingerprint run inside step 0 + LAW3_REF asserted by the arms driver; tokenizer files / A1-rare list / G directions hashed; A1-rare declared a BPE-id proxy. B1 sent for its own advisor pass before step 0 runs (`advisor_b1.md`).

## Review text (verbatim)

**Verdict: FIX-FIRST**

**Single most important next step:** amend/fix init **G** before any run. As coded, G is algebraically just M’s constituent-token mean with a norm rescale: `(R - mu).mean(0) + mu == R.mean(0)`, then norm matching. That does not implement the prereg’s claimed “all-but-the-top correction” or a grounded init, yet A7-mint-G is the primary span-vs-novelty arm. See `docs/C10L_MINT_TOKEN_PREREG.md:44-45`, `docs/C10L_MINT_TOKEN_PREREG.md:64`, `experiments/track_c/c10l_mint_lib.py:64-68`.

**Issues, Priority Order**

1. **Primary G arm does not test the intended criterion.**  
   The prereg says G removes the shared collapse component; the implementation cancels the de-meaning before rescaling. A G pass/fail would be interpretable mostly as “mean direction plus norm,” not the promised grounded/de-collapsed init. This can create either a false negative for minting or a misleading G-vs-M story. `experiments/track_c/c10l_mint_lib.py:64-68`, `docs/C10L_MINT_TOKEN_PREREG.md:45`, `docs/C10L_MINT_TOKEN_PREREG.md:74-78`.

2. **P3 is recorded but not fail-closed.**  
   The prereg makes P3 blocking: if `compute_z` does not reach ≥0.98 for ≥22/24, the write cannot be attributed to the solve. Step 0 stores `P3_compute_z`, but `admitted_inits` ignores it, and arms only check `excluded_from_arms`. `docs/C10L_MINT_TOKEN_PREREG.md:34`, `docs/C10L_MINT_TOKEN_PREREG.md:73`, `experiments/track_c/c10l_mint_step0.py:37`, `experiments/track_c/c10l_mint_step0.py:74-81`, `experiments/track_c/c10l_mint_arms.py:79-86`.

3. **“live” is internally inconsistent between prereg and code.**  
   Code labels a token live if it is top-1 on ≥1 paraphrase, but excludes an init only if total step-0 `para_full > 2`. The prereg text says live is `step-0 para_full > 2/72`, then says “any live token” excludes. That ambiguity must be resolved before reading exclusions. `docs/C10L_MINT_TOKEN_PREREG.md:49`, `docs/C10L_MINT_TOKEN_PREREG.md:53`, `experiments/track_c/c10l_mint_lib.py:118-123`, `experiments/track_c/c10l_mint_step0.py:74`.

4. **P1 is not implemented in the listed mint scripts.**  
   The prereg requires fingerprint PASS and LAW#3 reproduction, shared only if already run in-session. I found no P1/fingerprint/LAW#3 check in the mint implementation; otherwise this is **UNVERIFIABLE** at run time from these files. `docs/C10L_MINT_TOKEN_PREREG.md:32`.

5. **Provenance hashing is incomplete.**  
   The prereg says minted rows, tokenizer files, and A1-rare list are hashed into JSON. Step 0 hashes init rows only; it saves the tokenizer and records A1-rare values, but I do not see tokenizer-file hashes or an A1-rare-list hash. `docs/C10L_MINT_TOKEN_PREREG.md:86`, `experiments/track_c/c10l_mint_step0.py:51-56`, `experiments/track_c/c10l_mint_step0.py:76-78`.

What looks solid: token registration asserts spare-row ids and `tok(" "+v)==[ĥ]`; binding top-1-id and string readout are separated correctly; A1-rare is acceptable only if described as a high-BPE-id proxy, not literal frequency rank. `experiments/track_c/c10l_mint_lib.py:24-36`, `experiments/track_c/c10e_bandknob.py:109-130`, `experiments/track_c/c10l_mint_lib.py:133-144`.

Drift check: this does advance F1 via the live C10 span-vs-novelty falsifier, but only if G and the gates are fixed before results are treated as evidence.