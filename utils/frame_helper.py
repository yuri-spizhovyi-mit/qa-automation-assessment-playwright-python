from playwright.sync_api import Page, FrameLocator

from config.settings import OUTER_FRAME_ID, INNER_FRAME_ID


def get_app_frame(page: Page) -> FrameLocator:
    """Resolve the nested iframe chain to the innermost application frame."""
    return (
        page.frame_locator(f"#{OUTER_FRAME_ID}")
        .frame_locator(f"#{INNER_FRAME_ID}")
    )
