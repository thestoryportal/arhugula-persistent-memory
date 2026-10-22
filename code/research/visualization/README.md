# Seeing the shape of the Qwen2.5-3B model

`qwen25_3b_2layer_structure.onnx` is a picture-able blueprint of the model our experiments edit (Qwen2.5-3B). Open it in a free viewer called Netron and you can click around the model's wiring like a circuit diagram.

## What the file shows

The real model is one "stage" repeated 36 times in a row (the code calls each stage a "layer"). All 36 stages have the same design. This file draws only 2 of them (stage 0 and stage 1) so it opens fast. If you understand one stage, you understand all 36.

The sizes are the real ones (the width of the data flowing through, the size of the word list, the number of attention heads). Only the number of stages was cut from 36 to 2.

**This file holds random numbers, not the real weights.** It shows how the model is wired, not what it knows. Do not run it expecting sensible text.

## How to open it

1. Download the desktop app from https://netron.app (the Mac download is the easiest).
2. Open the app and choose File > Open, then pick `/Volumes/memit/llmdb-preserved/icm21-20261013/M/visualization/qwen25_3b_2layer_structure.onnx`.
3. The file is about 1.5 GB, so give it a few seconds to load. Use the mouse wheel to zoom and drag to move around. Click any box to see its details on the right.

## What to look for

Each stage has two main parts. Box names in Netron look like `/model/layers.0/mlp/down_proj/MatMul`, so you can read where each one sits.

- **The attention block** (names contain `self_attn`). This is where each word looks at the other words in the text. Inside you will see `q_proj`, `k_proj` and `v_proj` (three "look-up" steps), a `Softmax` (the step that decides how much to focus on each word), and `o_proj` (the step that combines the result).
- **The MLP block** (names contain `mlp`). Think of this as the model's memory bank, where facts are mostly stored. It has three steps: `gate_proj` and `up_proj` expand the data, and `down_proj` shrinks it back down.
- **`down_proj`** (for example `/model/layers.0/mlp/down_proj/MatMul`). This is the part our experiments edit. In the real model we edit it in stages 4 through 8. This file only has stages 0 and 1, so the same box is there, but at a different position than the real ones.

At the very top and bottom you will also see the word-list lookup (`embed_tokens`), the final cleanup step (`norm`), and the last step that turns the result into a score for every possible next word (`lm_head`). Small `Add` boxes are shortcuts that carry a copy of the data around each block.

## Where the real weights live

The real model is stored in two files in this folder:

`/Volumes/memit/llm-database-poc-mirror/hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/`

- `model-00001-of-00002.safetensors`
- `model-00002-of-00002.safetensors`

## How the file was made

`build_structure_onnx.py` (in this folder) reads the real `config.json` from that snapshot, builds the model with 2 stages and random numbers on the CPU only (no GPU), and exports it. Rerun it with the project's Python plus the `onnx` and `onnxscript` packages on the path.
