from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from resume_agent_automation.config.settings import PATHS


class ApprovedInputStore:
    def __init__(self, base_dir: str | Path | None = None):
        self.base_dir = Path(base_dir) if base_dir else PATHS.approved_input_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_approved_input(self, scenario_id: str, payload: dict[str, Any]) -> Path:
        file_path = self.base_dir / f"{scenario_id}.json"
        with file_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
        return file_path

    def load_approved_input(self, scenario_id: str) -> dict[str, Any]:
        file_path = self.base_dir / f"{scenario_id}.json"
        if not file_path.exists():
            return {}
        with file_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
