from typing import Self

from .area import Area
from .character import Character
from .enemy import BASE_DAMAGE
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
    main_hand: Item | None
    inventory: Inventory

    def __init__(self: Self, world: World, name: str, health: int = BASE_PLAYER_HEALTH):
        super().__init__(world, name, world.l10n.format_value("player-description"), health)
        self.area = Area.empty(world)
        # put us in the void
        # We will (hopefully) never see this, but it's important for the
        # transition to the next area.
        self.area.contents.append(self)
        self.main_hand = None
        self.inventory = Inventory(world, BASE_INVENTORY_CAPACITY)

    def __repr__(self: Self) -> str:
        return f"Player({self.name}, {self.health})"

    def look_at(self, obj: object):
        """Calls the on_look method of an object."""
        print(self.world.l10n.format_value(
            "look-at-message",
            { "player": self.name, "object": obj, },
        ))
        print(obj.on_look())

    def pick_up(self, item: Item):
        """Picks up item and puts it into the inventory."""
        self.inventory.add(item)
        print(self.world.l10n.format_value(
            "pick-up-item-message",
            { "player": self.name, "item": item.name, },
        ))

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
    
    def enter_area(self, new_area: Area):
        # leave the previous area
        self.area.contents.remove(self)
        self.area = new_area
        # enter the new one
        self.area.contents.append(self)
        print(self.world.l10n.format_value(
            "enter-area-message",
            {"area": self.area.name, },
        ))
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
