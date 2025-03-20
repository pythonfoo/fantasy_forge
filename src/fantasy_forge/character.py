from __future__ import annotations

from typing import Any, Self

from fantasy_forge.entity import Entity
from fantasy_forge.inventory import Inventory
from fantasy_forge.weapon import Weapon
from fantasy_forge.world import World

BASE_INVENTORY_CAPACITY = 10
BASE_DAMAGE = 1

def bare_hands(world: World):
    return Weapon(
        world,
        {
            "name": world.l10n.format_value("bare-hands-name"),
            "description": world.l10n.format_value("bare-hands-description"),
            "damage": BASE_DAMAGE,
        },
    )

class Character(Entity):
    """A character in the world."""

    __important_attributes__ = ("name", "health", "alive")

    health: int
    inventory: Inventory
    main_hand: Weapon | None
    _alive: bool

    def __init__(self: Self, world: World, config_dict: dict[str, Any]) -> None:
        self.health = config_dict.pop("health")
        self.inventory = Inventory(world, BASE_INVENTORY_CAPACITY)
        self.main_hand = None
        super().__init__(world, config_dict)

    @property
    def alive(self: Self) -> bool:
        self._alive = self.health > 0
        return self._alive

    def attack(self: Self, target: Character) -> None:
        if self.main_hand is None:
            weapon = bare_hands(self.world)
        else:
            weapon = self.main_hand
        target.on_attack(weapon)     
        print(
            self.world.l10n.format_value(
                "attack-character-message",
                {
                    "source": self.name,
                    "target": target.name,
                    "weapon": getattr(weapon, "name", None),
                },
            )
        )

    def on_attack(self: Self, weapon: Weapon):
        self.health -= weapon.damage
