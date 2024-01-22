import socket

import log
import config

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_pool = []


def init():
    server_socket.bind((config.LISTEN_ADDR, int(config.LISTEN_PORT)))
    server_socket.setblocking(False)
    server_socket.listen(int(config.MAX_CLIENTS))
    log.listening()
