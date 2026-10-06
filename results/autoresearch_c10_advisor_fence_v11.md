**FIX-FIRST**

**Next:** narrow the `~/Library/Caches` allowance to required runtime caches; deny browser caches in all three layers before launch six.

1. **Confirmed history leak:** [Chrome cache object](</Users/robertrhu/Library/Caches/Google/Chrome/Profile 4/Cache/Cache_Data/f85e6e4504c67b38_0>) remains readable under freshly generated v11 Seatbelt rules: **25,490 bytes**, decompressing to **63,126 bytes**. It contains prior C10 findings: A1/A2 **93.1/97.2 → 0/0**, A7 **9/72 → 1/72**, and fictional-frame leakage **31/36**. This exceeds the accepted screen exposure.

2. **Controlled verification:** probe exit **0**; the same profile denied CORPUS and read required hparams (**639 bytes**). `Google` escapes the cache-name blacklist. [Saved probe evidence](/Users/robertrhu/.gstack/projects/thestoryportal-arhugula-persistent-memory/checkpoints/20261006-123455-autoresearch-fence-v11-review.md). Actual optimizer consumption is **UNVERIFIABLE**.

**Cheapest overturning test:** deny that exact object under Seatbelt and live Claude Bash/Read while GPU, imports, capture and own-temp controls succeed.

**Drift:** this protects C10 candidate-generation integrity toward F1. Equivalence PASS remains independently necessary; it cannot prove isolation.

