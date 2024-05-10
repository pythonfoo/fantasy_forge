from __future__ import annotations

from pathlib import Path
from typing import Iterator, Self, TYPE_CHECKING

import toml

from .entity import Entity


class Area(Entity):
    """An Area is a place in the world, containing NPCs, Items and connections to other areas."""

    contents: list[Entity]

    def __init__(self: Self, world: World, name: str, description: str):
        super().__init__(world, name, description)
        self.contents = []

    def __iter__(self: Self) -> Iterator:
        for obj in self.contents:
            yield obj

    def __repr__(self: Self) -> str:
        return f"Area({self.name})"

    def on_look(self: Self) -> str:
        output = f"{self.description}\n"
        for obj in self.contents:
            output += f"You see {obj.name}\n"
        return output

    def to_dict(self: Self) -> dict:
        area_dict: dict = super().to_dict()
        area_dict["contents"] = self.contents
        return area_dict

    @staticmethod
    def from_dict(world: World, area_dict: dict) -> Area:
        entity: Entity = Entity.from_dict(world, area_dict)
        contents: list = area_dict.get("contents", [])
        area = Area(world, entity.name, entity.description)
        area.contents = contents
        return area


    @staticmethod
    def load(world, root_path: Path, name: str):
        path = root_path / "areas" / f"{name}.toml"
        with path.open() as area_file:
            area_toml = toml.load(area_file)
        return Area.from_dict(world, area_toml)

    @staticmethod
    def empty(world: World) -> Area:
        """Return an empty area, this is a placeholder."""
        return Area(
            world,
            world.l10n.format_value("void-name"),
            world.l10n.format_value("void-description"),
        )

if TYPE_CHECKING:
    from .world import World
