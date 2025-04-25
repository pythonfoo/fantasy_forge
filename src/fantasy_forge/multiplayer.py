from argparse import ArgumentParser
from socket import AF_INET6
from socketserver import StreamRequestHandler, TCPServer, ThreadingMixIn
from threading import current_thread
from typing import Optional

from fantasy_forge.player import Player
from fantasy_forge.world import World


class FakeFile:
    """Wrap rfile or wfile to convert bytes to str and vice-versa."""

    def __init__(self, file):
        self.file = file

    def write(self, text: str):
        self.file.write(text.encode())

    def readline(self, max_length: Optional[int] = None) -> str:
        if max_length is not None:
            text = self.file.readline(max_length)
        else:
            text = self.file.readline()
        return text.decode()

    def flush(self):
        self.file.flush()


class MyTCPHandler(StreamRequestHandler):
    def handle(self):
        rfile = FakeFile(self.rfile)
        wfile = FakeFile(self.wfile)
        while True:
            wfile.write(
                self.server.world.l10n.format_value(
                    "character-name-prompt-multiplayer", {"default_name": "Player"}
                )
                + " "
            )
            name_input = rfile.readline(10000).rstrip()
            if any(
                (
                    name_input in area.contents.keys()
                    for area in self.server.world.areas.values()
                )
            ):
                wfile.write(
                    self.server.world.l10n.format_value(
                        "character-name-taken", name=name_input
                    )
                    + " "
                )
                continue
            if name_input:
                player_name = name_input
                break
            else:
                wfile.write(
                    self.server.world.l10n.format_value("character-name-empty") + " "
                )
                continue
        player_desc = "the heroic player"
        wfile.write(
            self.server.world.l10n.format_value(
                "character-desc-prompt-multiplayer",
                {"default_description": player_desc},
            )
            + " "
        )
        desc_input = rfile.readline(10000).rstrip()
        if desc_input:
            player_desc = desc_input
        ip_adress = self.client_address[0]
        thread = current_thread().getName()
        print(f"new connection from {player_name} @ {ip_adress} on {thread}")
        self.server.world.messages.to(
            self.server.world.players, "player-join", player_name=player_name
        )
        player = Player(self.server.world, player_name, player_desc)
        player.main_loop(stdin=rfile, stdout=wfile)
        print(f"closed connection from {player_name} @ {ip_adress} on {thread}")
        self.server.world.messages.to(
            self.server.world.players, "player-quit", player_name=player_name
        )


class ThreadedTCPServer6(ThreadingMixIn, TCPServer):
    address_family = AF_INET6


def parse_args():
    parser = ArgumentParser(description="Fantasy Forge: A text-based RPG")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    parser.add_argument("--world", help="The world to play in", default="chaosdorf")
    parser.add_argument("--host", help="The address to bind to", default="::")
    parser.add_argument("--port", help="The port to bind to", default=9999, type=int)
    return parser.parse_args()


def main():
    args = parse_args()

    # first, create the world
    world = World.load(args.world)

    # Create the server, binding to localhost on port 9999
    with ThreadedTCPServer6((args.host, args.port), MyTCPHandler) as server:
        server.world = world
        print(f"Serving {args.world} on [{args.host}]:{args.port}")
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
