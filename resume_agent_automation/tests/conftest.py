from __future__ import annotations

import os

import pytest
from playwright.sync_api import Page, PlaywrightContextManager, sync_playwright

from resume_agent_automation.config.settings import APP, ensure_directories
from resume_agent_automation.pages.resume_agent_page import ResumeAgentPage

ensure_directories()


@pytest.fixture(scope="session")
def playwright() -> PlaywrightContextManager:
    with sync_playwright() as playwright_ctx:
        yield playwright_ctx


@pytest.fixture(scope="function")
def browser(playwright):
    browser_name = APP.browser
    browser = getattr(playwright, browser_name).launch(headless=APP.headless)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(viewport={"width": 1600, "height": 1200})
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def resume_page(page) -> ResumeAgentPage:
    return ResumeAgentPage(page)
