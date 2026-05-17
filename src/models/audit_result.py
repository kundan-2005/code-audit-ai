"""Audit result model."""

from typing import List, Optional
from src.models.issue import Issue
from src.models.config import AuditConfig
import json
from datetime import datetime


class AuditResult:
    """Result of a code audit."""

    def __init__(
        self,
        code: str,
        issues: List[Issue],
        filename: Optional[str] = None,
        total_issues: int = 0,
        config: Optional[AuditConfig] = None,
    ):
        """Initialize AuditResult.

        Args:
            code: The code that was audited
            issues: List of issues found
            filename: Optional filename
            total_issues: Total issues before filtering
            config: Audit configuration used
        """
        self.code = code
        self.issues = issues
        self.filename = filename
        self.total_issues = total_issues
        self.config = config
        self.timestamp = datetime.now().isoformat()

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"AuditResult(filename={self.filename}, "
            f"issues={len(self.issues)}, total={self.total_issues})"
        )

    def __bool__(self) -> bool:
        """Boolean evaluation - True if issues found."""
        return len(self.issues) > 0

    def __len__(self) -> int:
        """Return number of issues found."""
        return len(self.issues)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "filename": self.filename,
            "timestamp": self.timestamp,
            "total_issues": self.total_issues,
            "filtered_issues": len(self.issues),
            "issues": [issue.to_dict() for issue in self.issues],
            "config": str(self.config),
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    def has_critical_issues(self) -> bool:
        """Check if result has critical issues."""
        from src.models.issue import Severity
        return any(issue.severity == Severity.CRITICAL for issue in self.issues)
