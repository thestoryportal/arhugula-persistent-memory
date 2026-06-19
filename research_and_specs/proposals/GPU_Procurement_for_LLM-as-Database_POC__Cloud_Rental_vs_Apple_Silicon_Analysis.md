# GPU procurement recommendation for the LLM-as-Database POC

## 1. Bottom Line Up Front

**Rent, do not buy.** The recommended primary venue is **RunPod Secure Cloud RTX 4090 (24 GB) on-demand at $0.69/hr** with a small persistent Network Volume; the recommended secondary (cost-floor) venue is **Vast.ai on-demand RTX 4090 from a Secure Cloud / Trusted Datacenter host at ~$0.29/hr**. Apple Silicon — despite winning the cost-symmetric comparison on paper — **fails HC-2 categorically**: an exhaustive April 2026 search found zero precedent for MEMIT, ROME, GRACE, or EasyEdit on PyTorch MPS or MLX, and PyTorch MPS has a documented silent-correctness history on the exact `linalg.inv`/`linalg.solve` ops MEMIT depends on. Before procuring, the operator must decide (a) whether to accept Community Cloud / interruptible pricing for ~50% savings against a 3–6 week Stage 2 sweep, and (b) which of RunPod or Vast is preferred on audit posture.

## 2. Candidate field

### 2a. Free-tier (smoke-test only — explicitly disallowed as primary venue)

| Provider | Key spec | April 2026 status | Source |
|---|---|---|---|
| Kaggle Notebooks | P100 16 GB or 2× T4 (32 GB combined); 9-hr session, ~30 hr/wk, 20 GB persistent /working/ | Active; phone verification gates GPU | kaggle.com/docs/efficient-gpu-usage |
| Lightning AI free Studio | L4 24 GB / A10G 24 GB / L40S 48 GB; 4-hr auto-restart; 100 GB persistent | 15 monthly credits (was "80 hr/mo"; that figure is stale) | lightning.ai/pricing |
| Google Colab free + Pro | T4 16 GB; ~15–30 hr/wk free; Pro $9.99/mo ≈ 57 T4-hr | Active; quotas undocumented | research.google.com/colaboratory/faq.html |
| Hugging Face ZeroGPU | H200 slice ~70 GB, per-call burst | Free users **cannot create** ZeroGPU Spaces (PRO-gated); ~3 min/day equivalent | huggingface.co/docs/hub/spaces-zerogpu |
| SageMaker Studio Lab | T4 16 GB; 4 hr/day cap; 15 GB persistent | Active | docs.aws.amazon.com/sagemaker/latest/dg/studio-lab-overview.html |
| Paperspace Gradient free | M4000 8 GB (when available) | Effectively deprecated post-DigitalOcean acquisition; high-end gated to $39/mo | paperspace.com/pricing |

### 2b. Paid cloud GPU rental

| Provider | 24 GB-class option | April 2026 on-demand $/hr | Spot/interruptible $/hr | Source |
|---|---|---|---|---|
| RunPod Community | RTX 4090 24 GB | **$0.34** | n/a (host-preempt) | runpod.io/pricing |
| RunPod Secure | RTX 4090 24 GB | **$0.69** | n/a | runpod.io/pricing |
| RunPod Secure | L4 24 GB | $0.43 | — | runpod.io/pricing |
| RunPod Secure | RTX A5000 24 GB | $0.27–0.36 | — | runpod.io/pricing |
| Vast.ai (marketplace) | RTX 4090 24 GB | **$0.29 floor** | ~$0.15–0.20 | vast.ai/pricing/gpu/RTX-4090 |
| Vast.ai | RTX 3090 24 GB | $0.12 | ~$0.06–0.10 | vast.ai/pricing |
| Lambda Labs | Quadro RTX 6000 24 GB | **$0.69** | none offered | lambda.ai/pricing |
| Lambda Labs | A10 24 GB | $1.29 | none | lambda.ai/pricing |
| CoreWeave | smallest single-GPU = 1× GH200 | $6.50 | n/a | coreweave.com/pricing |
| Together.ai | smallest = HGX H100 | $3.49 | none (cluster product) | together.ai/pricing |
| Modal | L4 24 GB (preemptible base) | $0.80 base / **$2.40 non-preempt (3×)** | preempt is default | modal.com/pricing |
| Modal | A10 24 GB | $1.10 base / $3.30 non-preempt | — | modal.com/pricing |
| DigitalOcean GPU Droplet | RTX 4000 Ada 20 GB | $0.76 | none | digitalocean.com/pricing/gpu-droplets |
| DigitalOcean GPU Droplet | RTX 6000 Ada 48 GB | $1.57 | none | digitalocean.com/pricing/gpu-droplets |
| AWS g6.xlarge | L4 24 GB | $0.8048 | ~$0.30 | aws.amazon.com/ec2/pricing/on-demand/ |
| AWS g5.xlarge | A10G 24 GB | $1.006 | ~$0.30 | instances.vantage.sh/aws/ec2/g5.xlarge |
| GCP g2-standard-4 | L4 24 GB | $0.7068 | ~$0.27 (24-hr cap) | cloud.google.com/compute/gpus-pricing |
| Azure NC24ads A100 v4 | A100 80 GB | $3.673 | **$0.679** | instances.vantage.sh/azure/vm/nc24ads-v4 |

