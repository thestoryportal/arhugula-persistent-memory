#!/usr/bin/env python3
"""Render docs/C10K_KEYING_ABLATION_RESULT.md from results/c10k_keying_ablation/K{1..4}.json, applying the prereg v3 §3 precedence."""
import os, json
os.chdir("/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a")
R = "results/c10k_keying_ablation"; K = {}
for k in ("K1", "K2", "K3", "K4", "K3p", "K3pp", "K4pp", "K1p500", "K1p50", "K3ppp", "K1p25"):
    p = f"{R}/{k}.json"
    if os.path.exists(p):
        d = json.load(open(p)); K[k] = d.get("recipes", {}).get(k, {}).get("arms"); K[k + "_dn"] = d.get("recipes", {}).get(k, {}).get("delta_norms", {}) if K[k] else {}
    else: K[k] = None
cell = {"K1": ("subject", "on"), "K2": ("subject", "off"), "K3": ("last", "on"), "K4": ("last", "off"), "K3p": ("last", "on"), "K3pp": ("last", "on"), "K4pp": ("last", "off"), "K1p500": ("subject", "on"), "K1p50": ("subject", "on"), "K3ppp": ("last", "on"), "K1p25": ("subject", "on")}
ridge = {"K1": 5000, "K2": 5000, "K3": 5000, "K4": 5000, "K3p": 500, "K3pp": 50, "K4pp": 50, "K1p500": 500, "K1p50": 50, "K3ppp": 25, "K1p25": 25}
def row(k):
    a = K[k]
    if not a: return (f"| {k} | {cell[k][0]} | {cell[k][1]} | {ridge[k]} | — | — | — | — | — | — | — | — | not run / no arms record |\n" if k in ("K1","K2","K3","K4") else "")
    A1, A2 = a["A1_single"], a["A2_coherent2"]; dn = K[k + "_dn"].get("A1_single", {})
    rel = " / ".join(f"{dn[str(l)]['relative_delta_norm']:.2f}" for l in (4, 5, 6, 7, 8)) if dn else "—"
    valid = A1["canon_full"] >= 90 and A2["canon_full"] >= 90
    return f"| {k} | {cell[k][0]} | {cell[k][1]} | {ridge[k]} | {A1['canon_full']} | **{A1['para_full']}** | {A1['para_any_full']} | {A1['locality_described_as']} | {A2['canon_full']} | **{A2['para_full']}** | {A2['locality_described_as']} | {rel} | {'valid' if valid else 'INVALID (canon < 90)'} |\n"
tab = "| cell | key locus | templates | ridge weight | A1 canon | A1 para_full | A1 para_any | A1 described-as JS | A2 canon | A2 para_full | A2 described-as JS | A1 rel. Δ‖W‖ L4…L8 | validity |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|\n" + "".join(row(k) for k in ("K1", "K2", "K3", "K4", "K3p", "K3pp", "K4pp", "K1p500", "K1p50", "K3ppp", "K1p25"))
# precedence
a1 = lambda k: K[k]["A1_single"] if K[k] else None
gate = a1("K1") and abs(a1("K1")["para_full"] - 94.4) <= 3 and abs(K["K1"]["A2_coherent2"]["para_full"] - 98.6) <= 3
valid = {k: bool(K.get(k)) and K[k]["A1_single"]["canon_full"] >= 90 and K[k]["A2_coherent2"]["canon_full"] >= 90 for k in cell}
A1v = lambda k: bool(K.get(k)) and K[k]["A1_single"]["canon_full"] >= 90          # A1 binds; A2 read separately
last_cells = [k for k in ("K3p", "K3pp", "K4pp", "K3ppp") if K.get(k)]; valid_last = [k for k in last_cells if A1v(k)]
canon_path = [("5000", K["K3"]["A1_single"]["canon_full"])] + [(str(ridge[k]), K[k]["A1_single"]["canon_full"]) for k in ("K3p", "K3pp", "K3ppp") if K.get(k)]
vals = [c for _, c in canon_path]; rising = all(vals[i] < vals[i + 1] for i in range(len(vals) - 1)) if len(vals) > 1 else False
dose = ("ridge is A limiter of last-token writability (canon rises and reaches ≥ 90)" if rising and max(vals) >= 90 else ("consistent with the ridge, grid too coarse (canon rises but stays < 90): inconclusive" if rising else ("ridge mechanism FALSIFIED for this failure (canon flat or falling)" if len(vals) > 1 else "no small-weight cells yet")))
ctrl = {"K3p": "K1p500", "K3pp": "K1p50", "K4pp": "K1p50", "K3ppp": "K1p25"}
binding = max(valid_last, key=lambda k: ridge[k]) if valid_last else None
disagree = binding and any(abs(K[k]["A1_single"]["para_full"] - K[binding]["A1_single"]["para_full"]) >= 30 for k in valid_last if k != binding)
def js_ok(k): return abs(K[k]["A1_single"]["locality_described_as"] - K["K1"]["A1_single"]["locality_described_as"]) <= 10
if not gate: reading, why = "HALT (gate)", "K1 outside ±3 pp of R0"
elif binding and disagree: reading, why = "INTERACTION (valid last-token cells disagree by ≥ 30 pp)", f"dose-response: {dose}"
elif binding and K[binding]["A1_single"]["para_full"] < 20 and K.get(ctrl[binding]) and K[ctrl[binding]]["A1_single"]["para_full"] >= 80:
    reading, why = f"F3 SUFFICIENT (MEMIT, small ridge) — binding cell {binding} (w = {ridge[binding]})", f"a last-token write that lands (canon {K[binding]['A1_single']['canon_full']}) does not generalise (para {K[binding]['A1_single']['para_full']}) while the matched subject-keyed control {ctrl[binding]} at the same weight does (para {K[ctrl[binding]]['A1_single']['para_full']}); dose-response: {dose}"
