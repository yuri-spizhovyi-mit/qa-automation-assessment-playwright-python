from playwright.sync_api import Page, expect

from config.settings import MODAL_TIMEOUT_MS, GRID_LOAD_TIMEOUT_MS
from pages.base_page import BasePage


class HomePage(BasePage):
    """Dashboard page interactions."""

    _MODAL_OVERLAY = "#welcomeModal"
    _MODAL_DISMISS_BUTTON = "#welcomeModal button"
    _SOLVE_BUTTON = "#solveBtn"
    _ISSUES_PAGE = "#page-issues"
    _GRID_LOADING = ".grid-loading"

    def __init__(self, page: Page, frame) -> None:
        super().__init__(frame)
        self._page = page

    def dismiss_modal_if_present(self) -> None:
        """Dismiss the welcome modal that appears after page load."""
        modal = self._page.locator(self._MODAL_OVERLAY)
        try:
            modal.wait_for(state="visible", timeout=MODAL_TIMEOUT_MS)
            self._page.locator(self._MODAL_DISMISS_BUTTON).click()
            modal.wait_for(state="hidden", timeout=MODAL_TIMEOUT_MS)
        except Exception:
            pass

    def navigate_to_issues(self) -> None:
        """Click 'Review & Fix Issues' and wait for the grid to fully load."""
        self.click(self._SOLVE_BUTTON)
        self._wait_for_grid_to_load()

    def _wait_for_grid_to_load(self) -> None:
        loading = self._frame.locator(self._GRID_LOADING)
        try:
            loading.wait_for(state="visible", timeout=3000)
        except Exception:
            pass
        loading.wait_for(state="hidden", timeout=GRID_LOAD_TIMEOUT_MS)
