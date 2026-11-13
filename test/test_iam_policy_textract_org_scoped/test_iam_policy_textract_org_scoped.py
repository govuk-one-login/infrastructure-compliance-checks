import unittest
from pathlib import Path

from conftest import run_check

FIXTURES = Path(__file__).resolve().parent / "fixtures"
CHECK_ID = "GDS_DEVPLATFORM_008"


class TestIAMTextractOrgScoped(unittest.TestCase):
    def test_pass_explicit_action(self):
        passed, failed = run_check(FIXTURES / "pass_scoped_org.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, passed)
        self.assertNotIn(CHECK_ID, failed)

    def test_fail_explicit_action(self):
        passed, failed = run_check(FIXTURES / "fail_scoped_org.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, failed)
        self.assertNotIn(CHECK_ID, passed)


if __name__ == "__main__":
    unittest.main()
