from __future__ import annotations

import logging
import toml

from collections import defaultdict
from pathlib import Path
from typing import Any, Optional, Self, TYPE_CHECKING
from importlib import resources

from fantasy_forge.area import Area
from fantasy_forge.load_assets import ASSET_TYPES
from fantasy_forge.utils import WORLDS_FOLDER
from fantasy_forge.messages import Messages


logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


class World:
    """A world contains many rooms. It's where the game happens."""

    l10n: FluentLocalization

    name: str
    areas: dict[str, Area]
    spawn_str: str  # area name to spawn in
    spawn: Optional[Area]
    intro_text: str
    messages: Messages
    assets: dict[str, list[ASSET_TYPE]]  # store of all loaded assets

    def __init__(
        self: Self,
        l10n: FluentLocalization,
        name: str,
        areas: dict[str, Area],
        spawn_str: str,
        intro_text: str,
    ):
        self.l10n = l10n
        self.name = name
        self.areas = areas
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
        fluent_loader = FluentResourceLoader(str(locale_path))
        path = Path("data/worlds") / name
        if not path.exists():
            logger.debug(f"Path {path} not found, using {name}")
            path = Path(name)
        areas: dict[str, Area] = dict()
        with (path / "world.toml").open() as world_file:
            world_toml = toml.load(world_file)
            logger.debug("language")
            logger.debug(world_toml["language"])
            l10n = FluentLocalization(
                locales=[world_toml["language"]],
                resource_ids=["main.ftl"],
                resource_loader=fluent_loader,
                functions={
                    "INTER": highlight_interactive,
                    "NUM": highlight_number,
                    "EXISTS": check_exists,
                },
            )
            world_spawn: str = world_toml["spawn"]
            world = World(
                l10n, world_toml["name"], areas, world_spawn, world_toml["intro_text"]
            )
            for area_name in world_toml["areas"]:
                areas[area_name] = Area.load(world.messages, path, area_name)
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
                asset = asset_type.from_dict(toml_data, self.l10n)
            else:
                logger.info("skipped %s", toml_path.name)
                continue

            self.assets[asset_type.__name__].append(asset)

    def resolve(self):
        for area in self.areas.values():
            for entity in area.contents.values():
                entity.resolve(self)

        self.spawn = self.areas[self.spawn_str]

    @property
    def spawn_point(self) -> Area:
        """Returns spawnpoint as area."""
        return self.areas[self.spawn]

if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
