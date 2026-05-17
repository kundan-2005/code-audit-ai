"""Performance analysis agent."""

from typing import List, Optional
from src.agents.base_agent import BaseAgent
from src.models.issue import Issue, Severity, IssueType
from src.utils.logger import get_logger
import re

logger = get_logger(__name__)


class PerformanceAgent(BaseAgent):
    """Agent for performance analysis."""

    def analyze(self, code: str, filename: Optional[str] = None) -> List[Issue]:
        """Analyze code for performance issues.

        Args:
            code: Source code to analyze
            filename: Optional filename

        Returns:
            List of performance issues found
        """
        issues: List[Issue] = []

        # Check for nested loops
        issues.extend(self._check_nested_loops(code))

        # Check for inefficient string operations
        issues.extend(self._check_string_operations(code))

        # Check for unnecessary imports in loops
        issues.extend(self._check_imports_in_loops(code))

        # Check for unoptimized list operations
        issues.extend(self._check_list_operations(code))

        self._log_analysis("PerformanceAgent", len(issues))
        return issues

    def _check_nested_loops(self, code: str) -> List[Issue]:
        """Check for nested loops."""
        issues = []
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if re.search(r'^\s*for\s+\w+\s+in', line):
                # Check if there's another for loop indented more
                for j in range(i + 1, len(lines)):
                    if not lines[j].strip():
                        continue
                    if len(lines[j]) - len(lines[j].lstrip()) <= len(line) - len(line.lstrip()):
                        break
                    if re.search(r'^\s*for\s+\w+\s+in', lines[j]):
                        issues.append(
                            Issue(
                                title="Nested Loop Detected",
                                message="Nested loops can have O(n²) complexity",
                                severity=Severity.MEDIUM,
                                issue_type=IssueType.PERFORMANCE,
                                line=i + 1,
                                suggestion="Consider using list comprehension or optimizing algorithm",
                            )
                        )
                        break
        return issues

    def _check_string_operations(self, code: str) -> List[Issue]:
        """Check for inefficient string operations."""
        issues = []
        if "str +=" in code or "string +=" in code:
            issues.append(
                Issue(
                    title="Inefficient String Concatenation",
                    message="Using += for string concatenation is inefficient",
                    severity=Severity.MEDIUM,
                    issue_type=IssueType.PERFORMANCE,
                    line=1,
                    suggestion="Use ''.join() or f-strings instead",
                )
            )
        return issues

    def _check_imports_in_loops(self, code: str) -> List[Issue]:
        """Check for imports inside loops."""
        issues = []
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if re.search(r'^\s*for\s+', line):
                for j in range(i + 1, min(i + 20, len(lines))):
                    if re.search(r'^\s*import\s+|^\s*from\s+', lines[j]):
                        issues.append(
                            Issue(
                                title="Import Inside Loop",
                                message="Importing modules inside loops can slow down code",
                                severity=Severity.LOW,
                                issue_type=IssueType.PERFORMANCE,
                                line=j + 1,
                                suggestion="Move imports to the top of the file",
                            )
                        )
                        break
        return issues

    def _check_list_operations(self, code: str) -> List[Issue]:
        """Check for unoptimized list operations."""
        issues = []
        if re.search(r'\[.*\s+for\s+.*\s+in\s+.*\].*in\s+', code):
            issues.append(
                Issue(
                    title="Inefficient List Membership Test",
                    message="Testing membership in lists is O(n), consider using sets",
                    severity=Severity.MEDIUM,
                    issue_type=IssueType.PERFORMANCE,
                    line=1,
                    suggestion="Use a set for O(1) membership testing",
                )
            )
        return issues
