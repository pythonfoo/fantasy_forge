from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from fantasy_forge.item import Item
from fantasy_forge.messages import Messages


class Weapon(Item):
    """A Weapon is an item, which can deal damage to players or NPCs."""

    __important_attributes__ = ("name", "damage")
    __attributes__ = {**Item.__attributes__, "damage": int}

    damage: int

    def __init__(self: Self, messages: Messages, config_dict: dict[str, Any]) -> None:
        """
        config_dict contents
        'damage' (int): damage dealt using the weapon

        inherited from Item
        'moveable' (bool): can the item be moved by the player (default: True)
        'carryable' (bool): can the item be put in the inventory by the player (default: True)

        inherited from Entity
        'name' (str): name of the entity
        'description' (str): description of the entity (default: "")
        'obvious'(bool): whether the entity will be spotted immediately (default: False)
        """
        self.damage = config_dict.pop("damage")
        super().__init__(messages, config_dict)
