from time import time

import log
import reply
import server
import config
import command
from state import State
from server import server_socket
from server import client_pool


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


def accept():
    try:
        connection = server_socket.accept()
    except BlockingIOError:
        return

    sock = connection[0]
    addr = connection[1][0]
    port = connection[1][1]

    sock.setblocking(False)
    client = Client(sock, addr, port)

    if len(client_pool) == int(config.MAX_CLIENTS):
        reply.service_busy(client)
        return

    client_pool.append(client)
    reply.service_ready(client)
    log.accepted(client)


def receive():
    for client in client_pool.copy():

        # time out client
        if time() > client.timeout:
            log.timeout(client)
            client_pool.remove(client)

        # fetch an ascii character from the data stream
        try:
            char = client.recv_char()
        except BlockingIOError:
            continue
        except UnicodeDecodeError:
            continue
        except SocketDisconnectException:
            log.terminated(client)
            client_pool.remove(client)
            continue

        # command issued
        if char == "\n":
            client.reset_timeout()
            command.exec_command(client)
