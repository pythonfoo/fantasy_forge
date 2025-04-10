from __future__ import annotations

from typing import Any, Self

from fantasy_forge.item import Item
from fantasy_forge.messages import Messages


class Key(Item):
    """A Key can be used to unlock Gateways or Container."""

    __important_attributes__ = ("name", "key_id")

    key_id: str
    used: bool  # wether the key was used already

    def __init__(self: Self, messages: Messages, config_dict: dict[str, Any]) -> None:
        self.key_id = config_dict.pop("key_id")

        self.moveable = True  # keys are moveable by default
        self.carryable = True  # keys are carryable by default
        super().__init__(messages, config_dict)
        self.used = False

    def __eq__(self: Self, other: Key):
        """Compares key ids."""
        return self.key_id == other.key_id
