from __future__ import annotations

from typing import Iterator, Self

from fantasy_forge.item import Item
from fantasy_forge.world import World, highlight_interactive


class InventoryFull(Exception):
    pass


class InventoryTooSmall(Exception):
    pass


class Inventory:
    """An Inventory contains multiple items."""

    world: World
    capacity: int
    contents: dict[str, Item]

    def __init__(self: Self, world: World, capacity: int):
        self.world = world
        self.capacity = capacity
        self.contents = {}

    def __iter__(self: Self) -> Iterator[Item]:
        """Iterates over items in inventory."""
        yield from self.contents.values()

    def __contains__(self: Self, other: str) -> bool:
        """Returns if item is in inventory."""
        return other in self.contents.keys()

    def __repr__(self: Self) -> str:
        output: str = f"Inventory({len(self)}/{self.capacity})\n"
        output += "[" + ", ".join(self.contents.keys()) + "]"
        return output

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
                self.world.l10n.format_value(
                    "inventory-capacity-message",
                    {
                        "capacity": self.capacity,
                    },
                )
            )
        elif weight + item.weight > self.capacity:
            raise InventoryTooSmall(
                self.world.l10n.format_value(
                    "inventory-too-small-message",
                    {
                        "capacity": self.capacity,
                        "weight": item.weight,
                    },
                )
            )

    def get(self: Self, item_name: str) -> Item | None:
        """Gets item by name."""
        return self.contents.get(item_name)

    def pop(self: Self, item_name: str) -> Item | None:
        """Pops item from inventory."""
        if item_name in self:
            return self.contents.pop(item_name)
        return None

    def on_look(self: Self) -> str:
        if not self.contents:
            return self.world.l10n.format_value("inventory-look-empty-message")
        else:
            return self.world.l10n.format_value(
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
