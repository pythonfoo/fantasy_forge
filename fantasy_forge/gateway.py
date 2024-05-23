from __future__ import annotations

from typing import Any, Self

from .entity import Entity
from .world import World


class Gateway(Entity):
    """A Gateway is a one-way connection to an area."""
    target: str  # This is not an area because the target might not be loaded yet.

    def __init__(self: Self, world: World, config_dict: dict[str, Any], ):
        self.target = config_dict.pop("target")
        super().__init__(world, config_dict)

    def __repr__(self: Self) -> str:
        return f"Gateway({self.name}, -> {self.target})"

    def on_use(self: Self) -> str:
        """Returns the target area."""
        return self.target

    def to_dict(self: Self) -> dict:
        gateway_dict: dict = super().to_dict()
        gateway_dict["target"] = self.target
        return gateway_dict

