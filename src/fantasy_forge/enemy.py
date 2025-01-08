"""Enemy class

An enemy is a hostile character which will attack the player on contact.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from fantasy_forge.character import Character, bare_hands
from fantasy_forge.item import Item


class Enemy(Character):
    """An enemy is a person which will fight back."""

    def __init__(self: Self, config_dict: dict[str, Any], l10n: FluentLocalization):
        """
        config_dict contents
        'loot' (list[Item]): items dropped after death

        inherited from Character
        'health' (int): health points

        inherited from Entity:
        'name' (str): name of the entity
        'description' (str): description of the entity (default: "")
        'obvious'(bool): whether the entity will be spotted immediately (default: False)
        """
        super().__init__(config_dict, l10n)
        for item_dict in config_dict.get("loot", []):
            self.inventory.add(Item(item_dict, l10n))

    def __str__(self: Self) -> str:
        return self.name


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
