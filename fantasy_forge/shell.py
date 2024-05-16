from __future__ import annotations

from cmd import Cmd
from typing import TYPE_CHECKING

class Shell(Cmd):
    player: Player
    prompt = '> '

    def __new__(self, player: Player) -> Shell:
        match player.world.l10n.locales[0]:
            case "en":
                shell_type = ShellEn
            case default:
                raise RuntimeError(player.world.l10n.format_value(
                    "unknown-language-error",
                    { "language": default, },
                ))
        shell = super().__new__(shell_type)
        return shell

    def __init__(self, player: Player):
        super().__init__()
        self.player = player

    def do_EOF(self, arg: str) -> bool:
        return True

class ShellEn(Shell):
    def do_quit(self, arg: str) -> bool:
        return self.do_EOF(arg)

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
