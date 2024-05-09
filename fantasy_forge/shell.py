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

if TYPE_CHECKING:
    from .player import Player
