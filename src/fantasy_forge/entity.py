from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self


class Entity:
    """An Entity is an abstract object in the world."""

    __important_attributes__ = ("name",)

    world: World
    name: str
    description: str
    obvious: bool  # obvious entities are seen when entering the room

    def __init__(
        self: Self,
        world: World,
        config_dict: dict[str, Any],
    ) -> None:
        self.world = world
        self.name = config_dict.pop("name")
        self.description = config_dict.pop("description", "")
        self.obvious = config_dict.pop("obvious", False)

    def on_look(self: Self) -> str:
        return self.description

    def on_use(self: Self, other: Entity | None = None):
        print(self.world.l10n.format_value(
            "cannot-use-message",
            {
                "self": self.name,
                "other": getattr(other, "name", None),
            }
        ))

    def __repr__(self: Self) -> str:
        listed_attrs = []
        for attr in self.__important_attributes__:
            if not hasattr(self, attr):
                raise AttributeError(
                    f"Missing attribute {attr} in {self.__class__.__name__}"
                )
            listed_attrs.append(f"{attr}={getattr(self, attr)}")
        return f"{self.__class__.__name__}({', '.join(listed_attrs)})"

    def __str__(self: Self) -> str:
        return self.name

    def to_dict(self: Self) -> dict:
        entity_dict: dict = {"name": self.name, "description": self.description}
        return entity_dict


if TYPE_CHECKING:
    from fantasy_forge.world import World
