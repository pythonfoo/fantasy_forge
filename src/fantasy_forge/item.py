from __future__ import annotations

from typing import Any, Self

from fantasy_forge.entity import Entity
from fantasy_forge.world import World


class Item(Entity):
    """An Item is an entity which can be picked up by the player."""

    __important_attributes__ = ("name", "moveable", "carryable")

    moveable: bool
    carryable: bool
    weight: int

    def __init__(self: Self, world: World, config_dict: dict[str, Any]) -> None:
        self.moveable = config_dict.pop("moveable", True)
        self.carryable = config_dict.pop("carryable", True)
        self.weight = config_dict.pop("weight", 1)
        super().__init__(world, config_dict)

    def __repr__(self: Self) -> str:
        return f"Item({self.name}, {self.description}, moveable={self.moveable}, carryable={self.carryable})"

    def on_pickup(self: Self):
        # TODO
        pass

    def to_dict(self: Self) -> dict:
        item_dict: dict = super().to_dict()
        item_dict["moveable"] = self.moveable
        item_dict["carryable"] = self.carryable
        item_dict["weight"] = self.weight
        return item_dict

    @staticmethod
    def from_dict(world: World, item_dict: dict) -> Item:
        item: Item = Item(world, item_dict)
        return item
