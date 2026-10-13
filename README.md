# LLM-as-Database

**Can an AI model's own memory work like a database?** This project tests, honestly and step by step, whether facts can be written directly into a language model's internal "brain", then looked up, changed and tracked like records in a database, without the model rereading everything on every request.

---

## In plain words

*Last updated 2026-10-10 UTC.*

**The problem.** Today's AI models forget everything between conversations. To "remember" your work, a model has to reread it every time, and that rereading costs time and money.

**The idea.** Write facts straight into the model's brain, the numbers inside it, the way a record is saved in a database. The model would then simply know them. Like a real database, you could also look facts up, change them, and keep a record of every change.

**What this project is for.** It is not building that system yet. It is finding out whether the system *can* be built, before anyone spends money building it. The answer will be "yes", "no", or "yes, if these conditions are met". The current draft answer is **"not ready yet, with conditions"**: most pieces work, and a short list of open problems decides the rest.

**The open problem being worked on now.** Invented names made of more than one word, such as a new product called "Qorvex Zentra". The model learns the exact sentence it was taught but stumbles when asked the same thing in different words. It is like teaching someone a new friend's name: they can answer "what's your new friend's name?" but go blank at "who did you meet on Tuesday?". The best attempt so far answers **24 of 72** differently worded questions correctly. It needs to do much better before the answer can be "yes".

**What happens next.** The latest fixed test with invented names did not meet its learning and safety checks within the allotted work. An independent reviewer confirmed that reading, and the trial stops under its current approval. This result applies to that setup; the broader memory question remains open. The mathematical lab also remains stopped, while the separate study comparing saved model changes retains its own checks. [Detailed finding](evidence/CORPUS/61_C10Z_ATTEMPT4_UNDERFIT.md).

## Where things stand

| Question | Status | In plain terms |
|---|---|---|
| Can facts be written into the model? | ✅ Works | Many simple facts can be written in one go without corrupting each other. |
| Does the rest of the model stay intact? | ✅ Works, within tested limits | Unrelated knowledge is left alone in the tested range. |
| Does it survive being compressed for everyday use? | ✅ Works | Edited facts survive the compression that makes models small enough to ship. |
| Can it run on an ordinary computer? | ✅ Works | It runs on a regular laptop processor at usable speed. |
| Do the safety and record-keeping rules hold? | ✅ Works as designed | The project's own checks, approvals and audit trail behave as specified. These test the design, not the model. |
| Can it learn invented multi-word names and recall them when asked differently? | 🔴 Open, being worked on | Best so far: 24 of 72 reworded questions. |
| Other open conditions | 🟡 Open | Very large collections of facts, a proper search layer, security testing, deleting facts, and larger models. |

## Progress record

Newest first.

- **2026-10-10.** A fixed test with invented names did not meet its learning or safety checks within the allotted work. Independent review confirmed the reading; the trial stops and the broader question remains open. [Detailed finding](evidence/CORPUS/61_C10Z_ATTEMPT4_UNDERFIT.md).

