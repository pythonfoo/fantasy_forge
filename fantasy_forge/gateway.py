from __future__ import annotations

from typing import Self

from .area import Area
from .entity import Entity


class Gateway(Entity):
    """A Gateway is a one-way connection between two areas."""

    source: Area
    target: Area

    def __init__(self: Self, name: str, description: str, source: Area, target: Area):
        super().__init__(name, description)
        self.source = source
        self.target = target

    def __repr__(self: Self) -> str:
        return f"Gateway({self.name}, {self.source} -> {self.target})"

    def on_use(self: Self) -> Area:
        """Returns the target area."""
        return self.target

    def to_dict(self: Self) -> dict:
        gateway_dict: dict = super().to_dict()
        gateway_dict["source"] = self.source
        gateway_dict["target"] = self.target
        return gateway_dict

    @staticmethod
    def from_dict(gateway_dict: dict) -> Gateway:
        entity: Entity = Entity.from_dict(gateway_dict)
        source: Area = gateway_dict.get("source")
        target: Area = gateway_dict.get("target")
        gateway: Gateway = Gateway(entity.name, entity.description, source, target)
        return gateway
