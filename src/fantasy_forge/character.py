from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from fantasy_forge.entity import Entity
from fantasy_forge.inventory import Inventory
from fantasy_forge.weapon import Weapon

BASE_INVENTORY_CAPACITY = 10


class Character(Entity):
    """A character in the world."""

    __important_attributes__ = ("name", "health", "alive")
    __attributes__ = {**Entity.__attributes__, "health": int, "alive": bool}

    health: int
    inventory: Inventory
    main_hand: Weapon | None
    _alive: bool

    def __init__(
        self: Self, config_dict: dict[str, Any], l10n: FluentLocalization
    ) -> None:
        self.health = config_dict.pop("health")
        self.inventory = Inventory(BASE_INVENTORY_CAPACITY, l10n)
        self.main_hand = None
        super().__init__(config_dict, l10n)

    @property
    def alive(self: Self) -> bool:
        self._alive = self.health > 0
        return self._alive

    def on_attack(self: Self, weapon: Weapon):
        self.health -= weapon.damage


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
