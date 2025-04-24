from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterator, Self

import toml

from fantasy_forge.entity import Entity
from fantasy_forge.utils import UniqueDict


class Area(Entity):
    """An Area is a place in the world, containing NPCs, Items and connections to other areas."""

    __important_attributes__ = ("name",)
    contents: UniqueDict[str, Entity]

    def __init__(self: Self, messages: Messages, config_dict: dict[str, Any]):
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
        contents_list: list[Entity] = []
        for entity_dict in area_dict.get("contents", []):
            match entity_dict.get("kind", "entity"):
                case "item":
                    from fantasy_forge.item import Item

                    contents_list.append(Item(messages, entity_dict))
                case "gateway":
                    from fantasy_forge.gateway import Gateway

                    contents_list.append(Gateway(messages, entity_dict))
                case "key":
                    from fantasy_forge.key import Key

                    contents_list.append(Key(messages, entity_dict))
                case "enemy":
                    from fantasy_forge.enemy import Enemy

                    contents_list.append(Enemy(messages, entity_dict))
                case "weapon":
                    from fantasy_forge.weapon import Weapon

                    contents_list.append(Weapon(messages, entity_dict))
                case "armour":
                    from fantasy_forge.armour import Armour

                    contents_list.append(Armour(messages, entity_dict))

                case default:
                    contents_list.append(Entity(messages, entity_dict))
        area = Area(messages, area_dict)
        for entity in contents_list:
            area.contents[entity.name] = entity
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
