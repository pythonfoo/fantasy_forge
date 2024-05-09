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

BARE_HANDS = Weapon("bare hands", "the harmful hands of the player", BASE_DAMAGE)


class Player(Character):
    world: World
    area: Area  # the area we are currently in
    main_hand: Item | None
    inventory: Inventory

    def __init__(self: Self, world: World, name: str, health: int = BASE_PLAYER_HEALTH):
        super().__init__(name, "the heroic player", health)
        self.world = world
        self.area = Area.empty()
        # put us in the void
        # We will (hopefully) never see this, but it's important for the
        # transition to the next area.
        self.area.contents.append(self)
        self.main_hand = None
        self.inventory = Inventory(BASE_INVENTORY_CAPACITY)

    def __repr__(self: Self) -> str:
        return f"Player({self.name}, {self.health})"

    def look_at(self, obj: object):
        """Calls the on_look method of an object."""
        print(f"{self.name} looks at {obj}")
        print(obj.on_look())

    def pick_up(self, item: Item):
        """Picks up item and puts it into the inventory."""
        self.inventory.add(item)
        print(f"{self.name} picked up {item.name} and put the item in the inventory.")

    def equip(self, item_name: str):
        """Gets an item from player inventory and puts it in the main hand."""
        item = self.inventory.get(item_name)
        self.main_hand = item
        print(f"{self.name} equipped {item.name}")

    def attack(self, target: Character):
        """Player attacks character using his main hand."""
        weapon: Item
        if self.main_hand is None or not hasattr(self.main_hand, "damage"):
            weapon = BARE_HANDS
        else:
            weapon = self.main_hand
        print(f"{self.name} attacks {target.name} with {weapon.name}")
        target.on_attack(weapon)

        if target.alive:
            print(f"{target} remains at {target.health} health points")
        else:
            print(f"{target} vanished.")
    
    def enter_area(self, new_area: Area):
        # leave the previous area
        self.area.contents.remove(self)
        self.area = new_area
        # enter the new one
        self.area.contents.append(self)
        print(f"You are now in {self.area}.")
        # TODO: output better text
    
    def main_loop(self):
        """Runs the game."""
        self.enter_area(self.world.spawn_point)
        Shell(self).cmdloop()
