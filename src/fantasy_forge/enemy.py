from typing import Any, Self

from fantasy_forge.character import Character, bare_hands
from fantasy_forge.item import Item
from fantasy_forge.messages import Messages


class Enemy(Character):
    """An enemy is a person which will fight back."""

    def __init__(self: Self, messages: Messages, config_dict: dict[str, Any]):
        super().__init__(messages, config_dict)
        for item_dict in config_dict.get("loot", []):
            self.inventory.add(Item(messages, item_dict))

    def __str__(self: Self) -> str:
        return self.name
