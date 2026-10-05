#!/usr/bin/env python3
"""D-C10k-keying-ablation close-out. Reads results/c10k_keying_ablation/summary.json (written by ablation_result_doc.py).
Usage: ablation_closeout.py corpus      → writes CORPUS/43 + fingerprint registry entry
       ablation_closeout.py propagate <8hex>   → stamps every canonical tracker (idempotent per file)"""
import os, sys, json
from pathlib import Path
os.chdir("/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a")
DID = "D-C10k-keying-ablation"; PREV = "D-C10k-route-a"; DATE = "2026-10-04"
R = "results/c10k_keying_ablation"; S = json.load(open(f"{R}/summary.json"))
assert S["complete"], "N = 1 chain incomplete — do not close out"
FR = S["frame"]; HF = FR.startswith("H-FRAME"); SUFF = S["claimB"].startswith("F3 SUFFICIENT")
fl = [r for r in S["fb_rows"] if r["locus"] == "last" and r["canon_full"]]; fs = [r for r in S["fb_rows"] if r["locus"] == "subject"]
fb_num = (f"real-country frame prompts flipped to the edited value {'/'.join(str(r['real_flipped_to_value']) for r in fl)} of 12 (subject-keyed {'/'.join(str(r['real_flipped_to_value']) for r in fs)}), "
          f"never-edited fictional frame prompts {'/'.join(str(r['bystander_flipped_to_value']) for r in fl)} of 6 (subject-keyed {'/'.join(str(r['bystander_flipped_to_value']) for r in fs)})") if fl else "probe not run"
if SUFF and HF:
    VERDICT = "KEYING LOCUS DECIDES WHAT IS WRITTEN — a last-token-keyed write is a frame write (F3 SUFFICIENT, MEMIT, N = 1, qualified)"
    SHORT = "last-token write = frame write (F3 SUFFICIENT in MEMIT, N = 1, qualified)"
elif SUFF and FR.startswith("BETWEEN"):
    VERDICT = "KEYING LOCUS DECIDES WHAT IS WRITTEN — a last-token-keyed write is read from the frame, not the subject (F3 SUFFICIENT, MEMIT, N = 1; frame-bleed BETWEEN)"
    SHORT = "last-token write is read from the frame, not the subject (F3 SUFFICIENT in MEMIT, N = 1)"
else:
    VERDICT = f"N = 24: {S['n24']}; N = 1: claim A {S['claimA']}, claim B {S['claimB']}; frame-bleed {FR}"
    SHORT = f"claim B {S['claimB']}; frame-bleed {FR}"
BT = FR.startswith("BETWEEN")
by_tot = sum(r["bystander_flipped_to_value"] for r in fl); re_tot = sum(r["real_flipped_to_value"] for r in fl)
ONE = (f"**{{ST}}** (keying-locus ablation in the program's MEMIT engine, `CORPUS/43`, {DATE}): **{VERDICT}.** "
       f"K1 gate PASS (A1 {S['K1']['A1']} / A2 {S['K1']['A2']} vs R0 94.4 / 98.6). At N = 24 the last-token cells do not land (K3/K4 canon {S['K3canon']['A1']} / {S['K4canon']['A1']} % A1) because the 24 last-token keys are one vector (cos ≥ 0.985, eff. rank 1.02; `keygram.json`) — key interference first, ridge second; z-probe clears the z-objective. "
       f"At N = 1 (the valid last-token cells) {S['landL']}/{S['nL']} last-token singles land with {S['paraL']}/{3*S['nL']} paraphrase hits while {S['highS']}/{S['nS']} subject-keyed singles land with ≥ 2/3 ({S['paraS']}/{3*S['nS']} hits). "
       f"Frame-bleed probe: {fb_num}. " +
       (f"Where a write is keyed decides what is written: keyed at the subject it is a subject fact (fits, transfers to paraphrases, flips 0 of {18*len(fs)} frame prompts); keyed at the prompt's final token it is a frame fact — read from the trained prompt only, and taken up by {by_tot}/{6*len(fl)} never-edited fictional frame prompts and {re_tot}/{12*len(fl)} real-country frame prompts (real capitals resist unless the write is large; the described-as probe sees none of it). F3 → EVIDENCE-SHOWS-in-MEMIT (N = 1, qualified); the Route A attribution itself stays I-INFER; the keying rule becomes unconditional for this mechanism class; option (ii) keeps its rationale with evidence; the small-ridge sweep and the covariance-corpus knob are not motivated by this result. " if SUFF and (HF or BT) else
        f"{S['claimB_why']} {S['claimA_why']} ") +
       f"K2 (subject, no templates) A1 {S['K2']['A1']} / A2 {S['K2']['A2']}: templates not necessary for ≥ 80 with subject keying. Scope 3B/fp16/band [4–8]/w 5000/1 seed; nothing to C10. Full detail `docs/C10K_KEYING_ABLATION_RESULT.md`.")

