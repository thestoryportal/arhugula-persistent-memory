# HANDOFF — research pass 2026-10-06 (D-C10r-rulings-2) → program session

**Read this file first.** It is the single entry point to the pass. Everything the pass produced lives under `results/research_pass_2026-10-06/` on branch `research-pass/2026-10-06` (worktree `chat_8376051e-0cc1-4c9c-94f6-eb257a489254`, branched from 545d11e). Nothing in this folder is evidence: no experiment was run, no CORPUS, runbook, register, overlay or memory file was touched, and the ledger nodes are a hypothesis ledger with no runs. The program session carries everything below through its own close-out gate.

## 1. Final prioritised decisions reached with the operator in this session

1. **Writing, not training.** Any route that needs a training set or a training loop per commit is not a route. H-13 (merged band-LoRA) and H-15 (full fine-tuning of the band) are kept only as a labelled measurement ("oracle arm", step 5 below). H-18 (minted row by gradient tuning) is demoted from the top tier; its closed-form variant may be revisited.
2. **Sequence over ranking.** The operator accepted the order in `recommended_sequence.md`: four pure-write harness passes (steps 1–4), a replication gate, the oracle measurement (step 5), then the two engine-path arms and the direct-ΔW arm (steps 6–7), a background covariance job (step 8), multi-day builds later, model changes only after the Qwen ceiling rule (D-C10k-rulings-2) is met or overridden.
3. **No multi-day work starts now.** Steps 6, 7 and the "later" items are sequenced, not started.
4. **Side stores remain an engineering fallback** (runbook row 307 stands); they are logged in `dispositions.md` and never ranked.

The earlier `top3.md` (H-1, H-18, H-13) is superseded by these decisions; it carries a dated note and stays for the record because the council critique was written against it.

## 2. Where everything is

| file | what it is | status |
|---|---|---|
| `recommended_sequence.md` | the agreed order, plain language, with a technical appendix | final |
| `prereg_stubs.md` | pre-registration stubs for steps 1–8 with the council's amendments built in | final (stubs, not program-format pre-registrations) |
| `hypotheses.md` | 30 hypotheses, every class, each with claim, mechanism, sources, cheapest test, pass/fail numbers, would-advance, spec-amendment, feasibility, source-metric, disposition; addendum with the H-18 labelling correction | final |
| `top3.md` | the first top three and their stubs | superseded; see note at its top |
| `council_critique.md` | six Framework Council lenses on the first top three plus a synthesis of where they converge | final; critique, not evidence |
| `dispositions.md` | every class with disposition, search evidence, yields per instrument, the exit condition and which instruments met it | final |
| `contradictions.md` | BetaEdit id (real), AnyEdit++ repo (exists, CUDA-bound), MDM-KE code (does not exist), GPU-proposal hardware claim (superseded) | final |
| `grounding_coverage.md` | what was read, by whom, and what was not reached; the three calibration classifications | final |
| `ledger_nodes.md` | root node `00157b6d-461c-4324-8ed4-ead8d2006876` and the 30 child node ids | final |
| `instrument_logs/` | one JSON per instrument (arXiv, research CLI, GitHub, Hugging Face, Perplexity, InfraNodus, browser sources) with every query and hit id; raw research-CLI and browser captures | final |
| `helper_reports/` | condensed grounding reports from four read-only helpers | reference |
| `council/` | the six lens files individually | reference |
| `_parts/` | the source parts `hypotheses.md` was assembled from | reference; may be deleted at close-out |

Outside the repo, authorised by the brief: four Connected Papers `.bib` exports added to `/Volumes/memit/llm-database-poc-mirror/connected-papers-knowledge-graphs/INBOX/` (BetaEdit, Keys to Robust Edits, Memory as a Markov Matrix, LOKI); one InfraNodus graph `llmdb-rp-hits-20261006` in the account.

## 3. Actions the program session must take (through the §0.4 close-out gate; none done here)

