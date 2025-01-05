from pathlib import Path

import toml

from fantasy_forge.folder_structure import (
    ASSET_TYPE,
    ASSET_TYPE_DICT,
    asset2path,
)
from fantasy_forge.utils import WORLDS_FOLDER, clean_filename
# TODO: use questionairy for type parsing

def bool_from_str(str_data: str) -> bool:
    match str_data.casefold():
        case "true" | "y":
            return True
        case "false" | "n":
            return False
        case _:
            return False


def get_asset_data(asset_type: ASSET_TYPE) -> dict:
    config_dict: dict = {}
    attr_name: str
    attr_type: type
    for attr_name, attr_type in asset_type.__attributes__.items():
        raw = input(f"{attr_type.__name__:>8} {attr_name}: ")
        data = PARSER[attr_type](raw)
        config_dict[attr_name] = data
    return config_dict


def main():
    # select world
    # TODO: allow world selection through argument parser
    world_name: str = input("World name: ")
    world_path: Path = WORLDS_FOLDER / world_name
    assert world_path.exists()

    while True:
        # select asset type
        asset_type_inp: str = input("Asset type: ")
        if not asset_type_inp:
            break

        asset_type: ASSET_TYPE = ASSET_TYPE_DICT[asset_type_inp]

        # input asset specific data
        config_dict: dict = get_asset_data(asset_type)

        name: str = config_dict["name"]

        # save asset to file
        filename = f"{clean_filename(name)}.toml"

        asset_path: Path = asset2path(world_name, asset_type)
        filepath = asset_path / Path(filename)

        # TODO: implement a "safe" non-writing mode, selectable via ArgumentParser
        with filepath.open("w", encoding="utf-8") as f:
            content = toml.dumps(config_dict)
            f.write(content)

        print(f"your {asset_type.__name__!r} was saved at {filepath}")
        print()


PARSER = {
    int: int,
    str: str,
    bool: bool_from_str,
}

if __name__ == "__main__":
    main()