if sys.argv[1] == "corpus":
    fbt = ("| subject → value | locus | canon | para (of 3) | real frame prompts → value (of 12) | real capitals correct pre → post | bystander frame prompts → value (of 6) | described-as JS |\n|---|---|---|---|---|---|---|---|\n" +
           "".join(f"| {r['subject']} → {r['value']} | {r['locus']} | {'100' if r['canon_full'] else '0'} | {r['para_hits']} | **{r['real_flipped_to_value']}** | {r['real_top1_correct_pre']} → {r['real_top1_correct_post']} | **{r['bystander_flipped_to_value']}** | {r['described_as_js']} |\n" for r in S["fb_rows"]))
    doc = f"""# 43 — Keying-locus ablation in the program's MEMIT engine: {SHORT}

_Result {DATE}. Decision-ID {DID}. Pre-registered `docs/C10K_KEYING_ABLATION_PREREG.md` (v3 §3; amendments §6, §6b; three advisor rounds). Full detail `docs/C10K_KEYING_ABLATION_RESULT.md`. Records `results/c10k_keying_ablation/` (`K{{1..4}}.json`, `zprobe.json`, `keygram.json`, `n1/N1_*.json`, `n1/framebleed.json`); harness `experiments/track_c/c10e_bandknob.py` (knobs only; engine unmodified, LAW#5 INERT every cell); chains `tools/c10k_keying_ablation_chain.sh`, `tools/c10k_keying_ablation_n1.sh`; probe `experiments/track_c/c10k_keying_ablation_n1_framebleed.py`. Reviews: `logs/claude_c10k_keying_ablation_result_review{{,_v2}}.md`, `logs/codex_c10k_keying_ablation_result_review{{,_v2}}.md`._

## Claim class
**Single-variable mechanism test in the program's own engine (LAW#5: harness knobs only) — NOT C10 evidence (A7 untouched); sufficient-in-MEMIT at N = 1, not exclusive, not a re-run of Route A's modules.**

## VERDICT — {VERDICT}

**N = 24 (prereg §3):** {S['n24']}.

| cell | key locus | templates | A1 canon / para_full | A2 canon / para_full | validity |
|---|---|---|---|---|---|
| K1 | subject | on | 100 / **{S['K1']['A1']}** | 100 / **{S['K1']['A2']}** | valid (LAW#3 gate PASS) |
| K2 | subject | off | 100 / **{S['K2']['A1']}** | 100 / **{S['K2']['A2']}** | valid |
| K3 | last | on | {S['K3canon']['A1']} / **0.0** | {S['K3canon']['A2']} / **0.0** | INVALID (canon < 90) |
| K4 | last | off | {S['K4canon']['A1']} / **0.0** | {S['K4canon']['A2']} / **0.0** | INVALID (canon < 90) |

**Mechanism of the N = 24 failure (§3b–§3c):** z-probe — K3-style `compute_z` reaches the target (prob ≥ 0.983), so the loss is at the solve; keygram — the 24 last-token keys have pairwise cosine ≥ 0.985 and effective rank 1.02 at every band layer (subject keys 0.02–0.07, rank 16–23): one key, 24 targets → **interference first**; the ridge (5.7–60× over key energy at w = 5000 vs 0.5–5.3 for subject keys) second. Claim A: **{S['claimA']}** — {S['claimA_why']}

**N = 1 (prereg §6b; the valid last-token cells, w = 5000):** last-token singles land {S['landL']}/{S['nL']} with {S['paraL']}/{3*S['nL']} paraphrase hits; subject-keyed singles land {S['landS']}/{S['nS']} with {S['paraS']}/{3*S['nS']} hits ({S['highS']}/{S['nS']} at ≥ 2/3). Claim B: **{S['claimB']}** — {S['claimB_why']}

**Frame-bleed probe (§6b): {FR}.**

{fbt}
## Findings (scoped: Qwen2.5-3B base, fp16, band [4–8], w = 5000, 1 seed; N = 24 for the 2×2, N = 1 for six subjects, three in the probe; A1 single-token values)
- **F-A1 (EVIDENCE-SHOWS).** In the program's engine, 24 writes keyed at the prompt's final token do not land (canon {S['K3canon']['A1']} / {S['K4canon']['A1']} % A1) because their keys are one vector; the same 24 writes keyed at the subject land and transfer ({S['K1']['A1']} / {S['K1']['A2']}).
- **F-A2 (EVIDENCE-SHOWS).** A single write keyed at the prompt's final token lands ({S['landL']}/{S['nL']}) and is read from the trained prompt only ({S['paraL']}/{3*S['nL']} paraphrase hits); the same single write keyed at the subject lands and transfers ({S['paraS']}/{3*S['nS']}).
- **F-A3 (EVIDENCE-SHOWS).** {fb_num}: {"the landed last-token write is a write about the frame `… is the city of`, not about the subject — it rewrites the real capitals that share the frame, which the described-as locality probe cannot see." if HF else (f"the landed last-token write is read by prior-free prompts that share the frame `… is the city of` ({by_tot}/{6*len(fl)} never-edited fictional subjects take the value; real capitals resist in two of three cases and lose 9/12 in the third), damage the described-as locality probe cannot see; the subject-keyed write touches none of them." if BT else "see the probe table.")}
- **F-A4 (EVIDENCE-SHOWS).** Templates are not necessary for ≥ 80 % paraphrase transfer with subject keying (K2 {S['K2']['A1']} / {S['K2']['A2']}); they add about 4–8 points.
- **F-A5 (I-INFER).** Route A's F3 (the ported AnyEdit keys at the last prompt token, hence 0/72) is **sufficient in MEMIT** by F-A2/F-A3; it is not shown exclusive for Route A, whose modules also differ in z-objective, preservation term and projector and were not re-run with subject keying.

## What this changes
- The memory_mirror rule "read the keying locus against the generalisation criterion before porting an editor" becomes **unconditional for this mechanism class**: a last-token-keyed write is a frame write, not a subject fact. Option (ii) (subject-keyed per-token hybrid) keeps its rationale, now with in-engine evidence.
- The small-ridge sweep (§6) is not run and the covariance-corpus knob (Moir) is no longer motivated by this result: the ridge was not the primary limiter.
- C10 unchanged (A7 not run). The operator decision on the forward route stands: (i) LRE-faithfulness admission test, (ii) subject-keyed per-token hybrid, (iii) accept-bounded + side-store.
- Limitations: N = 1 and six subjects; single-token values; one seed; the claim-B criterion and the probe were pre-registered after three of twelve runs were visible (prereg §6b, timing disclosure).
"""
    open("CORPUS/43_C10K_KEYING_ABLATION.md", "w").write(doc)
    reg = json.load(open("tools/closeout_fingerprints.json"))
    reg[DID] = {"source": "CORPUS/43_C10K_KEYING_ABLATION.md", "what": f"keying-locus ablation in the vendored MEMIT engine: K1 gate PASS; N=24 last-token cells INVALID (key interference: 24 keys cos>=0.985); N=1 last-token singles land {S['landL']}/{S['nL']} with {S['paraL']}/{3*S['nL']} paraphrase hits vs subject-keyed {S['paraS']}/{3*S['nS']}; frame-bleed {FR}; {SHORT}"}
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
    if DID not in s: assert s.count(anchor) == 1; p.write_text(s.replace(anchor, f"## {DATE} - Keying-locus ablation in the MEMIT engine: {SHORT} ({DID})\n{ONE}\n\n" + anchor), encoding="utf-8"); print("inserted PROGRESS.md")
    ins_after("EVIDENCE_INDEX.md", f"- **{PREV} ⟨{PREV}@", f"- {ONE}")
    append("docs/HYPOTHESIS_REGISTER_2026-06-18.md", f"{ONE} Hypothesis status: 'keying locus is the cause of Route A's 0/72' — tested in the program's engine at N = 1: {S['claimB']}; frame-bleed {FR}. Sufficient in MEMIT; exclusivity for Route A untested.")
    append("CORPUS/00_MASTER_EVIDENCE.md", f"## {DATE} - Keying-locus ablation in the MEMIT engine ({DID})\n{ONE}")
    append("CORPUS/03_STATUS_LEDGER.md", f"## {DATE} - Keying-locus ablation ({DID})\n- {ONE}\n- C10 unchanged. Next: operator decision on the forward route (LRE-faithfulness admission test / subject-keyed hybrid / accept-bounded).")
    append("CORPUS/01_PROVENANCE_MANIFEST.md", f"| {ST} | c10e harness with `C10_KEY_LOCUS`/`C10_CTX_TEMPLATES`/`C10_ARMS`/`C10_RECIPES`/`N_EDIT`/`C10_SUBJECT_OFFSET` knobs (engine unmodified); chains `tools/c10k_keying_ablation_chain.sh`, `tools/c10k_keying_ablation_n1.sh`; probe `experiments/track_c/c10k_keying_ablation_n1_framebleed.py` | `results/c10k_keying_ablation/K1-4.json`, `zprobe.json`, `keygram.json`, `n1/N1_*.json`, `n1/framebleed.json`, `logs/c10k_keying_ablation_*.log` | K1 A1 {S['K1']['A1']} / A2 {S['K1']['A2']}; K3/K4 canon {S['K3canon']['A1']} / {S['K4canon']['A1']} para 0; keygram last-token cos ≥ 0.985 rank 1.02; N=1 last-token land {S['landL']}/{S['nL']} para {S['paraL']}/{3*S['nL']}, subject para {S['paraS']}/{3*S['nS']}; frame-bleed {fb_num} | CORPUS/43 |")
    append("CORPUS/02_VANDV_CHAIN.md", f"### C-C10k-ka - Keying-locus ablation ({ST})\n- **Hypothesis:** keying the write at the prompt's final token (instead of the subject's last token) removes held-out-paraphrase generalisation in the program's own MEMIT engine.\n- **Method:** 2×2 (key locus × context templates) on A1/A2, N = 24, same engine/covariance/ridge/band; K1 as LAW#3 gate; validity = canon ≥ 90 + keyed-token + identical eval strings. Then (§6b) z-probe, key Gram matrices, N = 1 singles × 6 subjects × both loci, frame-bleed probe on 12 real + 6 bystander frame prompts.\n- **Criterion:** §3 SUFFICIENT needs valid K3/K4 < 20 with K2 ≥ 80; §6b SUFFICIENT (N = 1) needs ≥ 5/6 landed last-token singles with ≤ 1/3 paraphrases and ≥ 5/6 subject singles with ≥ 2/3; frame-bleed H-frame = ≥ 6/12 real and ≥ 3/6 bystander flips vs ≤ 1 for the control.\n- **Verdict:** N = 24 INVALID (interference, not ridge); N = 1 {S['claimB']}; frame-bleed {FR} → {SHORT}.")
    ins_after("docs/EXPERIMENT_REGISTRY.md", "| **C10K-route-a** |", f"| **C10K-keying-ablation** | track_c | does keying at the prompt's final token remove paraphrase generalisation in the vendored MEMIT engine? | c10e harness knobs, 2×2 at N = 24 (K1 LAW#3 gate), z-probe, key Gram, N = 1 singles, frame-bleed probe | `results/c10k_keying_ablation/`, `docs/C10K_KEYING_ABLATION_RESULT.md` | CORPUS/43 | {SHORT} {ST} (N = 24 last-token cells INVALID by key interference; N = 1 last-token singles land {S['landL']}/{S['nL']} with {S['paraL']}/{3*S['nL']} paraphrase hits vs subject {S['paraS']}/{3*S['nS']}; frame-bleed {FR}) |")
    ins_after("EXPERIMENT_RUNBOOK.md", f"- **{PREV} ⟨{PREV}@", f"- **{ST} (CORPUS/43) — keying ablation in the program's engine: {SHORT}.** N = 24 last-token cells INVALID (24 keys are one vector → interference first, ridge second); N = 1 last-token singles land {S['landL']}/{S['nL']} and transfer {S['paraL']}/{3*S['nL']} vs subject-keyed {S['paraS']}/{3*S['nS']}; frame-bleed {FR}. Keying rule unconditional for this mechanism class; option (ii) keeps its rationale; small-ridge sweep and covariance knob not motivated.", region=("## §5", "## §6"))
    ins_after("EXPERIMENT_RUNBOOK.md", f"C10K Route A on the M3 Pro — HALTED — CONTROLS_NOT_RECOVERED {DATE} ({PREV}", f"- **Keying-locus ablation {DATE} ({ST}, CORPUS/43): {SHORT}** — in the vendored engine a last-token-keyed write is a frame write: at N = 24 nothing lands (24 keys one vector), at N = 1 it lands, is read from the trained prompt only ({S['paraL']}/{3*S['nL']} paraphrases vs subject-keyed {S['paraS']}/{3*S['nS']}), and {'rewrites the real capitals sharing the frame' if HF else ('is taken up by prior-free frame prompts (' + str(by_tot) + '/' + str(6*len(fl)) + ' bystanders) while real capitals mostly resist' if BT else 'frame-bleed ' + FR)}. F3 sufficient in MEMIT; C10 unchanged.", region=("## §12", "## §13"))
    Rb = Path("EXPERIMENT_RUNBOOK.md"); s = Rb.read_text(encoding="utf-8")
    if f"### §13 changelog — {DATE} (keying ablation" not in s: Rb.write_text(s.rstrip("\n") + f"\n\n### §13 changelog — {DATE} (keying ablation: {SHORT})\n{ONE} Harness: LAW#5 parity check made knob-independent; `C10_ARMS`/`C10_RECIPES`/`N_EDIT`/`C10_SUBJECT_OFFSET` knobs; frame-bleed probe script.\n", encoding="utf-8"); print("runbook §13 appended")
    P = Path("docs/program_state.json"); st = json.loads(P.read_text(encoding="utf-8"))
    if not st["current_latest"].startswith("**⮕ KEYING ABLATION"):
        st["current_latest"] = (f"**⮕ KEYING ABLATION ({DATE}): {SHORT.upper()} ⟨{DID}@{FP}⟩ — CORPUS/43.** In the program's own MEMIT engine (unmodified), *where* a write is keyed decides *what* is written. Keyed at the subject's last token the write is a subject fact (K1 A1 {S['K1']['A1']} / A2 {S['K1']['A2']}; singles transfer {S['paraS']}/{3*S['nS']}). Keyed at the prompt's final token it is a frame fact: at N = 24 the 24 keys are one vector (cos ≥ 0.985, eff. rank 1.02) and nothing lands (canon {S['K3canon']['A1']} / {S['K4canon']['A1']} %, interference first, ridge second — z-probe clears the z-objective); at N = 1 it lands ({S['landL']}/{S['nL']}), is read from the trained prompt only ({S['paraL']}/{3*S['nL']} paraphrases), and {'overwrites the real capitals that share the frame (frame-bleed ' + fb_num + ')' if HF else ('is taken up by prior-free prompts that share the frame (' + fb_num + ') while real capitals mostly resist' if BT else 'frame-bleed ' + FR)}. Route A's F3 is **sufficient in MEMIT (N = 1, qualified)**; the Route A attribution itself stays I-INFER (modules not re-run subject-keyed). The keying rule is unconditional for this mechanism class; option (ii) keeps its rationale with evidence; the small-ridge sweep and the covariance-corpus knob are not motivated. C10 unchanged. **The operator decision on the forward route stands: (i) LRE-faithfulness admission test, (ii) subject-keyed per-token hybrid, (iii) accept-bounded + side-store.**\n\n" + st["current_latest"])
    st["updated"] = f"{DATE} (keying ablation: {SHORT}; Route A HALTED; operator decision on the forward route)"
    i1 = next(i for i, v in enumerate(st["next_actions"]) if "(1) C10 — **C10K Route A (ported AnyEdit) = HALTED" in v)
    if DID not in st["next_actions"][i1]: st["next_actions"][i1] = st["next_actions"][i1].replace("(1) C10 — **C10K Route A (ported AnyEdit) = HALTED", f"(1) C10 — **Keying ablation = {SHORT} ⟨{DID}@{FP}⟩ (CORPUS/43): in the program's engine a last-token-keyed write is a frame write (N = 24: interference, nothing lands; N = 1: lands, no paraphrase transfer {S['paraL']}/{3*S['nL']} vs subject {S['paraS']}/{3*S['nS']}, {'rewrites real capitals sharing the frame' if HF else 'frame-bleed ' + FR}); F3 sufficient in MEMIT; keying rule unconditional; option (ii) keeps its rationale.** Prior: **C10K Route A (ported AnyEdit) = HALTED", 1)
    P.write_text(json.dumps(st, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"); print("program_state updated")
    C = Path("SESSION_CHECKPOINT.md"); c = C.read_text(encoding="utf-8"); anchor = f"## FRESH SESSION HANDOFF - {DATE} (C10K Route A HALTED — CONTROLS_NOT_RECOVERED; operator decision on the forward route)\n"
    if DID not in c:
        assert c.count(anchor) == 1
        C.write_text(c.replace(anchor, f"""## FRESH SESSION HANDOFF - {DATE} (keying ablation: {SHORT}; Route A HALTED; operator decision pending)

**Start here after context reset.** Two decisions closed today: **{PREV}** (Route A HALTED, CORPUS/42) and **{ST}** (CORPUS/43; `docs/C10K_KEYING_ABLATION_RESULT.md`). The ablation found that in the program's own engine *where* a write is keyed decides *what* is written: keyed at the subject it is a subject fact (fits, transfers to paraphrases, leaves other countries alone); keyed at the prompt's final token it is a frame fact — at N = 24 the 24 keys are one vector and nothing lands (interference first, ridge second); at N = 1 it lands, is read from the trained prompt only ({S['paraL']}/{3*S['nL']} paraphrases vs {S['paraS']}/{3*S['nS']} subject-keyed), and {'rewrites every real capital that shares the frame (' + fb_num + ')' if HF else ('is taken up by prior-free frame prompts (' + fb_num + ') while real capitals mostly resist' if BT else 'frame-bleed ' + FR)}. Route A's F3 is sufficient in MEMIT (N = 1, qualified); the keying rule is unconditional for this mechanism class; the small-ridge sweep and the covariance knob are not motivated. Prior art added today: `docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md`, `docs/PRIOR_ART_ANYEDITPP_BAYES_CHUNK_2026.md`, `docs/PRIOR_ART_SWEEP_2026-10-04.md` (+ `docs/CONNECTED_PAPERS_GRAPH_INDEX_2026-10-04.md`), `docs/PRIOR_ART_CHRISHAYUK_LARQL_2026-10.md`.

**The next step is an operator decision, not a run:** (i) LRE-faithfulness admission-test prereg (recommended; must first reproduce the R0 split post hoc), (ii) subject-keyed per-token hybrid (re-implementation; its rationale now has in-engine evidence), (iii) accept-bounded + side-store routing.


""" + anchor), encoding="utf-8"); print("checkpoint handoff inserted")
    ins_after("memory_mirror/MEMORY.md", "- [Read keying locus before porting an editor]", f"- [Last-token-keyed write is a frame write, not a subject fact](last-token-keyed-write-is-a-frame-write.md) - {DATE} keying ablation ({DID}, CORPUS/43): N=24 keys one vector → nothing lands; N=1 lands, {S['paraL']}/{3*S['nL']} paraphrases vs subject {S['paraS']}/{3*S['nS']}; frame-bleed {FR}")
    Path("memory_mirror/last-token-keyed-write-is-a-frame-write.md").write_text(f"""# A write keyed at the prompt's final token is a frame write, not a subject fact (program engine)

**Fact ({DATE}, {ST}, CORPUS/43):** in the vendored MEMIT engine (unmodified; w = 5000; band [4–8]; Qwen2.5-3B), the 24 keys taken at the prompt's final token `" of"` are one vector (pairwise cosine ≥ 0.985, effective rank 1.02 at every band layer; subject keys cosine 0.02–0.07, rank 16–23), so a batch of 24 last-token writes does not land (canon {S['K3canon']['A1']} / {S['K4canon']['A1']} %) — key interference first, the covariance ridge second (z-probe clears the z-objective). A single last-token write lands ({S['landL']}/{S['nL']}) but transfers to {S['paraL']}/{3*S['nL']} held-out paraphrases (subject-keyed singles {S['paraS']}/{3*S['nS']}) and — frame-bleed probe — {fb_num}: {'it rewrites every real capital that shares the frame, which the described-as locality probe cannot see.' if HF else ('prior-free prompts that share the frame take the value (' + str(by_tot) + '/' + str(6*len(fl)) + ' bystanders) and real capitals resist unless the write is large (one of three lost 9/12) — damage the described-as probe cannot see.' if BT else FR + '.')}

**How to apply:** before porting or designing any editor, read where it keys the write; a last-token (frame) key cannot encode a subject fact in this engine, whatever the ridge. Check locality with prompts that share the written frame, not only with described-as probes. Do not spend compute on small-ridge or covariance-corpus sweeps to rescue last-token keying. Supersedes the conditional reading in [[read-keying-locus-before-porting-an-editor]]; the Route A attribution (F3) is sufficient-in-MEMIT, exclusivity untested.
""", encoding="utf-8"); print("memory_mirror written")