- **2026-10-09, later.** Two inexpensive mathematical signals failed a check against known results, so the lab stopped as planned and its next step was shelved. An independent reviewer confirmed the reading. A separate study comparing saved model changes continues under its own checks.
- **2026-10-09.** A diagnostic found agreement with a fixed sample of records, and an offline calculator reproduced saved edits. Tests of whether the edited model reliably remembers the facts remain open.
- **2026-10-08, evening.** The sixth planned experiment finished after three restarts (each restart fixed a problem in how the run checked or recorded itself, never the science). Re-weighting the words of the answer before writing it raised the reworded-question score from 12 to 17 of 72, too little to count. Rebuilding the answer a different way made the ordinary control facts worse, so that result is not read. Neither idea is taken forward. An independent reviewer from another AI company confirmed the reading.
- **2026-10-08, early morning.** The ceiling test's official result: training the same small part of the model answered 70 and 71 of 72 reworded questions on two runs, so that part is big enough to hold invented names. It disturbed other facts along the way, and one run lost some general knowledge, so a clean ceiling is not shown. The first try at the official check had stopped on a rounding bug; it was fixed, reviewed and re-run rather than read around. The next two experiments go ahead on their own plans.
- **2026-10-07, evening.** The third planned experiment gave no clear answer on either of its two new ideas: one was measured on names where the usual method already did unusually well, and the other never ran because it failed an early fitting check that the usual method fails too. The earlier one-word-per-name method repeated its result (46, 37 and 40 of 72 against 14). The finding stays provisional until the project lead confirms the third attempt.
- **2026-10-06, around 8:40 pm.** The automated agent reached 34 of 72, but a closer look showed that since its third change it had been practising on near-copies of two of the three test questions, which inflates part of its score; on the one question it never copied, it went from 3 to 12 of 24. The project lead paused it so the machine can run the first planned test and the one-hour check of the agent's first win. Before it restarts, the project lead decides whether to hide the test questions from it.
- **2026-10-06, around 7 pm.** The automated agent reached 30 of 72 with every safety check passing, by turning its protection up; writing deeper inside the model made things worse (13 of 72), which is a useful hint for a later test. The one-hour check of its first win is now built, reviewed three times and locked: a reviewer caught a flaw that would have stopped the check by mistake, and it was fixed and re-tested on this Mac. Five outside papers the project lead found were reviewed: none changes the plan, and one independently hit the same "only works in the taught wording" wall.
- **2026-10-06, around 5 pm.** The automated agent's fourth change answered 29 of the 72 reworded questions with every safety check passing, its best so far. It teaches each fact in three phrasings and touches the model more gently. The one-hour check of its first win was redesigned before it ran: two reviewers showed the original plan would only confirm a number already known. The new check keeps the protection but aims it at ordinary words, to tell whether the protection itself or simply a bigger change caused the gain.
- **2026-10-06, around 4 pm.** The automated agent has now tried four changes. Its first win, protecting the answer words while writing, raised the reworded-question score from 7 to 18 of 72 with every safety check passing. An independent reviewer from another AI company found no cheating and no sign of luck, and proposed a one-hour test that switches the protection off to see whether the win disappears; the project lead approved it for the next pause. The agent's third change scored 26 of 72 but narrowly failed one safety check, so it was thrown away as the rules require; its fourth change is running.
- **2026-10-06, late afternoon.** The last of the four test plans is finished and frozen. It needed 24 new invented first names (the old ones doubled as place names, which would have broken the test); they were written and checked against every word the test uses, with the real tokenizer, and two independent reviewers then checked the plan and the list. One reviewer rebuilt every checksum from scratch and matched them all. The two reviewers disagreed on one rule (what to do if the test fails to reproduce an earlier result): the plan now runs that reproduction first and stops if it misses. The first test is ready and waits for the project lead's go. The sealed-folder agent finished its second idea and is scoring it.
- **2026-10-06, mid-afternoon.** The sealed-folder agent is running: its first, untouched run reproduced the instrument check to the digit, and it has proposed its first change on its own. Test plans for the first four ideas from the outside research run are written and reviewed (two independent reviewers each); three are frozen, one waits on a decision from the project lead. A reviewer also caught a reversed reading in an earlier write-up (a number meaning "how much was left" had been read as "how much was done"); it was verified against the code and corrected everywhere, with no verdict changing. Later: the sealed-folder agent tested and discarded its first idea cleanly (no gain) and moved to a second; the project lead ruled on the open items (one experiment at a time; the two-token idea tests both variants; two later ideas moved down the list).
- **2026-10-06, early afternoon.** The sealed folder's reviewer found four more cracks in a row (an old archive copy, a code-hosting cache, a folder of old trial files on the drive, a browser cache), so the seal was rebuilt to block everything by default and open only the dozen pieces an experiment needs; the reviewer then cleared it. The instrument re-check that must pass before the agent starts is finishing. The research run's first idea has a draft test plan, corrected once by an independent advisor.
- **2026-10-06, afternoon.** The outside research run finished: thirty ideas from the literature, ranked with the cheapest test first; the top one takes about half an hour on this Mac. The automated research agent was started five times and stopped five times while its sealed folder was tightened — an independent reviewer kept finding a crack each time (old notes, temp files, cached files) and each crack was closed and tested; it restarts once the instrument re-check passes.
- **2026-10-06.** A second, stacked edit doubled the score on reworded questions, from 12 to 24 of 72, but disturbed the model a little too much. The overnight research agent and the outside research run were set up. A full check confirmed the agent's rebuilt tools measure exactly like the original experiment.

