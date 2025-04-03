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
        wfile.write(
            self.server.world.l10n.format_value(
                "character-name-prompt", {"default": "Player"}
            )
            + " "
        )
        name_input = rfile.readline(10000).rstrip()
        if name_input:
            player_name = name_input
        else:
            player_name = "Player"
        ip_adress = self.client_address[0]
        thread = current_thread().getName()
        print(f"new connection from {player_name} @ {ip_adress} on {thread}")
        player = Player(self.server.world, player_name)
        player.main_loop(stdin=rfile, stdout=wfile)


class ThreadedTCPServer6(ThreadingMixIn, TCPServer):
    address_family = AF_INET6


def main():
    HOST, PORT = "::", 9998
    WORLD = "chaosdorf"
    # TODO: argparse

    # first, create the world
    world = World.load(WORLD)

    # Create the server, binding to localhost on port 9999
    with ThreadedTCPServer6((HOST, PORT), MyTCPHandler) as server:
        server.world = world
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
