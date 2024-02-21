import socket
from time import time

import log
import config
import reply
import command
from client import Client
from client import SocketDisconnectException


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
Listen socket for receiving email, non-blocking.
"""

client_pool = []
"""
List of connected clients, the server receives at most one byte from each every iteration of the main loop.
"""


def init():
    """
    Initializes the server socket.
    """

    server_socket.bind((config.LISTEN_ADDR, int(config.LISTEN_PORT)))
    server_socket.setblocking(False)
    server_socket.listen(int(config.MAX_CLIENTS))
    log.listening()


def accept():
    """
    Accepts new connections and adds them to the connection pool.
    """

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
    """
    Wrapper for client.recv_char() to handle blocking I/O, disconnects and command execution for every client in the connection pool.
    """

    for client in client_pool.copy():

        # check if we didn't disconnect the client before
        if client.socket.fileno() == -1:
            client_pool.remove(client)
            continue

        # time out client
        if time() > client.timeout:
            log.timeout(client)
            client.socket.close()

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
