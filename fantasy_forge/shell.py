from __future__ import annotations

from cmd import Cmd
from typing import TYPE_CHECKING

from .item import Item


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
    
    def completenames(self, text, *ignored):
        """This is called when completing the command itself.
        
        This is uses the stdlib's Cmd, but adds a space after every command,
        so that the user doesn't have to enter it manually.
        """
        return [
            name + ' '
            for name in super().completenames(text, *ignored)
        ]

    def default(self, line: str):
        """Display an error message, because the command was invalid."""
        print(self.player.world.l10n.format_value("shell-invalid-command"))

    def do_EOF(self, arg: str) -> bool:
        return True

class ShellEn(Shell):
    def do_quit(self, arg: str) -> bool:
        return self.do_EOF(arg)

    def do_look(self, arg: str):
        if arg.strip() == "around":
            self.player.look_around()
        elif arg.strip().startswith("at"):
            self.player.look_at(arg.strip().removeprefix("at").strip())
        else:
            self.default(arg)
    
    def complete_look(self, text: str, line: str, begidx: int, endidx: int,):
        if line.startswith("look at "):
            entity_name = line.removeprefix("look at ").strip()
            completions = [
                text + name.removeprefix(entity_name).strip() + ' '
                for name in self.player.seen_entities.keys()
                if name.startswith(entity_name)
            ]
            if ' ' in completions:
                completions.remove(' ')
            return completions
        if line.startswith("look around "):
            return []
        if line.startswith("look "):
            return [ 
                verb for verb in 
                ["at ", "around "]
                if verb.startswith(text)
            ]
        return []

    def do_pick(self, arg: str):
        if arg.startswith("up "):
            arg = arg.removeprefix("up ")
        self.player.pick_up(arg.strip())
    
    def complete_pick(self, text: str, line: str, begidx: int, endidx: int,):
        if line.startswith("pick up "):
            entity_name = line.removeprefix("pick up ").strip()
            completions = [
                text + name.removeprefix(entity_name).strip() + ' '
                for name, entity in self.player.seen_entities.items()
                if name.startswith(entity_name) and isinstance(entity, Item) and entity.carryable
            ]
            if ' ' in completions:
                completions.remove(' ')
            return completions
        if line.startswith("pick "):
            entity_name = line.removeprefix("pick ").strip()
            completions = [
                text + name.removeprefix(entity_name).strip() + ' '
                for name, entity in self.player.seen_entities.items()
                if name.startswith(entity_name) and isinstance(entity, Item) and entity.carryable
            ]
            if ' ' in completions:
                completions.remove(' ')
            if not text or text.startswith("u") or text.startswith("up"):
                completions.append("up ")
            return completions
        return []

if TYPE_CHECKING:
    from .player import Player
