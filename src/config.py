import socket

MAX_CLIENTS = "10"
CLIENT_TIMEOUT = "100"
HOSTNAME = socket.gethostname()
USER_LIST = dict()

LISTEN_ADDR = "127.0.0.1"
LISTEN_PORT = "25"


def load():
    conf = open("mail.conf", "r")

    for line in conf:
        if line.strip() == str():
            continue

        pair = line.split("=")

        key = pair[0].strip()
        val = pair[1].strip()

        if key == "USERS_FILE":
            parse_users(val)
            continue

        exec(f"global {key}\n{key} = \"{val}\"")

    conf.close()


def parse_users(filename):
    users = open(filename, "r")

    for line in users:
        split = line.split(":")

        name = split[0].strip()
        mbox = split[1].strip()

        USER_LIST[name] = mbox
