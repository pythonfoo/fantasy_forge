from __future__ import annotations

from typing import TYPE_CHECKING, Self

from fantasy_forge.container import Container
from fantasy_forge.entity import Entity
from fantasy_forge.item import Item
from fantasy_forge.localization import highlight_interactive
from fantasy_forge.utils import UniqueDict


class InventoryFull(Exception):
    pass


class InventoryTooSmall(Exception):
    pass


class Inventory(Container):
    """An Inventory contains multiple entities."""

    def __init__(self: Self, messages: Messages, capacity: int):
        self.messages = messages
        self.capacity = capacity
        self.contents = UniqueDict()

    def calculate_weight(self: Self) -> int:
        weight = 0
        for item in self.contents.values():
            weight += item.weight
        return weight

    def add(self: Self, item: Item) -> None:
        """Adds Item to inventory with respect to capacity."""
        assert item.name not in self.contents
        weight = self.calculate_weight()
        if weight + item.weight <= self.capacity:
            self.contents[item.name] = item
        elif weight == self.capacity:
            raise InventoryFull(
                self.messages.l10n.format_value(
                    "inventory-capacity-message",
                    {
                        "capacity": self.capacity,
                    },
                )
            )
        elif weight + item.weight > self.capacity:
            raise InventoryTooSmall(
                self.messages.l10n.format_value(
                    "inventory-too-small-message",
                    {
                        "capacity": self.capacity,
                        "weight": item.weight,
                    },
                )
            )

    def get(self: Self, entity_name: str) -> Entity | None:
        """Gets item by name."""
        return self.contents.get(entity_name)

    def pop(self: Self, entity_name: str) -> Entity | None:
        """Pops item from inventory."""
        if entity_name in self:
            return self.contents.pop(entity_name)
        return None

    def pop_all(self: Self) -> list[Item]:
        """Pops all items from the inventory, used for when the player dies/leaves the game in mp"""
        items = list(self.contents.values())
        self.contents.clear()
        return items

    def on_look(self: Self) -> str:
        if not self.contents:
            return self.messages.l10n.format_value("inventory-look-empty-message")
        else:
            return self.messages.l10n.format_value(
                "inventory-look-message",
                {
                    "items": ", ".join(
                        [
                            highlight_interactive(str(item)).format(None)
                            + f" (weight: {item.weight})"
                            for item in self
                        ]
                    ),
                },
            )

    def to_dict(self) -> dict:
        """Returns inventory as a dictionary."""
        entity_dict: dict = super().to_dict()
        inventory_dict: dict = {**entity_dict, "capacity": self.capacity}
        return inventory_dict


if TYPE_CHECKING:
    from fantasy_forge.messages import Messages
