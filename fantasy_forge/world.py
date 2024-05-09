from __future__ import annotations

from pathlib import Path
from typing import Self

import toml

from .area import Area


class World:
    """A world contains many rooms. It's where the game happens."""
    def __init__(self, name: str, areas: list[Area]):
        self.name = name
        self.areas = areas

    @staticmethod
    def load(name: str) -> World:
        path = Path("worlds") / name
        if not path.exists():
            path = Path(name)
        areas = []
        with (path / "world.toml").open() as world_file:
            world_toml = toml.load(world_file)
            for area_name in world_toml["areas"]:
                areas.append(Area.load(path, area_name))
        return World(world_toml["name"], areas)
