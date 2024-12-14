from pathlib import Path
from typing import IO, Iterator

import toml
from fluent.runtime import FluentLocalization

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
from fantasy_forge.world import World

ASSET_TYPES: tuple[type] = (
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
    Player,
    Weapon,
)

WORLDS_DIR: Path = Path("data/worlds")


# TODO: save assets in world object

def load_assets(world_name: str) -> Iterator[Entity]:
    world_path = WORLDS_DIR / world_name

    # load world.toml
    world: World = World.load(world_name)

    # load localization
    l10n: FluentLocalization = world.l10n

    # load assets
    path: Path
    asset_type_names = [at.__name__ for at in ASSET_TYPES]
    for path in world_path.glob("**/*.toml"):
        asset_type: type
        parent: str = path.parent.name

        # infer type from parent directory
        if parent in asset_type_names:
            asset_type = globals().get(parent)
        else:
            print(f"skipped {path.name}")
            continue

        # parse asset from toml file
        io: IO
        with path.open("r", encoding="UTF-8") as io:
            content: dict = toml.load(io)

        obj = asset_type.from_dict(content, l10n)
        yield obj


def init_flat_folder_structure(world_name: str):
    """Generates flat directory structure for asset types."""
    world_path = WORLDS_DIR / world_name
    world_path.mkdir()
    for cls_dir in ASSET_TYPES:
        (world_path / cls_dir).mkdir()


def init_nested_folder_structure(world_name: str):
    """Generates nested directory structure based on class inheritance."""
    world_path = WORLDS_DIR / world_name

    asset_type: type
    for asset_type in ASSET_TYPES:
        current: type = asset_type
        type_hierachy: list[type] = [current]

        while True:
            bases: tuple[type, ...] = current.__bases__
            if object in bases:
                break
            else:
                current = bases[0]
                type_hierachy.insert(0, current)

        path_str: str = "/".join((t.__name__ for t in type_hierachy))
        path: Path = world_path / path_str
        path.mkdir(parents=True, exist_ok=True)
