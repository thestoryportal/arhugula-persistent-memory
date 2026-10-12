CONFIRM

**Reviewer: GPT-6-Astra (high)**

Valid calibration **FAIL—the designed cheap stop**.

- Admission passed; all three mints admitted. Rehashed **56 file references** successfully; all **73 harvest source hashes** remain unchanged. Harvest→step-2→step-3 bindings match, with prereg SHA `85b389ec92248dbccf61d4ecc1de65f47bedf5ce99f88f17866f0db29d3e4bf8`.
- Step 2: **61/61 gate-2a checks PASS**. Gate 2b remains **OPERANDS-ONLY**, which does not invalidate calibration.
- Counts: A1=68, A2=71, mints=46/37/40, A7=14. Tier margins independently recompute to **22/23**, both ≥10.
- All twelve arm/proxy arrays contain 72 finite values; no **INVALID-ARITHMETIC**. Independent NumPy recomputation from saved values exactly matches scores, orderings and bootstrap counts. No model/torch/GPU execution.

Scores from [calibration.json](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab/m3_20261009T225557.353172Z/calibration.json:5), rounded:

| Arm | Sρ | Scoll |
|---|---:|---:|
| A1 | 0.753970 | −0.049858 |
| A2 | 0.725869 | −0.050704 |
| mint s0 | 0.758199 | −0.051046 |
| mint s1 | 0.733293 | −0.049738 |
| mint s2 | 0.740254 | −0.049699 |
| A7 | 0.758815 | −0.051835 |

Each cell below gives **point ordering ✓/✗; bootstrap count /2000**. Every row must have ✓ and count ≥1900.

| Required ordering | ρ | coll |
|---|---:|---:|
| A1 > s0 | ✗; 742 | ✓; 1403 |
| A1 > s1 | ✓; 1926 | ✗; 890 |
| A1 > s2 | ✓; 1641 | ✗; 1233 |
| A2 > s0 | ✗; 49 | ✓; 1058 |
| A2 > s1 | ✗; 589 | ✗; 579 |
| A2 > s2 | ✗; 221 | ✗; 814 |
| s0 > A7 | ✗; 975 | ✓; 1247 |
| s1 > A7 | ✗; 156 | ✓; 1474 |
| s2 > A7 | ✗; 340 | ✓; 1210 |

Thus **both proxies FAIL**; the “any proxy passes” rule cannot rescue calibration. Terminal events show FAIL after **12.964 s**, consistent with the reported exit 3. The stage-completion PASS does not override terminal calibration FAIL.

**Consequences**

- **Lab stops under §8.** Stop already staged; canonical fold-in remains the lead’s responsibility. An amended proxy requires a written amendment and calibration on unused arms—not rescoring these six. [Frozen rules](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/MATHLAB_PREREG.md:258)
- **Step 4 is SHELVED** by its explicit harvest-2 calibration-PASS prerequisite. [Step-4 prereg](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/MATHLAB_STEP4_PREREG.md:3)
- **MATH-PROXY tooling finding only:** these two frozen proxies fail the registered tier-separation criterion on these arms. No behavioral claim, route closure, F1 conclusion, or statement about other proxies follows.
- **NEW-1 is not falsified or automatically shelved.** It separately pins harvest 1 and has its own descriptive geometry predictions. Its build/execution gates still apply; this review authorizes no launch. Queue use still requires its own calibration and demonstrated prospective utility. [NEW-1 inputs](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:29), [utility boundary](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:135)

🌱 graft saved ~71,464 tokens (~$0.04), 1 successful call.

