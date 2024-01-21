import re
import socket
from time import time

import log
import reply
import config
import command
from state import State
from client import Client
from client import SocketDisconnectException
from envelope import Envelope
from relay import relay_queue
from relay import relay

client_pool = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def init():
    server.bind((config.LISTEN_ADDR, int(config.LISTEN_PORT)))
    server.setblocking(False)
    server.listen(int(config.MAX_CLIENTS))
    log.listening()


def accept():
    try:
        connection = server.accept()
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
            exec_command(client)


def exec_command(client):
    if client.state == State.DATA:
        client.recv_data()
        return
    else:
        log.command_issued(client)

    if re.match(r"^HELO \S+[\r\n]$", client.buffer):
        command.helo(client)
        return

    if re.match(r"^MAIL FROM:<(\S|)+>[\r\n]$", client.buffer):
        command.mail(client)
        return

    if re.match(r"^RCPT TO:<\S+>[\r\n]$", client.buffer):
        command.rcpt(client)
        return

    if re.match(r"^DATA[\r\n]$", client.buffer):
        command.data(client)
        return

    if re.match(r"^RSET[\r\n]$", client.buffer):
        command.rset(client)
        return

    if re.match(r"^NOOP[\r\n]$", client.buffer):
        command.noop(client)
        return

    if re.match(r"^QUIT[\r\n]$", client.buffer):
        command.quit(client, client_pool)
        return

    reply.invalid_command(client)
    client.buffer = str()


def main():
    envelope = Envelope()
    envelope.reverse_path = "barbo@err0r.cz"
    envelope.forward_path.append("barborikadam@gmail.com")
    envelope.data = "From: Test Test <barbo@err0r.cz>\r\nTo: Adam Barborik <barborikadam@gmail.com>\r\nSubject: Saying Hello\r\n\r\nAhoj, jak se vede!\r\n"

    relay_queue.append(envelope)
    relay()

    exit(0)

    log.starting()
    config.load()
    init()
    while True:
        accept()
        receive()


if __name__ == "__main__":
    main()
