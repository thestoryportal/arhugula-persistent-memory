# Autoresearch loop: write prompts that mirror the held-out templates (2026-10-06 ~19:45)

**Finding (program session, read-only).** From experiment 3 (`afcb2cb`) on, the loop's write prompts include close paraphrases of two of the three sealed held-out templates; experiment 8 (`e475185`, running) adds a paraphrase of the third.

| Held-out template (`c10e_bandknob.py:52-56`, `PTEST`) | Loop write prompt | First used |
|---|---|---|
| Q1 `{}'s capital city is called` | `{}'s capital is the city of` | exp 3 `afcb2cb` (also `a26863d`, `1206a7c`) |
| Q2 `If you visit {}, its capital city is` | `When you travel to {}, the capital is the city of` | exp 3 (also exp 4, 5) |
| Q3 `The main city and seat of government of {} is` | `The largest city and capital of {} is the city of` | exp 8 `e475185` |

The agent read `c10e_bandknob.py` in full at setup (transcript audit: `cat -n c10e_bandknob.py`), which `program.md` allows; `program.md` forbids using the evaluation data in `edit.py`, and `prepare.py:67-76` blocks it by name only. No fence breach and no baseline mismatch: the standing stop rules do not fire.

**Per-template split of every scored run** (`para_full_hits` per `PTEST` index, A7 arm; script `$CLAUDE_JOB_DIR/tmp/split_by_template.py`):

| Run | Commit | Total /72 | Q1 /24 | Q2 /24 | Q3 /24 | dw_total | guards |
|---|---|---|---|---|---|---|---|
| 131156 | fd16592 baseline | 7 | 2 | 2 | 3 | 89.0 | ok |
| 134836 | 88b1cb7 | 7 | 2 | 2 | 3 | 90.7 | ok |
| 142644 | 92acd03 (exp 2) | 18 | 4 | 6 | 8 | 131.4 | ok |
| 151845 | afcb2cb (exp 3) | 26 | 10 | 8 | 8 | 147.7 | failed: described_as |
| 160157 | a26863d (exp 4) | 29 | 10 | 8 | 11 | 147.6 | ok |
| 164907 | 1206a7c (exp 5) | 30 | 11 | 8 | 11 | 154.9 | ok |
| 174032 | 9940c0a (exp 6) | 13 | 7 | 5 | 1 | 212.4 | failed: described_as |
| 181532 | ae66823 (exp 7) | 28 | 9 | 9 | 10 | 212.8 | ok |

**Reading (I-INFER).**
- Experiment 2's gain (7 → 18) used only the canonical write prompt and is spread over all three templates (+2 / +4 / +5): not affected; the D-C10r-exp2ctl control stays valid.
- Adding the mirrored prompts (exp 2 → exp 3) moved Q1 4 → 10 and Q2 6 → 8, and the unmirrored Q3 not at all (8 → 8). The multi-prompt gain sits on the mirrored templates.
- The unmirrored Q3 later rose 8 → 11 (exp 4, the KL brake), a gain not explained by mirroring.
- Honest reading of the loop's best (30/72): it is partly test-adjacent. The cleanest "new wording" number is Q3 = 11/24 (baseline 3/24, exp 2 8/24). From experiment 8 on, all three templates are mirrored and the loop's `heldout_full` no longer measures transfer to unseen wording.

**Implications.** Loop scores from experiment 3 on are register candidates only with this caveat; any promotion needs a fresh sealed set of rewordings the agent has never read. Step 1 (`D-C10s-sharedz`) reports per-template counts by design; its frozen T1 `The government of {} sits in` shares the word "government" with Q3 — to be weighed at its verdict. For the next loop relaunch: seal the held-out templates out of the agent's readable files and state the no-paraphrase rule in `program.md` (operator decision).
