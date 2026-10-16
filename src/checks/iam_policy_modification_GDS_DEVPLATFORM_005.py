from checkov.cloudformation.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckCategories, CheckResult
from helpers import get_policy_documents, matches_with_wildcard

POLICY_MODIFICATION_ACTIONS = {
    "iam:PutRolePolicy",
    "iam:AttachRolePolicy",
    "iam:DetachRolePolicy",
    "iam:DeleteRolePolicy",
    "iam:CreatePolicy",
    "iam:DeletePolicy",
    "iam:CreatePolicyVersion",
    "iam:DeletePolicyVersion",
    "iam:SetDefaultPolicyVersion",
    "iam:*",
    "iam:Put*",
    "iam:Attach*",
    "iam:Detach*",
    "iam:Delete*",
    "iam:Create*",
}


class IAMPolicyModification(BaseResourceCheck):
    def __init__(self):
        super().__init__(
            name="Ensure IAM policies do not grant policy modification actions on wildcard resources",
            id="GDS_DEVPLATFORM_005",
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

                if not any(
                    matches_with_wildcard(str(action), target)
                    for action in actions
                    for target in POLICY_MODIFICATION_ACTIONS
                ):
                    continue

                resources = statement.get("Resource", [])
                if isinstance(resources, str):
                    resources = [resources]

                if any(r == "*" for r in resources):
                    return CheckResult.FAILED

        return CheckResult.PASSED


check = IAMPolicyModification()
