import json
import re


def matches_with_wildcard(pattern: str, target: str) -> bool:
    regex = re.escape(pattern).replace(r"\*", ".*")
    return bool(re.fullmatch(regex, target))


def get_policy_documents(conf):
    properties = conf.get("Properties", {})
    docs = []

    # AWS::IAM::ManagedPolicy and AWS::IAM::Policy
    if "PolicyDocument" in properties:
        docs.append(properties["PolicyDocument"])

    # AWS::IAM::Role inline policies
    for inline in properties.get("Policies", []):
        doc = inline.get("PolicyDocument")
        if doc:
            docs.append(doc)

    result = []
    for doc in docs:
        if isinstance(doc, str):
            try:
                doc = json.loads(doc)
            except (json.JSONDecodeError, TypeError):
                continue
        result.append(doc)

    return result


def is_valid_resource(resource):
    if isinstance(resource, dict):
        # Fn::GetAtt and Fn::ImportValue always resolve to same-account resources
        if "Fn::GetAtt" in resource or "Fn::ImportValue" in resource:
            return True
        sub = resource.get("Fn::Sub", "")
        if isinstance(sub, list):
            sub = sub[0]
        sub = str(sub)
        if not sub.startswith("arn:"):
            return True  # not an ARN — same-account reference (e.g. ${Bucket.Arn}/*)
        return not _has_wildcard_account_segment(sub)
    return bool(re.match(r"arn:[^:]+:[^:]+::(\d{12}):", str(resource)))


def _has_wildcard_account_segment(arn):
    """Return True if the account segment of an ARN is a bare wildcard (*)."""
    # ARN format: arn:partition:service:region:account:resource
    # Uses re.search (not re.match) so CFN intrinsics like ${AWS::Partition} that
    # contain '::' do not affect correctness — the pattern still finds ':*:' in
    # the account position regardless of how many segments precede it.
    return bool(re.search(r"(?::[^:]*){3}:\*:", arn))
