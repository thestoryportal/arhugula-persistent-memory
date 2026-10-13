## UPDATE - 2026-10-07 morning (step 2 D-C10t-secondkey CLOSED: NULL-LARGE-WRITE; candidate not advanced; next = step 3 D-C10u-mint2 implementation + reviews)

**State.** Step 2 of the agreed sequence ran under the overnight standing approval (D-C10r-rulings-8) with the pre-run ruling D-C10t-p5rule (§5.2). Its first pass-1 attempt HALTED on a float64 conversion on MPS at a diagnostic readout; one reviewed fix (9e88912, Codex PROCEED) and a fresh rerun (`results/c10t_secondkey_r2`, same selection and requests) gave the binding result **NULL-LARGE-WRITE ⟨D-C10t-secondkey@76a722d3⟩** (CORPUS/53): 23 vs the same-run reference 15/72, +8 below the +10 margin, at a summed write ×2.05, with ten of 24 per-prefix locality gates failing; the duplicate control is null. Candidate not advanced; no replication pending; H-10/H-5 stay open (scoped NOT-ADVANCED note in the register). Verdict review `results/c10t_secondkey_codex_verdict.md` CONFIRMED. Propagated to every tracker (`closeout_check D-C10t-secondkey` ALL GREEN, `--audit` clean, `render_state --check` current); uncommitted at propagation time.

**Sealing (D-C10r-seal) is still parked** on the graft decision: the fresh one-script install-and-probe (`results/c10r_seal_codex_fix1.md` §6–7) needs every graft-enabled attached session closed first. No loop relaunch before the sealing passes review.

**Also on disk:** the Netron structure diagram of Qwen2.5-3B lives in `visualization/` (build script + plain-English README, aa5c8a9; the 1.5 GB .onnx stays local, not committed).

**Next:** step 3 (D-C10u-mint2 v3, `docs/C10U_MINT2_PREREG.md`) — Codex implementation, then the advisor's implementation review (and Codex review), before any run; block F's mint-1(frozen) seed reproduction gate runs first, then F, then V2. Then step 4 (D-C10v-layerpick v2). Candidates only (not designed, not authorized): a fit-guarded stopping rule; a write-size-matched second-key control.

