#!/usr/bin/env python3
"""Route A close-out, step B: carry D-C10k-route-a (stamped) into every canonical tracker — pointer + one-line verdict, no restated copy.
Usage: closeout_b_propagate.py <8hex>  (from: python3 tools/closeout_check.py --fp D-C10k-route-a)"""
import sys, json, os
from pathlib import Path
os.chdir("/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a")
FP = sys.argv[1]; DID = "D-C10k-route-a"; ST = f"{DID} ⟨{DID}@{FP}⟩"; DATE = "2026-10-04"; PREV = "D-C10k-m3pro-stage0"
ONE = (f"**{ST}** (C10K Route A — ported official AnyEdit on the M3 Pro, `CORPUS/42`, {DATE}): **HALTED — CONTROLS_NOT_RECOVERED.** "
       "At upstream L2=10 the ported AlphaEdit_ARE solve realises 5–13 % of the residual (A1/A2 para 0/72); the one allowed fix (L2 → 0.01, calibration rule) restores the trained prompt (24/24 every arm) but paraphrases stay 0/72 and locality breaks (NLL +0.26–0.35 nats). "
       "Mechanism: last-prompt-token keying gives ~0 paraphrase hidden-state transfer at any ridge (subject-token linear decoding, Hernandez 2024). C10 stays OPEN. Forward (operator): LRE-faithfulness admission test / subject-keyed hybrid / accept-bounded (`docs/C10K_ROUTEA_RESULT.md` §5).")

def sub(path, old, new, count=1):
    p = Path(path); s = p.read_text(encoding="utf-8"); n = s.count(old); assert n == count, f"{path}: {n}x {old[:70]!r}"
    p.write_text(s.replace(old, new), encoding="utf-8"); print("edited", path)
def ins_after(path, anchor_sub, text):
    p = Path(path); lines = p.read_text(encoding="utf-8").split("\n")
    if any(DID in l for l in lines): print("already has", path); return
    idx = [i for i, l in enumerate(lines) if anchor_sub in l]; assert idx, f"{path}: anchor {anchor_sub[:50]!r}"
    lines.insert(idx[0] + 1, text); p.write_text("\n".join(lines), encoding="utf-8"); print("inserted", path)
def append(path, text):
    p = Path(path); s = p.read_text(encoding="utf-8")
    if DID in s: print("already has", path); return
    p.write_text(s.rstrip("\n") + "\n\n" + text + "\n", encoding="utf-8"); print("appended", path)
def prepend_section(path, anchor_line, text):
    p = Path(path); s = p.read_text(encoding="utf-8")
    if DID in s: print("already has", path); return
    assert s.count(anchor_line) == 1, (path, anchor_line); p.write_text(s.replace(anchor_line, text + anchor_line), encoding="utf-8"); print("inserted", path)