### 2c. Apple Silicon (verified April 25, 2026)

| Model | Chip / unified mem | GPU cores / bandwidth | Price (US) | 12-mo Apple Card 0% | Source |
|---|---|---|---|---|---|
| Mac Studio (base) | M4 Max 14C / 36 GB | 32-core / 410 GB/s | $1,999 | $166.58 | apple.com/shop/buy-mac/mac-studio |
| Mac Studio M4 Max upgraded | M4 Max 16C / 64 GB | 40-core / 546 GB/s | ~$2,499 | ~$208 | apple.com |
| Mac Studio M4 Max upgraded | M4 Max 16C / 128 GB | 40-core / 546 GB/s | ~$3,499 | ~$291.58 | apple.com |
| Mac Studio M3 Ultra (base) | M3 Ultra 28C / 96 GB | 60-core / 819 GB/s | **$3,999** | **$333.25** | apple.com |
| Mac Studio M3 Ultra 128 GB | M3 Ultra | 60-core / 819 GB/s | **currently unavailable on apple.com** (DRAM shortage) | n/a | macrumors.com/2026/03/05/... |
| Mac Studio M3 Ultra 256 GB | M3 Ultra | 60-core / 819 GB/s | $5,999 | $499.92 | apple.com |
| MacBook Pro 16″ M5 Pro | M5 Pro / 24 GB base, 64 GB max | 20-core / 307 GB/s | from $2,699 | from $224.92 | apple.com/newsroom/2026/03/... |
| MacBook Pro 16″ M5 Max | M5 Max / 36 GB base | 32-core / 460 GB/s | $3,899 | $324.92 | apple.com |
| MacBook Pro 16″ M5 Max 64 GB | M5 Max 18C / 40-GPU / 64 GB | 40-core / 614 GB/s | ~$4,599 (2 TB) | ~$383.25 | appleinsider.com |
| MacBook Pro 16″ M5 Max 128 GB | M5 Max 40-GPU / 128 GB | 40-core / 614 GB/s | ~$5,599 (2 TB Std) | ~$466.58 | apple.com / Gizmodo review |
| MacBook Pro 16″ M4 Max 128 GB | M4 Max / 128 GB | 40-core / 546 GB/s | discontinued at Apple; ~$4,526 reseller | n/a (Apple Card requires Apple direct) | amazon listing |

**Critical Apple findings the operator must absorb up front.** First, **Apple Card Monthly Installments on Macs is 12 months only, not 24** (apple.com/apple-card/monthly-installments; support.apple.com/en-us/102730). The 24-month figure in the brief is wrong for Macs — it applies to iPhone. Second, **the 128 GB Mac Studio M3 Ultra is currently unorderable on apple.com** as of mid-April 2026 due to a global DRAM shortage; only 96 GB and (a $2,000 upgrade above 96) 256 GB are listable. Third, **the 16″ MacBook Pro M4 Max is discontinued at Apple direct** (replaced by M5 Max on March 11, 2026); only resellers carry it, and reseller purchases cannot use Apple Card 0% installments.

## 3. Per-candidate evaluation

### Free-tier — Kaggle Notebooks (smoke-test candidate)
- **HC-1 Memory:** PASS for GPT-J 6B FP16 (P100 16 GB or 2× T4 32 GB); MARGINAL for LLaMA 3.1 8B FP16 + 1.5× headroom (kaggle.com/docs/efficient-gpu-usage).
- **HC-2 Toolchain:** PASS — CUDA T4/P100, MEMIT runs unmodified.
- **HC-3 Persistence:** PARTIAL — 20 GB /working/ persists between sessions on the same notebook; not durable across notebooks.
- **HC-4 Tenant isolation:** FAIL for production — shared, public-by-default notebooks; private notebooks share the same quota.
- **HC-5 Reproducibility:** PASS for smoke test (pin `pip install` cell, deterministic seed).
- **OC-1 Cost:** $0; **OC-2 Wall-clock:** 9-hr session limit; **OC-4 Latency:** P100/T4 marginal for ≤800 ms p95 on 8B; **OC-5 Egress:** n/a.
- **Verdict: ADMIT as smoke-test only.**

