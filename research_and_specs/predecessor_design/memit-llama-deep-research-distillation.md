---

# Source: Gemini
Date run: 2026-04-29
Candidate caches found:

  ## Candidate 1:
    URL: [https://github.com/Ymm-cll/UniErase/blob/main/data/P_loc/Llama-3.1-8B-Instruct_multi.pt](https://github.com/Ymm-cll/UniErase/blob/main/data/P_loc/Llama-3.1-8B-Instruct_multi.pt) [7]
    Source organization / paper / author: Ymm-cll / UniErase framework 
    Exact base model: meta-llama/Llama-3.1-8B-Instruct (Fails base model criterion) [7]
    Layer indices: Superset (Standard configurations inherently cover 4-8)
    mom2_dataset: wikipedia [7]
    mom2_n_samples: 100000 [7]
    mom2_dtype: float32
    File format:.pt [7]
    Total size: ~4.1 GB (Estimated cumulative)
    Provenance strength: MODERATE

  ## Candidate 2:
    URL: [https://github.com/xpq-tech/PMET](https://github.com/xpq-tech/PMET) [8]
    Source organization / paper / author: Li et al. (PMET / CoME frameworks) [8]
    Exact base model: meta-llama/Llama-3.1-8B [8]
    Layer indices: [1, 2, 3, 4, 5][8]
    mom2_dataset: WikiText (Fails wikipedia criterion) [8]
    mom2_n_samples: 10000 (Fails 100,000 criterion) [8]
    mom2_dtype: float32 [8]
    File format: Unspecified (.npz or.pt typically)
    Total size: ~4.1 GB (Estimated cumulative)
    Provenance strength: STRONG

## Confidence: High (High confidence that a perfect match does not currently exist publicly, based on exhaustive scanning of the ecosystem).

## Anything else worth flagging: 
- No public artifact perfectly matches all five criteria. The major hurdle is that 100,000-sample Wikipedia caches are now almost exclusively generated for Instruct models rather than Base models, or they use much smaller sample sizes due to out-of-memory bottlenecks. 
- **High-Value Lead for Base Model Stats:** A recent paper currently under review at ICLR 2026, "Quantifying Edits Decay in Fine-tuned LLMs" by Cheng et al., explicitly notes generating MEMIT covariance statistics for the exact `meta-llama/Llama-3.1-8B` base model using `mom2_n_samples: 100000`, a `float32` data type, and the `wikipedia` dataset for layers `[6, 1, 2, 3, 4]`. The authors state their code is available in a repository to foster reproducibility, meaning these exact cache files may be released shortly or could be acquired by reaching out to the authors directly.

---

# MEMIT Covariance Cache Search — Summary

**Source:** Claude Deep Research
**Date run:** 2026-04-29

## Candidate caches found:

### Candidate 1:
- **URL:** https://drive.google.com/file/d/1GhDb4vPd1NIyRCbbIlgXV45xbE2UQMav/view
- **Source organization / paper / author:** jianghoucheng / AlphaEdit (Fang et al., ICLR 2025 Outstanding Paper) — https://github.com/jianghoucheng/AlphaEdit
- **Exact base model:** meta-llama/Meta-Llama-3-8B-**Instruct** (NOT Llama-3.1, and Instruct variant)
- **Layer indices:** [4, 5, 6, 7, 8]
- **mom2_dataset:** wikipedia
- **mom2_n_samples:** 100000
- **mom2_dtype:** float32
- **File format:** archive of per-layer tensors (Google Drive download, decompressed to `./data/stats/`)
- **Total size:** ~4 GB estimated (~822 MB/layer × 5 layers; not stated by authors)
- **Provenance strength:** STRONG
- **Acceptance verdict:** **FAIL** — fails criterion 1 on two axes (Llama-3 vs. Llama-3.1, and Instruct vs. base). Criteria 2, 3, 4, 5 all PASS.

### Candidate 2:
- **URL:** https://drive.google.com/drive/folders/1IGt7NNV-OxXqIljjr02_k0dDY50Z5N_E (linked from WanliYoung/Revisit-Editing-Evaluation `download_stats.sh`)
- **Source organization / paper / author:** zjunlp / EasyEdit team (redistributed by "Mirage of Model Editing", Yang et al., ACL 2025)
- **Exact base model:** meta-llama/Llama-2-7b
- **Layer indices:** unverified from README (likely default EasyEdit MEMIT layers)
- **mom2_dataset:** wikipedia
- **mom2_n_samples:** unspecified (likely 100000 per EasyEdit defaults)
- **mom2_dtype:** unspecified (likely float32 per EasyEdit defaults)
- **File format:** directory of per-layer files (`wikipedia_stats/`)
- **Total size:** unstated
- **Provenance strength:** STRONG
- **Acceptance verdict:** **FAIL** — fails criterion 1 (Llama-2-7B, not Llama-3.1-8B). Other criteria not fully verifiable from public README.

---

## Overall result against acceptance criteria:

**Zero candidates PASS all five criteria.** No public release of a MEMIT covariance cache for `meta-llama/Llama-3.1-8B` (exact base, non-Instruct) computed on Wikipedia with ≥100K samples in float32 covering layers 4–8 was found.

**Confidence:** high

---

## Anything else worth flagging:

- **EasyEdit (zjunlp) only ships a Llama-2-7B cache.** Its `hparams/MEMIT/` directory contains a `llama3-8b.yaml` config but no corresponding stats file is published by zjunlp on GitHub Releases or HuggingFace.
- **The "Mirage of Model Editing" repo (WanliYoung/Revisit-Editing-Evaluation) has an explicit "coming soon" note** stating they intend to upload llama3-8b and mistral-7b stats — as of last update, not yet released. This means even Llama-3-8B *base* (let alone 3.1) is not publicly distributed by the major framework maintainers.
- **AlphaEdit's cache is the closest functional match** (layers 4–8, Wikipedia, 100K samples, float32 — all four secondary criteria PASS exactly), but it's built against Llama-3-8B-**Instruct**, which differs from Llama-3.1-8B base on two independent axes (pretraining checkpoint version + post-training SFT/RLHF). Tensor shapes are architecturally identical (32 layers, hidden 4096, intermediate 14336), so the file would *load* without error — but the activation statistics will not faithfully represent the target model.
- **Original MEMIT/ROME author repos (kmeng01) ship no LLaMA-family caches at all** — only GPT-2 XL, GPT-J, GPT-NeoX. Confirmed via repo inspection.
- **Several 2024–2026 papers that evaluate MEMIT-family methods on Llama-3.1-8B** (e.g., the OpenReview "Resolving UnderEdit & OverEdit" paper) treat EasyEdit as the cache source rather than releasing their own — meaning any Llama-3.1-8B caches actually used in published experiments appear to have been computed locally by the authors and not redistributed.
- **HuggingFace Datasets has no relevant hits.** The single name-overlap result `balu1235/llama-3.1-8b-Wikipedia` is an unrelated fine-tuned model checkpoint, not a covariance cache.
- **The "Efficient Knowledge Editing via Minimal Precomputation" paper (arxiv 2506.04226) explicitly motivates avoiding the 36–40 hour cache computation** — indirect confirmation that no off-the-shelf Llama-3.1-8B cache is circulating in the research community.

---

# Candidate entries
Source: ChatGPT Deep Research
Date run: 2026-04-29

## Candidate 1

URL: https://github.com/wanglne/DELMAN and linked artifact folder https://drive.google.com/drive/folders/1uee2b_rti0UlNgQ52hlY2oVB5AduO7Ch?usp=sharing

Source organization / paper / author: official repo for the DELMAN paper, marked “Accepted by ACL 2025 Findings,” under the GitHub account wanglne. The README states: “We directly provide the cov matrix of models that we have already calculated.”

Exact base model (verbatim): meta-llama/Llama-3.1-8B-Instruct
Layer indices: [7,8]
mom2_dataset: wikipedia
mom2_n_samples: 100000
mom2_dtype: float32

File format: unspecified in the public indexed folder listing.
Total size: unspecified.

Provenance strength: STRONG
Confidence: medium

Acceptance verdict: PARTIAL
Fails: criterion 1 because the checkpoint is meta-llama/Llama-3.1-8B-Instruct, not the exact base model meta-llama/Llama-3.1-8B; criterion 2 because the hparams cover only layers [7,8], not a superset of [4,5,6,7,8].

Anything else worth flagging: the repo is explicit that the target rewrite module is model.layers.{}.mlp.down_proj, which is the correct Llama-family target for MEMIT-style second-moment caches. The missing piece is exact-model identity and layer coverage.

## Candidate 2

URL: https://github.com/jianghoucheng/AlphaEdit and linked artifact file https://drive.google.com/file/d/1GhDb4vPd1NIyRCbbIlgXV45xbE2UQMav/view?usp=sharing

Source organization / paper / author: official repo for AlphaEdit, identified in the README as “ICLR 2025 Outstanding Paper,” under the GitHub account jianghoucheng. The repo says it “directly provide[s] the cov matrix of Llama3-8B-instruct that we have already calculated.”

Exact base model (verbatim): meta-llama/Meta-Llama-3-8B-Instruct in the repo’s example command.
Layer indices: [4,5,6,7,8]
mom2_dataset: wikipedia
mom2_n_samples: 100000
mom2_dtype: float32

File format: the accessible Drive object resolves to null_space_project.pt, so the public indexed file page is .pt.
Total size: unspecified from the accessible Drive page.

Provenance strength: STRONG
Confidence: medium

Acceptance verdict: PARTIAL
Fails: criterion 1 because the model is meta-llama/Meta-Llama-3-8B-Instruct, not the exact requested base model meta-llama/Llama-3.1-8B.

Anything else worth flagging: there is a real ambiguity here. The README describes the linked artifact as a precomputed covariance matrix, but the accessible Google Drive file page titles it null_space_project.pt, which sounds like an AlphaEdit projection matrix rather than a raw MEMIT covariance cache. Separately, an issue in the same repo mentions “the covariance matrix provided by the authors,” which suggests the authors did distribute covariance-related artifacts, but the indexed public page does not cleanly prove that the linked Drive file is the covariance cache itself.

## Candidate 3

URL: https://huggingface.co/datasets/jasonrichdarmawan/rke/tree/main/data/stats/Meta-Llama-3-8B-Instruct/wikipedia_stats

Source organization / paper / author: public Hugging Face dataset jasonrichdarmawan/rke. I did not find a primary-paper or institutional affiliation exposed on the dataset page itself.

Exact base model (verbatim): Meta-Llama-3-8B-Instruct
Layer indices: explicit files are listed for model.layers.4.mlp.down_proj_float32_mom2_100000.npz, 5, 6, 7, and 8, so this artifact includes the full required layer set.
mom2_dataset: wikipedia
mom2_n_samples: 100000
mom2_dtype: float32

File format: .npz for the individual down-proj covariance files.
Total size: the wikipedia_stats folder is listed as 9.85 GB; each required down-proj file is 822 MB, so the five required down-proj files total approximately 4.11 GB.

Provenance strength: WEAK
Confidence: high

Acceptance verdict: PARTIAL
Fails: criterion 1 because the model path is Meta-Llama-3-8B-Instruct, not the exact base meta-llama/Llama-3.1-8B.

Anything else worth flagging: this is the cleanest concrete file manifest I found. The folder also contains null_space_project.pt (4.11 GB) and null_space_project_unke_Alpha.pt (1.22 GB), suggesting the uploader bundled covariance caches and AlphaEdit-style projection artifacts together. That makes this a useful fallback reference set, but not a pass for your exact-model requirement.

## Bottom-line assessment and limitations
No candidate I could verify qualifies as a PASS for the exact base checkpoint meta-llama/Llama-3.1-8B. The official Meta model page makes clear that meta-llama/Llama-3.1-8B is the pretrained base model you want, distinct from the instruct-tuned variants; none of the concrete public artifacts I verified used that exact model string while also satisfying your other four criteria.

The strongest near-match by family/version is DELMAN’s official meta-llama/Llama-3.1-8B-Instruct setup, but it misses your required layer coverage. The strongest near-match by layer/dataset/sample/dtype metadata is AlphaEdit’s Meta-Llama-3-8B-Instruct hparams. The strongest near-match by concrete downloadable file manifest is the jasonrichdarmawan/rke Hugging Face dataset, which explicitly lists the five required .npz down-proj files for layers 4 through 8, but for the wrong instruct-tuned Llama 3.0 checkpoint.

Two limits are worth stating clearly. First, some linked Google Drive artifacts do not expose indexed internal manifests, so I could not verify their file lists or total sizes from the public pages alone. Second, absence is always harder to prove than presence; what I can say rigorously is that the primary public sources you prioritized did not surface a verifiable public cache release for the exact base model. The supporting negative evidence is the lack of official MEMIT/Bau Lab Llama-family stats in the public index, no GitHub release channel on MEMIT or EasyEdit, and an EasyEdit-adjacent ACL 2025 repo still describing Llama 3 stats as future uploads rather than present public artifacts.
