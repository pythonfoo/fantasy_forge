from __future__ import annotations

from typing import Self, Iterator

from .item import Item
from .world import World


class Inventory:
    """An Inventory contains multiple items."""

    world: World
    capacity: int
    contents: dict[str, Item]

    def __init__(self: Self, world: World, capacity: int):
        self.world = world
        self.capacity = capacity
        self.contents = {}

    def __len__(self: Self) -> int:
        """Returns current capacity."""
        return len(self.contents)

    def __iter__(self: Self) -> Iterator[Item]:
        """Iterates over items in inventory."""
        yield from self.contents.values()

    def __repr__(self: Self) -> str:
        output: str = f"Inventory({len(self)}/{self.capacity})\n"
        output += "[" + ", ".join(self.contents.keys()) + "]"
        return output

    def add(self: Self, item: Item) -> None:
        """Adds Item to inventory with respect to capacity."""
        assert item.name not in self.contents
        if len(self) < self.capacity:
            self.contents[item.name] = item
        else:
            raise Exception(self.world.l10n.format_value(
                "inventory-capacity",
                {"capacity": self.capacity, },
            ))

    def on_look(self: Self) -> str:
        return self.world.l10n.format_value(
            "inventory-look-message",
            { "items": ", ".join(map(str, self)), },
        )
