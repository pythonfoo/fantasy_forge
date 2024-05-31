from typing import Self

from .entity import Entity
from .weapon import Weapon
from .world import World


class Character(Entity):
    """A character in the world."""

    __important_attributes__ = ("name", "health", "alive")

    health: int
    _alive: bool

    def __init__(
        self: Self, world: World, name: str, description: str, health: int
    ) -> None:
        # TODO: implement config_dict like the other classes
        self.health = health
        super().__init__(world, dict(name=name, description=description))

    @property
    def alive(self: Self) -> bool:
        self._alive = self.health > 0
        return self._alive

    def on_attack(self: Self, weapon: Weapon):
        self.health -= weapon.damage
