from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Self

import toml

from fantasy_forge.area import Area
from fantasy_forge.utils import get_fluent_locale

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


class World:
    """A world contains many rooms. It's where the game happens."""
    l10n: FluentLocalization
    areas: dict[str, Area]
    name: str
    spawn: str  # area name to spawn in

    def __init__(
        self: Self, l10n: FluentLocalization, name: str, areas: dict[str, Area], spawn: str
    ):
        self.l10n = l10n
        self.name = name
        self.areas = areas
        self.spawn = spawn

    @property
    def spawn_point(self) -> Area:
        """Returns spawnpoint as area."""
        return self.areas[self.spawn]

    @staticmethod
    def load(name: str) -> World:
        path = Path("data/worlds") / name
        if not path.exists():
            logger.debug(f"Path {path} not found, using {name}")
            path = Path(name)
        areas: dict[str, Area] = dict()
        with (path / "world.toml").open() as world_file:
            world_toml = toml.load(world_file)
            language: str = world_toml["language"]
            world_name: str = world_toml["name"]
            l10n: FluentLocalization = get_fluent_locale(language)
            logger.debug("language")
            logger.debug(language)
            world_spawn: str = world_toml["spawn"]
            world = World(l10n, world_name, areas, world_spawn)
            for area_name in world_toml["areas"]:
                areas[area_name] = Area.load(world, path, area_name)
        return world

if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization