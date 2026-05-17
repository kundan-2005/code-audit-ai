# Agents Documentation

## Overview

Each agent is specialized in analyzing different aspects of code. They inherit from `BaseAgent` and implement the `analyze()` method.

## SecurityAgent

### Checks Performed

1. **Hardcoded Credentials**
   - Severity: CRITICAL
   - Detects passwords, API keys, secrets
   - Pattern matching with regex

2. **SQL Injection Vulnerabilities**
   - Severity: HIGH
   - Detects string concatenation in SQL queries
   - Suggests parameterized queries

3. **Insecure Random**
   - Severity: MEDIUM
   - Detects non-cryptographic random usage
   - Suggests cryptographic alternatives

4. **Dangerous eval()**
   - Severity: CRITICAL
   - Detects eval() usage
   - Extremely dangerous for security

5. **Insecure Deserialization**
   - Severity: HIGH
   - Detects pickle.loads() usage
   - Suggests safer alternatives

## PerformanceAgent

### Checks Performed

1. **Nested Loops**
   - Severity: MEDIUM
   - O(n²) or worse complexity
   - Suggests optimization

2. **String Concatenation**
   - Severity: MEDIUM
   - Using += for strings is O(n)
   - Suggests ''.join() or f-strings

3. **Imports in Loops**
   - Severity: LOW
   - Repeated module loading
   - Move to module level

4. **Inefficient List Operations**
   - Severity: MEDIUM
   - List membership testing is O(n)
   - Use sets for O(1) lookup

## QualityAgent

### Checks Performed

1. **Missing Docstrings**
   - Severity: LOW
   - Functions without documentation
   - Suggests adding docstrings

2. **Long Functions**
   - Severity: LOW
   - Functions over 50 lines
   - Suggests refactoring

3. **Complex Conditionals**
   - Severity: LOW
   - More than 3 logical operators
   - Suggests breaking into smaller parts

4. **Magic Numbers**
   - Severity: LOW
   - Unexplained numeric literals
   - Define as named constants

5. **Naming Conventions**
   - Severity: LOW
   - Single letter variable names
   - Use descriptive names

## FunctionalityAgent

### Checks Performed

1. **Unreachable Code**
   - Severity: MEDIUM
   - Code after return/break statements
   - Remove or fix control flow

2. **Unused Variables**
   - Severity: LOW
   - Variables assigned but not used
   - Remove or use the variable

3. **Bare Exception Handlers**
   - Severity: MEDIUM
   - Bare except: catches all exceptions
   - Specify exception types

4. **Inconsistent Returns**
   - Severity: LOW
   - Function returns both values and None
   - Ensure consistent return types

## Custom Implementation

To create a custom agent:

```python
from src.agents.base_agent import BaseAgent
from src.models.issue import Issue, Severity, IssueType

class CustomAgent(BaseAgent):
    def analyze(self, code: str, filename: str = None) -> List[Issue]:
        issues = []
        # Your analysis logic here
        return issues
```

## Agent Integration

Add custom agent to CodeAuditor:

```python
from src.main import CodeAuditor

class CodeAuditorExtended(CodeAuditor):
    def __init__(self, config):
        super().__init__(config)
        self.custom_agent = CustomAgent(config)
    
    def audit(self, code, filename=None):
        result = super().audit(code, filename)
        custom_issues = self.custom_agent.analyze(code, filename)
        result.issues.extend(custom_issues)
        return result
```
