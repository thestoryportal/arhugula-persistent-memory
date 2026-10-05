#!/usr/bin/env python3
"""D-C10k-keying-ablation close-out: (a) CORPUS/43 + registry entry; then (after --fp) (b) propagate the stamp to every tracker.
Usage: ablation_closeout.py corpus      → writes CORPUS/43 + registry
       ablation_closeout.py propagate <8hex>"""
import os, sys, json
from pathlib import Path
os.chdir("/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a")
DID = "D-C10k-keying-ablation"; PREV = "D-C10k-route-a"; DATE = "2026-10-04"
R = "results/c10k_keying_ablation"; K = {}
for k in ("K1", "K2", "K3", "K4"):
    d = json.load(open(f"{R}/{k}.json")); K[k] = d["recipes"][k]["arms"]
A = lambda k, arm, f: K[k][arm][f]
k2ok = A("K2", "A1_single", "canon_full") >= 90 and A("K2", "A2_coherent2", "canon_full") >= 90
k2_line = (f"K2 (subject keying, templates off): A1 para {A('K2','A1_single','para_full')} / A2 {A('K2','A2_coherent2','para_full')} (canon {A('K2','A1_single','canon_full')} / {A('K2','A2_coherent2','canon_full')}) → " +
           ("templates are not what carries paraphrase generalisation; the locus is." if k2ok and A("K2", "A1_single", "para_full") >= 80 else ("templates are a factor; no keying claim from K2." if k2ok else "K2 INVALID (canon < 90).")))
VERDICT = "INVALID-LAST-TOKEN-CELLS — no keying reading; writability finding"
ONE = (f"**{{ST}}** (keying-locus ablation in the program's MEMIT engine, `CORPUS/43`, {DATE}): **{VERDICT}.** "
       f"K1 gate PASS (A1 {A('K1','A1_single','para_full')} / A2 {A('K1','A2_coherent2','para_full')} vs R0 94.4 / 98.6). Keying the same writes at the prompt's final token (K3/K4, templates on/off) fits the trained prompt on only "
       f"{A('K3','A1_single','canon_full')} / {A('K4','A1_single','canon_full')} % of A1 (A2 {A('K3','A2_coherent2','canon_full')} / {A('K4','A2_coherent2','canon_full')} %), paraphrases 0/72, locality untouched — INVALID by the pre-registered canon ≥ 90 rule: "
       f"last-token keys are not writable under the Wikipedia covariance ridge (behavioural face of Route A's ridge diagnostic). {k2_line} "
       "F3 stays I-INFER (supported by the combined Route A + ablation picture, not proven causal); the memory_mirror keying rule stays conditional. Full detail `docs/C10K_KEYING_ABLATION_RESULT.md`.")
