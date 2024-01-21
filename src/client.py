from time import time

import reply
import config
from state import State


class SocketDisconnectException(Exception):
    pass


class Client:
    def recv_char(self):
        data = self.socket.recv(1)

        if not data:
            raise SocketDisconnectException()

        char = data.decode("ascii")
        self.buffer += char
        return char

    def recv_data(self):
        # transfer done
        if self.buffer.strip() == ".":
            self.state = State.IDENTIFIED
            reply.action_success(self)

            self.buffer = str()
            self.envelope.process()
            return

        # remove leading dot
        if self.buffer[0] == ".":
            self.buffer = self.buffer[1:]

        self.envelope.data += self.buffer.strip() + "\n"
        self.buffer = str()

    def send(self, string):
        data = string.encode("ascii")
        self.socket.send(data)

    def reset_timeout(self):
        self.timeout = time() + int(config.CLIENT_TIMEOUT)

    def __init__(self, sock, addr, port):
        self.socket = sock
        self.address = addr
        self.port = port
        self.buffer = str()
        self.state = State.UNIDENTIFIED
        self.timeout = time() + int(config.CLIENT_TIMEOUT)
        self.hostname = None
        self.envelope = None
