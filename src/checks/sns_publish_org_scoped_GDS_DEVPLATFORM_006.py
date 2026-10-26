from checkov.cloudformation.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckCategories, CheckResult
from helpers import get_policy_documents, is_valid_resource, matches_with_wildcard

SNS_PUBLISH_ACTION = "sns:Publish"
PRINCIPAL_ORG_ID_KEY = "aws:PrincipalOrgID"


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


def _grants_sns_publish(statement):
    return any(
        matches_with_wildcard(action, SNS_PUBLISH_ACTION)
        for action in _actions(statement)
    )


def _has_principal_org_id(condition):
    if not isinstance(condition, dict):
        return False
    return any(
        isinstance(block, dict) and PRINCIPAL_ORG_ID_KEY in block
        for block in condition.values()
    )


def _is_exempt(statement):
    """Exempt if Resource is "*" (Cognito) or all resources are scoped to own account."""
    resources = statement.get("Resource", [])
    if isinstance(resources, str):
        resources = [resources]
    return resources == ["*"] or (
        bool(resources) and all(is_valid_resource(r) for r in resources)
    )


class SNSPublishOrgScoped(BaseResourceCheck):
    def __init__(self):
        super().__init__(
            name="Ensure sns:Publish is scoped to the AWS organisation via aws:PrincipalOrgID",
            id="GDS_DEVPLATFORM_006",
            categories=[CheckCategories.IAM],
            supported_resources=[
                "AWS::SNS::TopicPolicy",
                "AWS::IAM::ManagedPolicy",
                "AWS::IAM::Policy",
                "AWS::IAM::Role",
            ],
        )

    def scan_resource_conf(self, conf):
        properties = conf.get("Properties", {})

        # AWS::SNS::TopicPolicy stores its document directly under PolicyDocument
        topic_policy_doc = properties.get("PolicyDocument")
        all_docs = (
            [topic_policy_doc] if topic_policy_doc else []
        ) + get_policy_documents(conf)

        for doc in all_docs:
            for statement in _statements(doc):
                if statement.get("Effect") != "Allow":
                    continue
                if not _grants_sns_publish(statement):
                    continue
                if _is_exempt(statement):
                    continue
                if not _has_principal_org_id(statement.get("Condition", {})):
                    return CheckResult.FAILED

        return CheckResult.PASSED


check = SNSPublishOrgScoped()
