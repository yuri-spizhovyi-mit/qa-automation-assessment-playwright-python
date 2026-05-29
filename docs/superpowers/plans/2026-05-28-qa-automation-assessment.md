# QA Automation Assessment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a production-quality Playwright + Python + pytest automation framework for a mock CRM data quality application with double-iframe nesting, testing 5 scenarios covering navigation, data extraction, radio selection, inline editing, and checkbox selection counters.

**Architecture:** All page objects receive a `FrameLocator` pointing to the innermost app iframe (`#outerFrame > #appFrame`), so no page object ever touches the outer `Page` object. A `BasePage` wraps common Playwright actions. `HomePage` handles modal dismissal and navigation. `IssuesPage` handles the issues grid interactions.

**Tech Stack:** Python 3.11+, Playwright sync API, pytest, pytest-playwright

---

## File Map

| File | Responsibility |
|---|---|
| `config/settings.py` | BASE_URL, timeouts, test data constants |
| `utils/frame_helper.py` | Resolve nested iframes to innermost FrameLocator |
| `pages/base_page.py` | Reusable wrapped Playwright actions on a FrameLocator |
| `pages/home_page.py` | Dashboard: dismiss modal, click "Review & Fix Issues" |
| `pages/issues_page.py` | Issues grid: cards, checkboxes, radios, inline edits, counter |
| `models/issue_card.py` | IssueCard dataclass (record_id + locator) |
| `conftest.py` | pytest fixtures: browser context, page, app_frame, home_page, issues_page |
| `tests/test_data_issues.py` | 5 pytest tests |
| `requirements.txt` | pytest, playwright, pytest-playwright |
| `pytest.ini` | markers, base_url, test paths |
| `README.md` | Professional project README |

---

### Task 1: Project skeleton + config

**Files:**
- Create: `config/__init__.py`
- Create: `config/settings.py`
- Create: `requirements.txt`
- Create: `pytest.ini`
- Create all `__init__.py` stubs

- [ ] Write `config/settings.py`
- [ ] Write `requirements.txt`
- [ ] Write `pytest.ini`
- [ ] Write `__init__.py` files for all packages

---

### Task 2: Frame helper utility

**Files:**
- Create: `utils/__init__.py`
- Create: `utils/frame_helper.py`

- [ ] Write `frame_helper.py` with `get_app_frame(page)` returning innermost FrameLocator

---

### Task 3: BasePage

**Files:**
- Create: `pages/__init__.py`
- Create: `pages/base_page.py`

- [ ] Write `BasePage` with `__init__(frame)` and helper methods

---

### Task 4: IssueCard model

**Files:**
- Create: `models/__init__.py`
- Create: `models/issue_card.py`

- [ ] Write `IssueCard` dataclass

---

### Task 5: HomePage

**Files:**
- Create: `pages/home_page.py`

- [ ] Write `HomePage` with `dismiss_modal()` and `navigate_to_issues()`

---

### Task 6: IssuesPage

**Files:**
- Create: `pages/issues_page.py`

- [ ] Write `IssuesPage` with all grid interaction methods

---

### Task 7: conftest.py fixtures

**Files:**
- Create: `conftest.py`

- [ ] Write pytest fixtures for browser, page, frame, page objects

---

### Task 8: All 5 tests

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_data_issues.py`

- [ ] Write all 5 test functions

---

### Task 9: Execute and fix

- [ ] Install dependencies
- [ ] Run tests
- [ ] Fix failures

---

### Task 10: README + GitHub

- [ ] Write professional README
- [ ] Create GitHub repo and push
