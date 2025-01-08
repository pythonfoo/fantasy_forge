"""An Area is a place in the world, containing NPCs, Items and connections to other areas."""

from __future__ import annotations

import logging

from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterator, Self

import toml

from fantasy_forge.entity import Entity

logger = logging.getLogger(__name__)


class Area(Entity):
    """An Area is a place in the world, containing NPCs, Items and connections to other areas."""

    __important_attributes__ = ("name",)
    contents: dict[str, Entity]
    content_refs: list[str]  # names of Entities

    def __init__(self: Self, config_dict: dict[str, Any], l10n: FluentLocalization):
        """
        config_dict contents
        'content_refs' (list[str]): list of contents as  names of Entity objects (default: [])

        inherited from Entity
        'name' (str): name of the entity
        'description' (str): description of the entity (default: "")
        'obvious'(bool): whether the entity will be spotted immediately (default: False)
        """
        self.contents_refs = config_dict.get("content_refs", [])
        self.contents: dict = {}
        super().__init__(config_dict, l10n)

    def __iter__(self: Self) -> Iterator:
        for obj in self.contents:
            yield obj

    def on_look(self: Self) -> str:
        return self.l10n.format_value(
            "look-around-begin",
            {
                "area-name": self.name,
                "area-description": self.description,
            },
        )

    def to_dict(self: Self) -> dict:
        """Return area as a dictionary."""
        area_dict: dict = super().to_dict()
        area_dict["content_refs"] = self.content_refs
        return area_dict

    @staticmethod
    def load(world, root_path: Path, name: str):
        """Loads an area from toml-file."""
        path = root_path / "areas" / f"{name}.toml"
        with path.open() as area_file:
            area_toml = toml.load(area_file)
        return Area.from_dict(area_toml, world.l10n)

    @staticmethod
    def empty(l10n: FluentLocalization) -> Area:
        """Return an empty area, this is a placeholder."""
        return Area(
            {
                "name": l10n.format_value("void-name"),
                "description": l10n.format_value("void-description"),
            },
            l10n,
        )


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
