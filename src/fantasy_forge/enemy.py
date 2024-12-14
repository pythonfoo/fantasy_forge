from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from fantasy_forge.character import Character
from fantasy_forge.item import Item

BASE_DAMAGE = 1


class Enemy(Character):
    """An enemy is a person which will fight back."""

    def __init__(self: Self, config_dict: dict[str, Any], l10n: FluentLocalization):
        super().__init__(config_dict, l10n)
        for item_dict in config_dict.get("loot", []):
            self.inventory.add(Item(item_dict, l10n))

    def __str__(self: Self) -> str:
        return self.name

    def attack(self: Self, target: Character):
        if self.main_hand is None:
            damage = BASE_DAMAGE
        else:
            damage = self.main_hand.damage
        target.health = target.health - damage
        print(
            self.world.l10n.format_value(
                "attack-character-message",
                {
                    "source": self.name,
                    "target": target.name,
                    "weapon": getattr(self.main_hand, "name", None),
                },
            )
        )

    @staticmethod
    def from_dict(enemy_dict: dict, l10n: FluentLocalization) -> Enemy:
        enemy = Enemy(enemy_dict, l10n)
        return enemy

if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
