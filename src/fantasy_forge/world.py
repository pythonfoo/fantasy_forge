from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Self

import toml

from fantasy_forge.area import Area
from fantasy_forge.localization import get_fluent_locale

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


class World:
    """A world contains many rooms. It's where the game happens."""

    l10n: FluentLocalization
    areas: dict[str, Area]
    name: str
    spawn: str  # area name to spawn in

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

    @property
    def spawn_point(self) -> Area:
        """Returns spawnpoint as area."""
        return self.areas[self.spawn]

    @staticmethod
    def load(name: str) -> World:
        world_path = Path("data/worlds") / name

        if not world_path.exists():
            logger.debug(f"Path {world_path} not found, using {name}")
            world_path = Path(name)

        areas: dict[str, Area] = dict()

        world_toml_path: Path = world_path / "world.toml"
        with world_toml_path.open() as world_file:
            world_toml_data: dict = toml.load(world_file)

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


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