### Free-tier — Lightning AI free Studio (backup smoke-test)
- **HC-1:** PASS (L4/A10G 24 GB).
- **HC-2:** PASS (CUDA).
- **HC-3:** PASS — 100 GB persistent, Studio environment survives between sessions.
- **HC-4:** PASS (private Studios by default).
- **HC-5:** PASS.
- 15-credit/month cap is the binding constraint. **Verdict: ADMIT as smoke-test backup.**

### Free-tier — Hugging Face ZeroGPU
- **HC-1:** PASS (H200 slice). **HC-3:** FAIL (ephemeral per-call only). **HC-4:** FAIL (PRO required to create Spaces, public by default). Architecturally wrong. **REJECT.**

### Free-tier — Colab free / SageMaker Studio Lab
- 16 GB T4 only, undocumented quotas, public-by-default ToS posture. Tertiary fallback only. **REJECT for primary; admit as last-resort smoke-test.**

### Paid cloud — RunPod Secure Cloud RTX 4090 (24 GB)
- **HC-1:** PASS (24 GB clears LLaMA 3.1 8B FP16 + 1.5× MEMIT headroom).
- **HC-2:** PASS (CUDA, recent driver).
- **HC-3:** PASS — Network Volume $0.05–0.07/GB/mo persists independent of pod (runpod.io/pricing).
- **HC-4:** PASS — RunPod-managed datacenter, SOC 2 alignment, isolated containers; ToS includes no model-output-logging or workload-introspection language; RunPod blog explicitly states "we do not inspect your pod data or transmissions, nor do we allow our hosts to do so" (runpod.io/blog/anonai-private-chatbot-scaling-runpod). Not bare-metal; isolated container is the boundary.
- **HC-5:** PASS — pinned PyTorch container images, deterministic decoding supported.
- **OC-1 Cost:** $0.69/hr × 1,000 hr = **$690 low**; × 2,400 hr = **$1,656 high**; 250-hr/mo burn = **$172.50** (✅ under $250).
- **OC-2 Wall-clock:** PASS — Secure Cloud is not preemptible.
- **OC-4 Latency:** PASS (RTX 4090 well above mid-tier).
- **OC-5 Egress:** PASS — free egress, free ingress (runpod.io/pricing).
- **Verdict: ADMIT — primary recommendation.**

### Paid cloud — RunPod Community Cloud RTX 4090
Identical to Secure on HC-1/HC-2/HC-5 but **HC-3 weaker** (Network Volume not supported on Community per the runpod.io RTX 4090 page) and **HC-4 weaker** (third-party host, privacy-by-policy not architecture). **OC-2 FAIL** for the 3–6 week Stage 2 sweep — Community pods can be preempted without warning when the host reclaims; container disk lost on preempt. $0.34/hr × 2,400 hr = $816 high; 250-hr/mo = $85. **Verdict: REJECT for Stage 2; admissible only for Stage 1 pre-flight after smoke testing succeeds, with aggressive checkpointing.**

### Paid cloud — Vast.ai on-demand RTX 4090 (Secure Cloud filter)
- **HC-1:** PASS. **HC-2:** PASS (CUDA). **HC-3:** PASS — persistent disk per-host; storage billed continuously even when stopped (docs.vast.ai/documentation/instances/pricing). **HC-4:** PARTIAL — marketplace; SOC 2 Type II covers the platform (vast.ai/article/vast-soc2-typeII-certification) but not individual hosts; Secure Cloud filter restricts to vetted DC partners (vast.ai/article/security-and-compliance-at-vast-ai). ToS contains no workload-introspection clause. **HC-5:** PASS.
- **OC-1:** $0.29/hr × 1,000 hr = **$290 low**; × 2,400 hr = **$696 high**; 250-hr/mo = **$72.50** (✅ best in class). Interruptible tier ~50% lower.
- **OC-2:** PASS on on-demand from a high-reliability host; FAIL on interruptible.
- **OC-4:** PASS. **OC-5:** **FLAG** — bandwidth is per-host priced and the most opaque cost in the survey.
- **Verdict: ADMIT — secondary (cost-floor) recommendation, conditional on reliability ≥ 0.95 and Secure Cloud filter.**

### Paid cloud — Lambda Labs Quadro RTX 6000 24 GB
- HC-1/HC-2/HC-5 PASS; **HC-4 PASS strongest of the survey** ("No Virtualization. No Shared GPUs", dedicated hardware, processor-only data terms — lambda.ai/legal/terms-of-service); **HC-3 PARTIAL** (Lambda Cloud Filesystem $0.20/GB/mo, not on current price page).
- **OC-1:** $0.69/hr × 1,000 hr = $690 / × 2,400 hr = $1,656; 250-hr/mo = $172.50 (✅).
- **OC-2:** PASS (no spot tier exists — Lambda is on-demand only).
- **Capacity for the cheapest 24 GB SKU is reportedly tight.** A10/A6000/A100 SKUs all blow the budget.
- **Verdict: ADMIT — tertiary, on availability.**

