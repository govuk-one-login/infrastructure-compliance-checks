from checkov.cloudformation.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckCategories, CheckResult
from helpers import get_policy_documents, is_valid_resource, matches_with_wildcard

COVERED_ACTIONS = [
    "sqs:ChangeMessageVisibility",
    "sqs:DeleteMessage",
    "sqs:GetQueue*",
    "sqs:ReceiveMessage",
    "sqs:SendMessage*",
    "sns:Publish",
    "execute-api:Invoke",
    "dynamodb:BatchGetItem",
    "dynamodb:BatchWriteItem",
    "dynamodb:DescribeTable",
    "dynamodb:Get*",
    "dynamodb:Query",
    "dynamodb:Scan",
    "dynamodb:UpdateItem",
    "dynamodb:PutItem",
    "dynamodb:DeleteItem",
    "s3:AbortMultipartUpload",
    "s3:DeleteObject",
    "s3:DeleteObject*",
    "s3:PutObject",
    "s3:PutObject*",
    "s3:PutObjectAcl",
    "s3:PutObjectTagging",
    "s3:PutLifecycleConfiguration",
    "s3:PutLifecycle*",
    "s3:RestoreObject",
    "acm-pca:DescribeCertificateAuthority",
]

RESOURCE_ACCOUNT_KEY = "aws:ResourceAccount"


def _statements(doc):
    if not isinstance(doc, dict):
        return []
    statements = doc.get("Statement", [])
    if isinstance(statements, dict):
        statements = [statements]
    return [s for s in statements if isinstance(s, dict)]


def _actions(statement):
    actions = statement.get("Action", [])
    if isinstance(actions, str):
        actions = [actions]
    return [a for a in actions if isinstance(a, str)]


def _grants_covered_action(statement):
    return any(
        matches_with_wildcard(action, covered) or matches_with_wildcard(covered, action)
        for action in _actions(statement)
        for covered in COVERED_ACTIONS
    )


def _has_wildcard_account_resource(statement):
    resources = statement.get("Resource", [])
    if isinstance(resources, (str, dict)):
        resources = [resources]
    return any(not is_valid_resource(r) for r in resources if r != "*")


def _has_resource_account_condition(condition):
    if not isinstance(condition, dict):
        return False
    return any(
        isinstance(block, dict) and RESOURCE_ACCOUNT_KEY in block
        for block in condition.values()
    )


class ResourceAccountCondition(BaseResourceCheck):
    def __init__(self):
        super().__init__(
            name="Ensure cross-account actions include aws:ResourceAccount condition",
            id="GDS_DEVPLATFORM_007",
            categories=[CheckCategories.IAM],
            supported_resources=[
                "AWS::IAM::ManagedPolicy",
                "AWS::IAM::Policy",
                "AWS::IAM::Role",
            ],
        )

    def scan_resource_conf(self, conf):
        for doc in get_policy_documents(conf):
            for statement in _statements(doc):
                if statement.get("Effect") != "Allow":
                    continue
                if not _grants_covered_action(statement):
                    continue
                if not _has_wildcard_account_resource(statement):
                    continue
                if not _has_resource_account_condition(statement.get("Condition", {})):
                    return CheckResult.FAILED

        return CheckResult.PASSED


check = ResourceAccountCondition()
