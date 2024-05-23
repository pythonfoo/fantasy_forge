from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self


class Entity:
    """An Entity is an abstract object in the world."""

    world: World
    name: str
    description: str
    obvious: bool # obvious entities are seen when entering the room

    def __init__(
        self: Self, world: World, config_dict: dict[str, Any],
    ) -> None:
        self.world = world
        self.name = config_dict.pop("name")
        self.description = config_dict.pop("description", "")
        self.obvious = config_dict.pop("obvious", False)

    def on_look(self: Self) -> str:
        return self.description

    def __repr__(self: Self) -> str:
        return f"Entity({self.name}, {self.description})"

    def __str__(self: Self) -> str:
        return self.name

    def to_dict(self: Self) -> dict:
        entity_dict: dict = {"name": self.name, "description": self.description}
        return entity_dict


if TYPE_CHECKING:
    from .world import World
