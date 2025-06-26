from __future__ import annotations

"""Container class

A container is an item in the world which holds an inventory.
"""

from typing import TYPE_CHECKING, Any, Iterator, Self

from fantasy_forge.item import Item
from fantasy_forge.localization import highlight_interactive
from fantasy_forge.messages import Messages
from fantasy_forge.utils import UniqueDict, inflate_contents


class Container(Item):
    """Container object."""

    contents: UniqueDict[str, Item]
    capacity: int
    __important_attributes__ = (*Item.__important_attributes__, "capacity")
    __attributes__ = {**Item.__attributes__, "capacity": int}

    def __init__(self: Self, messages: Messages, config_dict: dict[str, Any]) -> None:
        """
        config_dict contents
        'capacity' (int): maximum capacity of the container
        'contents' (list): contents of the container

        inherited from Item
        'moveable' (bool): can the item be moved by the player (default: True)
        'carryable' (bool): can the item be put in the inventory by the player (default: True)

        inherited from Entity
        'name' (str): name of the entity
        'description' (str): description of the entity (default: "")
        'obvious'(bool): whether the entity will be spotted immediately (default: False)
        """
        super().__init__(messages, config_dict)
        self.capacity = config_dict.get("capacity", 10)
        self.contents = UniqueDict()
        inflate_contents(messages, config_dict.get("contents", []), self)

    def __len__(self: Self) -> int:
        """Returns current capacity."""
        return len(self.contents)

    def __iter__(self: Self) -> Iterator[Item]:
        """Iterates over items in container."""
        yield from self.contents.values()

    def __contains__(self: Self, other: str) -> bool:
        """Returns if entity is in container."""
        return other in self.contents

    def on_look(self: Self, player: Player):
        super().on_look(player)
        if not self.contents:
            self.messages.to(
                [player], "container-look-empty-message", container=self.name
            )
        else:
            self.messages.to(
                [player],
                "container-look-message",
                container=self.name,
                contents=", ".join(
                    [
                        highlight_interactive(str(item)).format(None)
                        + f" (weight: {item.weight})"
                        for item in self
                    ]
                ),
            )


if TYPE_CHECKING:
    from fantasy_forge.player import Player
