from checkov.cloudformation.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckCategories, CheckResult
from helpers import get_policy_documents

TEXTRACT_WILDCARD = "textract:*"
AWS_PRINCIPAL_ORG_ID = "aws:PrincipalOrgID"
STRING_CONDITION = "StringEquals"


class IAMTextractOrgScoped(BaseResourceCheck):
    def __init__(self):
        super().__init__(
            name="Ensures Textract permissions in CloudFormation templates are restricted to principals within the AWS organisation",
            id="GDS_DEVPLATFORM_008",
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

                if not any(action == TEXTRACT_WILDCARD for action in actions):
                    continue

                conditions = statement.get("Condition", {})
                if isinstance(conditions, dict):
                    conditions = [conditions]

                for condition in conditions:
                    if not (
                        STRING_CONDITION in condition
                        and AWS_PRINCIPAL_ORG_ID in condition.get(STRING_CONDITION, {})
                    ):
                        return CheckResult.FAILED

        return CheckResult.PASSED


check = IAMTextractOrgScoped()
