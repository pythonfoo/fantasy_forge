from typing import Any, Self

from fantasy_forge.item import Item
from fantasy_forge.world import World


class Weapon(Item):
    """A Weapon is an item, which can deal damage to players or NPCs."""

    __important_attributes__ = ("name", "damage")

    damage: int

    def __init__(self: Self, world: World, config_dict: dict[str, Any]) -> None:
        self.damage = config_dict.pop("damage")
        super().__init__(world, config_dict)
