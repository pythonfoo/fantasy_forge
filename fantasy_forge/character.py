from typing import Any, Self

from .entity import Entity
from .weapon import Weapon
from .world import World


class Character(Entity):
    """A character in the world."""

    __important_attributes__ = ("name", "health", "alive")

    health: int
    _alive: bool

    def __init__(self: Self, world: World, config_dict: dict[str, Any]) -> None:
        self.health = config_dict.pop("health")
        super().__init__(world, config_dict)

    @property
    def alive(self: Self) -> bool:
        self._alive = self.health > 0
        return self._alive

    def on_attack(self: Self, weapon: Weapon):
        self.health -= weapon.damage
