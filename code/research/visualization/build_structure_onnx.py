"""Build a 2-layer, random-weight Qwen2.5-3B structure file for Netron (CPU only).

Usage: PYTHONPATH=<dir with onnx+onnxscript> .venv/bin/python visualization/build_structure_onnx.py [dynamo]
"""
import os
import sys

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ.pop("PYTORCH_ENABLE_MPS_FALLBACK", None)

import torch
from transformers import AutoConfig, AutoModelForCausalLM

SNAP = "/Volumes/memit/llm-database-poc-mirror/hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qwen25_3b_2layer_structure.onnx")
DYNAMO = len(sys.argv) > 1 and sys.argv[1] == "dynamo"

cfg = AutoConfig.from_pretrained(SNAP, local_files_only=True)
cfg.num_hidden_layers = 2
cfg.use_cache = False
cfg._attn_implementation = "eager"
model = AutoModelForCausalLM.from_config(cfg, torch_dtype=torch.float16).to("cpu").eval()
print("params:", sum(p.numel() for p in model.parameters()))


class Wrapper(torch.nn.Module):
    """Same modules/names as the HF model, minus the logits_to_keep slicing that adds a stray graph input."""

    def __init__(self, m):
        super().__init__()
        self.model = m.model
        self.lm_head = m.lm_head

    def forward(self, input_ids):
        return self.lm_head(self.model(input_ids=input_ids, use_cache=False).last_hidden_state)


model = Wrapper(model).eval()
ids = torch.arange(8).unsqueeze(0)
with torch.no_grad():
    torch.onnx.export(
        model,
        (ids,),
        OUT,
        input_names=["input_ids"],
        output_names=["logits"],
        opset_version=18 if DYNAMO else 17,
        dynamo=DYNAMO,
    )
print("wrote", OUT)
