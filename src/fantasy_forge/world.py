from __future__ import annotations

import logging
import toml

from collections import defaultdict
from pathlib import Path
from typing import Container, Optional, Self, TYPE_CHECKING
from importlib import resources

from fantasy_forge.area import Area
from fantasy_forge.armour import Armour
from fantasy_forge.character import Character
from fantasy_forge.enemy import Enemy
from fantasy_forge.entity import Entity
from fantasy_forge.gateway import Gateway
from fantasy_forge.inventory import Inventory
from fantasy_forge.item import Item
from fantasy_forge.key import Key
from fantasy_forge.localization import get_fluent_locale
from fantasy_forge.player import Player
from fantasy_forge.utils import WORLDS_FOLDER
from fantasy_forge.messages import Messages
from fantasy_forge.utils import UniqueDict
from fantasy_forge.weapon import Weapon


logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

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

class World:
    """A world contains many rooms. It's where the game happens."""

    l10n: FluentLocalization
    areas: UniqueDict[str, Area]
    messages: Messages
    name: str
    spawn_str: str  # area name to spawn in
    spawn: Optional[Area]
    intro_text: str
    assets: dict[str, list[ASSET_TYPE]]  # store of all loaded assets

    def __init__(
        self: Self,
        l10n: FluentLocalization,
        name: str,
        spawn_str: str,
        intro_text: str,
    ):
        self.l10n = l10n
        self.name = name
        self.areas = UniqueDict()
        self.spawn_str = spawn_str
        self.spawn = None
        self.intro_text = intro_text
        self.messages = Messages(l10n)
        
        self.assets = defaultdict(list)
        self._load_assets()
        
        # populate areas dict
        for area in self.assets["Area"]:
            self.areas[area.name] = area
        
    @staticmethod
    def load(name: str) -> World:
        with resources.as_file(resources.files()) as resource_path:
            locale_path = resource_path / "l10n/{locale}"
        path = Path("data/worlds") / name
        if not path.exists():
            logger.debug(f"Path {path} not found, using {name}")
            path = Path(name)
        with (path / "world.toml").open() as world_file:
            world_toml = toml.load(world_file)
            logger.debug("language")
            logger.debug(world_toml["language"])
            l10n = get_fluent_locale(locale_path)
            world_spawn: str = world_toml["spawn"]
            world = World(
                l10n, world_toml["name"], world_spawn, world_toml["intro_text"],
            )
        world.resolve()
        return world
            
    def _load_assets(self):
        world_path = WORLDS_FOLDER / self.name

        # iterate through world dir
        toml_path: Path
        for toml_path in world_path.glob("**/*.toml"):
            asset_type: type
            parent: str = toml_path.parent.name

            # infer type from parent directory
            if parent in ASSET_TYPES.keys():
                asset_type = ASSET_TYPES[parent]
            else:
                logger.info("skipped %s", toml_path.name)
                continue

            # read toml
            io: IO
            with toml_path.open(encoding="utf-8") as io:
                toml_data: dict = toml.load(io)

            # parse asset from toml data
            if hasattr(asset_type, "from_dict"):
                asset = asset_type.from_dict(self.messages, toml_data)
            else:
                logger.info("skipped %s", toml_path.name)
                continue

            self.assets[asset_type.__name__].append(asset)

    @property
    def players(self: Self) -> list[Player]:
        players = []
        for area in self.areas.values():
            players += area.players

        return players

    def resolve(self):
        for area in self.areas.values():
            for entity in area.contents.values():
                entity.resolve(self)

        self.spawn = self.areas[self.spawn_str]

if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
