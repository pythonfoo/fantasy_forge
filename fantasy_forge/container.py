from typing import Self

from .entity import Entity
from .inventory import Inventory


class Container(Entity, Inventory):
    __important_attributes__ = ("name", "capacity")

    def __init__(self: Self, name: str, description: str, capacity: int):
        super(Container, self).__init__(name, description)
        super(Entity, self).__init__(capacity)
