from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class AppConfig:
    app_url: str = os.getenv("APP_URL", "https://dna-preprod.hashedin.com/home/me/")
    app_username: str = os.getenv("APP_USERNAME", "")
    app_password: str = os.getenv("APP_PASSWORD", "")
    headless: bool = os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() == "true"
    browser: str = os.getenv("PLAYWRIGHT_BROWSER", "chromium")
    resume_agent_enabled: bool = os.getenv("RESUME_AGENT_ENABLED", "false").lower() == "true"
    resume_agent_feature_path: str = os.getenv("RESUME_AGENT_FEATURE_PATH", "/profile")


@dataclass(frozen=True)
class OllamaConfig:
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model: str = os.getenv("OLLAMA_MODEL", "gemma2:2b")
    judge_model: str = os.getenv("OLLAMA_JUDGE_MODEL", "gemma2:2b")
    timeout_seconds: int = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "120"))
    temperature: float = 0.0


@dataclass(frozen=True)
class PathsConfig:
    project_root: Path = PROJECT_ROOT
    transcripts_dir: Path = PROJECT_ROOT / "transcripts"
    reports_dir: Path = PROJECT_ROOT / "reports"
    screenshots_dir: Path = PROJECT_ROOT / "screenshots"
    logs_dir: Path = PROJECT_ROOT / "logs"
    test_data_dir: Path = PROJECT_ROOT / "test_data"
    manual_cases_path: Path = PROJECT_ROOT / "test_data" / "manual_test_cases.xlsx"
    approved_input_dir: Path = PROJECT_ROOT / "test_data" / "approved_test_inputs"


APP = AppConfig()
OLLAMA = OllamaConfig()
PATHS = PathsConfig()


def ensure_directories() -> None:
    for directory in [
        PATHS.transcripts_dir,
        PATHS.reports_dir,
        PATHS.screenshots_dir,
        PATHS.screenshots_dir / "passed",
        PATHS.screenshots_dir / "failed",
        PATHS.logs_dir,
        PATHS.test_data_dir,
        PATHS.approved_input_dir,
    ]:
        directory.mkdir(parents=True, exist_ok=True)
