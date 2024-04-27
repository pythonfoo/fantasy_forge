class NPC:
    """A non player character is a person in the world.

    The Player might interact with NPCs.
    """

    name: str


class Area:
    """An Area is a place in the world, containing NPCs, Items and connections to other areas."""

    name: str
    description: str


class Item:
    """An Item is an object with which players and NPC can interact with."""

    name: str
    description: str
    value: int

    def __init__(self, name: str, description: str, value: int) -> None:
        self.name = name
        self.description = description
        self.value = value

    def __repr__(self) -> str:
        return f"Item({self.name}, {self.description}, {self.value})"


class Inventory:
    """An Inventory contains multiple items."""

    capacity: int
    contents: list[Item]
