"""Enemy class

An enemy is a hostile character which will attack the player on contact.
"""

from typing import TYPE_CHECKING, Any, Self
from fantasy_forge.character import Character, bare_hands
from fantasy_forge.item import Item
from fantasy_forge.messages import Messages


class Enemy(Character):
    """An enemy is a person which will fight back."""
    def __init__(self: Self, messages: Messages, config_dict: dict[str, Any]):
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
        super().__init__(messages, config_dict)
        for item_dict in config_dict.get("loot", []):
            self.inventory.add(Item(messages, item_dict))

    def __str__(self: Self) -> str:
        return self.name
