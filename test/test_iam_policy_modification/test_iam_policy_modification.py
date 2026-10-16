import unittest
from pathlib import Path

from conftest import run_check

FIXTURES = Path(__file__).resolve().parent / "fixtures"
CHECK_ID = "GDS_DEVPLATFORM_005"


class TestIAMPolicyModification(unittest.TestCase):
    def test_fail_explicit_action(self):
        passed, failed = run_check(FIXTURES / "fail_explicit_action.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, failed)
        self.assertNotIn(CHECK_ID, passed)

    def test_fail_wildcard_action(self):
        passed, failed = run_check(FIXTURES / "fail_wildcard_action.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, failed)
        self.assertNotIn(CHECK_ID, passed)

    def test_fail_iam_star(self):
        passed, failed = run_check(FIXTURES / "fail_iam_star.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, failed)
        self.assertNotIn(CHECK_ID, passed)

    def test_pass_scoped_arn(self):
        passed, failed = run_check(FIXTURES / "pass_scoped_arn.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, passed)
        self.assertNotIn(CHECK_ID, failed)

    def test_pass_deny(self):
        passed, failed = run_check(FIXTURES / "pass_deny.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, passed)
        self.assertNotIn(CHECK_ID, failed)

    def test_pass_unrelated_action(self):
        passed, failed = run_check(FIXTURES / "pass_unrelated_action.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, passed)
        self.assertNotIn(CHECK_ID, failed)


if __name__ == "__main__":
    unittest.main()
