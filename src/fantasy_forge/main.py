import logging
import shutil
from argparse import ArgumentParser
from importlib import resources
from pathlib import Path
from sys import argv
from typing import Any

import toml
from xdg_base_dirs import xdg_config_home

from fantasy_forge.player import Player
from fantasy_forge.world import World


def parse_args(config: dict[str, Any], argv=argv[1:]):
    parser = ArgumentParser(description="Fantasy Forge: A text-based RPG")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    parser.add_argument("--world", help="The world to play in", default=config["world"])
    parser.add_argument("--name", help="Set player name", default=config["name"])
    parser.add_argument(
        "--logfile",
        help="Enables logging for debug purposes",
        default=config["logfile"],
    )
    parser.add_argument(
        "--loglevel", help="Severity Level for logging", default=config["loglevel"]
    )
    return parser.parse_args(argv)


def load_config() -> dict[str, Any]:
    with resources.as_file(resources.files()) as resource_path:
        default_config_file = resource_path / "config.toml"

    usr_config_file = xdg_config_home() / "fantasy_forge.toml"

    if not usr_config_file.exists():
        shutil.copyfile(default_config_file, usr_config_file)

    with usr_config_file.open() as config_file:
        config = toml.load(config_file)

    return config


def main():
    # load config and args
    config = load_config()
    args = parse_args(config)

    # init logger
    logger = logging.getLogger(__name__)
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    logging.basicConfig(filename=args.logfile, level=numeric_level, filemode="w")
    logger.info("load world %s" % args.world)

    # set player name and load world
    world = World.load(args.world)
    name_input = input(
        world.l10n.format_value("character-name-prompt", {"default": args.name}) + " "
    )
    if name_input:
        player_name = name_input
        print("Succesfully changed name! Your hormones should arrive soon.")
        print()
    else:
        player_name = args.name
    player = Player(world, player_name)

    # main loop
    logger.info("starting mainloop for player %s" % player)
    player.main_loop()
