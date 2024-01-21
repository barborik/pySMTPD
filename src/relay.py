import socket

import config
from state import State

relay_queue = []
relay_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def relay():
    envelope = relay_queue[0]

    address = envelope.forward_path[0].split("@")[1]
    relay_socket.connect(("err0r.cz", 25))
    print(relay_socket.recv(512))

    relay_socket.send(f"HELO {config.HOSTNAME}\r\n".encode("ascii"))
    print(relay_socket.recv(512))

    relay_socket.send(f"MAIL FROM:<{envelope.reverse_path}>\r\n".encode("ascii"))
    print(relay_socket.recv(512))

    for mailbox in envelope.forward_path:
        relay_socket.send(f"RCPT TO:<{mailbox}>\r\n".encode("ascii"))
        print(relay_socket.recv(512))

    relay_socket.send(f"DATA\r\n".encode("ascii"))
    print(relay_socket.recv(512))

    relay_socket.send(envelope.data.encode("ascii"))
    relay_socket.send("\r\n.\r\n".encode("ascii"))
    print(relay_socket.recv(512))
    relay_socket.close()
