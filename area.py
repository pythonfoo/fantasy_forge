from __future__ import annotations

from typing import Self, Iterator

from entity import Entity


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
