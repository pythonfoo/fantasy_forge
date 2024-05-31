from pathlib import Path

import toml

root_dir: Path = Path("worlds")

world_name = input("Select a name for your world: ")
world_dir: Path = root_dir / world_name

if world_dir.exists():
    print("A world with that name already exists.")
    exit()

# create folder for new world
world_dir.mkdir()

# create world.toml file
world_toml_path: Path = world_dir / "world.toml"
world_toml_path.touch()

# create readme file
readme_file: Path = world_dir / "README.md"
readme_file.touch()
readme_file.write_text(f"# {world_name}\n", encoding="UTF-8")

# create areas folder
area_dir: Path = world_dir / "areas"
area_dir.mkdir()

word_toml = {
    "name": world_name,
    "language": "en",
    "areas": [],
}

# ask for areas
while True:
    area_name: str = input("Select a name for the next area: ")

    if not area_name:
        break

    area_path: Path = area_dir / area_name
    if area_path.exists():
        print("An Area with that name already exists.")
        continue

    # ask for area description
    area_description: str = input("Give a description for that area: ")

    area_toml = {"name": area_name, "description": area_description}
    with area_path.open("w", encoding="UTF-8") as stream:
        toml.dump(area_toml, stream)

    word_toml["areas"].append(area_name)

# dump world toml
with world_toml_path.open("w", encoding="UTF-8") as stream:
    toml.dump(word_toml, stream)
