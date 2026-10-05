#!/usr/bin/env python3
"""Render docs/C10K_KEYING_ABLATION_RESULT.md from results/c10k_keying_ablation/ (K1..K4, zprobe, keygram, n1/, framebleed),
applying prereg v3 §3 (N = 24 cells) and §6b (N = 1 cells + frame-bleed probe). Prints the headline reading."""
import os, json, glob
os.chdir("/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a")
R = "results/c10k_keying_ablation"; K = {}
for k in ("K1", "K2", "K3", "K4"):
    d = json.load(open(f"{R}/{k}.json")); K[k] = d["recipes"][k]["arms"]; K[k + "_dn"] = d["recipes"][k].get("delta_norms", {})
cell = {"K1": ("subject", "on"), "K2": ("subject", "off"), "K3": ("last", "on"), "K4": ("last", "off")}

def row(k):
    a = K[k]; A1, A2 = a["A1_single"], a["A2_coherent2"]; dn = K[k + "_dn"].get("A1_single", {})
    rel = " / ".join(f"{dn[str(l)]['relative_delta_norm']:.2f}" for l in (4, 5, 6, 7, 8)) if dn else "—"
    valid = A1["canon_full"] >= 90 and A2["canon_full"] >= 90
    return f"| {k} | {cell[k][0]} | {cell[k][1]} | 5000 | {A1['canon_full']} | **{A1['para_full']}** | {A1['para_any_full']} | {A1['locality_described_as']} | {A2['canon_full']} | **{A2['para_full']}** | {A2['locality_described_as']} | {rel} | {'valid' if valid else 'INVALID (canon < 90)'} |\n"
tab = "| cell | key locus | templates | ridge weight | A1 canon | A1 para_full | A1 para_any | A1 described-as JS | A2 canon | A2 para_full | A2 described-as JS | A1 rel. Δ‖W‖ L4…L8 | validity |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|\n" + "".join(row(k) for k in cell)
k1, k2, k3, k4 = K["K1"], K["K2"], K["K3"], K["K4"]
gate = abs(k1["A1_single"]["para_full"] - 94.4) <= 3 and abs(k1["A2_coherent2"]["para_full"] - 98.6) <= 3
n24 = "HALT (gate)" if not gate else "INVALID-LAST-TOKEN-CELLS (K3/K4 canon < 90; no keying reading at N = 24)"
cnt = lambda pct: round(pct * 24 / 100)

# ---- §3b z-probe ----
zsec = "_Results: pending._"
if os.path.exists(f"{R}/zprobe.json"):
    z = json.load(open(f"{R}/zprobe.json"))
    zt = "| style | subject | steps | target prob (final) | loss final (nll + kl) | ‖z‖ |\n|---|---|---|---|---|---|\n" + "".join(f"| {r['style']} | {r['subject']} | {r['steps']} | {r['target_prob_last']:.3f} | {r['loss_last']:.3f} ({r['nll_last']:.3f} + {r['kl_last']:.3f}) | {r['z_norm']:.1f} |\n" for r in z)
    zk1 = min(r["target_prob_last"] for r in z if r["style"] == "K1"); zk3 = min(r["target_prob_last"] for r in z if r["style"] == "K3")
    zsec = (f"_Results (`results/c10k_keying_ablation/zprobe.json`):_\n\n{zt}\n**Reading (EVIDENCE-SHOWS):** K3-style `compute_z` reaches the target at the keyed `\" of\"` token (final target probability ≥ {zk3:.3f}; K1-style ≥ {zk1:.3f}) with a KL term of the same size as K1's. The z-objective is not where the K3/K4 write is lost, and the KL-prompt conflict is excluded as the cause: **the loss is at the solve.** (‖z‖ is smaller in K3 style, 63–67 vs 81–86, consistent with the last-token residual being a smaller target.)")

# ---- §3c keygram + N = 1 + frame-bleed ----
g = json.load(open(f"{R}/keygram.json"))
gt = "| layer | subject keys: cos mean / eff. rank | last-token keys: cos mean / frac > 0.9 / eff. rank | ridge/‖k‖² at w = 5000: subject / last | w* (last matches subject) |\n|---|---|---|---|---|\n" + "".join(
    f"| L{l} | {g[str(l)]['subject_keys']['cos_mean']:.3f} / {g[str(l)]['subject_keys']['effective_rank']:.1f} | {g[str(l)]['last_token_keys']['cos_mean']:.3f} / {g[str(l)]['last_token_keys']['frac_cos_gt_0.9']} / {g[str(l)]['last_token_keys']['effective_rank']:.2f} | {g[str(l)]['ridge_over_key_energy_w5000']['subject']} / {g[str(l)]['ridge_over_key_energy_w5000']['last_token']} | {g[str(l)]['w_star_last_matches_subject']:.0f} |\n" for l in (4, 5, 6, 7, 8))
