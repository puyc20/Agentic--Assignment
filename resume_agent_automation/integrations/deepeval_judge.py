from __future__ import annotations

from typing import Any

from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, HallucinationMetric
from deepeval.models import OllamaModel
from deepeval.test_case import LLMTestCase

from resume_agent_automation.config.settings import OLLAMA
from resume_agent_automation.utils.logger import get_logger

logger = get_logger(__name__)


class DeepEvalJudge:
    def __init__(
        self,
        model_name: str | None = None,
        base_url: str | None = None,
        temperature: float = 0.0,
    ):
        self.model_name = model_name or OLLAMA.judge_model
        self.base_url = base_url or OLLAMA.base_url
        self.model = OllamaModel(model=self.model_name, base_url=self.base_url, temperature=temperature)

    def build_test_case(
        self,
        *,
        input_text: str,
        actual_output: str,
        context: list[str] | None = None,
        retrieval_context: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> LLMTestCase:
        return LLMTestCase(
            input=input_text,
            actual_output=actual_output,
            context=context or [],
            retrieval_context=retrieval_context or [],
            metadata=metadata or {},
        )

    def answer_relevancy(self, test_case: LLMTestCase, threshold: float = 0.70) -> dict[str, Any]:
        metric = AnswerRelevancyMetric(model=self.model, threshold=threshold, include_reason=True, async_mode=False)
        score = metric.measure(test_case)
        return {
            "metric": "Answer Relevancy",
            "score": score,
            "threshold": threshold,
            "reason": getattr(metric, "reason", "No reason provided."),
            "passed": bool(score >= threshold),
        }

    def faithfulness(self, test_case: LLMTestCase, threshold: float = 0.70) -> dict[str, Any]:
        metric = FaithfulnessMetric(model=self.model, threshold=threshold, include_reason=True, async_mode=False)
        score = metric.measure(test_case)
        return {
            "metric": "Faithfulness",
            "score": score,
            "threshold": threshold,
            "reason": getattr(metric, "reason", "No reason provided."),
            "passed": bool(score >= threshold),
        }

    def hallucination(self, test_case: LLMTestCase, threshold: float = 0.30) -> dict[str, Any]:
        metric = HallucinationMetric(model=self.model, threshold=0.70, include_reason=True, async_mode=False)
        raw_score = metric.measure(test_case)
        risk = 1.0 - raw_score
        return {
            "metric": "Hallucination",
            "consistency_score": raw_score,
            "hallucination_risk": risk,
            "threshold": threshold,
            "reason": getattr(metric, "reason", "No reason provided."),
            "passed": bool(risk <= threshold),
        }
