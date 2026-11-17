from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from resume_agent_automation.integrations.deepeval_judge import DeepEvalJudge
from resume_agent_automation.utils.logger import get_logger

logger = get_logger(__name__)


class EvaluationRunner:
    def __init__(self, judge: DeepEvalJudge | None = None):
        self.judge = judge or DeepEvalJudge()

    def evaluate_case(
        self,
        *,
        test_id: str,
        scenario_name: str,
        user_input: str,
        actual_output: str,
        context: list[str] | None = None,
        retrieval_context: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        test_case = self.judge.build_test_case(
            input_text=user_input,
            actual_output=actual_output,
            context=context or [],
            retrieval_context=retrieval_context or [],
            metadata=metadata or {},
        )

        answer = self.judge.answer_relevancy(test_case)
        faithfulness = self.judge.faithfulness(test_case)
        hallucination = self.judge.hallucination(test_case)

        result = {
            "test_id": test_id,
            "scenario": scenario_name,
            "answer_relevancy": answer,
            "faithfulness": faithfulness,
            "hallucination": hallucination,
            "overall_pass": (
                answer["passed"]
                and faithfulness["passed"]
                and hallucination["passed"]
            ),
        }

        logger.info("Evaluation result for %s: %s", test_id, json.dumps(result, ensure_ascii=False))
        return result
