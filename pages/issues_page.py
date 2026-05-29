from playwright.sync_api import FrameLocator, Locator, expect

from config.settings import SAVE_TIMEOUT_MS
from models.issue_card import IssueCard
from pages.base_page import BasePage


class IssuesPage(BasePage):
    """Interactions with the Data Issues grid."""

    _CARDS_CONTAINER = "#issueCardsContainer"
    _ISSUE_CARD = ".issue-card"
    _CONFIRM_BAR = "#confirmBar"
    _SELECTED_COUNT = "#selectedCount"
    _SELECT_ALL = "#selectAll"
    _ORIGINAL_ROW = "tr[data-row-type='original']"
    _FINAL_ROW = "tr[data-row-type='final']"
    _EDITABLE_CELL = ".cell-editable"
    _INLINE_INPUT = ".inline-edit-input"
    _CELL_SPINNER = ".cell-spinner"

    def get_all_cards(self) -> list[IssueCard]:
        """Return all visible issue cards as IssueCard models."""
        cards_locator = self._frame.locator(self._ISSUE_CARD)
        count = cards_locator.count()
        return [
            IssueCard(
                record_id=cards_locator.nth(i).get_attribute("data-record-id") or "",
                locator=cards_locator.nth(i),
            )
            for i in range(count)
        ]

    def get_card_count(self) -> int:
        return self._frame.locator(self._ISSUE_CARD).count()

    def get_card_by_index(self, index: int) -> IssueCard:
        card_loc = self._frame.locator(self._ISSUE_CARD).nth(index)
        record_id = card_loc.get_attribute("data-record-id") or ""
        return IssueCard(record_id=record_id, locator=card_loc)

    def get_card_by_record_id(self, record_id: str) -> IssueCard:
        card_loc = self._frame.locator(f"[data-record-id='{record_id}']")
        return IssueCard(record_id=record_id, locator=card_loc)

    def get_original_row_sfid(self, card: IssueCard) -> str:
        """Extract the sfid text from the original row of a card."""
        sfid_cell = (
            card.locator
            .locator(self._ORIGINAL_ROW)
            .locator("td:last-child span")
        )
        return sfid_cell.inner_text().strip()

    def select_original_radio(self, card: IssueCard) -> None:
        """Select the 'original' radio button for the issue column."""
        radio = card.locator.locator(
            f"{self._ORIGINAL_ROW} input[type='radio'][value='original']"
        )
        radio.click()
        self._wait_for_save_spinner_to_clear(card)

    def get_final_row_issue_cell_text(self, card: IssueCard) -> str:
        """Return the current text shown in the final row's editable cell."""
        span = card.locator.locator(f"{self._FINAL_ROW} {self._EDITABLE_CELL} span")
        return span.inner_text().strip()

    def edit_final_row_value(self, card: IssueCard, new_value: str) -> None:
        """Click the editable cell, clear it, type a new value, and confirm."""
        editable = card.locator.locator(f"{self._FINAL_ROW} {self._EDITABLE_CELL}")
        editable.click()

        inline_input = card.locator.locator(self._INLINE_INPUT)
        inline_input.wait_for(state="visible")
        inline_input.fill(new_value)
        inline_input.press("Enter")

        self._wait_for_save_spinner_to_clear(card)

    def check_card_by_index(self, index: int) -> None:
        """Check the checkbox on the card at the given index."""
        card = self.get_card_by_index(index)
        checkbox = card.locator.locator("input.issue-checkbox")
        checkbox.check()

    def check_all_issues(self) -> None:
        """Click the Select All checkbox to select every issue."""
        self._frame.locator(self._SELECT_ALL).check()

    def uncheck_all_issues(self) -> None:
        """Uncheck the Select All checkbox to deselect every issue."""
        self._frame.locator(self._SELECT_ALL).uncheck()

    def get_selection_count_text(self) -> str:
        """Return the full text of the selection counter bar."""
        bar = self._frame.locator(self._CONFIRM_BAR)
        return bar.inner_text().strip()

    def is_selection_bar_visible(self) -> bool:
        return self._frame.locator(self._CONFIRM_BAR).is_visible()

    def _wait_for_save_spinner_to_clear(self, card: IssueCard) -> None:
        spinner = card.locator.locator(self._CELL_SPINNER)
        try:
            spinner.first.wait_for(state="visible", timeout=2000)
        except Exception:
            pass
        spinner.first.wait_for(state="hidden", timeout=SAVE_TIMEOUT_MS)
