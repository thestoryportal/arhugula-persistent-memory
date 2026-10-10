import json
import os
from pathlib import Path
import signal
import time
import unittest
from investigation_io import write_json
from state_observer import snapshot


class NumericalInitialization(unittest.TestCase):
    def test_parent_initialization(self):
        import numpy as np
        import torch
        torch.set_num_threads(1)
        matrix=torch.eye(5,device='cpu',dtype=torch.float64)
        torch.linalg.svd(matrix)
        np.linalg.svd(np.eye(5))
        write_json(Path(os.environ['NEW1_CONDITION_DIR'])/'numerical_initialization.json',
                   {'phase':'preceding-numerical-initialization','device':'cpu','model_load':False,
                    'state':snapshot(),'tensor_sum':float(matrix.sum())})
        self.assertEqual(float(matrix.sum()),5.)


class CapturedBlockedMask(unittest.TestCase):
    def test_apply_observed_parent_mask(self):
        before=snapshot()
        signal.pthread_sigmask(signal.SIG_BLOCK,[signal.SIGINT,signal.SIGALRM])
        write_json(Path(os.environ['NEW1_CONDITION_DIR'])/'captured_mask_condition.json',
                   {'phase':'synthetic-captured-condition','source':'step2_baseline_03',
                    'before':before,'after':snapshot(),'intent':'condition persists through subsequent control in this fresh process'})
        self.assertEqual(set(signal.pthread_sigmask(signal.SIG_BLOCK,[])),{signal.SIGINT,signal.SIGALRM})
