from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from fluent.runtime import FluentLocalization


class Messages:
    """
    A utility class to send messages to a single or multiple players – or
    even to a whole area. This is mostly useful for multi-player mode.
    """

    l10n: FluentLocalization

    def __init__(self: Self, l10n: FluentLocalization):
        self.l10n = l10n

    def to(
        self: Self,
        receivers: list[Character],
        message_id: str,
        **parameters: Any,
    ):
        from fantasy_forge.player import Player

        localized = self.l10n.format_value(message_id, parameters)
        for receiver in receivers:
            if not isinstance(receiver, Player):
                # only deliver messages to actual players
                continue
            receiver.shell.stdout.write(localized + "\n")


if TYPE_CHECKING:
    from fantasy_forge.player import Character
