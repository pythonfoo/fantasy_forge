from typing import Any, Self

from fantasy_forge.entity import Entity
from fantasy_forge.inventory import Inventory
from fantasy_forge.world import World


class Container(Entity, Inventory):
    __important_attributes__ = ("name", "capacity")

    def __init__(self: Self, world: World, config_dict: dict[str, Any]):
        capacity: int = config_dict.get("capacity", 10)
        Entity.__init__(world, capacity)
        Inventory.__init__(world, config_dict)
