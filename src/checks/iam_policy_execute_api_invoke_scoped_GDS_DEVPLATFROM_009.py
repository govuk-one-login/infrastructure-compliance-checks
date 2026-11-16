from checkov.cloudformation.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckCategories, CheckResult
from helpers import get_policy_documents

EXECUTE_API_INVOKE = "execute-api:Invoke"
AWS_PRINCIPAL_ORG_ID = "aws:PrincipalOrgID"
STRING_CONDITION = "StringEquals"
BOOLEAN_CONDITION = "Bool"
AWS_SECURE_TRANSPORT = "aws:SecureTransport"


class IAMExecuteApiInvokeScoped(BaseResourceCheck):
    def __init__(self):
        super().__init__(
            name="Ensures API Gateway invoke permissions in CloudFormation templates are restricted to principals within the AWS organisation",
            id="GDS_DEVPLATFORM_009",
            categories=[CheckCategories.IAM],
            supported_resources=[
                "AWS::IAM::ManagedPolicy",
                "AWS::IAM::Policy",
                "AWS::IAM::Role",
            ],
        )

    def scan_resource_conf(self, conf):
        for doc in get_policy_documents(conf):
            for statement in doc.get("Statement", []):
                if statement.get("Effect") != "Allow":
                    continue

                actions = statement.get("Action", [])
                if isinstance(actions, str):
                    actions = [actions]

                if not any(action == EXECUTE_API_INVOKE for action in actions):
                    continue

                conditions = statement.get("Condition", {})
                if isinstance(conditions, dict):
                    conditions = [conditions]

                for condition in conditions:
                    if not (
                        STRING_CONDITION in condition and BOOLEAN_CONDITION in condition
                    ):
                        return CheckResult.FAILED

                    string_condition = condition.get(STRING_CONDITION, {})
                    boolean_condition = condition.get(BOOLEAN_CONDITION, {})

                    if not (
                        AWS_PRINCIPAL_ORG_ID in string_condition
                        and boolean_condition.get(AWS_SECURE_TRANSPORT)
                    ):
                        return CheckResult.FAILED

        return CheckResult.PASSED


check = IAMExecuteApiInvokeScoped()
