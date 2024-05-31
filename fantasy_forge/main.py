from argparse import ArgumentParser
from sys import argv

import logging

from .player import Player
from .world import World


def parse_args(argv=argv[1:]):
    parser = ArgumentParser(description="Fantasy Forge: A text-based RPG")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    parser.add_argument("--world", help="The world to play in", default="chaosdorf")
    parser.add_argument(
        "--logfile",
        help="Enables logging for debug purposes",
        default="fantasy_forge.log",
    )
    parser.add_argument("--loglevel", help="Severity Level for logging", default="INFO")
    return parser.parse_args(argv)


def main():
    args = parse_args()

    logger = logging.getLogger(__name__)
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    logging.basicConfig(filename=args.logfile, level=numeric_level, filemode="w")

    logger.info("load world %s" % args.world)
    world = World.load(args.world)
    player_name = input(world.l10n.format_value("character-name-prompt") + " ")
    player = Player(world, player_name)

    logger.info("starting mainloop for player %s" % player)
    player.main_loop()
