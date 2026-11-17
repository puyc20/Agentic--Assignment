from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Locator, Page, expect

from resume_agent_automation.config.settings import APP
from resume_agent_automation.pages.base_page import BasePage


class ResumeAgentPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def login(self, username: str | None = None, password: str | None = None) -> None:
        username = username or APP.app_username
        password = password or APP.app_password
        self.goto(APP.app_url, timeout=120000)
        self.page.get_by_role("button", name="Sign In").click(timeout=60000)
        self.page.wait_for_load_state("networkidle", timeout=60000)

        form = self.page.locator('form[name="cognitoSignInForm"]').nth(1)
        form.locator('input[name="username"]').fill(username, timeout=60000)
        form.locator('input[name="password"]').fill(password, timeout=60000)
        form.locator('input[name="signInSubmitButton"]').click(timeout=60000)
        try:
            self.page.wait_for_url("**/home**", timeout=60000)
        except Exception:
            pass
        self.page.wait_for_timeout(3000)

    def open_resume_agent(self) -> None:
        if not APP.resume_agent_enabled:
            raise RuntimeError("Resume agent automation is disabled. Set RESUME_AGENT_ENABLED=true to enable it.")

        candidate_selectors = [
            'a:has-text("Resume")',
            'button:has-text("Resume")',
            'text=Resume Updating Agent',
            'text=Resume Agent',
            '[aria-label*="resume" i]',
            '[data-testid*="resume" i]',
        ]

        for selector in candidate_selectors:
            locator = self.page.locator(selector)
            if locator.count() > 0:
                try:
                    locator.first.click()
                    return
                except Exception:
                    continue

        if "resume" not in self.page.url.lower():
            raise RuntimeError(
                "Resume Updating Agent feature was not found in the authenticated application. "
                "This environment does not expose the required workflow."
            )

    def upload_resume(self, file_path: str | Path) -> None:
        resume_path = Path(file_path)
        self.page.locator('input[type="file"]').set_input_files(str(resume_path))

    def enter_target_role(self, role_name: str) -> None:
        role_input = self.page.locator('input[placeholder*="role" i], textarea[placeholder*="role" i], input[aria-label*="role" i]')
        if role_input.count() > 0:
            role_input.first.fill(role_name)
            return
        self.page.locator('textarea').first.fill(role_name)

    def ask_agent(self, message: str) -> None:
        prompt_box = self.page.locator(
            'textarea, input[placeholder*="message" i], input[placeholder*="prompt" i], [role="textbox"]'
        )
        if prompt_box.count() == 0:
            raise RuntimeError("No conversation box found for the resume agent.")
        prompt_box.first.fill(message)
        prompt_box.first.press("Enter")

    def read_latest_agent_response(self) -> str:
        response_blocks = self.page.locator('div, p, span').filter(has_text='')
        # This is intentionally resilient for generic page layouts; choose the last visible non-empty block.
        for idx in range(response_blocks.count() - 1, -1, -1):
            block = response_blocks.nth(idx)
            text = block.inner_text().strip()
            if text and len(text) > 20:
                return text
        return self.page.locator('body').inner_text()

    def capture_screenshot(self, file_path: str, *, failed: bool = False) -> None:
        destination = Path(file_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(destination), full_page=True)
