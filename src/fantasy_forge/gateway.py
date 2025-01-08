"""Gateway class

A gateway connects two areas.
"""

from __future__ import annotations

from typing import Any, Self, TYPE_CHECKING

from fantasy_forge.entity import Entity
from fantasy_forge.key import Key


class Gateway(Entity):
    """A Gateway is a one-way connection to an area."""

    __important_attributes__ = ("name", "target", "locked")
    __attributes__ = {
        **Entity.__attributes__,
        "target": str,
        "locked": bool,
        "key_list": list,
    }

    target: str  # This is not an area because the target might not be loaded yet.
    locked: bool
    key_list: list[str]

    def __init__(self: Self, config_dict: dict[str, Any], l10n: FluentLocalization):
        """
        config_dict contents
        'target' (str): name of the target area
        'locked' (bool): whether the gateway is locked (default: False)
        'key_list' (list[str]): a list of keys to use for this gateway (default: [])

        inherited from Entity
        'name' (str): name of the entity
        'description' (str): description of the entity (default: "")
        'obvious'(bool): whether the entity will be spotted immediately (default: False)
        """
        self.target = config_dict.pop("target")
        self.locked = config_dict.pop("locked", False)
        self.key_list = config_dict.pop("key_list", [])
        super().__init__(config_dict, l10n)

    def on_look(self: Self) -> str:
        """Returns description if unlocked."""
        text = []
        if self.key_list and self.locked:
            text.append(self.l10n.format_value("gateway-on-look-locked"))
        text.append(self.description)
        return "\n".join(text)

    def on_use(self: Self, other: Entity | None = None):
        """Handles gateway use."""
        if other is None:
            super().on_use()
            return
        if not self.key_list:
            print(
                self.l10n.format_value(
                    "gateway-no-keys",
                    {
                        "name": self.name,
                    },
                )
            )
        if not isinstance(other, Key):
            print(
                self.l10n.format_value("gateway-key-needed"),
                {
                    "name": self.name,
                },
            )
            return
        if self.locked:
            self.on_unlock(other)
        else:
            self.on_lock(other)

    def on_unlock(self: Self, key: Key):
        """Handles gateway unlock."""
        if key.key_id in self.key_list:
            self.locked = False
            key.used = True
            print(
                self.l10n.format_value(
                    "gateway-unlock-message",
                    {
                        "name": self.name,
                    },
                )
            )

    def on_lock(self: Self, key: Key):
        """Handles gateway lock."""
        if key.key_id in self.key_list:
            self.locked = True
            key.used = True
            print(
                self.l10n.format_value(
                    "gateway-lock-message",
                    {
                        "name": self.name,
                    },
                )
            )

    def to_dict(self: Self) -> dict:
        """Returns gateway as a dictionary."""
        gateway_dict: dict = super().to_dict()
        gateway_dict["target"] = self.target
        return gateway_dict


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
