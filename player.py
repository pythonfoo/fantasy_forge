from model import Inventory

BASE_INVENTORY_CAPACITY = 10


class Player:
    name: str
    inventory: Inventory

    def __init__(self, name):
        self.name = name
        self.inventory = Inventory(BASE_INVENTORY_CAPACITY)

    def look_at(self, obj: object):
        """Prints the description of an object."""
        print(f"{self.name} looks at {obj.name}")
        print(obj.on_look())

    def pick_up(self, item_name: str):
        self.inventory.add(item_name)
        print(f"{self.name} picked up {item_name} and put the item in the inventory.")
