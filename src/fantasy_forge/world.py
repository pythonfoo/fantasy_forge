from __future__ import annotations

import logging
from collections import defaultdict
from pathlib import Path
from typing import IO, TYPE_CHECKING, Iterator, Self

from toml import load

from fantasy_forge.area import Area
from fantasy_forge.folder_structure import ASSET_TYPE, ASSET_TYPE_DICT
from fantasy_forge.localization import get_fluent_locale
from fantasy_forge.utils import WORLDS_FOLDER

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


class World:
    """A world contains many rooms. It's where the game happens."""

    l10n: FluentLocalization
    name: str
    areas: dict[str, Area]
    spawn: str  # area name to spawn in
    assets: dict[str, list[ASSET_TYPE]]  # store of all loaded assets

    def __init__(
        self: Self,
        l10n: FluentLocalization,
        name: str,
        areas: dict[str, Area],
        spawn: str,
    ):
        self.l10n = l10n
        self.name = name
        self.areas = areas
        self.spawn = spawn

        self.assets = defaultdict(list)
        self._load_assets()

    @property
    def spawn_point(self) -> Area:
        """Returns spawnpoint as area."""
        return self.areas[self.spawn]

    @staticmethod
    def load(name: str) -> World:
        world_path = WORLDS_FOLDER / name

        if not world_path.exists():
            logger.debug(f"Path {world_path} not found, using {name}")
            world_path = Path(name)

        areas: dict[str, Area] = dict()

        world_toml_path: Path = world_path / "world.toml"
        with world_toml_path.open() as world_file:
            world_toml_data: dict = load(world_file)

            world_name: str = world_toml_data["name"]
            assert world_name == name

            # load language for localization
            language: str = world_toml_data["language"]
            l10n: FluentLocalization = get_fluent_locale(language)
            logger.debug("language")
            logger.debug(language)

            world_spawn: str = world_toml_data["spawn"]
            world = World(l10n, world_name, areas, world_spawn)
        return world

    def _load_assets(self):
        world_path = WORLDS_FOLDER / self.name

        # iterate through world dir
        toml_path: Path
        for toml_path in world_path.glob("**/*.toml"):
            asset_type: ASSET_TYPE
            parent: str = toml_path.parent.name

            # infer type from parent directory
            if parent in ASSET_TYPE_DICT.keys():
                asset_type = ASSET_TYPE_DICT[parent]
            else:
                logger.info("skipped " + toml_path.name)
                continue

            # read toml
            io: IO
            with toml_path.open(encoding="utf-8") as io:
                toml_data: dict = load(io)

            # parse asset from toml data
            if hasattr(asset_type, "from_dict"):
                asset = asset_type.from_dict(toml_data, self.l10n)
            else:
                logger.info("skipped " + toml_path.name)
                continue

            self.assets[asset_type.__name__].append(asset)

    def iter_assets(self) -> Iterator[ASSET_TYPE]:
        for assets in self.assets.values():
            yield from assets

    def get_asset(self, asset_name: str, asset_type: str = "") -> ASSET_TYPE:
        if asset_type:
            assets = self.assets[asset_type]
        else:
            assets = self.iter_assets()

        for asset in assets:
            if asset.__name__ == asset_name:
                return asset


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
