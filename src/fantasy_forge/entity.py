"""Entity class

An entity is an abstract object in the world.
Each entity is identifiable by its name.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self


class Entity:
    """An Entity object"""

    __important_attributes__: tuple[str, ...] = ("name",)
    __attributes__: dict[str, type] = {"name": str, "description": str, "obvious": bool}

    name: str
    description: str
    obvious: bool  # obvious entities are seen when entering the room
    l10n: FluentLocalization

    def __init__(
        self: Self, config_dict: dict[str, Any], l10n: FluentLocalization
    ) -> None:
        """
        config_dict contents
        'name' (str): name of the entity
        'description' (str): description of the entity (default: "")
        'obvious'(bool): whether the entity will be spotted immediately (default: False)
        """
        self.name = config_dict.pop("name")
        self.description = config_dict.pop("description", "")
        self.obvious = config_dict.pop("obvious", False)
        self.l10n = l10n

    def on_look(self: Self) -> str:
        """Returns description of entity."""
        return self.description

    def on_use(self: Self, other: Entity | None = None):
        """Handles usage of entity."""
        print(
            self.l10n.format_value(
                "cannot-use-message",
                {
                    "self": self.name,
                    "other": getattr(other, "name", None),
                },
            )
        )

    def __repr__(self: Self) -> str:
        listed_attrs = []
        for attr in self.__important_attributes__:
            if not hasattr(self, attr):
                raise AttributeError(
                    f"Missing attribute {attr} in {self.__class__.__name__}"
                )
            listed_attrs.append(f"{attr}={getattr(self, attr)}")
        return f"{self.__class__.__name__}({', '.join(listed_attrs)})"

    def __str__(self: Self) -> str:
        return self.name

    def to_dict(self: Self) -> dict:
        """Returns entity attributes as a dictionary."""
        entity_dict: dict = {"name": self.name, "description": self.description}
        return entity_dict

    @classmethod
    def from_dict(cls, entity_dict: dict, l10n: FluentLocalization) -> Self:
        """Creates new entity from a dictionary."""
        entity = cls(entity_dict, l10n)
        return entity


if TYPE_CHECKING:
    from fluent.runtime import FluentLocalization
