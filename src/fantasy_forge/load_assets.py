import logging
from pathlib import Path

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
from fantasy_forge.player import Player
from fantasy_forge.weapon import Weapon

logger = logging.getLogger(__name__)

ASSET_TYPES: dict[str, type] = {
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
    "Player": Player,
    "Weapon": Weapon,
}

WORLDS_DIR: Path = Path("data/worlds")


def init_flat_folder_structure(world_name: str):
    """Generates flat directory structure for asset types."""
    world_path = WORLDS_DIR / world_name
    world_path.mkdir()
    asset_type: str
    for asset_type in ASSET_TYPES:
        (world_path / asset_type).mkdir()


def init_nested_folder_structure(world_name: str):
    """Generates nested directory structure based on class inheritance."""
    world_path = WORLDS_DIR / world_name

    asset_type: type
    for asset_type in ASSET_TYPES.values():
        current: type = asset_type
        type_hierarchy: list[type] = [current]

        while True:
            bases: tuple[type, ...] = current.__bases__
            if object in bases:
                break
            else:
                current = bases[0]
                type_hierarchy.insert(0, current)

        path_str: str = "/".join((t.__name__ for t in type_hierarchy))
        path: Path = world_path / path_str
        path.mkdir(parents=True, exist_ok=True)
