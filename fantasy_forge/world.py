from __future__ import annotations

from pathlib import Path
from typing import Any, Self

import huepy
import toml
from fluent.runtime import FluentLocalization, FluentResourceLoader
from fluent.runtime.types import FluentNone

from .area import Area


class World:
    """A world contains many rooms. It's where the game happens."""

    def __init__(
        self: Self, l10n: FluentLocalization, name: str, areas: dict[str, Area]
    ):
        self.l10n = l10n
        self.name = name
        self.areas = areas

    @property
    def spawn_point(self) -> Area:
        assert len(self.areas) > 0, "World has no areas"
        return self.areas[list(self.areas.keys())[0]]  # TODO

    @staticmethod
    def load(name: str) -> World:
        fluent_loader = FluentResourceLoader("l10n/{locale}")
        path = Path("worlds") / name
        if not path.exists():
            path = Path(name)
        areas: dict[str, Area] = dict()
        with (path / "world.toml").open() as world_file:
            world_toml = toml.load(world_file)
            l10n = FluentLocalization(
                locales=[world_toml["language"]],
                resource_ids=["main.ftl"],
                resource_loader=fluent_loader,
                functions={
                    "INTER": highlight_interactive,
                    "NUM": highlight_number,
                },
            )
            world = World(l10n, world_toml["name"], areas)
            for area_name in world_toml["areas"]:
                areas[area_name] = Area.load(world, path, area_name)
        return world

def highlight_interactive(text: Any) -> FluentNone:
    """INTER() for the localization"""
    return FluentNone(huepy.bold(huepy.green(str(text))))

def highlight_number(text: Any) -> FluentNone:
    """NUM() for the localization"""
    return FluentNone(huepy.bold(huepy.orange(str(text))))
