from .area import Area
from .item import Item


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
