from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from fantasy_forge.item import Item


class Weapon(Item):
    """A Weapon is an item, which can deal damage to players or NPCs."""

    __important_attributes__ = ("name", "damage")

    damage: int

    def __init__(
        self: Self, config_dict: dict[str, Any], l10n: FluentLocalization
    ) -> None:
        self.damage = config_dict.pop("damage")
        super().__init__(config_dict, l10n)


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
