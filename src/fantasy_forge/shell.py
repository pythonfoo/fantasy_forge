from __future__ import annotations

import logging
from cmd import Cmd
from typing import TYPE_CHECKING

import fuzzywuzzy.process

from fantasy_forge.armour import Armour
from fantasy_forge.character import Character
from fantasy_forge.gateway import Gateway
from fantasy_forge.item import Item
from fantasy_forge.messages import Messages
from fantasy_forge.weapon import Weapon

logger = logging.getLogger(__name__)


class Shell(Cmd):
    """Base class for the Cmd shell"""

    player: Player
    messages: Messages
    prompt = "> "

    def __new__(
        cls, messages: Messages, player: Player, stdin=None, stdout=None
    ) -> Shell:
        match messages.l10n.locales[0]:
            case "en":
                shell_type = ShellEn
            case default:
                raise RuntimeError(
                    messages.l10n.format_value(
                        "unknown-language-error",
                        {
                            "language": default,
                        },
                    )
                )
        shell = super().__new__(shell_type)
        return shell

    def __init__(self, messages: Messages, player: Player, stdin=None, stdout=None):
        super().__init__(stdin=stdin, stdout=stdout)
        if stdin is not None:
            assert stdout is not None
            self.use_rawinput = False
        self.player = player
        self.messages = messages

    def completenames(self, text, *ignored):
        """This is called when completing the command itself.

        This is uses the stdlib's Cmd, but adds a space after every command,
        so that the user doesn't have to enter it manually.
        """
        return [name + " " for name in super().completenames(text, *ignored)]

    def default(self, line: str):
        if len(line) < 3:
            """Display an error message, because the command was invalid."""
            self.stdout.write(self.messages.l10n.format_value("shell-invalid-command"))

        else:
            """Check for potential typos and recommend closest command"""
            commands = [x[3:] for x in self.get_names() if x.startswith("do_")]
            possibilities = fuzzywuzzy.process.extract(line, commands)
            closest_cmd, closest_ratio = possibilities[0]
            self.stdout.write(
                self.messages.l10n.format_value(
                    "shell-invalid-command-suggest", {"closest_cmd": closest_cmd}
                )
            )

    def do_EOF(self, arg: str) -> bool:
        """This is called if an EOF occures while parsing the command."""
        return True


