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
        super(Container, self).__init__(capacity, l10n)
        super(Entity, self).__init__(config_dict, l10n)


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
