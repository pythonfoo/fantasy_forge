from socket import AF_INET6
from socketserver import StreamRequestHandler, TCPServer, ThreadingMixIn
from threading import current_thread

from fantasy_forge.player import Player
from fantasy_forge.world import World


class MyTCPHandler(StreamRequestHandler):
    def handle(self):
        self.wfile.write(
            self.server.world.l10n.format_value(
                "character-name-prompt", {"default": "Player"}
            ).encode()
            + b" "
        )
        name_input = self.rfile.readline(10000).rstrip().decode()
        if name_input:
            player_name = name_input
        else:
            player_name = "Player"
        ip_adress = self.client_address[0]
        thread = current_thread().getName()
        print(f"new connection from {player_name} @ {ip_adress} on {thread}")
        player = Player(self.server.world, player_name)
        while True:
            pass


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
