import html
from datetime import date
from pathlib import Path

from app.services.qa_metrics import build_metrics


REPORT_DIR = Path(__file__).resolve().parents[1] / "reports"


def metric_rows(metrics):
    labels = {
        "total_tests": "Manual test cases",
        "passed": "Passed executions",
        "failed": "Failed executions",
        "blocked": "Blocked executions",
        "not_run": "Not run executions",
        "pass_percentage": "Pass percentage",
        "total_defects": "Total defects",
        "open_defects": "Open defects",
        "closed_defects": "Closed defects",
        "automation_total": "Automated executions",
        "automation_passed": "Automation passed",
        "automation_percentage": "Automation pass percentage",
        "requirements_covered": "Requirements covered",
        "requirements_uncovered": "Requirements not covered",
        "traceability_percentage": "Traceability percentage",
    }
    return "".join(f"<tr><th>{label}</th><td>{metrics[key]}</td></tr>" for key, label in labels.items())


def render(title, heading, summary, metrics):
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{html.escape(title)}</title><style>body{{font:16px system-ui;max-width:900px;margin:40px auto;color:#17212b}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #ddd;padding:10px;text-align:left}}th{{background:#f6f1e9}}h1{{color:#e4572e}}</style></head><body><p>CineSuggest QA</p><h1>{html.escape(heading)}</h1><p>Testing period: 2026-09-20 | Environment: Local Python/Flask</p><p>{html.escape(summary)}</p><table>{metric_rows(metrics)}</table></body></html>"""


metrics = build_metrics()
REPORT_DIR.mkdir(exist_ok=True)
reports = {
    "test_execution_report.html": ("Test Execution Report", "Test execution report", "Execution metrics derived from qa/test_execution.csv."),
    "defect_report.html": ("Defect Summary Report", "Defect summary report", "Defect metrics derived from qa/defects.csv. DEMO-001 is explicitly marked as demonstration data."),
    "qa_summary.html": ("QA Summary Report", "QA summary report", "Combined quality summary with traceability and automation metrics."),
}
for filename, content in reports.items():
    (REPORT_DIR / filename).write_text(render(*content, metrics), encoding="utf-8")
print(f"Generated {len(reports)} reports in {REPORT_DIR}")
