import unittest
from pathlib import Path

from conftest import run_check

FIXTURES = Path(__file__).resolve().parent / "fixtures"
CHECK_ID = "GDS_DEVPLATFORM_007"


class TestResourceAccountCondition(unittest.TestCase):
    def test_pass_sqs(self):
        passed, failed = run_check(FIXTURES / "pass_sqs.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, passed)
        self.assertNotIn(CHECK_ID, failed)

    def test_fail_sqs(self):
        passed, failed = run_check(FIXTURES / "fail_sqs.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, failed)
        self.assertNotIn(CHECK_ID, passed)

    def test_pass_sns(self):
        passed, failed = run_check(FIXTURES / "pass_sns.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, passed)
        self.assertNotIn(CHECK_ID, failed)

    def test_fail_sns(self):
        passed, failed = run_check(FIXTURES / "fail_sns.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, failed)
        self.assertNotIn(CHECK_ID, passed)

    def test_pass_dynamodb(self):
        passed, failed = run_check(FIXTURES / "pass_dynamodb.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, passed)
        self.assertNotIn(CHECK_ID, failed)

    def test_fail_dynamodb(self):
        passed, failed = run_check(FIXTURES / "fail_dynamodb.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, failed)
        self.assertNotIn(CHECK_ID, passed)

    def test_pass_s3(self):
        passed, failed = run_check(FIXTURES / "pass_s3.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, passed)
        self.assertNotIn(CHECK_ID, failed)

    def test_fail_s3(self):
        passed, failed = run_check(FIXTURES / "fail_s3.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, failed)
        self.assertNotIn(CHECK_ID, passed)

    def test_pass_execute_api(self):
        passed, failed = run_check(FIXTURES / "pass_execute_api.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, passed)
        self.assertNotIn(CHECK_ID, failed)

    def test_fail_execute_api(self):
        passed, failed = run_check(FIXTURES / "fail_execute_api.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, failed)
        self.assertNotIn(CHECK_ID, passed)

    def test_pass_acm_pca(self):
        passed, failed = run_check(FIXTURES / "pass_acm_pca.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, passed)
        self.assertNotIn(CHECK_ID, failed)

    def test_fail_acm_pca(self):
        passed, failed = run_check(FIXTURES / "fail_acm_pca.yaml", CHECK_ID)
        self.assertIn(CHECK_ID, failed)
        self.assertNotIn(CHECK_ID, passed)


if __name__ == "__main__":
    unittest.main()
