from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from fantasy_forge.item import Item
from fantasy_forge.inventory import Inventory


class Container(Inventory, Item):
    __attributes__ = {**Inventory.__attributes__, **Item.__attributes__}

    def __init__(
        self: Self, config_dict: dict[str, Any], l10n: FluentLocalization
    ) -> None:
        Inventory.__init__(self, config_dict, l10n)
        Item.__init__(self, config_dict, l10n)

if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
