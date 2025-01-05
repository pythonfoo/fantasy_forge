from pathlib import Path

import questionary

from fantasy_forge.utils import WORLDS_FOLDER, LOCALE_FOLDER
from fantasy_forge.localization import get_fluent_locale
from fluent.runtime import FluentLocalization
from fantasy_forge.folder_structure import init_nested_folder_structure

world_name = questionary.text("Select a name for your world: ").ask()
world_dir: Path = WORLDS_FOLDER / world_name

if world_dir.exists():
    print("A world with that name already exists.")
    exit()
else:
    print(f"Creating a new world at {world_dir}.")

# choose locale
locale_options = [path.name for path in LOCALE_FOLDER.iterdir()]
locale = questionary.select("Choose a locale: ", choices=locale_options).ask()

l10n: FluentLocalization = get_fluent_locale(locale)

# create folder for new world
world_dir.mkdir()

# init nested folder structure
init_nested_folder_structure(world_name)

# create readme file
readme_file: Path = world_dir / "README.md"
readme_file.touch()
readme_file.write_text(f"# {world_name}\n", encoding="UTF-8")

# TODO: enter areas
# TODO: create and save world object