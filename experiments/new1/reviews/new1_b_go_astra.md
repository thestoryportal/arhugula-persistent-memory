VERDICT: GO-WITH-CONDITIONS

1. **Q1 — Implementation matches Amendment B.** Native normalization, U32/projector identity and native excluded-energy parity remain separate from U64 geometry. Every integer cutoff is evaluated; a layer counts only after passing every cutoff, preventing unions of different three-layer sets. Missing cutoffs become INVALID. See `tools/new1_geometry.py:138–218`, `:418–434`, `:485–496`, `:335–354`. All-nominal-FAIL also becomes BOUNDARY-SENSITIVE, exactly as the frozen “otherwise” rule requires (`docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:210`), although that label alone does not establish actual cutoff sensitivity. The fixtures exercise these distinctions (`tests/test_new1_geometry.py:331–436`). No blocking divergence found.

2. **Q2 — The increases are justified proposals, not mathematically necessary amounts.** The measured 8.06-GiB peak demonstrates that the old 6-GiB cap is unsuitable for the measured implementation. It does not uniquely justify 11 GiB or 2,700 seconds: those incorporate discretionary margins and an unmeasured 600-second allowance (`docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:216–220`). Approval of the variant does not establish approval of these exact spending limits (`SESSION_CHECKPOINT.md:14`).

   **C1 — Before launch, record operator authorization for exactly one attempt capped at 2,700 seconds and 11 GiB, with no automatic retry or cap increase.**

3. **Q3 — Acceptable risk for one explicitly authorized feasibility attempt; no speculative headroom increase first.** The quoted 6.4% is residual headroom *after* a 50% covariance-time margin; likewise 10.07 GiB already includes 25% above the measured peak. Nevertheless, full-workload completion remains UNVERIFIED (`results/mathlab_staging/new1_v2_build_report.md:763–801`).

   **C2 — Explicitly authorize this sole real attempt to serve as complete-workload resource validation, replacing the earlier requirement for validation before execution** (`results/mathlab_staging/new1_b_variant_astra.md:21`). Without that disposition, the earlier prerequisite remains unsatisfied.

   **C3 — Launch through the unchanged supervisor with fresh CPU admission and functioning process-family monitoring; retain every cell reserve, including 19 GiB available for float64 SVD/checks, and nice-10 scheduling.** See `tools/new1_supervisor.py:129–161`, `:189–255`, `:439–445`. Admission refusal ends this dispatch; it is not permission to bypass enforcement.

4. **Q4 — No missing-control or label-laundering blocker found.** All five adapters, both 20-draw control families and applicable M16 diagnostics are retained (`tools/new1_geometry.py:435–495`). BOUNDARY-SENSITIVE survives literally in receipts/findings and uses INVALID transport without a Boolean prediction gate (`tools/new1_supervisor.py:271–289`, `:390–396`). The old launch pin would be refused before numerical work; use the command below (`:66–73`, `:442–444`).

   Correction: time exhaustion returns **STOPPED-DEADLINE**, and exhausted cleanup time can leave **no terminal event** (`:417–424`). Neither partial artifacts nor worker completion alone authorize a prediction verdict. Even successful completion permits only reviewed **MATH-PROXY** reporting; calibration/prospective utility still block queue promotion (`tools/new1_geometry.py:555–560`). I independently confirmed HEAD and the supplied file hashes; the 95-test rerun is orchestrator-provided evidence.

**Endorsed command, only after C1–C3 are satisfied:**

```sh
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a &&
/usr/bin/env PATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin \
  TMPDIR=/private/tmp LLMDB_ROOT="$PWD" \
  LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= \
  OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 \
  "$PWD/.venv/bin/python" -B "$PWD/tools/new1_supervisor.py" \
  --prereg-sha 1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f
```

🌱 graft reported ~74,570 tokens saved (~$0.05), 1 successful call.