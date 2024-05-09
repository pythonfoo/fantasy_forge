from __future__ import annotations

from pathlib import Path
from typing import Self

import toml

from .area import Area


class World:
    """A world contains many rooms. It's where the game happens."""
    def __init__(self, name: str, areas: dict[str, Area]):
        self.name = name
        self.areas = areas
    
    @property
    def spawn_point(self) -> Area:
        assert len(self.areas) > 0, "World has no areas"
        return self.areas[list(self.areas.keys())[0]]  # TODO

    @staticmethod
    def load(name: str) -> World:
        path = Path("worlds") / name
        if not path.exists():
            path = Path(name)
        areas = dict()
        with (path / "world.toml").open() as world_file:
            world_toml = toml.load(world_file)
            for area_name in world_toml["areas"]:
                areas[area_name] = Area.load(path, area_name)
        return World(world_toml["name"], areas)
