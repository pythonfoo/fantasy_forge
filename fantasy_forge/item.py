from __future__ import annotations

from typing import Any, Self

from .entity import Entity
from .world import World


class Item(Entity):
    """An Item is an entity which can be picked up by the player."""

    __important_attributes__ = ("name", "moveable", "carryable")

    moveable: bool
    carryable: bool

    def __init__(self: Self, world: World, config_dict: dict[str, Any]) -> None:
        self.moveable = config_dict.pop("moveable", True)
        self.carryable = config_dict.pop("carryable", True)
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
        return item_dict

    @staticmethod
    def from_dict(world: World, item_dict: dict) -> Item:
        moveable = item_dict.get("moveable", True)
        carryable = item_dict.get("carryable", True)
        item: Item = Item(
            world,
            item_dict["name"],
            item_dict.get("description", ""),
            moveable,
            carryable,
        )
        return item
