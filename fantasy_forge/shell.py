from __future__ import annotations

from cmd import Cmd
from typing import TYPE_CHECKING

class Shell(Cmd):
    player: Player
    prompt = '> '

    def __init__(self, player: Player):
        super().__init__()
        self.player = player
    
    def do_quit(self, arg):
        print("Bye.")
        return True
    
    def do_EOF(self, arg):
        return self.do_quit(arg)

    def do_look(self, arg):
        match arg.split():
            case ["around"]:
                print("You take a look around.")
                print("You see: nothing")
            case ["at", entity]:
                print(f"You are looking at {entity}.")
            case default:
                print("This is no valid command.")

if TYPE_CHECKING:
    from .player import Player
