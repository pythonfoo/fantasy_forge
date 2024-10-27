from typing import Self

from fantasy_forge.area import Area
from fantasy_forge.armour import ARMOUR_TYPES, Armour
from fantasy_forge.character import Character
from fantasy_forge.enemy import BASE_DAMAGE
from fantasy_forge.entity import Entity
from fantasy_forge.gateway import Gateway
from fantasy_forge.item import Item
from fantasy_forge.shell import Shell
from fantasy_forge.weapon import Weapon
from fantasy_forge.world import World

BASE_PLAYER_HEALTH = 100


def BARE_HANDS(world: World):
    return Weapon(
        world,
        {
            "name": world.l10n.format_value("bare-hands-name"),
            "description": world.l10n.format_value("bare-hands-description"),
            "damage": BASE_DAMAGE,
        },
    )


class Player(Character):
    __important_attributes__ = ("name", "area", "health")

    area: Area  # the area we are currently in
    seen_entities: dict[str, Entity]
    armour_slots: dict[str, Armour]

    def __init__(self: Self, world: World, name: str, health: int = BASE_PLAYER_HEALTH):
        super().__init__(
            world,
            dict(
                name=name,
                description=world.l10n.format_value("player-description"),
                health=health,
            ),
        )
        self.area = Area.empty(world)
        # put us in the void
        # We will (hopefully) never see this, but it's important for the
        # transition to the next area.
        self.area.contents[self.name] = self
        self.seen_entities = {}

        # define armour slots
        for armour_type in ARMOUR_TYPES:
            self.armour_slots[armour_type] = None

    def look_around(self):
        """Player looks around the current area."""
        # clear seen items, but re-add inventory items
        self.seen_entities.clear()
        for item in self.inventory:
            self.seen_entities[item.name] = item
        print(self.area.on_look())
        for entity in self.area.contents.values():
            if entity is self:
                continue
            print(
                self.world.l10n.format_value(
                    "look-around-single",
                    {
                        "object": entity.name,
                    },
                )
            )
            self.seen_entities[entity.name] = entity

    def look_at(self, name: str):
        """Calls the on_look method of an object."""
        entity = self.seen_entities.get(name)
        if entity is None:
            print(
                self.world.l10n.format_value(
                    "entity-not-seen",
                    {
                        "entity": name,
                    },
                )
            )
            return
        print(
            self.world.l10n.format_value(
                "look-at-message",
                {
                    "object": entity.name,
                },
            )
        )
        print(entity.on_look())

    def pick_up(self, item_name: str):
        """Picks up item and puts it into the inventory."""
        item = self.seen_entities.get(item_name)
        if item is None:
            print(
                self.world.l10n.format_value(
                    "entity-does-not-exist",
                    {"entity": item_name},
                )
            )
            return
        if item_name not in self.area.contents:
            if item_name in self.inventory.contents:
                print(self.world.l10n.format_value("item-is-in-inventory"))
                return
            print(self.world.l10n.format_value("item-vanished"))
            self.seen_entities.pop(item_name)
            return
        if isinstance(item, Item) and item.carryable:
            self.inventory.add(item)
            # picking up items keeps them in seen_entities
            self.area.contents.pop(item_name)
            print(
                self.world.l10n.format_value(
                    "pick-up-item-message",
                    {
                        "item": item.name,
                    },
                )
            )
        else:
            print(self.world.l10n.format_value("pick-up-failed-message"))

    def equip(self, item_name: str):
        """Equips item."""
        item = self.seen_entities.get(item_name)
        # check if item was already seen
        if item is None:
            print(
                self.world.l10n.format_value(
                    "entity-does-not-exist",
                    {"entity": item_name},
                )
            )
            return
        # item must be in the area or the inventory to be equiped
        if (
            item_name not in self.area.contents
            and item_name not in self.inventory.contents
        ):
            print(self.world.l10n.format_value("item-vanished"))
            self.seen_entities.pop(item_name)
            return

        # by equipping the item is implicitly picked up
        if item not in self.inventory.contents.values():
            # if it's not already in the inventory, place it there
            self.inventory.add(item)
            # picking up items keeps them in seen_entities
            self.area.contents.pop(item_name)
            print(
                self.world.l10n.format_value(
                    "pick-up-item-message",
                    {
                        "item": item.name,
                    },
                )
            )
        if isinstance(item, Weapon):
            self.equip_weapon(item)
        elif isinstance(item, Armour):
            self.equip_armour(item)
        else:
            print(
                self.world.l10n.format_value(
                    "cannot-equip",
                    {
                        "weapon": item.name,
                    },
                )
            )

    def equip_weapon(self, weapon: Weapon):
        """Equips weapon."""
        self.main_hand = weapon
        print(
            self.world.l10n.format_value(
                "equip-item-message",
                {
                    "player": self.name,
                    "item": weapon.name,
                },
            )
        )

    def equip_armour(self, armour: Armour) -> None:
        """Equips armour piece."""
        # TODO
        pass

    # TODO: Refactor
    def attack(self, target_name: str) -> None:
        """Player attacks character using their main hand."""
        target = self.seen_entities.get(target_name)
        if target is None:
            print(
                self.world.l10n.format_value(
                    "entity-does-not-exist",
                    {"entity": target_name},
                )
            )
            return
        if not isinstance(target, Character):
            print(
                self.world.l10n.format_value("cannot-attack", {"target": target_name})
            )
            return
        if target_name not in self.area.contents:
            print(self.world.l10n.format_value("item-vanished"))
            self.seen_entities.pop(target_name)
            return
        if self.main_hand is None:
            weapon = BARE_HANDS(self.world)
        else:
            weapon = self.main_hand
        print(
            self.world.l10n.format_value(
                "attack-character-message",
                {
                    "source": self.name,
                    "target": target.name,
                    "weapon": weapon.name,
                },
            )
        )
        target.on_attack(weapon)

        if target.alive:
            # give the enemy an option for revenge
            target.attack(self)
            print(
                self.world.l10n.format_value(
                    "attack-character-alive-message",
                    {
                        "target": target.name,
                        "health": target.health,
                    },
                )
            )
        else:
            print(
                self.world.l10n.format_value(
                    "attack-character-dead-message",
                    {
                        "target": target.name,
                    },
                )
            )
            # if the target is dead, remove it from the area and drop their inventory
            self.area.contents.pop(target.name)
            self.seen_entities.pop(target.name)
            print(
                self.world.l10n.format_value(
                    "attack-drop-begin",
                    {
                        "target": target.name,
                        "loot_count": len(target.inventory),
                    },
                )
            )
            for loot_item in target.inventory:
                self.area.contents[loot_item.name] = loot_item
                self.seen_entities[loot_item.name] = loot_item
                print(
                    self.world.l10n.format_value(
                        "attack-drop-single",
                        {"item": loot_item.name},
                    )
                )

        if self.alive:
            print(
                self.world.l10n.format_value(
                    "player-health-remaining",
                    {"health": self.health},
                )
            )
        else:
            print(self.world.l10n.format_value("player-died"))
            exit()

    def use(self, subject_name: str, other_name: str | None = None):
        subject = self.seen_entities.get(subject_name)
        if subject is None:
            print(
                self.world.l10n.format_value(
                    "entity-not-seen",
                    {
                        "entity": subject_name,
                    },
                )
            )
            return

        if other_name is None:
            subject.on_use()
            return

        other = self.seen_entities.get(other_name)
        if other is None:
            print(
                self.world.l10n.format_value(
                    "entity-not-seen",
                    {
                        "entity": other_name,
                    },
                )
            )
            return
        # It makes more sense to implement the key logic in the gateway
        other.on_use(other=subject)

    def go(self, gateway_name: str):
        """
        Go through a gateway.

        This is like enter_area, but takes a string.
        """
        gateway = self.seen_entities.get(gateway_name)
        if gateway is None:
            print(
                self.world.l10n.format_value(
                    "entity-does-not-exist",
                    {"entity": gateway_name},
                )
            )
            return
        if gateway_name not in self.area.contents:
            print(self.world.l10n.format_value("item-vanished"))
            self.seen_entities.pop(gateway_name)
            return
        if isinstance(gateway, Gateway):
            self.enter_gateway(gateway)
        else:
            print(self.world.l10n.format_value("go-failed-message"))

    def enter_gateway(self: Self, gateway: Gateway):
        """Uses gateway to enter a new area."""
        if gateway.locked:
            print(
                self.world.l10n.format_value(
                    "gateway-locked-message",
                    {
                        "gateway": gateway.name,
                    },
                )
            )
            return
        area = self.world.areas[gateway.target]
        self.enter_area(area)

    def enter_area(self, new_area: Area):
        """Enters a new area."""
        # leave the previous area
        self.area.contents.pop(self.name)
        self.area = new_area
        # clear seen items, but re-add inventory items
        self.seen_entities.clear()
        for item in self.inventory:
            self.seen_entities[item.name] = item
        # enter the new one
        self.area.contents[self.name] = self
        print(
            self.world.l10n.format_value(
                "enter-area-message",
                {
                    "area": self.area.name,
                },
            )
        )
        for entity in self.area.contents.values():
            if entity.obvious:
                print(
                    self.world.l10n.format_value(
                        "look-around-single",
                        {
                            "object": entity.name,
                        },
                    )
                )
                self.seen_entities[entity.name] = entity
        # TODO: output better text

    def drop(self, item_name: str):
        """Drops item from inventory or main hand to the area."""
        item = self.inventory.pop(item_name)
        if item is None:
            print(
                self.world.l10n.format_value(
                    "drop-not-found",
                    {
                        "item": item_name,
                    },
                )
            )
            return
        self.area.contents[item.name] = item  # adds item to current area
        if self.main_hand is item:  # clears main hand if item was dropped from it
            self.main_hand = None
        print(
            self.world.l10n.format_value(
                "dropped",
                {
                    "item": item_name,
                },
            )
        )

    def main_loop(self):
        """Runs the game."""
        self.enter_area(self.world.spawn_point)
        Shell(self).cmdloop()
        # afterwards, leave the current area for the void
        self.enter_area(Area.empty(self.world))
        print(
            self.world.l10n.format_value(
                "quit-game-message",
                {},
            )
        )
