from typing import Self
from model import Inventory, Item, Person

BASE_INVENTORY_CAPACITY = 10
BASE_PLAYER_HEALTH = 100


class Player(Person):
    main_hand: Item
    inventory: Inventory

    def __init__(self: Self, name: str, health: int = BASE_PLAYER_HEALTH):
        super().__init__(name, health)
        self.inventory = Inventory(BASE_INVENTORY_CAPACITY)

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

    def attack(self, target: Person):
        """Player attacks Person using his main hand."""
        print(f"{self.name} attacks {target.name} with {self.main_hand.name}")
        damage = self.main_hand.damage
        target.health = target.health - damage

        if target.health:
            print(f"{target} remains at {target.health} health points")
        else:
            print(f"{target} vanished.")
