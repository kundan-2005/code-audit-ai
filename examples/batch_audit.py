#!/usr/bin/env python3
"""Batch processing example."""

from pathlib import Path
from src.main import CodeAuditor
from src.models.config import AuditConfig
import json


def audit_directory(directory: str = "src", output_file: str = "audit_results.json"):
    """Audit all Python files in directory.

    Args:
        directory: Directory to audit
        output_file: Output file for results
    """
    # Create auditor
    config = AuditConfig(
        severity_threshold="low",
        verbose=False,
    )
    auditor = CodeAuditor(config=config)

    # Collect results
    all_results = {}
    total_issues = 0

    print(f"Auditing Python files in '{directory}'...")
    print("=" * 80)

    # Find and audit all Python files
    py_files = list(Path(directory).glob("**/*.py"))
    print(f"Found {len(py_files)} Python files\n")

    for py_file in py_files:
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                code = f.read()

            # Run audit
            result = auditor.audit(code, filename=str(py_file))

            # Store result
            all_results[str(py_file)] = {
                "total_issues": result.total_issues,
                "filtered_issues": len(result.issues),
                "issues": [issue.to_dict() for issue in result.issues],
                "timestamp": result.timestamp,
            }

            total_issues += result.total_issues

            # Print summary
            if result.issues:
                print(f"✓ {py_file}: {len(result.issues)} issues")
            else:
                print(f"✓ {py_file}: OK")

        except Exception as e:
            print(f"✗ {py_file}: Error - {str(e)}")
            all_results[str(py_file)] = {"error": str(e)}

    # Print summary
    print("\n" + "=" * 80)
    print(f"Total issues across all files: {total_issues}")
    print(f"Files with issues: {sum(1 for r in all_results.values() if r.get('issues'))}")

    # Save results to file
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"Results saved to {output_file}")

    return all_results


if __name__ == "__main__":
    # Run batch audit on src directory
    results = audit_directory("src", "audit_results.json")

    # Print sample result
    if results:
        first_file = list(results.keys())[0]
        print(f"\nSample result for {first_file}:")
        print(json.dumps(results[first_file], indent=2))
