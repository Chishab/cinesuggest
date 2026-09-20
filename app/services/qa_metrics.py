import csv
from collections import Counter
from pathlib import Path

QA_DIR = Path(__file__).resolve().parents[2] / "qa"


def read_csv(name):
    with (QA_DIR / name).open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def build_metrics():
    cases = read_csv("test_cases.csv")
    executions = read_csv("test_execution.csv")
    defects = read_csv("defects.csv")
    requirements = read_csv("requirements_traceability.csv")
    result_counts = Counter(row["Result"] for row in executions)
    severity_counts = Counter(row["Severity"] for row in defects)
    status_counts = Counter(row["Status"] for row in defects)
    automated = [row for row in executions if row["Browser"] == "pytest"]
    automated_passed = sum(row["Result"] == "PASS" for row in automated)
    covered = sum(bool(row["Test Case IDs"].strip()) for row in requirements)
    return {
        "total_tests": len(cases),
        "passed": result_counts["PASS"],
        "failed": result_counts["FAIL"],
        "blocked": result_counts["BLOCKED"],
        "not_run": result_counts["NOT RUN"],
        "pass_percentage": round(result_counts["PASS"] / len(executions) * 100, 1) if executions else 0,
        "fail_percentage": round(result_counts["FAIL"] / len(executions) * 100, 1) if executions else 0,
        "total_defects": len(defects),
        "open_defects": sum(row["Status"] not in {"Closed", "Rejected"} for row in defects),
        "closed_defects": status_counts["Closed"],
        "severity": dict(severity_counts),
        "statuses": dict(status_counts),
        "automation_total": len(automated),
        "automation_passed": automated_passed,
        "automation_failed": len(automated) - automated_passed,
        "automation_percentage": round(automated_passed / len(automated) * 100, 1) if automated else 0,
        "requirements_total": len(requirements),
        "requirements_covered": covered,
        "requirements_uncovered": len(requirements) - covered,
        "traceability_percentage": round(covered / len(requirements) * 100, 1) if requirements else 0,
    }
