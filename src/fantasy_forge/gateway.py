from __future__ import annotations

from typing import Any, Self

from fantasy_forge.entity import Entity
from fantasy_forge.key import Key
from fantasy_forge.item import Item
from fantasy_forge.world import World


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
        text = []
        if self.key_list and self.locked:
            text.append(self.world.l10n.format_value("gateway-on-look-locked"))
        text.append(self.description)
        return "\n".join(text)

    def on_use(self: Self, other: Item | None = None):
        if other is None:
            super().on_use()
            return
        if not self.key_list:
            print(self.world.l10n.format_value("gateway-no-keys", {
                "name": self.name,
            }))
        if not isinstance(other, Key):
            print(self.world.l10n.format_value("gateway-key-needed"), {
                "name": self.name,
            })
            return
        if self.locked:
            self.on_unlock(other)
        else:
            self.on_lock(other)

    def on_unlock(self: Self, key: Key):
        if key.key_id in self.key_list:
            self.locked = False
            key.used = True
            print(self.world.l10n.format_value("gateway-unlock-message", {
                "name": self.name,
            }))

    def on_lock(self: Self, key: Key):
        if key.key_id in self.key_list:
            self.locked = True
            key.used = True
            print(self.world.l10n.format_value("gateway-lock-message", {
                "name": self.name,
            }))

    def to_dict(self: Self) -> dict:
        gateway_dict: dict = super().to_dict()
        gateway_dict["target"] = self.target
        return gateway_dict