# CORPUS/42 stamp
if f"Decision-ID {DID}." in Path("CORPUS/42_C10K_ROUTEA_CONTROLS_NOT_RECOVERED.md").read_text(encoding="utf-8"): sub("CORPUS/42_C10K_ROUTEA_CONTROLS_NOT_RECOVERED.md", f"Decision-ID {DID}.", f"Decision-ID {ST}.")
else: print("CORPUS/42 already stamped")
# PROGRESS.md (newest first)
prepend_section("PROGRESS.md", f"## {DATE} - C10K Stage 0 on the M3 Pro: HALTED - HARDWARE_ENVELOPE ({PREV})\n", f"## {DATE} - C10K Route A (ported AnyEdit) on the M3 Pro: HALTED — CONTROLS_NOT_RECOVERED ({DID})\n{ONE}\n\n")
# EVIDENCE_INDEX.md, HYPOTHESIS_REGISTER, CORPUS/00, /03: after the stage0 line
ins_after("EVIDENCE_INDEX.md", f"- **{PREV} ⟨{PREV}@", f"- {ONE}")
append("docs/HYPOTHESIS_REGISTER_2026-06-18.md", f"{ONE} Hypothesis status: the ported official AnyEdit (Route A) does **not** recover the A1/A2 controls on the program's held-out-paraphrase criterion; the C10 rescue hypothesis via AnyEdit-port is HALTED on this hardware/port; the mechanism (keying locus) is a new, testable hypothesis (LRE-faithfulness admission test).")
append("CORPUS/00_MASTER_EVIDENCE.md", f"## {DATE} - C10K Route A (ported AnyEdit) on the M3 Pro: HALTED — CONTROLS_NOT_RECOVERED ({DID})\n{ONE}")
append("CORPUS/03_STATUS_LEDGER.md", f"## {DATE} - C10K Route A on the M3 Pro ({DID})\n- {ONE}\n- C10 status unchanged: OPEN/BLOCKING. The AnyEdit-port route is HALTED at the controls (one fix spent). Next is an operator decision (`docs/C10K_ROUTEA_RESULT.md` §5).")
append("CORPUS/01_PROVENANCE_MANIFEST.md", f"| {ST} | ported `external_prior_art/AnyEdit@057a77f1` (device-only diff) on Qwen2.5-3B base fp32/MPS; launcher `experiments/track_c/c10k_route_a_launcher.py`; chain `tools/c10k_route_a_chain.sh` | `results/c10k_route_a/R1_w1_*_L2-10.json`, `R1_w1_*.json`, `solve_gain_diag.json`, `solve_backtest.json`, `projector_gate_v2*.json`, `anchor*.json`, `R0_baseline.json`, `logs/route_a_chain*.log` | L2=10: A1 para 0/72 canon 11/24, A2 0/72; gain 0.05–0.13; L2=0.01: canon 24/24 all arms, para 0/72, hidden transfer canonical 1.00 / paraphrase 0.009, NLL +0.26/+0.35, real-country 10/12, JS 87/83 | CORPUS/42 |")
append("CORPUS/02_VANDV_CHAIN.md", f"### C-C10k-ra - C10K Route A ported AnyEdit controls ({ST})\n- **Hypothesis:** the official AnyEdit modules, ported device-only and run on Qwen2.5-3B base, recover the A1/A2 controls (`para_full ≥ 80`) and can then be read on A7.\n- **Method:** prereg + 3 amendments; projector gate v2 + controls; D5 anchor; R0 LAW#3; R1 controls at L2=10, one fix (L2=0.01) and rerun; back-test of the solve; A7/memit_ARE diagnostic-only.\n- **Measurement:** canon/para full-sequence hits, locality (real-country, JS, stock item, generic NLL), band norms, realised-residual fractions, hidden-state transfer.\n- **Criterion (prereg §3):** A1 and A2 `para_full ≥ 80` after at most one localized fix → else HALTED.\n- **Verdict:** HALTED — CONTROLS_NOT_RECOVERED (0/72 both arms at both ridges; trained prompt 24/24 after the fix). Mechanism: last-prompt-token keying, ~0 paraphrase transfer.")
# EXPERIMENT_REGISTRY row after the stage0 row
ins_after("docs/EXPERIMENT_REGISTRY.md", "| **C10K-stage0-m3pro** |",
          f"| **C10K-route-a** | track_c | does the ported official AnyEdit recover the A1/A2 controls on Qwen2.5-3B base (then A7)? | `experiments/track_c/c10k_route_a_launcher.py` + `tools/c10k_route_a_chain.sh` (prereg + Amendments 1–3) | `results/c10k_route_a/`, `architecture_profile/c10k_route_a_halt_diagnostic.json` | CORPUS/42 | HALTED — CONTROLS_NOT_RECOVERED {ST} (para 0/72 both arms at L2=10 and 0.01; canon 24/24 after the fix; keying mechanism) |")
# runbook §5.3 decisions ledger (after the stage0 bullet), §12 dashboard (after stage0 bullet), §13 changelog (append)
ins_after("EXPERIMENT_RUNBOOK.md", f"- **{PREV} ⟨{PREV}@", f"- **{ST} (CORPUS/42) — Route A HALTED at the controls; the one allowed fix (ridge rescale) restores the trained prompt only.** Paraphrase 0/72 at every ridge because the port keys at the last prompt token (~0 hidden-state transfer to paraphrases); rescaling the ridge to write at all breaks locality. C10 stays OPEN; forward is an operator decision (LRE-faithfulness admission test recommended).")
R = Path("EXPERIMENT_RUNBOOK.md"); lines = R.read_text(encoding="utf-8").split("\n")
s12 = next(i for i, l in enumerate(lines) if l.startswith("## §12")); s13 = next(i for i, l in enumerate(lines) if l.startswith("## §13"))
if not any(DID in l for l in lines[s12:s13]):
    j = next(i for i in range(s12, s13) if f"C10K Stage 0 on the M3 Pro — HALTED - HARDWARE_ENVELOPE {DATE} ({PREV}" in lines[i]); indent = lines[j][: len(lines[j]) - len(lines[j].lstrip())]
    lines.insert(j + 1, f"{indent}- **C10K Route A on the M3 Pro — HALTED — CONTROLS_NOT_RECOVERED {DATE} ({ST}, CORPUS/42):** ported official AnyEdit: A1/A2 paraphrase 0/72 at upstream L2=10 (solve realises 12–28 % of the residual) and after the one fix (L2=0.01: canon 24/24, para 0/72, locality breached). Mechanism = keying locus (ablation pre-registered). Not a method verdict on AnyEdit's own metrics. Operator decision next.")
    R.write_text("\n".join(lines), encoding="utf-8"); print("inserted runbook §12")
