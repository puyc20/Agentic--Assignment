from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MetricResult:
    metric_name: str
    score: float
    threshold: float
    reason: str
    passed: bool
    raw_details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ScenarioEvaluation:
    test_id: str
    scenario_name: str
    ui_status: str
    functional_status: str
    metrics: list[MetricResult] = field(default_factory=list)
    transcript_path: str | None = None
    screenshot_path: str | None = None
    execution_duration: float | None = None
    final_status: str = "not_run"