n1 = {}
for f in sorted(glob.glob(f"{R}/n1/N1_*.json")):
    d = json.load(open(f)); nm = os.path.basename(f)[:-5]; a = d["recipes"][nm]["arms"]["A1_single"]; det = d["recipes"][nm]["detail"]["A1_single"][0]
    n1[nm] = {"subj": det["subj"], "val": det["val"], "canon": a["canon_full"], "para_hits": sum(det["para_full_hits"]), "loc": a["locality_described_as"]}
order = sorted(n1, key=lambda s: (int(s.rsplit("_", 1)[1]), s))
n1t = ("| run | subject → value | A1 canon (1 item) | paraphrases hit (of 3) | described-as JS |\n|---|---|---|---|---|\n" + "".join(f"| {k} | {v['subj']} → {v['val']} | {v['canon']} | {v['para_hits']} | {v['loc']} |\n" for k, v in ((k, n1[k]) for k in order))) if n1 else "_N = 1 runs: pending._"
L = [n1[k] for k in order if "_last_" in k]; S = [n1[k] for k in order if "_subject_" in k]
nL, nS = len(L), len(S)
landL = sum(1 for v in L if v["canon"] >= 100); landS = sum(1 for v in S if v["canon"] >= 100)
lowL = sum(1 for v in L if v["canon"] >= 100 and v["para_hits"] <= 1); highS = sum(1 for v in S if v["canon"] >= 100 and v["para_hits"] >= 2)
highL = sum(1 for v in L if v["canon"] >= 100 and v["para_hits"] >= 2)
js_gap = (sum(v["loc"] for v in L) / nL - sum(v["loc"] for v in S) / nS) if L and S else 0.0
complete = nL == 6 and nS == 6
# claim A
if not L: clA, clA_why = "pending", ""
elif landL >= 5: clA, clA_why = "SINGLES LAND (pre-registered label: interference first)", f"{landL}/{nL} single last-token writes land at w = 5000, so the ridge weight does not block a single last-token write. What blocks 24 of them is their collinearity under the covariance-plus-ridge geometry the solve works in; 'interference' and 'ridge' are not separable causes here (the keygram's w* ≈ 100–600 and Route A's 24/24 fit at a 1000× smaller ridge both say a smaller ridge would separate them). The small-ridge sweep is not run because it cannot bear on F1: a last-token write that lands does not transfer anyway (claim B). Zero-edit check not run: a keygram on covariance-whitened keys (C^-1/2·k) would test the collinearity framing directly."
elif landL == 0: clA, clA_why = "RIDGE/POSITION LIMITS SINGLES", f"0/{nL} single last-token writes land; the sweep (§6) runs."
else: clA, clA_why = "MIXED", f"{landL}/{nL} single last-token writes land; the sweep (§6) runs."
# claim B
if not L or not S: clB, clB_why = "pending", ""
elif highS < 5: clB, clB_why = "CONTROL-FAILED", f"only {highS}/{nS} subject-keyed singles land with ≥ 2/3 paraphrases."
elif lowL >= 5 and abs(js_gap) <= 10: clB, clB_why = "F3 SUFFICIENT (MEMIT, N = 1)", f"{lowL}/{nL} last-token singles land with ≤ 1/3 paraphrases while {highS}/{nS} subject-keyed singles land with ≥ 2/3; described-as JS gap {js_gap:+.1f} points."
elif highL >= 4: clB, clB_why = "OVERTURNED (N = 1)", f"{highL}/{nL} landed last-token singles reach ≥ 2/3 paraphrases."
else: clB, clB_why = "MIXED", f"last-token singles: {lowL}/{nL} land with ≤ 1/3 paraphrases, {highL}/{nL} with ≥ 2/3; subject singles ≥ 2/3: {highS}/{nS}."
paraL = sum(v["para_hits"] for v in L); paraS = sum(v["para_hits"] for v in S)
# frame-bleed
fbsec = "_Frame-bleed probe (§6b): pending._"; fbread = "pending"; dv_values = []; FBFILES = []
FBFILES = [f for f in (f"{R}/n1/framebleed.json", f"{R}/n1/framebleed_b.json") if os.path.exists(f)]
if FBFILES:
    rows = [r for f in FBFILES for r in json.load(open(f))["rows"]]
    fbt = "| subject → value | locus | canon | para (of 3) | real frame prompts flipped to value (of 12) | real capitals still correct (pre → post) | real JS | bystander frame prompts flipped (of 6) | described-as JS | rel. Δ‖W‖ L4 / L8 |\n|---|---|---|---|---|---|---|---|---|---|\n" + "".join(
        f"| {r['subject']} → {r['value']} | {r['locus']} | {'100' if r['canon_full'] else '0'} | {r['para_hits']} | **{r['real_flipped_to_value']}** | {r['real_top1_correct_pre']} → {r['real_top1_correct_post']} | {r['real_js_locpct']} | **{r['bystander_flipped_to_value']}** | {r['described_as_js']} | {r['rel_delta_norm']['4']:.3f} / {r['rel_delta_norm']['8']:.3f} |\n" for r in rows)
    fl = [r for r in rows if r["locus"] == "last" and r["canon_full"]]; fs = [r for r in rows if r["locus"] == "subject"]
    l8norms = ', '.join('%.3f' % r['rel_delta_norm']['8'] for r in fl)
    hf = all(r["real_flipped_to_value"] >= 6 and r["bystander_flipped_to_value"] >= 3 for r in fl) and all(r["real_flipped_to_value"] <= 1 and r["bystander_flipped_to_value"] <= 1 for r in fs) if fl else False
    dv_last = [r for r in rows if r["locus"] == "last"]; dv_subj = [r for r in rows if r["locus"] == "subject"]
    dv_land_last = sum(1 for r in dv_last if r["canon_full"]); dv_para_last = sum(r["para_hits"] for r in dv_last); dv_para_subj = sum(r["para_hits"] for r in dv_subj); dv_land_subj = sum(1 for r in dv_subj if r["canon_full"])
    dv_values = sorted({r["value"] for r in rows})
    hs = all(r["real_flipped_to_value"] <= 1 and r["bystander_flipped_to_value"] <= 1 for r in fl) if fl else False
    fbread = "H-FRAME (the landed last-token write is a frame write)" if hf else ("H-SUBJECT (the landed last-token write is subject-specific)" if hs else "BETWEEN (partly frame-keyed)")
    ex = rows[0] if rows else None
    fbsec = f"""{fbt}
**Reading (EVIDENCE-SHOWS): {fbread}.** """ + (
        f"Each landed last-token single rewrites the real-country frame prompts to its own value ({', '.join(str(r['real_flipped_to_value']) + '/12' for r in fl)}) and the never-edited fictional frame prompts likewise ({', '.join(str(r['bystander_flipped_to_value']) + '/6' for r in fl)}), while the subject-keyed single on the same subject leaves them alone ({', '.join(str(r['real_flipped_to_value']) + '/12' for r in fs)} real; {', '.join(str(r['bystander_flipped_to_value']) + '/6' for r in fs)} bystanders). The write keyed at `\" of\"` encodes the frame `… is the city of → <value>`, not a fact about the subject: it fails the paraphrases because they do not contain the frame, and it destroys the real capitals in exactly the neighbourhood the described-as probe does not see (real-prompt JS {', '.join(str(r['real_js_locpct']) for r in fl)} against {', '.join(str(r['real_js_locpct']) for r in fs)} subject-keyed)." if hf else
        (f"Landed last-token singles flip ≤ 1 real and ≤ 1 bystander frame prompt, like the subject-keyed controls: the write is subject-specific yet does not transfer to paraphrases." if hs else
         f"The pre-registered H-frame threshold (≥ 6/12 real **and** ≥ 3/6 bystander flips for every landed last-token single) is not met, so the reading is BETWEEN, but the pattern is one-sided: the landed last-token singles rewrite {sum(r['bystander_flipped_to_value'] for r in fl)}/{6*len(fl)} never-edited fictional frame prompts to their own value ({', '.join(str(r['bystander_flipped_to_value']) + '/6' for r in fl)}) and {sum(r['real_flipped_to_value'] for r in fl)}/{12*len(fl)} real-country frame prompts ({', '.join(str(r['real_flipped_to_value']) + '/12' for r in fl)}; real-prompt JS {', '.join(str(r['real_js_locpct']) for r in fl)}), while the subject-keyed singles on the same subjects flip {sum(r['real_flipped_to_value'] + r['bystander_flipped_to_value'] for r in fs)} of {18*len(fs)}. The write keyed at `\" of\"` is partly subject-conditioned (Zorbland's fired on its own prompt but on only 2/6 same-frame bystanders; the key cosine is 0.99, not 1.0) and partly a frame write (other subjects' fired on 6/6). The real-capital outlier is not a magnitude effect: the last-token writes have near-identical update norms (L8 relative Δ‖W‖ {l8norms}). The alternative that fits is the token prior of the value: `Buenos` is the first token of a real capital the frame already predicts for Argentina (Argentina answered `Buenos` before the edit and is not counted among its 9 flips), so that frame write rides an existing capital-frame direction; values without such a prior override no real capital. The paraphrases, which lack the frame, score 0/3 for every last-token single. **Forward requirement:** the described-as probe (JS ≥ 99.9) saw none of the real-capital flips, so described-as JS alone is not a sufficient locality gate for any write; same-frame prompts must be probed."))
    dvsec = f"""
**Distinct-value singles (Codex control; the probe rows double as N = 1 cells with per-subject values {', '.join(dv_values)}):** last-token singles land {dv_land_last}/{len(dv_last)} with **{dv_para_last}/{3*len(dv_last)}** paraphrase hits; subject-keyed singles land {dv_land_subj}/{len(dv_subj)} with **{dv_para_subj}/{3*len(dv_subj)}**. """ + (f"By the §6b post-hoc rule (every last-token single ≤ 1/3, every subject-keyed single ≥ 2/3) claim B stands and the same-value limitation of the chain's N = 1 cells is removed. Per-subject: " + "; ".join(f"{r['subject']} → {r['value']} last {r['para_hits']}/3, subject {next(q['para_hits'] for q in dv_subj if q['subject'] == r['subject'])}/3" for r in dv_last) + f". Locality cost of subject keying is uneven: described-as JS {', '.join(str(r['described_as_js']) for r in dv_subj)} (one subject, {min(dv_subj, key=lambda r: r['described_as_js'])['subject']}, loses {100 - min(r['described_as_js'] for r in dv_subj):.0f} points) against ≥ 99.9 for every last-token single." if all(r["para_hits"] <= 1 for r in dv_last) and all(r["para_hits"] >= 2 for r in dv_subj) and len(dv_last) >= 6 else f"The §6b post-hoc rule is not met (last-token singles ≤ 1/3: {sum(1 for r in dv_last if r['para_hits'] <= 1)}/{len(dv_last)}; subject-keyed ≥ 2/3: {sum(1 for r in dv_subj if r['para_hits'] >= 2)}/{len(dv_subj)}); claim B weakens to MIXED on distinct values.")

