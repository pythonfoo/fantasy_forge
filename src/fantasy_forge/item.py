from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from fantasy_forge.entity import Entity


class Item(Entity):
    """An Item is an entity which can be picked up by the player."""


    __attributes__ = {**Entity.__attributes__, "moveable": bool, "carryable": bool, "weight": int}
    __important_attributes__ = ("name", "moveable", "carryable", "weight")

    moveable: bool
    carryable: bool
    weight: int

    def __init__(self: Self, messages: Messages, config_dict: dict[str, Any]) -> None:
                """
        config_dict contents
        'moveable' (bool): can the item be moved by the player (default: True)
        'carryable' (bool): can the item be put in the inventory by the player (default: True)
        'weight' (int): weight of the item (important for inventory capacity)

        inherited from Entity
        'name' (str): name of the entity
        'description' (str): description of the entity (default: "")
        'obvious'(bool): whether the entity will be spotted immediately (default: False)
        """
        self.moveable = config_dict.pop("moveable", True)
        self.carryable = config_dict.pop("carryable", True)
        self.weight = config_dict.pop("weight", 1)
        super().__init__(messages, config_dict)

    def __repr__(self: Self) -> str:
        return f"Item({self.name}, {self.description}, moveable={self.moveable}, carryable={self.carryable}, weight={self.weight})"

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
    def from_dict(messages: Messages, item_dict: dict) -> Item:
        item: Item = Item(messages, item_dict)
        return item


if TYPE_CHECKING:
    from fantasy_forge.messages import Messages
