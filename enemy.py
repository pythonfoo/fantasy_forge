from typing import Self

from character import Character
from inventory import Inventory
from weapon import Weapon

BASE_DAMAGE = 1


class Enemy(Character):
    """An enemy is a person which will fight back."""

    weapon: Weapon | None
    loot: Inventory

    def __init__(self: Self, name: str, description: str, health: int):
        super().__init__(name, description, health)
        self.weapon = None
        self.loot = Inventory(5)

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
        print(f"{self.name} attacks {target.name} using {self.weapon}")
