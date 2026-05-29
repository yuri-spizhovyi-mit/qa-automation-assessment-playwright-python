from playwright.sync_api import FrameLocator, Locator


class BasePage:
    """Wraps common Playwright actions scoped to a FrameLocator."""

    def __init__(self, frame: FrameLocator) -> None:
        self._frame = frame

    def locator(self, selector: str) -> Locator:
        return self._frame.locator(selector)

    def get_by_role(self, role: str, **kwargs) -> Locator:
        return self._frame.get_by_role(role, **kwargs)

    def wait_for_selector(self, selector: str, timeout: int | None = None) -> Locator:
        loc = self._frame.locator(selector)
        if timeout is not None:
            loc.wait_for(timeout=timeout)
        else:
            loc.wait_for()
        return loc

    def click(self, selector: str) -> None:
        self._frame.locator(selector).click()

    def fill(self, selector: str, value: str) -> None:
        self._frame.locator(selector).fill(value)

    def is_visible(self, selector: str) -> bool:
        return self._frame.locator(selector).is_visible()
