"""Code Audit AI - Multi-Agent Trust Verification System"""

__version__ = "1.0.0"
__author__ = "kundan-2005"
__description__ = "Multi-Agent Trust Verification System for AI-Generated Code"

from src.main import CodeAuditor
from src.models.config import AuditConfig
from src.models.audit_result import AuditResult
from src.models.issue import Issue, Severity

__all__ = [
    "CodeAuditor",
    "AuditConfig",
    "AuditResult",
    "Issue",
    "Severity",
]
