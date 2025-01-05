import logging
from pathlib import Path
from typing import TypeAlias, Union

from fantasy_forge.area import Area
from fantasy_forge.armour import Armour
from fantasy_forge.character import Character
from fantasy_forge.container import Container
from fantasy_forge.enemy import Enemy
from fantasy_forge.entity import Entity
from fantasy_forge.gateway import Gateway
from fantasy_forge.inventory import Inventory
from fantasy_forge.item import Item
from fantasy_forge.key import Key
from fantasy_forge.weapon import Weapon
from fantasy_forge.utils import WORLDS_FOLDER

logger = logging.getLogger(__name__)

ASSET_TYPE: TypeAlias = Union[
    Area,
    Armour,
    Character,
    Container,
    Enemy,
    Entity,
    Gateway,
    Inventory,
    Item,
    Key,
    Weapon,
]

ASSET_TYPE_DICT: dict[str, ASSET_TYPE] = {
    "Area": Area,
    "Armour": Armour,
    "Character": Character,
    "Container": Container,
    "Enemy": Enemy,
    "Entity": Entity,
    "Gateway": Gateway,
    "Inventory": Inventory,
    "Item": Item,
    "Key": Key,
    "Weapon": Weapon,
}


def init_flat_folder_structure(world_name: str):
    """Generates flat directory structure for asset types."""
    world_path = WORLDS_FOLDER / world_name
    world_path.mkdir()
    asset_type: str
    for asset_type in ASSET_TYPE_DICT:
        (world_path / asset_type).mkdir()


def init_nested_folder_structure(world_name: str):
    """Generates nested directory structure based on class inheritance."""
    world_path = WORLDS_FOLDER / world_name

    asset_type: ASSET_TYPE
    for asset_type in ASSET_TYPE_DICT.values():
        path = asset2path(world_name, asset_type)
        path.mkdir(parents=True, exist_ok=True)

def asset2path(world_name: str, asset_type: ASSET_TYPE) -> Path:
    world_path = WORLDS_FOLDER / world_name

    current: ASSET_TYPE = asset_type
    type_hierarchy: list[ASSET_TYPE] = [current]
    while True:
        bases: tuple[ASSET_TYPE, ...] = current.__bases__
        if object in bases:
            break
        current = bases[0]
        type_hierarchy.insert(0, current)
    path_str: str = "/".join((t.__name__ for t in type_hierarchy))
    path: Path = world_path / path_str
    return path