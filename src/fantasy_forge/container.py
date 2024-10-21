from typing import Self

from fantasy_forge.entity import Entity
from fantasy_forge.inventory import Inventory


class Container(Entity, Inventory):
    __important_attributes__ = ("name", "capacity")

    def __init__(self: Self, name: str, description: str, capacity: int):
        super(Container, self).__init__(name, description)
        super(Entity, self).__init__(capacity)
