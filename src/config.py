import os
import socket

RELAY_PORT = "25"

LISTEN_ADDR = "127.0.0.1"
LISTEN_PORT = "25"

MAX_CLIENTS = "10"
CLIENT_TIMEOUT = "100"
HOSTNAME = socket.gethostname()
USER_LIST = dict()


def load(mail_conf, user_conf):
    parse_users(user_conf)
    conf = open(mail_conf, "r")

    for line in conf:
        if line.strip() == str():
            continue

        pair = line.split("=")

        key = pair[0].strip()
        val = pair[1].strip()

        exec(f"global {key}\n{key} = \"{val}\"")

    conf.close()


def parse_users(user_conf):
    users = open(user_conf, "r")

    for line in users:
        split = line.split(":")

        name = split[0].strip()
        mbox = split[1].strip()

        if not os.path.exists(mbox):
            os.makedirs(mbox)

        USER_LIST[name] = mbox

    users.close()
