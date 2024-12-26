from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from fantasy_forge.entity import Entity
from fantasy_forge.inventory import Inventory


class Container(Entity, Inventory):
    __important_attributes__ = ("name", "capacity")

    def __init__(
        self: Self, config_dict: dict[str, Any], l10n: FluentLocalization
    ) -> None:
        capacity: int = config_dict.get("capacity", 10)
        Inventory.__init__(self, capacity, l10n)
        Entity.__init__(self, config_dict, l10n)

    @staticmethod
    def from_dict(container_dict, l10n) -> Container:
        container: Container = Container(container_dict, l10n)
        return container


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
