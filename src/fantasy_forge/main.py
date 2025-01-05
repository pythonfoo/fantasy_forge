import logging
from argparse import ArgumentParser

from fantasy_forge.area import Area
from fantasy_forge.player import Player
from fantasy_forge.world import World


def parse_args():
    parser = ArgumentParser(description="Fantasy Forge: A text-based RPG")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    parser.add_argument("--world", help="The world to play in", default="chaosdorf")
    parser.add_argument("--name", help="Set player name", default="")
    parser.add_argument(
        "--logfile",
        help="Enables logging for debug purposes",
        default="fantasy_forge.log",
    )
    parser.add_argument("--loglevel", help="Severity Level for logging", default="INFO")
    return parser.parse_args()


def main():
    args = parse_args()

    # init logger
    logger = logging.getLogger(__name__)
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    logging.basicConfig(filename=args.logfile, level=numeric_level, filemode="w")
    logger.info("load world %s" % args.world)

    # load world
    world = World.load(args.world)

    if args.name == "":
        player_name = input(world.l10n.format_value("character-name-prompt") + " ")
    else:
        player_name = args.name

    player = Player(world, player_name)

    #  enter spawn area
    spawn: Area = world.spawn_point
    player.enter_area(spawn)

    # main loop
    logger.info("starting mainloop for player %s" % player)
    player.main_loop()
