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
    __attributes__ = {**Item.__attributes__, "armour_type": str, "defense": int}

    def __init__(self, config_dict, l10n: FluentLocalization):
        """
        config_dict contents
        'armour_type' (str): armour slot ("head", "torso", "legs", "feet")
        'defense' (int): defense points gained by armour

        inherited from Item:
        'moveable' (bool): can the item be moved by the player (default: True)
        'carryable' (bool): can the item be put in the inventory by the player (default: True)

        inherited from Entity
        'name' (str): name of the entity
        'description' (str): description of the entity (default: "")
        'obvious'(bool): whether the entity will be spotted immediately (default: False)
        """
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
