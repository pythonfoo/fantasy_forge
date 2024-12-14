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
    world_path = WORLDS_FOLDER / world_name
    world_path.mkdir()
    for cls_dir, cls in ASSET_TYPES.items():
        (world_path / cls_dir).mkdir()
