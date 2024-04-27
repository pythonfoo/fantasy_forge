from model import Inventory, Item

BASE_INVENTORY_CAPACITY = 10


class Player:
    name: str
    main_hand: Item
    inventory: Inventory

    def __init__(self, name):
        self.name = name
        self.inventory = Inventory(BASE_INVENTORY_CAPACITY)

    def look_at(self, obj: object):
        """Prints the description of an object."""
        print(f"{self.name} looks at {obj}")
        print(obj.on_look())

    def pick_up(self, item_name: str):
        self.inventory.add(item_name)
        print(f"{self.name} picked up {item_name} and put the item in the inventory.")

    def equip(self, item_name: str):
        """Gets an item from player inventory and puts it in the main hand."""
        item = self.inventory.get(item_name)
        self.main_hand = item
        print(f"{self.name} equipped {item.name}")
