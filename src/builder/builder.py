"""Generates toml files for new world."""

from cmd import Cmd
from pathlib import Path
from typing import Self

import toml

# TODO: centralized save & load method
# TODO: auto completion for commands


class Builder(Cmd):
    root_dir: Path = Path.cwd() / "worlds"
    current_world: Path | None  # TODO: Change type to World
    current_area_dir: Path | None
    current_area: Path | None  # TODO: Change type to Area

    world_toml: dict | None
    area_toml: dict | None

    def __init__(self: Self):
        self.current_world = None
        self.current_area = None
        self.current_area_dir = None

        self.world_toml = None
        self.area_toml = None

    def do_status(self: Self, arg: str):
        print(f"root directory: {self.root_dir}")
        print(f"current world: {self.current_world}")
        print(f"current area: {self.current_area}")

    def do_new(self: Self, arg: str):
        match arg.strip().lower():
            case "world":
                self.new_world()
            case "area":
                self.new_area()
            case _:
                raise NotImplementedError(f"new {arg} is not yet implemented.")

    def new_world(self: Self):
        world_name: str = input("Enter a name for your world: ")
        world_dir = self.root_dir / world_name
        if world_dir.exists():
            print("A world with that name already exists.")
            return
        # create dir for world
        world_dir.mkdir()

        # create area dir for world
        area_dir: Path = world_dir / "areas"
        area_dir.mkdir()

        # sets up world.toml file
        toml_path: Path = world_dir / "world.toml"
        toml_path.touch()

        # sets up readme file for world
        readme_path: Path = world_dir / "README.md"
        readme_path.touch()

        # ask for world description
        description: str = input("Enter a description for your world: \n")

        self.current_world = world_dir
        self.world_toml = {"name": world_name, "description": description, "areas": []}
        self.current_area_dir = area_dir

    def new_area(self: Self):
        if self.current_world is None:
            print("You have to create or select a world first.")
            return

        area_name: str = input("Enter a name for your area: ")
        area_desc: str = input("Enter a description for your area: \n")

        area_toml = {"name": area_name, "description": area_desc}

        # create area.toml file
        area_path: Path = self.current_area_dir / f"{area_name}.toml"
        area_path.touch()

        # dump area toml to file
        with area_path.open("w", encoding="UTF-8") as stream:
            toml.dump(area_toml, stream)
        self.area_toml = area_toml

        # add area to world.toml
        self.world_toml["areas"].append(area_name)

        self.current_area = area_path

    def new_item(self: Self):
        # TODO
        pass

    def new_key(self: Self):
        # TODO
        pass

    def new_gateway(self: Self):
        # TODO
        pass

    def do_list(self: Self, arg: str):
        match arg.strip().lower():
            case "world":
                self.list_world()
            case "area":
                self.list_area()
            case _:
                raise NotImplementedError(f"new {arg} is not yet implemented.")

    def list_world(self: Self):
        for world_path in self.root_dir.iterdir():
            print(world_path)

    def list_area(self: Self):
        if self.current_area_dir is None:
            print("You have to create or select a world first.")
            return
        for area_path in self.current_area_dir.glob("*.toml"):
            print(area_path)

    def do_select(self: Self, arg: str):
        match arg.strip().lower():
            case "world":
                self.select_world()
            case "area":
                self.select_area()

    def select_world(self: Self):
        # TODO: implement select menu
        pass

    def select_area(self: Self):
        # TODO: implement select menu
        pass

    def do_quit(self: Self, arg: str):
        # write world.toml to file
        with self.current_world.open("w", encoding="UTF-8") as stream:
            toml.dump(self.world_toml, stream)


if __name__ == "__main__":
    builder = Builder()
    builder.cmdloop()
