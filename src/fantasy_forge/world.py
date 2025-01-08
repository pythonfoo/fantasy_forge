from __future__ import annotations

import logging
from pathlib import Path
from typing import IO, TYPE_CHECKING, Iterator, Self

from toml import load

from fantasy_forge.area import Area
from fantasy_forge.folder_structure import AssetType, ASSET_TYPE_DICT
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
    store: dict[str, AssetType]  # stores all assets

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

        self.store = {}
        self._load_assets()

        # populate areas dict
        area: Area
        for area in self.filter(Area):
            for ref in area.contents_refs:
                # load entity from asset store into area
                area.contents[ref.name] = self[ref.name]
            # save area in areas dict
            self.areas[area.name] = area

    @property
    def spawn_point(self) -> Area:
        """Returns spawnpoint as area."""
        return self.areas[self.spawn]

    @staticmethod
    def load(name: str) -> World:
        world_path = WORLDS_FOLDER / name

        if not world_path.exists():
            logger.debug(
                "Path %(world_path) not found, using %(name)",
                {"world_path": world_path, "name": name},
            )
            world_path = Path(name)

        world_toml_path: Path = world_path / "world.toml"
        with world_toml_path.open() as world_file:
            world_toml_data: dict = load(world_file)

        world_name: str = world_toml_data["name"]
        assert world_name == name

        areas: dict[str, Area] = {}

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
            asset_type: type
            parent: str = toml_path.parent.name

            # infer type from parent directory
            if parent in ASSET_TYPE_DICT:
                asset_type = ASSET_TYPE_DICT[parent]
            else:
                logger.info("skipped %s", toml_path.name)
                continue

            # read toml
            io: IO
            with toml_path.open(encoding="utf-8") as io:
                toml_data: dict = load(io)

            # parse asset from toml data
            if hasattr(asset_type, "from_dict"):
                asset = asset_type.from_dict(toml_data, self.l10n)
            else:
                logger.info("skipped %s", toml_path.name)
                continue

            assert asset.name not in self.store
            self.store[asset.name] = asset

    def __iter__(self) -> Iterator[AssetType]:
        yield from self.store.values()

    def __contains__(self, asset_key: str):
        return asset_key in self.store

    def __getitem__(self, asset_key: str) -> AssetType | None:
        return self.store.get(asset_key)

    def add_asset(self, asset: AssetType) -> None:
        assert asset.name not in self.store
        self.store[asset.name] = asset

    def pop_asset(self, asset_key: str) -> AssetType | None:
        if asset_key in self.store:
            asset: AssetType = self.store.pop(asset_key)
            return asset

        return None

    def filter(self, wanted_type: type) -> Iterator[AssetType]:
        yield from (asset for asset in self if isinstance(asset, wanted_type))


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
