import unittest
from pathlib import Path

from conftest import run_check

FIXTURES = Path(__file__).resolve().parent / "fixtures"
CHECK_ID = "GDS_DEVPLATFORM_009"


class TestExecuteIAMApiInvokeScoped(unittest.TestCase):
    def test_pass_explicit_action(self):
        passed, failed = run_check(FIXTURES / "pass.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, passed)
        self.assertNotIn(CHECK_ID, failed)

    def test_fail_explicit_action(self):
        passed, failed = run_check(FIXTURES / "fail.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, failed)
        self.assertNotIn(CHECK_ID, passed)

    def test_fail_without_boolean_condition(self):
        passed, failed = run_check(
            FIXTURES / "fail_without_boolean_condition.yaml", CHECK_ID
        )
        self.assertIn(CHECK_ID, failed)
        self.assertNotIn(CHECK_ID, passed)

    def test_fail_without_any_condition(self):
        passed, failed = run_check(
            FIXTURES / "fail_without_any_conditions.yaml", CHECK_ID
        )
        self.assertIn(CHECK_ID, failed)
        self.assertNotIn(CHECK_ID, passed)


if __name__ == "__main__":
    unittest.main()