1. **Runbook row 295 and `memory_mirror/betaedit-official-repo.md`:** replace "the arXiv 2605.09285 id was fabricated" with the verified record in `contradictions.md` §1 (real paper, IJCAI 2026; repository live, device-portable, Qwen2.5-3B-Instruct config).
2. **Inventory rows:** row 1 (BetaEdit) → repository live, no re-clone needed, Instruct config; row 3b (AnyEdit++) → code exists, CUDA-bound, 7B-Instruct configs, key never at the subject; row 10 (MDM-KE) → code location unverified, `holi-lab/MDM-KE` does not exist.
3. **`docs/PRIOR_ART_SWEEP_2026-10-04.md` §4:** annotate the MDM-KE code claim as unverified.
4. **Hypothesis register §J:** one row per hypothesis H-1…H-30 from `hypotheses.md` (builds-on, would-advance, source, disposition), or a pointer row to the file per the de-dup norm; mark H-13/H-15 "oracle measurement, not a route" and H-18 with its corrected spec-amendment.
5. **`docs/program_state.json` next-action pointer** to `recommended_sequence.md`, then `render_state.py --write`; runbook §5 decision line for the operator's write-only ruling (the operator's words in this session: training per commit defeats the spec's objective; likelihood of deploying it is essentially zero; run it only as a measurement).
6. **Pre-registrations:** author program-format documents for steps 1–4 from `prereg_stubs.md`, after `cat -n` of the harness seams named there (law 4), each through the advisor and the cross-family reviewer at its gate.
7. **`research_and_specs/proposals/GPU_Procurement…md`:** a dated note that the Apple-Silicon claim predates D-HW-1 (optional; `contradictions.md` §4).
8. **Delete `_parts/`** at close-out if the folder should hold only final files.

## 4. Exit condition (met)

Every class has a disposition; every artifact is deduplicated against the inventory's verified list and the 2026-10-05 pass log; the two inventory contradictions are resolved; the two consecutive independent search instruments adding no new class and no new in-class method after dedupe were the research-CLI recency sweep and the arXiv locate-then-edit sweep (details in `dispositions.md`); the browser-source helper, returning afterwards, also added nothing.

## 5. What this pass did not do, stated plainly

No run of any kind (no edit, no smoke solve, no model load). No program-format pre-registration. The harness source (`c10e_bandknob.py`, `c10l_mint_lib.py`) and the engine source were not read; seam names in the stubs are taken from CORPUS/44–50 and must be confirmed against the files before authoring. `DISCIPLINE.md`, `SESSION_CHECKPOINT.md`, `docs/program_state.json`, `tools/closeout_check.py` and `docs/F1_DETERMINATION.md` were not read by the lead agent. No memory file was written (the brief forbids it).

## 6. Open questions for the operator (decisions, not tasks)

1. Who authors the fixed phrasing frames for step 1 and the surprisal-position rule for step 2, and how they are ledgered (the council and the spec's §8.5 both need an answer before a pre-registration freezes).
2. Whether the ceiling rule of D-C10k-rulings-2 is to be overridden if steps 1–4 are null and step 5 fails (the model axis: H-21 Qwen2.5-7B, H-23 MiMo-7B-Base, H-26 OLMo-2-7B).
3. Whether a closed-form variant of H-18 (minted row solved as a linear readout, no gradient) should re-enter the sequence after step 3's result.

## 7. Confidence, as stated to the operator

Closing C10 on the current model with steps 1–8: about 3 in 10. With the model axis: 4 to 5 in 10. Advancing the science durably: about 8 in 10. The two measurements that move the first number most are step 5's result and whether step 1 or 2 clears 30/72 on a second process.

## 8. Addendum (2026-10-06, after the program session's option-B ruling)

- Integration of every item in §3 is the **program session's** work, from this file and `contradictions.md`, through its §0.4 close-out gate. The research pass edited no tracker file at any point; the branch holds only `results/research_pass_2026-10-06/`.
- Line numbers for item 1 in this worktree (HEAD 545d11e lineage): the BetaEdit row with the "fabricated" wording is `EXPERIMENT_RUNBOOK.md` **line 297** (the inventory's "RB:295" is stale), and a second "fabricated" mention sits at **line 507** in §8 (Deps line of the A3 entry). The memory file's caveat paragraph is the last paragraph of `memory_mirror/betaedit-official-repo.md`.
- Two-way channel: the research pass writes one short markdown file per message to `/Users/robertrhu/.local/share/openresearch/files/llm-as-database-research-pass-2026-10-06/to_program/` named `YYYYMMDD-HHMM-<topic>.md`, never edits an old one; the program session replies into the research-pass chat. Three files were sent (handoff pointer, step-1 gate accepted, integration-scope question); the program session's answers are recorded in `prereg_stubs.md` (reconciliation note) and here.
- Step 1 is pre-registered by the program session as `D-C10s-sharedz` (`docs/C10S_SHARED_Z_PREREG.md`, v2 at program worktree 02a383f, v3 pending its Codex design pass).
