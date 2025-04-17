from __future__ import annotations

import random
from typing import TYPE_CHECKING, Self

from fantasy_forge.area import Area
from fantasy_forge.armour import ARMOUR_TYPES, Armour
from fantasy_forge.character import Character, bare_hands
from fantasy_forge.entity import Entity
from fantasy_forge.gateway import Gateway
from fantasy_forge.inventory import Inventory, InventoryFull, InventoryTooSmall
from fantasy_forge.item import Item
from fantasy_forge.shell import Shell
from fantasy_forge.weapon import Weapon

if TYPE_CHECKING:
    from fantasy_forge.world import World


BASE_PLAYER_HEALTH = 100


class Player(Character):
    __important_attributes__ = ("name", "area", "health")

    area: Area  # the area we are currently in
    shell: Shell
    seen_entities: dict[str, Entity]
    armour_slots: dict[str, Armour]
    world: World

    def __init__(
        self: Self,
        world: World,
        name: str,
        description: int,
        health: int = BASE_PLAYER_HEALTH,
    ):
        super().__init__(
            world.messages,
            dict(
                name=name,
                description=description,
                health=health,
            ),
            world.l10n,
        )
        self.world = world
        self.area = Area.empty(world.messages)

        # put us in the void
        # We will (hopefully) never see this, but it's important for the
        # transition to the next area.
        self.area.contents[self.name] = self
        self.seen_entities = {}

        # define armour slots
        self.armour_slots: dict[str, Armour | None] = {}
        for armour_type in ARMOUR_TYPES:
            self.armour_slots[armour_type] = None

    @property
    def defense(self) -> int:
        defense_sum: int = 0
        armour_item: Armour | None
        for armour_item in self.armour_slots.values():
            if armour_item is not None:
                defense_sum += armour_item.defense
        return defense_sum

    def look_around(self):
        """Player looks around the current area."""
        # clear seen items, but re-add inventory items
        self.seen_entities.clear()
        for item in self.inventory:
            self.seen_entities[item.name] = item
        self.area.on_look(self)
        for entity in self.area.contents.values():
            if entity is self:
                continue
            self.messages.to(
                [self],
                "look-around-single",
                object=entity.name,
            )
            self.seen_entities[entity.name] = entity

    def inspect(self, name: str):
        """Calls the on_look method of an object."""
        entity = self.seen_entities.get(name)
        if entity is None:
            self.messages.to(
                [self],
                "entity-not-seen",
                entity=name,
            )
            return
        self.messages.to(
            [self],
            "look-at-message",
            object=entity.name,
        )
        entity.on_look(self)

    def pick_up(self, item_name: str):
        """Picks up item and puts it into the inventory."""
        item = self.seen_entities.get(item_name)
        if item is None:
            self.messages.to([self], "entity-does-not-exist", entity=item_name)
            return
        if item_name not in self.area.contents:
            if item_name in self.inventory.contents:
                self.messages.to([self], "item-is-in-inventory")
                return
            self.messages.to([self], "item-vanished")
            self.seen_entities.pop(item_name)
            return
        if isinstance(item, Item) and item.carryable:
            try:
                self.inventory.add(item)
            except InventoryFull:
                self.messages.to([self], "pick-up-failed-inv-full")
            except InventoryTooSmall:
                self.messages.to([self], "pick-up-failed-inv-too-small")
            else:
                # picking up items keeps them in seen_entities
                self.area.contents.pop(item_name)
            self.messages.to(
                [self],
                "pick-up-item-message",
                item=item.name,
            )
        else:
            self.messages.to([self], "pick-up-failed-message")

    def equip(self, item_name: str):
        """Equips item."""
        item = self.seen_entities.get(item_name)
        # check if item was already seen
        if item is None:
            self.messages.to(
                [self],
                "entity-does-not-exist",
                entity=item_name,
            )
            return
        # item must be in the area or the inventory to be equipped
        if (
            item_name not in self.area.contents
            and item_name not in self.inventory.contents
        ):
            self.messages.to([self], "item-vanished")
            self.seen_entities.pop(item_name)
            return

        # by equipping the item is implicitly picked up
        if item not in self.inventory.contents.values():
            # if it's not already in the inventory, place it there
            self.inventory.add(item)
            # picking up items keeps them in seen_entities
            self.area.contents.pop(item_name)
            self.messages.to(
                [self],
                "pick-up-item-message",
                item=item.name,
            )
        if isinstance(item, Weapon):
            self.equip_weapon(item)
        elif isinstance(item, Armour):
            self.equip_armour(item)
        else:
            self.messages.to(
                [self],
                "cannot-equip",
                weapon=item.name,
            )

    def equip_weapon(self, weapon: Weapon):
        """Equips weapon."""
        self.main_hand = weapon
        self.messages.to(
            [self],
            "equip-item-message",
            player=self.name,
            item=weapon.name,
        )

    def equip_armour(self, armour: Armour) -> None:
        """Equips armour piece."""
        current_armour: Armour | None = self.armour_slots.pop(armour.armour_type)
        # check if armour slot is already filled
        if current_armour is not None:
            self.messages.to(
                [self],
                "unequip-item-message",
                player=self.name,
                item=armour.name,
            )

        self.armour_slots[armour.armour_type] = armour
        self.messages.to(
            [self],
            "equip-item-message",
            player=self.name,
            item=armour.name,
        )

    def unequip(self, item_name: str):
        """Unequips weapon or armour."""
        if not item_name:
            self.messages.to([self], "unequip-nothing-message")
            return
        if item_name in self.seen_entities and item_name in self.inventory.contents:
            item = self.seen_entities.get(item_name)
        else:
            self.messages.to([self], "entity-does-not-exist", entity=item_name)
            return
        if self.main_hand is item:
            self.main_hand = None
        for armour_type, armour_item in self.armour_slots.items():
            if armour_item is item:
                self.armour_slots[armour_type] = None
        self.messages.to(
            [self],
            "unequip-item-message",
            player=self.name,
            item=item.name,
        )

    # TODO: Refactor
    def attack(self, target_name: str) -> None:
        """Player attacks character using their main hand."""
        target = self.seen_entities.get(target_name)
        if target is None:
            self.messages.to(
                [self],
                "entity-does-not-exist",
                entity=target_name,
            )
            return
        if target_name not in self.area.contents:
            self.messages.to([self], "item-vanished")
            self.seen_entities.pop(target_name)
            return
        if not isinstance(target, Character):
            self.messages.to([self], "cannot-attack", target=target_name)
            return
        super().attack(target)

        if target.alive and hasattr(target, "attack"):
            # give the enemy an option for revenge
            target.attack(self)
            self.messages.to(
                [self],
                "attack-character-alive-message",
                target=target.name,
                health=target.health,
            )
        else:
            target._on_death(self)
        if self.alive:
            self.messages.to(
                [self],
                "player-health-remaining",
                health=self.health,
            )
        else:
            # self._on_death(self)
            self.messages.to([self], "player-died")
            exit()

    def use(self, subject_name: str, other_name: str | None = None):
        subject = self.seen_entities.get(subject_name)
        if subject is None:
            self.messages.to(
                [self],
                "entity-not-seen",
                entity=subject_name,
            )
            return

        if other_name is None:
            subject.on_use(self)
            return

        other = self.seen_entities.get(other_name)
        if other is None:
            self.messages.to(
                [self],
                "entity-not-seen",
                entity=other_name,
            )
            return
        # It makes more sense to implement the key logic in the gateway
        other.on_use(self, other=subject)

    def go(self, gateway_name: str):
        """
        Go through a gateway.

        This is like enter_area, but takes a string.
        """
        gateway = self.seen_entities.get(gateway_name)
        if gateway is None:
            self.messages.to(
                [self],
                "entity-does-not-exist",
                entity=gateway_name,
            )
            return
        if gateway_name not in self.area.contents:
            self.messages.to([self], "item-vanished")
            self.seen_entities.pop(gateway_name)
            return
        if isinstance(gateway, Gateway):
            self.enter_gateway(gateway)
        else:
            self.messages.to([self], "go-failed-message")

    def enter_gateway(self: Self, gateway: Gateway):
        """Uses gateway to enter a new area."""
        # TODO: refactor
        # The Player holds no reference to the current world,
        # so a external function should do the area change

        if gateway.locked:
            self.messages.to(
                [self],
                "gateway-locked-message",
                gateway=gateway.name,
            )
            return
        self.enter_area(gateway.target)

    def enter_area(self, new_area: Area):
        """Enters a new area."""
        # leave the previous area
        self.leave_area()
        # enter new area
        self.area = new_area
        # clear seen items, but re-add inventory items
        self.seen_entities.clear()
        for item in self.inventory:
            self.seen_entities[item.name] = item
        # enter the new one
        self.area.contents[self.name] = self
        self.messages.to(
            [self],
            "enter-area-message",
            area=self.area.name,
        )
        for entity in self.area.contents.values():
            if entity.obvious:
                self.messages.to(
                    [self],
                    "look-around-single",
                    object=entity.name,
                )
                self.seen_entities[entity.name] = entity
        # TODO: output better text

    def leave_area(self):
        """Leave current area."""
        self.area.contents.pop(self.name)

    def drop(self, item_name: str):
        """Drops item from inventory or main hand to the area."""
        item = self.inventory.pop(item_name)
        if item is None:
            self.messages.to(
                [self],
                "drop-not-found",
                item=item_name,
            )
            return
        self.area.contents[item.name] = item  # adds item to current area
        if self.main_hand is item:  # clears main hand if item was dropped from it
            self.main_hand = None
        self.messages.to(
            [self],
            "dropped",
            item=item_name,
        )

    def shout(self: Self, message: str) -> None:
        for area in self.world.areas.values():
            self.messages.to(
                area.players, "player-shouts", player=self.name, message=message
            )

    def say(self: Self, message: str) -> None:
        self.messages.to(
            self.area.players, "player-says", player=self.name, message=message
        )

    def whisper(self: Self, target: str, message: str) -> None:
        for player in self.area.players:
            if player.name == target:
                self.messages.to(
                    [player, self],
                    "player-whispers",
                    player=self.name,
                    target=target,
                    message=message,
                )
                break
        else:
            self.messages.to([self], "whisper-target-nonexistant")

    def main_loop(self, stdin=None, stdout=None):
        """Runs the game."""
        if stdout is None:
            print(self.world.intro_text)
        else:
            stdout.write(self.world.intro_text + "\n")
        self.shell = Shell(self.world.messages, self, stdin=stdin, stdout=stdout)
        self.enter_area(self.world.spawn)
        self.shell.cmdloop()
        # afterwards, leave the current area
        self.leave_area()
        quit_message = random.choice(
            [
                "quit-game-message-light",
                "quit-game-message-dark",
                "quit-game-message-turtles",
                "quit-game-message-fractals",
                "quit-game-message-treasure",
                "quit-game-message-cat",
                "quit-game-message-dog",
                "quit-game-message-dream",
            ]
        )
        self.messages.to([self], quit_message)
