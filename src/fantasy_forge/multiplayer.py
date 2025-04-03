from socket import AF_INET6
from socketserver import StreamRequestHandler, TCPServer


class MyTCPHandler(StreamRequestHandler):
    def handle(self):
        self.data = self.rfile.readline(10000).rstrip()
        print(f"{self.client_address[0]} wrote:")
        print(self.data.decode("utf-8"))
        self.wfile.write(self.data)


class TCPServer6(TCPServer):
    address_family = AF_INET6


def main():
    HOST, PORT = "::", 9999

    # Create the server, binding to localhost on port 9999
    with TCPServer6((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