else: print("runbook §12 already has it")
R = Path("EXPERIMENT_RUNBOOK.md"); s = R.read_text(encoding="utf-8")
if f"### §13 changelog — {DATE} (C10K Route A" not in s:
    R.write_text(s.rstrip("\n") + f"\n\n### §13 changelog — {DATE} (C10K Route A HALTED — CONTROLS_NOT_RECOVERED)\n{ONE} Prereg `docs/C10K_ROUTEA_LOCAL_PORT_PREREG.md` + Amendments 1–3 (projector per-layer thresholds + controls; fp32 on MPS; ridge rescale). Prior art added: `docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md`, `docs/PRIOR_ART_ANYEDITPP_BAYES_CHUNK_2026.md`.\n", encoding="utf-8"); print("runbook §13 appended")
# program_state.json → render
S = Path("docs/program_state.json"); st = json.loads(S.read_text(encoding="utf-8"))
new_latest = (f"**⮕ C10K ROUTE A ({DATE}): HALTED — CONTROLS_NOT_RECOVERED ⟨{DID}@{FP}⟩ — CORPUS/42.** The official AnyEdit modules, ported device-only (D1) and run fp32 on MPS on Qwen2.5-3B base, do not recover the A1/A2 controls on the program's held-out-paraphrase criterion: at upstream `L2=10` the AlphaEdit_ARE solve realises 5–13 % of the residual (para 0/72); the one allowed fix (`L2 → 0.01` by a calibration-only rule, Amendment 3) restores the trained prompt on every arm (24/24) but paraphrases stay 0/72 and locality breaks (generic NLL +0.26–0.35 nats, real-country 10/12, JS 83–87). Mechanism (back-test): the port keys the write at the last prompt token; hidden-state transfer to paraphrases is 0.8–1.8 % at any ridge, which the recall-mechanism literature predicts (relations decode from the subject's last token — Hernandez et al. ICLR 2024, `docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md`); AnyEdit/AnyEdit++ score BLEU on the trained prompt = the canonical read, not the paraphrase criterion (`docs/PRIOR_ART_ANYEDITPP_BAYES_CHUNK_2026.md`). Surviving findings F1–F4 (projector strips 56–76 % of edit-key norm, L8 non-protective; L2=10 non-functional on 3B; keying → ~0 transfer; magnitude restores at locality cost). Four advisor rounds. **C10 stays OPEN/BLOCKING; the AnyEdit-port route is HALTED on local hardware. OPERATOR DECISION: (i) LRE-faithfulness admission-test prereg (recommended; local, cheap), (ii) subject-keyed per-token hybrid re-implementation, (iii) accept-bounded + side-store routing.**\n\n")
if not st["current_latest"].startswith("**⮕ C10K ROUTE A"): st["current_latest"] = new_latest + st["current_latest"]
st["updated"] = f"{DATE} (C10K Route A HALTED — CONTROLS_NOT_RECOVERED on the M3 Pro; operator decision on the forward route; Stage 0 halt; Phase 3 + B3 local serving done)"
old1 = "(1) C10 — **C10K Stage 0 on the M3 Pro = HALTED - HARDWARE_ENVELOPE"
i1 = next(i for i, v in enumerate(st["next_actions"]) if old1 in v)
st["next_actions"][i1] = st["next_actions"][i1].replace(old1, f"(1) C10 — **C10K Route A (ported AnyEdit) = HALTED — CONTROLS_NOT_RECOVERED ⟨{DID}@{FP}⟩ (CORPUS/42, {DATE}; `docs/C10K_ROUTEA_RESULT.md`)**: controls para 0/72 at L2=10 and after the one fix; keying-locus mechanism; locality breaks when the write magnitude is restored. **OPERATOR DECISION:** (i) LRE-faithfulness admission-test prereg (recommended), (ii) subject-keyed per-token hybrid (re-implementation), (iii) accept-bounded. Prior: **C10K Stage 0 on the M3 Pro = HALTED - HARDWARE_ENVELOPE", 1)
S.write_text(json.dumps(st, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"); print("program_state updated")
# SESSION_CHECKPOINT handoff (top)
C = Path("SESSION_CHECKPOINT.md"); c = C.read_text(encoding="utf-8")
anchor = "## FRESH SESSION HANDOFF - 2026-10-04 (overnight autonomous run; C10K Stage 0 HALTED on the M3 Pro — operator fork)\n"
assert c.count(anchor) == 1
block = f"""## FRESH SESSION HANDOFF - {DATE} (C10K Route A HALTED — CONTROLS_NOT_RECOVERED; operator decision on the forward route)

**Start here after context reset.** Route A (the operator's choice after CORPUS/41) ran end to end on the M3 Pro under a prereg with three advisor-reviewed amendments: **{ST}** (CORPUS/42; `docs/C10K_ROUTEA_RESULT.md`). The ported official AnyEdit recovers the trained prompt (24/24 on every arm once the ridge is rescaled) and **never the paraphrases (0/72)**; the back-test shows why (keying at the last prompt token → ~0 hidden-state transfer at any ridge), and rescaling the ridge to write at all breaks locality. The AnyEdit-port route is HALTED on local hardware; C10 stays OPEN/BLOCKING.

**Prior art added today (operator-supplied):** `docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md` (relations decode linearly from the subject's last token; open-range name relations are not linear) and `docs/PRIOR_ART_ANYEDITPP_BAYES_CHUNK_2026.md` (long-form lineage keys inside the written context and scores BLEU on the trained prompt). Together they frame the result and the value-class split.

**The next step is an operator decision, not a run:** (i) pre-register the LRE-faithfulness admission test (recommended: local, cheap, predicts the value-class split; read Christ 2025, Choe 2025, "Keys to Robust Edits" first); (ii) subject-keyed per-token hybrid as a re-implementation; (iii) accept-bounded with coined multi-word values routed to the side-store.

**Local infra state:** fp32 on MPS works for 3B (Amendment 2); launcher enforces projector hash + key dtype; chain script in `tools/`; Command Line Tools still broken (prebuilt llama.cpp); backup launchd blocked by TCC until Removable Volumes access is granted.


"""
C.write_text(c.replace(anchor, block + anchor), encoding="utf-8"); print("checkpoint handoff inserted")
# memory_mirror fact
Path("memory_mirror/anyedit-port-keys-at-last-prompt-token-no-paraphrase-transfer.md").write_text(f"""# AnyEdit-family ports key the write at the last prompt token → ~0 paraphrase transfer on Qwen2.5-3B

**Fact ({DATE}, {ST}, CORPUS/42):** the official AnyEdit modules (AlphaEdit_ARE / memit_ARE), ported device-only and run fp32 on the M3 Pro, fit the trained prompt (24/24) and never the paraphrases (0/72) on the A1/A2 controls, at upstream's ridge and after the one allowed rescale. Hidden-state transfer at the z-layer: canonical 1.00, paraphrase 0.01. The write is keyed at the last prompt token and answer-internal positions (`compute_z.py:91`), not the subject token.

**Why:** relations are decoded linearly from the subject's last token (Hernandez et al. ICLR 2024); a write keyed downstream of that in the template's context is not read from other templates. AnyEdit/AnyEdit++ evaluate BLEU on the trained prompt, which does not measure this.

**How to apply:** do not spend compute re-tuning a faithful AnyEdit port against the paraphrase gate; test linear decodability of the target relation first (LRE-faithfulness admission test), or build a subject-keyed hybrid as a re-implementation. `docs/C10K_ROUTEA_RESULT.md`.
""", encoding="utf-8"); print("memory_mirror written")
Path("memory_mirror/read-keying-locus-before-porting-an-editor.md").write_text(f"""# Read a ported editor's keying locus against the generalisation criterion BEFORE spending compute

**Learning ({DATE}, {ST}):** AnyEdit's ARE keys every write at the last token of the prompt-plus-answer-so-far input (`compute_z.py:85-91`); for one- and two-token answers that collapses to a single window keyed at the prompt's last token, outside AnyEdit's long-form regime. The program's control gate (`para_full ≥ 80` on held-out paraphrases) was therefore unreachable by construction, which was readable from the source before any run; it was only predicted after R1 at upstream L2 (Amendment 3).

**How to apply:** at prereg time, for any ported in-weight method, write down (a) where the key is read (token position, templates), (b) what the program's generalisation criterion requires of that key, and (c) a hidden-space transfer check on 3 items if (a) and (b) disagree. If the port cannot pass the criterion by construction, pre-register it as diagnostic, not as a rescue candidate.
""", encoding="utf-8"); print("memory_mirror learning written")
ins_after("memory_mirror/MEMORY.md", "- [AnyEdit local transplant controls fail before A7](anyedit-local-transplant-controls-fail-before-a7.md)",
          f"- [Read keying locus before porting an editor](read-keying-locus-before-porting-an-editor.md) - process learning from Route A ({DID}): the control gate was unreachable by construction, readable from compute_z.py:85-91 before any run\n" + f"- [AnyEdit port keys at last prompt token → no paraphrase transfer](anyedit-port-keys-at-last-prompt-token-no-paraphrase-transfer.md) - {DATE} Route A HALTED CONTROLS_NOT_RECOVERED ({DID}, CORPUS/42): trained prompt 24/24, paraphrases 0/72 at any ridge; test linear decodability (LRE) before any further in-weight port")
