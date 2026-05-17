# Usage Examples

## Basic Usage

### Simple Audit

```python
from src.main import CodeAuditor

# Create auditor
auditor = CodeAuditor()

# Code to audit
code = """
def process_data(items):
    password = "secret123"
    result = []
    for item in items:
        if item > 0:
            result.append(item * 2)
    return result
"""

# Run audit
result = auditor.audit(code)

# View results
print(f"Issues found: {len(result.issues)}")
for issue in result.issues:
    print(f"- {issue.title} (Line {issue.line}): {issue.message}")
```

## Advanced Configuration

### Custom Configuration

```python
from src.main import CodeAuditor
from src.models.config import AuditConfig

# Create custom config
config = AuditConfig(
    check_security=True,
    check_performance=True,
    check_quality=True,
    check_functionality=True,
    severity_threshold="medium",  # Only show medium and above
    language="python",
    max_issues=50,
    timeout=30,
    verbose=True
)

# Create auditor with custom config
auditor = CodeAuditor(config=config)

# Audit code
result = auditor.audit(code)
```

## Report Generation

### Generate Text Report

```python
auditor = CodeAuditor()
result = auditor.audit(code)

# Generate report
report = auditor.generate_report(result)
print(report)
```

### Export to JSON

```python
import json

result = auditor.audit(code)
json_report = result.to_json()

# Save to file
with open('audit_report.json', 'w') as f:
    f.write(json_report)
```

## Filtering Results

### By Severity

```python
from src.models.issue import Severity

# Get only critical issues
critical = [issue for issue in result.issues 
            if issue.severity == Severity.CRITICAL]

# Get high and critical
high_priority = [issue for issue in result.issues 
                 if issue.severity.value >= Severity.HIGH.value]
```

### By Type

```python
from src.models.issue import IssueType

# Get only security issues
security_issues = [issue for issue in result.issues 
                   if issue.issue_type == IssueType.SECURITY]
```

## Batch Processing

### Audit Multiple Files

```python
import os
from pathlib import Path

auditor = CodeAuditor()
results = {}

# Process all Python files in directory
for py_file in Path('src').glob('**/*.py'):
    with open(py_file, 'r') as f:
        code = f.read()
    
    result = auditor.audit(code, filename=str(py_file))
    results[str(py_file)] = result
    
    print(f"Audited {py_file}: {len(result.issues)} issues")
```

## Error Handling

### Handle Invalid Input

```python
from src.main import CodeAuditor

auditor = CodeAuditor()

try:
    result = auditor.audit("")  # Empty code
except ValueError as e:
    print(f"Error: {e}")

try:
    result = auditor.audit("x" * 2000000)  # Too large
except ValueError as e:
    print(f"Error: {e}")
```

## Custom Analysis

### Extend with Custom Agent

```python
from src.agents.base_agent import BaseAgent
from src.models.issue import Issue, Severity, IssueType
from src.main import CodeAuditor

class CustomAgent(BaseAgent):
    def analyze(self, code, filename=None):
        issues = []
        # Your custom analysis
        if 'TODO' in code:
            issues.append(Issue(
                title="TODO Found",
                message="Code contains TODO comments",
                severity=Severity.LOW,
                issue_type=IssueType.QUALITY,
                suggestion="Address TODO before deployment"
            ))
        return issues

# Create extended auditor
class ExtendedAuditor(CodeAuditor):
    def __init__(self, config=None):
        super().__init__(config)
        self.custom_agent = CustomAgent(self.config)
    
    def audit(self, code, filename=None):
        result = super().audit(code, filename)
        custom_issues = self.custom_agent.analyze(code, filename)
        result.issues.extend(custom_issues)
        return result

# Use extended auditor
auditor = ExtendedAuditor()
result = auditor.audit(code)
```

## Integration with CI/CD

### GitHub Actions Example

```python
# scripts/audit_pr.py
import sys
from pathlib import Path
from src.main import CodeAuditor
from src.models.config import AuditConfig

def main():
    config = AuditConfig(
        severity_threshold="medium",
        verbose=True
    )
    
    auditor = CodeAuditor(config=config)
    has_issues = False
    
    for py_file in Path('.').glob('**/*.py'):
        if '.venv' in str(py_file):
            continue
        
        with open(py_file, 'r') as f:
            code = f.read()
        
        result = auditor.audit(code, filename=str(py_file))
        
        if result.has_critical_issues():
            print(f"CRITICAL ISSUES in {py_file}")
            has_issues = True
    
    return 1 if has_issues else 0

if __name__ == '__main__':
    sys.exit(main())
```
