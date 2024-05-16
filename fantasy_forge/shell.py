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
        return True
    
    def do_EOF(self, arg):
        return self.do_quit(arg)

    def do_look(self, arg):
        match arg.split():
            case ["around"]:
                self.player.area.on_look()
            case ["at", entity]:
                self.player.look_at(entity)
            case default:
                print(self.player.world.l10n.format_value("shell-invalid-command"))

if TYPE_CHECKING:
    from .player import Player
