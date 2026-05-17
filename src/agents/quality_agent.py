"""Code quality analysis agent."""

from typing import List, Optional
from src.agents.base_agent import BaseAgent
from src.models.issue import Issue, Severity, IssueType
from src.utils.logger import get_logger
import re

logger = get_logger(__name__)


class QualityAgent(BaseAgent):
    """Agent for code quality analysis."""

    def analyze(self, code: str, filename: Optional[str] = None) -> List[Issue]:
        """Analyze code for quality issues.

        Args:
            code: Source code to analyze
            filename: Optional filename

        Returns:
            List of quality issues found
        """
        issues: List[Issue] = []

        # Check for missing docstrings
        issues.extend(self._check_missing_docstrings(code))

        # Check for long functions
        issues.extend(self._check_long_functions(code))

        # Check for complex conditionals
        issues.extend(self._check_complex_conditionals(code))

        # Check for magic numbers
        issues.extend(self._check_magic_numbers(code))

        # Check for naming conventions
        issues.extend(self._check_naming_conventions(code))

        self._log_analysis("QualityAgent", len(issues))
        return issues

    def _check_missing_docstrings(self, code: str) -> List[Issue]:
        """Check for missing docstrings."""
        issues = []
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if re.search(r'^\s*def\s+\w+\s*\(', line):
                # Check if next non-empty line is a docstring
                for j in range(i + 1, min(i + 5, len(lines))):
                    if lines[j].strip():
                        if not (lines[j].strip().startswith('"""') or lines[j].strip().startswith("'''")):
                            issues.append(
                                Issue(
                                    title="Missing Docstring",
                                    message="Function lacks documentation",
                                    severity=Severity.LOW,
                                    issue_type=IssueType.QUALITY,
                                    line=i + 1,
                                    suggestion="Add a docstring describing the function purpose",
                                )
                            )
                        break
        return issues

    def _check_long_functions(self, code: str) -> List[Issue]:
        """Check for functions longer than 50 lines."""
        issues = []
        lines = code.split('\n')
        in_function = False
        func_start = 0
        func_name = ""

        for i, line in enumerate(lines):
            if re.search(r'^\s*def\s+(\w+)\s*\(', line):
                if in_function:
                    func_length = i - func_start
                    if func_length > 50:
                        issues.append(
                            Issue(
                                title="Long Function",
                                message=f"Function '{func_name}' is {func_length} lines long",
                                severity=Severity.LOW,
                                issue_type=IssueType.QUALITY,
                                line=func_start + 1,
                                suggestion="Consider refactoring into smaller functions",
                            )
                        )
                in_function = True
                func_start = i
                func_name = re.search(r'def\s+(\w+)', line).group(1)

        return issues

    def _check_complex_conditionals(self, code: str) -> List[Issue]:
        """Check for overly complex conditional statements."""
        issues = []
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if re.search(r'if\s+', line):
                and_count = line.count(' and ')
                or_count = line.count(' or ')
                if and_count + or_count > 3:
                    issues.append(
                        Issue(
                            title="Complex Conditional",
                            message="Conditional statement is too complex",
                            severity=Severity.LOW,
                            issue_type=IssueType.QUALITY,
                            line=i + 1,
                            suggestion="Break complex conditions into smaller, readable parts",
                        )
                    )
        return issues

    def _check_magic_numbers(self, code: str) -> List[Issue]:
        """Check for magic numbers (unexplained numeric literals)."""
        issues = []
        # Simple pattern: look for numeric literals not in comments or strings
        pattern = r'(?<![a-zA-Z])\b(10|100|1000|256|512|1024)\b(?![a-zA-Z])'
        for match in re.finditer(pattern, code):
            line_num = code[:match.start()].count('\n') + 1
            issues.append(
                Issue(
                    title="Magic Number",
                    message=f"Unexplained number: {match.group(1)}",
                    severity=Severity.LOW,
                    issue_type=IssueType.QUALITY,
                    line=line_num,
                    suggestion="Define as a named constant for clarity",
                )
            )
        return issues

    def _check_naming_conventions(self, code: str) -> List[Issue]:
        """Check for naming convention violations."""
        issues = []
        # Check for single letter variable names in functions
        pattern = r'\s([a-z])\s*='
        for match in re.finditer(pattern, code):
            if match.group(1) not in ['i', 'j', 'k', 'x', 'y', 'z']:
                line_num = code[:match.start()].count('\n') + 1
                issues.append(
                    Issue(
                        title="Poor Variable Naming",
                        message=f"Single letter variable name: {match.group(1)}",
                        severity=Severity.LOW,
                        issue_type=IssueType.QUALITY,
                        line=line_num,
                        suggestion="Use descriptive variable names",
                    )
                )
        return issues
