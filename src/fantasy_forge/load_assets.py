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


def iter_assets(world_name: str) -> Iterator[tuple[type, Path]]:
    world_path = WORLDS_DIR / world_name

    # iterate through world dir
    path: Path
    for path in world_path.glob("**/*.toml"):
        asset_type: type
        parent: str = path.parent.name

        # infer type from parent directory
        if parent in ASSET_TYPES.keys():
            asset_type = ASSET_TYPES[parent]
        else:
            # TODO: proper logging
            print(f"skipped {path.name}")
            continue

        yield asset_type, path


# TODO: save assets in world object
def load_assets(world_name: str) -> Iterator[Entity]:
    # load world.toml
    world: World = World.load(world_name)

    # load localization
    l10n: FluentLocalization = world.l10n

    for asset_type, path in iter_assets(world_name):
        # parse asset from toml file
        io: IO
        with path.open("r", encoding="UTF-8") as io:
            content: dict = toml.load(io)

        if hasattr(asset_type, "from_dict"):
            obj = asset_type.from_dict(content, l10n)
            yield obj
        else:
            # TODO: proper logging
            print(f"skipped {asset_type}")


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
