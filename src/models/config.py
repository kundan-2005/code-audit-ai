"""Configuration models for audits."""

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class AuditConfig:
    """Configuration for code audits."""

    check_security: bool = True
    """Enable security vulnerability checks."""

    check_performance: bool = True
    """Enable performance analysis."""

    check_quality: bool = True
    """Enable code quality checks."""

    check_functionality: bool = True
    """Enable functionality verification."""

    severity_threshold: Optional[str] = None
    """Filter issues by severity: low, medium, high, critical. None = show all."""

    language: str = "python"
    """Programming language of the code being audited."""

    max_issues: int = 100
    """Maximum number of issues to report."""

    timeout: int = 30
    """Timeout for audit in seconds."""

    verbose: bool = False
    """Enable verbose logging."""

    def __repr__(self) -> str:
        """String representation of config."""
        return (
            f"AuditConfig(security={self.check_security}, "
            f"performance={self.check_performance}, "
            f"quality={self.check_quality}, "
            f"functionality={self.check_functionality}, "
            f"language={self.language})"
        )
