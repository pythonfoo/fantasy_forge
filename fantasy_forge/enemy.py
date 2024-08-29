from typing import Any, Self

from .character import Character
from .inventory import Inventory
from .weapon import Weapon
from .world import World

BASE_DAMAGE = 1


class Enemy(Character):
    """An enemy is a person which will fight back."""

    weapon: Weapon | None
    loot: Inventory

    def __init__(self: Self, world: World, config_dict: dict[str, Any]):
        super().__init__(world, config_dict)
        self.weapon = None
        self.loot = Inventory(world, 5)

    def __str__(self: Self) -> str:
        return self.name

    def attack(self: Self, target: Character):
        if self.weapon is None:
            damage = BASE_DAMAGE
        else:
            damage = self.weapon.damage
        target.health = target.health - damage
        print(
            self.world.l10n.format_value(
                "attack-character-message",
                {
                    "source": self.name,
                    "target": target.name,
                    "weapon": getattr(self.weapon, "name", None),
                },
            )
        )
