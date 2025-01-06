"""Generates toml files for new world."""

from pathlib import Path

import logging
import questionary
from fluent.runtime import FluentLocalization

from fantasy_forge.folder_structure import init_nested_folder_structure
from fantasy_forge.localization import get_fluent_locale
from fantasy_forge.utils import LOCALE_FOLDER, WORLDS_FOLDER, clean_filename
from fantasy_forge.world import World

logger = logging.getLogger(__name__)


def new_world() -> World:
    name = questionary.select("Which world do ou choose? ", choices=world_list).ask()
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


def select_world() -> World:
    world_list = [world.name for world in WORLDS_FOLDER.iterdir()]
    name = questionary.select("Which world do ou choose? ", choices=world_list).ask()
    world = World.load(name)
    return world
