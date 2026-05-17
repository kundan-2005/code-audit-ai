"""Integration tests."""

import pytest
from src.main import CodeAuditor
from src.models.config import AuditConfig


class TestCodeAuditor:
    """Test CodeAuditor integration."""

    def test_basic_audit(self):
        """Test basic audit functionality."""
        auditor = CodeAuditor()
        code = '''
def process_data(items):
    result = []
    for item in items:
        if item > 0:
            result.append(item * 2)
    return result
'''
        result = auditor.audit(code)
        assert result is not None
        assert len(result) >= 0

    def test_custom_config(self):
        """Test with custom configuration."""
        config = AuditConfig(
            check_security=True,
            check_performance=True,
            check_quality=False,
            check_functionality=False,
        )
        auditor = CodeAuditor(config=config)
        code = 'password = "secret"'
        result = auditor.audit(code)
        assert result is not None

    def test_report_generation(self):
        """Test report generation."""
        auditor = CodeAuditor()
        code = 'eval(input())'
        result = auditor.audit(code)
        report = auditor.generate_report(result)
        assert "CODE AUDIT REPORT" in report
