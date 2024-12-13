from typing import Self, Any

from fantasy_forge.entity import Entity
from fantasy_forge.inventory import Inventory
from fantasy_forge.world import World


class Container(Entity, Inventory):
    __important_attributes__ = ("name", "capacity")

    def __init__(self: Self, world: World, config_dict: dict[str, Any]):
        capacity: int = config_dict.get("capacity", 10)
        super(Container, self).__init__(world, capacity)
        super(Entity, self).__init__(world, config_dict)
