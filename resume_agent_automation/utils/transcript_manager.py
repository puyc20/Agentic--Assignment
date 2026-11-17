from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from resume_agent_automation.config.settings import PATHS


class TranscriptManager:
    def __init__(self, base_dir: str | Path | None = None):
        self.base_dir = Path(base_dir) if base_dir else PATHS.transcripts_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def create_transcript(self, test_id: str, scenario: str, payload: dict[str, Any]) -> Path:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        file_name = f"{test_id}_{scenario.replace(' ', '_')}_{timestamp}.json"
        file_path = self.base_dir / file_name
        transcript = {
            "test_id": test_id,
            "scenario": scenario,
            "execution_timestamp": timestamp,
            "conversation": [],
            **payload,
        }
        with file_path.open("w", encoding="utf-8") as handle:
            json.dump(transcript, handle, indent=2, ensure_ascii=False)
        return file_path

    def append_turn(self, file_path: str | Path, turn_number: int, role: str, text: str) -> None:
        file_path = Path(file_path)
        with file_path.open("r", encoding="utf-8") as handle:
            transcript = json.load(handle)

        transcript.setdefault("conversation", []).append(
            {
                "turn_number": turn_number,
                "role": role,
                "text": text,
            }
        )

        with file_path.open("w", encoding="utf-8") as handle:
            json.dump(transcript, handle, indent=2, ensure_ascii=False)

    def update_status(self, file_path: str | Path, status: str, **kwargs: Any) -> None:
        file_path = Path(file_path)
        with file_path.open("r", encoding="utf-8") as handle:
            transcript = json.load(handle)

        transcript["execution_status"] = status
        for key, value in kwargs.items():
            transcript[key] = value

        with file_path.open("w", encoding="utf-8") as handle:
            json.dump(transcript, handle, indent=2, ensure_ascii=False)
