from argparse import ArgumentParser
from sys import argv

from .player import Player
from .world import World


def parse_args(argv=argv[1:]):
    parser = ArgumentParser(description="Fantasy Forge: A text-based RPG")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    parser.add_argument("--world", help="The world to play in", default="chaosdorf")
    return parser.parse_args(argv)

def main():
    args = parse_args()
    world = World.load(args.world)
    player = Player(world, input("Please name your character: "))
    player.main_loop()
