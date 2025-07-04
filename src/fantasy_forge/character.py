"""Character class

A character is a living entity, which can interact with other entities or characters.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from fantasy_forge.entity import Entity
from fantasy_forge.inventory import Inventory
from fantasy_forge.messages import Messages
from fantasy_forge.weapon import Weapon

BASE_INVENTORY_CAPACITY = 10
BASE_DAMAGE = 1


def bare_hands(messages: Messages):
    return Weapon(
        messages,
        {
            "name": messages.l10n.format_value("bare-hands-name"),
            "description": messages.l10n.format_value("bare-hands-description"),
            "damage": BASE_DAMAGE,
        },
    )


class Character(Entity):
    """A character in the world."""

    __important_attributes__ = ("name", "health", "alive")
    __attributes__ = {**Entity.__attributes__, "health": int, "alive": bool}

    health: int
    inventory: Inventory
    main_hand: Weapon | None
    _alive: bool

    def __init__(self: Self, messages: Messages, config_dict: dict[str, Any]) -> None:
        """
        config_dict contents
        'health' (int): health points

        inherited from Entity:
        'name' (str): name of the entity
        'description' (str): description of the entity (default: "")
        'obvious'(bool): whether the entity will be spotted immediately (default: False)
        """
   
        self.health = config_dict.pop("health")
        self.inventory = Inventory(messages, BASE_INVENTORY_CAPACITY)
        self.main_hand = None
        super().__init__(messages, config_dict)

    @property
    def alive(self: Self) -> bool:
        """Return True if the character is alive."""
        self._alive = self.health > 0
        return self._alive

    def attack(self: Self, target: Character) -> None:
        if self.main_hand is None:
            weapon = bare_hands(self.messages)
        else:
            weapon = self.main_hand
        target.on_attack(weapon)
        self.messages.to(
            [self, target],
            "attack-character-message",
            source=self.name,
            target=target.name,
            weapon=getattr(weapon, "name", None),
        )

    def on_attack(self: Self, weapon: Weapon):
        """Handles an incoming attack."""
        self.health -= weapon.damage

    def _on_death(self: Self, player: Player):
        """
        Automatic on death call.
        """
        assert self is not player
        assert not self.alive, "On_death called while entity is alive"
        self.messages.to(
            [player],
            "attack-character-dead-message",
            target=self.name,
        )
        # Populate area with loot
        self.messages.to(
            [player],
            "attack-drop-begin",
            target=self.name,
            loot_count=len(self.inventory),
        )
        for loot_item in self.inventory.pop_all():
            player.area.contents[loot_item.name] = loot_item
            player.seen_entities[loot_item.name] = loot_item

            self.messages.to(
                [player],
                "attack-drop-single",
                item=loot_item.name,
            )
        # if the target is dead, remove it from the area
        del player.area.contents[self.name]
        del player.seen_entities[self.name]


if TYPE_CHECKING:
    from fantasy_forge.player import Player