if sys.argv[1] == "corpus":
    doc = f"""# 43 — Keying-locus ablation in the program's MEMIT engine: INVALID-LAST-TOKEN-CELLS (writability finding)

_Result {DATE}. Decision-ID {DID}. Pre-registered `docs/C10K_KEYING_ABLATION_PREREG.md` (v3; two advisor rounds). Full detail `docs/C10K_KEYING_ABLATION_RESULT.md`. Records `results/c10k_keying_ablation/K{{1..4}}.json`; harness `experiments/track_c/c10e_bandknob.py`; chain `tools/c10k_keying_ablation_chain.sh`. Advisor on the result: `logs/claude_c10k_keying_ablation_result_review.md`._

## Claim class
**Single-variable mechanism test in the program's own engine (LAW#5: engine unmodified; harness knobs only) — NOT C10 evidence (A7 untouched) and NOT a causal verdict on Route A's F3.**

## VERDICT — {VERDICT}

| cell | key locus | templates | A1 canon / para_full / described-as JS | A2 canon / para_full / JS | validity |
|---|---|---|---|---|---|
""" + "".join(f"| {k} | {loc} | {tm} | {A(k,'A1_single','canon_full')} / **{A(k,'A1_single','para_full')}** / {A(k,'A1_single','locality_described_as')} | {A(k,'A2_coherent2','canon_full')} / **{A(k,'A2_coherent2','para_full')}** / {A(k,'A2_coherent2','locality_described_as')} | {'valid' if A(k,'A1_single','canon_full') >= 90 and A(k,'A2_coherent2','canon_full') >= 90 else 'INVALID (canon < 90)'} |\n"
             for k, loc, tm in (("K1","subject","on"),("K2","subject","off"),("K3","last","on"),("K4","last","off"))) + f"""
## Findings (scoped: Qwen2.5-3B base, fp16, band [4–8], ridge 5000·C, N = 24, 1 seed)
- **F-A1 (EVIDENCE-SHOWS).** In the program's engine, a write keyed at the prompt's final token does not land: trained-prompt fit 25–29 % (A1) and 4–8 % (A2) against 100 % for the subject-keyed write on the same subjects, with locality untouched and update norms *larger* than K1's. This is the behavioural face of the Route A ridge diagnostic (last-token keys 17–180× under the covariance ridge).
- **F-A2 (EVIDENCE-SHOWS).** {k2_line}
- **F-A3 (I-INFER).** With Route A (projector + 1000× smaller ridge forces the last-token write in: trained prompt 24/24, paraphrases 0/72), no observed configuration lets a last-token-keyed write generalise, and the subject-keyed write does on the same stimuli; the pre-registered SUFFICIENT reading is nonetheless not reached, because the last-token cells are INVALID by construction of the engine's ridge, so F3 remains I-INFER.

## What this changes
- The memory_mirror rule (read the keying locus against the generalisation criterion before porting) stays **conditional**. Option (ii) (subject-keyed per-token hybrid) keeps its rationale without new evidence.
- New local reason to pre-register the **covariance-corpus knob** (Moir; `docs/PRIOR_ART_SWEEP_2026-10-04.md` §3.4) before any further keying experiment: the Wikipedia covariance forbids last-token writes in this engine.
- C10 unchanged (A7 not run).
"""
    open("CORPUS/43_C10K_KEYING_ABLATION.md", "w").write(doc)
    reg = json.load(open("tools/closeout_fingerprints.json")); reg[DID] = {"source": "CORPUS/43_C10K_KEYING_ABLATION.md", "what": "keying-locus ablation in the vendored MEMIT engine: K1 gate PASS; last-token cells INVALID (canon 25-29%, para 0/72, locality intact) — last-token keys not writable under the covariance ridge; F3 stays I-INFER; rule conditional"}
    json.dump(reg, open("tools/closeout_fingerprints.json", "w"), indent=1, ensure_ascii=False); print("CORPUS/43 + registry written")
