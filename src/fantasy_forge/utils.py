from pathlib import Path

SOURCE_FOLDER: Path = Path(__file__).parent.resolve()  # fantasy_forge/src/fantasy_forge

ROOT_FOLDER: Path = SOURCE_FOLDER.parent.parent.resolve()  # fantasy_forge

DATA_FOLDER: Path = ROOT_FOLDER / "data"  # fantasy_forge/data
WORLDS_FOLDER: Path = DATA_FOLDER / "worlds"  # fantasy_forge/data/worlds
LOCALE_FOLDER: Path = DATA_FOLDER / "l10n"  # fantasy_forge/data/l10n
