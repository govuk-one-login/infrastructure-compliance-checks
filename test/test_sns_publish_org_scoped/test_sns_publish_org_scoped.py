import unittest
from pathlib import Path

from conftest import run_check

FIXTURES = Path(__file__).resolve().parent / "fixtures"
CHECK_ID = "GDS_DEVPLATFORM_006"


class TestSNSPublishOrgScoped(unittest.TestCase):
    def test_pass_with_principal_org_id(self):
        passed, failed = run_check(FIXTURES / "pass.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, passed)
        self.assertNotIn(CHECK_ID, failed)

    def test_fail_without_principal_org_id(self):
        passed, failed = run_check(FIXTURES / "fail.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, failed)
        self.assertNotIn(CHECK_ID, passed)

    def test_fail_wildcard_action(self):
        passed, failed = run_check(FIXTURES / "fail_wildcard_action.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, failed)
        self.assertNotIn(CHECK_ID, passed)

    def test_pass_cognito_wildcard_resource(self):
        passed, failed = run_check(
            FIXTURES / "pass_cognito_wildcard_resource.yaml", CHECK_ID
        )
        self.assertIn(CHECK_ID, passed)
        self.assertNotIn(CHECK_ID, failed)

    def test_pass_same_account_resource(self):
        passed, failed = run_check(
            FIXTURES / "pass_same_account_resource.yaml", CHECK_ID
        )
        self.assertIn(CHECK_ID, passed)
        self.assertNotIn(CHECK_ID, failed)


if __name__ == "__main__":
    unittest.main()
