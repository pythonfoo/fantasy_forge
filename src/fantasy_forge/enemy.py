from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from fantasy_forge.character import Character, bare_hands
from fantasy_forge.item import Item


class Enemy(Character):
    """An enemy is a person which will fight back."""

    def __init__(self: Self, config_dict: dict[str, Any], l10n: FluentLocalization):
        super().__init__(config_dict, l10n)
        for item_dict in config_dict.get("loot", []):
            self.inventory.add(Item(item_dict, l10n))

    def __str__(self: Self) -> str:
        return self.name


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
