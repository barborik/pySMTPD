import os
import socket

__MAIL_CONF = "conf/mail.conf"
__USER_CONF = "conf/user.conf"


LISTEN_ADDR = "127.0.0.1"
LISTEN_PORT = "25"

MAX_CLIENTS = "10"
CLIENT_TIMEOUT = "100"
HOSTNAME = socket.gethostname()
USER_LIST = dict()


def load():
    parse_users()
    conf = open(__MAIL_CONF, "r")

    for line in conf:
        if line.strip() == str():
            continue

        pair = line.split("=")

        key = pair[0].strip()
        val = pair[1].strip()

        exec(f"global {key}\n{key} = \"{val}\"")

    conf.close()


def parse_users():
    users = open(__USER_CONF, "r")

    for line in users:
        split = line.split(":")

        name = split[0].strip()
        mbox = split[1].strip()

        if not os.path.exists(mbox):
            os.makedirs(mbox)

        USER_LIST[name] = mbox

    users.close()
