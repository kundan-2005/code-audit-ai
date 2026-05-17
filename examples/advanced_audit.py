#!/usr/bin/env python3
"""Advanced usage example with custom configuration."""

from src.main import CodeAuditor
from src.models.config import AuditConfig
from src.models.issue import Severity


def main():
    """Run advanced audit example."""
    # Create custom configuration
    config = AuditConfig(
        check_security=True,
        check_performance=True,
        check_quality=True,
        check_functionality=True,
        severity_threshold="medium",  # Only show medium and above
        language="python",
        max_issues=50,
        timeout=30,
        verbose=True,
    )

    # Create auditor with custom config
    auditor = CodeAuditor(config=config)

    # Complex sample code
    code = '''
def complex_function(data):
    """Process data with multiple issues."""
    import requests  # Should be at top
    
    for item in data:
        query = "SELECT * FROM users WHERE id = " + str(item)
        
        # Nested loops
        for user in query:
            for entry in user:
                s = ""
                s += str(entry)  # Inefficient
    
    try:
        result = eval(input())
    except:
        pass
    
    return None
'''

    print("Running Advanced Audit")
    print("=" * 80)
    print(f"Configuration: {config}")
    print("=" * 80 + "\n")

    # Run audit
    result = auditor.audit(code, filename="complex.py")

    # Group issues by severity
    severity_groups = {}
    for issue in result.issues:
        if issue.severity not in severity_groups:
            severity_groups[issue.severity] = []
        severity_groups[issue.severity].append(issue)

    # Display grouped results
    print(f"Total issues found: {result.total_issues}")
    print(f"Filtered issues (severity >= {config.severity_threshold}): {len(result.issues)}\n")

    for severity in sorted(severity_groups.keys(), key=lambda x: x.value, reverse=True):
        issues = severity_groups[severity]
        print(f"\n{severity.name} ({len(issues)} issues):")
        print("-" * 40)
        for issue in issues:
            print(f"  • {issue.title}")
            print(f"    Message: {issue.message}")
            if issue.suggestion:
                print(f"    Fix: {issue.suggestion}")

    # Export result as JSON
    print("\n" + "=" * 80)
    print("Result as JSON:")
    print("=" * 80)
    print(result.to_json())


if __name__ == "__main__":
    main()
