from __future__ import annotations

from typing import Any

from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str, wait_for_load: bool = True, timeout: int = 120000) -> None:
        self.page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        if wait_for_load:
            try:
                self.page.wait_for_load_state("networkidle", timeout=timeout)
            except Exception:
                pass

    def fill(self, locator: Any, value: str, *, timeout: int = 30000) -> None:
        locator.fill(value, timeout=timeout)

    def click(self, locator: Any, *, timeout: int = 30000) -> None:
        locator.click(timeout=timeout)

    def expect_visible(self, locator: Any, *, timeout: int = 30000) -> None:
        expect(locator).to_be_visible(timeout=timeout)

    def take_screenshot(self, file_path: str, *, full_page: bool = False) -> None:
        self.page.screenshot(path=file_path, full_page=full_page)
