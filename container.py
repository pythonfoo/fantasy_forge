from typing import Self

from entity import Entity
from inventory import Inventory


class Container(Entity, Inventory):
    def __init__(self: Self, name: str, description: str, capacity: int):
        super(Container, self).__init__(name, description)
        super(Entity, self).__init__(capacity)

    def __repr__(self: Self) -> str:
        return f"Container({self.name}, {self.description}, {self.capacity})"
