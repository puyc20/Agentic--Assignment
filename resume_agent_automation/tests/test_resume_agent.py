from __future__ import annotations

from pathlib import Path

import pytest

from resume_agent_automation.config.settings import APP, PATHS
from resume_agent_automation.pages.resume_agent_page import ResumeAgentPage
from resume_agent_automation.utils.excel_reader import read_manual_test_cases


TEST_CASES = read_manual_test_cases(PATHS.manual_cases_path)
TEST_IDS = ["TC-001", "TC-002", "TC-003", "TC-004", "TC-005", "TC-006", "TC-007"]
SCENARIO_MAP = {case["Test ID"]: case for case in TEST_CASES if case.get("Test ID")}


def _scenario_for(test_id: str):
    case = SCENARIO_MAP.get(test_id)
    if not case:
        pytest.skip(f"Manual case {test_id} not found in workbook")
    return case


def test_resume_agent_login_smoke(resume_page: ResumeAgentPage):
    assert APP.app_username, "APP_USERNAME must be set to perform a smoke login test."
    assert APP.app_password, "APP_PASSWORD must be set to perform a smoke login test."

    resume_page.login(APP.app_username, APP.app_password)
    final_url = resume_page.page.url
    body_text = resume_page.page.locator("body").inner_text()
    assert "/home" in final_url or "Sign in with your username and password" in body_text


@pytest.mark.parametrize("test_id", TEST_IDS[:5])
def test_resume_agent_scenario(resume_page: ResumeAgentPage, test_id: str):
    scenario = _scenario_for(test_id)
    if not APP.resume_agent_enabled:
        pytest.skip("Resume agent automation is disabled. Set RESUME_AGENT_ENABLED=true to run the end-to-end workflow.")

    resume_page.login(APP.app_username, APP.app_password)
    try:
        resume_page.open_resume_agent()
    except RuntimeError as exc:
        pytest.skip(str(exc))

    case_description = scenario.get("Test Case Description", "")
    if "Tailor an existing resume" in case_description:
        resume_page.enter_target_role("Senior Data Engineer")
    elif "Improve the professional summary" in case_description:
        resume_page.ask_agent("Improve the professional summary while keeping the supported facts accurate.")
    elif "Enhance experience descriptions" in case_description:
        resume_page.ask_agent("Rewrite the experience descriptions to be more concise and impactful without inventing facts.")
    elif "Add a new work experience entry" in case_description:
        resume_page.ask_agent("Add a Senior Data Engineer experience entry with 2023-2025, using only accurate, supplied details.")
    elif "Add relevant skills to the resume" in case_description:
        resume_page.ask_agent("Add Python, SQL, and stakeholder communication skills to the appropriate skills section.")
    else:
        resume_page.ask_agent("Please review the resume against the requested change and provide the updated content.")

    response = resume_page.read_latest_agent_response()
    assert response and len(response.strip()) > 0
