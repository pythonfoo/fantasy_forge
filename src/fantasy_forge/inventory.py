from __future__ import annotations

from typing import TYPE_CHECKING, Iterator, Self

from fantasy_forge.item import Item
from fantasy_forge.localization import highlight_interactive


class Inventory:
    """An Inventory contains multiple items."""

    capacity: int
    contents: dict[str, Item]
    l10n: FluentLocalization

    def __init__(self: Self, capacity: int, l10n: FluentLocalization):
        self.capacity = capacity
        self.contents = {}
        self.l10n = l10n

    def __len__(self: Self) -> int:
        """Returns current capacity."""
        return len(self.contents)

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

    def add(self: Self, item: Item) -> None:
        """Adds Item to inventory with respect to capacity."""
        assert item.name not in self.contents
        if len(self) < self.capacity:
            self.contents[item.name] = item
        else:
            raise Exception(
                self.l10n.format_value(
                    "inventory-capacity-message",
                    {
                        "capacity": self.capacity,
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
            return self.l10n.format_value("inventory-look-empty-message")
        else:
            return self.l10n.format_value(
                "inventory-look-message",
                {
                    "items": ", ".join(
                        [highlight_interactive(str(item)).format(None) for item in self]
                    ),
                },
            )

    @classmethod
    def from_dict(cls, inventory_dict: dict, l10n: FluentLocalization) -> Self:
        capacity = inventory_dict.get("capacity", 10)
        inventory: Inventory = cls(capacity, l10n)
        return inventory


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
