from __future__ import annotations

from typing import Iterator, Self, TYPE_CHECKING

from fantasy_forge.entity import Entity
from fantasy_forge.localization import highlight_interactive


class Inventory(Entity):
    """An Inventory contains multiple entities."""

    capacity: int
    contents: dict[str, Entity]
    l10n: FluentLocalization

    __important_attributes__ = ("name", "capacity")
    __attributes__ = {**Entity.__attributes__, "capacity": int}

    def __init__(self: Self, config_dict: dict, l10n: FluentLocalization):
        self.capacity = config_dict.pop("capacity")
        self.contents = {}
        super().__init__(config_dict, l10n)

    def __len__(self: Self) -> int:
        """Returns current capacity."""
        return len(self.contents)

    def __iter__(self: Self) -> Iterator[Entity]:
        """Iterates over entities in inventory."""
        yield from self.contents.values()

    def __contains__(self: Self, other: str) -> bool:
        """Returns if entity is in inventory."""
        return other in self.contents.keys()

    def add(self: Self, entity: Entity) -> None:
        """Adds Item to inventory with respect to capacity."""
        assert entity.name not in self.contents
        if len(self) < self.capacity:
            self.contents[entity.name] = entity
        else:
            raise Exception(
                self.world.l10n.format_value(
                    "inventory-capacity-message",
                    {
                        "capacity": self.capacity,
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

    def on_look(self: Self) -> str:
        if not self.contents:
            return self.world.l10n.format_value("inventory-look-empty-message")
        else:
            return self.world.l10n.format_value(
                "inventory-look-message",
                {
                    "items": ", ".join(
                        [highlight_interactive(str(item)).format(None) for item in self]
                    ),
                },
            )

    def to_dict(self) -> dict:
        """Returns inventory as a dictionary."""
        entity_dict: dict = super().to_dict()
        inventory_dict: dict = {**entity_dict, "capacity": self.capacity}
        return inventory_dict


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
