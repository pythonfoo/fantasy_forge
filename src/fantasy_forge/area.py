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

    def __init__(self: Self, config_dict: dict[str, Any], l10n: FluentLocalization):
        super().__init__(config_dict, l10n)
        self.contents: dict = {}

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
        area_dict: dict = super().to_dict()
        area_dict["contents"] = self.contents
        return area_dict

    @classmethod
    def from_dict(cls, area_dict: dict, l10n: FluentLocalization) -> Area:
        contents_list: list[Entity] = []
        for entity_dict in area_dict.get("contents", []):
            match entity_dict.get("kind", "entity"):
                case "item":
                    from fantasy_forge.item import Item

                    contents_list.append(Item(entity_dict, l10n))
                case "gateway":
                    from fantasy_forge.gateway import Gateway

                    contents_list.append(Gateway(entity_dict, l10n))
                case "key":
                    from fantasy_forge.key import Key

                    contents_list.append(Key(entity_dict, l10n))
                case "enemy":
                    from fantasy_forge.enemy import Enemy

                    contents_list.append(Enemy(entity_dict, l10n))
                case "weapon":
                    from fantasy_forge.weapon import Weapon

                    contents_list.append(Weapon(entity_dict, l10n))
                case "armour":
                    from fantasy_forge.armour import Armour

                    contents_list.append(Armour(entity_dict, l10n))

                case default:
                    logger.info("could not determine %s used Entity instead" % default)
                    contents_list.append(Entity(entity_dict, l10n))
        contents = {entity.name: entity for entity in contents_list}
        area = cls(area_dict, l10n)
        area.contents = contents
        return area

    @staticmethod
    def load(world, root_path: Path, name: str):
        path = root_path / "areas" / f"{name}.toml"
        with path.open() as area_file:
            area_toml = toml.load(area_file)
        return Area.from_dict(area_toml, world.l10n)

    @staticmethod
    def empty(l10n: FluentLocalization) -> Area:
        """Return an empty area, this is a placeholder."""
        return Area(
            dict(
                name=l10n.format_value("void-name"),
                description=l10n.format_value("void-description"),
            ),
            l10n,
        )


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
