"""Issue and Severity models."""

from enum import Enum


class Severity(Enum):
    """Severity levels for issues."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    def __str__(self) -> str:
        """String representation."""
        return self.name


class IssueType(Enum):
    """Types of issues that can be found."""

    SECURITY = "security"
    PERFORMANCE = "performance"
    QUALITY = "quality"
    FUNCTIONALITY = "functionality"

    def __str__(self) -> str:
        """String representation."""
        return self.value


class Issue:
    """Represents a code issue found during audit."""

    def __init__(
        self,
        title: str,
        message: str,
        severity: Severity,
        issue_type: IssueType,
        line: int = 0,
        suggestion: str = None,
    ):
        """Initialize an Issue.

        Args:
            title: Short title of the issue
            message: Detailed description
            severity: Severity level
            issue_type: Type of issue
            line: Line number where issue occurs
            suggestion: Suggested fix
        """
        self.title = title
        self.message = message
        self.severity = severity
        self.issue_type = issue_type
        self.line = line
        self.suggestion = suggestion

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"Issue(title='{self.title}', severity={self.severity}, "
            f"type={self.issue_type}, line={self.line})"
        )

    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, Issue):
            return False
        return (
            self.title == other.title
            and self.message == other.message
            and self.severity == other.severity
            and self.issue_type == other.issue_type
            and self.line == other.line
        )

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "message": self.message,
            "severity": self.severity.name,
            "type": self.issue_type.value,
            "line": self.line,
            "suggestion": self.suggestion,
        }