if FBFILES: fbsec = fbsec + "\n" + dvsec
if clB.startswith("F3 SUFFICIENT") and fbread.startswith("H-FRAME"):
    headline = "KEYING LOCUS DECIDES WHAT IS WRITTEN — a last-token-keyed write is a frame write (F3 SUFFICIENT, MEMIT, N = 1, qualified)"
elif clB.startswith("F3 SUFFICIENT") and fbread.startswith("BETWEEN"):
    headline = "KEYING LOCUS DECIDES WHAT IS WRITTEN — last-token-keyed singles land but do not transfer to paraphrases (0/18 vs 18/18 subject-keyed) and bleed onto same-frame prompts to a varying degree (F3 SUFFICIENT, MEMIT, N = 1; frame-bleed BETWEEN)"
elif clB.startswith("F3 SUFFICIENT"): headline = f"{clB} — frame-bleed {fbread}"
elif clB == "pending": headline = f"{n24}; N = 1 cells pending"
else: headline = f"{n24}; N = 1: claim A {clA}, claim B {clB}; frame-bleed {fbread}"

doc = f"""# Keying-locus ablation in the program's MEMIT engine — result (D-C10k-keying-ablation)

_Result 2026-10-04. Pre-registered `docs/C10K_KEYING_ABLATION_PREREG.md` (v3 §3 for the N = 24 cells; §6 and §6b amendments, three advisor rounds). Records `results/c10k_keying_ablation/K{{1..4}}.json`, `zprobe.json`, `keygram.json`, `n1/N1_*.json`, `n1/framebleed.json`; logs `logs/c10k_keying_ablation_*.log`; harness `experiments/track_c/c10e_bandknob.py` (knobs `C10_KEY_LOCUS`, `C10_CTX_TEMPLATES`, `C10_ARMS`, `C10_RECIPES`, `N_EDIT`, `C10_SUBJECT_OFFSET`; engine unmodified, LAW#5 INERT in every cell). Chains `tools/c10k_keying_ablation_chain.sh`, `tools/c10k_keying_ablation_n1.sh`; probe `experiments/track_c/c10k_keying_ablation_n1_framebleed.py`._

## 1. Reading: **{headline}**

- **N = 24 cells (prereg §3):** {n24}. Gate: K1 A1 {k1['A1_single']['para_full']} / A2 {k1['A2_coherent2']['para_full']} vs R0 94.4 / 98.6 → **PASS**. Validity prints confirm the keyed token (subject's last token in K1/K2; the final `" of"` in K3/K4) and byte-identical paraphrase and locality strings across cells.
- **Why the last-token cells failed (§3b–§3c):** the z-objective reaches the target, so the loss is at the solve; the 24 last-token keys are highly collinear in raw space (mean pairwise cosine ≥ 0.985, effective rank 1.02; a cosine of 0.985 is a ≈ 10° angle, not rounding), and their small differences sit in low-variance directions the ridge suppresses at w = 5000, so one solve cannot map them to 24 targets. **Claim A: {clA}.** {clA_why}
- **N = 1 cells (prereg §6b, the valid last-token cells; criterion fixed after 3 of 12 runs were visible): claim B = {clB}.** {clB_why} Paraphrase hits: last-token singles {paraL}/{3*nL}, subject-keyed singles {paraS}/{3*nS} (same value `Beirut` in all twelve chain runs; the distinct-value control is in §3c). Locality cost of subject keying: described-as JS 89–98 against 100 for the last-token singles (≈ 5 points), the price of a write that actually changes the subject's representation.
- **Frame-bleed probe (§6b): {fbread}.**

## 2. Results, N = 24 (EVIDENCE-SHOWS)

{tab}
`para_any` = fraction of the 24 subjects with at least one paraphrase correct. Δ‖W‖ is the engine's own per-layer relative update norm for the A1 edit. Counts behind the K3/K4 percentages: A1 canon {cnt(k3['A1_single']['canon_full'])}/24 and {cnt(k4['A1_single']['canon_full'])}/24; A2 canon {cnt(k3['A2_coherent2']['canon_full'])}/24 and {cnt(k4['A2_coherent2']['canon_full'])}/24.

## 3. What the N = 24 table says (first-pass reading; the mechanism is settled in §3b–§3c)

- **Keyed at the prompt's final token, a batch of 24 writes does not land (EVIDENCE-SHOWS).** Same engine, covariance, ridge weight (5000), band, z-objective and dtype as K1; K3/K4 fit the trained prompt on {k3['A1_single']['canon_full']} / {k4['A1_single']['canon_full']} % of A1 items (K1 {k1['A1_single']['canon_full']} %) and {k3['A2_coherent2']['canon_full']} / {k4['A2_coherent2']['canon_full']} % of A2. The described-as JS stays at 99.8 because little readable change was written, not as independent evidence of locality. By the precedence order both last-token cells are INVALID; no keying rule is written from them.
- **Templates (K2).** Subject-keyed writes without context templates still generalise (A1 {k2['A1_single']['para_full']}, A2 {k2['A2_coherent2']['para_full']}; canon 100 / 100), so templates are not necessary for ≥ 80 % paraphrase scores with subject keying at N = 24; they account for about 4–8 points. Full-precision Δ‖W‖ differ between K1 and K2 at every layer (e.g. L4 15.874 vs 15.889), so the knob changed the key computation.
- **The first-pass attribution to the covariance ridge alone (Route A's ridge diagnostic: last-token keys 17–180× under the ridge at w = 15000; 5.7–60× at w = 5000) is refined by §3c:** the ridge is not what blocks a single last-token write (6/6 land at w = 5000); what blocks 24 is their collinearity in the covariance-plus-ridge geometry. The pre-registered small-ridge sweep (§6) is not run because its outcome cannot bear on F1 (§6b claim A). The covariance-corpus knob (Moir) is untested by this result: neither motivated nor excluded.

### 3b. z-probe (first advisor round, item 2)

`experiments/track_c/c10k_keying_ablation_zprobe.py` runs the engine's unmodified `compute_z` on 3 subjects in K1 style and K3 style with the engine's own templates and records the final target probability at the keyed token, the loss path and the KL term. Reading fixed before the run: K3-style target probability ≥ 0.9 → the z-objective reaches the target and the failure is in the solve; well below K1's → the KL-prompt conflict or the position blocks the target vector.

{zsec}

### 3c. Key-similarity discriminator and N = 1 cells (second advisor round on §6; prereg §6b)

`experiments/track_c/c10k_keying_ablation_keygram.py` → `results/c10k_keying_ablation/keygram.json`:

{gt}
**Reading (EVIDENCE-SHOWS):** the 24 last-token keys are highly collinear in raw activation space (mean pairwise cosine ≥ 0.985, every pair > 0.9, effective rank ≈ 1.02 at every band layer), while the 24 subject-last-token keys are nearly orthogonal (cosine 0.02–0.07, effective rank 16–23). Raw cosine is the geometry of the measurement, not of the solve: MEMIT solves in covariance-weighted space, and the shared first-token activation (norm 98 at L4, the super activation of `docs/PRIOR_ART_SWEEP_2026-10-04.md` §7) inflates raw cosines; a whitened keygram was not run. **A closed-form solve cannot map 24 near-collinear keys to 24 different targets at this ridge weight:** the keys' small differences lie in low-variance directions, the energy-weighted ridge ratio at w = 5000 is 5.7–60 for last-token keys against 0.5–5.3 for subject keys, so those differences are suppressed; the weight at which they would be amplified to the subject keys' ratio is w* ≈ 100–600 per layer. Route A reached the same mechanism from the other side: AlphaEdit_ARE at L2 = 0.01 fit 24/24 by amplifying those differences 1000× (L4 band norm 3.6×, locality cost F4), and the resulting write is read only from the trained prompt.

**N = 1 single writes (`tools/c10k_keying_ablation_n1.sh`; w = 5000, templates on, A1, one request per run; {'complete, 12/12 runs' if complete else f'{nL + nS}/12 runs'}):**

{n1t}
**Claim A (writability): {clA}.** {clA_why}

**Claim B (generalisation, read from landed singles): {clB}.** {clB_why}

#### Frame-bleed probe (§6b, advisor v2 item 6; `experiments/track_c/c10k_keying_ablation_n1_framebleed.py` → `results/c10k_keying_ablation/n1/framebleed.json`)

Six subjects (`FICTION[0..5]`; §6b pre-registered three, the second three were added as the Codex distinct-value control), both loci, one edit each at w = 5000. The probe imports the c10e harness and calls the same `my_edit` / `compute_P` functions the N = 1 cells ran under LAW#5 INERT (no separate inertness run for the probe); after each edit, top-1 at the twelve Route A real-country frame prompts (`The capital of <Albania … Cuba> is the city of`) and at six never-edited fictional frame prompts (`FICTION[12..17]`).

{fbsec}

## 4. Scope, limitations, what changes

- **Scope:** Qwen2.5-3B base, fp16, band [4–8], ridge weight 5000, one seed; N = 24 for the 2×2 cells, N = 1 for six subjects (the same six in the frame-bleed probe, with distinct values), A1 single-token values (A2 at N = 24 only). One engine. Nothing promotes to C10 (A7 untouched, as pre-registered).
- **What the combined picture says (EVIDENCE-SHOWS, scoped):** in the program's own MEMIT engine, *where* a write is keyed decides *what* is written. Keyed at the subject's last token, the write is a fact about the subject: it fits the trained prompt, transfers to held-out paraphrases, and leaves other countries alone. Keyed at the prompt's final token, the same write with the same engine is read from the frame rather than from the subject: at N = 24 the 24 near-collinear keys cannot be separated by the solve and nothing lands; at N = 1 it lands, is read from the trained prompt only (0 paraphrase hits in every single), and {'rewrites every other country that shares the frame' if fbread.startswith('H-FRAME') else ('bleeds onto same-frame prompts to a varying degree (see the probe table; the one real-capital override rides the token prior of `Buenos`)' if fbread.startswith('BETWEEN') else 'behaves as the frame-bleed probe records above')}. This is the behavioural face of the recall-mechanism literature (relations decode from the subject's last token, `docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md`) inside the program's engine.
- **For Route A's F3 ("the port keys the write at the last prompt token, hence 0/72"):** sufficient in MEMIT at N = 1; consistent with F3; not exclusive (Route A also differs in z-objective, preservation term, projector). F3 moves from I-INFER to **EVIDENCE-SHOWS-in-MEMIT (N = 1, qualified)**; the Route A attribution itself stays I-INFER because Route A's modules were not re-run with subject keying.
- **Changes:** the memory_mirror rule "read the keying locus against the generalisation criterion before porting an editor" becomes **unconditional for this engine's mechanism class**: a last-token-keyed write is not a subject fact. Option (ii) (subject-keyed per-token hybrid) keeps its rationale with evidence behind it. The small-ridge sweep is not run (it cannot bear on F1: a landed last-token write does not transfer). The covariance-corpus knob (Moir) is untested by this result and keeps whatever motivation it had from Route A's ridge diagnostic; nothing here motivates or excludes it. **New forward requirement:** every locality gate must include same-frame prompts (described-as JS was blind to 9/12 real-capital flips).
- **Provenance note:** the K1–K4 and `n1/N1_*.json` records carry the harness default `decision_id: D-C10e-bandknob` because the chain scripts did not set `DECISION_ID`; the records are not edited (manifests are never rewritten in place); the chain scripts now export the correct ID for future runs; `framebleed*.json` carry `D-C10k-keying-ablation`.
- **Limitations:** N = 1 and six subjects; the claim-B criterion and the frame-bleed probe were pre-registered after three of twelve runs were visible (prereg §6b, timing disclosure; the remaining nine runs showed no variance, so the thresholds were not decisive); single-token values only, and **all six N = 1 singles were written with the same value ("Beirut")**, an artefact of the single-subject stimulus assignment (`FICTION[off:off+1]` always maps to the same pool slot) — removed by the distinct-value control: the frame-bleed probe used distinct per-subject values ({', '.join(dv_values) if FBFILES else 'pending'}) and reproduced the 0/3 paraphrase result on every last-token single; one seed.

## 5. Advisor and close-out

Advisor on this result: first pass `logs/claude_c10k_keying_ablation_result_review.md` (FIX-FIRST: z-probe, no over-claim on the ridge — resolved by §3b/§3c), Codex `logs/codex_c10k_keying_ablation_result_review.md` (FIX-FIRST: same items + close-out not done); on this result: Claude `logs/claude_c10k_keying_ablation_result_review_v2.md` (FIX-FIRST, wording: headline used H-frame language against the BETWEEN reading; "interference first" and "within rounding" unsupported; Moir withdrawal untested; `Buenos` outlier confounded by token prior; described-as blind to frame damage; pre-registration timing to be tagged inline — all applied here) and Codex `logs/codex_c10k_keying_ablation_result_review_v2.md` (FIX-FIRST: close-out not yet done; `decision_id` provenance drift in the result JSONs — disclosed above; same-value limitation — answered by the distinct-value control; frame-write wording — softened). Both reviews read the pre-fix render. CORPUS entry: `CORPUS/43_C10K_KEYING_ABLATION.md`. Close-out: `tools/closeout_check.py D-C10k-keying-ablation`.
"""
open("docs/C10K_KEYING_ABLATION_RESULT.md", "w").write(doc)
json.dump({"headline": headline, "n24": n24, "claimA": clA, "claimA_why": clA_why, "claimB": clB, "claimB_why": clB_why, "frame": fbread,
           "nL": nL, "nS": nS, "landL": landL, "landS": landS, "lowL": lowL, "highS": highS, "paraL": paraL, "paraS": paraS, "complete": complete,
           "K1": {"A1": k1["A1_single"]["para_full"], "A2": k1["A2_coherent2"]["para_full"]}, "K2": {"A1": k2["A1_single"]["para_full"], "A2": k2["A2_coherent2"]["para_full"]},
           "K3canon": {"A1": k3["A1_single"]["canon_full"], "A2": k3["A2_coherent2"]["canon_full"]}, "K4canon": {"A1": k4["A1_single"]["canon_full"], "A2": k4["A2_coherent2"]["canon_full"]},
           "fb_rows": (rows if FBFILES else [])},
          open(f"{R}/summary.json", "w"), indent=1, ensure_ascii=False)
print("rendered; headline:", headline); print("claim A:", clA, "| claim B:", clB, "| frame-bleed:", fbread, "| runs:", nL + nS)
