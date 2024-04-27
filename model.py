from typing import Iterator


class Area:
    """An Area is a place in the world, containing NPCs, Items and connections to other areas."""

    name: str
    description: str
    contents: list

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def on_look(self) -> str:
        output = f"{self.description}\n"
        for obj in self.contents:
            output += f"You see {obj.name}\n"
        return output

    def __iter__(self) -> Iterator:
        for obj in self.contents:
            yield obj

    def __repr__(self) -> str:
        return f"Area({self.name})"

    def __str__(self) -> str:
        return self.name


class Gateway:
    """A Gateway connects two areas."""

    name: str
    description: str
    source: Area
    target: Area

    def __init__(self, name: str, source: Area, target: Area):
        self.name = name
        self.source = source
        self.target = target

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Gateway({self.name}, {self.source} -> {self.target})"


class Item:
    """An Item is an object with which players and NPC can interact with."""

    name: str
    description: str
    value: int

    def __init__(self, name: str, description: str, value: int) -> None:
        self.name = name
        self.description = description
        self.value = value

    def on_look(self) -> str:
        return self.description

    def __repr__(self) -> str:
        return f"Item({self.name}, {self.description}, {self.value})"

    def __str__(self) -> str:
        return self.name


class Inventory:
    """An Inventory contains multiple items."""

    capacity: int
    contents: list[Item]

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.contents = []

    def add(self, item: Item) -> None:
        """Adds Item to inventory with respect to capacity."""
        if len(self) < self.capacity:
            self.contents.append(item)
        else:
            raise Exception(f"Maximum capacity ({self.capacity}) reached.")

    def get(self, item_name: str) -> Item:
        """Returns item from inventory based on item name."""
        for item in self.contents:
            if item.name == item_name:
                self.contents.remove(item)
                return item
        raise Exception(f"Item {item_name} couldn't be found.")

    def on_look(self) -> str:
        output = f"In the inventory you find {', '.join(map(str, self))}"
        return output

    def __len__(self) -> int:
        """Returns current capacity."""
        return len(self.contents)

    def __iter__(self) -> Iterator[Item]:
        """Iterates over items in inventory."""
        for item in self.contents:
            yield item

    def __repr__(self) -> str:
        output: str = f"Inventory({len(self)}/{self.capacity})\n"
        output += "[" + ", ".join(map(lambda i: i.name, self.contents)) + "]"
        return output


class NPC:
    """A non player character is a person in the world.

    The Player might interact with NPCs.
    """

    name: str
    health: int

    def __init__(self, name: str, health: int) -> None:
        self.name = name
        self.health = health

    def __str__(self) -> str:
        return self.name


class Weapon(Item):
    """A Weapon is an item, which can deal damage to players or NPCs."""

    damage: int

    def __init__(self, name: str, description: str, value: int, damage: int) -> None:
        super().__init__(name, description, value)
        self.damage = damage
