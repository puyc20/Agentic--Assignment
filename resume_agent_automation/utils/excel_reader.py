from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from openpyxl import load_workbook


def read_manual_test_cases(path: str | Path) -> list[dict[str, Any]]:
    workbook = load_workbook(path, data_only=True)
    sheet = workbook[workbook.sheetnames[0]]
    rows = list(sheet.iter_rows(values_only=True))
    if not rows:
        return []

    headers = [str(cell).strip() if cell is not None else "" for cell in rows[0]]
    data_rows = rows[1:]
    records: list[dict[str, Any]] = []
    for row in data_rows:
        if not any(cell is not None and str(cell).strip() for cell in row):
            continue
        record = {}
        for idx, header in enumerate(headers):
            value = row[idx] if idx < len(row) else None
            record[header] = value
        records.append(record)
    return records


def get_automation_candidates(cases: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for case in cases:
        automation_candidate = str(case.get("Automation Candidate", "No")).strip().lower()
        if automation_candidate.startswith("yes"):
            selected.append(case)
    return selected
