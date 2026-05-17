"""Functionality verification agent."""

from typing import List, Optional
from src.agents.base_agent import BaseAgent
from src.models.issue import Issue, Severity, IssueType
from src.utils.logger import get_logger
import re

logger = get_logger(__name__)


class FunctionalityAgent(BaseAgent):
    """Agent for functionality verification."""

    def analyze(self, code: str, filename: Optional[str] = None) -> List[Issue]:
        """Analyze code for functionality issues.

        Args:
            code: Source code to analyze
            filename: Optional filename

        Returns:
            List of functionality issues found
        """
        issues: List[Issue] = []

        # Check for unreachable code
        issues.extend(self._check_unreachable_code(code))

        # Check for variable usage
        issues.extend(self._check_unused_variables(code))

        # Check for exception handling
        issues.extend(self._check_exception_handling(code))

        # Check for return statements
        issues.extend(self._check_return_consistency(code))

        self._log_analysis("FunctionalityAgent", len(issues))
        return issues

    def _check_unreachable_code(self, code: str) -> List[Issue]:
        """Check for unreachable code after return/break."""
        issues = []
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if re.search(r'\s*(return|break|continue)\s*', line):
                # Check next lines for non-empty code
                for j in range(i + 1, min(i + 5, len(lines))):
                    if lines[j].strip() and not lines[j].strip().startswith('#'):
                        if not lines[j].strip().startswith('except') and not lines[j].strip().startswith('else'):
                            issues.append(
                                Issue(
                                    title="Unreachable Code",
                                    message="Code after return/break statement",
                                    severity=Severity.MEDIUM,
                                    issue_type=IssueType.FUNCTIONALITY,
                                    line=j + 1,
                                    suggestion="Remove unreachable code or adjust control flow",
                                )
                            )
                            break
        return issues

    def _check_unused_variables(self, code: str) -> List[Issue]:
        """Check for unused variables."""
        issues = []
        lines = code.split('\n')
        # Simple pattern matching for unused variables
        for i, line in enumerate(lines):
            if '_' in line and '=' in line and not line.strip().startswith('#'):
                if '_=' in line:
                    issues.append(
                        Issue(
                            title="Unused Variable Assignment",
                            message="Variable assigned but never used",
                            severity=Severity.LOW,
                            issue_type=IssueType.FUNCTIONALITY,
                            line=i + 1,
                            suggestion="Remove unused assignment or use the variable",
                        )
                    )
        return issues

    def _check_exception_handling(self, code: str) -> List[Issue]:
        """Check for bare except clauses."""
        issues = []
        if 'except:' in code:
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if re.search(r'except\s*:', line):
                    issues.append(
                        Issue(
                            title="Bare Exception Handler",
                            message="Bare 'except:' catches all exceptions including system exits",
                            severity=Severity.MEDIUM,
                            issue_type=IssueType.FUNCTIONALITY,
                            line=i + 1,
                            suggestion="Specify exception types: 'except Exception:' or more specific",
                        )
                    )
        return issues

    def _check_return_consistency(self, code: str) -> List[Issue]:
        """Check for inconsistent return types."""
        issues = []
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if re.search(r'^\s*def\s+\w+', line):
                returns_value = False
                returns_none = False
                for j in range(i + 1, len(lines)):
                    if re.search(r'^\s*def\s+', lines[j]):
                        break
                    if 'return' in lines[j]:
                        if re.search(r'return\s*$', lines[j]):
                            returns_none = True
                        else:
                            returns_value = True

                if returns_value and returns_none:
                    issues.append(
                        Issue(
                            title="Inconsistent Returns",
                            message="Function returns both values and None",
                            severity=Severity.LOW,
                            issue_type=IssueType.FUNCTIONALITY,
                            line=i + 1,
                            suggestion="Ensure consistent return types throughout function",
                        )
                    )
        return issues
