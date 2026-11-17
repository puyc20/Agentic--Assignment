from __future__ import annotations

import json
from typing import Any

import ollama

from resume_agent_automation.config.settings import OLLAMA
from resume_agent_automation.utils.logger import get_logger

logger = get_logger(__name__)


class OllamaClient:
    def __init__(self, model: str | None = None, base_url: str | None = None, timeout: int | None = None):
        self.model = model or OLLAMA.model
        self.base_url = base_url or OLLAMA.base_url
        self.timeout = timeout or OLLAMA.timeout_seconds

    def is_available(self) -> bool:
        try:
            models = ollama.list()
            available = [m.model for m in models.get("models", [])]
            logger.info("Available Ollama models: %s", available)
            return self.model in available
        except Exception as exc:  # pragma: no cover - health check guard
            logger.exception("Ollama availability check failed: %s", exc)
            return False

    def generate(self, prompt: str, *, system_prompt: str | None = None, temperature: float | None = None, **kwargs: Any) -> dict[str, Any]:
        if not self.is_available():
            raise RuntimeError(f"Configured Ollama model '{self.model}' is not available on {self.base_url}")

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature if temperature is not None else OLLAMA.temperature},
        }
        if system_prompt:
            payload["system"] = system_prompt
        payload.update(kwargs)
        response = ollama.generate(**payload, timeout=self.timeout)
        logger.info("Ollama generation used model '%s'", self.model)
        return response

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> dict[str, Any]:
        if not self.is_available():
            raise RuntimeError(f"Configured Ollama model '{self.model}' is not available on {self.base_url}")
        response = ollama.chat(
            model=self.model,
            messages=messages,
            stream=False,
            options={"temperature": OLLAMA.temperature},
            **kwargs,
        )
        return response

    @staticmethod
    def parse_model_name(response: dict[str, Any]) -> str:
        model_name = response.get("model") or response.get("model_name")
        if model_name:
            return str(model_name)
        return "unknown"

    @staticmethod
    def parse_generated_text(response: dict[str, Any]) -> str:
        content = response.get("response")
        if isinstance(content, str):
            return content
        message = response.get("message") or {}
        if isinstance(message, dict):
            content = message.get("content")
            if isinstance(content, str):
                return content
        return json.dumps(response, ensure_ascii=False)
