from __future__ import annotations

from typing import Self


class Entity:
    """An Entity is an abstract object in the world."""

    name: str
    description: str

    def __init__(self: Self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def on_look(self: Self) -> str:
        return self.description

    def __repr__(self: Self) -> str:
        return f"Entity({self.name}, {self.description})"

    def __str__(self: Self) -> str:
        return self.name

    def to_dict(self: Self) -> dict:
        entity_dict: dict = {"name": self.name, "description": self.description}
        return entity_dict

    @staticmethod
    def from_dict(entity_dict: dict) -> Entity:
        name: str = entity_dict.get("name", "")
        description: str = entity_dict.get("description", "")
        return Entity(name, description)