else:
    FP = sys.argv[2]; ST = f"{DID} ⟨{DID}@{FP}⟩"; ONE = ONE.replace("{ST}", ST)
    def sub(path, old, new):
        p = Path(path); s = p.read_text(encoding="utf-8"); assert s.count(old) == 1, (path, old[:60]); p.write_text(s.replace(old, new), encoding="utf-8"); print("edited", path)
    def ins_after(path, anchor_sub, text, region=None):
        p = Path(path); lines = p.read_text(encoding="utf-8").split("\n")
        lo, hi = 0, len(lines)
        if region:
            lo = next(i for i, l in enumerate(lines) if l.startswith(region[0])); hi = next(i for i in range(lo + 1, len(lines)) if lines[i].startswith(region[1]))
        if any(DID in l for l in lines[lo:hi]): print("already has", path); return
        idx = [i for i in range(lo, hi) if anchor_sub in lines[i]]; assert idx, (path, anchor_sub[:50])
        lines.insert(idx[0] + 1, text); p.write_text("\n".join(lines), encoding="utf-8"); print("inserted", path)
    def append(path, text):
        p = Path(path); s = p.read_text(encoding="utf-8")
        if DID in s: print("already has", path); return
        p.write_text(s.rstrip("\n") + "\n\n" + text + "\n", encoding="utf-8"); print("appended", path)
    c = Path("CORPUS/43_C10K_KEYING_ABLATION.md").read_text(encoding="utf-8")
    if f"Decision-ID {DID}." in c: sub("CORPUS/43_C10K_KEYING_ABLATION.md", f"Decision-ID {DID}.", f"Decision-ID {ST}.")
    p = Path("PROGRESS.md"); s = p.read_text(encoding="utf-8"); anchor = f"## {DATE} - C10K Route A (ported AnyEdit) on the M3 Pro: HALTED — CONTROLS_NOT_RECOVERED ({PREV})\n"
    if DID not in s: assert s.count(anchor) == 1; p.write_text(s.replace(anchor, f"## {DATE} - Keying-locus ablation in the MEMIT engine: INVALID-LAST-TOKEN-CELLS ({DID})\n{ONE}\n\n" + anchor), encoding="utf-8"); print("inserted PROGRESS.md")
    ins_after("EVIDENCE_INDEX.md", f"- **{PREV} ⟨{PREV}@", f"- {ONE}")
    append("docs/HYPOTHESIS_REGISTER_2026-06-18.md", f"{ONE} Hypothesis status: 'keying locus is the cause of Route A's 0/72' — tested in the program's engine; last-token cells INVALID (the ridge forbids the write), so the hypothesis stays open/supported, not confirmed.")
    append("CORPUS/00_MASTER_EVIDENCE.md", f"## {DATE} - Keying-locus ablation in the MEMIT engine ({DID})\n{ONE}")
    append("CORPUS/03_STATUS_LEDGER.md", f"## {DATE} - Keying-locus ablation ({DID})\n- {ONE}\n- C10 unchanged. Next: operator decision on the forward route (LRE-faithfulness admission test / subject-keyed hybrid / accept-bounded) with the covariance-corpus knob (Moir) as the first cheap pre-registration.")
    append("CORPUS/01_PROVENANCE_MANIFEST.md", f"| {ST} | c10e harness with `C10_KEY_LOCUS`/`C10_CTX_TEMPLATES`/`C10_ARMS`/`C10_RECIPES` knobs (engine unmodified); chain `tools/c10k_keying_ablation_chain.sh` | `results/c10k_keying_ablation/K1-4.json`, `dryrun_keyed_token.json`, `logs/c10k_keying_ablation_*.log` | K1 A1 {A('K1','A1_single','para_full')} / A2 {A('K1','A2_coherent2','para_full')}; K3 canon {A('K3','A1_single','canon_full')} para 0; K4 canon {A('K4','A1_single','canon_full')} para 0; K2 A1 {A('K2','A1_single','para_full')} | CORPUS/43 |")
    append("CORPUS/02_VANDV_CHAIN.md", f"### C-C10k-ka - Keying-locus ablation ({ST})\n- **Hypothesis:** keying the write at the prompt's final token (instead of the subject's last token) removes held-out-paraphrase generalisation in the program's own MEMIT engine.\n- **Method:** 2×2 (key locus × context templates) on A1/A2, N = 24, same engine/covariance/ridge/band; K1 as LAW#3 gate; validity = canon ≥ 90 + keyed-token + identical eval strings.\n- **Criterion (prereg v3 §3 precedence):** SUFFICIENT needs valid K3/K4 < 20 with K2 ≥ 80.\n- **Verdict:** INVALID-LAST-TOKEN-CELLS — the last-token write does not land (canon 25–29 %), so no keying reading; writability finding recorded; F3 stays I-INFER.")
    ins_after("docs/EXPERIMENT_REGISTRY.md", "| **C10K-route-a** |", f"| **C10K-keying-ablation** | track_c | does keying at the prompt's final token remove paraphrase generalisation in the vendored MEMIT engine? | c10e harness knobs, 2×2, K1 LAW#3 gate | `results/c10k_keying_ablation/`, `docs/C10K_KEYING_ABLATION_RESULT.md` | CORPUS/43 | INVALID-LAST-TOKEN-CELLS {ST} (last-token write does not land: canon 25–29 %, para 0/72; F3 stays I-INFER) |")
    ins_after("EXPERIMENT_RUNBOOK.md", f"- **{PREV} ⟨{PREV}@", f"- **{ST} (CORPUS/43) — keying ablation in the program's engine: last-token cells INVALID (the covariance ridge forbids the write; canon 25–29 %, para 0/72), K1 gate PASS, K2 {A('K2','A1_single','para_full')}.** F3 stays I-INFER; the keying rule stays conditional; next cheap prereg = covariance-corpus knob (Moir).", region=("## §5", "## §6"))
    ins_after("EXPERIMENT_RUNBOOK.md", f"C10K Route A on the M3 Pro — HALTED — CONTROLS_NOT_RECOVERED {DATE} ({PREV}", f"- **Keying-locus ablation {DATE} ({ST}, CORPUS/43): INVALID-LAST-TOKEN-CELLS** — in the vendored engine a last-token-keyed write does not land (canon 25–29 %, para 0/72, locality intact); subject-keyed K1 reproduces R0; F3 stays I-INFER; covariance-corpus knob is the next cheap prereg.", region=("## §12", "## §13"))
    Rb = Path("EXPERIMENT_RUNBOOK.md"); s = Rb.read_text(encoding="utf-8")
    if f"### §13 changelog — {DATE} (keying ablation" not in s: Rb.write_text(s.rstrip("\n") + f"\n\n### §13 changelog — {DATE} (keying ablation INVALID-LAST-TOKEN-CELLS)\n{ONE} Harness: LAW#5 parity check made knob-independent; `C10_ARMS`/`C10_RECIPES` knobs.\n", encoding="utf-8"); print("runbook §13 appended")
    S = Path("docs/program_state.json"); st = json.loads(S.read_text(encoding="utf-8"))
    if not st["current_latest"].startswith("**⮕ KEYING ABLATION"):
        st["current_latest"] = (f"**⮕ KEYING ABLATION ({DATE}): INVALID-LAST-TOKEN-CELLS ⟨{DID}@{FP}⟩ — CORPUS/43.** In the program's own MEMIT engine (unmodified), writes keyed at the prompt's final token do not land (trained-prompt fit 25–29 % on A1, 4–8 % on A2, paraphrases 0/72, locality untouched) while the subject-keyed K1 reproduces R0 (A1 {A('K1','A1_single','para_full')} / A2 {A('K1','A2_coherent2','para_full')}); K2 (subject keying, no templates) A1 {A('K2','A1_single','para_full')}. The last-token cells are INVALID by the pre-registered canon ≥ 90 rule, so the ablation yields a writability finding (the Wikipedia covariance ridge forbids last-token writes; behavioural face of the Route A ridge diagnostic) and no causal keying verdict: Route A's F3 stays I-INFER, the keying rule stays conditional. **Next cheap pre-registration: the covariance-corpus knob (Moir, self-generated-text covariance) before any further keying or capacity experiment; the operator decision on the forward route (LRE-faithfulness admission test / subject-keyed hybrid / accept-bounded) stands.**\n\n" + st["current_latest"])
    st["updated"] = f"{DATE} (keying ablation INVALID-LAST-TOKEN-CELLS; Route A HALTED; operator decision on the forward route)"
    i1 = next(i for i, v in enumerate(st["next_actions"]) if "(1) C10 — **C10K Route A (ported AnyEdit) = HALTED" in v)
    if DID not in st["next_actions"][i1]: st["next_actions"][i1] = st["next_actions"][i1].replace("(1) C10 — **C10K Route A (ported AnyEdit) = HALTED", f"(1) C10 — **Keying ablation = INVALID-LAST-TOKEN-CELLS ⟨{DID}@{FP}⟩ (CORPUS/43): last-token writes do not land in the program's engine; F3 stays I-INFER; next cheap prereg = covariance-corpus knob (Moir).** Prior: **C10K Route A (ported AnyEdit) = HALTED", 1)
    S.write_text(json.dumps(st, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"); print("program_state updated")
    C = Path("SESSION_CHECKPOINT.md"); c = C.read_text(encoding="utf-8"); anchor = f"## FRESH SESSION HANDOFF - {DATE} (C10K Route A HALTED — CONTROLS_NOT_RECOVERED; operator decision on the forward route)\n"
    if DID not in c:
        assert c.count(anchor) == 1
        C.write_text(c.replace(anchor, f"""## FRESH SESSION HANDOFF - {DATE} (keying ablation INVALID-LAST-TOKEN-CELLS; Route A HALTED; operator decision pending)

**Start here after context reset.** Two decisions closed today: **{PREV}** (Route A HALTED, CORPUS/42) and **{ST}** (CORPUS/43; `docs/C10K_KEYING_ABLATION_RESULT.md`). The ablation found that in the program's own engine a write keyed at the prompt's final token does not land at all (canon 25–29 %, para 0/72, locality intact) while the subject-keyed write reproduces R0 — so the Wikipedia covariance ridge forbids last-token writes and Route A's keying mechanism (F3) stays I-INFER, supported by the combined picture but not proven causal. Prior art added today: `docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md`, `docs/PRIOR_ART_ANYEDITPP_BAYES_CHUNK_2026.md`, `docs/PRIOR_ART_SWEEP_2026-10-04.md` (+ `docs/CONNECTED_PAPERS_GRAPH_INDEX_2026-10-04.md`).

**The next step is an operator decision, not a run:** (i) LRE-faithfulness admission-test prereg (recommended; must first reproduce the R0 split post hoc), (ii) subject-keyed per-token hybrid (re-implementation), (iii) accept-bounded + side-store routing. **Before any of them, the cheapest pre-registration is the covariance-corpus knob (Moir): self-generated-text covariance instead of Wikipedia, tested first on the K3/K4 cells (does a last-token write land under a different covariance?) and on locality.**


""" + anchor), encoding="utf-8"); print("checkpoint handoff inserted")
    ins_after("memory_mirror/MEMORY.md", "- [Read keying locus before porting an editor]", f"- [Last-token keys not writable under the Wikipedia covariance ridge](last-token-keys-not-writable-under-covariance-ridge.md) - {DATE} keying ablation ({DID}, CORPUS/43): canon 25–29 % vs 100 % subject-keyed; para 0/72; test the covariance corpus (Moir) before further keying experiments")
    Path("memory_mirror/last-token-keys-not-writable-under-covariance-ridge.md").write_text(f"""# Last-token keys are not writable under the Wikipedia covariance ridge (program engine)

**Fact ({DATE}, {ST}, CORPUS/43):** in the vendored MEMIT engine (unmodified; ridge 5000·C; band [4–8]), a write keyed at the prompt's final token fits the trained prompt on 25–29 % of A1 items (4–8 % of A2), paraphrases 0/72, locality untouched, update norms larger than the subject-keyed write that fits 100 %. Route A's ridge diagnostic measured why: last-token keys lie 17–180× under the covariance ridge at every band layer.

**How to apply:** do not run keying-locus experiments through a covariance-ridge solve without first checking writability (single-key gain) at that locus; pre-register the covariance-corpus knob (Moir) before the next keying or capacity experiment; the Route A keying rule stays conditional until a configuration exists where a last-token write both lands and is tested on paraphrases in this engine.
""", encoding="utf-8"); print("memory_mirror written")
