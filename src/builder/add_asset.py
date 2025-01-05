from pathlib import Path
import questionary
import toml

from fantasy_forge.folder_structure import (
    ASSET_TYPE,
    ASSET_TYPE_DICT,
    asset2path,
)
from fantasy_forge.utils import WORLDS_FOLDER, clean_filename


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
        prompt = f"{attr_name}: "
        match attr_type.__name__:
            case "bool":
                data = questionary.confirm(prompt).ask()
            case "int":
                raw = questionary.text(prompt).ask()
                assert raw.isdigit()
                data = int(raw)
            case _:
                data = questionary.text(prompt).ask()
        config_dict[attr_name] = data
    return config_dict


def main():
    # select world
    # TODO: allow world selection through argument parser
    world_list = [path.name for path in WORLDS_FOLDER.iterdir()]
    world_name = questionary.select(
        "World name: ", choices=world_list, default="test"
    ).ask()

    world_path: Path = WORLDS_FOLDER / world_name
    assert world_path.exists()

    running: bool = True
    while running:
        # select asset type
        asset_type_inp: str = questionary.select(
            "Asset type: ", choices=list(ASSET_TYPE_DICT.keys()), default="Entity"
        ).ask()
        asset_type: ASSET_TYPE = ASSET_TYPE_DICT[asset_type_inp]

        # input asset specific data
        config_dict: dict = get_asset_data(asset_type)

        name: str = config_dict["name"]

        # save asset to file
        filename = f"{clean_filename(name)}.toml"

        asset_path: Path = asset2path(world_name, asset_type)
        filepath = asset_path / Path(filename)

        save = questionary.confirm(
            "Do you want to save this asset?", default=True
        ).ask()
        if save:
            with filepath.open("w", encoding="utf-8") as f:
                content = toml.dumps(config_dict)
                f.write(content)

            print(f"your {asset_type.__name__!r} was saved at: ")
            questionary.print(f"{filepath}", style="italic")
        else:
            print(f"your {asset_type.__name__!r} wasn't saved")

        print()

        running = questionary.confirm("Do you want to continue?").ask()


if __name__ == "__main__":
    main()
