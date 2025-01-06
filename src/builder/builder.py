"""Generates toml files for new world."""

import cmd
import logging
from pathlib import Path

import questionary
import toml
from fluent.runtime import FluentLocalization

from fantasy_forge.area import Area
from fantasy_forge.folder_structure import (
    ASSET_TYPE,
    ASSET_TYPE_DICT,
    asset2path,
    init_nested_folder_structure,
)
from fantasy_forge.localization import get_fluent_locale
from fantasy_forge.utils import LOCALE_FOLDER, WORLDS_FOLDER, clean_filename
from fantasy_forge.world import World

logger = logging.getLogger(__name__)


class BuilderShell(cmd.Cmd):
    world: World

    @property
    def world_name(self) -> str:
        return self.world.name

    @property
    def world_dir(self) -> Path:
        return WORLDS_FOLDER / clean_filename(self.world_name)

    def preloop(self):
        select = questionary.select(
            "What do you want to do?",
            choices=["Create a new world", "Edit an existing world"],
        ).ask()
        if select == "Create a new world":
            world = new_world()
        elif select == "Edit an existing world":
            world = select_world()
        else:
            exit(1)
        self.world = world
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
                print("Let's create a new area.")
                world = new_world()
                self.world = world
            case "area":
                print("Let's create a new area.")
                config_dict = get_asset_data(Area)
                area = Area(config_dict, self.world.l10n)
                area_name = area.name
                self.world.areas[area_name] = area
            case _:
                asset_type: ASSET_TYPE
                if line.title() in ASSET_TYPE_DICT:
                    asset_type = ASSET_TYPE_DICT[line.title()]
                else:
                    asset_type = select_asset_type()
                print(f"Let's create a new {asset_type.__name__}.")
                config_dict: dict = get_asset_data(asset_type)
                asset = asset_type(config_dict, self.world.l10n)
                self.world.assets[asset_type.__name__].append(asset)

    def do_edit(self):
        """Edits an existing element."""
        pass

    def do_list(self, line: str):
        """Lists all the elements of a kind."""
        match line:
            case "world":
                print("Let's list all worlds.")
                for world_dir in WORLDS_FOLDER.iterdir():
                    print(world_dir)
            case "area":
                print("Let's list all areas.")
                for area_name, area in self.world.areas.items():
                    print(area_name, repr(area))
            case "all" | "":
                print("Let's list all assets.")
                # list all assets
                for asset in self.world.iter_assets():
                    print(repr(asset))
            case _:
                asset_type: ASSET_TYPE
                if line.title() in ASSET_TYPE_DICT:
                    asset_type = ASSET_TYPE_DICT[line.title()]
                else:
                    asset_type = select_asset_type()
                print(f"Let's list all assets of type {asset_type.__name__}")
                for asset in self.world.assets[asset_type.__name__]:
                    print(repr(asset))

    def do_save(self, line):
        """Save the current world to filesystem."""
        for asset in self.world.iter_assets():
            save_asset(self.world, asset)
        # TODO: save world.toml
        pass

    def do_status(self, line: str):
        print(f"current world: {self.world}")
        print(f"current world dir: {self.world_dir}")

    def do_spawn(self, line: str):
        """Prints or selects the spawn area of the current world."""
        if line:
            # set spawn area
            area_name = questionary.select(
                "Choose a spawn area", choices=list(self.world.areas.keys())
            ).ask()
            self.world.spawn = area_name
        else:
            # print spawn
            print(f"current spawn: {self.world.spawn}")

    def _populate_area(self, area: Area):
        """Adds assets from world into an area."""
        assets_to_add = questionary.checkbox(
            "Choose the assets",
            choices=[str(asset) for asset in self.world.iter_assets()],
        ).ask()
        for asset_name in assets_to_add:
            asset = self.world.get_asset(asset_name)
            area.contents[asset_name] = asset


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


def save_asset(world: World, asset: ASSET_TYPE):
    asset_path = asset2path(world.name, asset) / clean_filename(asset.name)
    asset_data = asset.to_dict()
    content = toml.dumps(asset_data)
    with asset_path.open("w") as file:
        file.write(content)


if __name__ == "__main__":
    builder = BuilderShell()
    builder.cmdloop()
