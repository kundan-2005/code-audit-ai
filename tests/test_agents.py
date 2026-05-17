"""Unit tests for agents."""

import pytest
from src.agents.security_agent import SecurityAgent
from src.agents.performance_agent import PerformanceAgent
from src.agents.quality_agent import QualityAgent
from src.agents.functionality_agent import FunctionalityAgent
from src.models.config import AuditConfig
from src.models.issue import Severity, IssueType


@pytest.fixture
def config():
    """Create test config."""
    return AuditConfig()


class TestSecurityAgent:
    """Test SecurityAgent."""

    def test_hardcoded_credentials(self, config):
        """Test hardcoded credentials detection."""
        agent = SecurityAgent(config)
        code = 'password = "secret123"'
        issues = agent.analyze(code)
        assert len(issues) > 0
        assert any(issue.severity == Severity.CRITICAL for issue in issues)

    def test_eval_usage(self, config):
        """Test eval() detection."""
        agent = SecurityAgent(config)
        code = 'result = eval(user_input)'
        issues = agent.analyze(code)
        assert len(issues) > 0
        assert any(issue.severity == Severity.CRITICAL for issue in issues)


class TestPerformanceAgent:
    """Test PerformanceAgent."""

    def test_string_concatenation(self, config):
        """Test inefficient string concatenation detection."""
        agent = PerformanceAgent(config)
        code = 's = "" \n s += "hello"'
        issues = agent.analyze(code)
        assert len(issues) > 0


class TestQualityAgent:
    """Test QualityAgent."""

    def test_missing_docstring(self, config):
        """Test missing docstring detection."""
        agent = QualityAgent(config)
        code = 'def foo(x):\n    return x * 2'
        issues = agent.analyze(code)
        assert len(issues) > 0


class TestFunctionalityAgent:
    """Test FunctionalityAgent."""

    def test_bare_except(self, config):
        """Test bare except detection."""
        agent = FunctionalityAgent(config)
        code = 'try:\n    pass\nexcept:\n    pass'
        issues = agent.analyze(code)
        assert len(issues) > 0
