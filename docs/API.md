# API Reference

## CodeAuditor

### Constructor

```python
CodeAuditor(config: Optional[AuditConfig] = None)
```

Initialize a CodeAuditor instance.

**Parameters:**
- `config`: Optional AuditConfig instance. Uses defaults if not provided.

**Example:**
```python
from src.main import CodeAuditor
auditor = CodeAuditor()
```

### Methods

#### audit(code: str, filename: Optional[str] = None) -> AuditResult

Audit provided code.

**Parameters:**
- `code`: Source code to audit
- `filename`: Optional filename for context

**Returns:** AuditResult containing all findings

**Raises:** ValueError if code is invalid

**Example:**
```python
code = "def hello(): return 'world'"
result = auditor.audit(code)
```

#### generate_report(result: AuditResult) -> str

Generate a text report from audit result.

**Parameters:**
- `result`: AuditResult to generate report from

**Returns:** Formatted report string

**Example:**
```python
report = auditor.generate_report(result)
print(report)
```

## AuditConfig

### Constructor

```python
AuditConfig(
    check_security: bool = True,
    check_performance: bool = True,
    check_quality: bool = True,
    check_functionality: bool = True,
    severity_threshold: Optional[str] = None,
    language: str = "python",
    max_issues: int = 100,
    timeout: int = 30,
    verbose: bool = False
)
```

**Parameters:**
- `check_security`: Enable security checks
- `check_performance`: Enable performance checks
- `check_quality`: Enable quality checks
- `check_functionality`: Enable functionality checks
- `severity_threshold`: Filter by severity ("low", "medium", "high", "critical", or None)
- `language`: Programming language (default: "python")
- `max_issues`: Maximum issues to report
- `timeout`: Audit timeout in seconds
- `verbose`: Enable verbose logging

## AuditResult

### Properties

- `code`: The audited code
- `issues`: List of Issue objects found
- `filename`: Optional filename
- `total_issues`: Total issues before filtering
- `config`: AuditConfig used
- `timestamp`: Audit timestamp

### Methods

#### to_dict() -> dict
Convert result to dictionary.

#### to_json() -> str
Convert result to JSON string.

#### has_critical_issues() -> bool
Check if result contains critical issues.

## Issue

### Constructor

```python
Issue(
    title: str,
    message: str,
    severity: Severity,
    issue_type: IssueType,
    line: int = 0,
    suggestion: str = None
)
```

**Parameters:**
- `title`: Short issue title
- `message`: Detailed description
- `severity`: Severity level (Severity enum)
- `issue_type`: Issue type (IssueType enum)
- `line`: Line number where issue occurs
- `suggestion`: Suggested fix

### Methods

#### to_dict() -> dict
Convert issue to dictionary.

## Severity Enum

```python
class Severity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
```

## IssueType Enum

```python
class IssueType(Enum):
    SECURITY = "security"
    PERFORMANCE = "performance"
    QUALITY = "quality"
    FUNCTIONALITY = "functionality"
```
