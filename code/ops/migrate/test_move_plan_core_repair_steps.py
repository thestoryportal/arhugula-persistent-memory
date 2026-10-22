"""Behavioral contract for the explicit repair-step set (Step 386)."""
import unittest
from unittest import mock

from ops.migrate import fdsafe
from ops.migrate import move_plan_core as core
from test_move_plan_core import check_plans, occ, repairs


def check_step(step):
    return check_plans([occ()], repairs((
        "code/x.py", 3, "/p/u1/a.json", "/m/experiments/c10r/runs/u1/a.json", step)))


class RepairSteps(unittest.TestCase):
    def test_each_allowed_step_is_accepted(self):
        for step in (*range(261, 270), 387):
            with self.subTest(step=step):
                self.assertEqual(check_step(step), ())

    def test_each_disallowed_step_has_exact_refusal(self):
        for step in (260, 270, 386, 388):
            with self.subTest(step=step):
                with self.assertRaises(fdsafe.Refusal) as caught:
                    check_step(step)
                self.assertEqual(str(caught.exception),
                                 f"'/m/program/repairs.tsv:2': repair step {step} "
                                 "is not one of 261-269, 387")

    def test_refusal_is_derived_from_current_set(self):
        # [LAW:behavior-not-structure] Observe the public refusal after changing its authority.
        with mock.patch.object(core, "REPAIR_STEPS", frozenset({1, 2, 3, 7, 9, 10})):
            with self.assertRaises(fdsafe.Refusal) as caught:
                check_step(4)
        self.assertEqual(str(caught.exception),
                         "'/m/program/repairs.tsv:2': repair step 4 is not one of 1-3, 7, 9-10")

    def test_repair_steps_is_exact_frozenset(self):
        self.assertIs(type(core.REPAIR_STEPS), frozenset)
        self.assertEqual(core.REPAIR_STEPS, frozenset({*range(261, 270), 387}))


if __name__ == "__main__":
    unittest.main()
