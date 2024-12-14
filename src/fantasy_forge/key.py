from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from fantasy_forge.item import Item


class Key(Item):
    """A Key can be used to unlock Gateways or Container."""

    __important_attributes__ = ("name", "key_id")

    key_id: str
    used: bool  # wether the key was used already

    def __init__(
        self: Self, config_dict: dict[str, Any], l10n: FluentLocalization
    ) -> None:
        self.key_id = config_dict.pop("key_id")

        self.moveable = True  # keys are moveable by default
        self.carryable = True  # keys are carryable by default
        super().__init__(config_dict, l10n)
        self.used = False

    def __eq__(self: Self, other: Key):
        """Compares key ids."""
        return self.key_id == other.key_id


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
