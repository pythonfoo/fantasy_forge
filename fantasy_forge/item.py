from __future__ import annotations

from typing import Self

from .entity import Entity
from .world import World


class Item(Entity):
    """An Item is an entity which can be picked up by the player."""

    moveable: bool
    carryable: bool

    def __init__(self: Self, world: World, name: str, description: str, moveable: bool, carryable: bool) -> None:
        super().__init__(world, name, description)
        self.moveable = moveable
        self.carryable = carryable

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
    def from_dict(world: World, item_dict: dict) -> Item:
        moveable = item_dict.get("moveable", True)
        carryable = item_dict.get("carryable", True)
        item: Item = Item(world, item_dict["name"], item_dict.get("description", ""), moveable, carryable)
        return item