### Paid cloud — GCP g2-standard-4 (L4 24 GB)
- HC-1/HC-2/HC-3/HC-5 PASS; HC-4 PASS (multi-tenant by default, Cloud DPA processor-only).
- **OC-1:** $0.7068/hr × 1,000 = $707 / × 2,400 = $1,696; 250-hr/mo = **$176.70 ✅**.
- **OC-5 RISK:** Premium-tier egress $0.12/GB, Standard $0.085/GB, with **doubling of peering/CDN-Interconnect rates effective May 1, 2026** (cloud.google.com/vpc/network-pricing). Pull-to-disk of edited checkpoints could materially shift total cost.
- **Verdict: ADMIT — viable hyperscaler tertiary; flagged on OC-5.**

### Paid cloud — AWS g6.xlarge (L4 24 GB)
- All HC PASS. **OC-1:** $0.8048/hr × 1,000 = $804.80 / × 2,400 = $1,931.50; 250-hr/mo = **$201.20 ✅** (margin of ~$50 vs ceiling). **OC-5 RISK:** $0.09/GB egress + NAT gateway $0.045/GB + $0.045/hr if used. **Verdict: ADMIT with OC-5 caveat.**

### Paid cloud — Azure NC24ads A100 v4 (spot only)
- HC PASS. **OC-1 spot:** $0.679/hr × 1,000 = $679 / × 2,400 = $1,630; 250-hr/mo = **$170 ✅**. **OC-2 FAIL** for Stage 2 sweep — 30-second eviction notice, harder than AWS spot's 2 min. On-demand $3.673/hr fails ceiling. **Verdict: ADMIT only as cost-floor with checkpointing; reject for the 3–6 week sweep.**

### Paid cloud — DigitalOcean GPU Droplet RTX 4000 Ada (20 GB)
- **HC-1 BORDERLINE** — 20 GB is below the 24 GB target; tight for LLaMA 3.1 8B FP16 + 1.5× MEMIT headroom; would require 8-bit weights or aggressive paging. Other HC PASS. **OC-1:** $0.76/hr × 250 hr/mo = $190 ✅. **OC-5 strong** — 10–15 TB bundled egress, $0.01/GiB overage. **Verdict: REJECT on HC-1 marginal; would need to step up to RTX 6000 Ada 48 GB at $1.57/hr → $393/mo, which fails OC-1.**

### Paid cloud — Modal (serverless)
- HC-1 PASS on L4 24 GB, but **OC-2 FAIL** at base preemptible rate; non-preemptible mode is **3× base** ($2.40/hr L4 → $600/mo), failing OC-1. Team plan adds $250/mo platform fee that alone consumes the budget. **Verdict: REJECT.**

### Paid cloud — Together.ai
- **HC-1 N/A** at the relevant tier — no 24 GB-class SKU; smallest is HGX H100. **OC-1 FAIL** ($3.49/hr → $873/mo). **Verdict: REJECT.**

### Paid cloud — CoreWeave
- Strongest audit posture in the survey (single-tenant DPU node isolation; explicit "No Assessment of Customer Data" in ToS — docs.coreweave.com/policies/terms-of-service). **OC-1 FAIL** — smallest single-GPU is 1× GH200 at $6.50/hr ($1,625/mo at 250 hr); inference-platform single-GPU rates require sales engagement and the cheapest L40 still pushes $312/mo. **Verdict: REJECT on cost.**

### Paid cloud — AWS p4d/p5, GCP a2/a3, Azure NC A100/H100 on-demand
$3.67–$98/hr → $918–$24,580/mo at 250 hr. **REJECT — categorically over budget.**

