import logging

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
from fantasy_forge.utils import WORLDS_FOLDER
from fantasy_forge.weapon import Weapon

logger = logging.getLogger(__name__)

ASSET_TYPES: dict[str, type] = {
    "areas": Area,
    "armour": Armour,
    "characters": Character,
    "containers": Container,
    "enemies": Enemy,
    "entities": Entity,
    "gateways": Gateway,
    "inventories": Inventory,
    "items": Item,
    "keys": Key,
    "players": Player,
    "weapons": Weapon,
}


def init_flat_folder_structure(world_name: str):
    """Generates flat directory structure for asset types."""
    world_path = WORLDS_FOLDER / world_name
    world_path.mkdir()
    for cls_dir in ASSET_TYPES:
        (world_path / cls_dir).mkdir()


def init_nested_folder_structure(world_name: str):
    """Generates nested directory structure based on class inheritance."""
    world_path = WORLDS_FOLDER / world_name

    asset_type: type
    for asset_type in ASSET_TYPES.values():
        current: type = asset_type
        path_str: str = current.__name__
        while True:
            bases: tuple[type, ...] = current.__bases__
            if object in bases:
                break
            else:
                current = bases[0]
                path_str = f"{current.__name__}/{path_str}"
        path = world_path / path_str
        path.mkdir(parents=True, exist_ok=True)
