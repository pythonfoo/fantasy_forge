"""Gateway class

A gateway connects two areas.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Self

from fantasy_forge.area import Area
from fantasy_forge.entity import Entity
from fantasy_forge.key import Key
from fantasy_forge.messages import Messages
from fantasy_forge.world import World


class Gateway(Entity):
    """A Gateway is a one-way connection to an area."""

    __important_attributes__ = ("name", "target", "locked")
    __attributes__ = {
        **Entity.__attributes__,
        "target": str,
        "locked": bool,
        "key_list": list,
    }

    target_str: str  # This is not an area because the target might not be loaded yet.
    target: Optional[Area]
    locked: bool
    key_list: list[str]

    def __init__(
        self: Self,
        messages: Messages,
        config_dict: dict[str, Any],
    ):
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
        self.target_str = config_dict.pop("target")
        self.target = None
        self.locked = config_dict.pop("locked", False)
        self.key_list = config_dict.pop("key_list", [])
        super().__init__(messages, config_dict)
        
    def on_look(self: Self, actor: Player):
        if self.key_list and self.locked:
            self.messages.to([actor], "gateway-on-look-locked")
        actor.shell.stdout.write(self.description + "\n")

    def on_use(self: Self, actor: Player, other: Item | None = None):
        if other is None:
            super().on_use(actor)
            return
        if not self.key_list:
            self.messages.to(
                [actor],
                "gateway-no-keys",
                name=self.name,
            )
        if not isinstance(other, Key):
            self.messages.to(
                [actor],
                "gateway-key-needed",
                name=self.name,
            )
            return
        if self.locked:
            self.on_unlock(actor, other)
        else:
            self.on_lock(actor, other)

    def on_unlock(self: Self, actor: Player, key: Key):
        if key.key_id in self.key_list:
            self.locked = False
            key.used = True
            self.messages.to(
                [actor],
                "gateway-unlock-message",
                name=self.name,
            )

    def on_lock(self: Self, actor: Player, key: Key):
        if key.key_id in self.key_list:
            self.locked = True
            key.used = True
            self.messages.to(
                [actor],
                "gateway-lock-message",
                name=self.name,
            )

    def to_dict(self: Self) -> dict:
        """Returns gateway as a dictionary."""
        gateway_dict: dict = super().to_dict()
        gateway_dict["target"] = self.target
        return gateway_dict

    def resolve(self, world: World):
        self.target = world.areas[self.target_str]
        if self.locked:
            assert self.key_list
            all_keys = []
            for area in world.areas.values():
                for entity in area.contents.values():
                    if isinstance(entity, Key):
                        all_keys.append(entity.key_id)

            for key in self.key_list:
                assert key in all_keys


if TYPE_CHECKING:
    from fantasy_forge.player import Player