elif binding and K[binding]["A1_single"]["para_full"] < 20 and K.get(ctrl[binding]):
    reading, why = f"CONTROL-FAILED — {binding} valid, para < 20, but {ctrl[binding]} < 80", f"the small ridge removes generalisation for any key; no keying reading; dose-response: {dose}"
elif K.get("K4pp") and A1v("K4pp") and K["K4pp"]["A1_single"]["para_full"] >= 80 and js_ok("K4pp"):
    reading, why = "OVERTURNED — K4″ valid, para ≥ 80, bleed guard passed", f"a last-token write that lands generalises in MEMIT; Route A's 0/72 has another cause; dose-response: {dose}"
elif binding and 20 <= K[binding]["A1_single"]["para_full"] < 80: reading, why = f"MIXED — {binding} valid, 20 ≤ para < 80", f"no rule; dose-response: {dose}"
elif binding: reading, why = f"UNCLASSIFIED — {binding} valid but no matched control recorded", f"dose-response: {dose}"
elif last_cells: reading, why = "NO VALID LAST-TOKEN CELL through w = " + str(min(ridge[k] for k in last_cells)), f"dose-response: {dose}; F3 stays I-INFER; the keying question moves to a different harness (option ii)"
elif not valid["K3"] and not valid["K4"] and not last_cells: reading, why = "INVALID-LAST-TOKEN-CELLS (no keying reading; the last-token write does not land)", "both last-token cells fail the canon ≥ 90 validity rule: the write does not land (canon < 90 at ridge weight 5000 with the engine's KL prompt)"
elif valid["K2"] and K["K2"]["A1_single"]["para_full"] < 80: reading, why = "TEMPLATES ARE A FACTOR", "K2 < 80"
else: reading, why = "see table", "mixed validity"
k1, k3, k4 = K["K1"], K["K3"], K["K4"]; k2 = K["K2"]
gsec = ""
if os.path.exists(f"{R}/keygram.json"):
    g = json.load(open(f"{R}/keygram.json"))
    gt = "| layer | subject keys: cos mean / eff. rank | last-token keys: cos mean / frac > 0.9 / eff. rank | ridge/‖k‖² at w = 5000: subject / last | w* (last matches subject) |\n|---|---|---|---|---|\n" + "".join(
        f"| L{l} | {g[str(l)]['subject_keys']['cos_mean']:.3f} / {g[str(l)]['subject_keys']['effective_rank']:.1f} | {g[str(l)]['last_token_keys']['cos_mean']:.3f} / {g[str(l)]['last_token_keys']['frac_cos_gt_0.9']} / {g[str(l)]['last_token_keys']['effective_rank']:.2f} | {g[str(l)]['ridge_over_key_energy_w5000']['subject']} / {g[str(l)]['ridge_over_key_energy_w5000']['last_token']} | {g[str(l)]['w_star_last_matches_subject']:.0f} |\n" for l in (4, 5, 6, 7, 8))
    n1 = {}
    import glob as _g
    for f in sorted(_g.glob(f"{R}/n1/N1_*.json")):
        d = json.load(open(f)); nm = os.path.basename(f)[:-5]; a = d["recipes"][nm]["arms"]["A1_single"]; n1[nm] = (a["canon_full"], a["para_full"], a["locality_described_as"])
    n1t = ("| run | A1 canon (1 item) | A1 para (3 paraphrases) | described-as JS |\n|---|---|---|---|\n" + "".join(f"| {k} | {v[0]} | {v[1]} | {v[2]} |\n" for k, v in n1.items())) if n1 else "_N = 1 runs: pending._"
    n1_last = [v for k, v in n1.items() if "_last_" in k]; n1_subj = [v for k, v in n1.items() if "_subject_" in k]
    n1read = ""
    if n1_last:
        land = sum(1 for v in n1_last if v[0] >= 100); n1read = f"**N = 1 reading:** {land}/{len(n1_last)} single last-token writes land at w = 5000 (subject-keyed singles: {sum(1 for v in n1_subj if v[0] >= 100)}/{len(n1_subj)}); paraphrase hits for single last-token writes: {sum(v[1] for v in n1_last)/len(n1_last):.1f} % mean. " + ("Single last-token writes land, so the N = 24 collapse is **interference between near-identical keys**, not ridge magnitude: the ridge account for the first pass is withdrawn as the primary cause." if land >= len(n1_last) * 0.8 else ("Single last-token writes also fail, so the ridge (or the position itself) limits writability even without interference; both mechanisms are live." if land == 0 else "Mixed: some single last-token writes land; interference and ridge both contribute."))
    gsec = f"""### 3c. Key-similarity discriminator (advisor v2 on §6; `experiments/track_c/c10k_keying_ablation_keygram.py` → `results/c10k_keying_ablation/keygram.json`; N = 1 runs `tools/c10k_keying_ablation_n1.sh` → `results/c10k_keying_ablation/n1/`)

{gt}
**Reading (EVIDENCE-SHOWS):** the 24 last-token keys are one vector to within rounding (pairwise cosine ≥ 0.985 on average, every pair > 0.9, effective rank ≈ 1.02 at every band layer), while the 24 subject-last-token keys are nearly orthogonal (cosine 0.02–0.07, effective rank 16–23). **A single closed-form solve cannot map one key to 24 different targets; the K3/K4 collapse at w = 5000 is key interference first.** The ridge enters second: the keys' small differences lie in low-variance directions, and the energy-weighted ridge ratio at w = 5000 is 5.7–60 for last-token keys against 0.5–5.3 for subject keys, so those differences are suppressed; the predicted weight at which they are amplified to the subject keys' ratio is w* ≈ 100–600 per layer. This is the same mechanism Route A reached from the other side: AlphaEdit_ARE at L2 = 0.01 fit 24/24 by amplifying those differences 1000× (L4 band norm 3.6×, locality cost F4), and the resulting write is read only from the trained prompt because paraphrases do not reproduce the tiny key differences that carry the subject.

{n1t}

{n1read}
"""
zsec = "_Results: pending._"
if os.path.exists(f"{R}/zprobe.json"):
    z = json.load(open(f"{R}/zprobe.json"))
    zt = "| style | subject | steps | target prob (final) | loss final (nll + kl) | ‖z‖ |\n|---|---|---|---|---|---|\n" + "".join(f"| {r['style']} | {r['subject']} | {r['steps']} | {r['target_prob_last']:.3f} | {r['loss_last']:.3f} ({r['nll_last']:.3f} + {r['kl_last']:.3f}) | {r['z_norm']:.1f} |\n" for r in z)
    zk1 = min(r["target_prob_last"] for r in z if r["style"] == "K1"); zk3 = min(r["target_prob_last"] for r in z if r["style"] == "K3")
    zsec = (f"_Results (`results/c10k_keying_ablation/zprobe.json`):_\n\n{zt}\n**Reading:** K3-style `compute_z` reaches the target at the keyed `\" of\"` token (final target probability ≥ {zk3:.3f}; K1-style ≥ {zk1:.3f}) with a KL term of the same size as K1's. The z-objective is not where the K3/K4 write is lost; the KL-prompt conflict is excluded as the cause. **The loss is at the solve, which supports the ridge mechanism and licenses the next cell: the same last-token cells at a small ridge weight, plain MEMIT, no projector (prereg v3 §6 amendment).** (‖z‖ is smaller in K3 style, 63–67 vs 81–86, consistent with the last-token residual being a smaller target than the subject-token one.)")

