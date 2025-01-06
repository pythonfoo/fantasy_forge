"""Generates toml files for new world."""

import cmd
import logging
from pathlib import Path

import questionary
from fluent.runtime import FluentLocalization

from fantasy_forge.area import Area
from fantasy_forge.folder_structure import (
    ASSET_TYPE,
    ASSET_TYPE_DICT,
    init_nested_folder_structure,
)
from fantasy_forge.localization import get_fluent_locale
from fantasy_forge.utils import LOCALE_FOLDER, WORLDS_FOLDER, clean_filename
from fantasy_forge.world import World

logger = logging.getLogger(__name__)


class Builder(cmd.Cmd):
    world: World
    world_dir: Path

    def preloop(self):
        select = questionary.select(
            "What do you want to do?",
            choices=["Create a new world?", "Edit an existing world"],
        ).ask()
        if select == "Create a new world?":
            world = new_world()
        elif select == "Edit an existing world":
            world = select_world()
        else:
            exit(1)
        self.world = world
        self.world_dir = WORLDS_FOLDER / clean_filename(world.name)
        super().preloop()

    def precmd(self, line):
        line = line.strip()
        line = line.casefold()
        return line

    def do_new(self, line):
        """Creates a new element."""
        match line:
            case "world":
                self.do_save()
                world = new_world()
                self.world = world
                self.world_dir = WORLDS_FOLDER / clean_filename(world.name)
            case "area":
                config_dict = get_asset_data(Area)
                area = Area(config_dict, self.world.l10n)
                area_name = area.name
                self.world.areas[area_name] = area
            case _:
                asset_type: ASSET_TYPE = select_asset_type()
                config_dict: dict = get_asset_data(asset_type)
                asset = asset_type(config_dict, self.world.l10n)
                self.world.assets[asset_type.__name__].append(asset)

    def do_edit(self):
        """Edits an existing element."""
        pass

    def do_list(self):
        """Lists all the elements."""
        pass

    def do_save(self, line):
        """Save the current world to filesystem."""
        # save all assets in world
        # save world.toml
        pass

    def do_status(self, line: str):
        print(f"current world: {self.world}")
        print(f"current world dir: {self.world_dir}")


def new_world() -> World:
    name = questionary.text("Choose a name for your new world: ").ask()
    world_dir: Path = WORLDS_FOLDER / clean_filename(name)

    # choose locale
    locale_options = [path.name for path in sorted(LOCALE_FOLDER.iterdir())]
    locale = questionary.select("Choose a locale: ", choices=locale_options).ask()

    l10n: FluentLocalization = get_fluent_locale(locale)

    # create folder for new world
    world_dir.mkdir()

    # init nested folder structure
    init_nested_folder_structure(name)

    # create readme file
    readme_file: Path = world_dir / "README.md"
    readme_file.touch()
    readme_file.write_text(f"# {name}\n", encoding="UTF-8")

    # create world object
    world = World(l10n, name, {}, "")
    return world


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


def select_world() -> World:
    world_list = [world.name for world in WORLDS_FOLDER.iterdir()]
    name = questionary.select("Which world do ou choose? ", choices=world_list).ask()
    world = World.load(name)
    return world


def select_asset_type() -> ASSET_TYPE:
    asset_type_inp: str = questionary.select(
        "Asset type: ", choices=list(ASSET_TYPE_DICT.keys()), default="Entity"
    ).ask()
    asset_type: ASSET_TYPE = ASSET_TYPE_DICT[asset_type_inp]
    return asset_type


if __name__ == "__main__":
    builder = Builder()
    builder.cmdloop()
