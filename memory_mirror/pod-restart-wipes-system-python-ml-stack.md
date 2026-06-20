---
name: pod-restart-wipes-system-python-ml-stack
description: "After a RunPod restart, system-python3.11 loses transformers/datasets/etc; torch survives — reinstall the pinned stack before any run"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7e49dca7-c684-465a-936b-1c2ce4852502
---

On this RunPod pod the ML stack is installed into **system** `python3.11` (`/usr/local/lib/python3.11/dist-packages`), NOT a venv. A pod restart/reimage **wipes the pip-installed packages that aren't in the base image** — `transformers`, `datasets`, `matplotlib`, `accelerate`, `tokenizers`, `safetensors`, `scipy` were all gone — while **torch 2.4.1+cu124 (CUDA) survived** (it's in the base image). Symptom: `ModuleNotFoundError: No module named 'transformers'` (then `datasets`, then `matplotlib`) on engine import, even though everything worked last session.

**Fix (infra restoration, standing-auth — NOT an upgrade):** reinstall the **exact pin** (`REPRODUCIBILITY.md`):
`python3.11 -m pip install "transformers==4.51.0" accelerate datasets scipy matplotlib`
Then verify torch is UNCHANGED: `python3.11 -c "import transformers,torch;print(transformers.__version__,torch.__version__,torch.cuda.is_available())"` → must print `4.51.0 2.4.1+cu124 True`. Do NOT let pip bump torch (transformers treats torch as optional, so it won't — confirm anyway). Engine import also needs the script to `os.chdir(ENGINE_ROOT)` (it reads `globals.yml` relative to cwd).

**Gotchas:** (1) the interpreter is **`python3.11`**, not bare `python`/`python3` (those are a different system python WITHOUT the stack — a detached `setsid bash -c '... python ...'` will silently use the wrong one). (2) pip HAS PyPI network from Claude's sandboxed Bash (the "no network" caveat is about git push / credentials, not PyPI). Related: [[verify-canonical-state-edits-persist]].
