from __future__ import annotations

from typing import Any, Self, TYPE_CHECKING

from fantasy_forge.entity import Entity


class Item(Entity):
    """An Item is an entity which can be picked up by the player."""

    __important_attributes__ = ("name", "moveable", "carryable")

    moveable: bool
    carryable: bool

    def __init__(
        self: Self, config_dict: dict[str, Any], l10n: FluentLocalization
    ) -> None:
        self.moveable = config_dict.pop("moveable", True)
        self.carryable = config_dict.pop("carryable", True)
        super().__init__(config_dict, l10n)

    def on_pickup(self: Self):
        # TODO
        pass

    def to_dict(self: Self) -> dict:
        item_dict: dict = super().to_dict()
        item_dict["moveable"] = self.moveable
        item_dict["carryable"] = self.carryable
        return item_dict


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
