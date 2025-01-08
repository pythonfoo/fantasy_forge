from __future__ import annotations

import logging
from cmd import Cmd
from typing import TYPE_CHECKING

import fuzzywuzzy.process

from fantasy_forge.armour import Armour
from fantasy_forge.character import Character
from fantasy_forge.gateway import Gateway
from fantasy_forge.item import Item
from fantasy_forge.weapon import Weapon

logger = logging.getLogger(__name__)


class Shell(Cmd):
    """Base class for the Cmd shell"""

    player: Player
    prompt = "> "

    def __new__(cls, player: Player) -> Shell:
        match player.l10n.locales[0]:
            case "en":
                shell_type = ShellEn
            case default:
                raise RuntimeError(
                    player.l10n.format_value(
                        "unknown-language-error",
                        {
                            "language": default,
                        },
                    )
                )
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
        return [name + " " for name in super().completenames(text, *ignored)]

    def default(self, line: str):
        if len(line) < 3:
            """Display an error message, because the command was invalid."""
            print(self.player.l10n.format_value("shell-invalid-command"))

        else:
            """Check for potential typos and recommend closest command"""
            commands = [x[3:] for x in self.get_names() if x.startswith("do_")]
            possibilities = fuzzywuzzy.process.extract(line, commands)
            closest_cmd, closest_ratio = possibilities[0]
            print(
                self.player.l10n.format_value("shell-invalid-command"),
                f"Did you mean '{closest_cmd}'?",
            )

    def do_EOF(self, arg: str) -> bool:
        """This is called if an EOF occurs while parsing the command."""
        return True


class ShellEn(Shell):
    def do_quit(self, arg: str) -> bool:
        """Quits the shell."""
        return self.do_EOF(arg)

    def do_exit(self, arg: str) -> bool:
        """Quits the shell."""
        return self.do_EOF(arg)

    def do_look(self, arg: str):
        """look around
        look at <entity>
        """
        if arg.strip() == "around":
            self.player.look_around()
            logger.debug("%s looks around", elf.player.name)
        elif arg.strip().startswith("at"):
            entity_name = arg.strip().removeprefix("at").strip()
            self.player.look_at(entity_name)
            logger.debug("%s looks at %s", self.player.name, entity_name)
        else:
            self.default(arg)

    def complete_look(
        self,
        text: str,
        line: str,
        begidx: int,
        endidx: int,
    ):
        if line.startswith("look at "):
            entity_name = line.removeprefix("look at ").strip()
            completions = [
                text + name.removeprefix(entity_name).strip() + " "
                for name in self.player.seen_entities.keys()
                if name.startswith(entity_name)
            ]
            if " " in completions:
                completions.remove(" ")
            return completions
        if line.startswith("look around "):
            return []
        if line.startswith("look "):
            return [verb for verb in ["at ", "around "] if verb.startswith(text)]
        return []

    def do_pick(self, arg: str):
        """pick [up] <entity>"""
        if arg.startswith("up "):
            arg = arg.removeprefix("up ")
        self.player.pick_up(arg.strip())
        logger.debug("%s picks up %s", self.player.name, arg.strip())

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
        logger.debug("%s goes to %s", self.player.name, arg)

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
        print(self.player.inventory.on_look())

    def do_armour(self, arg: str):
        """shows the players armour"""
        for armour_type, armour_item in self.player.armour_slots.items():
            print(
                self.player.l10n.format_value(
                    "armour-detail",
                    {
                        "type": armour_type,
                        "item": armour_item,
                        "item-name": getattr(armour_item, "name", None),
                        "item-defense": getattr(armour_item, "defense", None),
                    },
                )
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

    def do_drop(self, arg: str) -> None:
        """
        drop <item>

        drops item from main hand or inventory
        """
        self.player.drop(arg)


if TYPE_CHECKING:
    from fantasy_forge.player import Player
