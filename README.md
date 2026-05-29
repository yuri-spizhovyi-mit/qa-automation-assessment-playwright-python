# QA Automation Assessment — Playwright + Python + pytest

A production-quality test automation framework for a mock CRM data quality application. Built with **Playwright (sync API)**, **Python 3.11+**, and **pytest**, following **Page Object Model**, **SOLID principles**, and **Clean Code** practices.

---

## Project Overview

The application under test is a GenericCRM Data Quality module that surfaces data issues across CRM records. The UI uses a **double-nested iframe** architecture: `index.html → vf-container.html → app.html`. The framework transparently resolves this iframe chain so all page objects work against the innermost application frame without leaking iframe concerns into test code.

---

## Test Coverage

| # | Test | What's Validated |
|---|------|-----------------|
| 1 | `test_navigate_to_issues_shows_ten_cards` | Navigation to Data Issues grid renders exactly 10 issue cards |
| 2 | `test_all_original_rows_have_non_empty_sfid` | Every issue card's original row contains a non-empty `sfid` value |
| 3 | `test_select_original_value_updates_final_row` | Selecting the original radio on the 7th card updates the final row value |
| 4 | `test_edit_final_row_value` | Inline editing the final row for a specific sfid persists the typed value |
| 5 | `test_checkbox_selection_counter` | Partial, full, and empty checkbox selection reflects correct counter text |

---

## Framework Architecture

```
qa-automation-assessment-playwright-python/
│
├── pages/
│   ├── base_page.py        ← Reusable browser actions scoped to a FrameLocator
│   ├── home_page.py        ← Dashboard: modal dismissal, navigation trigger
│   └── issues_page.py      ← Data Issues grid: cards, radios, edits, checkboxes, counter
│
├── tests/
│   └── test_data_issues.py ← All 5 independent pytest test cases
│
├── models/
│   └── issue_card.py       ← IssueCard dataclass (record_id + locator)
│
├── utils/
│   └── frame_helper.py     ← Resolves double-iframe nesting to innermost FrameLocator
│
├── config/
│   └── settings.py         ← Centralized URLs, timeouts, and test data constants
│
├── test-results/
│   ├── screenshots/        ← Captured on test failure
│   └── traces/             ← Playwright trace files captured on test failure
│
├── conftest.py             ← pytest fixtures: browser context, page, frame, page objects
├── pytest.ini              ← pytest configuration
└── requirements.txt        ← Pinned dependencies
```

### Key Design Decisions

- **Double-iframe resolution in one place** — `utils/frame_helper.py:get_app_frame()` resolves `#outerFrame → #appFrame`. No page object or test touches raw iframe selectors.
- **Page objects accept a `FrameLocator`** — `BasePage.__init__(frame)` makes every page object iframe-agnostic. Tests only see page objects.
- **Dynamic delays handled by Playwright auto-waiting** — The app uses random 500–5000ms delays for grid loading and 500–1000ms for save spinners. All waits use `locator.wait_for(state=...)` — never `time.sleep()`.
- **Failure artifacts** — On test failure, a screenshot and Playwright trace zip are written to `test-results/` automatically via the `pytest_runtest_makereport` hook.
- **Constants in `config/settings.py`** — No magic numbers or hardcoded strings in tests.

---

## Tools Used

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Language |
| Playwright | 1.52.0 | Browser automation (sync API) |
| pytest | 8.3.5 | Test runner and fixture management |
| pytest-playwright | 0.7.0 | Playwright-pytest integration, browser fixtures |

---

## Setup & Execution

### 1. Clone the repository

```bash
git clone https://github.com/yspizhoviy/qa-automation-assessment-playwright-python.git
cd qa-automation-assessment-playwright-python
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright browsers

```bash
playwright install chromium
```

### 4. Serve the application locally

In a separate terminal, navigate to the application directory and start the server:

```bash
cd /path/to/app
python -m http.server 8080
```

The tests expect the app at `http://localhost:8080/index.html`.

### 5. Run the tests

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run a single test:

```bash
pytest tests/test_data_issues.py::TestDataIssuesGrid::test_navigate_to_issues_shows_ten_cards -v
```

Run in headed mode (visible browser):

```bash
pytest --headed
```

---

## Viewing Reports, Traces & Screenshots

### Screenshots

On test failure, screenshots are saved to:

```
test-results/screenshots/<test_name>.png
```

### Playwright Traces

On test failure, trace files are saved to:

```
test-results/traces/<test_name>.zip
```

Open a trace in the Playwright Trace Viewer:

```bash
playwright show-trace test-results/traces/<test_name>.zip
```

The Trace Viewer provides a timeline of every action, network request, DOM snapshot, and screenshot taken during the test run — invaluable for debugging failures in CI.

---

## Running in CI

The framework is headless by default. For CI environments, ensure `playwright install --with-deps chromium` is called to install system dependencies alongside the browser binary.

---

## Author

Senior QA Automation Architect assessment submission.
