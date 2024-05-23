from typing import Self

from .area import Area
from .character import Character
from .enemy import BASE_DAMAGE
from .entity import Entity
from .gateway import Gateway
from .inventory import Inventory
from .item import Item
from .shell import Shell
from .weapon import Weapon
from .world import World

BASE_INVENTORY_CAPACITY = 10
BASE_PLAYER_HEALTH = 100

def BARE_HANDS(l10n):
    return Weapon(
        l10n.format_value("bare-hands-name"),
        l10n.format_value("bare-hand-description"),
        BASE_DAMAGE,
    )


class Player(Character):
    area: Area  # the area we are currently in
    seen_entities: dict[str, Entity]
    main_hand: Item | None
    inventory: Inventory

    def __init__(self: Self, world: World, name: str, health: int = BASE_PLAYER_HEALTH):
        super().__init__(world, name, world.l10n.format_value("player-description"), health)
        self.area = Area.empty(world)
        # put us in the void
        # We will (hopefully) never see this, but it's important for the
        # transition to the next area.
        self.area.contents[self.name]=self
        self.seen_entities = dict()
        self.main_hand = None
        self.inventory = Inventory(world, BASE_INVENTORY_CAPACITY)

    def __repr__(self: Self) -> str:
        return f"Player({self.name}, {self.health})"

    def look_around(self):
        self.seen_entities.clear()
        print(self.area.on_look())
        for entity in self.area.contents.values():
            print(self.world.l10n.format_value(
                "look-around-single",
                { "object": entity.name, },
            ))
            self.seen_entities[entity.name] = entity

    def look_at(self, name: str):
        """Calls the on_look method of an object."""
        entity = self.seen_entities.get(name)
        if entity is None:
            print(self.world.l10n.format_value(
                "entity-not-seen",
                {"entity": name, },
            ))
            return
        print(self.world.l10n.format_value(
            "look-at-message",
            { "object": entity.name, },
        ))
        print(entity.on_look())

    def pick_up(self, item_name: str):
        """Picks up item and puts it into the inventory."""
        item = self.seen_entities.get(item_name)
        if item is None:
            print(
                self.world.l10n.format_value(
                    "item-does-not-exist",
                    {"item": item_name},
                )
            )
            return
        if item_name not in self.area.contents:
            print(self.world.l10n.format_value("item-vanished"))
            self.seen_entities.pop(item_name)
            return
        if isinstance(item, Item) and item.carryable:
            self.inventory.add(item)
            self.seen_entities.pop(item_name)
            self.area.contents.pop(item_name)
            print(self.world.l10n.format_value(
                "pick-up-item-message",
                { "item": item.name, },
            ))
        else:
            print(
                self.world.l10n.format_value("pick-up-failed-message")
            )

    def equip(self, item_name: str):
        """Gets an item from player inventory and puts it in the main hand."""
        item = self.inventory.get(item_name)
        self.main_hand = item
        print(self.world.l10n.format_value(
            "equip-item-message",
            { "player": self.name, "item": item.name, },
        ))

    def attack(self, target: Character) -> None:
        """Player attacks character using their main hand."""
        weapon: Item
        if self.main_hand is None or not hasattr(self.main_hand, "damage"):
            weapon = BARE_HANDS(self.world.l10n)
        else:
            weapon = self.main_hand
        print(self.world.l10n.format_value(
            "attack-character-message",
            { "source": self.name, "target": target.name, "weapon": weapon.name, },
        ))
        target.on_attack(weapon)

        if target.alive:
            print(self.world.l10n.format_value(
                "attack-character-alive-message",
                { "target": target.name, "health": target.health, },
            ))
        else:
            print(self.world.l10n.format_value(
                "attack-character-dead-message",
                { "target": target.name, },
            ))
            # TODO
    
    def go(self, gateway_name: str):
        """
        Go through a gateway.
        
        This is like enter_area, but takes a string.
        """
        gateway = self.seen_entities.get(gateway_name)
        if gateway is None:
            print(
                self.world.l10n.format_value(
                    "item-does-not-exist",
                    {"item": gateway_name},
                )
            )
            return
        if gateway_name not in self.area.contents:
            print(self.world.l10n.format_value("item-vanished"))
            self.seen_entities.pop(gateway_name)
            return 
        if isinstance(gateway, Gateway):
            self.enter_area(self.world.areas[gateway.target])
        else:
            print(
                self.world.l10n.format_value("go-failed-message")
            )
    
    def enter_area(self, new_area: Area):
        # leave the previous area
        self.area.contents.pop(self.name)
        self.area = new_area
        # clear seen items
        self.seen_entities.clear()
        # enter the new one
        self.area.contents[self.name] = self
        print(self.world.l10n.format_value(
            "enter-area-message",
            {"area": self.area.name, },
        ))
        for entity in self.area.contents.values():
            if entity.obvious:
                print(self.world.l10n.format_value(
                    "look-around-single",
                    { "object": entity.name, },
                ))
                self.seen_entities[entity.name] = entity
        # TODO: output better text
    
    def main_loop(self):
        """Runs the game."""
        self.enter_area(self.world.spawn_point)
        Shell(self).cmdloop()
        # afterwards, leave the current area for the void
        self.enter_area(Area.empty(self.world))
        print(self.world.l10n.format_value(
            "quit-game-message", {},
        ))
