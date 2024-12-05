from typing import Any, Self

from fantasy_forge.character import Character
from fantasy_forge.item import Item
from fantasy_forge.world import World

BASE_DAMAGE = 1


class Enemy(Character):
    """An enemy is a person which will fight back."""

    def __init__(self: Self, world: World, config_dict: dict[str, Any]):
        super().__init__(world, config_dict)
        for item_dict in config_dict.get("loot", []):
            self.inventory.add(Item(world, item_dict))

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
