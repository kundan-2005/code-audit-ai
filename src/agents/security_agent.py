"""Security analysis agent."""

from typing import List, Optional
from src.agents.base_agent import BaseAgent
from src.models.issue import Issue, Severity, IssueType
from src.utils.logger import get_logger
import re

logger = get_logger(__name__)


class SecurityAgent(BaseAgent):
    """Agent for security vulnerability analysis."""

    def analyze(self, code: str, filename: Optional[str] = None) -> List[Issue]:
        """Analyze code for security vulnerabilities.

        Args:
            code: Source code to analyze
            filename: Optional filename

        Returns:
            List of security issues found
        """
        issues: List[Issue] = []

        # Check for hardcoded credentials
        issues.extend(self._check_hardcoded_credentials(code))

        # Check for SQL injection vulnerabilities
        issues.extend(self._check_sql_injection(code))

        # Check for insecure random
        issues.extend(self._check_insecure_random(code))

        # Check for use of eval
        issues.extend(self._check_eval_usage(code))

        # Check for insecure deserialization
        issues.extend(self._check_insecure_deserialization(code))

        self._log_analysis("SecurityAgent", len(issues))
        return issues

    def _check_hardcoded_credentials(self, code: str) -> List[Issue]:
        """Check for hardcoded credentials."""
        issues = []
        patterns = [
            (r'password\s*=\s*["\'](?!\{|\$)[^"\']]+["\']', "Hardcoded password detected"),
            (r'api[_-]?key\s*=\s*["\'](?!\{|\$)[^"\']]+["\']', "Hardcoded API key detected"),
            (r'secret\s*=\s*["\'](?!\{|\$)[^"\']]+["\']', "Hardcoded secret detected"),
        ]

        for pattern, message in patterns:
            for match in re.finditer(pattern, code, re.IGNORECASE):
                line_num = code[:match.start()].count('\n') + 1
                issues.append(
                    Issue(
                        title="Hardcoded Credentials",
                        message=message,
                        severity=Severity.CRITICAL,
                        issue_type=IssueType.SECURITY,
                        line=line_num,
                        suggestion="Use environment variables or configuration files",
                    )
                )

        return issues

    def _check_sql_injection(self, code: str) -> List[Issue]:
        """Check for SQL injection vulnerabilities."""
        issues = []
        # Look for string concatenation in SQL queries
        pattern = r'(query|sql)\s*=\s*["\'].*\+|execute\s*\(\s*["\'].*\+'

        for match in re.finditer(pattern, code, re.IGNORECASE):
            line_num = code[:match.start()].count('\n') + 1
            issues.append(
                Issue(
                    title="Potential SQL Injection",
                    message="SQL query concatenation detected",
                    severity=Severity.HIGH,
                    issue_type=IssueType.SECURITY,
                    line=line_num,
                    suggestion="Use parameterized queries or prepared statements",
                )
            )

        return issues

    def _check_insecure_random(self, code: str) -> List[Issue]:
        """Check for insecure random usage."""
        issues = []
        if "random.random()" in code or "random.choice" in code:
            line_num = code.find("random.") // len(code.split('\n')[0]) if code else 0
            issues.append(
                Issue(
                    title="Insecure Random Usage",
                    message="Using non-cryptographic random function",
                    severity=Severity.MEDIUM,
                    issue_type=IssueType.SECURITY,
                    line=line_num,
                    suggestion="Use secrets or cryptographic random for security purposes",
                )
            )
        return issues

    def _check_eval_usage(self, code: str) -> List[Issue]:
        """Check for eval usage."""
        issues = []
        if "eval(" in code:
            line_num = code.find("eval(") // len(code.split('\n')[0]) if code else 0
            issues.append(
                Issue(
                    title="Dangerous eval() Usage",
                    message="eval() can execute arbitrary code",
                    severity=Severity.CRITICAL,
                    issue_type=IssueType.SECURITY,
                    line=line_num,
                    suggestion="Avoid eval(), use safer alternatives like ast.literal_eval()",
                )
            )
        return issues

    def _check_insecure_deserialization(self, code: str) -> List[Issue]:
        """Check for insecure deserialization."""
        issues = []
        if "pickle.loads" in code:
            line_num = code.find("pickle.loads") // len(code.split('\n')[0]) if code else 0
            issues.append(
                Issue(
                    title="Insecure Deserialization",
                    message="pickle.loads() can execute arbitrary code",
                    severity=Severity.HIGH,
                    issue_type=IssueType.SECURITY,
                    line=line_num,
                    suggestion="Use safer serialization like JSON or use restricted unpickling",
                )
            )
        return issues