class ShellEn(Shell):
    def do_quit(self, arg: str) -> bool:
        """Quits the shell."""
        return self.do_EOF(arg)

    def do_exit(self, arg: str) -> bool:
        """Quits the shell."""
        return self.do_EOF(arg)

    def do_inspect(self, arg: str):
        """inspect entity
        inspect <entity>
        """
        entity_name = arg.strip()
        self.player.inspect(entity_name)
        logger.debug("%s looks at %s" % (self.player.name, entity_name))

    def complete_inspect(
        self,
        text: str,
        line: str,
        begidx: int,
        endidx: int,
    ):
        if line.startswith("inspect "):
            entity_name = line.removeprefix("inspect ").strip()
            completions = [
                text + name.removeprefix(entity_name).strip() + " "
                for name in self.player.seen_entities.keys()
                if name.startswith(entity_name)
            ]
            if " " in completions:
                completions.remove(" ")
            return completions

    def do_look(self, arg: str):
        """look around
        look around <entity>
        """
        if arg.strip() == "around":
            self.player.look_around()
            logger.debug("%s looks around" % self.player.name)
        else:
            self.default(arg)

    def complete_look(
        self,
        text: str,
        line: str,
        begidx: int,
        endidx: int,
    ):
        if line.startswith("look "):
            return ["around"]
        if line.startswith("look around "):
            return []
        return []

    def do_pick(self, arg: str):
        """pick [up] <entity>"""
        if arg.startswith("up "):
            arg = arg.removeprefix("up ")
        self.player.pick_up(arg.strip())
        logger.debug("%s picks up %s" % (self.player.name, arg.strip()))

    def complete_pick(
        self,
        text: str,
        line: str,
        begidx: int,
        endidx: int,
    ):
        if line.startswith("pick up "):
            entity_name = line.removeprefix("pick up ").strip()
            completions = [
                text + name.removeprefix(entity_name).strip() + " "
                for name, entity in self.player.seen_entities.items()
                if name.startswith(entity_name)
                and isinstance(entity, Item)
                and entity.carryable
            ]
            if " " in completions:
                completions.remove(" ")
            return completions
        if line.startswith("pick "):
            entity_name = line.removeprefix("pick ").strip()
            completions = [
                text + name.removeprefix(entity_name).strip() + " "
                for name, entity in self.player.seen_entities.items()
                if name.startswith(entity_name)
                and isinstance(entity, Item)
                and entity.carryable
            ]
            if " " in completions:
                completions.remove(" ")
            if not text or text.startswith("u") or text.startswith("up"):
                completions.append("up ")
            return completions
        return []

    def do_go(self, arg: str):
        """go <gateway>"""
        self.player.go(arg)
        logger.debug("%s goes to %s" % (self.player.name, arg))

    def complete_go(
        self,
        text: str,
        line: str,
        begidx: int,
        endidx: int,
    ):
        entity_name = line.removeprefix("go ").strip()
        completions = [
            text + name.removeprefix(entity_name).strip() + " "
            for name, entity in self.player.seen_entities.items()
            if name.startswith(entity_name) and isinstance(entity, Gateway)
        ]
        if " " in completions:
            completions.remove(" ")
        return completions

    def do_inventory(self, arg: str):
        """shows the contents of the players inventory"""
        self.messages.to([self.player], self.player.inventory.on_look())

    def do_armour(self, arg: str):
        """shows the players armour"""
        for armour_type, armour_item in self.player.armour_slots.items():
            self.messages.to(
                [self.player],
                "armour-detail",
                type=armour_type,
                item=armour_item,
                item_name=getattr(armour_item, "name", None),
                item_defense=getattr(armour_item, "defense", None),
            )

    def do_use(self, arg: str):
        """
        use <subject> [with <other>]
        """
        if "with" in arg:
            subject, other = arg.split("with")
            self.player.use(subject.strip(), other.strip())
            logger.debug(
                "%(player)s uses %(subject)s with %(other)s",
                {"player": self.player.name, "subject": subject, "other": other},
            )
        else:
            subject = arg.strip()
            self.player.use(subject)
            logger.debug(
                "%(player)s uses %(subject)s",
                {"player": self.player.name, "subject": subject},
            )

    def complete_use(
        self,
        text: str,
        line: str,
        begidx: int,
        endidx: int,
    ) -> list[str]:
        args = line.split(" ")
        assert args[0] == "use"
        del args[0]
        if "with" in args:
            # we're looking for the object
            with_index = args.index("with")
            object_name = " ".join(args[with_index + 1 :])
            subject_name = " ".join(args[:with_index])
            completions = [
                text + name.removeprefix(object_name).strip() + " "
                for name in self.player.seen_entities.keys()
                if name.startswith(object_name) and name != subject_name
            ]
            if " " in completions:
                completions.remove(" ")
            return completions
        else:
            # we're looking for the subject
            subject_name = " ".join(args).strip()
            completions = [
                text + name.removeprefix(subject_name).strip() + " "
                for name in self.player.seen_entities.keys()
                if name.startswith(subject_name)
            ]
            if " " in completions:
                completions.remove(" ")
            # we might already be in the "with"
            if any(
                (
                    entity_name == subject_name.rstrip("ihtw").strip()
                    for entity_name in self.player.seen_entities
                )
            ):
                completions.append("with ")
            return completions

    def do_attack(self, arg: str) -> None:
        """Attack another entity."""
        self.player.attack(arg)

    def complete_attack(
        self,
        text: str,
        line: str,
        begidx: int,
        endidx: int,
    ) -> list[str]:
        target = line.removeprefix("attack ").strip()
        completions = [
            text + name.removeprefix(target).strip() + " "
            for name, entity in self.player.seen_entities.items()
            if name.startswith(target) and isinstance(entity, Character)
        ]
        if " " in completions:
            completions.remove(" ")
        return completions

    def do_equip(self, arg: str) -> None:
        """Take an item out of the inventory and put it on."""
        self.player.equip(arg)

    def complete_equip(
        self,
        text: str,
        line: str,
        begidx: int,
        endidx: int,
    ) -> list[str]:
        item = line.removeprefix("equip ").strip()
        completions = [
            text + name.removeprefix(item).strip() + " "
            for name, entity in self.player.seen_entities.items()
            if name.startswith(item) and isinstance(entity, (Weapon, Armour))
        ]
        if " " in completions:
            completions.remove(" ")
        return completions

    def do_unequip(self, arg: str) -> None:
        """Unequips item or armour."""
        self.player.unequip(arg)

    def complete_unequip(
        self,
        text: str,
        line: str,
        begidx: int,
        endidx: int,
    ) -> list[str]:
        item = line.removeprefix("unequip ").strip()
        equipped_items = [self.player.main_hand] + list(self.player.armour_slots.values())
        
        completions = [
            text + entity.name.removeprefix(item).strip() + " "
            for entity in equipped_items
            if entity is not None and entity.name.startswith(item)
        ]
        if " " in completions:
            completions.remove(" ")
        return completions

    def do_drop(self, arg: str) -> None:
        """
        drop <item>

        drops item from main hand or inventory
        """
        self.player.drop(arg)

    def complete_drop(
        self,
        text: str,
        line: str,
        begidx: int,
        endidx: int,
    ) -> list[str]:
        item = line.removeprefix("drop ").strip()
        
        completions = [
            text + entity.name.removeprefix(item).strip() + " "
            for entity in self.player.inventory
            if entity.name.startswith(item)
        ]
        if " " in completions:
            completions.remove(" ")
        return completions

    def do_shout(self, arg: str) -> None:
        self.player.shout(arg)

    def do_say(self, arg: str) -> None:
        self.player.say(arg)

    def do_whisper(self, arg: str) -> None:
        fragments = []
        for player_fragment in arg.split(" "):
            fragments.append(player_fragment)
            target = " ".join(fragments)
            if len(arg.split(" ")) < 1 + len(target.split(" ")):
                self.messages.to([self.player], "whisper-invalid")
                return
            if target in self.player.area.contents:
                message = arg.removeprefix(target + " ")
                self.player.whisper(target, message)
                return
        self.messages.to([self.player], "whisper-invalid")
        return


if TYPE_CHECKING:
    from fantasy_forge.player import Player
