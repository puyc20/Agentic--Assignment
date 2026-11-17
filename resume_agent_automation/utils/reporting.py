from __future__ import annotations

import csv
import html
from pathlib import Path
from typing import Any, Iterable


def generate_html_report(results: Iterable[dict[str, Any]], output_path: str | Path) -> Path:
    rows = list(results)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    total = len(rows)
    passed = sum(1 for row in rows if row.get("overall_pass") is True)
    failed = total - passed

    rows_html = []
    for item in rows:
        metrics_html = "".join(
            f"<tr><td>{html.escape(str(item.get('test_id', '')))}</td><td>{html.escape(str(item.get('scenario', '')))}</td><td>{html.escape(metric_name)}</td><td>{score}</td><td>{threshold}</td><td>{'Pass' if passed else 'Fail'}</td><td>{html.escape(reason)}</td></tr>"
            for metric_name, score, threshold, passed, reason in [
                (
                    "Answer Relevancy",
                    item.get("answer_relevancy", {}).get("score", 0),
                    item.get("answer_relevancy", {}).get("threshold", 0),
                    item.get("answer_relevancy", {}).get("passed", False),
                    item.get("answer_relevancy", {}).get("reason", ""),
                ),
                (
                    "Faithfulness",
                    item.get("faithfulness", {}).get("score", 0),
                    item.get("faithfulness", {}).get("threshold", 0),
                    item.get("faithfulness", {}).get("passed", False),
                    item.get("faithfulness", {}).get("reason", ""),
                ),
                (
                    "Hallucination",
                    item.get("hallucination", {}).get("hallucination_risk", 0),
                    item.get("hallucination", {}).get("threshold", 0),
                    item.get("hallucination", {}).get("passed", False),
                    item.get("hallucination", {}).get("reason", ""),
                ),
            ]
        )
        rows_html.append(
            f"<tr><td>{html.escape(str(item.get('test_id', '')))}</td><td>{html.escape(str(item.get('scenario', '')))}</td><td>{'Pass' if item.get('overall_pass') else 'Fail'}</td><td>{len(item.get('answer_relevancy', {}))}</td></tr>"
        )

    html_report = f"""<!doctype html>
<html lang=\"en\">
  <head><meta charset=\"UTF-8\"><title>Resume Agent Evaluation Report</title></head>
  <body>
    <h1>Resume Agent Evaluation Report</h1>
    <p>Total Test Scenarios: {total}</p>
    <p>Passed: {passed}</p>
    <p>Failed: {failed}</p>
    <table border=\"1\" cellpadding=\"6\" cellspacing=\"0\">
      <thead>
        <tr><th>Test ID</th><th>Scenario</th><th>Overall Status</th><th>Metrics</th></tr>
      </thead>
      <tbody>
        {''.join(rows_html)}
      </tbody>
    </table>
    <h2>Metric Details</h2>
    <table border=\"1\" cellpadding=\"6\" cellspacing=\"0\">
      <thead><tr><th>Test ID</th><th>Scenario</th><th>Metric</th><th>Score</th><th>Threshold</th><th>Status</th><th>Reason</th></tr></thead>
      <tbody>{''.join(r for r in rows_html if False)}</tbody>
    </table>
  </body>
</html>"""
    output.write_text(html_report, encoding="utf-8")
    return output


def generate_csv_report(results: Iterable[dict[str, Any]], output_path: str | Path) -> Path:
    rows = list(results)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "test_id",
        "scenario",
        "overall_pass",
        "answer_relevancy_score",
        "answer_relevancy_threshold",
        "answer_relevancy_passed",
        "faithfulness_score",
        "faithfulness_threshold",
        "faithfulness_passed",
        "hallucination_consistency_score",
        "hallucination_risk",
        "hallucination_threshold",
        "hallucination_passed",
    ]

    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            answer = row.get("answer_relevancy", {})
            faith = row.get("faithfulness", {})
            hallucination = row.get("hallucination", {})
            writer.writerow(
                {
                    "test_id": row.get("test_id", ""),
                    "scenario": row.get("scenario", ""),
                    "overall_pass": row.get("overall_pass", False),
                    "answer_relevancy_score": answer.get("score", 0),
                    "answer_relevancy_threshold": answer.get("threshold", 0),
                    "answer_relevancy_passed": answer.get("passed", False),
                    "faithfulness_score": faith.get("score", 0),
                    "faithfulness_threshold": faith.get("threshold", 0),
                    "faithfulness_passed": faith.get("passed", False),
                    "hallucination_consistency_score": hallucination.get("consistency_score", 0),
                    "hallucination_risk": hallucination.get("hallucination_risk", 0),
                    "hallucination_threshold": hallucination.get("threshold", 0),
                    "hallucination_passed": hallucination.get("passed", False),
                }
            )
    return output
