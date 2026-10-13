## DEPLOYMENT CONSTRAINT (operator, 2026-06-17): local Intel CPU, no GPU
End product (LLM-as-DB) must do INFERENCE on the operator's Intel CPU machine. Not a current blocker; a steering consideration. See memory `deployment-target-intel-cpu`.
- Separate paths: INFERENCE (CPU → small models: Gemma E2B/E4B, quantized Qwen2.5-3B/7B via llama.cpp/GGUF Q4) vs EDIT/WRITE (heavy MEMIT solve).
- If writes can be OFFLINE-batched on GPU then redeploy quantized → MEMIT-on-GPU OK. If writes must be ONLINE-on-CPU → favors GRACE (rung 5; write = codebook entry, cheap, quant-friendly). OPEN Q for operator: online-CPU vs offline-batch writes.
- Strategic: GATE-CAL v2 shows Qwen-7B same-entity-LOCAL, GPT-J NOT. Add SMALL CPU-class models (Gemma E2B/E4B, Qwen2.5-3B) to the GATE-CAL v2 sweep — if a small model is also local, CPU-deployable LLM-as-DB is viable.

