from __future__ import annotations

from typing import TYPE_CHECKING, Self

from fantasy_forge.item import Item

# Armour types:
# 'head': for caps, hats, helmets
# 'torso': for shirts, hoodies
# 'legs': for short, trousers, cargos
# 'feet': for shoes
ARMOUR_TYPES = ("head", "torso", "legs", "feet")


class Armour(Item):
    armour_type: str
    defense: int

    __important_attributes__ = ("name", "armour_type", "defense")

    def __init__(self, config_dict, l10n: FluentLocalization):
        a_type: str = config_dict.pop("armour_type")
        assert a_type in ARMOUR_TYPES
        self.armour_type = a_type
        self.defense = config_dict.pop("defense")
        super().__init__(config_dict, l10n)

    def to_dict(self: Self) -> dict:
        armour_dict: dict = super().to_dict()
        armour_dict["armour_type"] = self.armour_type
        armour_dict["defense"] = self.defense
        return armour_dict


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