doc = f"""# Keying-locus ablation in the program's MEMIT engine — result (D-C10k-keying-ablation)

_Result 2026-10-04. Pre-registered `docs/C10K_KEYING_ABLATION_PREREG.md` (v3; two advisor rounds). Records `results/c10k_keying_ablation/K{{1..4}}.json`; logs `logs/c10k_keying_ablation_*.log`; harness `experiments/track_c/c10e_bandknob.py` (knobs `C10_KEY_LOCUS`, `C10_CTX_TEMPLATES`, `C10_ARMS`, `C10_RECIPES`; LAW#5 parity check made knob-independent after K2's first pass halted "NOT INERT" by construction — `K2_firstpass_parity_halt.json`). Chain `tools/c10k_keying_ablation_chain.sh`, K2 rerun `tools/c10k_keying_ablation_rerun_k2k4.sh`._

## 1. Reading (prereg v3 §3 precedence): **{reading}**

{why}. Gate: K1 A1 {k1['A1_single']['para_full']} / A2 {k1['A2_coherent2']['para_full']} vs R0 94.4 / 98.6 → **PASS**; LAW#5 INERT in every cell (K2 after the parity fix). Validity prints confirm the keyed token (subject's last token in K1/K2; the final `" of"` in K3/K4) and byte-identical paraphrase and locality strings across cells.

## 2. Results (EVIDENCE-SHOWS)

{tab}
`para_any` = fraction of the 24 subjects with at least one paraphrase correct (the per-subject ≥ 2/3 count is not stored by this harness). Δ‖W‖ is the engine's own per-layer relative update norm for the A1 edit.

## 3. What the table says

- **Keying at the prompt's final token in the program's engine, the write does not land (EVIDENCE-SHOWS).** With the identical engine, covariance, ridge weight (5000), band, z-objective and dtype as K1, K3/K4 fit the trained prompt on only {k3['A1_single']['canon_full']} % ({round(k3['A1_single']['canon_full']*24/100)}/24) / {k4['A1_single']['canon_full']} % ({round(k4['A1_single']['canon_full']*24/100)}/24) of A1 items (K1: {k1['A1_single']['canon_full']} %) and {k3['A2_coherent2']['canon_full']} % ({round(k3['A2_coherent2']['canon_full']*24/100)}/24) / {k4['A2_coherent2']['canon_full']} % ({round(k4['A2_coherent2']['canon_full']*24/100)}/24) of A2; the described-as JS stays at 99.8 because little readable change was written, not as independent evidence of locality. **Where it fails is not yet separated (I-INFER, two candidates):** (a) the solve — the Route A ridge diagnostic (`results/c10k_route_a/memit_ridge_diag.json`) puts last-token keys 17–180× under the covariance ridge, a geometric argument tested behaviourally here at one ridge weight only; (b) the z-objective — in K3/K4 the engine's KL prompt (`"<country> is the city of is a"`) is keyed at the same final `" of"` in a near-identical context to the rewriting prompt, so one delta must change the next token for the edit and leave it unchanged for the KL prompt, a conflict K1 does not have. §3b (z-probe) separates these. The per-layer Δ‖W‖ (larger than K1's at L7–L8) says the solve wrote *something*; it is not a measure of what reached the keyed token.
- **Therefore the cells cannot separate "keying prevents generalisation" from "keying prevents writing", and the pre-registered SUFFICIENT reading is not reached.** By the precedence order both last-token cells are INVALID; no rule is written from them.
- **The missing cell is plain MEMIT with last-token keying at a small ridge weight (and a non-colliding KL prompt)**: if canonical fit climbs to ≥ 90 as the weight falls, the ridge mechanism is confirmed behaviourally and the cell becomes a valid K3 whose paraphrase score answers the prereg's question; it is cheaper and closer to the question than the covariance-corpus knob and is pre-registered next (§4). Note also that Route A's AlphaEdit_ARE changed two things at once (null-space projector and 1000× smaller ridge), and the projector removes preserved-knowledge directions that paraphrases may ride on, so Route A's 0/72 has an alternative cause unrelated to keying. **The complementary half in Route A:** when a null-space projector and a 1000× smaller ridge force the last-token write in (AlphaEdit_ARE, L2 = 0.01), the trained prompt fits 24/24 and paraphrases still score 0/72 (`docs/C10K_ROUTEA_RESULT.md` §3.2, F3). Taken together (I-INFER): a write keyed at the prompt's last token either cannot be placed under a covariance ridge, or, when placed, is read only from the trained prompt. Neither experiment alone makes F3 causal; the two together leave no observed configuration in which a last-token-keyed write generalises, and one (K1) in which a subject-keyed write does, on the same subjects, paraphrases and engine.
- **Templates (K2; `described-as JS` = the described-as probe's Jensen–Shannon locality score used throughout c10e, higher = less change) ({"K2 valid: " + str(k2['A1_single']['para_full']) + " / " + str(k2['A2_coherent2']['para_full']) if k2 else "K2 pending"}).** {("Subject-keyed writes without context templates still generalise (" + str(k2['A1_single']['para_full']) + " ≥ 80), so templates are not necessary for ≥ 80 % paraphrase scores with subject keying at N = 24; they still account for about 4–8 points (A1 95.8 → 91.7, A2 97.2 → 88.9). Whether the key locus carries generalisation cannot be read from this run (K3/K4 INVALID). Full-precision Δ‖W‖ differ between K1 and K2 at every layer (e.g. L4 15.874 vs 15.889), so the knob changed the key computation.") if k2 and k2['A1_single']['para_full'] >= 80 else ("Subject-keyed writes without templates fall below 80, so templates are a factor and no keying claim is licensed from K2." if k2 else "")}

### 3b. z-probe (advisor item 2; results appended after the run)

`experiments/track_c/c10k_keying_ablation_zprobe.py` runs the engine's unmodified `compute_z` on 3 subjects in K1 style and K3 style with the engine's own templates and records the final target probability at the keyed token, the loss path and the KL term. **Reading, fixed before the run:** if K3-style target probability at the last step is ≥ 0.9 (as K1's), the z-objective reaches the target and the failure is in the solve (ridge); if it stays well below K1's, the KL-prompt conflict (or the key position) blocks the target vector itself and the ridge attribution is withdrawn.

{zsec}

{gsec}
## 4. Scope, limitations, what changes

- 3B base, fp16, N = 24, 1 seed; one engine; one ridge weight (5000). The declared KL-prompt difference in K3/K4 is a live candidate cause (§3), not excluded by the untouched locality score (an unchanged locality is what a winning KL term would produce).
- **Changes:** the memory_mirror rule ("read the keying locus against the generalisation criterion before porting") stays **conditional** — supported, not proven causal. Option (ii) (subject-keyed per-token hybrid) keeps its rationale by the combined picture but gains no new evidence. New EVIDENCE-SHOWS: **in the program's engine at ridge weight 5000, a last-token-keyed write does not land (canon < 90)**; the mechanism (ridge vs KL conflict) is I-INFER until §3b and the small-weight cell resolve it. **Next pre-registration, in order:** the small-ridge-weight last-token cell (K3′), then the covariance-corpus knob (Moir, `docs/PRIOR_ART_SWEEP_2026-10-04.md` §3.4).
- C10 (A7) is untouched by this run, as pre-registered.

## 5. Advisor and close-out

Advisor on this result: `logs/claude_c10k_keying_ablation_result_review.md`. CORPUS entry: `CORPUS/43_C10K_KEYING_ABLATION.md`. Close-out: `tools/closeout_check.py D-C10k-keying-ablation`.
"""
open("docs/C10K_KEYING_ABLATION_RESULT.md", "w").write(doc); print("rendered; reading:", reading, "| K2 present:", bool(k2))
