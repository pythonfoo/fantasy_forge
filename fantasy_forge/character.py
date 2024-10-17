from typing import Any, Self

from .entity import Entity
from .inventory import Inventory
from .weapon import Weapon
from .world import World

BASE_INVENTORY_CAPACITY = 10

class Character(Entity):
    """A character in the world."""

    __important_attributes__ = ("name", "health", "alive")

    health: int
    inventory: Inventory
    _alive: bool

    def __init__(self: Self, world: World, config_dict: dict[str, Any]) -> None:
        self.health = config_dict.pop("health")
        self.inventory = Inventory(world, BASE_INVENTORY_CAPACITY)
        super().__init__(world, config_dict)

    @property
    def alive(self: Self) -> bool:
        self._alive = self.health > 0
        return self._alive

    def on_attack(self: Self, weapon: Weapon):
        self.health -= weapon.damage
