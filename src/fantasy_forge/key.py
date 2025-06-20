from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from fantasy_forge.item import Item
from fantasy_forge.messages import Messages


class Key(Item):
    """A Key can be used to unlock Gateways or Container."""

    __important_attributes__ = ("name", "key_id")
    __attributes__ = {**Item.__attributes__, "key_id": str, "used": bool}

    key_id: str
    used: bool  # wether the key was used already


    def __init__(self: Self, messages: Messages, config_dict: dict[str, Any]) -> None:
        """
        config_dict contents
        key_id (str): identifiable key id

        inherited from Item
        'moveable' (bool): can the item be moved by the player (default: True)
        'carryable' (bool): can the item be put in the inventory by the player (default: True)
        'weight' (int): weight of the item (important for inventory capacity)

        inherited from Entity
        'name' (str): name of the entity
        'description' (str): description of the entity (default: "")
        'obvious'(bool): whether the entity will be spotted immediately (default: False)
        """
        self.key_id = config_dict.pop("key_id")

        self.moveable = True  # keys are moveable by default
        self.carryable = True  # keys are carryable by default
        self.weight = 0  # keys are weightless by default

        super().__init__(messages, config_dict)
        self.used = False

    def __eq__(self: Self, other: object):
        """Compares key ids."""
        if not isinstance(other, Key):
            return False
        return self.key_id == other.key_id

    def __hash__(self) -> int:
        """Returns hash of key id."""
        return hash(self.key_id)


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization

