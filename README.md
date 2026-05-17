# Code Audit AI

🤖 **Multi-Agent Trust Verification System for AI-Generated Code**

Code Audit AI is an intelligent code analysis and verification system that uses multiple specialized AI agents to audit, verify, and ensure the quality and security of AI-generated code.

## Features

✅ **Multi-Agent Architecture** - Specialized agents for different audit aspects
- **Security Agent** - Identifies vulnerabilities and security issues
- **Performance Agent** - Detects performance bottlenecks and optimizations
- **Quality Agent** - Analyzes code quality, style, and best practices
- **Functionality Agent** - Verifies code functionality and correctness

✅ **Comprehensive Code Analysis**
- Static code analysis
- Security vulnerability detection
- Performance optimization suggestions
- Code quality metrics
- Best practices validation

✅ **Flexible Configuration**
- Customizable audit rules
- Severity level filtering
- Report generation

✅ **Easy Integration**
- Simple API
- Python library
- CLI support

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/kundan-2005/code-audit-ai.git
cd code-audit-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from src.main import CodeAuditor
from src.models.config import AuditConfig

# Create auditor with default config
auditor = CodeAuditor()

# Audit code
code = """
def process_data(items):
    result = []
    for item in items:
        if item > 0:
            result.append(item * 2)
    return result
"""

audit_result = auditor.audit(code)
print(audit_result)
```

### Advanced Usage

```python
from src.main import CodeAuditor
from src.models.config import AuditConfig

# Create custom config
config = AuditConfig(
    check_security=True,
    check_performance=True,
    check_quality=True,
    check_functionality=True,
    severity_threshold="medium",
    language="python"
)

# Create auditor with custom config
auditor = CodeAuditor(config=config)

# Audit code
audit_result = auditor.audit(code)

# Generate report
report = auditor.generate_report(audit_result)
print(report)
```

## Usage Examples

See the `examples/` directory for more usage examples:
- `basic_audit.py` - Basic usage
- `advanced_audit.py` - Advanced configuration
- `batch_audit.py` - Batch processing

## Project Structure

```
code-audit-ai/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Main CodeAuditor class
│   ├── models/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration models
│   │   ├── audit_result.py     # Result models
│   │   └── issue.py            # Issue and Severity enums
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py       # Abstract base agent
│   │   ├── security_agent.py   # Security analysis
│   │   ├── performance_agent.py # Performance analysis
│   │   ├── quality_agent.py    # Quality analysis
│   │   └── functionality_agent.py # Functionality verification
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # Logging utilities
│       ├── validators.py       # Input validation
│       └── helpers.py          # Helper functions
├── tests/
│   ├── __init__.py
│   ├── test_agents.py          # Agent tests
│   └── test_integration.py     # Integration tests
├── docs/
│   ├── ARCHITECTURE.md         # System architecture
│   ├── AGENTS.md               # Agent documentation
│   ├── API.md                  # API reference
│   └── EXAMPLES.md             # Usage examples
├── examples/
│   ├── basic_audit.py
│   ├── advanced_audit.py
│   └── batch_audit.py
├── requirements.txt
├── setup.py
├── LICENSE
└── README.md
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design and architecture
- [Agents](docs/AGENTS.md) - Detailed agent documentation
- [API Reference](docs/API.md) - Complete API reference
- [Examples](docs/EXAMPLES.md) - Usage examples and tutorials

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_agents.py

# Run with verbose output
pytest -v
```

## Configuration

Customize behavior through `AuditConfig`:

```python
from src.models.config import AuditConfig

config = AuditConfig(
    check_security=True,          # Enable security checks
    check_performance=True,       # Enable performance checks
    check_quality=True,           # Enable quality checks
    check_functionality=True,     # Enable functionality checks
    severity_threshold="medium", # Filter by severity: low, medium, high, critical
    language="python",           # Code language
    max_issues=100,              # Maximum issues to report
    timeout=30                    # Audit timeout in seconds
)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Support

For questions or support, please open an issue on the GitHub repository.

## Roadmap

- [ ] Support for multiple programming languages
- [ ] Integration with CI/CD pipelines
- [ ] Web UI for audit reports
- [ ] API server
- [ ] Batch processing improvements
- [ ] Custom rule engine

## Changelog

### v1.0.0 (2026-05-17)
- Initial release
- Multi-agent architecture
- Security, performance, quality, and functionality analysis
- Comprehensive reporting