---

## For researchers

A falsification-first research program testing whether facts can be **stored in, retrieved from, governed within, and deployed from an LLM's weights**, treating a transformer as a queryable database rather than an opaque generator. Editing uses the MEMIT/AlphaEdit family (closed-form `down_proj` null-space solves) on Qwen2.5-3B in fp16 on Apple MPS. The program stress-tests a written spec ([`knowledge/specs/integrated-spec-v1_2/`](knowledge/specs/integrated-spec-v1_2)) toward an implementation-readiness determination, drafted in [`knowledge/findings/F1_DETERMINATION.md`](knowledge/findings/F1_DETERMINATION.md) as **NOT-READY-WITH-CONDITIONS** with a ten-row conditions register.

Every headline claim resolves to a raw artifact, every experiment is pre-registered and re-runnable, and caveats sit next to results. The repo follows the ML Reproducibility Checklist (Pineau et al.), "Good enough practices in scientific computing" (Wilson et al.), Model-Card disclosure norms (Mitchell et al.) and the FAIR principles.

**Read in this order:** this README → [`_system/governance/REPRODUCIBILITY.md`](_system/governance/REPRODUCIBILITY.md) → [`program/registers/EXPERIMENT_REGISTRY.md`](program/registers/EXPERIMENT_REGISTRY.md) → [`evidence/CORPUS/README.md`](evidence/CORPUS/README.md) (the evidence) → the spec. The live roadmap is [`program/runbook/`](program/runbook) §0.3, and the operating discipline is [`_system/governance/DISCIPLINE.md`](_system/governance/DISCIPLINE.md).

### Selected findings (early phases)

The complete, current ledger is [`evidence/CORPUS/00_MASTER_EVIDENCE.md`](evidence/CORPUS/00_MASTER_EVIDENCE.md); the multi-token value line (C10) runs through `evidence/CORPUS/37`–`50`.

