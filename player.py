from model import Inventory, Item, NPC

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

    def attack(self, target: NPC):
        """Player attacks NPC using his main hand."""
        print(f"{self.name} attacks {target.name} with {self.main_hand.name}")
        damage = self.main_hand.damage
        target.health = target.health - damage

        if target.health:
            print(f"{target} remains at {target.health} health points")
        else:
            print(f"{target} vanished.")
