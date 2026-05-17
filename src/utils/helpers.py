"""Helper utilities."""

from typing import List, Dict
from src.models.issue import Issue, Severity


def format_issue(issue: Issue) -> str:
    """Format an issue for display.

    Args:
        issue: Issue to format

    Returns:
        Formatted string representation
    """
    return (
        f"[{issue.severity.name}] {issue.title}\n"
        f"  Line: {issue.line}\n"
        f"  Message: {issue.message}\n"
        f"  Type: {issue.issue_type}\n"
        + (f"  Suggestion: {issue.suggestion}\n" if issue.suggestion else "")
    )


def group_issues(issues: List[Issue]) -> Dict[Severity, List[Issue]]:
    """Group issues by severity.

    Args:
        issues: List of issues to group

    Returns:
        Dictionary mapping severity to list of issues
    """
    grouped: Dict[Severity, List[Issue]] = {}
    for issue in issues:
        if issue.severity not in grouped:
            grouped[issue.severity] = []
        grouped[issue.severity].append(issue)
    return grouped