| Area | Result | Evidence |
|---|---|---|
| **Governance** (in-pipeline write, 2PC, security, validation) | ✅ PROVEN-FOR-SCOPE (design-viability — these test our own control flow, not nature; weaker-than-empirical) | `evidence/CORPUS/07–12` (CP1–CP3, G1–G3) |
| **Single/few-fact, same-entity store** | ✅ VALIDATED (Qwen2.5; model- & size-dependent — Qwen2.5-7B local, GPT-J not) | Phase-1, `knowledge/findings/framework_findings/` |
| **Cross-entity store at scale (sequential)** | ❌ FALSIFIED — held-out same-relation reads corrupt 100→41.7% with N (the first empirical falsifier) | `evidence/CORPUS/13` (G6.1) |
| **Batch / Genesis write at scale** | ✅ ELIMINATES the corruption at 3B (flat 100→100→100%) | `evidence/CORPUS/14` (A1) |
| **In-solve sentinels / K_S refresh** | 🟡 PARTIAL / ruled-out (halve but don't arrest the sequential decline; staleness not the cause) | `evidence/CORPUS/15–16` (A2, A2b) |
| **Real Q4_K_M quantization survival** | ✅ PASS — edits survive deployment quantization (edited 100% vs native 97.4%) | `evidence/CORPUS/17` (B3) |
| **CPU deployment serving** | ✅ Claim A PASS via **llama.cpp** (~8–13 tok/s) · ❌ Claim B FALSIFIED via **LARQL** (drops Qwen2.5 attn bias; A7 causal proof) | `evidence/CORPUS/18` (E1) |
| **Size-density (3B→7B)** | 🟡 PARTIAL — batch-clean does not *fully* replicate at 7B (100→91.7%) | `evidence/CORPUS/19` (B1) |
| **Cross-entity mechanism (keying)** | ⛔ relation-keying PRUNED; same-relation key collinearity is U-shaped in depth (min L8–12) — a measured mechanism + a spec-C15 tension | `evidence/CORPUS/20` (C2) |

**Net state:** the **batch-rebuild deployment path** is clean at 3B and survives Q4_K_M; CPU serving works via llama.cpp. Open frontier: whether in-weight storage (L2) is even required vs. retrieval (L1) + an external query index; the capacity law (D1 — structural DONE+model-general; §8.7 numeric guardrail set conservative at per-relation **k≤1** on 3B, D-D1-2 ⟨D-D1-2@e023d8d2⟩, cross-model transfer open); and whether the edit-validated family (Qwen2.5) should move to the LARQL-servable family (Qwen3). See `program/registers/HYPOTHESIS_REGISTER_2026-06-18.md`.

### Reproduce

```bash
export LLMDB_ROOT="$PWD"
# no GPU: re-derive the quantization verdict from stored predictions
python code/lab/track_b/b3_verdict.py
# GPU, about a minute: load Qwen2.5-3B and print the key-collinearity depth map
python code/lab/track_c/c2_key_collinearity.py
```

Every experiment's exact command, inputs and expected artifact are in [`_system/governance/REPRODUCIBILITY.md`](_system/governance/REPRODUCIBILITY.md) and [`program/registers/EXPERIMENT_REGISTRY.md`](program/registers/EXPERIMENT_REGISTRY.md).

### Scope and caveats (read before citing)

- **Model and range:** primarily Qwen2.5-3B (some 7B and Qwen3-0.6B); N ≤ 100 edits; Q4_K_M quantization only; mostly single-seed, single write-ordering; counterfactual-reassignment edits, not insertion or deletion.
- **Governance (CP1–G3) is design-viability**, not empirical falsification: it verifies that our code implements the spec's contracts, a weaker category (see `evidence/CORPUS/03`).
- **A measurement confound runs through the edit metrics:** MEMIT's `compute_z` inflates edited-fact margins relative to native facts (`evidence/CORPUS/17`), so read retention numbers with that in mind.
- Reproducibility survived a 2026-06-18 repository reorganization through the `LLMDB_ROOT` path convention.

### Repository map

```
README.md  _system/governance/REPRODUCIBILITY.md            start here
program/runbook/                    living roadmap (§0.3 = what's next)
_system/governance/DISCIPLINE.md  CLAUDE.md  AGENTS.md      operating rules for people and agents
evidence/CORPUS/                                  the evidence ledger (numbered findings + provenance and status ledgers)
research_and_specs/                      the governing spec and research synthesis
docs/                                    registries, prereg documents, design docs (e.g. AUTORESEARCH.md)
experiments/                             re-runnable code by track (governance, scale, track_a/b/c/e, deployment)
code/configs/                                 hyperparameters, stimulus screens, probes
results/  logs/                          result JSONs and run logs
_system/memory/                           durable cross-session learnings
archive/                                 frozen historical scripts and notebooks
memit_dry_run/                           the vendored MEMIT engine (fingerprinted, never modified)
```

---

<details>
<summary><b>Detailed program state</b> (auto-generated from the program tracker; technical)</summary>

[Program status](program/STATUS.md)

</details>
