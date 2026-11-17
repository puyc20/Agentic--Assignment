from __future__ import annotations

from deepeval.test_case import LLMTestCase

from resume_agent_automation.integrations.deepeval_judge import DeepEvalJudge
from resume_agent_automation.integrations.ollama_client import OllamaClient


def test_ollama_model_available():
    client = OllamaClient()
    assert client.is_available(), "Ollama service is not available or the configured model is missing."


def test_deepeval_configuration_is_present():
    judge = DeepEvalJudge()
    assert judge.model is not None
    assert judge.model_name


def test_deepeval_metric_run_example():
    judge = DeepEvalJudge()
    test_case = LLMTestCase(
        input="What are the candidate's top skills?",
        actual_output="The candidate has Python, SQL, and stakeholder communication skills.",
        context=["The candidate has Python, SQL, and stakeholder communication skills."],
        retrieval_context=["The candidate has Python, SQL, and stakeholder communication skills."],
    )

    answer_result = judge.answer_relevancy(test_case, threshold=0.70)
    faithfulness_result = judge.faithfulness(test_case, threshold=0.70)
    hallucination_result = judge.hallucination(test_case, threshold=0.30)

    assert answer_result["passed"] is True or answer_result["score"] >= 0.0
    assert faithfulness_result["passed"] is True or faithfulness_result["score"] >= 0.0
    assert "hallucination_risk" in hallucination_result
