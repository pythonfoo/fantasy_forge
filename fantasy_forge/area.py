from __future__ import annotations

from pathlib import Path
from typing import Iterator, Self

import toml

from .entity import Entity


class Area(Entity):
    """An Area is a place in the world, containing NPCs, Items and connections to other areas."""

    contents: list[Entity]

    def __init__(self: Self, name: str, description: str):
        super().__init__(name, description)
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
    def from_dict(area_dict: dict) -> Area:
        entity: Entity = Entity.from_dict(area_dict)
        contents: list = area_dict.get("contents", [])
        area = Area(entity.name, entity.description)
        area.contents = contents
        return area


    @staticmethod
    def load(root_path: Path, name: str):
        path = root_path / "areas" / f"{name}.toml"
        with path.open() as area_file:
            area_toml = toml.load(area_file)
        return Area.from_dict(area_toml)

    @staticmethod
    def empty() -> Area:
        """Return an empty area, this is a placeholder."""
        return Area("the void", "a place filled with nothingness")
