from pathlib import Path

SOURCE_DIR = Path(__file__).parent.resolve()  # fantasy_forge/src/fantasy_forge
ROOT_DIR = SOURCE_DIR.parent.parent.resolve()  # fantasy_forge
WORLDS_DIR = ROOT_DIR / "data" / "worlds"  # fantasy_forge/data/worlds
