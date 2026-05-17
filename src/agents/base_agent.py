"""Base agent class."""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.issue import Issue
from src.models.config import AuditConfig
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(self, config: AuditConfig):
        """Initialize base agent.

        Args:
            config: Audit configuration
        """
        self.config = config
        logger.debug(f"Initializing {self.__class__.__name__}")

    @abstractmethod
    def analyze(self, code: str, filename: Optional[str] = None) -> List[Issue]:
        """Analyze code and return list of issues.

        Args:
            code: Source code to analyze
            filename: Optional filename for context

        Returns:
            List of Issue objects found
        """
        pass

    def _log_analysis(self, agent_name: str, issues_count: int):
        """Log analysis results.

        Args:
            agent_name: Name of the analyzing agent
            issues_count: Number of issues found
        """
        logger.debug(f"{agent_name} found {issues_count} issues")
