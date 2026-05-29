import pytest
from playwright.sync_api import Page, BrowserContext, Browser, Playwright, sync_playwright

from config.settings import BASE_URL, GRID_LOAD_TIMEOUT_MS
from pages.home_page import HomePage
from pages.issues_page import IssuesPage
from utils.frame_helper import get_app_frame


@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {"headless": True}


@pytest.fixture
def context(browser: Browser):
    ctx: BrowserContext = browser.new_context(
        viewport={"width": 1280, "height": 800},
    )
    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx
    ctx.tracing.stop()
    ctx.close()


@pytest.fixture
def page(context: BrowserContext, request) -> Page:
    pg = context.new_page()
    pg.goto(BASE_URL)
    yield pg

    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        _save_failure_artifacts(pg, context, request.node.name)

    pg.close()


@pytest.fixture
def app_frame(page: Page):
    """Resolve the double-iframe nesting to the innermost FrameLocator."""
    return get_app_frame(page)


@pytest.fixture
def home_page(page: Page, app_frame) -> HomePage:
    return HomePage(page=page, frame=app_frame)


@pytest.fixture
def issues_page(page: Page, app_frame, home_page: HomePage) -> IssuesPage:
    """Navigate from the home page to the issues grid and return IssuesPage."""
    home_page.dismiss_modal_if_present()
    home_page.navigate_to_issues()
    return IssuesPage(frame=app_frame)


def _save_failure_artifacts(page: Page, context: BrowserContext, test_name: str) -> None:
    safe_name = test_name.replace("/", "_").replace("\\", "_")
    page.screenshot(path=f"test-results/screenshots/{safe_name}.png", full_page=True)
    context.tracing.stop(path=f"test-results/traces/{safe_name}.zip")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
