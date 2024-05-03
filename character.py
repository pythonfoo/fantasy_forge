from typing import Self

from entity import Entity
from weapon import Weapon


class Character(Entity):
    """A character in the world."""

    health: int
    _alive: bool

    def __init__(self: Self, name: str, description: str, health: int) -> None:
        super().__init__(name, description)
        self.health = health

    def __repr__(self: Self) -> str:
        return f"Character({self.name}, {self.description}, {self.health}, alive={self.alive})"

    @property
    def alive(self: Self) -> bool:
        self._alive = self.health > 0
        return self._alive

    def on_attack(self: Self, weapon: Weapon):
        self.health -= weapon.damage
