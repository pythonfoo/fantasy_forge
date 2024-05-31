from __future__ import annotations

from typing import Any, Self

from .entity import Entity
from .key import Key
from .item import Item
from .world import World


class Gateway(Entity):
    """A Gateway is a one-way connection to an area."""

    __important_attributes__ = ("name", "target", "locked")

    target: str  # This is not an area because the target might not be loaded yet.
    locked: bool
    key_list: list[str]

    def __init__(
        self: Self,
        world: World,
        config_dict: dict[str, Any],
    ):
        self.target = config_dict.pop("target")
        self.locked = config_dict.pop("locked", False)
        self.key_list = config_dict.pop("key_list", [])
        super().__init__(world, config_dict)

    def on_look(self: Self) -> str:
        if not self.key_list:
            return self.description
        return self.description + (" (locked)" if self.locked else "")  # TODO: l10n

    def on_use(self: Self, other: Item | None = None) -> str:
        if other is None:
            return super().on_use()
        if not self.key_list:
            print("You can't use {self.name} like that.")  # TODO: l10n
        if not isinstance(other, Key):
            print("You need a key.")  # TODO: l10n
        if self.locked:
            self.on_unlock(other)
        else:
            self.on_lock(other)

    def on_unlock(self: Self, key: Key):
        if key.key_id in self.key_list:
            self.locked = False
            key.used = True

    def on_lock(self: Self, key: Key):
        if key.key_id in self.key_list:
            self.locked = True
            key.used = True

    def to_dict(self: Self) -> dict:
        gateway_dict: dict = super().to_dict()
        gateway_dict["target"] = self.target
        return gateway_dict
