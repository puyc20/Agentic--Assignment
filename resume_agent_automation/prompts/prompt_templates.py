"""Reusable prompt templates for resume-agent test generation."""

from __future__ import annotations


def build_resume_tuning_prompt(target_role: str, existing_resume_summary: str) -> str:
    return (
        "You are generating controlled test inputs for resume update scenarios. "
        f"The target role is '{target_role}'. The source context is: {existing_resume_summary}. "
        "Return JSON with 'job_title', 'summary_focus', 'key_skills', and 'experience_update' only."
    )


def build_follow_up_answer_prompt(question: str, resume_summary: str) -> str:
    return (
        "Answer the following follow-up question using only the supplied resume context. "
        f"Question: {question}\nResume context: {resume_summary}.\n"
        "Keep the answer short, factual, and aligned with the resume details."
    )