### Apple Silicon — Mac Studio M3 Ultra 96 GB ($3,999)
- **HC-1:** PASS (96 GB unified, 819 GB/s).
- **HC-2: FAIL.** Lead constraint. Exhaustive April 2026 search of kmeng01/memit, kmeng01/rome, zjunlp/EasyEdit (including the April 2025 EasyEdit2 release), scalable-model-editing/unified-model-editing, ml-explore/mlx, and ml-explore/mlx-examples returned **zero precedent** for MEMIT/ROME/GRACE/EasyEdit on PyTorch MPS or MLX. The MEMIT reference notebook hardcodes `if not torch.cuda.is_available(): raise Exception(...)` (github.com/kmeng01/memit/blob/main/notebooks/memit.ipynb); none of the 22 open issues mention MPS/MLX/Mac/Apple/Metal. EasyEdit issue #33 documents the maintainers explicitly route through CUDA `device_map='auto'`. mlx-examples lists ~20 example projects (LLaMA, Mixtral, LoRA, Whisper, Stable Diffusion) but **no model-editing example** of any kind.
- **HC-3:** PASS (local NVMe). **HC-4:** PASS (single-user, single-tenant).
- **HC-5:** RISK — PyTorch MPS has documented FP precision differences vs CUDA; "even with identical seeds the numerical path will diverge immediately" (tunguz.github.io/PyTorch_Hardware_2025/).
- **AS-1 Port effort:** **1–2 weeks for limp-along port; 4–8+ weeks for a port the researcher would trust for paper-quality results; 8–16+ weeks for native MLX rewrite** (no `nethook` equivalent in MLX, no editing example precedent). PyTorch issues confirm the dependency chain is fragile: `torch.linalg.solve` on MPS only landed Feb 2025 (PR #146531), `torch.linalg.inv` had a silent batch-correctness regression on MPS (#78363), `_linalg_solve_ex` still routes through CPU fallback (#148547), and `torch.linalg.lstsq` is still unimplemented on MPS (#118362).
- **AS-2 Numerical-precision risk: HIGH.** MEMIT's covariance precomputation stores FP32 second-moment matrices over 100,000 Wikipedia samples and solves a normal-equation system. The exact ops in this hot path have a documented MPS history of silent correctness issues. MPS lacks FP64 entirely (#78168), so cross-validation against a CUDA double-precision baseline cannot be done on-device.
- **AS-3 TCO:** $3,999 upfront vs $1,656 high-end cloud — Mac wins on absolute dollars *if it works*, and retains ~55–65% at 2 years, leaving net cost ~$1,400–$1,800. **HC-2 fails this candidate before AS-3 matters.**
- **Verdict: REJECT on HC-2.**

### Apple Silicon — MacBook Pro 16″ M5 Max 64 GB (~$4,599 / $383.25/mo on 12-mo Apple Card)
- HC-1 PASS, HC-2 FAIL (same evidence). HC-5 same risk. AS-1 effort identical. **Verdict: REJECT on HC-2.**

### Apple Silicon — MacBook Pro 16″ M5 Max 128 GB (~$5,599 / $466.58/mo)
- 12-month installment **exceeds the $250/mo opex ceiling** even before the HC-2 toolchain failure. **REJECT on OC-1 and HC-2.**

### Apple Silicon — Mac Studio M4 Max 64 GB (~$2,499 / $208/mo)
- This is the only Apple SKU whose 12-month installment fits under the $250/mo ceiling. **HC-2 FAIL** identical to above. **REJECT on HC-2.**

## 4. Comparison matrix

| Candidate | HC-1 | HC-2 | HC-3 | HC-4 | HC-5 | OC-1 | OC-2 | OC-4 | OC-5 | Total POC low (1k hr) | Total POC high (2.4k hr) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **RunPod Secure RTX 4090** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ ($172.50/mo) | ✅ | ✅ | ✅ free egress | $690 | $1,656 | **ADMIT — primary** |
| **Vast.ai on-demand RTX 4090 (Secure DC)** | ✅ | ✅ | ✅ | ⚠ marketplace | ✅ | ✅ ($72.50/mo) | ✅ on-demand | ✅ | ⚠ per-host bw opaque | $290 | $696 | **ADMIT — secondary** |
| RunPod Community RTX 4090 | ✅ | ✅ | ⚠ no Network Volume | ⚠ | ✅ | ✅ ($85/mo) | ❌ host-preempt | ✅ | ✅ | $340 | $816 | ADMIT for Stage 1 only |
| Lambda Quadro RTX 6000 24 GB | ✅ | ✅ | ⚠ filesystem unposted | ✅ best | ✅ | ✅ ($172.50/mo) | ✅ | ✅ | ✅ | $690 | $1,656 | ADMIT — tertiary on availability |
| GCP g2-standard-4 L4 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ ($176.70/mo) | ✅ | ✅ | ❌ $0.085–0.12/GB egress | $707 | $1,696 | ADMIT with egress flag |
| AWS g6.xlarge L4 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ ($201.20/mo, narrow) | ✅ | ✅ | ❌ $0.09/GB + NAT | $805 | $1,932 | ADMIT with egress flag |
| Azure NC24ads A100 v4 spot | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ ($170/mo) | ❌ 30-sec evict | ✅ | ❌ $0.087/GB | $679 | $1,630 | ADMIT cost-floor only |
| Modal L4 (preempt base) | ✅ | ✅ | ⚠ | ✅ | ✅ | ✅ ($200/mo base) | ❌ 3× non-preempt | ✅ | ⚠ | $800 | $1,920 | REJECT for Stage 2 |
| DigitalOcean RTX 4000 Ada | ⚠ 20 GB borderline | ✅ | ✅ | ✅ | ✅ | ✅ ($190/mo) | ✅ | ✅ | ✅ generous bundle | $760 | $1,824 | REJECT on HC-1 marginal |
| CoreWeave (any single-GPU) | ✅ | ✅ | ✅ | ✅ best | ✅ | ❌ ($1,625/mo+) | ✅ | ✅ | ✅ free | $6,500 | $15,600 | REJECT on cost |
| Together.ai HGX H100 | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ ($873/mo) | ✅ | ✅ | ✅ free | $3,490 | $8,376 | REJECT on cost |
| AWS/GCP/Azure A100/H100 on-demand | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ ($918–$24k/mo) | ✅ | ✅ | ❌ | $3,673+ | $8,815+ | REJECT on cost |
| **Mac Studio M3 Ultra 96 GB** | ✅ | **❌ no MEMIT precedent on MPS/MLX** | ✅ | ✅ | ⚠ FP precision risk | ⚠ $333.25/mo (12-mo) | ✅ | ✅ | ✅ | $3,999 capex | $3,999 capex | **REJECT on HC-2** |
| Mac Studio M4 Max 64 GB | ✅ | ❌ same | ✅ | ✅ | ⚠ | ✅ $208/mo | ✅ | ✅ | ✅ | $2,499 | $2,499 | REJECT on HC-2 |
| MacBook Pro 16″ M5 Max 64 GB | ✅ | ❌ same | ✅ | ✅ | ⚠ | ⚠ $383/mo | ✅ | ✅ | ✅ | ~$4,599 | ~$4,599 | REJECT on HC-2 + OC-1 |
| MacBook Pro 16″ M5 Max 128 GB | ✅ | ❌ same | ✅ | ✅ | ⚠ | ❌ $466/mo | ✅ | ✅ | ✅ | ~$5,599 | ~$5,599 | REJECT on HC-2 + OC-1 |

## 5. Cost-symmetric comparison: cloud rental vs financed Apple Silicon

The operator's framing — "$200–250/mo cloud OR finance a top MacBook Pro" — is **superficially decisive in Apple's favor** and **categorically decided against Apple by HC-2.**

### Side-by-side at the operator's monthly ceiling

| Envelope | Cloud burn | Apple equivalent (12-mo Apple Card 0% APR) | Net to operator after POC |
|---|---|---|---|
| 12 mo × $250/mo = **$3,000** | RunPod Secure RTX 4090 = $1,656 high; **net under-spend $1,344** | Mac Studio M3 Ultra 96 GB at **$333/mo × 12** = $3,999 (over by $999/yr); or Mac Studio M4 Max 64 GB at **$208/mo × 12** = $2,499 ✅ | Cloud: $0 asset. Mac: ~$1,400–$2,600 at 2-yr resale. |
| 18 mo × $250/mo = **$4,500** | RunPod $1,656 + ~$80 storage; **net under-spend $2,764** | M3 Ultra 96 GB cleared in 12 mo + 6 mo of post-POC operation | Same |
| 24 mo × $250/mo = **$6,000** | Same cloud project ends at $1,656; balance is opportunity cost | Mac Studio M3 Ultra 96 GB ($3,999) + AppleCare+ ($400) + 6 mo cushion | Same |

**Naïve verdict: Mac Studio M3 Ultra 96 GB at $3,999 ($333.25/mo on 12-mo Apple Card) beats every cloud envelope ≥18 months on raw dollars and leaves a depreciable asset.** The MacBook Pro 16″ M5 Max 64 GB at ~$4,599 ($383/mo) and 128 GB at ~$5,599 ($467/mo) **exceed the $250/mo opex ceiling on 12-month financing** — if the operator wants a MacBook Pro at $250/mo, the only candidate that fits is the M5 Pro 16″ at $2,699 / $224.92/mo (48 GB max), which barely clears the LLaMA 3.1 8B + 1.5× headroom on unified memory but has weaker GPU bandwidth.

**The HC-2 verdict overrides all of this.** No precedent for MEMIT, ROME, GRACE, or EasyEdit exists on PyTorch MPS or MLX as of April 25, 2026. The MEMIT reference notebook **explicitly raises** when CUDA is absent. Of the four required linear-algebra ops on the MEMIT critical path — `linalg.solve`, `linalg.inv`, `_linalg_solve_ex`, `linalg.lstsq` — only `solve` is recently and natively implemented on MPS (PR #146531, Feb 2025); the others either silently mis-compute (`inv`, GitHub #78363) or route through CPU fallback (#148547, #118362). Even at the most optimistic estimate (1–2 weeks for a limp-along port) the operator burns 10–20% of the wall-clock envelope on toolchain debugging *before producing a single edit*, with no validation harness to confirm the numbers match published CUDA reference.

**Decision axis:** the dollar advantage of buying a Mac is real (~$1,400–$2,400 net over 2 years vs cloud), but it is conditional on the toolchain working. Since the toolchain has zero precedent and meaningful silent-correctness risk, the cloud-rental envelope is the only path that produces scientifically defensible MEMIT results within the 7–22 week window. **Recommended: rent.**

## 6. Short-list

**Primary (recommended):** **RunPod Secure Cloud RTX 4090 (24 GB) on-demand at $0.69/hr** with a 100–200 GB Network Volume at $0.07/GB/mo. This is the only candidate that simultaneously clears all five hard constraints, fits comfortably under $250/mo at the 250-hr/month pace ($172.50/mo + ~$10–14 storage), supports a 3–6 week uninterrupted Stage 2 sweep, has free egress, has a managed-DC tenant-isolation posture with a documented no-introspection policy, and has per-second billing so partial hours do not round up. Total POC cost: **$690 low / $1,656 high**, well inside any of the cost-symmetric envelopes.

**Secondary (cost-floor):** **Vast.ai on-demand RTX 4090 from a Secure Cloud / Trusted Datacenter host with reliability ≥ 0.95.** Halves the primary's cost ($290 low / $696 high) at the price of marketplace audit posture and per-host bandwidth opacity. Recommended if the operator confirms the workload is checkpoint-resumable and accepts a Secure Cloud filter on hosts. Treat the Vast.ai marketplace as the "we know enough about MEMIT now to accept some operational fiddling for ~60% savings" tier.

**Tertiary backup:** **Lambda Labs Quadro RTX 6000 24 GB on-demand at $0.69/hr**, used if RunPod RTX 4090 capacity is unavailable. Lambda's audit posture is the strongest in the survey ("No Virtualization. No Shared GPUs"), but capacity for the cheapest 24 GB SKU is reportedly tight, and the absence of any spot tier eliminates a savings lever.

**Free-tier pre-flight smoke test:** **Kaggle Notebooks (P100 16 GB or 2× T4 32 GB).** Use it to load GPT-J 6B, run a single MEMIT covariance-precomputation step on one MLP layer, and run one edit-and-evaluate cycle to confirm the environment stack works before committing a payment method to the paid provider. Kaggle's 9-hour session limit, ~30 hr/week quota, 20 GB persistent /working/, and background execution are the most predictable free envelope. Lightning AI free Studio (24 GB L4) is the backup if Kaggle phone verification fails.

## 7. Open questions for operator

1. **Spot vs on-demand on the Stage 2 sweep.**
   (a) Decide whether to run Stage 2 (3–6 weeks continuous) on RunPod Secure on-demand ($0.69/hr, no preemption) or on a cheaper interruptible tier (Vast.ai interruptible ~$0.15/hr; AWS g5 spot ~$0.30/hr; Azure NC24ads A100 spot $0.679/hr).
   (b) This decision affects total POC cost by a factor of ~2–3× and determines how robust the checkpoint-resume harness must be.
   (c) **Default if undecided: run Stage 2 on RunPod Secure on-demand RTX 4090** — eliminates the failure mode of a 3-day sweep losing the last hour to preemption.

2. **Audit posture preference between RunPod and Vast.**
   (a) Decide whether the workload's audit posture requirement is satisfied by RunPod's "managed datacenter, isolated container, no-introspection ToS" or whether it must reach Vast's marketplace tier (with the SOC 2 platform certificate but third-party hosts).
   (b) This decision affects which becomes primary and which becomes secondary; it does not affect total cost meaningfully at the 24 GB tier.
   (c) **Default if undecided: RunPod Secure as primary**, since the architectural isolation is stronger than marketplace privacy-by-policy.

3. **Persistent storage size and pull-to-disk cadence.**
   (a) Decide a target size for the Network Volume (50 / 100 / 200 GB) and the cadence for pulling covariance caches and edited checkpoints to local disk.
   (b) This affects monthly storage spend ($3.50 / $7 / $14) and bandwidth usage; on free-egress providers (RunPod, Vast, Lambda, CoreWeave, Together) this has zero OC-5 impact, but on AWS/GCP/Azure egress charges accumulate fast.
   (c) **Default if undecided: 100 GB Network Volume on RunPod (~$7/mo) with weekly rsync to local Mac.**

4. **Free-tier smoke-test commitment before paid provider activation.**
   (a) Decide whether to run a 1–3 day Kaggle smoke test of the full MEMIT-on-GPT-J-6B environment before swiping a card.
   (b) Affects exposure to "the toolchain is broken on this provider's container image" failure mode; near-zero downside on operator time.
   (c) **Default if undecided: yes, run the smoke test on Kaggle first.**

5. **Apple Silicon decision freeze.**
   (a) Decide whether the Apple Silicon path is fully off the table for the POC, or kept as a "watch-and-revisit if community port emerges" item.
   (b) Affects whether the operator monitors kmeng01/memit and zjunlp/EasyEdit issues for MPS/MLX activity over the 7–22 week POC window.
   (c) **Default if undecided: Apple Silicon is rejected for the POC; revisit only post-POC under Section 8.**

6. **Local pull-to-disk machine.**
   (a) Decide whether the existing 2020 Intel 16 GB MacBook Pro is sufficient as the local-primary archive endpoint, or whether a small drive upgrade / external SSD is needed.
   (b) Affects whether the local-primary persistence requirement (HC-3) is fully met. The 2020 MBP cannot run any candidate locally but is fine as an rsync target.
   (c) **Default if undecided: keep current MBP as rsync target; budget ~$100 for a 1 TB external SSD if covariance caches grow beyond the local SSD.**

## 8. Apple Silicon long-term note

Apple Silicon should be reconsidered post-POC under the following conditions, in increasing order of significance: **(a)** at least one published, citable run of MEMIT or EasyEdit on PyTorch MPS that validates edit-success, specificity, and locality metrics within tolerance of the original CUDA reference numbers — this would close the "no precedent" verdict; **(b)** a community PR merged into kmeng01/memit, kmeng01/rome, or zjunlp/EasyEdit that adds an explicit MPS device path, with passing tests; **(c)** an MLX-native model-editing example in ml-explore/mlx-examples or mlx-community that ports the locate-and-edit objective to MLX primitives, demonstrating that the `nethook`-equivalent layer-interception and MLP weight-rewriting patterns translate; **(d)** PyTorch resolves the open silent-correctness history on `linalg.inv` (#78363) and lands a native (non-CPU-fallback) implementation of `_linalg_solve_ex` on MPS (#148547).

For the **v2 use cases** the operator named — ongoing harness operation, agent execution against already-edited models, software development, judge inference — Apple Silicon is **already viable today**: standard inference of LLaMA 3.1 8B and GPT-J 6B on PyTorch MPS or MLX-LM is a well-trodden path, and the M3 Ultra's 819 GB/s memory bandwidth and 96 GB unified memory comfortably handle multi-model serving. The HC-2 failure is **specific to research-grade model editing**, not to the harness's steady-state operation. A reasonable medium-term plan: rent during the POC, then evaluate buying a Mac Studio for ongoing operation once the edited weights are in hand and the workload shifts from "rewrite MLP weights via numerically delicate covariance solves" to "run the agent harness against fixed edited models."

## 9. Session summary block

**Decisions made:** Recommended primary procurement venue is RunPod Secure Cloud RTX 4090 (24 GB) on-demand at $0.69/hr with a Network Volume; recommended secondary is Vast.ai on-demand RTX 4090 from a Secure DC host. Apple Silicon rejected for the POC on HC-2 (no MEMIT/ROME/GRACE/EasyEdit precedent on PyTorch MPS or MLX as of April 25, 2026). Free-tier pre-flight smoke test on Kaggle Notebooks before activating any paid provider.

**Constraints established:** Total POC cost ceiling implied by operator framing is $3,000 / $4,500 / $6,000 over 12 / 18 / 24 months at $250/mo. Recommended primary fits inside the 12-month envelope at $1,656 high-end. RunPod Network Volume cost confirmed at $0.05–0.07/GB/mo; egress is free. Apple Card Monthly Installments on Macs is **12 months only, not 24** — the brief's 24-month assumption is invalid for Macs. The 128 GB Mac Studio M3 Ultra is **currently unorderable on apple.com** due to DRAM shortage. The 16″ MacBook Pro M4 Max is **discontinued at Apple direct** as of March 11, 2026 (replaced by M5 Max).

**Open questions deferred:** Spot vs on-demand on Stage 2 sweep; audit-posture preference between RunPod and Vast; Network Volume sizing and pull-to-disk cadence; whether to run a free-tier smoke test before card activation; Apple Silicon watch-list status; local rsync target adequacy.

**Interface contracts defined:** Persistent state lives on a RunPod Network Volume in the same region as the GPU pod (architecture profile hash anchor, .vindex overlays equivalent, edited model checkpoints, covariance caches, drift sweeps, judge calibration data). Local-primary mirror on the 2020 Intel MBP via rsync; provider-side persistence on the Network Volume. Pinned PyTorch container image for HC-5 reproducibility. Free-tier smoke test executes one MEMIT edit on GPT-J 6B with deterministic seed and validates against the published CounterFact reference number on a single fact before any paid provider is activated.

**Next session candidates:** (1) Procurement execution session — operator decides Open Questions 1–6 and activates RunPod with a small storage volume and a smoke-test pod. (2) Toolchain validation session — run the MEMIT smoke test on Kaggle, confirm GPT-J 6B FP16 + MEMIT covariance precomputation succeeds end-to-end, and capture the reference edit-success number. (3) Stage 1 kickoff — load LLaMA 3.1 8B FP16 on the chosen RTX 4090 and reproduce one published CounterFact edit before launching the Stage 2 sweep.