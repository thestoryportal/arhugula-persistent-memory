#!/usr/bin/env python3
"""B1: exercise the production merge on tiny CPU tensors (prereg:250)."""
import ast
import unittest
from pathlib import Path

import torch


def merge(weight, delta):
    # Isolate the actual merge statements so the fixed model dimensions need no model.
    tree = ast.parse(Path(__file__).with_name("c10w_oracle_eval.py").read_text())
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Evaluator")
    method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "apply_adapter")
    loop = next(n for n in method.body if isinstance(n, ast.For))
    statements = [n for n in loop.body if
                  isinstance(n, ast.With) or
                  (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "d16" for t in n.targets))]
    assert sum(isinstance(n, ast.With) for n in statements) == 1, "production merge absent"
    exec(compile(ast.Module(body=statements, type_ignores=[]), "production-merge", "exec"),
         {"torch": torch, "weight": weight, "delta": delta})


def bits(tensor):
    return tensor.detach().contiguous().view(torch.uint8).tolist()


class SignedZeroTests(unittest.TestCase):
    def test_zero_delta_preserves_every_fp16_byte(self):
        weight = torch.tensor([-0.0, 0.0, 1.0, -2.0], dtype=torch.float16, device="cpu")
        before = bits(weight)
        merge(weight, torch.zeros(4, dtype=torch.float32, device="cpu"))
        self.assertEqual(bits(weight), before)

    def test_nonzero_delta_applies_and_zero_entries_keep_their_bits(self):
        weight = torch.tensor([-0.0, 0.0, 1.0, -2.0], dtype=torch.float16, device="cpu")
        merge(weight, torch.tensor([0.0, -1.0, 0.25, 0.0], dtype=torch.float32, device="cpu"))
        expected = torch.tensor([-0.0, -1.0, 1.25, -2.0], dtype=torch.float16, device="cpu")
        self.assertEqual(bits(weight), bits(expected))

    def test_quantized_zero_boundary(self):
        # At the half-subnormal tie, fp16 rounds to even zero; above it applies.
        for sign in (-1, 1):
            for factor in (0.99, 1.0, 1.01):
                with self.subTest(sign=sign, factor=factor):
                    weight = torch.tensor([-0.0], dtype=torch.float16, device="cpu")
                    delta = torch.tensor([sign * 2**-25 * factor], dtype=torch.float32, device="cpu")
                    expected = (weight + delta.to(torch.float16)) if factor > 1 else weight.clone()
                    merge(weight, delta)
                    self.assertEqual(bits(weight), bits(expected))


if __name__ == "__main__":
    unittest.main(verbosity=2)
