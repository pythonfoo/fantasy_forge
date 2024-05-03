from typing import Self

from entity import Entity


class Character(Entity):
    """A character in the world."""

    health: int

    def __init__(self: Self, name: str, description: str, health: int) -> None:
        super().__init__(name, description)
        self.health = health

    def __repr__(self: Self) -> str:
        return f"Character({self.name}, {self.description}, {self.health})"
