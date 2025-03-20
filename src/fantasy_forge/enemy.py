from typing import Any, Self

from fantasy_forge.character import bare_hands, Character
from fantasy_forge.item import Item
from fantasy_forge.world import World




class Enemy(Character):
    """An enemy is a person which will fight back."""

    def __init__(self: Self, world: World, config_dict: dict[str, Any]):
        super().__init__(world, config_dict)
        for item_dict in config_dict.get("loot", []):
            self.inventory.add(Item(world, item_dict))

    def __str__(self: Self) -> str:
        return self.name

