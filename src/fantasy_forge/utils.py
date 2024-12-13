import json
from pathlib import Path
from typing import IO
from fantasy_forge.area import Area
from fantasy_forge.entity import Entity
from fantasy_forge.item import Item


def pickup_menu(area: Area) -> Item | None:
    # filter items contained in area
    pickup_items: list[Item] = list(
        filter(lambda c: isinstance(c, Item), area.contents)
    )

    for idx, item in enumerate(pickup_items):
        print(f"[{idx:>2}] {item.name}")
    print("[ q] Quit")
    selection: str = input(area.world.l10n.format_value("pick-up-item-menu") + " ")
    if selection.upper() == "Q":
        return None
    if selection.isnumeric():
        selection_index = int(selection)
        return pickup_items[selection_index]

def dump_entity(entity: Entity, path: Path):
    entity_dict = entity.to_dict()
    assert path.exists()
    io: IO
    with path.open("w", encoding="UTF-8") as io:
        json.dump(entity_dict, io)

def load_entity(path: Path) -> Entity:
    assert path.exists()
    io: IO
    with path.open("w", encoding="UTF-8") as io:
        entity_dict = json.load(io)
        entity = Entity(**entity_dict)
        return entity