"""
Data Issues grid test suite.

Each test is independently runnable starting from index.html.
All tests navigate through the double-iframe chain and interact with the
Data Issues page via the IssuesPage page object.
"""
import pytest

from config.settings import (
    EXPECTED_ISSUE_COUNT,
    SFID_EDIT_TARGET,
    EDIT_VALUE,
    SEVENTH_CARD_INDEX,
    SEVENTH_CARD_ORIGINAL_PHONE,
    FIRST_CARD_INDEX,
    THIRD_CARD_INDEX,
    FIFTH_CARD_INDEX,
    SELECTION_COUNT_3,
    SELECTION_COUNT_10,
)
from pages.issues_page import IssuesPage


class TestDataIssuesGrid:

    def test_navigate_to_issues_shows_ten_cards(self, issues_page: IssuesPage) -> None:
        """Test 1: Navigate to Data Issues and assert 10 issue cards are displayed."""
        card_count = issues_page.get_card_count()

        assert card_count == EXPECTED_ISSUE_COUNT, (
            f"Expected {EXPECTED_ISSUE_COUNT} issue cards, found {card_count}"
        )

    def test_all_original_rows_have_non_empty_sfid(self, issues_page: IssuesPage) -> None:
        """Test 2: Every issue card's original row must contain a non-empty sfid."""
        cards = issues_page.get_all_cards()

        assert len(cards) == EXPECTED_ISSUE_COUNT

        for card in cards:
            sfid = issues_page.get_original_row_sfid(card)
            assert sfid, (
                f"Card {card.record_id} has an empty sfid in its original row"
            )

    def test_select_original_value_updates_final_row(self, issues_page: IssuesPage) -> None:
        """Test 3: Select original radio on the 7th card; assert final row reflects original value."""
        seventh_card = issues_page.get_card_by_index(SEVENTH_CARD_INDEX)

        issues_page.select_original_radio(seventh_card)

        final_value = issues_page.get_final_row_issue_cell_text(seventh_card)
        assert final_value == SEVENTH_CARD_ORIGINAL_PHONE, (
            f"Expected final row to show '{SEVENTH_CARD_ORIGINAL_PHONE}', got '{final_value}'"
        )

    def test_edit_final_row_value(self, issues_page: IssuesPage) -> None:
        """Test 4: Edit the final row field for sfid 00Qak00000RHtuzEAD and assert the new value."""
        target_card = issues_page.get_card_by_record_id(SFID_EDIT_TARGET)

        issues_page.edit_final_row_value(target_card, EDIT_VALUE)

        final_value = issues_page.get_final_row_issue_cell_text(target_card)
        assert final_value == EDIT_VALUE, (
            f"Expected final row to display '{EDIT_VALUE}', got '{final_value}'"
        )

    def test_checkbox_selection_counter(self, issues_page: IssuesPage) -> None:
        """Test 5: Verify selection counter for partial, full, and no selection."""
        issues_page.check_card_by_index(FIRST_CARD_INDEX)
        issues_page.check_card_by_index(THIRD_CARD_INDEX)
        issues_page.check_card_by_index(FIFTH_CARD_INDEX)

        assert issues_page.is_selection_bar_visible(), "Selection bar should be visible with 3 items checked"
        counter_text = issues_page.get_selection_count_text()
        assert SELECTION_COUNT_3 in counter_text, (
            f"Expected '{SELECTION_COUNT_3}' in counter, got '{counter_text}'"
        )

        issues_page.check_all_issues()

        counter_text = issues_page.get_selection_count_text()
        assert SELECTION_COUNT_10 in counter_text, (
            f"Expected '{SELECTION_COUNT_10}' in counter, got '{counter_text}'"
        )

        issues_page.uncheck_all_issues()

        assert not issues_page.is_selection_bar_visible(), (
            "Selection bar should not be visible after deselecting all"
        )
