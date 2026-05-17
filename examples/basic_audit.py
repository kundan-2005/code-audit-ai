#!/usr/bin/env python3
"""Basic usage example."""

from src.main import CodeAuditor


def main():
    """Run basic audit example."""
    # Create auditor
    auditor = CodeAuditor()

    # Sample code with various issues
    code = '''
def process_data(items):
    password = "secret123"
    api_key = "key_abc123"
    result = []
    
    for item in items:
        if item > 0:
            result.append(item * 2)
    
    return result


def unsafe_eval(user_input):
    return eval(user_input)
'''

    print("Auditing code...")
    print("-" * 80)

    # Run audit
    result = auditor.audit(code, filename="sample.py")

    # Display results
    print(f"\nTotal issues found: {result.total_issues}")
    print(f"Issues (after filtering): {len(result.issues)}\n")

    if result.issues:
        for issue in result.issues:
            print(f"[{issue.severity.name}] {issue.title}")
            print(f"  Type: {issue.issue_type}")
            print(f"  Message: {issue.message}")
            if issue.suggestion:
                print(f"  Suggestion: {issue.suggestion}")
            print()
    else:
        print("No issues found!")

    # Generate full report
    print("\n" + "=" * 80)
    print("FULL REPORT")
    print("=" * 80)
    report = auditor.generate_report(result)
    print(report)


if __name__ == "__main__":
    main()
