import logging
import shutil
from argparse import ArgumentParser
from importlib import resources
from pathlib import Path
from sys import argv
from threading import current_thread
from typing import Any

from fantasy_forge.area import Area
from fantasy_forge.config import Config
from fantasy_forge.player import Player
from fantasy_forge.world import World


def parse_args(config: Config, argv=argv[1:]):
    parser = ArgumentParser(description="Fantasy Forge: A text-based RPG")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    parser.add_argument("--world", help="The world to play in", default=config.world)
    parser.add_argument("--name", help="Set player name", default=config.name)
    parser.add_argument(
        "--description", help="Set player description", default=config.description
    )
    parser.add_argument(
        "--logfile", help="Enables logging for debug purposes", default=config.logfile
    )
    parser.add_argument(
        "--loglevel", help="Severity Level for logging", default=config.loglevel
    )
    return parser.parse_args(argv)


def main():
    # load config and args
    config = Config.read()
    args = parse_args(config)
    description = args.description

    # init logger
    logger = logging.getLogger(__name__)
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    logging.basicConfig(filename=args.logfile, level=numeric_level, filemode="w")
    logger.info("load world %s", args.world)

    # set player name and load world
    world = World.load(args.world)

    name_input = input(
        world.l10n.format_value("character-name-prompt", {"default_name": args.name})
        + " "
    )

    while True:
        if not any(
            (
                (name_input or args.name) in area.contents.keys()
                for area in world.areas.values()
            )
        ):
            if name_input:
                player_name = name_input
                setattr(config, "name", name_input)
                print(
                    world.l10n.format_value(
                        "character-name-change-successful", {"chosen_name": name_input}
                    )
                )
                break
            else:
                player_name = args.name
                break
        else:
            if name_input:
                name_input = input(
                    world.l10n.format_value(
                        "character-name-taken-prompt", {"name": name_input}
                    )
                    + " "
                )
            else:
                name_input = input(
                    world.l10n.format_value(
                        "character-name-taken-prompt", {"name": args.name}
                    )
                    + " "
                )
            continue

    config.save()

    print()
    player = Player(world, player_name, description, current_thread())

    # main loop
    logger.info("starting mainloop for player %s", player)
    player.main_loop()
