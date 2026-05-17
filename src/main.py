"""Main CodeAuditor class for conducting code audits."""

from typing import Optional, List, Dict, Any
from src.models.config import AuditConfig
from src.models.audit_result import AuditResult
from src.models.issue import Issue, Severity
from src.agents.security_agent import SecurityAgent
from src.agents.performance_agent import PerformanceAgent
from src.agents.quality_agent import QualityAgent
from src.agents.functionality_agent import FunctionalityAgent
from src.utils.logger import get_logger
from src.utils.validators import validate_code, validate_config

logger = get_logger(__name__)


class CodeAuditor:
    """Main auditor class that orchestrates multiple agents."""

    def __init__(self, config: Optional[AuditConfig] = None):
        """Initialize CodeAuditor.

        Args:
            config: Optional AuditConfig. Uses default if not provided.
        """
        self.config = config or AuditConfig()
        validate_config(self.config)
        logger.info(f"CodeAuditor initialized with config: {self.config}")

        # Initialize agents
        self.security_agent = SecurityAgent(self.config)
        self.performance_agent = PerformanceAgent(self.config)
        self.quality_agent = QualityAgent(self.config)
        self.functionality_agent = FunctionalityAgent(self.config)

    def audit(self, code: str, filename: Optional[str] = None) -> AuditResult:
        """Audit provided code.

        Args:
            code: Source code to audit
            filename: Optional filename for context

        Returns:
            AuditResult containing all findings
        """
        logger.info(f"Starting audit for {filename or 'code'}")
        validate_code(code)

        issues: List[Issue] = []

        try:
            # Run security analysis
            if self.config.check_security:
                logger.debug("Running security analysis...")
                security_issues = self.security_agent.analyze(code, filename)
                issues.extend(security_issues)

            # Run performance analysis
            if self.config.check_performance:
                logger.debug("Running performance analysis...")
                perf_issues = self.performance_agent.analyze(code, filename)
                issues.extend(perf_issues)

            # Run quality analysis
            if self.config.check_quality:
                logger.debug("Running quality analysis...")
                quality_issues = self.quality_agent.analyze(code, filename)
                issues.extend(quality_issues)

            # Run functionality verification
            if self.config.check_functionality:
                logger.debug("Running functionality verification...")
                func_issues = self.functionality_agent.analyze(code, filename)
                issues.extend(func_issues)

        except Exception as e:
            logger.error(f"Error during audit: {str(e)}", exc_info=True)
            raise

        # Filter issues by severity threshold
        filtered_issues = self._filter_issues(issues)

        # Create result
        result = AuditResult(
            code=code,
            filename=filename,
            issues=filtered_issues,
            total_issues=len(issues),
            config=self.config
        )

        logger.info(f"Audit completed. Found {len(filtered_issues)} issues (total: {len(issues)})")
        return result

    def _filter_issues(self, issues: List[Issue]) -> List[Issue]:
        """Filter issues by severity threshold.

        Args:
            issues: List of issues to filter

        Returns:
            Filtered list of issues
        """
        if not self.config.severity_threshold:
            return issues

        threshold_level = Severity[self.config.severity_threshold.upper()].value
        return [issue for issue in issues if issue.severity.value >= threshold_level]

    def generate_report(self, result: AuditResult) -> str:
        """Generate a text report from audit result.

        Args:
            result: AuditResult to generate report from

        Returns:
            Formatted report string
        """
        lines = [
            "="*80,
            "CODE AUDIT REPORT",
            "="*80,
            f"\nFile: {result.filename or 'N/A'}",
            f"Total Issues Found: {result.total_issues}",
            f"Issues (after filtering): {len(result.issues)}",
            f"\nSeverity Threshold: {self.config.severity_threshold or 'None'}",
            "\n" + "-"*80,
        ]

        if not result.issues:
            lines.append("No issues found!\n")
        else:
            lines.append(f"\nIssues by Severity:\n")
            severity_groups = self._group_issues_by_severity(result.issues)
            for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
                if severity in severity_groups:
                    lines.append(f"\n{severity.name} ({len(severity_groups[severity])})")
                    for issue in severity_groups[severity]:
                        lines.append(f"  - {issue.title}")
                        lines.append(f"    Line: {issue.line}")
                        lines.append(f"    Message: {issue.message}")
                        if issue.suggestion:
                            lines.append(f"    Suggestion: {issue.suggestion}")
                        lines.append("")

        lines.append("="*80)
        return "\n".join(lines)

    def _group_issues_by_severity(self, issues: List[Issue]) -> Dict[Severity, List[Issue]]:
        """Group issues by severity level.

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
