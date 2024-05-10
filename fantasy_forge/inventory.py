from __future__ import annotations

from typing import Self, Iterator

from .item import Item
from .world import World


class Inventory:
    """An Inventory contains multiple items."""

    world: World
    capacity: int
    contents: list[Item]

    def __init__(self: Self, world: World, capacity: int):
        self.world = world
        self.capacity = capacity
        self.contents = []

    def __len__(self: Self) -> int:
        """Returns current capacity."""
        return len(self.contents)

    def __iter__(self: Self) -> Iterator[Item]:
        """Iterates over items in inventory."""
        yield from iter(self.contents)

    def __repr__(self: Self) -> str:
        output: str = f"Inventory({len(self)}/{self.capacity})\n"
        output += "[" + ", ".join(map(lambda i: i.name, self.contents)) + "]"
        return output

    def add(self: Self, item: Item) -> None:
        """Adds Item to inventory with respect to capacity."""
        if len(self) < self.capacity:
            self.contents.append(item)
        else:
            raise Exception(self.world.l10n.format_value(
                "inventory-capacity",
                {"capacity": self.capacity, },
            ))

    def get(self: Self, item_name: str) -> Item:
        """Returns item from inventory based on item name."""
        for item in self.contents:
            if item.name == item_name:
                self.contents.remove(item)
                return item
        raise Exception(self.world.l10n.format_value(
            "inventory-item-not-found",
            {"item": item_name, },
        ))

    def on_look(self: Self) -> str:
        return self.world.l10n.format_value(
            "inventory-look-message",
            { "items": ", ".join(map(str, self)), },
        )
