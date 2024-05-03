from __future__ import annotations
from typing import Iterator, Self


class Entity:
    """An Entity is an abstract object in the world."""

    name: str
    description: str

    def __init__(self: Self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def on_look(self: Self) -> str:
        return self.description

    def __repr__(self: Self) -> str:
        return f"Entity({self.name}, {self.description})"

    def __str__(self: Self) -> str:
        return self.name

    def to_dict(self: Self) -> dict:
        entity_dict: dict = {"name": self.name, "description": self.description}
        return entity_dict

    @staticmethod
    def from_dict(entity_dict: dict) -> Entity:
        name: str = entity_dict.get("name", "")
        description: str = entity_dict.get("description", "")
        return Entity(name, description)


class Area(Entity):
    """An Area is a place in the world, containing NPCs, Items and connections to other areas."""

    contents: list

    def __init__(self: Self, name: str, description: str):
        super().__init__(name, description)

    def __iter__(self: Self) -> Iterator:
        for obj in self.contents:
            yield obj

    def __repr__(self: Self) -> str:
        return f"Area({self.name})"

    def on_look(self: Self) -> str:
        output = f"{self.description}\n"
        for obj in self.contents:
            output += f"You see {obj.name}\n"
        return output

    def to_dict(self: Self) -> dict:
        area_dict: dict = super().to_dict()
        area_dict["contents"] = self.contents
        return area_dict

    @staticmethod
    def from_dict(area_dict: dict) -> Area:
        entity: Entity = Entity.from_dict(area_dict)
        contents: list = area_dict.get("contents", [])
        area = Area(entity.name, entity.description)
        area.contents = contents
        return area


class Gateway(Entity):
    """A Gateway is a one-way connection between two areas."""

    source: Area
    target: Area

    def __init__(self: Self, name: str, description: str, source: Area, target: Area):
        super().__init__(name, description)
        self.source = source
        self.target = target

    def __repr__(self: Self) -> str:
        return f"Gateway({self.name}, {self.source} -> {self.target})"

    def on_use(self: Self) -> Area:
        """Returns the target area."""
        return self.target

    def to_dict(self: Self) -> dict:
        gateway_dict: dict = super().to_dict()
        gateway_dict["source"] = self.source
        gateway_dict["target"] = self.target
        return gateway_dict

    @staticmethod
    def from_dict(gateway_dict: dict) -> Gateway:
        entity: Entity = Entity.from_dict(gateway_dict)
        source: Area = gateway_dict.get("source")
        target: Area = gateway_dict.get("target")
        gateway: Gateway = Gateway(entity.name, entity.description, source, target)
        return gateway


class Item(Entity):
    """An Item is an entity which can be picked up by the player."""

    moveable: bool
    carryable: bool

    def __init__(self: Self, name: str, description: str) -> None:
        super().__init__(name, description)
        self.moveable = True
        self.carryable = True

    def __repr__(self: Self) -> str:
        return f"Item({self.name}, {self.description}, moveable={self.moveable}, carryable={self.carryable})"

    def on_pickup(self: Self):
        # TODO
        pass

    def to_dict(self: Self) -> dict:
        item_dict: dict = super().to_dict()
        item_dict["moveable"] = self.moveable
        item_dict["carryable"] = self.carryable
        return item_dict

    @staticmethod
    def from_dict(item_dict: dict) -> Entity:
        entity: Entity = Entity.from_dict(item_dict)
        moveable = item_dict.get("moveable", True)
        carryable = item_dict.get("carryable", True)
        item: Item = Item(entity.name, entity.description, moveable, carryable)
        return item


class Inventory:
    """An Inventory contains multiple items."""

    capacity: int
    contents: list[Item]

    def __init__(self: Self, capacity: int):
        self.capacity = capacity
        self.contents = []

    def __len__(self: Self) -> int:
        """Returns current capacity."""
        return len(self.contents)

    def __iter__(self: Self) -> Iterator[Item]:
        """Iterates over items in inventory."""
        yield from iter(self.contents)

    def __repr__(self: Self) -> str:
        output: str = f"Inventory({len(self)}/{self.capacity})\n"
        output += "[" + ", ".join(map(lambda i: i.name, self.contents)) + "]"
        return output

    def add(self: Self, item: Item) -> None:
        """Adds Item to inventory with respect to capacity."""
        if len(self) < self.capacity:
            self.contents.append(item)
        else:
            raise Exception(f"Maximum capacity ({self.capacity}) reached.")

    def get(self: Self, item_name: str) -> Item:
        """Returns item from inventory based on item name."""
        for item in self.contents:
            if item.name == item_name:
                self.contents.remove(item)
                return item
        raise Exception(f"Item {item_name} couldn't be found.")

    def on_look(self: Self) -> str:
        output = f"In the inventory you find {', '.join(map(str, self))}"
        return output


class Character(Entity):
    """A character in the world."""

    health: int

    def __init__(self: Self, name: str, description: str, health: int) -> None:
        super().__init__(name, description)
        self.health = health

    def __repr__(self: Self) -> str:
        return f"Character({self.name}, {self.description}, {self.health})"


class Weapon(Item):
    """A Weapon is an item, which can deal damage to players or NPCs."""

    damage: int

    def __init__(
        self: Self, name: str, description: str, value: int, damage: int
    ) -> None:
        super().__init__(name, description)
        self.damage = damage


class Enemy(Character):
    """An enemy is a person which will fight back."""

    weapon: Weapon
    loot: Inventory

    def __init__(self: Self, name: str, description: str, health: int):
        super().__init__(name, description, health)
        self.loot = Inventory(5)

    def attack(self: Self, target: Character):
        damage = self.weapon.damage
        target.health = target.health - damage
        print(f"{self.name} attacks {target.name} using {self.weapon}")

    def __str__(self: Self) -> str:
        return self.name

    def __repr__(self: Self) -> str:
        return f"Weapon({self.name}, {self.weapon})"


class Container(Entity, Inventory):
    def __init__(self: Self, name: str, description: str, capacity: int):
        super(Container, self).__init__(name, description)
        super(Entity, self).__init__(capacity)

    def __repr__(self: Self) -> str:
        return f"Container({self.name}, {self.description}, {self.capacity})"
