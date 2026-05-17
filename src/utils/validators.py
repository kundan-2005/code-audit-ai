"""Input validation utilities."""

from src.models.config import AuditConfig
from src.utils.logger import get_logger

logger = get_logger(__name__)


def validate_code(code: str) -> bool:
    """Validate input code.

    Args:
        code: Code to validate

    Returns:
        True if valid

    Raises:
        ValueError: If code is invalid
    """
    if not isinstance(code, str):
        raise ValueError("Code must be a string")
    if len(code.strip()) == 0:
        raise ValueError("Code cannot be empty")
    if len(code) > 1000000:
        raise ValueError("Code is too large (max 1MB)")
    return True


def validate_config(config: AuditConfig) -> bool:
    """Validate audit configuration.

    Args:
        config: Configuration to validate

    Returns:
        True if valid

    Raises:
        ValueError: If config is invalid
    """
    if not isinstance(config, AuditConfig):
        raise ValueError("Config must be an AuditConfig instance")

    valid_severity = ["low", "medium", "high", "critical", None]
    if config.severity_threshold not in valid_severity:
        raise ValueError(
            f"Invalid severity threshold: {config.severity_threshold}. "
            f"Must be one of {valid_severity}"
        )

    if config.max_issues < 1:
        raise ValueError("max_issues must be at least 1")

    if config.timeout < 1:
        raise ValueError("timeout must be at least 1 second")

    return True
