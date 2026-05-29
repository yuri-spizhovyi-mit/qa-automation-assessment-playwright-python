from dataclasses import dataclass

from playwright.sync_api import Locator


@dataclass
class IssueCard:
    """Represents a single data issue card in the grid."""

    record_id: str
    locator: Locator
