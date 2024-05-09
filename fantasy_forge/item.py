from __future__ import annotations

from typing import Self

from .entity import Entity


class Item(Entity):
    """An Item is an entity which can be picked up by the player."""

    moveable: bool
    carryable: bool

    def __init__(self: Self, name: str, description: str) -> None:
        super().__init__(name, description)
        self.moveable = True
        self.carryable = True

    def __repr__(self: Self) -> str:
        return f"Item({self.name}, {self.description}, moveable={self.moveable}, carryable={self.carryable})"

    def on_pickup(self: Self):
        # TODO
        pass

    def to_dict(self: Self) -> dict:
        item_dict: dict = super().to_dict()
        item_dict["moveable"] = self.moveable
        item_dict["carryable"] = self.carryable
        return item_dict

    @staticmethod
    def from_dict(item_dict: dict) -> Entity:
        entity: Entity = Entity.from_dict(item_dict)
        moveable = item_dict.get("moveable", True)
        carryable = item_dict.get("carryable", True)
        item: Item = Item(entity.name, entity.description, moveable, carryable)
        return item
