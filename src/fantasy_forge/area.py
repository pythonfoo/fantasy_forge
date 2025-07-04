"""An Area is a place in the world, containing NPCs, Items and connections to other areas."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterator, Self

import toml

from fantasy_forge.entity import Entity
from fantasy_forge.utils import UniqueDict, inflate_contents

logger = logging.getLogger(__name__)


class Area(Entity):
    """An Area is a place in the world, containing NPCs, Items and connections to other areas."""

    __important_attributes__ = ("name",)
    contents: UniqueDict[str, Entity]

    def __init__(self: Self, messages: Messages, config_dict: dict[str, Any]):
        """
        config_dict contents

        inherited from Entity
        'name' (str): name of the entity
        'description' (str): description of the entity (default: "")
        'obvious'(bool): whether the entity will be spotted immediately (default: False)
        """
        super().__init__(messages, config_dict)
        self.contents = UniqueDict()

    def __iter__(self: Self) -> Iterator:
        for obj in self.contents:
            yield obj

    @property
    def players(self: Self) -> list[Player]:
        from fantasy_forge.player import Player

        return [
            player for player in self.contents.values() if isinstance(player, Player)
        ]

    def on_look(self: Self, actor: Player):
        self.messages.to(
            [actor],
            "look-around-begin",
            area_name=self.name,
            area_description=self.description,
        )

    def to_dict(self: Self) -> dict:
        area_dict: dict = super().to_dict()
        area_dict["contents"] = self.contents
        return area_dict

    @staticmethod
    def from_dict(messages: Messages, area_dict: dict) -> Area:
        area = Area(messages, area_dict)
        inflate_contents(messages, area_dict.get("contents", []), area)
        return area

    @staticmethod
    def load(messages: Messages, root_path: Path, name: str):
        path = root_path / "areas" / f"{name}.toml"
        with path.open() as area_file:
            area_toml = toml.load(area_file)
        return Area.from_dict(messages, area_toml)

    @staticmethod
    def empty(messages: Messages) -> Area:
        """Return an empty area, this is a placeholder."""
        return Area(
            messages,
            dict(
                name=messages.l10n.format_value("void-name"),
                description=messages.l10n.format_value("void-description"),
            ),
        )


if TYPE_CHECKING:
    from fantasy_forge.messages import Messages
    from fantasy_forge.player import Player
