from typing import Self

from .item import Item


class Weapon(Item):
    """A Weapon is an item, which can deal damage to players or NPCs."""

    damage: int

    def __init__(self: Self, name: str, description: str, damage: int) -> None:
        # TODO: implement config_dict like the other classes
        super().__init__(name, description)
        self.damage = damage
