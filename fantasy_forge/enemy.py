from typing import Self

from .character import Character
from .inventory import Inventory
from .weapon import Weapon
from .world import World

BASE_DAMAGE = 1


class Enemy(Character):
    """An enemy is a person which will fight back."""

    weapon: Weapon | None
    loot: Inventory

    def __init__(self: Self, world: World, name: str, description: str, health: int):
        super().__init__(world, name, description, health)
        self.weapon = None
        self.loot = Inventory(world, 5)

    def __str__(self: Self) -> str:
        return self.name

    def __repr__(self: Self) -> str:
        return f"Weapon({self.name}, {self.weapon}, alive={self.alive})"

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
                    "weapon": self.weapon.name,
                },
            )
        )
